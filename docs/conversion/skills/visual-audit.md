# `visual-audit` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/visual-audit/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d31724a02b3cc9a85f6b3224ba434cb9cfb39edb2ef61cb9b912b93c45fba4e3`
- Target: `skills/visual-audit/SKILL.md`
- Target SHA-256: `cabe3afece9933a535a0c83ac508634764008e3854bc8db22c7276ce7e88a73a`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Mapped review to the project `slide-auditor` or portable role.
- Required recorded rendering plus inspection of every rendered slide for PASS,
  with explicit source-only UNVERIFIED status.
- Expanded evidence, accessibility, per-slide status, and no-edit/deploy
  boundaries while preserving spacing-first recommendations.

## Behavior preserved

Overflow, font, box fatigue, spacing, layout, alignment, and legibility checks
remain, with severity-ranked per-slide recommendations.

## Behavior loss or limitation

No renderer/browser is assumed. A visually inspected Beamer and Quarto forward
test remains pending.
