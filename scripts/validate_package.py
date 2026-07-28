#!/usr/bin/env python3
"""Validate MAW Codex structure, portability, provenance, and release gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.parse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
BASELINE_COMMIT = "be53c12f235996dff41fb7f21580506fd2dd8d50"
EXPECTED = {
    "skill": 52,
    "agent": 18,
    "rule": 32,
    "reference": 9,
    "template": 21,
}
PACKAGED_SKILL_COUNT = 58
PACKAGED_AGENT_COUNT = 19
ALLOWED_CLASSIFICATIONS = {
    "direct port",
    "native rewrite",
    "composed replacement",
    "retained reference",
    "unsupported",
}
EXPECTED_RUNTIME_SURFACES = {
    "root-instructions",
    "settings",
    "academic-writing-output-style",
    "referee-output-style",
    "status-line",
    "workflow-quick-reference",
    "git-guardrails",
    "claim-reconcile",
    "pre-compact",
    "post-compact-restore",
    "context-monitor",
    "log-reminder",
    "notify",
}
RUNTIME_REFERENCE_COUNT = 9
ALLOWED_HOOK_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "SessionEnd",
}
REQUIRED_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PreCompact",
    "SessionStart",
}
PROVIDER_PATTERNS = {
    "legacy .claude path": re.compile(r"\.claude(?:/|\\)", re.I),
    "Claude Code runtime": re.compile(r"\bClaude Code\b", re.I),
    "Claude environment variable": re.compile(r"\bCLAUDE_[A-Z_]+\b"),
    "Claude permission mode": re.compile(r"\bbypassPermissions\b", re.I),
    "Claude-only tool": re.compile(
        r"\b(?:AskUserQuestion|EnterPlanMode|ExitPlanMode|WebSearch|"
        r"WebFetch|Task tool|Monitor tool)\b",
        re.I,
    ),
    "Claude skill metadata": re.compile(
        r"\b(?:allowed-tools|disallowed-tools|disable-model-invocation|"
        r"argument-hint)\b",
        re.I,
    ),
    "Anthropic model alias": re.compile(
        r"\b(?:Opus|Sonnet|Haiku)(?:\s+\d[\d.]*)?\b",
        re.I,
    ),
    "positional slash-command argument": re.compile(
        r"`\$(?:0|[1-9]\d*)`"
    ),
    "Claude clear command": re.compile(r"(?<!\w)/(?:clear|compact)\b"),
}
PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|REPLACE_ME)\b",
    re.I,
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


@dataclass
class Finding:
    level: str
    gate: str
    message: str
    path: str | None = None


class Audit:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def pass_(self, gate: str, message: str) -> None:
        self.findings.append(Finding("PASS", gate, message))

    def warn(self, gate: str, message: str, path: Path | None = None) -> None:
        self.findings.append(
            Finding("WARN", gate, message, relative(path) if path else None)
        )

    def fail(self, gate: str, message: str, path: Path | None = None) -> None:
        self.findings.append(
            Finding("FAIL", gate, message, relative(path) if path else None)
        )

    @property
    def failed(self) -> bool:
        return any(finding.level == "FAIL" for finding in self.findings)


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_project_bytes(data: bytes, mode: str) -> bytes:
    if mode == "raw-bytes":
        return data
    if mode != "utf-8-lf":
        raise ValueError(f"unsupported project hash mode: {mode}")
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


PROJECT_SKILL_INVOCATION = re.compile(
    r"(?<!\\)\$([a-z][a-z0-9-]*)\b"
)


def escape_project_tex_skill_invocations(text: str) -> tuple[str, int]:
    """Reproduce the project importer TeX-content transformation."""

    converted: list[str] = []
    total = 0
    for line in text.splitlines(keepends=True):
        comment_index: int | None = None
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                comment_index = index
                break
        if comment_index is None:
            content, comment = line, ""
        else:
            content, comment = line[:comment_index], line[comment_index:]
        content, count = PROJECT_SKILL_INVOCATION.subn(r"\\$\1", content)
        total += count
        converted.append(content + comment)
    return "".join(converted), total


def project_sha256(path: Path, mode: str) -> str:
    return hashlib.sha256(
        canonical_project_bytes(path.read_bytes(), mode)
    ).hexdigest()


def release_snapshot() -> tuple[str, int]:
    """Hash the release-relevant tree with portable text line endings."""

    excluded_directories = {
        ".git",
        ".source-baseline",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "build",
        "dist",
        "tmp",
    }
    excluded_files = {
        ROOT / "docs" / "conversion" / "OFFICIAL_VALIDATION.json",
    }
    paths = sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and path not in excluded_files
            and not any(part in excluded_directories for part in path.parts)
            and path.suffix.lower() not in {".pyc", ".pyo"}
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    snapshot = hashlib.sha256()
    for path in paths:
        relative_path = path.relative_to(ROOT).as_posix().encode("utf-8")
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            portable = data
        else:
            portable = (
                text.replace("\r\n", "\n")
                .replace("\r", "\n")
                .encode("utf-8")
            )
        snapshot.update(relative_path)
        snapshot.update(b"\0")
        snapshot.update(hashlib.sha256(portable).digest())
        snapshot.update(b"\0")
    return snapshot.hexdigest(), len(paths)


def sha256_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error
    metadata: dict[str, str] = {}
    current: str | None = None
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            current = match.group(1)
            if current in metadata:
                raise ValueError(f"duplicate frontmatter key: {current}")
            metadata[current] = match.group(2).strip().strip("\"'")
        elif current and (line.startswith(" ") or line.startswith("\t")):
            metadata[current] += " " + line.strip()
        elif line.strip():
            raise ValueError(f"unparseable frontmatter line: {line!r}")
    return metadata, "\n".join(lines[end + 1 :]).strip()


def inventory(audit: Audit) -> list[str]:
    skills = sorted(
        path.name
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    agents = sorted((ROOT / ".codex" / "agents").glob("*.toml"))
    roles = sorted((ROOT / "references" / "agent-roles").glob("*.md"))
    rules = sorted(
        path
        for path in (ROOT / "references" / "rules").glob("*.md")
        if path.name != "INDEX.md"
    )
    references = sorted(
        path
        for path in (ROOT / "references").glob("*.md")
        if path.name != "INDEX.md"
    )
    templates = sorted(
        path
        for path in (ROOT / "assets" / "templates").rglob("*")
        if path.is_file()
    )
    actual = {
        "skill": len(skills),
        "agent": len(agents),
        "role": len(roles),
        "rule": len(rules),
        "reference": len(references),
        "template": len(templates),
    }
    expected = {
        **EXPECTED,
        "skill": PACKAGED_SKILL_COUNT,
        "agent": PACKAGED_AGENT_COUNT,
        "reference": RUNTIME_REFERENCE_COUNT,
        "role": PACKAGED_AGENT_COUNT,
    }
    problems = [
        f"{kind}: expected {expected[kind]}, found {count}"
        for kind, count in actual.items()
        if count != expected[kind]
    ]
    if problems:
        audit.fail("inventory", "; ".join(problems))
    else:
        audit.pass_(
            "inventory",
            "58 packaged skills (52 source-derived plus 6 ManageRAW), 19 "
            "agents/roles (18 source-derived plus manageraw), 32 rules, "
            "9 runtime references "
            "(plus 1 retained historical reference), and 21 templates present",
        )
    return skills


def validate_skills(audit: Audit, skills: list[str], release: bool) -> None:
    problems: list[str] = []
    for name in skills:
        directory = ROOT / "skills" / name
        skill_file = directory / "SKILL.md"
        try:
            metadata, body = parse_frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as error:
            problems.append(f"{name}: {error}")
            continue
        if set(metadata) != {"name", "description"}:
            problems.append(
                f"{name}: frontmatter keys are {sorted(metadata)}, expected "
                "only name and description"
            )
        if metadata.get("name") != name:
            problems.append(
                f"{name}: frontmatter name is {metadata.get('name')!r}"
            )
        description = metadata.get("description", "")
        if len(description) < 40:
            problems.append(f"{name}: description is too short")
        if len(body) < 300:
            problems.append(f"{name}: body is implausibly short")
        if PLACEHOLDER.search(body):
            problems.append(f"{name}: unresolved migration placeholder")
        metadata_file = directory / "agents" / "openai.yaml"
        if not metadata_file.is_file():
            problems.append(f"{name}: agents/openai.yaml missing")
        else:
            metadata_text = metadata_file.read_text(encoding="utf-8")
            for required in ("interface:", "display_name:", "short_description:"):
                if required not in metadata_text:
                    problems.append(
                        f"{name}: openai.yaml missing {required.rstrip(':')}"
                    )
        record = ROOT / "docs" / "conversion" / "skills" / f"{name}.md"
        if not record.is_file():
            problems.append(f"{name}: conversion record missing")
        elif release:
            record_text = record.read_text(encoding="utf-8")
            status_match = re.search(
                r"(?m)^-\s*Status:\s*`([^`]+)`",
                record_text,
            )
            if (
                not status_match
                or status_match.group(1)
                not in {"validated", "forward-tested"}
            ):
                problems.append(
                    f"{name}: conversion record is not validated"
                )
            if not re.search(r"(?i)validation.*pass", record_text):
                problems.append(
                    f"{name}: conversion record lacks validation PASS"
                )
    if problems:
        for problem in problems:
            audit.fail("skills", problem)
    else:
        audit.pass_(
            "skills",
            f"all {len(skills)} skills have valid native structure"
            + (" and reviewed conversion records" if release else ""),
        )


def validate_agents(audit: Audit) -> None:
    problems: list[str] = []
    names: set[str] = set()
    for path in sorted((ROOT / ".codex" / "agents").glob("*.toml")):
        try:
            value = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
            problems.append(f"{path.name}: {error}")
            continue
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(value.get(key), str) or not value[key].strip():
                problems.append(f"{path.name}: required string {key} missing")
        name = value.get("name")
        if isinstance(name, str):
            if name in names:
                problems.append(f"{path.name}: duplicate name {name}")
            names.add(name)
            if path.stem.replace("-", "_") != name:
                problems.append(
                    f"{path.name}: filename does not match agent name {name}"
                )
            role = (
                ROOT
                / "references"
                / "agent-roles"
                / f"{name.replace('_', '-')}.md"
            )
            if not role.is_file():
                problems.append(
                    f"{path.name}: portable role {role.name} missing"
                )
        if value.get("sandbox_mode") not in {"read-only", "workspace-write"}:
            problems.append(f"{path.name}: invalid sandbox_mode")
        if "model" in value:
            problems.append(f"{path.name}: provider model is pinned")
    if problems:
        for problem in problems:
            audit.fail("agents", problem)
    else:
        audit.pass_(
            "agents",
            f"all {PACKAGED_AGENT_COUNT} custom agents parse and map to roles",
        )


def validate_manifest(audit: Audit, release: bool) -> None:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail("manifest", f"invalid plugin manifest: {error}", manifest_path)
        return
    required = {"name", "version", "description", "author", "license", "skills"}
    missing = sorted(required - set(manifest))
    if missing:
        audit.fail("manifest", f"missing keys: {', '.join(missing)}")
        return
    if manifest.get("name") != "mawcodex":
        audit.fail("manifest", "plugin name must be mawcodex")
    if manifest.get("skills") != "./skills/":
        audit.fail("manifest", "skills path must be ./skills/")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        audit.fail("manifest", "interface must be an object")
    else:
        prompts = interface.get("defaultPrompt")
        if (
            not isinstance(prompts, list)
            or not 1 <= len(prompts) <= 3
            or any(
                not isinstance(prompt, str)
                or not prompt.strip()
                or len(prompt) > 128
                for prompt in prompts
            )
        ):
            audit.fail(
                "manifest",
                "interface.defaultPrompt must contain 1-3 non-empty "
                "strings of at most 128 characters",
            )
    version = str(manifest.get("version", ""))
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        audit.fail("manifest", f"version is not stable semver: {version}")
    elif release and int(version.split(".", 1)[0]) < 1:
        audit.fail(
            "manifest",
            f"stable release version must have major >= 1, found {version}",
        )
    else:
        audit.pass_("manifest", f"plugin manifest valid at version {version}")


def validate_release_metadata(audit: Audit, release: bool) -> None:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    citation_path = ROOT / "CITATION.cff"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        citation = citation_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail("release-metadata", f"metadata could not be read: {error}")
        return
    manifest_version = str(manifest.get("version", ""))
    citation_match = re.search(
        r"(?m)^version:\s*[\"']?([^\"'\s]+)[\"']?\s*$",
        citation,
    )
    citation_version = citation_match.group(1) if citation_match else None
    problems: list[str] = []
    if citation_version != manifest_version:
        problems.append(
            "CITATION.cff version "
            f"{citation_version!r} differs from manifest {manifest_version!r}"
        )
    if release:
        date_match = re.search(
            r"(?m)^date-released:\s*(\d{4}-\d{2}-\d{2})\s*$",
            citation,
        )
        if not date_match:
            problems.append("CITATION.cff lacks an ISO date-released")
        stability_path = ROOT / "docs" / "conversion" / "STABILITY.md"
        if stability_path.is_file():
            target_match = re.search(
                r"Current target:\s*`([^`]+)`\s+stable",
                stability_path.read_text(encoding="utf-8"),
            )
            if not target_match or target_match.group(1) != manifest_version:
                problems.append(
                    "stability target does not match the manifest version"
                )
        changelog = ROOT / "CHANGELOG.md"
        if not changelog.is_file():
            problems.append("CHANGELOG.md missing")
        elif not re.search(
            rf"(?m)^##\s+\[?{re.escape(manifest_version)}\]?"
            r"\s*(?:-|\u2014)\s*\d{4}-\d{2}-\d{2}\s*$",
            changelog.read_text(encoding="utf-8"),
        ):
            problems.append(
                f"CHANGELOG.md lacks a dated {manifest_version} heading"
            )
    if problems:
        for problem in problems:
            audit.fail("release-metadata", problem)
    else:
        audit.pass_(
            "release-metadata",
            f"manifest and citation metadata agree at {manifest_version}",
        )


def validate_hooks(audit: Audit) -> None:
    path = ROOT / "hooks" / "hooks.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail("hooks", f"invalid hooks.json: {error}", path)
        return
    hooks = value.get("hooks")
    if not isinstance(hooks, dict):
        audit.fail("hooks", "hooks.json does not contain a hooks object")
        return
    events = set(hooks)
    problems: list[str] = []
    if not events <= ALLOWED_HOOK_EVENTS:
        problems.append(
            "unknown events: " + ", ".join(sorted(events - ALLOWED_HOOK_EVENTS))
        )
    if events != REQUIRED_HOOK_EVENTS:
        problems.append(
            "enabled events differ from expected mapping: "
            + ", ".join(sorted(events))
        )
    serialized = json.dumps(value)
    if "transcript" in serialized.lower():
        problems.append("hook configuration relies on transcript internals")
    if "PLUGIN_ROOT" not in serialized or "commandWindows" not in serialized:
        problems.append("cross-platform plugin-root commands are incomplete")
    for implementation in (
        ROOT / "hooks" / "scripts" / "maw_hook.sh",
        ROOT / "hooks" / "scripts" / "maw_hook.py",
        ROOT / "hooks" / "scripts" / "maw_hook.ps1",
    ):
        if not implementation.is_file():
            problems.append(f"{implementation.name} missing")
    map_path = ROOT / "docs" / "conversion" / "HOOK_MAP.md"
    if not map_path.is_file():
        problems.append("HOOK_MAP.md missing")
    else:
        mapped = len(
            re.findall(
                r"(?m)^\|\s*`(?:git-guardrails|claim-reconcile|pre-compact|"
                r"post-compact-restore|context-monitor|log-reminder|notify)"
                r"[^`]*`",
                map_path.read_text(encoding="utf-8"),
            )
        )
        if mapped != 7:
            problems.append(f"expected 7 hook dispositions, found {mapped}")
    if problems:
        for problem in problems:
            audit.fail("hooks", problem)
    else:
        audit.pass_("hooks", "four hooks enabled; all seven source hooks mapped")


def operational_files() -> Iterable[Path]:
    patterns = (
        "skills/*/SKILL.md",
        "references/*.md",
        "references/rules/*.md",
        "references/agent-roles/*.md",
        ".codex/agents/*.toml",
        "hooks/hooks.json",
        "hooks/scripts/*",
        "assets/templates/*.md",
        "assets/templates/*.yaml",
        "assets/project-template/**/*.md",
        "assets/project-template/**/*.py",
        "assets/project-template/**/*.R",
        "assets/project-template/**/*.qmd",
        "assets/project-template/**/*.tex",
    )
    seen: set[Path] = set()
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def validate_provider_residue(audit: Audit, skills: list[str]) -> None:
    slash_skill = re.compile(
        r"(?<![\w.])/(?:"
        + "|".join(re.escape(name) for name in sorted(skills, key=len, reverse=True))
        + r")\b"
    )
    problems: list[tuple[Path, int, str]] = []
    for path in operational_files():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("<!--") and (
                "Adapted from .claude/" in stripped
                or "Native rewrite of .claude/" in stripped
                or "Native replacement for .claude/" in stripped
                or "Native reimplementation of .claude/" in stripped
            ):
                continue
            for label, pattern in PROVIDER_PATTERNS.items():
                if pattern.search(line):
                    problems.append((path, number, label))
            if slash_skill.search(line):
                problems.append((path, number, "slash-style skill invocation"))
    if problems:
        for path, number, label in problems:
            audit.fail(
                "provider-residue",
                f"line {number}: {label}",
                path,
            )
    else:
        audit.pass_(
            "provider-residue",
            "no operational Claude-only tools, paths, aliases, or invocation "
            "syntax remain",
        )


def normalize_link_target(raw: str) -> str | None:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        raw = raw[1 : raw.index(">")]
    elif re.search(r'\s+["\']', raw):
        raw = re.split(r'\s+["\']', raw, maxsplit=1)[0]
    if (
        not raw
        or raw.startswith(("#", "http://", "https://", "mailto:", "app://"))
        or any(token in raw for token in ("{", "}", "[", "]", "*"))
        or "LectureN" in raw
        or raw.startswith(("path/to/", "YYYY", "$"))
    ):
        return None
    raw = urllib.parse.unquote(raw.split("#", 1)[0])
    return raw or None


def validate_markdown_links(audit: Audit) -> None:
    problems: list[tuple[Path, str]] = []
    roots = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "skills",
        ROOT / "references",
        ROOT / "assets" / "templates",
        ROOT / "docs" / "conversion",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(root.rglob("*.md"))
    for path in sorted(set(files)):
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw in MARKDOWN_LINK.findall(text):
            target = normalize_link_target(raw)
            if target is None:
                continue
            candidate = (
                ROOT / target.lstrip("/")
                if target.startswith("/")
                else path.parent / target
            )
            template_candidate: Path | None = None
            try:
                template_relative = path.relative_to(
                    ROOT / "assets" / "templates"
                )
            except ValueError:
                pass
            else:
                template_candidate = (
                    ROOT
                    / "assets"
                    / "project-template"
                    / "templates"
                    / template_relative.parent
                    / target
                )
            if not candidate.exists() and not (
                template_candidate and template_candidate.exists()
            ):
                problems.append((path, target))
    if problems:
        for path, target in problems:
            audit.fail(
                "links",
                f"missing relative link target: {target}",
                path,
            )
    else:
        audit.pass_("links", "all checked relative Markdown links resolve")


def validate_provenance(audit: Audit, release: bool) -> None:
    required_files = (
        ROOT / "LICENSE",
        ROOT / "NOTICE.md",
        ROOT / "THIRD_PARTY_NOTICES.md",
        ROOT / "docs" / "conversion" / "SOURCE_BASELINE.md",
        ROOT / "docs" / "conversion" / "SOURCE_MANIFEST.json",
        ROOT / "docs" / "conversion" / "THIRD_PARTY_AUDIT.md",
        ROOT / "docs" / "conversion" / "PROJECT_TEMPLATE_MANIFEST.json",
    )
    missing = [path for path in required_files if not path.is_file()]
    for path in missing:
        audit.fail("provenance", "required provenance file missing", path)
    if missing:
        return
    notices = (
        (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        + (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    )
    required_names = (
        "Pedro",
        "Matt Pocock",
        "Chris Blattman",
        "Scott Cunningham",
        "Academic Research Skills",
    )
    absent = [name for name in required_names if name not in notices]
    if absent:
        audit.fail(
            "provenance",
            "notices omit: " + ", ".join(absent),
        )
    source_manifest_path = (
        ROOT / "docs" / "conversion" / "SOURCE_MANIFEST.json"
    )
    try:
        source_manifest = json.loads(
            source_manifest_path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as error:
        audit.fail("provenance", f"invalid SOURCE_MANIFEST.json: {error}")
        return
    if source_manifest.get("source_commit") != BASELINE_COMMIT:
        audit.fail("provenance", "source manifest commit differs from baseline")
    if source_manifest.get("schema_version") != 3:
        audit.fail("provenance", "source manifest schema_version must be 3")
    components = source_manifest.get("components")
    if not isinstance(components, list):
        audit.fail("provenance", "source manifest components are invalid")
        return
    counts = Counter(
        record.get("kind")
        for record in components
        if isinstance(record, dict)
    )
    count_problems = [
        f"{kind}: expected {expected}, found {counts.get(kind, 0)}"
        for kind, expected in EXPECTED.items()
        if counts.get(kind, 0) != expected
    ]
    if count_problems:
        audit.fail("provenance", "; ".join(count_problems))
    component_problems: list[str] = []
    for record in components:
        if not isinstance(record, dict):
            component_problems.append("non-object component record")
            continue
        targets: list[tuple[str, str]] = []
        if isinstance(record.get("target"), str):
            targets.append(("target", "target_sha256"))
        if record.get("kind") == "agent":
            targets.extend(
                [
                    ("role_target", "role_target_sha256"),
                    ("toml_target", "toml_target_sha256"),
                ]
            )
        if not targets:
            component_problems.append(
                f"{record.get('kind')}/{record.get('name')}: target missing"
            )
            continue
        classification = record.get("classification")
        if classification not in ALLOWED_CLASSIFICATIONS:
            component_problems.append(
                f"{record.get('kind')}/{record.get('name')}: "
                "classification missing or invalid"
            )
        revision_summary = record.get("revision_summary")
        if (
            not isinstance(revision_summary, str)
            or len(revision_summary) < 60
        ):
            component_problems.append(
                f"{record.get('kind')}/{record.get('name')}: "
                "revision summary missing or implausibly short"
            )
        revision_record = record.get("revision_record")
        if not isinstance(revision_record, str):
            component_problems.append(
                f"{record.get('kind')}/{record.get('name')}: "
                "revision record missing"
            )
        else:
            revision_path = (ROOT / revision_record).resolve()
            try:
                revision_path.relative_to(ROOT.resolve())
            except ValueError:
                component_problems.append(
                    f"{record.get('kind')}/{record.get('name')}: "
                    "revision record escapes the package"
                )
            else:
                if not revision_path.is_file():
                    component_problems.append(
                        f"{record.get('kind')}/{record.get('name')}: "
                        "revision record unavailable"
                    )
        for target_key, hash_key in targets:
            target_value = record.get(target_key)
            if not isinstance(target_value, str):
                component_problems.append(
                    f"{record.get('kind')}/{record.get('name')}: "
                    f"{target_key} missing"
                )
                continue
            target = Path(target_value)
            if not target.is_absolute():
                target = ROOT / target
            if not target.is_file():
                component_problems.append(
                    f"{record.get('kind')}/{record.get('name')}: "
                    f"{target_key} missing"
                )
            elif record.get(hash_key) != sha256_text(target):
                component_problems.append(
                    f"{record.get('kind')}/{record.get('name')}: "
                    f"{target_key} hash stale"
                )
        if release and record.get("status") not in {
            "validated",
            "forward-tested",
        }:
            component_problems.append(
                f"{record.get('kind')}/{record.get('name')}: "
                "component status is not validated"
            )
        source_value = record.get("source")
        if isinstance(source_value, str):
            source = Path(source_value)
            if not source.is_absolute():
                source = SOURCE_ROOT / source
            if not source.is_file():
                if release:
                    component_problems.append(
                        f"{record.get('kind')}/{record.get('name')}: "
                        "fixed source file unavailable"
                    )
            elif record.get("source_sha256") != sha256_text(source):
                component_problems.append(
                    f"{record.get('kind')}/{record.get('name')}: "
                    "source hash differs"
                )
    for problem in component_problems:
        audit.fail("provenance", problem)
    if not absent and not count_problems and not component_problems:
        audit.pass_(
            "provenance",
            "component inventory, hashes, baseline, and third-party notices "
            "are complete",
        )


def validate_project_template_manifest(
    audit: Audit,
    release: bool,
) -> None:
    path = (
        ROOT
        / "docs"
        / "conversion"
        / "PROJECT_TEMPLATE_MANIFEST.json"
    )
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail(
            "project-provenance",
            f"project-template manifest is invalid: {error}",
            path,
        )
        return
    problems: list[str] = []
    if manifest.get("schema_version") != 2:
        problems.append("schema_version must be 2")
    if manifest.get("source_commit") != BASELINE_COMMIT:
        problems.append("source commit differs from the fixed baseline")
    if manifest.get("generated_by") != "scripts/migrate_project_template.py":
        problems.append("generated_by is unexpected")
    records = manifest.get("files")
    if not isinstance(records, list):
        problems.append("files must be an array")
        records = []
    if len(records) != 18:
        problems.append(f"expected 18 imported files, found {len(records)}")

    seen_sources: set[str] = set()
    seen_targets: set[str] = set()
    source_root_resolved = SOURCE_ROOT.resolve()
    root_resolved = ROOT.resolve()
    for index, record in enumerate(records):
        label = f"record {index + 1}"
        if not isinstance(record, dict):
            problems.append(f"{label}: entry is not an object")
            continue
        source_value = record.get("source")
        target_value = record.get("target")
        if not isinstance(source_value, str):
            problems.append(f"{label}: source missing")
            continue
        if not isinstance(target_value, str):
            problems.append(f"{label}: target missing")
            continue
        if source_value in seen_sources:
            problems.append(f"{label}: duplicate source {source_value}")
        if target_value in seen_targets:
            problems.append(f"{label}: duplicate target {target_value}")
        seen_sources.add(source_value)
        seen_targets.add(target_value)

        source = (SOURCE_ROOT / source_value).resolve()
        target = (ROOT / target_value).resolve()
        try:
            source.relative_to(source_root_resolved)
        except ValueError:
            problems.append(f"{label}: source escapes the fixed clone")
            continue
        try:
            target.relative_to(root_resolved)
        except ValueError:
            problems.append(f"{label}: target escapes the package")
            continue
        if not target.is_file():
            problems.append(f"{label}: target missing: {target_value}")
            continue
        hash_mode = record.get("hash_mode")
        if hash_mode not in {"utf-8-lf", "raw-bytes"}:
            problems.append(f"{label}: invalid or missing hash_mode")
            continue
        try:
            observed_target_hash = project_sha256(target, hash_mode)
        except (OSError, UnicodeError, ValueError) as error:
            problems.append(f"{label}: target hashing failed: {error}")
            continue
        if record.get("target_sha256") != observed_target_hash:
            problems.append(f"{label}: target hash differs: {target_value}")

        if not source.is_file():
            if release:
                problems.append(
                    f"{label}: fixed source unavailable: {source_value}"
                )
            continue
        try:
            observed_source_hash = project_sha256(source, hash_mode)
        except (OSError, UnicodeError, ValueError) as error:
            problems.append(f"{label}: source hashing failed: {error}")
            continue
        if record.get("source_sha256") != observed_source_hash:
            problems.append(f"{label}: source hash differs: {source_value}")
            continue

        replacements = record.get("replacements")
        if not isinstance(replacements, list):
            problems.append(f"{label}: replacements must be an array")
            continue
        source_bytes = canonical_project_bytes(
            source.read_bytes(),
            hash_mode,
        )
        if hash_mode == "raw-bytes":
            if replacements:
                problems.append(
                    f"{label}: binary source cannot have text replacements"
                )
            expected_bytes = source_bytes
        else:
            adapted = source_bytes.decode("utf-8")
            for replacement in replacements:
                if not isinstance(replacement, dict):
                    problems.append(f"{label}: invalid replacement record")
                    continue
                operation = replacement.get("operation")
                if operation == "escape-tex-skill-invocations":
                    expected_count = replacement.get("count")
                    adapted, observed_count = (
                        escape_project_tex_skill_invocations(adapted)
                    )
                    if (
                        not isinstance(expected_count, int)
                        or expected_count < 1
                    ):
                        problems.append(
                            f"{label}: malformed TeX escape operation"
                        )
                    elif observed_count != expected_count:
                        problems.append(
                            f"{label}: TeX escape count is {observed_count}, "
                            f"expected {expected_count}"
                        )
                    continue
                if operation is not None:
                    problems.append(
                        f"{label}: unknown replacement operation {operation!r}"
                    )
                    continue
                old = replacement.get("from")
                new = replacement.get("to")
                count = replacement.get("count")
                if (
                    not isinstance(old, str)
                    or not isinstance(new, str)
                    or not isinstance(count, int)
                    or count < 1
                ):
                    problems.append(
                        f"{label}: malformed replacement record"
                    )
                    continue
                observed = adapted.count(old)
                if observed != count:
                    problems.append(
                        f"{label}: replacement count for {old!r} is "
                        f"{observed}, expected {count}"
                    )
                adapted = adapted.replace(old, new)
            expected_bytes = adapted.replace("\r\n", "\n").encode("utf-8")
        target_bytes = canonical_project_bytes(
            target.read_bytes(),
            hash_mode,
        )
        if target_bytes != expected_bytes:
            problems.append(
                f"{label}: target bytes do not match recorded adaptation"
            )

    if problems:
        for problem in problems:
            audit.fail("project-provenance", problem, path)
    else:
        audit.pass_(
            "project-provenance",
            "all 18 imported project assets match source, transformations, "
            "targets, and hashes",
        )


def validate_runtime_surface_manifest(
    audit: Audit,
    release: bool,
) -> None:
    path = (
        ROOT
        / "docs"
        / "conversion"
        / "RUNTIME_SURFACES_MANIFEST.json"
    )
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail(
            "runtime-provenance",
            f"runtime-surface manifest is invalid: {error}",
            path,
        )
        return
    problems: list[str] = []
    if document.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    if document.get("source_commit") != BASELINE_COMMIT:
        problems.append("source commit differs from the fixed baseline")
    if document.get("generated_by") != (
        "scripts/refresh_runtime_surface_manifest.py"
    ):
        problems.append("generated_by is unexpected")
    if document.get("counts") != {"core": 6, "hook": 7}:
        problems.append("counts must record 6 core and 7 hook surfaces")
    surfaces = document.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) != 13:
        problems.append("exactly 13 runtime surfaces are required")
        surfaces = []
    names = {
        record.get("name")
        for record in surfaces
        if isinstance(record, dict)
    }
    if names != EXPECTED_RUNTIME_SURFACES:
        problems.append("runtime-surface names differ from the fixed inventory")
    seen_sources: set[str] = set()
    for index, record in enumerate(surfaces):
        label = f"runtime surface {index + 1}"
        if not isinstance(record, dict):
            problems.append(f"{label}: entry is not an object")
            continue
        name = record.get("name")
        if record.get("kind") not in {"core", "hook"}:
            problems.append(f"{label}: invalid kind")
        if record.get("status") != "validated":
            problems.append(f"{name}: status is not validated")
        if record.get("classification") not in ALLOWED_CLASSIFICATIONS:
            problems.append(f"{name}: classification missing or invalid")
        if not isinstance(record.get("disposition"), str) or len(
            record["disposition"]
        ) < 10:
            problems.append(f"{name}: disposition missing")
        if not isinstance(record.get("revision_summary"), str) or len(
            record["revision_summary"]
        ) < 60:
            problems.append(f"{name}: revision summary missing")
        revision_record = record.get("revision_record")
        if not isinstance(revision_record, str) or not (
            ROOT / revision_record
        ).is_file():
            problems.append(f"{name}: revision record unavailable")
        source_value = record.get("source")
        if not isinstance(source_value, str):
            problems.append(f"{name}: source path missing")
            continue
        if source_value in seen_sources:
            problems.append(f"{name}: duplicate source path")
        seen_sources.add(source_value)
        source = SOURCE_ROOT / source_value
        if not source.is_file():
            if release:
                problems.append(f"{name}: fixed source unavailable")
        elif record.get("source_sha256") != sha256_text(source):
            problems.append(f"{name}: source hash differs")
        targets = record.get("targets")
        if not isinstance(targets, list) or not targets:
            problems.append(f"{name}: no target or replacement pointer")
            continue
        for target_record in targets:
            if not isinstance(target_record, dict):
                problems.append(f"{name}: target record is invalid")
                continue
            target_value = target_record.get("path")
            if not isinstance(target_value, str):
                problems.append(f"{name}: target path missing")
                continue
            target = (ROOT / target_value).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(f"{name}: target escapes the package")
                continue
            if not target.is_file():
                problems.append(f"{name}: target unavailable: {target_value}")
            elif target_record.get("sha256") != sha256_text(target):
                problems.append(f"{name}: target hash differs: {target_value}")
    if problems:
        for problem in problems:
            audit.fail("runtime-provenance", problem, path)
    else:
        audit.pass_(
            "runtime-provenance",
            "all 7 hooks and 6 core provider surfaces have fixed source "
            "hashes, classifications, revisions, and current targets",
        )


def validate_auxiliary_source_manifest(
    audit: Audit,
    release: bool,
) -> None:
    path = (
        ROOT
        / "docs"
        / "conversion"
        / "AUXILIARY_SOURCE_MANIFEST.json"
    )
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.fail(
            "source-coverage",
            f"auxiliary source manifest is invalid: {error}",
            path,
        )
        return
    problems: list[str] = []
    if document.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    if document.get("source_commit") != BASELINE_COMMIT:
        problems.append("source commit differs from the fixed baseline")
    if document.get("generated_by") != (
        "scripts/refresh_auxiliary_source_manifest.py"
    ):
        problems.append("generated_by is unexpected")
    if document.get("tracked_source_files") != 211:
        problems.append("tracked_source_files must be 211")
    if document.get("previously_mapped_files") != 163:
        problems.append("previously_mapped_files must be 163")
    if document.get("auxiliary_files") != 48:
        problems.append("auxiliary_files must be 48")
    records = document.get("files")
    if not isinstance(records, list) or len(records) != 48:
        problems.append("exactly 48 auxiliary records are required")
        records = []
    auxiliary_sources: set[str] = set()
    for index, record in enumerate(records):
        label = f"auxiliary record {index + 1}"
        if not isinstance(record, dict):
            problems.append(f"{label}: entry is not an object")
            continue
        source_value = record.get("source")
        if not isinstance(source_value, str):
            problems.append(f"{label}: source path missing")
            continue
        if source_value in auxiliary_sources:
            problems.append(f"{source_value}: duplicate source record")
        auxiliary_sources.add(source_value)
        if record.get("name") != source_value:
            problems.append(f"{source_value}: name must equal source path")
        if record.get("status") != "validated":
            problems.append(f"{source_value}: status is not validated")
        if record.get("classification") not in ALLOWED_CLASSIFICATIONS:
            problems.append(
                f"{source_value}: classification missing or invalid"
            )
        if not isinstance(record.get("disposition"), str) or len(
            record["disposition"]
        ) < 10:
            problems.append(f"{source_value}: disposition missing")
        if not isinstance(record.get("revision_summary"), str) or len(
            record["revision_summary"]
        ) < 60:
            problems.append(f"{source_value}: revision summary missing")
        revision_record = record.get("revision_record")
        if not isinstance(revision_record, str) or not (
            ROOT / revision_record
        ).is_file():
            problems.append(f"{source_value}: revision record unavailable")
        source = SOURCE_ROOT / source_value
        if not source.is_file():
            if release:
                problems.append(f"{source_value}: fixed source unavailable")
        elif record.get("source_sha256") != sha256_text(source):
            problems.append(f"{source_value}: source hash differs")
        targets = record.get("targets")
        if not isinstance(targets, list) or not targets:
            problems.append(f"{source_value}: no disposition target")
            continue
        for target_record in targets:
            if not isinstance(target_record, dict):
                problems.append(f"{source_value}: invalid target record")
                continue
            target_value = target_record.get("path")
            if not isinstance(target_value, str):
                problems.append(f"{source_value}: target path missing")
                continue
            target = (ROOT / target_value).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(f"{source_value}: target escapes package")
                continue
            if not target.is_file():
                problems.append(
                    f"{source_value}: target unavailable: {target_value}"
                )
            elif target_record.get("sha256") != sha256_text(target):
                problems.append(
                    f"{source_value}: target hash differs: {target_value}"
                )

    manifest_sources: list[set[str]] = [auxiliary_sources]
    try:
        component = json.loads(
            (
                ROOT / "docs" / "conversion" / "SOURCE_MANIFEST.json"
            ).read_text(encoding="utf-8")
        )
        project = json.loads(
            (
                ROOT
                / "docs"
                / "conversion"
                / "PROJECT_TEMPLATE_MANIFEST.json"
            ).read_text(encoding="utf-8")
        )
        runtime = json.loads(
            (
                ROOT
                / "docs"
                / "conversion"
                / "RUNTIME_SURFACES_MANIFEST.json"
            ).read_text(encoding="utf-8")
        )
        manifest_sources.extend(
            [
                {
                    record["source"]
                    for record in component["components"]
                },
                {record["source"] for record in project["files"]},
                {record["source"] for record in runtime["surfaces"]},
            ]
        )
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        problems.append(f"coverage manifests could not be reconciled: {error}")
    else:
        union: set[str] = set()
        for group in manifest_sources:
            overlap = union & group
            if overlap:
                problems.append(
                    "source files appear in multiple manifests: "
                    + ", ".join(sorted(overlap)[:5])
                )
            union.update(group)
        if len(union) != 211:
            problems.append(
                f"manifest union must cover 211 files, found {len(union)}"
            )
        if SOURCE_ROOT.is_dir():
            process = subprocess.run(
                [
                    "git",
                    "-c",
                    f"safe.directory={SOURCE_ROOT.resolve().as_posix()}",
                    "-C",
                    str(SOURCE_ROOT.resolve()),
                    "ls-files",
                ],
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
            )
            if process.returncode:
                if release:
                    problems.append(
                        "fixed source Git inventory could not be read"
                    )
            else:
                tracked = set(process.stdout.splitlines())
                if union != tracked:
                    problems.append(
                        "manifest union differs from fixed tracked files"
                    )
        elif release:
            problems.append("fixed source repository is unavailable")
    if problems:
        for problem in problems:
            audit.fail("source-coverage", problem, path)
    else:
        audit.pass_(
            "source-coverage",
            "all 211 files at the fixed source commit have exactly one "
            "hash-bound conversion or disposition record",
        )


def validate_release_documents(audit: Audit) -> None:
    stability = ROOT / "docs" / "conversion" / "STABILITY.md"
    forward = ROOT / "docs" / "conversion" / "FORWARD_TESTS.md"
    forward_results = (
        ROOT / "docs" / "conversion" / "FORWARD_TEST_RESULTS.json"
    )
    official_results = (
        ROOT / "docs" / "conversion" / "OFFICIAL_VALIDATION.json"
    )
    release_report = ROOT / "docs" / "conversion" / "RELEASE_REPORT.md"
    known_limitations = (
        ROOT / "docs" / "conversion" / "KNOWN_LIMITATIONS.md"
    )
    install_guide = ROOT / "docs" / "INSTALL.md"
    for status_record in (
        ROOT / "docs" / "conversion" / "AGENT_MAP.md",
        ROOT / "docs" / "conversion" / "shared-resources.md",
    ):
        try:
            status_text = status_record.read_text(encoding="utf-8")
        except OSError:
            audit.fail(
                "release",
                "conversion status record missing",
                status_record,
            )
        else:
            if (
                "mechanical-baseline" in status_text
                or "semantic-baseline" in status_text
            ):
                audit.fail(
                    "release",
                    "conversion status record is not validated",
                    status_record,
                )
    if not stability.is_file():
        audit.fail("release", "STABILITY.md missing")
    else:
        rows = re.findall(
            r"(?m)^\|\s*[^|]+\|\s*[^|]+\|\s*([^|]+)\|",
            stability.read_text(encoding="utf-8"),
        )
        values = [
            value.strip()
            for value in rows
            if set(value.strip()) != {"-"}
            and value.strip().lower() != "current result"
        ]
        if not values or any(value != "PASS" for value in values):
            audit.fail(
                "release",
                "stability matrix contains non-PASS release gates",
                stability,
            )
    if not forward.is_file():
        audit.fail("release", "FORWARD_TESTS.md missing")
    else:
        text = forward.read_text(encoding="utf-8")
        if "FAIL" in text or "UNTESTED" in text or "PENDING" in text:
            audit.fail(
                "release",
                "forward-test record contains unresolved results",
                forward,
            )
        elif len(re.findall(r"(?m)^\|\s*FT-\d+", text)) < 6:
            audit.fail(
                "release",
                "fewer than six representative forward tests recorded",
                forward,
            )
    result_ids: set[str] = set()
    if not forward_results.is_file():
        audit.fail("release", "FORWARD_TEST_RESULTS.json missing")
    else:
        try:
            result_document = json.loads(
                forward_results.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as error:
            audit.fail(
                "release",
                f"invalid forward-test results: {error}",
                forward_results,
            )
        else:
            tests = result_document.get("tests")
            problems: list[str] = []
            if result_document.get("schema_version") != 1:
                problems.append("forward-test schema_version must be 1")
            if result_document.get("source_commit") != BASELINE_COMMIT:
                problems.append("forward-test source commit differs")
            if not isinstance(tests, list) or len(tests) < 10:
                problems.append(
                    "at least ten machine-readable forward tests are required"
                )
                tests = []
            for index, test in enumerate(tests):
                label = f"forward test {index + 1}"
                if not isinstance(test, dict):
                    problems.append(f"{label}: result is not an object")
                    continue
                test_id = test.get("id")
                skill = test.get("skill")
                if not isinstance(test_id, str) or not re.fullmatch(
                    r"FT-\d{2}", test_id
                ):
                    problems.append(f"{label}: invalid id")
                    continue
                if test_id in result_ids:
                    problems.append(f"{test_id}: duplicate id")
                result_ids.add(test_id)
                if not isinstance(skill, str):
                    problems.append(f"{test_id}: skill missing")
                    continue
                skill_path = ROOT / "skills" / skill / "SKILL.md"
                if not skill_path.is_file():
                    problems.append(f"{test_id}: skill does not exist")
                elif test.get("skill_sha256") != sha256_text(skill_path):
                    problems.append(f"{test_id}: skill hash is stale")
                if test.get("evaluator") != "independent-subagent":
                    problems.append(
                        f"{test_id}: evaluator was not independent"
                    )
                if test.get("result") != "PASS":
                    problems.append(f"{test_id}: result is not PASS")
                if not isinstance(test.get("scenario"), str) or len(
                    test["scenario"]
                ) < 40:
                    problems.append(f"{test_id}: scenario is too short")
                observations = test.get("observed_behavior")
                if not isinstance(observations, list) or not observations:
                    problems.append(f"{test_id}: observed behavior missing")
            for problem in problems:
                audit.fail("release", problem, forward_results)
            if forward.is_file():
                markdown_ids = set(
                    re.findall(
                        r"(?m)^\|\s*(FT-\d{2})\s*\|",
                        forward.read_text(encoding="utf-8"),
                    )
                )
                if result_ids and markdown_ids != result_ids:
                    audit.fail(
                        "release",
                        "forward-test Markdown and JSON IDs differ",
                        forward,
                    )

    if not official_results.is_file():
        audit.fail("release", "OFFICIAL_VALIDATION.json missing")
    else:
        try:
            official = json.loads(
                official_results.read_text(encoding="utf-8")
            )
            manifest = json.loads(
                (
                    ROOT / ".codex-plugin" / "plugin.json"
                ).read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as error:
            audit.fail(
                "release",
                f"official validation evidence is invalid: {error}",
                official_results,
            )
        else:
            official_problems: list[str] = []
            if official.get("schema_version") != 1:
                official_problems.append(
                    "official evidence schema_version must be 1"
                )
            if official.get("package_version") != manifest.get("version"):
                official_problems.append(
                    "official evidence package version differs"
                )
            plugin_result = official.get("plugin_validator")
            if not isinstance(plugin_result, dict) or (
                plugin_result.get("result") != "PASS"
                or not re.fullmatch(
                    r"[0-9a-f]{64}",
                    str(plugin_result.get("validator_sha256", "")),
                )
            ):
                official_problems.append(
                    "official plugin-validator evidence is incomplete"
                )
            skill_result = official.get("skill_validator")
            if not isinstance(skill_result, dict) or (
                skill_result.get("result") != "PASS"
                or skill_result.get("passed") != PACKAGED_SKILL_COUNT
                or skill_result.get("total") != PACKAGED_SKILL_COUNT
                or not re.fullmatch(
                    r"[0-9a-f]{64}",
                    str(skill_result.get("validator_sha256", "")),
                )
            ):
                official_problems.append(
                    "official skill-validator evidence is incomplete"
                )
            source_result = official.get("source_contract")
            if not isinstance(source_result, dict) or (
                source_result.get("result") != "PASS"
                or source_result.get("commit") != BASELINE_COMMIT
            ):
                official_problems.append(
                    "source-contract evidence is incomplete"
                )
            test_result = official.get("unit_tests")
            if not isinstance(test_result, dict) or (
                test_result.get("result") != "PASS"
                or not isinstance(test_result.get("count"), int)
                or test_result["count"] < 10
                or test_result.get("skipped") != 0
            ):
                official_problems.append(
                    "unit-test evidence is incomplete"
                )
            snapshot_result = official.get("release_snapshot")
            current_snapshot, current_file_count = release_snapshot()
            if not isinstance(snapshot_result, dict) or (
                snapshot_result.get("algorithm") != "sha256"
                or snapshot_result.get("digest") != current_snapshot
                or snapshot_result.get("file_count") != current_file_count
            ):
                official_problems.append(
                    "official evidence does not match the current release "
                    "snapshot"
                )
            for validator_result, label in (
                (plugin_result, "plugin"),
                (skill_result, "skill"),
            ):
                if not isinstance(validator_result, dict):
                    continue
                validator_path_value = validator_result.get("path")
                if not isinstance(validator_path_value, str):
                    official_problems.append(
                        f"official {label} validator path is missing"
                    )
                    continue
                validator_path = Path(validator_path_value)
                if (
                    validator_path.is_file()
                    and validator_result.get("validator_sha256")
                    != sha256(validator_path)
                ):
                    official_problems.append(
                        f"official {label} validator hash differs from its "
                        "current local file"
                    )
            for problem in official_problems:
                audit.fail("release", problem, official_results)

    if not release_report.is_file():
        audit.fail("release", "RELEASE_REPORT.md missing")
    else:
        report_text = release_report.read_text(encoding="utf-8")
        required_evidence = (
            f"{PACKAGED_SKILL_COUNT}/{PACKAGED_SKILL_COUNT}",
            "plugin validator",
            "source clone",
            "forward tests",
            "unit tests",
        )
        missing_evidence = [
            item for item in required_evidence if item not in report_text.lower()
        ]
        if missing_evidence:
            audit.fail(
                "release",
                "release report omits: " + ", ".join(missing_evidence),
                release_report,
            )
    for required, label in (
        (known_limitations, "KNOWN_LIMITATIONS.md"),
        (install_guide, "docs/INSTALL.md"),
    ):
        if not required.is_file() or required.stat().st_size < 500:
            audit.fail("release", f"{label} missing or implausibly short")
    if not any(
        finding.level == "FAIL" and finding.gate == "release"
        for finding in audit.findings
    ):
        audit.pass_("release", "stable release evidence is complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        help="enforce stable documentation and forward-test gates",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable findings",
    )
    args = parser.parse_args()
    audit = Audit()

    skills = inventory(audit)
    validate_manifest(audit, args.release)
    validate_release_metadata(audit, args.release)
    validate_skills(audit, skills, args.release)
    validate_agents(audit)
    validate_hooks(audit)
    validate_provider_residue(audit, skills)
    validate_markdown_links(audit)
    validate_provenance(audit, args.release)
    validate_project_template_manifest(audit, args.release)
    validate_runtime_surface_manifest(audit, args.release)
    validate_auxiliary_source_manifest(audit, args.release)
    if args.release:
        validate_release_documents(audit)

    counts = Counter(finding.level for finding in audit.findings)
    if args.json:
        print(
            json.dumps(
                {
                    "ok": not audit.failed,
                    "release_mode": args.release,
                    "summary": dict(counts),
                    "findings": [
                        {
                            "level": finding.level,
                            "gate": finding.gate,
                            "message": finding.message,
                            "path": finding.path,
                        }
                        for finding in audit.findings
                    ],
                },
                indent=2,
            )
        )
    else:
        for finding in audit.findings:
            location = f" [{finding.path}]" if finding.path else ""
            print(
                f"{finding.level:<4}  {finding.gate:<18} "
                f"{finding.message}{location}"
            )
        print(
            f"\nSummary: {counts['PASS']} passed, {counts['WARN']} warned, "
            f"{counts['FAIL']} failed."
        )
    return 1 if audit.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
