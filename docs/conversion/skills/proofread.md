# `proofread` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/proofread/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `4d32d6bec6798616d6f8e8a7e8cfac843307414ec94339d796fca83d58259dfd`
- Target: `skills/proofread/SKILL.md`
- Target SHA-256: `bc5406fe0e191bfe5211281bf1df068d7e82d9486eb310fed466c6339e03cd4e`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Ported the proofreader to a bounded read-only custom agent or portable-role
  fallback.
- Added current-render evidence for overflow, deduplication, math and quote
  preservation, and explicit `UNVERIFIED` handling.
- Retained separate report paths for TeX and Quarto.

## Behavior preserved

Grammar, typo, consistency, academic-quality, and overflow reporting remain
read-only.

## Behavior differences and loss

Overflow is no longer inferred as passed or failed from source alone. A current
render and logs are required for that lens.
