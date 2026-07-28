---
name: validate-bib
description: "Audit bibliography structure and citation usage across LaTeX, Quarto, and Markdown. Default mode finds missing, unused, malformed, and near-typo keys; semantic mode adds duplicate detection, DOI metadata verification, and citation-style consistency. It does not decide whether a cited source supports an attributed claim."
---

# Validate Bibliography

Cross-reference in-text citations against one or more BibTeX sources without
editing either.

## Modes and contract

- Default: structural checks.
- `--semantic`: structural plus duplicates, DOI metadata, and style.
- `--skip-doi`: omit network DOI checks and mark them `UNVERIFIED`.
- `--cite-claim`: display source metadata/abstract beside context, without
  judging support.

Honor bibliography and scan-path overrides in applicable `AGENTS.md` files.
Otherwise locate a unique root bibliography and scan relevant `.tex`, `.qmd`,
and `.md` files. Stop on ambiguous bibliography selection. Network failures or
unavailable sources affect only the relevant checks and are `UNVERIFIED`.

## Structural audit

1. Parse all bibliography entries and citation keys.
2. Extract citation keys from common LaTeX commands and Pandoc citation syntax.
3. Report:
   - cited keys absent from the bibliography: `CRITICAL`;
   - bibliography entries never cited: informational;
   - cited keys within edit distance two of an existing key: typo candidates;
   - duplicate keys or parse errors;
   - missing author, title, year, and journal/booktitle as appropriate;
   - malformed author lists and encoding;
   - implausible year outside 1900 through the current year; and
   - non-normalized DOI fields.
4. Write `quality_reports/bib_audit_structural.md`.

Do not use regular expressions alone when a BibTeX parser is available. Report
parser/tool version and files scanned.

## Semantic audit

Run structural checks, then:

### Duplicate/citation-drift detection

Flag pairs by:

- identical DOI or normalized title: Critical;
- identical normalized author/year/container: Medium; and
- normalized title-token Jaccard above 0.85: Low candidate.

For every pair show both keys, exact signal, citation locations, and a proposed
canonical key (most-used, then deterministic tie-break). Do not apply changes.

### DOI verification

For at most 50 uncached DOIs, query Crossref's official works endpoint while
honoring its rate-limit/retry guidance. Cache metadata and retrieval dates in
`quality_reports/.doi_cache.json`. Compare normalized first author, year, title,
and container:

- author or title mismatch: Critical;
- year mismatch: Medium;
- container/abbreviation mismatch: Low.

Metadata existence does not establish that the cited paper supports the
manuscript claim.

### Style consistency

Within each source file, summarize narrative versus parenthetical citation
forms. Flag unexplained local inconsistency at Low severity; legitimate
grammatical differences are not errors.

### Optional cite-claim context

For the most-cited works, place verified metadata or available abstract next to
the manuscript context. Label this `FLAG-ONLY`; use `$verify-claims` for an
evidence-grounded support/partial/contradict verdict.

## Semantic report and gate

Write `quality_reports/bib_audit_semantic.md`:

```markdown
# Bibliography Semantic Audit
**Bibliography:** [path/hash] · **Files:** [...]
## Check status
| Check | Critical | Medium | Low | PASS/FAIL/UNVERIFIED |
## Missing entries and parse errors
## Duplicate candidates
## DOI mismatches
## Style findings
## Recommended manual changes
```

Any Critical finding is FAIL. A network outage cannot turn a structural PASS
into overall PASS; report structural PASS with semantic DOI `UNVERIFIED`.
This skill only recommends edits.

Use `$review-paper` for manuscript review, `$audit-reproducibility` for numeric
claims, and `$verify-claims` for citation appropriateness.

## Provenance

Native Codex rewrite of the upstream `validate-bib` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
