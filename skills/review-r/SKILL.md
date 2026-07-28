---
name: review-r
description: "Perform a read-only review of R scripts for code quality, reproducibility, domain correctness, numerical safety, and project conventions. Produce reports without editing or executing the scripts. Use for R code review; use audit-reproducibility for numeric execution checks."
---

# Review R Scripts

Review R source without changing it or representing unexecuted code as tested.

## Codex execution contract

- Follow applicable `AGENTS.md` files and
  [`r-code-conventions.md`](../../references/rules/r-code-conventions.md).
- This workflow is read-only for `.R` source files. It may write only review
  reports under `quality_reports/`.
- A missing file, unavailable reviewer, or skipped inspection is `UNVERIFIED`.
- Prefer the project `r-reviewer` custom agent. Otherwise give a bounded,
  read-only subagent
  [`r-reviewer.md`](../../references/agent-roles/r-reviewer.md).

## Scope

Interpret the user's supplied scope as:

- a specific `.R` path: review only that file;
- `LectureN`: review matching lecture scripts;
- `all`: review `.R` files in `scripts/R/` and `Figures/*/`; or
- another explicit path set: use exactly that set.

Resolve and list the files before review. Do not silently expand the scope.

## Workflow

For each file, independently inspect:

1. correctness, failure handling, and numerical edge cases;
2. reproducibility: relative paths, seeds, deterministic outputs, and recorded
   package assumptions;
3. research-design correctness, including estimand/inference alignment;
4. data handling, joins, exclusions, missingness, and immutable raw inputs;
5. R idioms, readability, modularity, and project conventions; and
6. disclosure or confidentiality risks in produced outputs.

Write `quality_reports/<script-name>_r_review.md` with findings classified
`Critical`, `High`, `Medium`, or `Low`. Each finding must include evidence,
location, consequence, and a suggested remedy. State explicitly that this was a
static review and that execution remains `UNVERIFIED`.

After all reports complete, summarize issue counts per script, the
severity breakdown, and the three highest-priority findings across the batch.
Do not apply fixes without a separate user request.

Use `$audit-reproducibility` when the user wants the scripts run and numeric
outputs checked.

## Provenance

Native Codex rewrite of the upstream `review-r` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
