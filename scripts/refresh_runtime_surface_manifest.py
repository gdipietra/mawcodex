#!/usr/bin/env python3
"""Record provenance for provider runtime surfaces outside core components."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from check_source_clone import BASELINE_COMMIT, GitCheckError, inspect


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
MANIFEST = (
    ROOT / "docs" / "conversion" / "RUNTIME_SURFACES_MANIFEST.json"
)

SURFACES = (
    {
        "kind": "core",
        "name": "root-instructions",
        "source": "CLAUDE.md",
        "classification": "composed replacement",
        "disposition": "native instruction hierarchy",
        "targets": (
            "AGENTS.md",
            "assets/project-template/AGENTS.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Split provider root instructions into package maintenance "
            "instructions and project research instructions, adding explicit "
            "Codex authority and verification boundaries."
        ),
    },
    {
        "kind": "core",
        "name": "settings",
        "source": ".claude/settings.json",
        "classification": "native rewrite",
        "disposition": "safe native configuration",
        "targets": (
            ".codex/config.toml",
            "hooks/hooks.json",
            "AGENTS.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Replaced provider hooks and planning settings with current Codex "
            "configuration while deliberately omitting permission bypass and "
            "broad filesystem, shell, and network allowlists."
        ),
    },
    {
        "kind": "core",
        "name": "academic-writing-output-style",
        "source": ".claude/output-styles/academic-writing.md",
        "classification": "composed replacement",
        "disposition": "portable writing rules and skills",
        "targets": (
            "references/prompt-formatting-core.md",
            "skills/humanize/SKILL.md",
            "skills/proofread/SKILL.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Composed the concise academic voice, evidence calibration, "
            "notation, and anti-fabrication intent into portable formatting "
            "guidance plus humanization and proofreading workflows."
        ),
    },
    {
        "kind": "core",
        "name": "referee-output-style",
        "source": ".claude/output-styles/referee.md",
        "classification": "composed replacement",
        "disposition": "review skill and portable referee role",
        "targets": (
            "skills/review-paper/SKILL.md",
            "references/agent-roles/domain-referee.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Moved terse evidence-backed referee structure, fatal-versus-"
            "fixable triage, and constructive asks into the review workflow "
            "and its independent portable referee role."
        ),
    },
    {
        "kind": "core",
        "name": "status-line",
        "source": ".claude/scripts/statusline.sh",
        "classification": "composed replacement",
        "disposition": "visible Codex state and context workflow",
        "targets": (
            "skills/context-status/SKILL.md",
            "docs/conversion/HOOK_MAP.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Replaced provider session JSON, permission badges, and private "
            "context files with visible Codex task state, explicit context "
            "status, and durable compaction pointers."
        ),
    },
    {
        "kind": "core",
        "name": "workflow-quick-reference",
        "source": ".claude/WORKFLOW_QUICK_REF.md",
        "classification": "composed replacement",
        "disposition": "package instructions and portable rules",
        "targets": (
            "AGENTS.md",
            "README.md",
            "references/rules/plan-first-workflow.md",
            "references/rules/quality-gates.md",
        ),
        "revision_record": "docs/conversion/CORE_SURFACE_MAP.md",
        "revision_summary": (
            "Retained the plan, execute, verify, report loop and quality-gate "
            "intent while replacing provider model and auto-deploy language "
            "with explicit Codex authorization boundaries."
        ),
    },
    {
        "kind": "hook",
        "name": "git-guardrails",
        "source": ".claude/hooks/git-guardrails.py",
        "classification": "native rewrite",
        "disposition": "enabled PreToolUse hook",
        "targets": (
            "hooks/hooks.json",
            "hooks/scripts/maw_hook.py",
            "hooks/scripts/maw_hook.ps1",
            "hooks/scripts/maw_hook.sh",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Reimplemented destructive Git and machine-path guardrails for "
            "current Codex hook input, cross-platform execution, quoted "
            "arguments, and compound command handling."
        ),
    },
    {
        "kind": "hook",
        "name": "claim-reconcile",
        "source": ".claude/hooks/claim-reconcile.py",
        "classification": "native rewrite",
        "disposition": "enabled PostToolUse hook",
        "targets": (
            "hooks/hooks.json",
            "hooks/scripts/maw_hook.py",
            "hooks/scripts/maw_hook.ps1",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Reimplemented claim staleness as a local advisory Codex hook "
            "that records no transcript content and never asserts that an "
            "estimate changed without rerunning the analysis."
        ),
    },
    {
        "kind": "hook",
        "name": "pre-compact",
        "source": ".claude/hooks/pre-compact.py",
        "classification": "native rewrite",
        "disposition": "enabled PreCompact hook",
        "targets": (
            "hooks/hooks.json",
            "hooks/scripts/maw_hook.py",
            "hooks/scripts/maw_hook.ps1",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Reimplemented compaction preparation using current Codex event "
            "fields and minimal plan and session-log pointers stored under "
            "plugin data rather than private transcript state."
        ),
    },
    {
        "kind": "hook",
        "name": "post-compact-restore",
        "source": ".claude/hooks/post-compact-restore.py",
        "classification": "native rewrite",
        "disposition": "enabled SessionStart hook",
        "targets": (
            "hooks/hooks.json",
            "hooks/scripts/maw_hook.py",
            "hooks/scripts/maw_hook.ps1",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Reimplemented context restoration as a compact or resume "
            "SessionStart handoff that reloads durable pointers and requires "
            "fresh Git state inspection before work continues."
        ),
    },
    {
        "kind": "hook",
        "name": "context-monitor",
        "source": ".claude/hooks/context-monitor.py",
        "classification": "composed replacement",
        "disposition": "native context UI and explicit workflow",
        "targets": (
            "skills/context-status/SKILL.md",
            "hooks/scripts/maw_hook.py",
            "hooks/scripts/maw_hook.ps1",
            "docs/conversion/HOOK_MAP.md",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Replaced undocumented transcript token estimation with Codex "
            "context UI, explicit status reporting, and supported compaction "
            "hooks while preserving durable continuity."
        ),
    },
    {
        "kind": "hook",
        "name": "log-reminder",
        "source": ".claude/hooks/log-reminder.py",
        "classification": "composed replacement",
        "disposition": "explicit checkpoint and session logging",
        "targets": (
            "skills/checkpoint/SKILL.md",
            "skills/compress-session/SKILL.md",
            "references/rules/session-logging.md",
            "docs/conversion/HOOK_MAP.md",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Replaced automatic stop-time project writes with explicit "
            "checkpoint and compression workflows plus portable session "
            "logging rules that remain reviewable."
        ),
    },
    {
        "kind": "hook",
        "name": "notify",
        "source": ".claude/hooks/notify.sh",
        "classification": "composed replacement",
        "disposition": "host notification surface",
        "targets": (
            "docs/conversion/HOOK_MAP.md",
        ),
        "revision_record": "docs/conversion/HOOK_MAP.md",
        "revision_summary": (
            "Replaced shell-specific desktop notification commands with the "
            "Codex host notification surface or an explicitly authorized "
            "user automation, without silently spawning background tools."
        ),
    },
)


def digest_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="strict")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    source_root = SOURCE_ROOT.resolve()
    try:
        contract = inspect(source_root, fetch=False)
    except (GitCheckError, OSError, ValueError) as error:
        raise SystemExit(f"source contract check failed: {error}") from error
    if not contract["ok"]:
        raise SystemExit(
            "source contract check failed: "
            + "; ".join(str(item) for item in contract["errors"])
        )

    records: list[dict[str, object]] = []
    for surface in SURFACES:
        source = source_root / str(surface["source"])
        if not source.is_file():
            raise SystemExit(f"source surface missing: {source}")
        targets = []
        for target_value in surface["targets"]:
            target = ROOT / target_value
            if not target.is_file():
                raise SystemExit(f"target surface missing: {target}")
            targets.append(
                {
                    "path": target_value,
                    "sha256": digest_text(target),
                }
            )
        record = {
            key: value
            for key, value in surface.items()
            if key != "targets"
        }
        record.update(
            {
                "source_sha256": digest_text(source),
                "status": "validated",
                "targets": targets,
            }
        )
        records.append(record)

    document = {
        "schema_version": 1,
        "source_repository": (
            "https://github.com/pedrohcgs/claude-code-my-workflow"
        ),
        "source_commit": BASELINE_COMMIT,
        "generated_by": "scripts/refresh_runtime_surface_manifest.py",
        "counts": {"core": 6, "hook": 7},
        "surfaces": records,
    }
    MANIFEST.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Recorded {len(records)} runtime surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
