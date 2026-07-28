# `r-package-check` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/r-package-check/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `18071638cd86cce69c3057f3b439b0501b4e6f47240861e9180db255fee147db`
- Target: `skills/r-package-check/SKILL.md`
- Target SHA-256: `165b1345afdf86b9160309d403e2671f9210e5ae116148843d2af4f921c51831`
- Validation: `PASS`
- Forward test: PASS (FT-15)
## Material revisions

- Replaced the Claude monitor pattern with managed background execution and the
  runtime wait mechanism.
- Added exact toolchain/check evidence, partial UNVERIFIED states, working-tree
  drift reporting, and a portable package-review role.
- Preserved the no-version-bump/no-submission boundary.

## Behavior preserved

Documentation regeneration, tests, CRAN-style check, note triage, optional
coverage, source review, and the 0/0/explained release gate remain.

## Behavior loss or limitation

No cross-platform CRAN service is assumed or auto-run. A real R package release
gate has not yet been forward-tested.
