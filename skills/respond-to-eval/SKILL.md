---
name: respond-to-eval
description: "Turn student course-evaluation text and numeric results into an evidence-bounded teaching-improvement plan by anonymizing inputs, clustering themes, weighting but not silencing low-frequency feedback, classifying each theme as Keep, Change, Investigate, or Out-of-scope, and mapping actions to course artifacts. Use for requests such as \"respond to my evals\", \"what do these course evaluations tell me?\", or \"turn teaching feedback into a plan\". Writes a plan but does not edit the syllabus or decks."
---

# Respond to Evaluations

Convert course feedback into a defensible revision plan. Frequency informs the
weight of a theme but does not determine whether it matters; one comment can
identify a serious accessibility, conduct, or comprehension problem.

## Privacy and scope

Course evaluations can contain sensitive personal information. Before
analysis:

- keep raw files local;
- remove student and third-party names, emails, IDs, accommodations, and other
  identifying details from working text;
- quote only the minimum needed and paraphrase when a quote could identify a
  respondent;
- do not attempt re-identification;
- do not send raw evaluations to external tools or services.

If extraction or analysis would cross the active workspace or use an external
service, explain that boundary and obtain explicit authorization first.

## Inputs

- one or more evaluation exports in CSV, TSV, text, Markdown, PDF, or DOCX;
- optional prior improvement plan;
- optional `--min-mentions <n>` threshold, default `2`;
- optional `--no-verify` for quote and target verification.

Use the appropriate local document capability for PDF or DOCX. If extraction
is unavailable, ask for a plain-text or CSV export and mark the source
`UNVERIFIED`.

## 1. Pre-flight

Record:

```markdown
## Pre-Flight
**Files and term:**
**Responses:** N total; M with usable text
**Response rate:** [if supplied]
**Numeric items:** [scale, mean, benchmark, missingness]
**Prior plan:** [path or none]
**Course artifacts:** [syllabus and controlling decks]
**Privacy actions:** [redactions and exclusions]
**Extraction status:** PASS / PARTIAL / UNVERIFIED
```

Do not infer representativeness when response rate, sampling, or benchmark is
unknown. Numeric averages do not overrule text, and text does not overrule
numeric evidence.

## 2. Build themes

1. Split responses into atomic, anonymized observations.
2. Allow one response to support multiple themes, but count each student at
   most once per theme.
3. Name themes in neutral instructor language: pacing, prerequisite gaps,
   assessment clarity, worked examples, relevance, accessibility, office
   hours, and so on.
4. For each theme record:
   - distinct-response mention count;
   - positive, negative, or mixed valence;
   - numeric corroboration or contradiction;
   - a short anonymized quote or faithful paraphrase;
   - uncertainty and possible alternative interpretation.
5. Tag themes below `--min-mentions` as `low-frequency`; never drop them.

Separate comments about teaching from comments driven by room, time slot,
institutional policy, or other constraints. Keep the latter visible.

## 3. Classify every theme

Assign exactly one:

| Label | Meaning | Required follow-up |
|---|---|---|
| **Keep** | Evidence supports preserving the current practice | State what not to break |
| **Change** | A concrete, supported problem has an actionable response | Name artifact, location, owner, and acceptance evidence |
| **Investigate** | Signal is real but cause or remedy is unclear | Name evidence to collect and a decision rule |
| **Out-of-scope** | Constraint is outside instructor control or conflicts with a justified objective | Record a respectful rationale and any mitigation |

Disagreement with the requested remedy is not grounds to discard the signal.
For example, retain a necessary proof objective while adding scaffolding if the
evidence concerns the on-ramp.

Map each `Change` to an existing syllabus section, deck, slide/frame, exercise,
assessment, or operating practice. If no target exists, create a clearly
labeled proposed target rather than inventing a location.

## 4. Compare the prior plan

If a prior plan was supplied, classify every promised action as `LANDED`,
`PARTIAL`, `NOT DONE`, or `UNVERIFIED`, with current evidence. Preserve the old
plan and show the new plan as a comparison; do not overwrite history.

## 5. Verify quotes and targets

Follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the project `claim-verifier` custom agent; otherwise spawn a bounded,
read-only subagent in an isolated context using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md).

Pass only anonymized quote snippets with local source pointers and proposed
artifact targets. Require it to confirm:

- the quote or paraphrase is faithful;
- the mention count is traceable;
- every cited syllabus section or slide/frame exists;
- prior-plan status has evidence.

Correct or remove failed items. `--no-verify` leaves them `UNVERIFIED`; it does
not permit fabricated quotes or targets.

## 6. Write the plan

Save
`quality_reports/teaching/YYYY-MM-DD_<course>_improvement-plan.md`:

1. course, term, instrument, response rate, and limitations;
2. privacy and extraction record;
3. numeric summary with benchmarks only when supplied;
4. prior-plan comparison;
5. theme matrix:
   `theme | mentions | valence | numeric evidence | class | target | source`;
6. protected `Keep` practices;
7. ordered `Change` list with owners and acceptance evidence;
8. `Investigate` list with collection plan and decision rule;
9. out-of-scope constraints and mitigation;
10. verification and unresolved checks.

Report totals by class, top three evidence-supported changes, open
investigations, and prior-plan completion. State:
`All themes classified; every Change mapped to a real or explicitly proposed
target` only when verified.

## Boundaries

- The syllabus and decks are read-only in this workflow.
- Use [$pedagogy-review](../pedagogy-review/SKILL.md) before implementing a
  deck-level change when pedagogical consequences are material.
- Do not compute new institutional ratings, infer demographic patterns, or
  claim causal effects of a teaching change from observational evaluations.
- Do not send, publish, or include evaluation material in a dossier without
  explicit authorization and a final privacy review.
