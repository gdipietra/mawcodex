# `respond-to-eval` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/respond-to-eval/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d01eedccb789a418c0383458e1fe8ae6e81548aba474dc0d69da106bb167ad8c`
- Target: `skills/respond-to-eval/SKILL.md`
- Target SHA-256: `3adf21a019efad2d768d537b81c28a7155da21010e433663802af2bd580e75b0`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Added anonymization, no-reidentification, local-data, extraction, and
  external-tool privacy boundaries.
- Preserved frequency-weighted theme clustering while preventing low-frequency
  accessibility, conduct, or comprehension signals from being silenced.
- Ported quote, count, and target verification to an isolated read-only Codex
  verifier and kept comparison versions of prior plans.

## Behavior preserved

Pre-flight, theme matrix, Keep/Change/Investigate/Out-of-scope classification,
artifact mapping, improvement plan, and read-only teaching-material boundary
remain.

## Behavior differences and loss

Raw identifiable quotes are not propagated into reviewer contexts or reports.
The skill plans changes but never edits or externally shares course materials.
