# `lit-review` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/lit-review/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `1242526dc11f9ebd6c168fb490a4af4c5f47f0918d1c90da29b268f0b3280dfa`
- Target: `skills/lit-review/SKILL.md`
- Target SHA-256: `a0b79abd1964644f9d80a72ba1f6d957f1ed9034c7a084e54a2c2b2d528b4767`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Added a reproducible search scope, inclusion log, version deduplication, and
  evidence-status table.
- Replaced generic web tool names with current search capabilities and primary
  source requirements.
- Ported CoVe to an isolated Codex verifier and prohibited guessed BibTeX
  fields or unbounded novelty claims.

## Behavior preserved

Structured search, thematic synthesis, methodological comparison, gap
identification, local report output, and citation extraction remain.

## Behavior differences and loss

The skill cannot claim exhaustiveness or full-text evidence when sources are
inaccessible. BibTeX output is restricted to verified metadata.
