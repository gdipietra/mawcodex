---
name: r-package-check
description: "Run an R package release gate: regenerate documentation, run tests, run R CMD check with CRAN checks, triage every error, warning, and note, optionally measure coverage, and perform a source review. Use before an R-package release or CRAN submission; never submits or bumps versions."
---

# R Package Release Gate

Decide whether an R package is releasable using reproducible evidence.

## Contract

- The input is a package root containing `DESCRIPTION`; if omitted, search the
  current project and stop on ambiguity.
- Follow
  [`r-package-conventions.md`](../../references/rules/r-package-conventions.md).
- Treat `man/` and `NAMESPACE` as generated. Regenerate them; never hand-edit.
- Report unavailable tools or skipped checks as `UNVERIFIED`.
- Do not bump a version, publish, upload, or submit to CRAN. Those actions
  require a separate explicit request.
- Prefer the project `r-package-reviewer`; otherwise use an isolated subagent
  with
  [`r-package-reviewer.md`](../../references/agent-roles/r-package-reviewer.md).

## Phase 0: Pre-flight

Read package name/version, exported functions, and dependency fields. Probe for
R, `devtools`, `roxygen2`, `testthat`, and optional `covr`. Report:

```markdown
## Pre-Flight Report — R Package Check
**Package:** [name version]
**Root:** [absolute path]
**Exports:** [count]
**Dependencies:** Imports [...] · Suggests [...] · Depends [...]
**Toolchain:** R [PASS/FAIL] · devtools [...] · roxygen2 [...] · testthat [...] · covr [...]
**Plan:** document → test → check --as-cran → coverage → source review
```

If R or a required package is missing, stop and mark downstream phases
`UNVERIFIED`; do not install dependencies without authorization.

## Phase 1: Documentation drift

Run `devtools::document(<package-root>)`, then inspect only `man/` and
`NAMESPACE` for changes. Report any drift as stale generated documentation.
Preserve the diff for review; do not commit it.

## Phase 2: Tests

Run `devtools::test(<package-root>)`. Capture command, R version, exit status,
test counts, failures, and warnings. A command that did not finish is
`UNVERIFIED`, not a passing test suite.

## Phase 3: CRAN-style check

Run `devtools::check(<package-root>, args = "--as-cran")` or an equivalent
`R CMD build` followed by `R CMD check --as-cran`. For a long run, launch it as
a managed background process, retain the process identifier and log path, and
wait on the process using the runtime's supported wait mechanism. Do not poll
with repeated sleeps.

Triage every result:

| Result | Tier | Policy meaning | Action |
| --- | --- | --- | --- |
| ... | ERROR / WARNING / NOTE | ... | fix / justify |

Errors and warnings block release. Fix a note when practical; otherwise draft
the exact evidence-based explanation for `cran-comments.md`.

## Phase 4: Coverage

If `covr` is available, run package coverage and flag exported functions with
zero coverage. If unavailable, mark coverage `UNVERIFIED`; absence alone does
not erase the completed test/check evidence.

## Phase 5: Independent source review

Give the package root to the package-review role in a separate context. Reconcile
its Critical and High findings with the command evidence. Do not describe an
issue as fixed unless the relevant check was rerun.

## Phase 6: Report and gate

Write `quality_reports/<package>_package_check.md`:

```markdown
## Release Gate — [package version]
- R CMD check --as-cran: E errors, W warnings, N notes
- Tests: P passed, F failed
- Coverage: X% or UNVERIFIED
- Source review: C critical, H high
- Verdict: RELEASABLE / FIX-FIRST / POLICY-VIOLATION / UNVERIFIED

### Submission checklist
[ ] 0 errors and 0 warnings; every note explained
[ ] Version and NEWS.md reviewed by maintainer
[ ] Cross-platform checks run separately
[ ] Reverse-dependency check considered for updates
```

`RELEASABLE` requires 0 errors, 0 warnings, every note explained, passing tests,
and no unresolved Critical/High source finding. Cross-platform services remain
`UNVERIFIED` unless actually run. Report the working-tree changes created by
documentation generation.

## Provenance

Native Codex rewrite of the upstream `r-package-check` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
