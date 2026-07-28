---
name: context-status
description: "Report the current task's observable context and preservation state: active plan, recent session log or checkpoint, working-tree state, and whether context-usage telemetry is available. Use when the user asks about context health, compaction readiness, or what state is safely on disk."
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

# $context-status — Check Session Health

Show evidence-backed task status: available context telemetry, active plan,
recent state artifacts, working-tree state, and preservation gaps.

## What This Skill Shows

1. **Context telemetry** — exact value only when the runtime exposes one
2. **Active plan** — current plan file and status
3. **State artifacts** — most recent session log, checkpoint, or compression
4. **Preservation evidence** — what is on disk versus only in conversation
5. **Working tree** — branch and uncommitted-file summary

## Workflow

### Step 1: Check available task telemetry

Use the runtime's supported task or goal-status capability when it exposes
token or context usage. Do not infer a percentage from tool-call count, message
count, or private cache files. If no supported telemetry is available, report:
`Context usage: UNAVAILABLE — no supported measurement exposed`.

### Step 2: Find Active Plan

Inspect `quality_reports/plans/` and read the newest applicable plan. Record its
declared status and first incomplete action. Missing files are `(none on disk)`.

### Step 3: Find Session Log

Inspect the newest files in `quality_reports/session_logs/` and
`quality_reports/checkpoints/`. Record their paths and timestamps.

### Step 4: Inspect repository state

Read the current branch and working-tree summary without modifying either.

### Step 5: Report status

Format the output:

```
📊 Session Status
─────────────────────────────────
Context Usage:  [runtime-reported value | UNAVAILABLE]
Compaction:     [runtime-reported state | UNKNOWN]

📋 Active Plan
File:   quality_reports/plans/YYYY-MM-DD_description.md
Status: [draft | approved | in_progress | completed]
Task:   [current unchecked task or "none"]

📝 State on disk
Session log:  <path or none>
Checkpoint:   <path or none>
Working tree: <clean | N modified paths>

✓ Preservation Check
  • Active plan: [saved | absent]
  • Resume checkpoint/compression: [saved | absent]
  • Conversation-only decisions: [none found | list | UNVERIFIED]
  • Optional compaction hooks: [configured | missing | UNVERIFIED]
```

## Notes

- Never state that all important state is preserved merely because hooks are
  configured.
- If material decisions exist only in the conversation, recommend
  `$checkpoint` or `$compress-session`.
- Missing telemetry is UNAVAILABLE, not evidence that compaction is near or
  far away.
