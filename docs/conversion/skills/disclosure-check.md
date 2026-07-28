# `disclosure-check` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/disclosure-check/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `9e2ea3484792480cada3e8191e963086a81d643cf9a474465a352bf9ad2f2286`
- Target: `skills/disclosure-check/SKILL.md`
- Target SHA-256 after semantic review: `37a1bfb30362f1a9e20ad2cb16a9cfe63b251881b571200cb0e1c27c6cee2886`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Removed the release-authorizing generic threshold and required a controlling
  signed provider/IRB rule source.
- Generic scans now return UNVERIFIED and block release; official review
  remains authoritative.
- Added authorized-environment, no-upload/no-delegation, redaction, and
  skipped-parser safeguards.

## Behavior preserved

Small-cell, complementary suppression, dominance, exact-count, identifier,
rounding, remediation, and staged-output reporting remain.

## Behavior loss or limitations

No generic profile can produce PASS or export clearance. A synthetic-output
forward test and provider-specific human review are pending.

- Validation: PASS
- Forward test: PASS (FT-04)