# `preregister` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/preregister/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `022dd080edc62fc9a98372f385f7f1eef565039aa9580809c75da653fe9fa8ba`
- Target: `skills/preregister/SKILL.md`
- Target SHA-256: `3e7f25f44978c99e19f6b35b0559cdc25eca2faf7fd70c699a3c7fce59176c65`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Added explicit data-collection and focal-outcome-access timing integrity.
- Required current official registry instructions before asserting field
  conformance, and preserved OSF, AsPredicted, and AEA RCT shapes as
  scaffolds.
- Ported power and citation checks to Codex skills and an isolated verifier
  role; added estimand, inference, multiplicity, and consistency gates.

## Behavior preserved

Prospective registry-shaped drafting, MUST/SHOULD/MAY labels, clarify markers,
readiness reporting, and local output remain.

## Behavior differences and loss

A plan written after focal outcomes were examined is labeled transparently
rather than called a preregistration. Registry submission is never automated.
