---
name: power-analysis
description: "Compute ex-ante statistical power, required sample size, or minimum detectable effect for a documented study design, with analytical support for two-arm, clustered, and multiple-arm experiments and simulation support for DiD, event-study, IV, panel, or nonstandard estimators. Use for requests such as \"power analysis\", \"MDE\", \"minimum detectable effect\", \"how large a sample do I need?\", \"is this design powered?\", or an $preregister power section. Produces reproducible code, tables, curves, and a registry-ready methods paragraph."
---

# Power Analysis

Treat power as an ex-ante design calculation. Fix two of effect size, sample
size, and target power, then solve for the third. Never back out "observed
power" from a realized estimate.

## Inputs

Accept:

- `--mode mde|n|power`;
- `--design rct|cluster|multiarm|sim`;
- `--input <research-spec-or-design-file>`;
- a user-specified output directory.

If a flag is absent, infer it only from explicit design evidence; otherwise
ask. Before computing, collect:

- estimand, outcome type, one- or two-sided test, and alpha;
- two of effect size, sample size, and power;
- raw effect and outcome scale or a standardized effect;
- baseline mean and SD, or baseline proportion, with provenance;
- allocation ratio;
- randomization and analysis units;
- for clustering: ICC, cluster-size distribution, and number of clusters;
- arms, primary outcomes, comparison family, and multiplicity procedure;
- anticipated attrition, noncompliance, missingness, and take-up assumptions;
- estimator and inference method planned for the final analysis.

Defaults such as alpha `0.05`, power `0.80`, and 1:1 allocation may be proposed
but must be shown as assumptions. Never guess an SD, ICC, attrition rate, or
number of comparisons.

## 1. Pre-flight design record

Echo a compact record before calculation:

```text
Estimand/outcome:
Design and analysis unit:
Estimator/inference:
Solving for:
Fixed quantities:
Alpha and sidedness:
Allocation:
Clustering:
Multiplicity:
Attrition/noncompliance:
Moment provenance:
```

Stop for a material ambiguity. A power result for the wrong estimand or
analysis unit is not useful.

## 2. Analytical designs

Use a documented, reproducible implementation in R, Stata, or Python that is
available in the project. Save the code rather than returning a console-only
number. Record software and package versions.

For a simple two-arm normal approximation, the MDE is based on:

```text
MDE = (critical value for alpha + critical value for beta) * SE(effect)
```

Build `SE(effect)` from the outcome variance, group sizes, allocation, and
design. Do not apply the formula when a binary, small-sample, noncompliant, or
nonlinear design requires a different calculation.

For equal-size clusters, use the design-effect approximation
`1 + (m - 1) * ICC` only when its assumptions are defensible. When cluster
sizes vary materially, use a method that accounts for that variation. Report
both total observations and clusters; few-cluster inference cannot be repaired
by a large within-cluster sample.

For multiple arms:

- define the comparison family explicitly;
- compute the number of comparisons from that family, not merely the number of
  arms;
- apply the chosen multiplicity procedure;
- report per-comparison and familywise targets separately.

Sweep a meaningful grid of sample size or clusters by effect size to support a
power curve and sensitivity table. Include attrition-adjusted recruitment
targets separately from the analysis sample.

## 3. Simulation for nonstandard designs

Use simulation when the actual estimator or dependence structure has no
credible closed-form approximation—for example staggered DiD or event studies,
IV with weak first stages, serially correlated panels, censored outcomes, or
complex randomization.

Follow
[`simulation-conventions.md`](../../references/rules/simulation-conventions.md)
and the [$simulation-study](../simulation-study/SKILL.md) pattern:

1. Specify a seeded, parameterized DGP that encodes the design, treatment
   assignment, missingness, dependence, and hypothesized effect.
2. Use the estimator and standard-error procedure planned for the study.
3. Under the null DGP, estimate empirical size before trusting power.
4. Under each alternative, estimate power as the rejection share.
5. Report Monte Carlo standard errors,
   `sqrt(p * (1 - p) / R)`, for size and power.
6. Sweep the design quantity being chosen and save per-replication results in
   a documented derived-output location.

A simulated power result without a size check, Monte Carlo uncertainty, seed,
or saved code is `UNVERIFIED`.

## 4. Verify

Check:

- inputs match the research spec and planned estimator;
- units are consistent;
- raw and standardized effects convert correctly;
- allocation totals and cluster counts reconcile;
- multiplicity uses the stated family;
- rounding does not reduce the design below the target;
- the plotted values match the result table;
- simulation size is plausibly close to nominal, with uncertainty considered.

Where practical, cross-check one central result with a second independent
implementation. Disagreement is a blocker until explained.

## 5. Deliverables

Write under `quality_reports/power/`:

- `power_<slug>.md`;
- `power_curve_<slug>.png` when plotting is available;
- a reproducible `.R`, `.do`, or `.py` script in the project's documented
  analysis-script location;
- saved simulation results when simulation mode is used.

The report must include:

| Quantity | Required content |
|---|---|
| Design | estimand, test, estimator, inference |
| Error rates | alpha, sidedness, target power |
| Moments | mean/SD or proportion and provenance |
| Allocation | treated/control or arm shares |
| Clustering | ICC, cluster-size assumptions, cluster count, design effect if used |
| Multiplicity | comparison family and correction |
| Sample | analysis N and recruitment N after attrition |
| Result | MDE, required N, or achieved power in raw and standardized units |
| Simulation | replications, seed, size, power, and MCSE |

Include a concise methods paragraph suitable for a preregistration, but label
all design assumptions and sources. When called from
[$preregister](../preregister/SKILL.md), return the paragraph and result row to
that workflow.

## Exit behavior

- Report `PASS` only when the code ran, outputs were inspected, and checks
  reconciled.
- Report `UNRELIABLE` when simulation size is materially inconsistent with the
  nominal test or the DGP does not represent the planned design.
- Report `UNVERIFIED` when required software, moments, source files, or checks
  are unavailable.
- Do not choose an effect size because it makes the planned N look adequate.
  Show sensitivity over substantively justified effects.

Follow
[`confidential-data.md`](../../references/rules/confidential-data.md) when
moments come from restricted data. Prefer publishable pilot or external
moments; do not expose protected summary statistics in a public-facing
preregistration.
