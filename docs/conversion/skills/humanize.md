# `humanize` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/humanize/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `a1fa778cde5ea54a856788521d95c26cead25a431472ad695b50eddac436443e`
- Target: `skills/humanize/SKILL.md`
- Target SHA-256: `a8fca16290eff94d71f59f9c0023d5dbc129d8f37a1985ccbdd9f4c5ddc315e6`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Reframed the workflow as a prose-pattern audit, not an AI-authorship
  detector.
- Preserved ten style lenses while labeling thresholds as editing heuristics.
- Added a read-only isolated reviewer role, deduplication, venue-policy
  verification, and explicit limitations.

## Behavior preserved

Detect-and-flag behavior, severity filtering, structured reporting, and the
no-rewrite boundary remain.

## Behavior differences and loss

The upstream's authorship-sounding classifications and unsupported diagnostic
threshold claims were removed. The skill cannot infer AI use or policy breach.
