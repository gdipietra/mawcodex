---
name: grant-proposal
description: "Scaffold a research-grant proposal for NSF, NIH, ERC, or a foundation by composing an $interview-me research spec, $data-management-plan, $capture-environment, and $lit-review outputs into a coherent draft and funder-requirements checklist. Use for requests such as \"draft a grant\", \"write a proposal\", \"NSF proposal\", \"NIH aims\", \"ERC application\", \"foundation grant\", \"specific aims\", or \"scaffold a grant proposal\". This is a drafting workflow, not a submission tool."
---

# Grant Proposal

Build a funder-shaped proposal from verified project artifacts. The research
spec supplies the science; the literature review supplies verified prior work;
the data-management and environment workflows supply specialist sections. Do
not invent an identification strategy, preliminary result, institutional fact,
budget, or sponsor requirement.

## Execution contract

- Treat the request and applicable `AGENTS.md` files as authoritative.
- Read every sibling skill used as a sub-workflow completely before applying it.
- Use bounded subagents only for separable sections or independent review.
- Treat missing tools, inaccessible sources, and skipped checks as
  `UNVERIFIED`, never `PASS`.
- Write only local draft artifacts. Submission, upload, sending, commit, push,
  or other publication requires a separate explicit user request.

## Inputs

- `--funder <nsf|nih|erc|foundation>` selects a scaffold. Infer only when the
  request clearly names a funder; otherwise ask. Default to `nsf` only when the
  user accepts that assumption.
- `--input <path>` names a research spec. Otherwise search
  `quality_reports/research_spec_*.md` and
  `quality_reports/specs/research_spec_*.md`.
- `--out <directory>` selects the output directory. Default to
  `quality_reports/grants/YYYY-MM-DD_<slug>/`.
- `--no-verify` records an explicit opt-out from citation verification. It does
  not turn unverified claims into verified ones.

## Funder scaffolds

Use these as section-name starting points, not as current sponsor policy:

| Funder | Typical scaffold |
|---|---|
| `nsf` | Project Summary; Project Description; Broader Impacts; Data Management and Sharing Plan; Facilities/Equipment; Budget Justification |
| `nih` | Specific Aims; Research Strategy; Human/Vertebrate Subjects if applicable; Data Management and Sharing; Facilities and Other Resources; Budget Justification |
| `erc` | Extended Synopsis; Scientific Proposal; CV/track record; Resources/Budget; Data Management |
| `foundation` | Project Summary; Statement of Need; Goals and Objectives; Methods; Evaluation; Budget; Sustainability |

Before calling any requirement, page limit, form name, or deadline current,
check the sponsor's official solicitation and application guide. Cite those
sources in the checklist. If official sources are inaccessible, mark the
affected rows `UNVERIFIED` and do not call the draft submission-ready.

## Workflow

### 1. Establish the source record

1. Resolve the funder and locate the research spec.
2. If no spec exists, stop and recommend
   [$interview-me](../interview-me/SKILL.md). Write nothing.
3. Extract the research question, directional hypotheses, estimand,
   identification strategy, data, sample, expected contribution, and any
   unresolved assumptions.
4. Inventory adjacent artifacts: an [$lit-review](../lit-review/SKILL.md),
   [$preregister](../preregister/SKILL.md), a research passport, and existing
   analysis outputs. Record paths and versions.

### 2. Draft the scientific sections

Map source content into the selected scaffold:

- **Summary or Specific Aims:** research question and two or three numbered
  aims grounded in the spec.
- **Background and Significance:** motivation and verified prior work. Do not
  add citations from memory.
- **Research Design and Methods:** state the estimand, treatment or exposure,
  comparison group, estimator, identifying assumptions, inference method, and
  diagnostics. Preserve the spec's language where precision matters.
- **Preliminary Results:** summarize only existing, traceable outputs.
  Otherwise use `[PRELIMINARY RESULTS: none yet — describe planned pilot]`.
- **Timeline and Milestones:** map every aim to at least one milestone.
- **Broader Impacts or Mission Fit:** frame for the verified sponsor
  requirements without making unsupported impact claims.
- **Budget Justification skeleton:** connect each line item to an aim; never
  fabricate rates, prices, effort, or institutional approvals.

For every required slot not supported by source material, use
`[CLARIFY: <specific question>]`. If available, apply the MUST/SHOULD/MAY
language in
[`requirements-spec.md`](../../assets/templates/requirements-spec.md).

### 3. Compose specialist sections

1. Apply [$data-management-plan](../data-management-plan/SKILL.md) to the
   funder and data inventory. Follow
   [`confidential-data.md`](../../references/rules/confidential-data.md).
   Never promise release of restricted or confidential data.
2. Apply [$capture-environment](../capture-environment/SKILL.md) to record the
   actual software, dependencies, compute, runtime, and storage environment.
   Do not claim a snapshot exists unless it was captured.

If a dependency is unavailable, add
`[DELEGATE: $skill-name — UNVERIFIED]` and list the section as unresolved.

### 4. Run the coherence gate

Check and report:

- aims to methods: each aim has a named method and estimand;
- methods to budget: each cost traces to a research activity;
- aims to timeline: every aim has a milestone;
- data plan to methods: named data agree and restricted data are not promised
  as open;
- claims to evidence: results and citations trace to source artifacts;
- format to solicitation: current official requirements are cited or marked
  `UNVERIFIED`.

### 5. Verify citations independently

When the draft cites prior work, follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Prefer the project `claim-verifier` custom agent; otherwise spawn a bounded,
isolated subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). Give the
reviewer the claims, verification questions, and source pointers, not the
proposal prose. Reconcile `PASS`, `PARTIAL`, `FAIL`, and `UNVERIFIED`
explicitly.

### 6. Write the deliverables

Write one Markdown file per section, `proposal_draft.md`, and `checklist.md`.
The checklist must include source paths, official requirement citations,
unresolved markers, the coherence gate, and verification status.

## Exit behavior

- If every required slot is supported, sponsor requirements are verified, and
  coherence passes, report `DRAFT READY FOR HUMAN REVIEW`.
- If any clarify, delegate, verification, or coherence item remains, report
  `INCOMPLETE — N items unresolved` and enumerate them.
- Never upload or submit the proposal. Never describe a draft as sponsor-ready
  solely because this workflow completed.

## Boundaries

- Develop the science with $interview-me, not here.
- Compute budgets with the PI and grants office, not here.
- Use exact sponsor forms for clinical-trial or other specialized protocols.
- This workflow flags likely page-limit pressure; it does not prove rendered
  page-limit compliance unless the final format was rendered and inspected.
