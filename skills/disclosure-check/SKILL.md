---
name: disclosure-check
description: "Pre-screen analysis outputs (tables, figures, logs) built on restricted or confidential data for statistical-disclosure-limitation problems before any release. Scans for small cell counts, complementary-suppression gaps, dominance (p-percent / (n,k)), re-identifiable exact counts, PII leakage, and unrounded sensitive statistics; classifies each finding CRITICAL / WARNING / OK and gates on any CRITICAL. Use before depositing or sharing restricted-data results, or when the user says \"disclosure check\", \"SDL scan\", \"is this output safe to release\", \"check for small cells\", \"disclosure avoidance\", \"pre-screen for the RDC\", or \"can I export this from the enclave\"."
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

# $disclosure-check — Statistical Disclosure Pre-Screen

Scan analysis outputs built on **restricted or confidential data** (Census FSRDC, IRS SOI, administrative registers, linked health records, proprietary firm panels) for the disclosure-avoidance problems that get an export request rejected — *before* it reaches the data provider's official disclosure review. The skill is a **pre-screen, not a substitute** for that review.

**Core principle:** Apply the signed provider or IRB rules inside the authorized
environment. A local heuristic scan can identify risks; it cannot authorize an
export or substitute for official review.

## When to use

- **Before requesting an export** from a Census FSRDC / secure data enclave / RDC.
- **Before depositing** restricted-data results to openICPSR, a journal, or a co-author outside the enclave.
- **Before sharing any figure, table, or log** derived from confidential microdata.
- **As a release gate.** Pair with a pre-commit / pre-deposit invocation so no restricted-data output ships un-screened. This is the foundation of the data-management plan for any restricted-data project.

## Inputs

- **Outputs directory** — defaults to `scripts/R/_outputs/`; recognized
  alternatives include `scripts/stata/_outputs/`,
  `scripts/python/_outputs/`, or an explicitly staged export-review directory.
- `--provider` — selects which disclosure-rule profile to load (Phase 0). One of `census` / `irs` / `irb` / `generic`. **Providers differ** — thresholds and rules are not interchangeable; default `generic` is deliberately conservative.
- `--threshold N` — use only when the user confirms that `N` comes from the
  controlling written agreement. A guessed threshold cannot yield PASS.

## Workflow

### Phase 0: Load the provider's disclosure rules

1. Read [`confidential-data.md`](../../references/rules/confidential-data.md)
   for the project's restricted-data handling contract and provider profiles.
2. Load the `--provider` profile populated from the controlling signed
   agreement or official project record. Confirm its version/date and scope:
   - **minimum cell count**,
   - **dominance rules**: `p`-percent (a cell is unsafe if the largest respondents contribute > `p`% of the total) and `(n,k)` (top `n` units > `k`% of total),
   - **rounding** required for sensitive statistics (counts, totals, ratios),
   - **top-coding / bottom-coding** thresholds for extreme values,
   - **geographic** minimum population for any geocoded statistic.
3. If signed-rule values are absent, run only a generic risk-discovery scan and
   label the result `UNVERIFIED — PROVIDER RULES MISSING`. A generic profile can
   never yield OK, PASS, or export authorization.
4. Confirm the scan will execute entirely inside the authorized environment.
   Do not upload values, send them to remote services, or delegate sensitive
   rows to a subagent. If local processing cannot be guaranteed, stop.

### Phase 1: Scan the outputs directory

Glob the outputs dir for `.tex`, `.csv`, `.txt`, `.log`, `.smcl`, `.out`, `.md` tables and figure-data files. For each:

- **Cell counts** — parse table cells / frequency columns; flag any count `0 < n < threshold` that is not already suppressed.
- **Complementary-suppression gaps** — if one cell in a row/column is suppressed but the margin total and the other cells let a reader back it out by subtraction, the suppression is **incomplete**.
- **Dominance** — for any total/mean cell where unit-level contributions are available (or inferable), apply the `p`-percent and `(n,k)` rules.
- **Exact re-identifying counts** — small exact integers (e.g., "4 hospitals", "1 firm", a max/min that is a single observation) that single out a unit.
- **PII leakage** — regex for names, SSNs (`\d{3}-\d{2}-\d{4}`), exact dates of birth, addresses, exact lat/long or fine geocodes, record IDs that survived into an output.
- **Unrounded sensitive statistics** — exact unrounded counts/totals where the provider requires rounding.

### Phase 2: Classify each finding — CRITICAL / WARNING / OK

| Disposition | Meaning | Examples |
|---|---|---|
| **CRITICAL** | Violates a loaded controlling rule or exposes direct identifiers; blocks release. | Cell below the verified threshold; complementary-suppression hole; verified dominance-rule failure; direct identifier. |
| **WARNING** | Plausibly safe but needs a human judgment call. | Cell at exactly the threshold; unrounded total just over a rounding base; geographic statistic near the min-population floor. |
| **OK** | Within every applicable loaded rule; official review may still be required. | Counts clear the verified threshold and rounding rule; dominance passes; no detected direct identifier. |

