---
name: stata-replication
description: "Build and optionally execute a numbered Stata replication pipeline with immutable raw data, logged transformations, publication-ready generated outputs, a one-command entry point, and optional R cross-checks. Use for Stata-first analyses, AEA-style replication packages, or Stata robustness checks."
---

# Stata Replication Pipeline

Create a reproducible `scripts/stata/` pipeline and verify its outputs using an
available Stata execution capability.

## Contract

- Follow
  [`stata-code-conventions.md`](../../references/rules/stata-code-conventions.md)
  and
  [`replication-protocol.md`](../../references/rules/replication-protocol.md).
- Never hand-edit raw or derived `.dta` files. All transformations belong in
  `.do` files.
- Detect and record the installed Stata version; do not invent or silently
  change a project version declaration.
- Prefer a connected, command-guarded Stata integration. A direct local Stata
  executable is acceptable when explicitly in project scope and logs are
  captured.
- Missing Stata/integration or `--no-execute` makes execution and outputs
  `UNVERIFIED`; scaffolding can still complete.
- Never install third-party software, commit, publish, or submit without an
  explicit user request.

## Phase 0: Pre-flight

Resolve the paper/data pointer and whether the user requested translation from R
or no execution. Report:

- Stata capability and version;
- project root and data sensitivity;
- raw, derived, and output locations;
- existing R pipeline if translation was requested; and
- planned estimand, specifications, inference, and expected outputs.

If translating from R, inventory every transformation, sample restriction,
estimator option, seed, and output contract before writing Stata. An unresolved
estimand or unavailable source pipeline blocks translation.

## Phase 1: Scaffold

Create or update:

```text
scripts/stata/
  00_install.do
  01_clean.do
  02_descriptive.do
  03_analyze.do
  04_robustness.do
  05_tables_figures.do
  99_run_all.do
  _outputs/
```

Each script must:

- declare compatible Stata version, purpose, inputs, outputs, and dependencies;
- use project-relative paths;
- write a durable log under `_outputs/`;
- preserve raw data;
- make sample exclusions and merges auditable;
- set and record seeds where randomness occurs; and
- use generated `.tex` tables and exported figures rather than hand-copied
  numbers.

Tailor the estimator to the research design. State the estimand, treatment
timing, comparison group, inference method, and relevant diagnostics. Never
default mechanically to robust or clustered errors without identifying the
correct inference level.

`99_run_all.do` must run the complete pipeline from documented inputs in order
and stop on errors.

## Phase 2: Execute

Unless no execution was requested, run the numbered pipeline through the
available Stata capability. Capture command, version, log path, exit status,
warnings, and output manifest. Halt on the first substantive failure; do not
auto-fix sample-size, collinearity, missing-variable, or identification
problems.

Use a managed background process and the runtime's supported wait mechanism for
long jobs. Do not poll with repeated sleeps.

## Phase 3: Verify

Check:

1. every declared output exists and is newer than its inputs;
2. every stage has a readable log and successful exit status;
3. software/add-on versions are captured;
4. tables/figures link to generated values; and
5. manuscript claims, if supplied, reconcile through
   `$audit-reproducibility`.

Do not call output verification PASS if Stata was not run.

## Phase 4: Optional R parity

When translating from R, execute both pipelines if capabilities permit and
compare estimates, standard errors, and exact analysis sample sizes using the
project tolerance contract. Explain known implementation differences rather
than forcing numerical equality. Any unmatched sample size is a blocking FAIL;
unexecuted counterpart results are `UNVERIFIED`.

Report scripts created/changed, commands run, output paths, warning/failure
evidence, and parity status. Use `$data-analysis` for R-first work.

## Provenance

Native Codex rewrite of the upstream `stata-replication` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT). The optional guarded Stata
integration remains attributable upstream to `SepineTam/stata-mcp`; availability
and installation are environment-specific.
