---
name: data-analysis
description: "Build a reproducible R analysis from an observed dataset: orient to data sensitivity and schema, distinguish descriptive from causal goals, create numbered scripts, inspect transformations, estimate the requested models, and produce verified tables and figures under `scripts/R/_outputs/`. Use for dataset exploration, regression, or a full empirical workflow."
---

## Codex execution contract

- Treat the user's request and applicable `AGENTS.md` files as authoritative.
- Resolve referenced resources relative to this skill first.
- Use bounded, isolated subagents for independent review roles; when a
  project custom agent is unavailable, use the matching portable role in
  `../../references/agent-roles/`.
- Treat missing tools, inaccessible sources, and skipped checks as
  UNVERIFIED rather than PASS.
- Require explicit user authorization for commit, push, merge, deploy,
  submission, sending, or other external publication.

# Data Analysis Workflow

Run an end-to-end data analysis in R: load, explore, analyze, and produce publication-ready output.

**Input:** a dataset path or an analysis goal supplied by the user. Resolve the
actual file and variables before writing code.

---

## Constraints

- Follow
  [`r-code-conventions.md`](../../references/rules/r-code-conventions.md)
- **Save all scripts** to `scripts/R/` with descriptive names
- **Keep raw inputs immutable**; write derived data and outputs to
  `scripts/R/_outputs/` or a project-documented derived-data directory
- Use `saveRDS()` for key fitted models, estimands, and reusable derived
  objects, with generating script and source-data provenance
- **Use project theme** for all figures (check for custom theme in `references/rules/`)
- Never turn an association into a causal claim without a stated estimand,
  identification assumptions, comparison group, treatment timing, inference
  method, and diagnostics
- Run the `r-reviewer` role before presenting results

---

## Workflow Phases

### Phase 0: Pre-Flight Report

**Before writing any analysis code, produce a Pre-Flight Report** showing you read the inputs. This prevents the common failure mode where the agent hallucinates variable names or skips project conventions.

Output block (in your response to the user, before Phase 1):

```markdown
## Pre-Flight Report

**Dataset:** [path]
- Variables found: [list from head()/names()]
- Rows: [count]
- Key types: [e.g., "outcome=numeric, treatment=binary, state=factor"]
- Missing-data summary: [% missing per key var]
- Sensitivity: [public | confidential | restricted | UNVERIFIED]

**Project conventions read:**
- `references/rules/r-code-conventions.md` — [relevant rule]
- `references/rules/content-invariants.md` — [applicable invariants]

**Task interpretation:** [one sentence restating what the user asked for]

**Plan:** [3-5 bullet outline of the R script structure]
```

If any input cannot be read (missing file, unreadable format), stop and ask the user before proceeding.

Classify the task as descriptive, predictive, or causal. For a causal task,
write the estimand and identifying assumptions into the pre-flight report. If
those cannot be resolved from project context, ask before estimation.

### Phase 1: Setup and Data Loading

1. Create R script with proper header (title, author, purpose, inputs, outputs)
2. Load required packages at top (`library()`, never `require()`)
3. Set seed once at top in YYYYMMDD format (per `r-code-conventions.md`), e.g. `set.seed(20260415)` (INV-9)
4. Load and inspect the dataset

### Phase 2: Exploratory Data Analysis

Generate diagnostic outputs:
- **Summary statistics:** `summary()`, missingness rates, variable types
- **Distributions:** Histograms for key continuous variables
- **Relationships:** Scatter plots, correlation matrices
- **Time patterns:** If panel data, plot trends over time
- **Group comparisons:** If treatment/control, compare pre-treatment means

Save all diagnostic figures to `scripts/R/_outputs/diagnostics/`.

### Phase 3: Main Analysis

Based on the research question and pre-specified design:
- **Regression analysis:** Use `fixest` for panel data, `lm`/`glm` for cross-section
- **Standard errors:** Cluster at the appropriate level (document why)
- **Multiple specifications:** Start simple, progressively add controls
- **Effect sizes:** Report raw effects with units; add standardized effects only
  when substantively meaningful and define the standardization sample

Record sample restrictions, missing-value handling, joins and cardinality
checks, fixed effects, weights, clustering, seeds, and software versions.
Inspect row counts before and after every join or exclusion.

### Phase 4: Publication-Ready Output

**Tables:**
- Use the project's installed table package; prefer a currently maintained
  package whose version is recorded
- Include all standard elements: coefficients, SEs, significance stars, N, R-squared
- Export as `.tex` for LaTeX inclusion and `.html` for quick viewing

**Figures:**
- Use `ggplot2` with project theme
- Set `bg = "transparent"` for Beamer compatibility
- Include proper axis labels (sentence case, units)
- Export with explicit dimensions: `ggsave(width = X, height = Y)`
- Save as both `.pdf` and `.png`

### Phase 5: Save and Review

1. Save key objects and machine-readable coefficient/diagnostic tables with
   explicit provenance.
2. Create `scripts/R/_outputs/` subdirectories as needed.
3. Run the project `r-reviewer` custom agent, or a bounded isolated subagent
   following
   [`r-reviewer.md`](../../references/agent-roles/r-reviewer.md), on the exact
   generated script.
4. Address Critical and High findings, then rerun affected code.
5. Run `$audit-reproducibility` when results feed manuscript claims. Missing R,
   packages, data access, or reviewer capability makes the affected step
   UNVERIFIED.

---

## Script Structure

Follow this template:

```r
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs: [Data files]
# Outputs: [Figures, tables, RDS files]
# ============================================================

# 0. Setup ----
library(tidyverse)
library(fixest)
library(modelsummary)

set.seed(20260415)  # YYYYMMDD per r-code-conventions.md (INV-9)

dir.create("scripts/R/_outputs/analysis", recursive = TRUE, showWarnings = FALSE)

# 1. Data Loading ----
# [Load and clean data]

# 2. Exploratory Analysis ----
# [Summary stats, diagnostic plots]

# 3. Main Analysis ----
# [Regressions, estimation]

# 4. Tables and Figures ----
# [Publication-ready output]

# 5. Export ----
# [saveRDS for all objects, ggsave for all figures]
```

---

## Important

- **Reproduce, don't guess.** If the user specifies a regression, run exactly that.
- **Show your work.** Print summary statistics before jumping to regression.
- **Check for issues.** Look for multicollinearity, outliers, perfect prediction.
- **Use relative paths.** All paths relative to repository root.
- **No hardcoded values.** Use variables for sample restrictions, date ranges, etc.

## Long-running fits

Use the available background-execution capability for long regressions,
simulations, or bootstrap loops. Retain the process identifier and wait or poll
in bounded intervals, relaying milestones and errors. Do not busy-loop or claim
completion without a terminal result. If monitoring is unavailable, mark the
run UNVERIFIED.