When two findings interact (a suppressed cell + a recoverable margin), report them **together** — the gate cares about the joint disclosure risk, not each cell in isolation. Be economics-aware: DiD / event-study cell counts per (cohort × period), IV first-stage subsamples, RCT arm × stratum balance tables, and panel firm-counts are the usual offenders.

### Phase 3: Suggest remediation

For each CRITICAL / WARNING, propose the standard SDL fix, in order of preference:

- **Suppress** the offending cell (and its complement, if a margin allows back-out).
- **Round** counts/totals to the provider's base (e.g., nearest 10 or 15).
- **Top-code / bottom-code** extreme values.
- **Aggregate** — collapse thin categories, coarsen geography, widen bins until every cell clears the threshold.
- **Drop** the statistic if no remediation preserves both safety and meaning.

Each suggestion names a non-sensitive file identifier, cell/location, rule,
and proposed remediation. Never apply it automatically. Avoid reproducing a
confidential value in the report when the location and rule are sufficient.

### Phase 4: Gate

Exit non-zero on any **CRITICAL**. WARNINGs surface but do not block. See Exit behavior.

## Output / Report format

Write `quality_reports/disclosure_check_[outputs-dir-slug].md`:

```markdown
# Disclosure Check: [outputs dir]

**Date:** [YYYY-MM-DD]
**Provider profile:** census | irs | irb | generic   (rules source: confidential-data.md)
**Min cell count:** [N]   **Dominance:** p=[p]%, (n,k)=([n],[k]%)   **Rounding base:** [b]

## Summary
| Disposition | Count |
|---|---|
| CRITICAL | M |
| WARNING | W |
| OK | P |
| **Verdict** | **PASS / FAIL / UNVERIFIED** |

## CRITICAL (blocks release)
| File | Location | Rule violated | Observed | Suggested remediation |
|---|---|---|---|---|
| tab3_by_cohort.tex | row "2008", col "n" | min cell (n<10) | n=4 | suppress cell + suppress complement in margin |

## WARNING (human judgment)
| File | Location | Concern | Suggested action |
|---|---|---|---|

## OK
[counts only, or a short list]

## Next steps
1. Resolve every CRITICAL — suppress / round / top-code / aggregate, then re-run.
2. Review WARNINGs with the agreement's written rules in hand.
3. Re-run until zero CRITICAL, THEN submit to the provider's OFFICIAL disclosure review.
```

## Exit behavior

- **Zero CRITICAL with all controlling rules loaded and every required check
  executed:** report PASS for the local pre-screen only.
- **Any CRITICAL:** report FAIL and block release.
- **Missing controlling rule, unavailable parser, skipped file, inaccessible
  output, or generic-only profile:** report UNVERIFIED and block release.
- WARNINGs require human review and may remain blocking when the controlling
  agreement says so. Official provider review remains authoritative.

## Flags

- `--provider` `<name>` — Load that data provider's disclosure rules (e.g. `census-fsrdc`, `irs`, `irb`). Default: the generic small-cell ruleset.
- `--threshold` `<n>` — supply the controlling minimum cell count and record
  its source; there is no release-authorizing default.

## Cross-references

- [`confidential-data.md`](../../references/rules/confidential-data.md) —
  restricted-data contract and provider profiles.
- [`replication-protocol.md`](../../references/rules/replication-protocol.md)
  — release and reproducibility contract.
- [`$audit-reproducibility`](../audit-reproducibility/SKILL.md) — retained
  numeric claims.
- [`$data-analysis`](../data-analysis/SKILL.md) and
  [`$stata-replication`](../stata-replication/SKILL.md) — producing pipelines.
- [AEA Data Editor checklist](https://aeadataeditor.github.io/) and the [DCAS standard](https://datacodestandard.org/) — disclosure + access expectations for restricted-data deposits (openICPSR restricted-access stub).

## What this skill does NOT do

- **It does not replace the data provider's official disclosure review.** Census/RDC, IRS, and IRB analysts run the authoritative review; this skill **pre-screens** so the official review is more likely to pass on the first pass. A PASS here is not clearance to release.
- **It does not certify your rules are correct.** It applies the thresholds *you load* from your signed agreement; if the loaded `--provider` profile is wrong, the scan is wrong. Reconcile with the written agreement, not a default.
- **It does not move, encrypt, or transmit data,** never exfiltrates microdata from the enclave — it reads only the staged outputs you point it at.
- **It does not catch every disclosure risk.** Differencing across released tables, longitudinal re-identification, and model-based inferential disclosure can evade a per-file scan. A clean run is necessary, not sufficient.
