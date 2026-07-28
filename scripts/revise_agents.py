#!/usr/bin/env python3
"""Create Codex custom agents and portable role definitions from upstream."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from migrate_from_claude import SOURCE_COMMIT, parse_frontmatter
from migrate_shared_resources import portable_text


WORKSPACE_WRITE = {
    "beamer-translator",
    "quarto-fixer",
    "r-package-reviewer",
    "verifier",
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def reasoning_effort(metadata: dict[str, str]) -> str:
    explicit = metadata.get("effort", "").lower()
    if explicit in {"low", "medium", "high", "xhigh"}:
        return explicit
    source_model = metadata.get("model", "").lower()
    if source_model == "haiku":
        return "low"
    if source_model == "opus":
        return "high"
    return "medium"


def role_contract(source_name: str, sandbox: str) -> str:
    mutation = (
        "Editing and verification writes are permitted only inside the "
        "assigned workspace scope."
        if sandbox == "workspace-write"
        else "Remain read-only; return proposed changes to the parent agent."
    )
    independence = (
        "For an independence-sensitive review, accept only the extracted "
        "claims/questions and source pointers specified by the parent; do not "
        "request the original draft."
        if source_name == "claim-verifier"
        else "Do not self-confirm work you produced; base findings on fresh "
        "inspection and concrete evidence."
    )
    return (
        "## Codex role contract\n\n"
        f"- {mutation}\n"
        f"- {independence}\n"
        "- Treat missing tools, inaccessible sources, and skipped checks as "
        "UNVERIFIED rather than PASS.\n"
        "- Keep findings within this role's scope and return them to the "
        "parent for synthesis.\n"
        "- Do not commit, push, deploy, submit, send, or publish externally.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    target = args.target.resolve()
    skill_names = sorted(
        path.parent.name
        for path in (source / ".claude" / "skills").glob("*/SKILL.md")
    )
    source_agents = sorted((source / ".claude" / "agents").glob("*.md"))
    if len(source_agents) != 18:
        raise SystemExit(
            f"expected 18 source agents, found {len(source_agents)}"
        )

    records: list[dict[str, str]] = []
    map_rows = [
        "# Agent portability map",
        "",
        "| Upstream role | Codex custom agent | Sandbox | Status |",
        "| --- | --- | --- | --- |",
    ]
    role_root = target / "references" / "agent-roles"
    toml_root = target / ".codex" / "agents"
    role_root.mkdir(parents=True, exist_ok=True)
    toml_root.mkdir(parents=True, exist_ok=True)

    for source_file in source_agents:
        source_text = source_file.read_text(
            encoding="utf-8", errors="replace"
        )
        metadata, body = parse_frontmatter(source_text)
        source_name = metadata.get("name", source_file.stem)
        native_name = source_name.replace("-", "_")
        sandbox = (
            "workspace-write"
            if source_name in WORKSPACE_WRITE
            else "read-only"
        )
        description = portable_text(
            metadata.get("description", f"Academic role for {source_name}."),
            skill_names,
        )
        adapted_body = portable_text(body, skill_names)
        adapted_body = adapted_body.replace(
            "](../skills/", "](../../skills/"
        )
        adapted_body = adapted_body.replace("](../agents/", "](")
        adapted_body = adapted_body.replace(
            "](../references/", "](../"
        )
        adapted_body = adapted_body.replace(
            "Sonnet 4 / original Opus 4 after 2026-06-15",
            "a retired or unavailable model alias",
        )
        provenance = (
            f"<!-- Adapted from .claude/agents/{source_file.name} at "
            f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->"
        )
        role_text = (
            f"{provenance}\n\n# {source_name} role\n\n"
            f"{role_contract(source_name, sandbox)}\n"
            f"{adapted_body.lstrip()}"
        ).rstrip() + "\n"
        role_file = role_root / source_file.name
        role_file.write_text(role_text, encoding="utf-8")

        effort = reasoning_effort(metadata)
        developer = (
            "Resolve the repository root, then read and follow "
            f"`references/agent-roles/{source_name}.md` completely. "
            "Stay within that narrow role, cite concrete evidence, "
            "distinguish PASS, FAIL, and UNVERIFIED, and return findings to "
            "the parent. Do not expand scope or perform external actions."
        )
        toml_text = (
            f"name = {json.dumps(native_name, ensure_ascii=False)}\n"
            f"description = {json.dumps(description, ensure_ascii=False)}\n"
            f"model_reasoning_effort = {json.dumps(effort)}\n"
            f"sandbox_mode = {json.dumps(sandbox)}\n"
            "developer_instructions = "
            f"{json.dumps(developer, ensure_ascii=False)}\n"
        )
        toml_file = toml_root / f"{source_name}.toml"
        toml_file.write_text(toml_text, encoding="utf-8")
        map_rows.append(
            f"| `{source_name}` | `{native_name}` | `{sandbox}` | "
            "`semantic-baseline` |"
        )
        records.append(
            {
                "kind": "agent",
                "name": source_name,
                "native_name": native_name,
                "source": str(source_file),
                "source_sha256": digest(source_text),
                "role_target": str(role_file),
                "role_target_sha256": digest(role_text),
                "toml_target": str(toml_file),
                "toml_target_sha256": digest(toml_text),
                "status": "semantic-baseline",
            }
        )

    map_file = target / "docs" / "conversion" / "AGENT_MAP.md"
    map_file.write_text("\n".join(map_rows) + "\n", encoding="utf-8")
    manifest_file = (
        target / "docs" / "conversion" / "SOURCE_MANIFEST.json"
    )
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest["components"] = [
        item
        for item in manifest["components"]
        if item.get("kind") != "agent"
    ] + records
    manifest_file.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Revised {len(records)} Codex agents and portable roles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
