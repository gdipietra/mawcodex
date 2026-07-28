---
name: interview-me
description: "Conduct a multi-turn research interview that turns a fuzzy idea into a structured specification covering the research question, motivation, hypotheses, estimand, identification, data, inference, expected results, contribution, and open risks. Use for requests such as \"interview me\", \"help me think through this idea\", \"I have a half-baked idea\", \"formalize this into a project\", or \"walk me through framing a study\". Saves a local spec; use $lit-review for a literature review and $research-ideation for one-shot ideation."
---

# Research Interview

Draw out the researcher's reasoning through a short conversation, then save a
traceable research specification. Be curious rather than prescriptive and do
not fill gaps with invented citations, data access, results, or institutional
facts.

## Interaction contract

- Treat the user's opening text as the initial topic. If they say "start
  fresh", begin with an open question.
- Ask one or two questions at a time in the conversation and wait for the
  response. Do not issue the whole questionnaire at once.
- Follow the user's answers. Probe the weakest live assumption rather than
  mechanically exhausting every prompt.
- Usually stop after five to eight exchanges; stop earlier if the design is
  already precise.
- Write the spec only after the researcher has seen and confirmed a compact
  summary of the proposed research question and design.

## Interview sequence

### 1. Phenomenon and stakes

- What phenomenon, puzzle, or decision are you trying to understand?
- Why does the answer matter, and to whom?
- What kind of paper seems plausible: reduced-form, structural,
  theory-plus-empirics, descriptive, formal theory, survey experiment, or
  unsure?

Use
[`methods-referee.md`](../../references/agent-roles/methods-referee.md) only
for the paper-type definitions. Record `unsure` without forcing a choice.

### 2. Mechanism and hypotheses

- What mechanism could generate the phenomenon?
- What does existing theory predict?
- State each confirmatory hypothesis directionally. Keep exploratory questions
  labeled separately.

### 3. Data and setting

- What data are available versus merely desired?
- What is the unit of observation, population, time period, and expected
  sample?
- Are any inputs restricted, proprietary, personally identifying, or governed
  by an IRB or data-use agreement?

Do not state access, variable availability, or coverage as fact without a
source or the researcher's explicit confirmation.

### 4. Estimand and identification

- What exact estimand answers the question?
- What treatment, exposure, or variation identifies it?
- What is the comparison group and timing structure?
- Which identifying assumption is load-bearing?
- What is the strongest alternative explanation or threat?
- What inference method, clustering level, or randomization inference matches
  the design?

For descriptive or theoretical work, replace causal-design questions with the
appropriate measurement, model, equilibrium, or falsifiability questions.

### 5. Expected results and contribution

- What result do you expect, and what would surprise you?
- What would each possible result imply?
- How would this differ from the nearest verified prior work?

Do not turn an expectation into a preliminary result. Do not make a negative
literature claim such as "nobody has studied this" without verification.

## Research specification

After confirmation, write
`quality_reports/research_spec_<sanitized-topic>.md`:

```markdown
# Research Specification: [Title]

**Date:** YYYY-MM-DD
**Researcher:** [only if supplied]
**Paper type:** [type or unsure]
**Status:** DRAFT / READY FOR DESIGN REVIEW

## Research Question
[One sentence]

## Motivation
[Why the question matters; sourced claims only]

## Estimand and Hypotheses
- **Estimand:** [...]
- **H1:** [directional prediction]
- **Exploratory questions:** [...]

## Design and Identification
- **Method:**
- **Treatment or exposure:**
- **Comparison group:**
- **Timing:**
- **Identifying assumptions:**
- **Inference:**
- **Diagnostics and falsification:**

## Data
- **Source and access status:**
- **Population and sample:**
- **Unit and time coverage:**
- **Outcomes, treatment, and controls:**
- **Confidentiality constraints:**

## Expected Results
[Expectations clearly labeled as expectations]

## Contribution
[Nearest verified literature and proposed advance]

## Open Questions and Unverified Claims
[One row per unresolved issue, with owner and next check]
```

## Citation post-flight

If Motivation or Contribution names prior work, datasets, or negative
literature claims, follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the `claim-verifier` custom agent; otherwise spawn a bounded, isolated
subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). Pass the
claims, questions, and source pointers, but not the draft prose.

- `PASS`: retain with evidence.
- `PARTIAL`: retain only with a visible qualification.
- `FAIL`: correct or remove.
- `UNVERIFIED`: label explicitly; never silently treat as true.

Skip only when there are no external claims, the user explicitly requests
`--no-verify`, or the user explicitly takes responsibility for later
verification.

## Decision records

When the researcher explicitly chooses among live alternatives—such as DiD
versus IV, administrative versus survey data, outcome definition, or sample
scope—write a separate record under
`quality_reports/decisions/YYYY-MM-DD_<topic>.md`. Include Status, Problem,
Options considered, Decision and rationale, Consequences, and Rejected
alternatives. Do not create a record for an uncontested default.

## Boundaries

- Use [$research-ideation](../research-ideation/SKILL.md) when the user wants
  several ideas generated in one pass.
- Use [$lit-review](../lit-review/SKILL.md) for a structured literature search.
- This skill does not analyze data, preregister, commit, submit, or contact
  anyone.
