# `pedagogy-review` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/pedagogy-review/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `929dcac39b2daad53d3303d884994e7e449d5280800d69e215a32df23d69fcd9`
- Target: `skills/pedagogy-review/SKILL.md`
- Target SHA-256: `76e53f6e39bfa5d473d88a4a6b33841e4d61e3ad9af2f1b5dfca796fdb20e4a0`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced Claude agent invocation with a read-only project custom agent and
  portable-role fallback.
- Added source/render freshness, student-perspective evidence, finding
  deduplication, and PASS/PARTIAL/FAIL/UNVERIFIED statuses.
- Preserved a strict no-edit boundary.

## Behavior preserved

The thirteen-pattern and deck-level pedagogical review, local report, and
prioritized recommendations remain.

## Behavior differences and loss

Visual evidence is not treated as checked unless a current render is actually
inspected. Named-agent execution remains to be forward-tested.
