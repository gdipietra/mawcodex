# `submission-disclosures` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/submission-disclosures/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `7021c02bb2bf7bd9f411ca8260c56939146ae700f369d3348e9e33ececcab025`
- Target: `skills/submission-disclosures/SKILL.md`
- Target SHA-256: `fb9ecdb646c83ad675525e451ac711fbb9bca0fa032c8ef2737f4e132dcd98bc`
- Validation: `PASS`
- Forward test: PASS (FT-10)
## Material revisions

- Replaced provider-specific web tools with current primary-source policy
  verification and explicit retrieval evidence.
- Tightened author confirmation for AI use, CRediT, conflicts, and data access.
- Added contradiction handling and a firm draft-only/submission boundary.

## Behavior preserved

The four-statement block, journal matching, repository evidence inventory,
manuscript parity check, conservative fallback, and no-AI contradiction gate
remain.

## Behavior loss or limitation

No bundled policy profile is treated as current authority. A real journal-policy
lookup and author interview remain pending.
