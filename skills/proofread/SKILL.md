---
name: proofread
description: "Perform a read-only proofreading pass over lecture or academic `.tex` and `.qmd` files, checking grammar, typos, terminology, notation, citation form, and render-visible overflow. Use for requests such as \"proofread\", \"check for typos\", \"look for grammar issues\", \"copy-edit this\", \"any writing errors?\", or a pre-release lecture check. Produces a report and never edits the source."
---

# Proofread

Review the requested source and report precise, actionable corrections without
changing it.

## Workflow

1. Resolve the user-supplied file. If the user says `all`, inspect lecture
   sources in `Slides/` and `Quarto/`. If no target is supplied, ask.
2. Read applicable project terminology, notation, and citation conventions.
3. Prefer the project `proofreader` custom agent. Otherwise spawn a bounded,
   read-only subagent in an isolated context using
   [`proofreader.md`](../../references/agent-roles/proofreader.md).
4. Check:
   - grammar: agreement, articles, prepositions, tense, fragments;
   - typos: spelling, duplicated words, replacement artifacts, missing words;
   - consistency: terminology, capitalization, notation, citation form;
   - academic clarity: ambiguity, unsupported promotional language, awkward
     constructions;
   - render evidence: LaTeX overfull boxes, clipping, or slide overflow.
5. For overflow, inspect a current render and logs when available. A source-only
   guess or missing renderer is `UNVERIFIED`, not an overflow finding or pass.
6. Deduplicate findings and require:

   ```text
   location | category | severity | current text | proposed local fix | evidence
   ```

   Preserve mathematical meaning and quoted text. Do not "correct" field terms
   solely because they are uncommon.
7. Save:
   - `.tex`: `quality_reports/<filename>_report.md`;
   - `.qmd`: `quality_reports/<filename>_qmd_report.md`.
8. Summarize totals by category, the most serious issues, rendered-check
   status, and unresolved questions.

Follow
[`proofreading-protocol.md`](../../references/rules/proofreading-protocol.md)
when it applies.

## Boundaries

- Do not edit source files.
- Use [$humanize](../humanize/SKILL.md) for repetitive or generic voice
  patterns, and $verify-claims for factual verification.
- Do not commit, publish, or send the report without explicit authorization.
