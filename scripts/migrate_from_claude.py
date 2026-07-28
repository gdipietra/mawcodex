#!/usr/bin/env python3
"""Create an auditable mechanical baseline from the fixed upstream clone.

This script intentionally performs only deterministic transformations.
Every generated skill remains in ``mechanical-baseline`` status until a
semantic reviewer reconciles the workflow with current Codex behavior.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import textwrap
from pathlib import Path


SOURCE_COMMIT = "be53c12f235996dff41fb7f21580506fd2dd8d50"
EDITING_AGENTS = {"beamer-translator", "quarto-fixer"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}, normalized
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    block = normalized[4:end]
    body = normalized[end + 5 :]
    lines = block.splitlines()
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            index += 1
            continue
        key, raw = match.groups()
        if raw in {"|", ">"}:
            collected: list[str] = []
            index += 1
            while index < len(lines) and (
                not lines[index].strip() or lines[index].startswith((" ", "\t"))
            ):
                collected.append(lines[index].lstrip())
                index += 1
            values[key] = " ".join(
                part.strip() for part in collected if part.strip()
            )
            continue
        values[key] = raw.strip().strip("\"'")
        index += 1
    return values, body


def replace_slash_invocations(text: str, skill_names: list[str]) -> str:
    for skill_name in sorted(skill_names, key=len, reverse=True):
        pattern = rf"(?<![\w.$`])/{re.escape(skill_name)}\b"
        text = re.sub(pattern, f"${skill_name}", text)
    return text


def adapt_text(text: str, skill_names: list[str]) -> tuple[str, list[str]]:
    changes: list[str] = []
    replacements = [
        ("CLAUDE.MD", "AGENTS.md", "instruction filename"),
        ("CLAUDE.md", "AGENTS.md", "instruction filename"),
        (".claude/agents/", ".codex/agents/", "agent path"),
        (".claude/rules/", "references/rules/", "rule path"),
        (".claude/hooks/", "hooks/", "hook path"),
        (".claude/state/", ".codex/state/", "state path"),
        (".claude/scripts/", "scripts/", "script path"),
        ("Claude Code", "Codex", "runtime name"),
        ("Claude", "Codex", "runtime name"),
        ("WebSearch", "web search", "capability name"),
        ("WebFetch", "web retrieval", "capability name"),
        ("Task tool", "subagent workflow", "subagent capability"),
        ("Task agents", "subagents", "subagent capability"),
        ("Task agent", "subagent", "subagent capability"),
        ("context: fork", "isolated context", "context isolation"),
        ("context=fork", "isolated-context=true", "context isolation"),
        ("model: opus", "reasoning: high", "model routing"),
        ("model: sonnet", "reasoning: medium", "model routing"),
        ("model: haiku", "reasoning: low", "model routing"),
    ]
    for old, new, label in replacements:
        if old in text:
            text = text.replace(old, new)
            changes.append(label)
    slash_adapted = replace_slash_invocations(text, skill_names)
    if slash_adapted != text:
        changes.append("skill invocation syntax")
        text = slash_adapted
    task_adapted = re.sub(
        r"\bTask:\s*subagent_type=([a-z0-9-]+)",
        lambda match: f"Subagent: role={match.group(1).replace('-', '_')}",
        text,
    )
    task_adapted = re.sub(
        r"\bTask\(\s*subagent_type\s*=\s*([a-z0-9-]+)",
        lambda match: (
            "Spawn a bounded subagent "
            f"(role={match.group(1).replace('-', '_')}"
        ),
        task_adapted,
    )
    if task_adapted != text:
        changes.append("subagent invocation syntax")
    return task_adapted, sorted(set(changes))


def write_skill(
    source_file: Path,
    target_file: Path,
    log_file: Path,
    skill_names: list[str],
) -> dict[str, str]:
    source_text = source_file.read_text(encoding="utf-8", errors="replace")
    metadata, body = parse_frontmatter(source_text)
    name = metadata.get("name", source_file.parent.name)
    description = metadata.get(
        "description", f"Run the {name} academic workflow."
    )
    description, description_changes = adapt_text(description, skill_names)
    body, body_changes = adapt_text(body, skill_names)
    contract = textwrap.dedent(
        """
        ## Codex execution contract

        - Treat the user's request and applicable `AGENTS.md` files as authoritative.
        - Resolve referenced resources relative to this skill first.
        - Use bounded, isolated subagents for independent review roles; when a
          project custom agent is unavailable, use the matching portable role in
          `../../references/agent-roles/`.
        - Treat missing tools, inaccessible sources, and skipped checks as
          UNVERIFIED rather than PASS.
        - Require explicit user authorization for commit, push, merge, deploy,
          submission, sending, or other external publication.
        """
    ).strip()
    target_text = (
        "---\n"
        f"name: {name}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n\n"
        f"{contract}\n\n"
        f"{body.lstrip()}"
    )
    target_text = target_text.rstrip() + "\n"
    target_file.write_text(target_text, encoding="utf-8")
    all_changes = sorted(set(description_changes + body_changes))
    record = textwrap.dedent(
        f"""
        # `{name}` conversion

        - Status: `mechanical-baseline`
        - Classification: `native rewrite`
        - Source: `.claude/skills/{name}/SKILL.md`
        - Source commit: `{SOURCE_COMMIT}`
        - Source SHA-256: `{sha256_text(source_text)}`
        - Target: `skills/{name}/SKILL.md`
        - Target SHA-256 after baseline: `{sha256_text(target_text)}`
        - Mechanical changes: {", ".join(all_changes) if all_changes else "frontmatter normalization only"}

        ## Preserved intent

        The source trigger intent, workflow body, outputs, and quality gates were
        retained as the semantic-review baseline.

        ## Required semantic review

        Reconcile tool capabilities, named-agent orchestration, context isolation,
        project paths, failure semantics, current-source requirements, and external
        action boundaries. Record material changes here and replace the status only
        after validation and a representative forward test where required.
        """
    ).lstrip()
    log_file.write_text(record, encoding="utf-8")
    return {
        "kind": "skill",
        "name": name,
        "source": str(source_file),
        "source_sha256": sha256_text(source_text),
        "target": str(target_file),
        "target_sha256": sha256_text(target_text),
        "status": "mechanical-baseline",
    }


def write_rule(
    source_file: Path,
    target_file: Path,
    skill_names: list[str],
) -> dict[str, str]:
    source_text = source_file.read_text(encoding="utf-8", errors="replace")
    adapted, _ = adapt_text(source_text, skill_names)
    provenance = (
        f"<!-- Adapted from {source_file.as_posix()} at {SOURCE_COMMIT}; "
        f"source SHA-256 {sha256_text(source_text)}. -->\n\n"
    )
    target_text = (provenance + adapted.lstrip()).rstrip() + "\n"
    target_file.write_text(target_text, encoding="utf-8")
    return {
        "kind": "rule",
        "name": source_file.stem,
        "source": str(source_file),
        "source_sha256": sha256_text(source_text),
        "target": str(target_file),
        "target_sha256": sha256_text(target_text),
        "status": "mechanical-baseline",
    }


def write_agent(
    source_file: Path,
    role_file: Path,
    toml_file: Path,
    skill_names: list[str],
) -> dict[str, str]:
    source_text = source_file.read_text(encoding="utf-8", errors="replace")
    metadata, body = parse_frontmatter(source_text)
    source_name = metadata.get("name", source_file.stem)
    native_name = source_name.replace("-", "_")
    description, _ = adapt_text(
        metadata.get("description", f"Academic role for {source_name}."),
        skill_names,
    )
    body, _ = adapt_text(body, skill_names)
    role_text = (
        f"<!-- Adapted from {source_file.as_posix()} at {SOURCE_COMMIT}; "
        f"source SHA-256 {sha256_text(source_text)}. -->\n\n"
        f"# {source_name} role\n\n"
        f"{body.lstrip()}"
    )
    role_text = role_text.rstrip() + "\n"
    role_file.write_text(role_text, encoding="utf-8")
    sandbox = (
        "workspace-write" if source_name in EDITING_AGENTS else "read-only"
    )
    source_effort = metadata.get("effort", "medium").lower()
    valid_efforts = {"low", "medium", "high", "xhigh"}
    effort = source_effort if source_effort in valid_efforts else "medium"
    developer = (
        "Follow the portable role definition at "
        f"references/agent-roles/{source_name}.md. "
        "Stay within that narrow role, cite concrete evidence, distinguish "
        "PASS, FAIL, and UNVERIFIED, and return findings to the parent agent. "
        "Do not expand scope or perform external actions."
    )
    toml_text = (
        f"name = {json.dumps(native_name, ensure_ascii=False)}\n"
        f"description = {json.dumps(description, ensure_ascii=False)}\n"
        f"model_reasoning_effort = {json.dumps(effort)}\n"
        f"sandbox_mode = {json.dumps(sandbox)}\n"
        "developer_instructions = "
        f"{json.dumps(developer, ensure_ascii=False)}\n"
    )
    toml_file.write_text(toml_text, encoding="utf-8")
    return {
        "kind": "agent",
        "name": source_name,
        "native_name": native_name,
        "source": str(source_file),
        "source_sha256": sha256_text(source_text),
        "role_target": str(role_file),
        "role_target_sha256": sha256_text(role_text),
        "toml_target": str(toml_file),
        "toml_target_sha256": sha256_text(toml_text),
        "status": "mechanical-baseline",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    target = args.target.resolve()

    source_skills = sorted(
        (source / ".claude" / "skills").glob("*/SKILL.md")
    )
    skill_names = [path.parent.name for path in source_skills]
    if len(source_skills) != 52:
        raise SystemExit(
            f"expected 52 source skills, found {len(source_skills)}"
        )

    skill_logs = target / "docs" / "conversion" / "skills"
    rules_target = target / "references" / "rules"
    roles_target = target / "references" / "agent-roles"
    agents_target = target / ".codex" / "agents"
    for directory in (
        skill_logs,
        rules_target,
        roles_target,
        agents_target,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, str]] = []
    for source_file in source_skills:
        name = source_file.parent.name
        target_file = target / "skills" / name / "SKILL.md"
        if not target_file.parent.exists():
            raise SystemExit(
                f"{target_file.parent} is missing; "
                "initialize skills with init_skill.py first"
            )
        manifest.append(
            write_skill(
                source_file,
                target_file,
                skill_logs / f"{name}.md",
                skill_names,
            )
        )

    source_rules = sorted((source / ".claude" / "rules").glob("*.md"))
    if len(source_rules) != 32:
        raise SystemExit(
            f"expected 32 source rules, found {len(source_rules)}"
        )
    for source_file in source_rules:
        manifest.append(
            write_rule(
                source_file,
                rules_target / source_file.name,
                skill_names,
            )
        )

    source_agents = sorted((source / ".claude" / "agents").glob("*.md"))
    if len(source_agents) != 18:
        raise SystemExit(
            f"expected 18 source agents, found {len(source_agents)}"
        )
    for source_file in source_agents:
        manifest.append(
            write_agent(
                source_file,
                roles_target / source_file.name,
                agents_target / f"{source_file.stem}.toml",
                skill_names,
            )
        )

    manifest_path = (
        target / "docs" / "conversion" / "SOURCE_MANIFEST.json"
    )
    manifest_path.write_text(
        json.dumps(
            {
                "source_repository": (
                    "https://github.com/pedrohcgs/"
                    "claude-code-my-workflow"
                ),
                "source_commit": SOURCE_COMMIT,
                "components": manifest,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Generated {len(source_skills)} skills, {len(source_rules)} rules, "
        f"and {len(source_agents)} agents."
    )
    print("All generated components remain in mechanical-baseline status.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
