---
name: humanize
description: "Audit academic `.tex`, `.qmd`, or `.md` prose for repetitive, generic, or LLM-associated style patterns such as boilerplate transitions, cliché phrasing, punctuation overuse, symmetric paragraph shapes, stacked hedges, and promotional framing. Use for requests such as \"humanize\", \"does this sound generic?\", \"check for AI tells\", \"de-AI this draft\", \"audit my prose\", or a pre-submission voice review. Produces a read-only report and never infers authorship or rewrites the source."
---

# Humanize

Run a detect-and-flag voice audit. The goal is to help an author notice
repetitive or generic prose and make their own revisions. These patterns are
not a reliable detector of AI use and must never be presented as evidence of
authorship, misconduct, or policy violation.

## Execution contract

- This workflow is read-only on the source. Write only the audit report.
- Treat the user's supplied path or `all` selection as the complete scope.
- Prefer the project `humanize-auditor` custom agent. Otherwise spawn a
  bounded, read-only subagent in an isolated context using
  [`humanize-auditor.md`](../../references/agent-roles/humanize-auditor.md).
- Treat unread files, unavailable renderers, and skipped checks as
  `UNVERIFIED`.
- If venue policy matters, verify the current policy on the venue's official
  site. Do not generalize about journal rules from memory.

## Scope

- A supplied `.tex`, `.qmd`, or `.md` file: audit that file.
- `all`: audit prose files in the project root, `Slides/`, `Quarto/`, and
  `master_supporting_docs/`.
- Exclude bibliographies, code, generated output, vendored files, and scripts.
- If no target is supplied, ask for one.

Accept `--severity low|med|high`; default to all severities. The level filters
the report only and does not imply a probability of AI authorship.

## Detection lenses

Review context, not isolated word matches.

1. **Boilerplate transitions:** repeated connective phrases such as
   "Moreover", "Furthermore", "It is important to note", or "In conclusion"
   that add little logical content.
2. **Generic or cliché lexicon:** phrases such as "delve into", "navigate the
   landscape", "robust framework", "play a pivotal role", "shed light on", or
   "underscore the importance", especially when clustered.
3. **Punctuation patterns:** dense em-dashes, semicolon stacks, or repeated
   list punctuation. Flag overuse, not legitimate individual instances.
4. **Symmetric paragraph shapes:** three or more adjacent paragraphs with the
   same topic-sentence, examples, summary cadence.
5. **Tricolon repetition:** patterned three-item lists, especially stacked
   adjective triples.
6. **Stacked hedging:** phrases such as "might potentially" or "could possibly
   suggest" that obscure the actual uncertainty.
7. **Repeated contrast frames:** overuse or misuse of "not only X, but also Y".
8. **Formulaic openers:** repeated section-title restatements or identical
   "This paper/section..." openings.
9. **Compound-modifier density:** repeated chains such as "data-driven",
   "evidence-based", and "well-established" in one paragraph.
10. **Promotional or sycophantic framing:** unsupported self-praise such as
    "our groundbreaking approach" or "this important contribution".

Treat all thresholds as editing heuristics, not validated diagnostic cutoffs.
Concentration and repetition matter more than a raw word count.

## Workflow

1. Resolve the file list and count prose words.
2. Give the reviewer the text, line mapping, and ten lenses. Do not give it a
   desired verdict.
3. Require one row per finding:

   ```text
   line or paragraph | lens | severity | excerpt | why it distracts | revision direction
   ```

   A revision direction may say "remove", "state the logical connection", or
   "rewrite in the author's own words"; it must not supply a wholesale
   replacement paragraph.
4. Deduplicate overlapping findings. A phrase should not become multiple
   findings merely because it matches several lists.
5. Save `quality_reports/humanize_<filename>_report.md` with:
   - scope and files read;
   - per-lens counts by severity;
   - the finding table;
   - the three most concentrated passages;
   - a recommendation: local cleanup, section rewrite by the author, or no
     material pattern detected;
   - limitations stating that the audit cannot determine authorship.
6. Summarize counts and recommended next action in the conversation.

## Pairings

- Use [$proofread](../proofread/SKILL.md) for grammar and copy-edit findings.
- Use $verify-claims for citations and numeric claims.
- Use $review-paper for argument, methods, and contribution.

These reviews are complementary; none substitutes for the others.

## Boundaries

- Do not edit the source and do not provide a hidden rewrite mode.
- Do not label prose "AI-generated" or estimate an AI probability.
- Do not report an isolated legitimate phrase as a finding without explaining
  the contextual pattern.
- Do not infer a policy breach. Policy conclusions require a current,
  venue-specific primary source and human judgment.
