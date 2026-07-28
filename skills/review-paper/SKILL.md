---
name: review-paper
description: "Review an academic manuscript in three modes: a comprehensive single pass, an adversarial critic-fixer loop, or a journal-calibrated simulated peer-review pipeline with R&R, stress, and reviewer-variance options. Integrates referenced-code and reproducibility checks unless explicitly skipped."
---

# Manuscript Review

Produce constructive, evidence-located manuscript criticism. The workflow
supports an economical single review, an iterative author-approved revision
loop, and a multi-role editorial simulation.

## Choose a mode

- default: one comprehensive report for most drafts;
- `--adversarial`: fresh-context critic/fixer rounds, at most five;
- `--peer <journal>`: editor plus blind domain and methods referees;
- `$seven-pass-review`: a separate seven-lens workflow for mature drafts; or
- `$respond-to-referees`: map an existing decision letter to a revision.

Peer options:

- `--r2` or `--r3`: continue a prior peer-review round with the same recorded
  roles/dispositions;
- `--stress`: two deliberately skeptical referees and a concern gauntlet;
- `--variance N`: three referees by default, at most five, with independently
  sampled dispositions and a decision distribution;
- `--no-novelty-check`: skip current-literature probing; and
- `--no-cross-artifact`: skip referenced-code/reproducibility integration.

Variance is mutually exclusive with stress and R&R continuation. R&R is capped
at round three. Stop on invalid combinations before spawning reviewers.

## Execution contract

- Require one readable `.tex`, `.qmd`, `.md`, or `.pdf` manuscript and read it
  end to end. Failed extraction or unread sections are `UNVERIFIED`.
- Never invent manuscript details, citations, prior work, results, or journal
  policy.
- Resolve journal profiles from the packaged reference when present; verify
  unstable journal policy/calibration claims using current official sources.
  An unknown or unverified profile blocks a journal-calibrated verdict.
- Named project custom agents are preferred. Otherwise use the matching
  portable roles:
  [`editor`](../../references/agent-roles/editor.md),
  [`domain-referee`](../../references/agent-roles/domain-referee.md),
  [`methods-referee`](../../references/agent-roles/methods-referee.md), and
  [`claim-verifier`](../../references/agent-roles/claim-verifier.md).
- Reviewers are bounded and read-only. Any proposed manuscript edit requires
  author approval before application.
- Commit, push, submission, or sharing requires explicit authorization.

## Shared pre-flight

Parse the manuscript path separately from options, resolve one exact file, and
record source hash, page/section coverage, available render capability, and
referenced `.R`, `.py`, or `.do` scripts.

When cross-artifact review is enabled:

1. run `$review-r` in isolated read-only contexts for referenced R scripts;
2. run `$audit-reproducibility` on the manuscript and available outputs; and
3. place any code bug or reproducibility FAIL that could invalidate a claim in a
   `Cross-Artifact Findings` section.

Missing referenced scripts or runtimes are `UNVERIFIED` and surfaced before a
peer pipeline begins. Follow
[`cross-artifact-review.md`](../../references/rules/cross-artifact-review.md).

## Default single-pass review

Assess:

1. argument structure and contribution;
2. estimand, identification assumptions, treatment timing, comparison group,
   and threats;
3. specification and inference, including clustering, selection, multiple
   testing, and economic magnitude;
4. literature positioning and cite-claim accuracy;
5. writing, notation, and limitations; and
6. standalone tables/figures and overall presentation.

Generate three to five demanding referee objections. Every Major concern needs
a precise location, evidence, consequence, feasible suggestion, and what would
change the reviewer's mind.

Write `quality_reports/paper_review_<name>_round1.md`:

```markdown
# Manuscript Review: [title]
**Source:** [path/hash] · **Coverage:** [...]
## Summary assessment
**Recommendation:** Strong Accept / Accept / Revise & Resubmit / Reject / UNVERIFIED
## Strengths
## Cross-artifact findings
## Major concerns
## Minor concerns
## Referee objections
## Section-specific comments
## Dimension ratings and evidence
## Unverified checks
```

Ratings must follow evidence; do not average incomparable dimensions into false
precision.

## Adversarial critic-fixer mode

### Round 0

Render/compile when possible and preserve a recoverable pre-review copy or
version-control diff without committing. A failed build is recorded before
edits.

### Review and proposal

Run the default review. Converge only when a fresh round finds zero unresolved
Major concerns and zero fatal objections. Otherwise draft concrete edits grouped
by severity and show them to the user.

Apply only the user's approved subset. Rerender/recompile, and roll back the
round's approved edits if they break the build. Then start a fresh isolated
reviewer that sees the updated manuscript, not the previous report or diff.

Use typed findings and deduplicate by location plus substance. Stop when:

- the convergence condition is met;
- five rounds complete;
- the user approves no fixes;
- the build fails and recovery cannot be verified; or
- the same concern recurs in alternating rounds, requiring author judgment.

Write `quality_reports/paper_review_<name>_FINAL.md` with round-by-round
findings, changes actually applied, build evidence, remaining concerns, and
`APPROVED`, `HALTED`, `ROLLED BACK`, or `UNVERIFIED`. “Approved” means the
automated critic found no blocker; it is not permission to submit.

## Peer-review pipeline

### Peer pre-flight

Before any subagent starts, report:

```markdown
## Pre-Flight Report — Peer Review
**Manuscript:** [path/hash/pages]
**Journal:** [short → verified full name]
**Profile:** [source/status/key calibration]
**Cross-artifact:** [scripts and PASS/FAIL/UNVERIFIED]
**Novelty probe:** enabled/disabled; source requirements
**Round:** fresh / r2 / r3 / stress / variance N
**Disposition plan:** [resolved]
```

Stop on unresolved manuscript, journal, prior-round, or cross-artifact inputs.

### 1. Editor desk review

Run an isolated editor on the abstract, introduction, methods overview,
headline results, verified journal profile, and cross-artifact evidence. It
returns `DESK REJECT` or `SEND OUT` with typed evidence.

If novelty probing is enabled, search current primary/official literature
sources. Put each apparent precedence claim through mandatory independent
post-flight verification before it affects the decision. Unverified novelty
leads are listed for manual checking, never asserted as prior work.

Write `quality_reports/peer_review_<paper>/desk_review.md`.

### 2. Referee assignment

For the default pipeline, assign different recorded dispositions from:
`STRUCTURAL`, `CREDIBILITY`, `MEASUREMENT`, `POLICY`, `THEORY`, and `SKEPTIC`.
Give each reviewer one critical and one constructive priority; stress mode uses
two critical priorities.

For R&R, reload the exact prior reports and recorded assignments, then classify
every previous concern as `Resolved`, `Partial`, or `Not addressed`.

For variance mode, sample N dispositions with replacement using a recorded
seed; when N is at least three include at least one skeptical reviewer. Report
the sampling method so this is a sensitivity exercise, not an empirical
estimate of real acceptance probability.

### 3. Blind parallel reviews

Launch domain and methods referees—or N referees in variance mode—in independent
contexts. They receive the same manuscript/profile evidence but cannot read one
another. Every Major concern must contain `change_my_mind`.

Write one report per reviewer in
`quality_reports/peer_review_<paper>/`.

### 4. Reduce and editorial decision

The editor reads typed referee findings, de-duplicates them, classifies each
Major issue as `FATAL`, `ADDRESSABLE`, or `TASTE`, and applies the documented
decision rule. The editor may downgrade findings but may not introduce a new
Critical blocker.

Any editor-only blocker is checked in a new isolated claim-verifier context. If
not verified, mark it `JUDGE-HALLUCINATED`, remove it as a blocker, and
recompute the decision.

Default/stress/R&R output:
`quality_reports/peer_review_<paper>/editorial_decision[_rN].md`.
Stress produces a gauntlet, not a simulated acceptance decision.

Variance output additionally includes:

- `decision_distribution.md`, making clear this is distribution across
  simulated dispositions;
- a concern-frequency table; and
- `editor_synthesis.md` with modal and dissenting concerns.

Do not turn N model reviews into claims about actual journal probabilities.

## Completion

Return the decision/recommendation, report paths, cross-artifact status,
verification status, remaining blockers, and only observed timing/resource
information. Use
[`journal-profile-template.md`](../../assets/templates/journal-profile-template.md)
to add a field-specific profile, with sources, when the packaged profile is
insufficient.

## Provenance

Native Codex rewrite of the upstream `review-paper` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT). The multi-role editorial
design retains upstream attribution to Hugo Sant'Anna's `clo-author` project;
the reviewer-variance discussion retains the upstream AgentReview research
reference.
