---
name: lit-review
description: "Conduct a structured, source-grounded literature search and synthesis with citation verification, thematic clustering, methodological comparison, and cautious gap identification. Use for requests such as \"find papers on X\", \"do a lit review\", \"what is the literature on...\", \"summarize what we know about...\", \"where is the gap?\", or \"review recent work on Y\". Produces a local review and verified BibTeX-ready records; never fabricates citations."
---

# Literature Review

Search, verify, and synthesize literature around the user's topic, named paper,
research question, or phenomenon. Separate what a source establishes from what
you infer.

## Execution contract

- Use current web search because publication records and working papers change.
- Prefer primary sources: the paper itself, publisher or journal record, DOI
  metadata, official working-paper series, author repository, and official
  dataset or codebook. Use secondary summaries only for discovery.
- Search project bibliographies and user-provided papers before duplicating
  work. Do not upload private papers or project text to external services.
- If a full text is unavailable, label the assessment `ABSTRACT-ONLY`,
  `METADATA-ONLY`, or `UNVERIFIED`; do not infer results from a title.
- External claims require linked evidence. Do not invent BibTeX fields.

## 1. Define the search

Record:

- the original query;
- scope and discipline;
- date range and language constraints;
- whether the goal is exhaustive, representative, or a rapid orientation;
- inclusion and exclusion criteria;
- any anchor paper or supplied corpus.

If the scope is too broad to search reproducibly, narrow it with one concise
question before proceeding.

## 2. Search in layers

1. Inspect project `.bib` files and
   `master_supporting_docs/supporting_papers/`.
2. Follow references and citations from verified anchor papers.
3. Search current official publisher, DOI, journal, working-paper, and author
   records.
4. Search relevant official repositories or registries for unpublished and
   recent work.
5. Keep a search log with query, source, date, result count where available,
   and inclusion decision.

Deduplicate preprint, working-paper, and published versions. Treat a published
version as controlling unless the research question specifically concerns an
earlier version; record material version differences.

## 3. Build an evidence table

For every included paper, record:

- verified title, authors, year, venue or series, DOI or canonical URL;
- publication status and version date;
- theory or mechanism;
- data, sample, setting, and period;
- estimand and identification strategy;
- inference method;
- main finding, including units and uncertainty when the source reports them;
- limitations stated by the authors;
- relevance to the user's question;
- evidence status: full text, abstract only, metadata only, or unverified.

Do not report an effect size unless it appears in the source you inspected.
Do not equate a working paper with a final published result.

## 4. Synthesize

Organize the review around:

- theoretical mechanisms;
- empirical findings and where they agree or conflict;
- methodological innovations and identifying assumptions;
- differences in population, treatment, outcome, and measurement;
- open debates;
- research opportunities.

A "gap" is an evidence-bounded opportunity, not a claim that no paper exists.
Use language such as "the reviewed set contains limited evidence on..." and
state the search boundary. Rank candidate gaps by contribution, feasibility,
and identification risk.

## 5. Verify independently

Follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the project `claim-verifier` custom agent; otherwise spawn a bounded,
isolated subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). Pass:

- the claims table;
- one verification question per citation, result, dataset claim, and negative
  literature statement;
- DOI, canonical URL, and local-source pointers.

Do not pass the draft synthesis. Reconcile the verifier's evidence into
`PASS`, `PARTIAL`, `FAIL`, or `UNVERIFIED`. Correct or remove failed claims.
An explicit `--no-verify` request records an opt-out; it does not permit
unverified citations to appear as fact.

## 6. Write the report

Save `quality_reports/lit_review_<sanitized-topic>.md`:

```markdown
# Literature Review: [Topic]
**Date:** YYYY-MM-DD
**Query and scope:** [...]

## Search and inclusion record
[sources, queries, dates, criteria, limitations]

## Evidence map
| Paper | Status | Design/data | Main source-supported result | Relevance |
|---|---|---|---|---|

## Synthesis
### Theory and mechanisms
### Empirical evidence
### Methods and identification
### Debates and heterogeneity

## Evidence-bounded gaps and opportunities
[ranked list with search-boundary caveats]

## Suggested next steps

## References and BibTeX
[verified records only; unresolved fields visibly marked]

## Post-flight verification
[PASS/PARTIAL/FAIL/UNVERIFIED counts and unresolved claims]
```

Generate BibTeX from verified metadata. If a required field cannot be checked,
omit it or mark it for manual completion; never guess.

## Exit behavior

- Report the number of candidates screened, papers included, evidence-status
  breakdown, and unresolved checks.
- A missing search capability or inaccessible corpus yields a scoped
  `UNVERIFIED` review, not a complete-review claim.
- Do not send, submit, post, or commit the report without explicit user
  authorization.
