#!/usr/bin/env python3
"""Migrate shared rules, references, and templates without touching skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from migrate_from_claude import SOURCE_COMMIT, adapt_text


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_frontmatter(text: str) -> tuple[list[str], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return [], normalized
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return [], normalized
    block = normalized[4:end]
    paths: list[str] = []
    in_paths = False
    for line in block.splitlines():
        if line.strip() == "paths:":
            in_paths = True
            continue
        if in_paths:
            match = re.match(r"\s*-\s*[\"']?(.+?)[\"']?\s*$", line)
            if match:
                paths.append(match.group(1))
            elif line and not line.startswith((" ", "\t")):
                in_paths = False
    return paths, normalized[end + 5 :]


def portable_text(text: str, skill_names: list[str]) -> str:
    replacements = [
        (".claude/references/", "references/"),
        (".claude/skills/", "skills/"),
        (".claude/rules/", "references/rules/"),
        (".claude/agents/", ".codex/agents/"),
        (".claude/settings.local.json", ".codex/config.local.toml"),
        (".claude/settings.json", ".codex/config.toml"),
        ("CLAUDE_STRICT_PATHS", "MAWCODEX_STRICT_PATHS"),
        (
            "CLAUDE_PRECOMPACT_BLOCK_ON_DRAFT",
            "MAWCODEX_PRECOMPACT_BLOCK_ON_DRAFT",
        ),
        ("CLAUDE_PROJECT_DIR", "the hook input `cwd`"),
        ("via Task", "using an isolated subagent"),
        ("Task with", "an isolated subagent with"),
        ("`Task`", "a bounded subagent"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text, _ = adapt_text(text, skill_names)
    for skill_name in sorted(skill_names, key=len, reverse=True):
        text = re.sub(
            rf"/{re.escape(skill_name)}\b",
            f"${skill_name}",
            text,
        )
        text = text.replace(
            f"skills${skill_name}",
            f"skills/{skill_name}",
        )
    text = re.sub(
        r"\.codex/agents/([a-z0-9-]+)\.md",
        r"references/agent-roles/\1.md",
        text,
    )
    text = text.replace(
        "a bounded subagent subagent", "bounded subagent"
    )
    text = text.replace(
        "the bounded subagent", "a bounded subagent"
    )
    text = text.replace("forked subagent", "isolated subagent")
    text = text.replace(
        "claude mcp add stata-mcp --scope user -- uvx stata-mcp",
        "configure the `stata-mcp` server in the active Codex profile",
    )
    return text


def provenance_comment(relative: Path, source_text: str) -> str:
    """Return a syntax-valid provenance comment for a template file."""

    message = (
        f"Adapted from templates/{relative.as_posix()} at {SOURCE_COMMIT}; "
        f"source SHA-256 {digest(source_text)}."
    )
    suffix = relative.suffix.lower()
    if suffix == ".tex":
        return f"% {message}"
    if suffix in {".yaml", ".yml"}:
        return f"# {message}"
    return f"<!-- {message} -->"


def native_model_rule(source_text: str) -> str:
    return (
        "<!-- Native rewrite of .claude/rules/model-routing.md at "
        f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
        "# Model and reasoning routing\n\n"
        "## Applicability\n\n"
        "Load this rule when defining or revising skills, custom agents, or "
        "multi-agent workflows.\n\n"
        "## Durable rule\n\n"
        "Route by cognitive demand, independence needs, and sandbox scope. "
        "Do not preserve upstream provider aliases or price tables: model "
        "catalogs and pricing drift, while the task classes remain stable.\n\n"
        "| Work class | Reasoning default | Examples |\n"
        "| --- | --- | --- |\n"
        "| Mechanical | low or medium | inventory, format conversion, "
        "deterministic checks |\n"
        "| Focused review or implementation | medium or high | proofreading, "
        "translation, bounded fixes |\n"
        "| High judgment | high or xhigh | identification review, claim "
        "verification, editorial synthesis, adversarial audit |\n\n"
        "Prefer the parent model. Pin a different model only after verifying "
        "the current official Codex model catalog and documenting a measured "
        "benefit. If current availability cannot be verified, inherit rather "
        "than guess.\n\n"
        "Use isolated subagents when error independence matters. Different "
        "roles, evidence sets, or fresh contexts matter more than cosmetic "
        "model diversity. A lower-cost model never weakens the output schema, "
        "scientific checks, or PASS/FAIL/UNVERIFIED semantics.\n"
    )


def native_agent_fleet(source_text: str) -> str:
    return (
        "<!-- Native rewrite of .claude/references/agent-fleet.md at "
        f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
        "# Codex academic agent fleet\n\n"
        "The project defines 18 narrow custom agents in `.codex/agents/` and "
        "portable equivalents under `references/agent-roles/`. Model names "
        "are intentionally inherited; the durable routing controls are "
        "reasoning effort, sandbox, role scope, and evidence independence.\n\n"
        "## High-judgment reviewers\n\n"
        "`claim_verifier`, `domain_referee`, `domain_reviewer`, `editor`, "
        "`methods_referee`, `quarto_critic`, `sim_reviewer`, and "
        "`tikz_reviewer` use high reasoning and read-only sandboxes.\n\n"
        "## Focused reviewers\n\n"
        "`humanize_auditor`, `pedagogy_reviewer`, `proofreader`, "
        "`r_reviewer`, and `slide_auditor` are read-only roles with focused "
        "review schemas. `promote_memory_council` is a low-reasoning, "
        "read-only voting role.\n\n"
        "## Workspace-writing roles\n\n"
        "`beamer_translator`, `quarto_fixer`, `r_package_reviewer`, and "
        "`verifier` may write only within their assigned workspace scope. "
        "The latter two need workspace writes because package checks and "
        "render/compile verification create artifacts.\n\n"
        "All agents return evidence to the parent for synthesis. None may "
        "commit, push, deploy, submit, send, or publish externally.\n\n"
        "See `docs/conversion/AGENT_MAP.md`, "
        "`references/orchestration-schemas.md`, and "
        "`references/rules/model-routing.md`.\n"
    )


def native_audit_peeves(source_text: str) -> str:
    return (
        "<!-- Native rewrite of .claude/references/audit-pet-peeves.md at "
        f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
        "# Codex migration and audit pet peeves\n\n"
        "Use this catalogue during `$deep-audit` and package review.\n\n"
        "1. **Declared behavior without an available capability.** A skill "
        "must identify missing connectors, compilers, or runtimes as "
        "UNVERIFIED.\n"
        "2. **Body/frontmatter trigger drift.** The description must state "
        "the real workflow and concrete trigger situations.\n"
        "3. **Flags documented in one surface only.** Every advertised flag "
        "must be handled consistently in the body and linked rules.\n"
        "4. **Broken relative references.** Resolve links from the file that "
        "contains them, especially `../../skills/` from rule and role files.\n"
        "5. **Provider syntax surviving as behavior.** Operational slash "
        "commands, Claude paths, tool allowlists, and retired model aliases "
        "are release blockers; provenance mentions are allowed.\n"
        "6. **Reviewers that can edit.** Review roles default to read-only. "
        "Workspace-write requires an explicit implementation or verification "
        "need.\n"
        "7. **Same-context self-verification.** Claim and adversarial checks "
        "need isolated inputs or a fresh subagent.\n"
        "8. **Skipped checks reported as clean.** Missing sources, renderers, "
        "or web access produce UNVERIFIED, never PASS.\n"
        "9. **Hooks presented as complete enforcement.** Tool hooks have "
        "coverage gaps and are defense-in-depth only.\n"
        "10. **Transcript parsing treated as stable.** Codex transcript "
        "format is not a stable hook interface.\n"
        "11. **External actions hidden inside workflow verbs.** Commit, push, "
        "deploy, send, submit, share, and delete need explicit authorization.\n"
        "12. **Source and adaptation mixed.** Upstream remains read-only and "
        "every target retains a source hash.\n"
        "13. **Counts updated without enumeration.** Verify all 52 "
        "source-derived skills, any native additions, 18 source-derived "
        "agents, any native agents, 32 rules, "
        "shared references, and hook mappings by path.\n"
        "14. **False-precision quality scores.** A numeric score is advisory; "
        "hard correctness, provenance, and disclosure failures remain "
        "blocking regardless of score.\n"
        "15. **Documentation claims ahead of tests.** Stable status follows "
        "validators and representative forward tests, not the other way "
        "around.\n"
    )


def native_scheduled_routines(source_text: str) -> str:
    return (
        "<!-- Native rewrite of .claude/references/scheduled-routines.md at "
        f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
        "# Scheduled academic routines in Codex\n\n"
        "Use a Codex Automation only when the user explicitly asks to create "
        "a recurring or scheduled task. Keep the repository workflow useful "
        "without automation.\n\n"
        "Good candidates include nightly reproducibility checks, monthly "
        "memory review, dependency-drift reports, and pre-deadline disclosure "
        "audits. Each automation must define the repository, cadence and "
        "timezone, inputs, allowed mutations, stop conditions, result "
        "location, and notification behavior.\n\n"
        "Scheduled work does not broaden authority. It must not submit, send, "
        "deploy, merge, publish, delete, or export restricted outputs unless "
        "the user explicitly authorized that action. Missing credentials or "
        "tools produce a report marked UNVERIFIED rather than an inferred "
        "success.\n"
    )


def native_tikz_prevention(source_text: str) -> str:
    return (
        "<!-- Native reimplementation of .claude/rules/tikz-prevention.md "
        f"at {SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. The "
        "upstream file credits Scott Cunningham's MixtapeTools; no "
        "MixtapeTools text is copied here. -->\n\n"
        "# TikZ defect-prevention rules\n\n"
        "## Applicability\n\n"
        "Load for `Slides/**/*.tex`, `Figures/**/*.tex`, and "
        "`Preambles/**/*.tex`.\n\n"
        "## P1 — Size boxed nodes explicitly\n\n"
        "For rectangles, circles, and callouts, set a text width or minimum "
        "width plus a minimum height. Account for inner separation. Do not "
        "let a long label silently determine geometry shared with other "
        "nodes.\n\n"
        "## P2 — Declare a coordinate map\n\n"
        "Before drawing, list the important node centers or axis coordinates "
        "and the intended horizontal and vertical gaps. Reuse named "
        "coordinates instead of duplicating numeric positions.\n\n"
        "## P3 — Scale shapes and text together\n\n"
        "Avoid a bare `scale=` on a `tikzpicture`; it changes coordinates "
        "without necessarily scaling node text. Use `transform shape`, or "
        "prefer explicit dimensions and coordinates.\n\n"
        "## P4 — Place edge labels deliberately\n\n"
        "Every non-trivial edge label states a side such as `above`, `below`, "
        "`left`, or `right`, plus a position when the midpoint is crowded. "
        "For curved edges, put the label on the outside of the bend.\n\n"
        "## P5 — Keep one visual claim per picture\n\n"
        "Split overloaded diagrams into separate frames or subfigures. Avoid "
        "overlay conditionals that make bounding boxes unpredictable.\n\n"
        "## Preflight\n\n"
        "1. Inspect node dimensions and coordinate gaps.\n"
        "2. Flag bare `scale=` without `transform shape`.\n"
        "3. Flag labeled edges with no directional placement.\n"
        "4. Compile standalone with the project preamble.\n"
        "5. Render to an image and run the `tikz_reviewer` role.\n"
        "6. Treat a skipped compile or render as UNVERIFIED.\n\n"
        "The packaged snippets in `assets/templates/tikz-snippets/` are "
        "starting points, not proof that a modified diagram is collision-free.\n"
    )


def native_tikz_measurement(source_text: str) -> str:
    return (
        "<!-- Native reimplementation of .claude/rules/tikz-measurement.md "
        f"at {SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. The "
        "upstream file credits Scott Cunningham's MixtapeTools; no "
        "MixtapeTools text is copied here. -->\n\n"
        "# TikZ measurement protocol\n\n"
        "## Applicability\n\n"
        "Load for TikZ authoring, extraction, and visual review.\n\n"
        "## Geometry model\n\n"
        "Treat each node as an axis-aligned box after TeX layout. Its usable "
        "half-width is `(text width + 2 * inner xsep) / 2`; its usable "
        "half-height is `(text height + text depth + 2 * inner ysep) / 2`. "
        "For two horizontally adjacent boxes, the clear gap is the center "
        "distance minus both half-widths. The vertical formula is analogous.\n\n"
        "A label fits in a gap only when its rendered extent plus a safety "
        "margin is smaller than that clear gap. Do not infer fit from source "
        "character count; compile and measure the rendered result.\n\n"
        "## Review procedure\n\n"
        "1. Compile a standalone crop with the same fonts and preamble as the "
        "target deck.\n"
        "2. Convert the crop to a high-resolution bitmap or SVG.\n"
        "3. Inspect every node box, arrow shaft, arrowhead, label, brace, and "
        "axis annotation at normal slide scale.\n"
        "4. For suspected collisions, record the two objects, their measured "
        "or estimated extents, the available gap, and the required move.\n"
        "5. Recompile after the smallest geometry change and compare before "
        "and after renders.\n"
        "6. Verify the exported SVG/PDF has a tight, non-clipping bounding "
        "box and remains legible in both Beamer and Quarto.\n\n"
        "## Common failure patterns\n\n"
        "- wide labels centered between wide boxes;\n"
        "- timeline labels at adjacent dates with identical vertical offsets;\n"
        "- labels placed on the inside of curved edges;\n"
        "- `scale=` shrinking coordinates but not text;\n"
        "- arrowheads or braces clipped by a tight crop;\n"
        "- a diagram readable in isolation but too small on the final slide.\n\n"
        "A source-only inspection cannot produce a visual PASS. Without a "
        "successful compile and rendered inspection, report UNVERIFIED.\n"
    )


def native_replication_protocol(source_text: str) -> str:
    return (
        "<!-- Native reimplementation of .claude/rules/"
        f"replication-protocol.md at {SOURCE_COMMIT}; source SHA-256 "
        f"{digest(source_text)}. The upstream file credits the Material "
        "Passport concept in Academic Research Skills; no ARS text or schema "
        "is copied here. -->\n\n"
        "# Replication and numeric-claim protocol\n\n"
        "## Applicability\n\n"
        "Load for analysis code, generated tables/figures, manuscripts with "
        "numeric claims, and replication-package preparation.\n\n"
        "## Reproduce before extending\n\n"
        "Run the documented entry point in a clean environment before adding "
        "new specifications. Record the command, software versions, seed, "
        "input hashes or stable identifiers, and output locations. If the "
        "baseline does not reproduce, stop extensions and isolate the first "
        "divergent step.\n\n"
        "## Numeric-claim passport\n\n"
        "Maintain one YAML passport per paper and branch at "
        "`quality_reports/passports/<paper-slug>.yaml`. Each load-bearing "
        "claim records a stable id, manuscript location, displayed value, "
        "estimand, source script and invocation, source output, tolerance, "
        "last verification date, and status. Show inferred mappings to the "
        "author before writing them.\n\n"
        "Statuses are:\n\n"
        "- `PASS`: manuscript and source agree within the recorded tolerance;\n"
        "- `FAIL`: they disagree and no concrete explanation is established;\n"
        "- `EXPLAINED`: a named alternative specification, sample, edition, "
        "or rounding rule explains the difference;\n"
        "- `STALE`: a source or output changed after verification;\n"
        "- `UNVERIFIED`: the claim has no completed evidence check.\n\n"
        "An empty note never converts FAIL to EXPLAINED. A source output is a "
        "challenger, not an oracle: either the manuscript or the code may be "
        "wrong.\n\n"
        "## Audit workflow\n\n"
        "1. Extract numeric claims with precise manuscript locations.\n"
        "2. Locate the generating code and machine-readable output.\n"
        "3. Re-run only when authorized and safe; otherwise inspect existing "
        "outputs and mark execution UNVERIFIED.\n"
        "4. Compare using a domain-appropriate absolute or relative tolerance "
        "that is recorded before judging the result.\n"
        "5. Investigate sample, weights, transformations, missingness, "
        "clustering, degrees of freedom, comparison groups, seeds, and "
        "package-version drift for every mismatch.\n"
        "6. Update the passport and emit a claim-by-claim report with evidence "
        "pointers.\n\n"
        "## Gates\n\n"
        "Submission-ready work has no load-bearing FAIL, STALE, or UNVERIFIED "
        "claim. `$commit` may stop when touched manuscript or analysis files "
        "have affected FAIL/STALE passport entries, but committing still "
        "requires explicit user intent and any override must name the reason. "
        "`$review-paper` reports passport counts, and `$verify-claims` remains "
        "separate for citation and prose claims.\n"
    )


def migrate_rules(
    source: Path,
    target: Path,
    skill_names: list[str],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    rows = [
        "# Rule routing index",
        "",
        "Codex plugin references do not auto-apply Claude-style glob "
        "frontmatter. The applicable skill or `AGENTS.md` must load every "
        "matching rule explicitly.",
        "",
        "| Rule | Applies to |",
        "| --- | --- |",
    ]
    for source_file in sorted((source / ".claude" / "rules").glob("*.md")):
        source_text = source_file.read_text(
            encoding="utf-8", errors="replace"
        )
        paths, body = split_frontmatter(source_text)
        portable_paths = [
            path.replace(".claude/skills/", "skills/")
            .replace(".claude/rules/", "references/rules/")
            .replace(".claude/agents/", ".codex/agents/")
            for path in paths
        ]
        portable_paths = [
            path.replace(
                ".codex/agents/**/*.md", ".codex/agents/**/*.toml"
            ).replace(
                ".codex/agents/*.md", ".codex/agents/*.toml"
            )
            for path in portable_paths
        ]
        adapted = portable_text(body, skill_names)
        adapted = adapted.replace("](../skills/", "](../../skills/")
        adapted = adapted.replace("](../agents/", "](../agent-roles/")
        adapted = adapted.replace("](../references/", "](../")
        if source_file.name == "model-routing.md":
            target_text = native_model_rule(source_text)
        elif source_file.name == "tikz-prevention.md":
            target_text = native_tikz_prevention(source_text)
        elif source_file.name == "tikz-measurement.md":
            target_text = native_tikz_measurement(source_text)
        elif source_file.name == "replication-protocol.md":
            target_text = native_replication_protocol(source_text)
        else:
            target_text = ""
        applies = (
            ", ".join(f"`{path}`" for path in portable_paths)
            if portable_paths
            else "All academic tasks when relevant"
        )
        provenance = (
            f"<!-- Adapted from .claude/rules/{source_file.name} at "
            f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->"
        )
        applicability = (
            "## Applicability\n\n"
            f"Load this rule for: {applies}.\n\n"
            "Routing is explicit: the active skill or project `AGENTS.md` "
            "must select this rule.\n\n"
        )
        if not target_text:
            target_text = (
                f"{provenance}\n\n{applicability}{adapted.lstrip()}"
            ).rstrip() + "\n"
        target_file = target / "references" / "rules" / source_file.name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(target_text, encoding="utf-8")
        rows.append(
            f"| [{source_file.stem}]({source_file.name}) | {applies} |"
        )
        records.append(
            {
                "kind": "rule",
                "name": source_file.stem,
                "source": str(source_file),
                "source_sha256": digest(source_text),
                "target": str(target_file),
                "target_sha256": digest(target_text),
                "status": "semantic-baseline",
                "applicability": portable_paths,
            }
        )
    index_file = target / "references" / "rules" / "INDEX.md"
    index_file.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return records


def native_model_routing(source_text: str) -> str:
    return (
        "<!-- Native replacement for .claude/references/model-versions.md at "
        f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
        "# Codex model routing\n\n"
        "Do not encode retired model aliases in workflow prose. Prefer the "
        "parent model unless a narrow custom agent has a measured need for a "
        "different model. Express durable intent through "
        "`model_reasoning_effort`, sandbox mode, and role instructions.\n\n"
        "Before pinning a model, verify the current Codex model catalog and "
        "official documentation. If the catalog cannot be verified, inherit "
        "the parent model and record the choice as UNVERIFIED rather than "
        "guessing.\n\n"
        "Suggested durable routing:\n\n"
        "- high reasoning: causal-methods review, claim verification, "
        "editorial synthesis, adversarial audits;\n"
        "- medium reasoning: focused proofreading, translation, deterministic "
        "fix execution, environment capture;\n"
        "- low reasoning: mechanical inventory or format checks whose outputs "
        "are independently verified.\n\n"
        "Model choice never relaxes scientific, provenance, or verification "
        "gates.\n"
    )


def migrate_references(
    source: Path,
    target: Path,
    skill_names: list[str],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    rows = [
        "# Shared reference index",
        "",
        "| Reference | Portability |",
        "| --- | --- |",
    ]
    reference_root = source / ".claude" / "references"
    for source_file in sorted(reference_root.glob("*.md")):
        source_text = source_file.read_text(
            encoding="utf-8", errors="replace"
        )
        if source_file.name == "v2.0-backlog.md":
            target_file = (
                target
                / "docs"
                / "conversion"
                / "upstream-v2.0-backlog.md"
            )
            classification = "retained historical reference"
            target_text = (
                f"<!-- Retained from {source_file.as_posix()} at "
                f"{SOURCE_COMMIT}; source SHA-256 {digest(source_text)}. -->\n\n"
                + source_text.lstrip()
            )
        else:
            target_file = target / "references" / source_file.name
            if source_file.name == "model-versions.md":
                classification = "native rewrite"
                target_text = native_model_routing(source_text)
            elif source_file.name == "agent-fleet.md":
                classification = "native rewrite"
                target_text = native_agent_fleet(source_text)
            elif source_file.name == "audit-pet-peeves.md":
                classification = "native rewrite"
                target_text = native_audit_peeves(source_text)
            elif source_file.name == "scheduled-routines.md":
                classification = "native rewrite"
                target_text = native_scheduled_routines(source_text)
            else:
                classification = "native rewrite"
                adapted = portable_text(source_text, skill_names)
                adapted = adapted.replace("](../rules/", "](rules/")
                adapted = adapted.replace(
                    ".codex/agents/*.md", ".codex/agents/*.toml"
                )
                adapted = adapted.replace(
                    ".codex/agents/**/*.md",
                    ".codex/agents/**/*.toml",
                )
                target_text = (
                    f"<!-- Adapted from .claude/references/{source_file.name} "
                    f"at {SOURCE_COMMIT}; source SHA-256 "
                    f"{digest(source_text)}. -->\n\n{adapted.lstrip()}"
                )
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_text = target_text.rstrip() + "\n"
        target_file.write_text(target_text, encoding="utf-8")
        rows.append(
            f"| [{source_file.stem}]({target_file.name}) | "
            f"{classification} |"
        )
        records.append(
            {
                "kind": "reference",
                "name": source_file.stem,
                "source": str(source_file),
                "source_sha256": digest(source_text),
                "target": str(target_file),
                "target_sha256": digest(target_text),
                "status": "semantic-baseline",
                "classification": classification,
            }
        )
    index_file = target / "references" / "INDEX.md"
    index_file.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return records


def codex_skill_template() -> str:
    return """# Codex skill template

Use Codex's `skill-creator` for new skills. This file is a compact review
reference, not a replacement for that scaffolder.

```markdown
---
name: descriptive-kebab-case-name
description: Describe what the skill does and concrete phrases or situations
  that should trigger it.
---

# Workflow title

## Inputs

State required inputs, defaults, and the smallest blocking questions.

## Workflow

1. Inspect applicable `AGENTS.md` and source-of-truth artifacts.
2. Define outputs, invariants, and verification.
3. Execute the bounded workflow.
4. Verify outputs and distinguish PASS, FAIL, and UNVERIFIED.

## Safety and external actions

State data, permission, and publication boundaries. Require explicit user
authorization before commit, push, deploy, send, submit, or delete.

## Resources

Reference only resources this skill actually needs, with paths relative to
the skill directory.
```

Keep frontmatter limited to `name` and `description`, add
`agents/openai.yaml`, run `quick_validate.py`, and forward-test complex skills
with realistic prompts.
"""


def migrate_templates(
    source: Path,
    target: Path,
    skill_names: list[str],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    source_root = source / "templates"
    target_root = target / "assets" / "templates"
    for source_file in sorted(source_root.rglob("*")):
        if not source_file.is_file():
            continue
        relative = source_file.relative_to(source_root)
        target_file = target_root / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        source_text = source_file.read_text(
            encoding="utf-8", errors="replace"
        )
        if relative.as_posix() == "skill-template.md":
            classification = "native rewrite"
            target_text = codex_skill_template()
        else:
            classification = "direct port"
            target_text = portable_text(source_text, skill_names)
            target_text = (
                f"{provenance_comment(relative, source_text)}\n\n"
                f"{target_text.lstrip()}"
            )
        target_text = target_text.rstrip() + "\n"
        target_file.write_text(target_text, encoding="utf-8")
        records.append(
            {
                "kind": "template",
                "name": relative.as_posix(),
                "source": str(source_file),
                "source_sha256": digest(source_text),
                "target": str(target_file),
                "target_sha256": digest(target_text),
                "status": "semantic-baseline",
                "classification": classification,
            }
        )
    return records


def update_manifest(
    target: Path,
    shared_records: list[dict[str, object]],
) -> None:
    manifest_path = target / "docs" / "conversion" / "SOURCE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    components = [
        item
        for item in manifest["components"]
        if item.get("kind") not in {"rule", "reference", "template"}
    ]
    components.extend(shared_records)
    manifest["components"] = components
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_record(
    target: Path,
    records: list[dict[str, object]],
) -> None:
    by_kind: dict[str, int] = {}
    for record in records:
        kind = str(record["kind"])
        by_kind[kind] = by_kind.get(kind, 0) + 1
    lines = [
        "# Shared-resource conversion",
        "",
        f"- Source commit: `{SOURCE_COMMIT}`",
        "- Status: `semantic-baseline`",
        (
            "- Inventory: "
            + ", ".join(
                f"{count} {kind}(s)"
                for kind, count in sorted(by_kind.items())
            )
        ),
        "",
        "## Material revisions",
        "",
        "- Converted rule glob frontmatter into an explicit applicability "
        "section and generated `references/rules/INDEX.md`.",
        "- Rewrote skill invocations and Claude runtime paths for Codex.",
        "- Replaced the provider-specific model-version table with durable "
        "Codex routing principles.",
        "- Retained the upstream backlog as historical conversion evidence.",
        "- Reimplemented the invalid Claude skill template as a Codex skill "
        "template while directly porting the remaining academic templates.",
        "- Made template provenance comments extension-aware: TeX uses `%`, "
        "YAML uses `#`, and Markdown uses HTML comments.",
        "- Preserved `$skill` in Quarto code spans and escaped it as "
        "`\\$skill` when typeset by TeX.",
        "",
        "## Known behavior difference",
        "",
        "Codex does not auto-route arbitrary glob frontmatter from plugin "
        "reference files. Applicable skills and project `AGENTS.md` files "
        "must load matching rules from the generated index.",
    ]
    record_file = (
        target / "docs" / "conversion" / "shared-resources.md"
    )
    record_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    records: list[dict[str, object]] = []
    records.extend(migrate_rules(source, target, skill_names))
    records.extend(migrate_references(source, target, skill_names))
    records.extend(migrate_templates(source, target, skill_names))
    update_manifest(target, records)
    write_record(target, records)
    print(
        f"Migrated {sum(r['kind'] == 'rule' for r in records)} rules, "
        f"{sum(r['kind'] == 'reference' for r in records)} references, and "
        f"{sum(r['kind'] == 'template' for r in records)} templates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
