# `did-event-study` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/did-event-study/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `3a7db439263d9fa3f41bd3d4695ffa4e4de144ceff6d33ab122b34005ad1b4dc`
- Target: `skills/did-event-study/SKILL.md`
- Target SHA-256 after semantic review: `729a76a3be929ffe6a6cac16fab83e06fb1dde3353acbf296d5a73fdbf33d0a3`
- Mechanical changes: rule path, skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Added a mandatory current-official-docs gate for installed package APIs and
  removed reliance on an internal triple-colon function.
- Replaced universal cross-engine `1e-6` claims with evidence-based tolerances
  and an explicit benchmark definition.
- Tightened overlap, estimand, comparison-group, sensitivity, and
  UNVERIFIED/outcome semantics.

## Behavior preserved

Canonical-package orchestration, group-time ATT design, doubly robust
starting point, TWFE benchmark-only posture, mandatory diagnostics,
sensitivity, uniform bands, aggregation, and graded credibility remain.

## Behavior loss or limitations

Version-specific API snippets are examples only until checked against official
docs. A benchmark dataset forward test is pending.

- Validation: PASS
- Forward test: PASS (FT-02)