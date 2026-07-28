---
name: seven-pass-review
description: "Run seven independent manuscript-review lenses in parallel—abstract, introduction, methods, results, robustness, prose, and citations—then reduce typed findings into a prioritized revision plan. Use for submission-ready or revise-and-resubmit papers that need broader coverage than a single review."
---

# Seven-Pass Adversarial Review

Use seven bounded, mutually independent review contexts so that one lens does
not anchor the others. This is intentionally more expensive than
`$review-paper` and is best reserved for mature drafts.

## Contract

- Require one readable `.tex`, `.qmd`, `.md`, or `.pdf` manuscript.
- Extract a PDF with an available trusted tool; failed extraction makes the
  review `UNVERIFIED`.
- Reviewers are read-only and blind to one another.
- Each reviewer rereads the manuscript and writes exactly one lens report.
- Prefer the named project agent where listed. Otherwise load its portable role
  from `../../references/agent-roles/`.
- This skill does not edit or submit the manuscript.

## Seven lenses

| # | Lens | Required questions | Preferred role |
| --- | --- | --- | --- |
| 1 | Abstract | Question, method, quantified result, contribution, consistency with body | bounded reviewer |
| 2 | Introduction | Hook, context, contribution, roadmap, magnitudes, literature placement | bounded reviewer |
| 3 | Methods/identification | Estimand, assumptions, comparison group, threats, inference | [`domain-reviewer`](../../references/agent-roles/domain-reviewer.md) |
| 4 | Results/tables | Standalone tables, units, uncertainty, magnitude, legibility | bounded reviewer |
| 5 | Robustness | Motivated diagnostics, placebos, power, heterogeneity, pre-empted threats | bounded reviewer |
| 6 | Prose | Clarity, hedging, active voice, cohesion, notation | [`proofreader`](../../references/agent-roles/proofreader.md) |
| 7 | Citations | Structural/semantic bibliography audit and cite-claim direction | bounded reviewer using `$validate-bib --semantic` |

## Phase 0: Pre-flight

Resolve the manuscript, record its hash and modification time, and create
`quality_reports/seven_pass_<stem>/`. If a prior synthesis exists, report
whether the manuscript changed; never claim to reuse a lens whose source
version differs.

## Phase 1: Fan out

Launch all seven reviews in parallel when capacity allows. Give each subagent:

- only the manuscript path, its lens rubric, and applicable project guidance;
- its unique output
  `quality_reports/seven_pass_<stem>/lens_<N>_<lens>.md`;
- a requirement to end with typed `findings` and `scorecard` blocks following
  the shared orchestration schema; and
- the rule that every `CRITICAL` or `MAJOR` finding needs exact evidence,
  location, consequence, and `change_my_mind`.

If capacity is limited, run bounded waves while preserving isolated contexts.
Do not let reviewers read each other's reports.

Lens 7 may use current primary sources for cite-claim verification. Any source
not actually accessed remains `UNVERIFIED`; bibliographic existence is not
evidence that an attributed claim is correct.

## Phase 2: Reduce, then judge

After all seven reports exist, parse their typed scorecards. Missing or malformed
reports are `UNVERIFIED` and prevent a `SUBMIT` verdict.

Reduce rather than conduct an eighth review:

1. de-duplicate findings by location and substance;
2. preserve every source-lens identifier;
3. surface cross-lens agreement and contradictions;
4. rank fixes by scientific consequence before prose polish; and
5. compute the verdict from the typed findings.

Apply the post-judge hallucination gate: a synthesis-introduced `CRITICAL` that
no lens raised must be checked by a fresh isolated verifier using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md). If it
cannot be verified, label it `JUDGE-HALLUCINATED`, drop it as a blocker, and
recompute the verdict.

## Synthesis output

Write `quality_reports/seven_pass_<stem>/_SYNTHESIS.md`:

```markdown
# Seven-Pass Review: [manuscript]
## Executive verdict
SUBMIT | REVISE-MINOR | REVISE-MAJOR | REJECT-AND-RESTART | UNVERIFIED

## Cross-lens CRITICAL issues
| ID | Lens(es) | Evidence | Consequence | Recommendation |

## MAJOR issues
## MINOR polish
## Per-lens scorecard
| Lens | Critical | Major | Minor | Score/10 | Status |

## Revision plan
1. [...]

## Contradictions between lenses
## Unverified checks
```

Any unresolved `CRITICAL` blocks submission. Report the seven lens paths, the
synthesis path, reviewers completed, and any missing evidence. Do not present
token or elapsed-time estimates as measured unless they were actually observed.

Use `$review-paper` for a cheaper single/adversarial pass. This workflow
recommends fixes but never auto-applies them and never replaces human
subfield judgment.

## Provenance

Native Codex rewrite of the upstream `seven-pass-review` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
