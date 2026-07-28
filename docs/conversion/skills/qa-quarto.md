# `qa-quarto` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/qa-quarto/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `3cc81b6937345d1c1d384df9f80775a698a4ed3eee49e76edb40536c4d9168ca`
- Target: `skills/qa-quarto/SKILL.md`
- Target SHA-256: `b05b14af2ea5699c8ab33111289729d4d1810d86dc016250ad963fe2d3148e8c`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced Claude critic/fixer dispatch with isolated read-only and
  workspace-write Codex roles with non-overlapping scope.
- Defined content, notation, overflow, figures, navigation, layout, and
  provenance hard gates across current renders and viewport evidence.
- Preserved loop-until-dry, two-strikes escalation, five-round cap, comparison
  versions, and final report.

## Behavior preserved

Adversarial Beamer-to-Quarto parity review, iterative fixes, rerendering, and
independent re-audit remain.

## Behavior differences and loss

The reference is not treated as requiring pixel identity; documented
format-appropriate improvements are allowed. Renderer and browser integration
still require forward testing.
