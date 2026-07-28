# `devils-advocate` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/devils-advocate/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `1183d98b234d058f77eb099ef4f2bba4ece7a0d0e0dbcdf7dc4e52827f50983b`
- Target: `skills/devils-advocate/SKILL.md`
- Target SHA-256 after semantic review: `165f5e9573ffc2a3130db81708118bd1a5644129e517a29bb9a196de5e12464c`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Removed source-specific invocation syntax.
- Added rendered-artifact evidence and explicit UNVERIFIED handling when
  visual inspection is unavailable.
- Preserved a strictly read-only scope.

## Behavior preserved

Five-to-seven constructive challenges across ordering, prerequisites, gaps,
alternatives, notation, cognitive load, and book vision remain.

## Behavior loss or limitations

No visual claim is made from source text alone. Representative deck forward
testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS