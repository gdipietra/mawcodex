# `audit-reproducibility` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/audit-reproducibility/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `8f14fedd2e1224e4b39015df2db189236b5a92bbbefed96e55b33dbf8d2a2a3d`
- Target: `skills/audit-reproducibility/SKILL.md`
- Target SHA-256 after semantic review: `2457d04e46a73f23c97a5d103877dcdb711189334893f47972081108ba37fb48`
- Mechanical changes: rule path, skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced positional inputs, slash invocations, stale paths, and the
  provider-specific long-job monitor.
- Required provenance-backed matches; magnitude similarity alone now yields an
  UNMATCHED candidate.
- Split PASS, QUALIFIED, FAIL, and UNVERIFIED so incomplete evidence cannot
  establish replication readiness.

## Behavior preserved

Numeric claim extraction, tolerance checks, passport mode, named-alternative
records, two-strikes escalation, and paper-versus-code symmetry remain.

## Behavior loss or limitations

No automatic fuzzy match can pass without provenance or user confirmation.
End-to-end forward testing on a real manuscript/output pair is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS