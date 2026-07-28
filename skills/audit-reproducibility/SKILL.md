---
name: audit-reproducibility
description: "Cross-check numeric manuscript claims against actual R, Stata, or Python outputs under the project's replication tolerances. Classify each claim as PASS, FAIL, EXPLAINED, or UNMATCHED and never treat incomplete evidence as a pass. Use before submission or replication-package release."
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

# Audit Reproducibility

Compare numeric claims in a manuscript (point estimates, standard errors,
p-values, and counts) against actual outputs produced by the analysis
pipeline. Apply the tolerances defined in
[`replication-protocol.md`](../../references/rules/replication-protocol.md).

**Core principle:** If the paper says `ATT = -1.632 (0.584)` and the code produces `-1.628 (0.591)`, we verify — **numerically** — that the difference is within the documented tolerance. No more "looks close enough" eyeballing.

## When to use

- **Before submission.** Catches the "I updated the analysis but forgot to update Table 2" bug.
- **Before releasing a replication package.** Verifies the code actually reproduces the paper.
- **After a major revision.** Ensures the paper still matches the latest code.
- **Quality gate in `$commit`.** Pair with a pre-commit audit when manuscript
  and analysis files changed.

## Inputs

- **Manuscript** — required path to a `.tex`, `.qmd`, `.md`, or `.pdf` file.
- **Outputs directory** — defaults to `scripts/R/_outputs/`; recognized
  alternatives include `scripts/stata/_outputs/`,
  `scripts/python/_outputs/`, `_targets/objects/`, or a user-specified
  directory. `$stata-replication` may produce the Stata outputs.

## Workflow

### Phase 0: Pre-flight

1. Read
   [`replication-protocol.md`](../../references/rules/replication-protocol.md)
   for the tolerance thresholds currently in effect.
2. Verify the outputs directory exists and is non-empty. If empty or stale (older than the manuscript), prompt the user to re-run their pipeline (e.g., `Rscript scripts/R/00_run_all.R`) before auditing.
3. Ensure a `sessionInfo.txt` or equivalent environment capture exists in the outputs dir.

### Phase 1: Extract claims from the manuscript

Parse the manuscript for numeric claims. Patterns to match:

- **Point-estimate + SE**: `ATT = -1.632 (0.584)`, `$\beta = 0.342$ (0.091)`, `hat{\tau} = 1.28**` with starred significance
- **Table cells**: `& -1.632$^{***}$ & 0.584 &` in LaTeX table environments
- **Counts**: `our sample of 2,847 firms`, `$N = 2{,}847$`
- **Summary stats**: `mean = 0.423`, `SD = 0.087`
- **P-values**: `p < 0.01`, `$p = 0.003$`

Record each claim as a tuple:

```
{
  claim_id: "Table2_col3_ATT",
  location: "Table 2, Column 3, row 'Treatment'",
  kind: "point_estimate" | "standard_error" | "p_value" | "count" | "percentage",
  reported_value: -1.632,
  uncertainty: 0.584,              # only for point estimates
  significance_stars: 3,            # 0-3 or None
  raw_context: "the ATT estimate of -1.632 (0.584) indicates..."
}
```

Write the extracted claims to `quality_reports/reproducibility_claims_[manuscript-name].json` so the user can review the extraction before audit.

### Phase 2: Extract results from outputs

Scan the resolved outputs directory for corresponding values. Priority order:

1. **`.rds` files** — inspect named components with an R process in a fresh
   temporary directory; never modify the source object.
2. **`.tex` tables** — parse LaTeX table cells directly; match on column headers + row labels.
3. **`.csv` summary files** — pandas/readr parse, key-value lookup.
4. **`.out` / `.log` files** (Stata, regress output) — regex extraction.
5. **`.json`** — direct key lookup.

Record each extracted result:

```
{
  source: "scripts/R/_outputs/results.rds",
  lookup_key: "fit_main$coefficients['treated']",
  value: -1.628,
  uncertainty: 0.591,
  p_value: 0.005
}
```

### Phase 3: Match claims to results

Prefer explicit provenance keys, generated-table inputs, row labels, and
column labels. Use fuzzy heuristics only to propose candidates when exact
labels do not match:

- Name similarity (`"treatment effect"` ~ `"ATT"` ~ `"treated"`)
- Magnitude similarity (if two candidates have values within 10% of the reported, prefer the one with closer SE)
- Context hints from the claim's `raw_context` field (table number, row label, description)

For every claim, record the evidence that identifies its computed counterpart.
Magnitude similarity alone can never establish a match. A proposed fuzzy match
must be confirmed by a provenance key or by the user; otherwise classify it as
`UNMATCHED — manual review needed`.

### Phase 4: Tolerance check

For each matched claim, apply the thresholds from `replication-protocol.md`:

| Kind | Tolerance | Example |
|---|---|---|
| Integers (N, counts) | Exact | 2,847 must equal 2,847 |
| Point estimates | `abs(reported - computed)` < 0.01 | -1.632 vs -1.628 → diff = 0.004 → PASS |
| Standard errors | `abs(reported - computed)` < 0.05 | 0.584 vs 0.591 → diff = 0.007 → PASS |
| P-values | Same significance level | p<0.01 and p<0.01 → PASS; p<0.01 and p=0.03 → FAIL |
| Percentages | ±0.1pp | 42.3% vs 42.35% → PASS |

Respect any **tolerance overrides** the user has written into their `replication-protocol.md` fork (they may loosen for MC noise or tighten for administrative data).

### Phase 4b: Disposition — PASS / FAIL / EXPLAINED / UNMATCHED

A tolerance check resolves to one of four dispositions:

- **PASS** — within tolerance.
- **FAIL** — outside tolerance, with no defensible alternative recorded. **Blocks** (exit 1).
- **EXPLAINED** — outside tolerance, **but** the author has recorded a
  *concrete, named alternative specification* that accounts for the gap (see
  the downgrade rule). Surface it separately; it is not an ordinary PASS.
- **UNMATCHED** — no computed counterpart found (Phase 3 confidence < 0.7). Never auto-downgradable.

**A mismatch is not automatically a failure.** In applied work the most common out-of-tolerance result is a *defensible alternative spec*, not a bug — `reghdfe` vs `feols` clustering df, never-treated vs not-yet-treated comparison group, conditional vs unconditional parallel trends, a different MC seed/reps, or display rounding. The skill's job is to *stage the disagreement* for a human auditor, not to pronounce the code right and the paper wrong. (The df-adjustment note in "Stata-specific notes" below is the canonical example of a named alternative.)

**The manuscript is not the oracle.** When the computed value disagrees with the manuscript, do not presume the code is correct and the paper stale — nor the reverse. A refactor may have broken a previously-correct table (the *on-disk output* is the buggy one), or the paper may carry an old number. The computed value is a **challenger**, not ground truth. Report a mismatch as "one of {paper, code} must change — isolate which," never "revert the code to match the paper." This prevents the trap of reverting a genuine bug-fix just to make the paper 'reproduce.'

#### Downgrade rule: FAIL → EXPLAINED

A FAIL may be downgraded to EXPLAINED **only** when a *specific named alternative* is recorded for that exact claim — in the passport entry's `notes:` field (passport mode) or the audit report's author-note column (default mode). Example of a valid note:

> "never-treated vs not-yet-treated comparison group; under not-yet-treated the published value is −1.19, within rounding of the script's −1.187. CODE-CORRECTED pending."

The author is the **auditor**: the skill stages the two-sided comparison (reported value *and* computed value, both shown); the human writes the one-line named alternative; the skill records it and thereafter respects it. Tag the resolution `PAPER-CORRECTED`, `CODE-CORRECTED`, or `DEFENSIBLE-ALTERNATIVE`.

**Hard floor — never downgradable to EXPLAINED:**
- A blank note, "unclear", "looks fine", or any note that does not *name a concrete alternative spec*.
- An **UNMATCHED** claim (no computed counterpart to compare against).
- A flat numerical contradiction with no alternative offered.

(Citation and existence claims are out of scope here; `$verify-claims` owns
those.)

#### Repeated EXPLAINED is a signal (two-strikes)

Reuse the two-strikes rule from `$review-paper --adversarial` and
[`summary-parity.md`](../../references/rules/summary-parity.md): if the same
claim is EXPLAINED in two consecutive audits without becoming PASS, surface it
prominently. In passport mode, compare the current `status` and `notes`
against the prior audit.

### Phase 5: Report

Write `quality_reports/reproducibility_audit_[manuscript-name].md`:

```markdown
# Reproducibility Audit: [Manuscript Title]

**Date:** [YYYY-MM-DD]
**Manuscript:** [path]
**Outputs directory:** [path]
**Tolerance source:** references/rules/replication-protocol.md

## Summary

| Status | Count |
|---|---|
| PASS | N |
| FAIL (diff > tolerance, no named alternative) | M |
| EXPLAINED (out of tolerance, named alternative recorded) | E |
| UNMATCHED (manual review) | K |
| **Overall verdict** | **PASS / QUALIFIED / FAIL / UNVERIFIED** |

## PASS (all within tolerance)
| Claim | Reported | Computed | Diff | Tolerance |
|---|---|---|---|---|
| Table2_col3_ATT | -1.632 (0.584) | -1.628 (0.591) | 0.004 / 0.007 | 0.01 / 0.05 |

## FAIL (outside tolerance — BLOCKER)
| Claim | Reported | Computed | Diff | Tolerance | Location in paper | Author note (name a concrete alternative to downgrade → EXPLAINED) |
|---|---|---|---|---|---|---|

## EXPLAINED (out of tolerance; defensible named alternative recorded — non-blocking, carry into response-to-referees)
| Claim | Reported | Computed | Named alternative (why the gap is defensible) | Resolution |
|---|---|---|---|---|
| Table3_col2_ATT | -1.187 | -1.19 | never-treated vs not-yet-treated comparison group | DEFENSIBLE-ALTERNATIVE |

## UNMATCHED (manual review)
| Claim | Raw context | Candidate sources |
|---|---|---|

## Environment
[sessionInfo excerpt]

## Next steps
1. Resolve each FAIL row — either correct the manuscript, rerun the analysis, or (if the gap is a defensible alternative spec) record a concrete named alternative to downgrade it to EXPLAINED.
2. Review UNMATCHED rows — add explicit lookup keys or widen the search scope.
3. Review EXPLAINED rows before submission — each should map to a sentence in the response-to-referees.
4. Claim replication-ready only when every in-scope claim is PASS. EXPLAINED
   rows produce a QUALIFIED result; UNMATCHED rows produce UNVERIFIED.
```

## Exit behavior

- **All in-scope claims PASS:** report PASS.
- **Any FAIL:** report FAIL and block the gate.
- **No FAIL but one or more EXPLAINED:** report QUALIFIED; do not claim the
  manuscript is fully reproducible.
- **Any UNMATCHED, missing output, stale output, missing environment capture,
  unavailable parser, or skipped check:** report UNVERIFIED and block any
  release-readiness claim.

## Source-language coverage

The skill compares manuscript claims against outputs in three source-language ecosystems:

| Source | Default outputs dir | Read-output via | Common claim sources |
|---|---|---|---|
| **R** (default) | `scripts/R/_outputs/` | `readRDS()`, `arrow::read_parquet()`, `vroom::vroom()` | `.rds` / `.parquet` / `.csv` / `tinytable` `.tex` |
| **Stata** (v1.9.0) | `scripts/stata/_outputs/` | `haven::read_dta()` from R, or `pyreadstat.read_dta()` from Python | `.dta` / `esttab` `.tex` / `.smcl` log values |
| **Python** | `scripts/python/_outputs/` (or `_targets/`) | `pandas.read_parquet`, `pickle.load` | `.parquet` / `.pickle` / `.csv` |

**Stata-specific notes (v1.9.0):**

- `.dta` outputs are read via `haven::read_dta()` (R), `pyreadstat.read_dta()` (Python), or by parsing the corresponding `esttab` `.tex` if the table-cell value is what the manuscript cites.
- Manuscript cell `\input{scripts/stata/_outputs/tab_main.tex}` is the strongest provenance signal — the cell value comes mechanically from the .do file. Match the location in the `.tex` to the regression call in `03_analyze.do`.
- Clustering df adjustments can differ between `reghdfe` and base `reg, cluster()`. If a SE mismatches at the 2nd decimal, the tolerance in `replication-protocol.md` covers it; if it mismatches at the 1st decimal, investigate the df adjustment.

## Passport-mode (v1.9.0)

When `quality_reports/passports/<paper-slug>.yaml` exists, the skill operates in **passport mode**: instead of emitting a one-shot report, it **reads, updates, and rewrites** the passport file in place.

- For each `claims:` entry in the passport, perform the same numeric audit as the default mode (extract reported value from manuscript at `location`, locate computed value at `source_file:source_line` / `output_file:output_field`, compare against `tolerance:`).
- After each claim is audited, update `status` in place:
  - PASS → claim within tolerance.
  - FAIL → claim outside tolerance **and** the entry's `notes` does not name a concrete alternative. Record the discrepancy (reported vs computed) in `notes`. Blocks (exit 1).
  - EXPLAINED → claim outside tolerance **but** the entry's `notes` already records a *specific named alternative spec* (not blank, not "unclear"). The skill reads `notes` on its next run and resolves the same out-of-tolerance claim to EXPLAINED instead of FAIL — surfaced, non-blocking. The hard floor still applies: an UNMATCHED claim or a note without a named alternative stays FAIL.
  - STALE → if `source_file` or `output_file` modification time is later than `last_verified_on`, mark STALE and re-run the audit logic (after the rerun, status becomes PASS / FAIL / EXPLAINED — STALE is transient).
- Update `last_verified_on` and `last_verified_by: "$audit-reproducibility"` per claim.
- Update `paper.last_audit` at the top level.

If a claim in the manuscript is detected that has no matching passport entry, emit an UNVERIFIED warning — the author should add it (passport scope is author-curated, not auto-populated, to avoid bad inferences).

Passport mode does NOT delete passport entries. If a claim disappears from the manuscript, the passport entry remains with a STALE status — the author decides whether to delete (claim retracted) or update the entry's `location` (claim moved).

See
[`replication-protocol.md`](../../references/rules/replication-protocol.md)
"Claims Provenance: `passport.yaml`" for the full schema and integration
points (`$commit`, `$review-paper`).

## Cross-references

- [`replication-protocol.md`](../../references/rules/replication-protocol.md)
  — the tolerance contract and passport schema.
- [`passport-template.yaml`](../../assets/templates/passport-template.yaml) —
  starter file for a new paper.
- [`$review-r`](../review-r/SKILL.md) — code-quality review.
- [`$diagnose`](../diagnose/SKILL.md) — localize one failing claim.
- [`$review-paper`](../review-paper/SKILL.md) — substantive review.
- [`$replication-package`](../replication-package/SKILL.md) — build the deposit
  only after this gate.
- [`$capture-environment`](../capture-environment/SKILL.md) and
  [`$disclosure-check`](../disclosure-check/SKILL.md) — environment and
  restricted-data gates.

## What this skill does NOT do

- **Re-run your analysis.** The skill compares CURRENT outputs against manuscript claims. If the outputs are stale, re-run your pipeline first (the pre-flight phase will warn).
- **Catch wrong specifications.** A regression that compiles cleanly and produces a reproducible `-1.632` is reproducible. Whether `-1.632` is the RIGHT estimand is a `review-paper` / domain-reviewer question.
- **Check external package versions.** The `sessionInfo.txt` capture lets a reviewer see the env; pinning versions is on the user (via `renv.lock` or a `DESCRIPTION` file).

## Long batch reruns

When `$audit-reproducibility` is asked to verify all numeric claims, rerun the
full pipeline only if the user authorized execution and the project rules allow
it. For a long process, launch it through the available background-execution
capability, retain its process identifier, and poll or wait in bounded
intervals while relaying failures. If the runtime cannot be observed or the
rerun is skipped, mark regenerated-output comparisons UNVERIFIED.
