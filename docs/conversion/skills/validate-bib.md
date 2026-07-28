# `validate-bib` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/validate-bib/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `f9045d13966de0ea654ff4ac837772f26bcb00b69f7ae5d2d03d8b493a55a200`
- Target: `skills/validate-bib/SKILL.md`
- Target SHA-256: `c98dd27a66c377aa806211c4bc5c071c622fa0db9a0530e8b9e6f873a92ecd02`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced provider-specific fetch/search language with official Crossref
  capability, cache, retrieval dates, and rate-limit handling.
- Added parser/tool provenance, ambiguous-bibliography stops, partial
  structural-versus-network status, and no-auto-edit behavior.
- Repaired sibling skill references and clarified citation existence versus
  appropriateness.

## Behavior preserved

Structural citation-key checks, malformed fields, duplicate heuristics, DOI
metadata comparison, style consistency, and flag-only cite-claim context remain.

## Behavior loss or limitation

No network or BibTeX parser is guaranteed. A representative mixed LaTeX/Quarto
bibliography audit remains pending.
