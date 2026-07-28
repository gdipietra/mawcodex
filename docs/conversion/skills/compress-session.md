# `compress-session` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/compress-session/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `cda761b84eb05a6ce01cd77ffc89ac1eb240ca4225414d2ec2b43dd1caec9806`
- Target: `skills/compress-session/SKILL.md`
- Target SHA-256 after semantic review: `f1977b3bf8f50c6a3d2ae0197d259a91977ffb40b68930105144be078de697bc`
- Mechanical changes: skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced slash commands, positional topic input, provider-specific reset
  language, and obsolete hook configuration.
- Context usage must be runtime-reported or UNVERIFIED.
- Memory promotion remains a separate explicitly authorized action.

## Behavior preserved

Decision distillation, discarded-dead-end capture, file pointers, open
questions, next actions, and reviewed on-disk handoff remain.

## Behavior loss or limitations

The hook only reminds; it never auto-invokes the skill. Compaction-resume
forward testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS