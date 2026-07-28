# `capture-environment` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/capture-environment/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `a1033120e0001a635341a281ac350431037c33431fb76fb4398300ba23413597`
- Target: `skills/capture-environment/SKILL.md`
- Target SHA-256 after semantic review: `31b9038ad808edcd3b94a8b72d76e7e545eeacedf99a13b4e15cc3a01a0e86d9`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced positional inputs and all stale rule/skill links.
- Separated capture, isolated restore, numeric reproducibility, and
  byte-for-byte claims.
- Missing runtimes or registries now produce UNVERIFIED; image digests may
  never be invented.

## Behavior preserved

R, Python, and Stata detection; lockfile/session capture; seed inventory;
optional container recipe; and restore reporting remain.

## Behavior loss or limitations

A Dockerfile is no longer represented as proof of byte-identical results.
Multi-stack clean-restore forward tests are pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS