# `scaffold-exercises` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/scaffold-exercises/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `cf21821ecc9972d37c288e96da7429e3a4722637121d24b718e48fe0ed394274`
- Target: `skills/scaffold-exercises/SKILL.md`
- Target SHA-256: `9876991f245d4dda65523cf7b3f87727b631fe11c1d9b75946ef0550679e35c2`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced command arguments with a resolved pre-flight contract.
- Added dataset-schema checks, deterministic simulation, code-execution status,
  and an explicit student/solution leakage scan.
- Replaced slash invocations with Codex skill references and added publication
  authorization boundaries.

## Behavior preserved

Analytical, empirical, and coding problem types, level calibration, separate
student/key files, worked solutions, and explainers remain.

## Behavior loss or limitation

Coding answers depend on an available runtime and otherwise remain
`DRAFTED — NOT RUN`. Classroom forward testing is pending.
