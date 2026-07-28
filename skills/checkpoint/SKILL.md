---
name: checkpoint
description: "Save a structured state snapshot before stopping or handing off. Captures the active plan, recent decisions, file pointers (with line numbers), open questions, and the next 1–3 actions into a checkpoint file under `quality_reports/checkpoints/`. Optionally proposes `[LEARN]` entries to add to MEMORY.md. Use when user says \"checkpoint\", \"save state\", \"snapshot before I stop\", \"where am I\", \"wrap up the session for handoff\", or before a long break / model switch / collaborator handoff. Companion to (NOT replacement for) the narrative session-log workflow."
---

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

<!-- Pattern adapted from Hugo Sant'Anna's clo-author v4.2.0 (github.com/hugosantanna/clo-author),
     used with permission. Original $checkpoint shape: project-level session handoff with
     state snapshot + memory updates. This implementation is reimplemented in original
     prose against this template's narrative-session-log + plan-on-disk + auto-memory
     architecture. Attribution credit: Hugo Sant'Anna. -->

# $checkpoint — Structured Session Handoff

Produce a state snapshot that the next task, collaborator, or fresh context can
resume from quickly. Narrative files under `quality_reports/session_logs/`
remain separate; `$checkpoint` writes the structured state: facts, file
pointers, and next actions.

## When to use

- Before a long break, task handoff, or end of a working day.
- Before auto-compaction would otherwise discard mid-plan context (paired with the PreCompact hook).
- Before handing off to a collaborator on the same repo.
- After completing a chunk of a multi-session plan, when "where am I" is the first question the next session will ask.

## When NOT to use

- For the narrative *what happened* — that lives in `quality_reports/session_logs/` (see `references/rules/session-logging.md`).
- For commit messages — those go through `$commit`, which writes its own
  structured commit body.
- For decisions about alternatives — those go to `templates/decision-record.md` via `quality_reports/decisions/`.

The three artifact types are complementary: **session-log = narrative**, **decision-record = trade-off captured**, **checkpoint = state to resume from**.

## Workflow

### PHASE 1 — Gather state

Read, in this order:

1. **Most recent plan** — `ls -t quality_reports/plans/*.md | head -1`. Extract: status (DRAFT / APPROVED / COMPLETED), title, top-level files-to-modify list, and any line that begins with "Open questions" / "Risks" / "Next".
2. **Most recent session log** — `ls -t quality_reports/session_logs/*.md | head -1`. Extract: latest "Next steps" or "Blockers" lines.
3. **Project `MEMORY.md`** — if the repository uses one, read existing
   `[LEARN]` entries so proposals do not duplicate them. Do not confuse this
   project file with Codex's private memory store.
4. **Git state** — `git log --oneline -20`, `git status -s`, `git branch --show-current`. Capture: current branch, last 5 subjects, uncommitted file count.
5. **Working files** — `git diff --stat HEAD` to see which files changed in this session (skip if branch is freshly cut; just say "no in-session edits").
6. **Active task plan** — capture the in-progress item and the next pending
   items from the current task plan, if one exists.

If any of these reads fails (file missing), record "(none on disk)" rather than fabricating content.

### PHASE 2 — Write the checkpoint

Write to `quality_reports/checkpoints/YYYY-MM-DD_<topic>.md`, where `<topic>`
comes from the user's topic argument. If none was supplied, derive it from the
active plan title and tell the user. The file uses this template:

```markdown
---
date: YYYY-MM-DD
branch: [current-branch]
plan: [path to active plan, or "(none)"]
session-log: [path to most recent session log, or "(none)"]
status: in_progress | paused | ready-to-merge
---

# Checkpoint — [short topic]

## Goal (one sentence)
[What this work is trying to accomplish]

## Where I am (one paragraph)
[Last completed step, current step, what's just-not-yet-done. Bullet points OK.]

## File pointers
[Concrete `path:line` references to where the next session should resume. Aim for 3–8.]
- `skills/checkpoint/SKILL.md:42` — body draft, needs trigger-phrase tightening
- `quality_reports/plans/[slug].md:135` — verification section to refresh after impl
- `CHANGELOG.md` — Unreleased section, v1.8.0 entry not yet drafted

## Recent decisions
[2–5 bullet points of *why* we did what we did this session. Things that wouldn't be obvious from the diff. Skip if none — do not pad.]

## Open questions
[Specific things you'd ask if someone else picked this up. Mark each as Q1, Q2 …]

## Next 1–3 actions
[Imperative form. Concrete. The next session opens this file and starts here.]
1. [...]
2. [...]
3. [...]

## Resume prompt
> Resuming from checkpoint `quality_reports/checkpoints/[filename]`. Read it, then continue with action 1.
```

Keep the file under ~80 lines. If state is too large for that, the plan file (not the checkpoint) is the right place; checkpoint is a thin index pointing back at the plan.

### PHASE 3 — Propose memory updates (skip if `--no-memory`)

Surface 0–3 candidate `[LEARN]` entries this session generated. **Don't write to MEMORY.md without user approval** — this is a propose-then-apply step:

For each candidate, present:

```
[LEARN:category] proposed: <one-line headline>
Why: <one sentence on what makes this non-obvious>
Apply where: <which future situations would benefit>
```

Only after explicit user approval, append accepted entries to the project's
committed `MEMORY.md` using its `[LEARN]` format. For machine-specific
information, recommend the repository's documented local state location; do
not write to Codex's private memory store from this skill.

Stay below 3 candidates. If you have more, the session was probably under-narrated — flag it and recommend a session-log update instead.

### PHASE 4 — Output summary

Print, to chat:

```
✓ Checkpoint saved: quality_reports/checkpoints/YYYY-MM-DD_<slug>.md
  Branch: <branch>     Status: <in_progress|paused|ready-to-merge>
  Active plan: <path or none>     Open questions: <count>
  Resume: open a fresh Codex task and paste the file's "Resume prompt"
```

If memory candidates were proposed, summarise which (if any) the user accepted.

## Cross-references

- [`session-logging.md`](../../references/rules/session-logging.md) — narrative
  companion.
- [`plan-first-workflow.md`](../../references/rules/plan-first-workflow.md) —
  plan conventions.
- [`decision-record.md`](../../assets/templates/decision-record.md) — records
  why an alternative was chosen.
- [`hooks.json`](../../hooks/hooks.json) — optional lifecycle-hook
  configuration. `$checkpoint` is appropriate when the configured pre-compact
  behavior reports an unpreserved draft.

## Examples

### Example 1 — End-of-day handoff
**User says:** "checkpoint v180-polisci"
**Actions:**
1. Read `quality_reports/plans/2026-04-27_v180-polisci-apr2026.md` (active, DRAFT).
2. Read `quality_reports/session_logs/2026-04-27_v180-polisci-apr2026.md`.
3. Capture: branch `feat/v1.8.0-polisci-apr2026`, 4 commits ahead of main, 8 files modified.
4. Write `quality_reports/checkpoints/2026-04-27_v180-polisci.md` with file pointers to the half-drafted `methods-referee.md` and the un-started `journal-profiles.md` poli-sci block.
5. Propose 1 candidate `[LEARN:scope]` entry on the linear-cost of disciplinary breadth.
**Result:** A fresh Codex task reads the checkpoint and starts at action 1.

### Example 2 — Mid-plan model switch
**User says:** "I want to hand these documentation edits to a fresh task —
checkpoint first"
**Actions:**
1. Capture state.
2. Write checkpoint with `status: paused`.
3. Skip memory proposal (small lift — just resuming on a different model).
**Result:** State is on disk; the next task reads the checkpoint and continues
without reconstructing the full plan.

## Troubleshooting

**No active plan found.** `$checkpoint` will still write a thin checkpoint with
`plan: (none)`, but should recommend creating a plan for non-trivial work.

**Topic missing.** Derive it from the active plan filename when possible. If
both are missing, ask the user for a short topic rather than fabricating one.

**Output too long.** Trim the "Recent decisions" and "Open questions" first. Plans go in plan files; the checkpoint should fit on a screen.
