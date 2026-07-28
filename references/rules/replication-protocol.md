<!-- Native reimplementation of .claude/rules/replication-protocol.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 6460fcce181fcefc6aa6802c552e45f3ef47c9083ec493f78fdec1bd82041388. The upstream file credits the Material Passport concept in Academic Research Skills; no ARS text or schema is copied here. -->

# Replication and numeric-claim protocol

## Applicability

Load for analysis code, generated tables/figures, manuscripts with numeric claims, and replication-package preparation.

## Reproduce before extending

Run the documented entry point in a clean environment before adding new specifications. Record the command, software versions, seed, input hashes or stable identifiers, and output locations. If the baseline does not reproduce, stop extensions and isolate the first divergent step.

## Numeric-claim passport

Maintain one YAML passport per paper and branch at `quality_reports/passports/<paper-slug>.yaml`. Each load-bearing claim records a stable id, manuscript location, displayed value, estimand, source script and invocation, source output, tolerance, last verification date, and status. Show inferred mappings to the author before writing them.

Statuses are:

- `PASS`: manuscript and source agree within the recorded tolerance;
- `FAIL`: they disagree and no concrete explanation is established;
- `EXPLAINED`: a named alternative specification, sample, edition, or rounding rule explains the difference;
- `STALE`: a source or output changed after verification;
- `UNVERIFIED`: the claim has no completed evidence check.

An empty note never converts FAIL to EXPLAINED. A source output is a challenger, not an oracle: either the manuscript or the code may be wrong.

## Audit workflow

1. Extract numeric claims with precise manuscript locations.
2. Locate the generating code and machine-readable output.
3. Re-run only when authorized and safe; otherwise inspect existing outputs and mark execution UNVERIFIED.
4. Compare using a domain-appropriate absolute or relative tolerance that is recorded before judging the result.
5. Investigate sample, weights, transformations, missingness, clustering, degrees of freedom, comparison groups, seeds, and package-version drift for every mismatch.
6. Update the passport and emit a claim-by-claim report with evidence pointers.

## Gates

Submission-ready work has no load-bearing FAIL, STALE, or UNVERIFIED claim. `$commit` may stop when touched manuscript or analysis files have affected FAIL/STALE passport entries, but committing still requires explicit user intent and any override must name the reason. `$review-paper` reports passport counts, and `$verify-claims` remains separate for citation and prose claims.
