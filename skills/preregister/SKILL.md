---
name: preregister
description: "Draft a prospective OSF, AsPredicted, or AEA RCT Registry preregistration from a research spec or study description, with directional hypotheses, estimands, sample and stopping rules, exclusions, estimator and inference choices, power, and a readiness gate. Use for requests such as \"preregister this\", \"write a PAP\", \"OSF preregistration\", \"AsPredicted form\", \"AEA RCT registration\", or \"draft a pre-analysis plan\". Produces a local draft only and never uploads or submits it."
---

# Preregister

Turn a prospective design into a precise, timestampable commitment. Do not
retroactively label decisions made after examining focal outcomes as
preregistered.

## Inputs

- `--input <path>`: an $interview-me spec or other structured design file;
- `--style osf|aspredicted|aea-rct`;
- `--no-verify`: explicit citation-verification opt-out.

Without `--input`, ask for a concise study description and the current data
collection and outcome-access status. Never infer that outcomes are unseen.

## 1. Establish timing and integrity

Before drafting, record:

- whether data collection has started or ended;
- whether anyone on the analysis team has accessed focal outcomes, treatment
  contrasts, or related results;
- which decisions were made before versus after that access;
- the intended registry and registration time.

If the supplied material contains realized results, do not call the document a
preregistration. Offer a transparently labeled prospective analysis plan for
remaining decisions, with a disclosure of prior outcome access. Exploratory
analyses remain allowed when clearly labeled.

## 2. Select and verify the registry shape

Use the requested style, or propose:

| Signal | Starting style |
|---|---|
| General social-science or survey experiment | `osf` |
| Short experimental commitment | `aspredicted` |
| Economics randomized controlled trial | `aea-rct` |

Registry fields and policies change. Before claiming a field is required or a
draft is ready, consult the registry's current official instructions and
record the access date and URL. If they are inaccessible, use the packaged
scaffold but mark registry conformance `UNVERIFIED`.

When available, read only the selected section of
[`preregistration-template.md`](../../assets/templates/preregistration-template.md).
Do not merge registry forms.

## 3. Draft the selected form

Every style must include title, authors if supplied, date, version, timing and
outcome-access disclosure, and source-spec path.

Typical content:

- **OSF:** directional hypotheses; design; sampling and stopping; variables;
  estimands; analysis and inference; exclusions; missing data; multiplicity;
  exploratory analyses.
- **AsPredicted:** data status; hypothesis; dependent variable; conditions;
  analyses; exclusions; sample size and stopping; other commitments; study
  name.
- **AEA RCT:** intervention; primary and secondary outcomes; hypotheses;
  eligibility; target N; randomization unit and method; trial dates; ethics or
  IRB status; power; analysis plan; current trial status.

Annotate each field:

- `MUST`: current registry requirement or logically necessary commitment;
- `SHOULD`: important for interpretation or reproducibility;
- `MAY`: optional extension.

For every unsupported field, use `[CLARIFY: <specific question>]`. Never invent
an IRB number, trial date, sample size, variable, stopping rule, dataset,
approval, or registry requirement.

## 4. Design-quality gate

Check:

1. **Directional confirmatory hypotheses.** State a sign or a formal
   equivalence/non-inferiority region. Keep exploratory questions separate.
2. **Estimand and outcome.** Name the population, treatment contrast,
   outcome, aggregation, and timing.
3. **Estimator and inference.** Name the estimator, standard-error or
   randomization-inference procedure, clustering level, and multiplicity
   family.
4. **Numeric sample plan.** State target N and stopping rule. For prospective
   experiments, apply
   [$power-analysis](../power-analysis/SKILL.md) and carry its assumptions and
   MDE or required-N result into the draft.
5. **Exclusions and missing data.** State ex-ante rules and treatment of
   attrition, missing outcomes, and outliers.
6. **Consistency.** Randomization and analysis units agree or clustering is
   addressed; treatment arms, outcomes, hypotheses, and comparisons reconcile.
7. **Timing integrity.** The document accurately discloses data and outcome
   access.

Write a draft with visible `[CLARIFY:]` markers when needed, but report it
`INCOMPLETE`; never weaken the gate.

## 5. Verify external claims

If the rationale cites prior work, follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the `claim-verifier` custom agent; otherwise spawn a bounded, isolated
subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). Give it
the claims and source pointers, not the draft. Reconcile `PASS`, `PARTIAL`,
`FAIL`, and `UNVERIFIED`.

An explicit `--no-verify` request records an opt-out; it does not make
citations verified.

## 6. Write and report

Write
`quality_reports/preregistrations/YYYY-MM-DD_<slug>.md` with:

- registry style and official-instructions source;
- timing and outcome-access disclosure;
- source-spec hash or version;
- complete selected form;
- design-quality gate;
- citation-verification block;
- unresolved items.

Report:

```text
Preregistration draft: <path>
Style: <style>
Registry conformance: VERIFIED / UNVERIFIED
Timing integrity: PASS / DISCLOSURE REQUIRED / FAIL
Sections: <complete> complete; <clarify> unresolved
Power: PASS / UNVERIFIED / NOT APPLICABLE
Citations: PASS / PARTIAL / FAIL / UNVERIFIED / none
Next: resolve listed items, review the final text, then submit separately.
```

## Boundaries

- Do not upload, register, timestamp externally, send, or commit the draft
  without explicit authorization.
- Do not treat a document written after focal outcomes were examined as a
  preregistration.
- Use a registry's native form when its current requirements exceed this
  scaffold.
- A local save is not proof of registration or priority.
