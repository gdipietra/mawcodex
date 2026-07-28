# `checkpoint` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/checkpoint/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `b605194b23d3d253573586feb33e006ad0e77f4b76247cf302994b0078b06bff`
- Target: `skills/checkpoint/SKILL.md`
- Target SHA-256 after semantic review: `597abeb5283225dae96f8cd723c231b893180cfa4d6fae2f27a2580cff796689`
- Mechanical changes: hook path, rule path, skill invocation syntax, state path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced model aliases, positional arguments, task-list tool names,
  source-specific resume commands, and obsolete hook references.
- Distinguished project `MEMORY.md` proposals from Codex private memory and
  retained explicit approval before any memory write.

## Behavior preserved

The compact state snapshot, file pointers, decisions, open questions, next
actions, and resume prompt remain.

## Behavior loss or limitations

No provider-specific continue command is emitted. Resume behavior must be
tested in a real multi-task handoff.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS