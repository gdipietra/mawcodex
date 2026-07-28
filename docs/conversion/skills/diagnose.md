# `diagnose` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/diagnose/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d897e566f3cb28daa5b71d5468b156ed1fbefc080d5076abee59f2c5af27ebb7`
- Target: `skills/diagnose/SKILL.md`
- Target SHA-256 after semantic review: `2e02bfb51cd28debf9e834fecf3533c336efa1f75ecdd3d2969b3dbc82f4f1be`
- Mechanical changes: context isolation, rule path, skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced source-specific orchestration with isolated hypothesis subagents and
  portable reporting.
- Removed universal tolerances and unsafe claims that history bisection is
  non-disruptive.
- Added clean disposable-worktree and confidential-report safeguards.

## Behavior preserved

Expected-versus-actual pinning, deterministic reproduction, minimal example,
hypothesis reduction, instrumentation, root-cause gate, minimal fix,
reverification, and prevention guard remain.

## Behavior loss or limitations

The skill will not edit on ambiguous causes or expose sensitive diagnostic
values. Representative R/Stata/Python bug forward tests are pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS