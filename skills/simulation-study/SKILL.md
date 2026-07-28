---
name: simulation-study
description: "Design and run a reproducible Monte Carlo study in R with a parameterized data-generating process, estimator and design grids, seeded replications, raw-result retention, Monte Carlo standard errors, and independent code review. Use to study bias, RMSE, coverage, size, power, or estimator comparisons."
---

# Monte Carlo Simulation Study

Build simulation evidence that remains auditable from the estimand through every
replication and summary statistic.

## Contract

- Follow
  [`simulation-conventions.md`](../../references/rules/simulation-conventions.md)
  and [`r-code-conventions.md`](../../references/rules/r-code-conventions.md).
- Keep raw data immutable. Write the simulation script under `scripts/R/` and
  generated outputs under `scripts/R/_outputs/`.
- Save per-replication results; a console-only summary is not evidence.
- Missing runtimes, failed runs, or skipped reviews are `UNVERIFIED`.
- Prefer the project `sim-reviewer`; otherwise use an isolated reviewer with
  [`sim-reviewer.md`](../../references/agent-roles/sim-reviewer.md).

## Phase 0: Design pre-flight

Before code, report:

```markdown
## Pre-Flight Report — Simulation Design
**Research question:** [...]
**Target estimand and truth:** [...]
**DGP:** [structure, fixed parameters, varied parameters]
**Estimator grid:** [estimator → estimand → returned est/se/CI]
**Design grid:** [...]
**Replications:** R; nominal coverage MCSE ≈ sqrt(.95*.05/R)
**Metrics:** bias, empirical SE, RMSE, coverage, size/power, failures
```

Stop for author input if the estimand, truth, null, or alternative is ambiguous.

## Phase 1: Parameterized DGP

Implement one function that receives `n` and parameters and returns both the
generated data and truth computed from those parameters. Truth must never be an
estimate from the simulated sample. Document treatment timing, heterogeneity,
selection, and error dependence when relevant.

## Phase 2: Estimator grid

Represent each estimator as a function returning at least:
`est`, `se`, `ci_lo`, `ci_hi`, and `converged`. State its target estimand.
Scoring an estimator against a different truth is a critical design error.

## Phase 3: Replication engine

- Set a recorded `YYYYMMDD` seed once.
- For parallel work, use a parallel-safe RNG such as L'Ecuyer-CMRG and seeded
  worker streams.
- One replication generates data, runs every estimator, and records one row per
  estimator/scenario.
- Retain failed/non-converged rows and their error class. Never silently drop
  them.
- Group summaries by every varying design dimension.

For a long run, use a managed background process with a durable log and the
runtime's supported wait mechanism. Do not poll with repeated sleeps.

## Phase 4: Metrics

Against per-row truth, report by estimator and scenario:

- bias and its Monte Carlo standard error;
- empirical standard error and RMSE;
- coverage and binomial Monte Carlo standard error;
- size under the null and power under alternatives, each with MCSE; and
- requested, completed, converged, and failed replication counts.

Do not interpret differences smaller than roughly two relevant MCSEs as stable
rankings.

## Phase 5: Figures and outputs

Produce transparent, dimensioned plots of bias/coverage (or the requested
metric) against design parameters, with reference lines at zero bias and nominal
coverage. Save:

- `<name>_raw.rds`;
- `<name>_summary.rds`;
- `<name>_summary.csv` and, when useful, `.tex`; and
- figure files with documented dimensions.

Include software/package versions and the script-to-output manifest.

## Phase 6: Independent review and rerun

Give only the generated script, design contract, and output manifest to the
simulation reviewer. Critical/High findings include truth-from-estimate,
estimand mismatch, coverage against the estimate, missing MCSEs, non-convergence
drops, seed misuse, or grid dimensions omitted from grouping.

Address approved Critical/High fixes, then rerun the affected phases. Results
remain `UNVERIFIED` until the corrected simulation completes and outputs are
reconciled. Report exact commands, exit status, replication counts, output
paths, and unresolved findings; never commit or publish without explicit
authorization.

## Provenance

Native Codex rewrite of the upstream `simulation-study` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
