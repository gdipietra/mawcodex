# `power-analysis` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/power-analysis/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `8adb7baf2b106148213903cd0e4015682f91873814102b2177b25ef66dc6cbe9`
- Target: `skills/power-analysis/SKILL.md`
- Target SHA-256: `705518c2ffcdfd1829039d17fa80598c38ab7cce64bcd80cfc2acb5161a1f750`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Strengthened the ex-ante design record, estimand, inference, clustering,
  multiplicity, attrition, noncompliance, and moment-provenance requirements.
- Preserved analytical and simulation branches while requiring size checks,
  Monte Carlo uncertainty, seeds, saved code, and independent cross-checks.
- Added confidential-moment safeguards and explicit unreliable/unverified
  states.

## Behavior preserved

MDE, required-N, and power modes; clustered and multi-arm logic; simulation;
curves; tables; reproducible code; and preregistration handoff remain.

## Behavior differences and loss

No single package or language is assumed to exist. Calculations remain
`UNVERIFIED` until the chosen implementation runs and outputs reconcile.
