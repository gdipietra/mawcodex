# `context-status` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/context-status/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `a0fadbfe21a28223364e77af6a4a1ab7a0bd31152dc2b820c4d327339b0ced77`
- Target: `skills/context-status/SKILL.md`
- Target SHA-256 after semantic review: `409858474e8d0886b1231bf3842f09ca3edb7ae5ae31d2b1d02c2d6cd21867b7`
- Mechanical changes: runtime name, skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Removed private cache inspection and tool-call-count context estimates.
- Uses supported runtime telemetry when available and otherwise reports
  UNAVAILABLE.
- Added plan, checkpoint, session-log, working-tree, and conversation-only
  preservation evidence.

## Behavior preserved

The task-health overview and preservation warning remain.

## Behavior loss or limitations

No fabricated context percentage or compaction prediction is supplied.
Runtime-telemetry forward testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS