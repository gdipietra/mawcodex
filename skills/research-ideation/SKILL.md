---
name: research-ideation
description: "Generate and rank three to five structured research questions, directional hypotheses, candidate estimands, designs, data requirements, assumptions, and falsification checks from a topic, phenomenon, or dataset description. Use for requests such as \"give me research ideas on X\", \"brainstorm questions about Y\", \"what could I study with this data?\", \"I need a paper idea\", or \"generate hypotheses\". One-shot and source-grounded; use $interview-me to refine one idea interactively."
---

# Research Ideation

Generate creative but defensible research directions. Distinguish ideas from
facts: a suggested dataset, literature connection, or identification strategy
is a hypothesis until verified.

## 1. Orient

Read the user's topic, phenomenon, dataset description, and referenced files.
Inspect relevant project papers and rules. For current literature, dataset
coverage, institutional settings, or software capabilities, search current
primary sources.

If the input is too ambiguous to produce meaningful ideas, ask one concise
scope question. Otherwise remain one-shot.

## 2. Generate a portfolio

Produce three to five questions spanning useful types where warranted:

- descriptive or measurement;
- correlational;
- causal reduced-form;
- mechanism;
- policy or welfare;
- structural, theoretical, or survey-experimental.

Tag each candidate with a paper type: `reduced-form`, `structural`,
`theory+empirics`, `descriptive`, `formal-theory`,
`survey-experiment`, or `unsure`. Use
[`methods-referee.md`](../../references/agent-roles/methods-referee.md) for
definitions; do not force every topic into a causal design.

For each question specify:

- precise research question and estimand;
- directional hypothesis or clearly labeled exploratory objective;
- proposed mechanism;
- design and comparison group;
- identifying assumptions;
- inference method and likely diagnostics;
- required variables, sample, timing, and access;
- threats, falsification tests, and plausible mitigations;
- nearest related work only when verified;
- feasibility and contribution;
- the cheapest decisive next check.

Do not manufacture quasi-experimental variation. If no credible design is
known, label it `DESIGN OPEN` rather than naming an estimator.

## 3. Verify hallucination-prone claims

Before ranking, verify:

- titles, authors, publication status, and findings of related papers;
- named dataset variables, years, populations, geography, access, and
  restricted-use status against official codebooks;
- policy dates and institutional details against primary sources;
- whether the proposed data structure supports the estimator;
- negative literature claims.

Follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the project `claim-verifier` custom agent; otherwise spawn a bounded,
isolated subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). Give it
claims, verification questions, and source pointers, not the ideation draft.

Use `PASS`, `PARTIAL`, `FAIL`, and `UNVERIFIED`. Correct or remove failed
claims. Phrase a literature gap as bounded by the search performed, never as
"no one has studied this" without compelling evidence.

An explicit `--no-verify` request records an opt-out and leaves claims visibly
`UNVERIFIED`.

## 4. Rank

Rank with separate dimensions:

- substantive contribution;
- identification credibility;
- data access and measurement feasibility;
- ethical and disclosure risk;
- execution cost;
- robustness to null or unexpected results.

Do not collapse these into false numerical precision. Explain tradeoffs and
select a lead candidate only when the evidence supports it.

## 5. Write the report

Save `quality_reports/research_ideation_<sanitized-topic>.md`:

```markdown
# Research Ideation: [Topic]
**Date:** YYYY-MM-DD
**Input and scope:** [...]

## Evidence and constraints
[verified literature, data, and institutional facts; unresolved claims]

## Candidate 1: [Question]
**Question type / paper type:**
**Estimand and hypothesis:**
**Mechanism:**
**Design and inference:**
**Data and access:**
**Assumptions and diagnostics:**
**Threats and mitigations:**
**Verified related work:**
**Feasibility / contribution:**
**Next decisive check:**

## Portfolio ranking
| Candidate | Contribution | Identification | Data feasibility | Risk | Next check |
|---|---|---|---|---|---|

## Post-flight verification
[status counts, source links, unresolved items]
```

## Boundaries

- Use [$interview-me](../interview-me/SKILL.md) to develop the selected idea.
- Use [$lit-review](../lit-review/SKILL.md) for an actual literature review.
- Do not claim data access, IRB feasibility, causal identification, or novelty
  from a brainstorming pass.
- Do not commit, submit, send, or publish the report without explicit user
  authorization.
