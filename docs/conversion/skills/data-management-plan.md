# `data-management-plan` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/data-management-plan/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `9b8567a18440498b811004c3cdc936687d787e52877e3998e666abb0ca19184c`
- Target: `skills/data-management-plan/SKILL.md`
- Target SHA-256 after semantic review: `69c2d41625241c12affdcf6580f569165d1f999d6afc1f9bff177ddab06d348b`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Converted fixed funder summaries into orientation only; current requirements
  must come from official primary sources or supplied solicitation materials.
- Repaired rule, skill, and reviewer links and isolated claim verification.
- Unknown policy, repository, threshold, IRB, or timeline facts remain
  `[CLARIFY:]` or UNVERIFIED.

## Behavior preserved

Funder-shaped sections, data sensitivity, access/sharing, FAIR metadata,
environment/replication commitments, checklist, and local draft remain.

## Behavior loss or limitations

The skill no longer labels an unverified generic draft compliant and never
submits it. Funder-specific forward testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS