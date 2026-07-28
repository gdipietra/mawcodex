---
name: capture-environment
description: "Snapshot the computational environment for a replication package — detects the analysis stack (R / Stata / Python) and emits the right lockfiles (renv.lock + sessionInfo.txt, requirements.txt / environment.yml / uv.lock, Stata version + ado package list), records seeds and RNG kind, optionally writes a pinning Dockerfile, and produces a paste-ready \"Computational requirements\" block. Use when user says \"capture the environment\", \"snapshot my dependencies\", \"pin the versions\", \"make a renv.lock / requirements.txt\", \"make this byte-reproducible\", or before releasing a replication package to openICPSR / the AEA Data Editor."
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

# $capture-environment — Snapshot the Computational Environment

A replication package that runs only on the author's machine is not
reproducible. This skill captures language versions, package versions, seeds,
random-number-generator settings, and optionally the OS layer. It detects the
project's stacks, emits each ecosystem's expected artifacts, and attempts an
isolated restore when the required runtimes are available.

**Core principle:** Pin every dependency a result uses. A successful restore
supports environment reproducibility; it does not by itself establish numeric
or byte-for-byte reproducibility. Numeric claims remain governed by
[`replication-protocol.md`](../../references/rules/replication-protocol.md).

## When to use

- **Before releasing a replication package** to openICPSR, Zenodo, Dataverse, or a journal archive — the AEA Data Editor / DCAS standard expects a documented, version-pinned environment.
- **Before submission**, alongside
  [`$audit-reproducibility`](../audit-reproducibility/SKILL.md), which checks
  the numbers produced in the captured environment.
- **After adding or upgrading a package** mid-project — re-snapshot so the lockfile doesn't drift from what the code actually loads.
- **When handing a project to a co-author or RA** who needs to reconstruct your stack.

## Inputs

- **Project directory** — defaults to the repository root. Inspect
  `scripts/R/`, `scripts/stata/`, `scripts/python/`, and root-level environment
  files.
- `--docker` — also emit a `Dockerfile` pinning OS + language version + system libraries for byte-identical reproduction.
- `--no-verify` — skip Phase 3 (the best-effort clean-install check). Useful in CI or when the toolchain isn't installed locally.

## Workflow

### Phase 0: Detect the stack

Glob for stack signals and decide which capture paths to run (a project may be multi-language — DiD in R, an IV robustness check in Stata):

| Signal | Stack | Capture path |
|---|---|---|
| `scripts/R/*.R`, `DESCRIPTION`, `renv/`, `*.Rproj` | **R** | renv + sessionInfo |
| `scripts/python/*.py`, `*.ipynb`, `pyproject.toml`, `requirements.txt`, `environment.yml`, `uv.lock` | **Python** | pip / conda / uv |
| `scripts/stata/*.do` | **Stata** | version + ado list |

If no signal is found, report and stop — there is no environment to capture.

### Phase 1: Capture per language

**R** — emit two artifacts:
- `renv.lock` via `renv::snapshot()` (run `renv::init(bare = TRUE)` first if the project isn't renv-managed; snapshot records every package + version + source/remote and the R version). Honors the seed conventions in [`r-code-conventions.md`](../../references/rules/r-code-conventions.md).
- `sessionInfo.txt` via `Rscript -e "writeLines(capture.output(sessionInfo()), 'scripts/R/_outputs/sessionInfo.txt')"` — the human-readable companion `$audit-reproducibility` looks for.

**Python** — emit whichever matches the project's existing tooling (do not invent a new one):
- `uv.lock` (preferred when `pyproject.toml` + `uv` present — fully-resolved, hashed, cross-platform): `uv lock` / `uv export --format requirements-txt > requirements.txt`.
- `requirements.txt` via `pip freeze` (or `python -m pip freeze`) for a venv/pip project — pin `==` exactly.
- `environment.yml` via `conda env export --no-builds` for a conda project.
Always also record the interpreter version (`python --version`) in the report.

**Stata** — Stata has no lockfile, so capture the closest equivalents (mirrors [`stata-code-conventions.md`](../../references/rules/stata-code-conventions.md) §3):
- The pinned `version` line each `.do` file declares (e.g. `version 18`) — grep `scripts/stata/*.do` and report the version actually pinned.
- An ado/plus package inventory: a small `.do` that runs `which` on the user-installed commands the pipeline uses (`reghdfe`, `ivreg2`, `estout`/`esttab`, `rdrobust`, `csdid`, …) plus `ado dir` and `about`, logged to `scripts/stata/_outputs/sessionInfo.txt`.
- A note that Stata version pinning is *semantic* (`version 18` fixes command behavior), not a binary pin — the Dockerfile (Phase 2) cannot help here because Stata is licensed and not redistributable; record the exact Stata version + flavor (SE/MP/IC) + update level in the report so a replicator can match it.

### Phase 1b: Record seeds and RNG

Grep the analysis scripts for the master seed and RNG kind so the "Computational requirements" block can state them:
- **R**: `set.seed(YYYYMMDD)`, and `RNGkind()` — flag `"L'Ecuyer-CMRG"` if parallel/Monte Carlo work is present (see [`simulation-conventions.md`](../../references/rules/simulation-conventions.md)).
- **Stata**: `set seed` and `set sortseed`.
- **Python**: `numpy.random.default_rng(seed)` / `random.seed()` / framework seeds.

If the pipeline does randomized work (bootstrap, MC, RCT re-randomization, permutation inference) and **no** seed is found, surface it as a WARNING — an unseeded random result is not reproducible.

### Phase 2: Dockerfile (only with `--docker`)

Emit a `Dockerfile` that pins the OS, language version, and system libraries
as tightly as the available registries permit:
- **R** → `FROM rocker/r-ver:<X.Y.Z>` (Rocker pins the R version), `COPY renv.lock`, `RUN R -e "renv::restore()"`, plus `apt-get install` for system libs the packages need (e.g. `libcurl4-openssl-dev`, `libgdal-dev` for spatial work).
- **Python** → `FROM python:<X.Y.Z>-slim`, `COPY requirements.txt` / `uv.lock`, `RUN pip install -r requirements.txt` (or `uv sync --frozen`).
- **Stata** → cannot pin the licensed binary; emit a `Dockerfile` stub that documents the expected Stata version + flavor and leaves the `stata` install/license step to the replicator (with a comment pointing at the AEA's guidance on Stata images).

Pin a verified digest where possible (`FROM image@sha256:…`). Never invent a
digest; if one cannot be resolved, record that layer as UNVERIFIED.

### Phase 3: Verify the lockfile installs clean (best-effort; skip with `--no-verify`)

Attempt a clean restore in a throwaway location and report PASS, FAIL, or
UNVERIFIED; never overwrite the working environment:
- **R**: `renv::restore()` into a temp library, or `Rscript -e "renv::status()"` for a dry check.
- **Python**: `uv sync --frozen` / `pip install --dry-run -r requirements.txt` into a fresh venv.
- **Docker** (if `--docker`): `docker build` the image.

A FAIL means the attempted restore found a concrete problem. A missing runtime,
network restriction, inaccessible private registry, or skipped restore is
UNVERIFIED rather than FAIL or PASS. Report the limitation; do not auto-edit
the lockfile.

### Phase 4: Report

Print a paste-ready block and write it to `scripts/<lang>/_outputs/computational_requirements.md`:

```markdown
## Computational requirements

**Software:** R 4.4.1 (or: Stata 18.0 SE, update 2026-01-15; Python 3.12.3)
**OS used:** macOS 15.5 (arm64) — Dockerfile pins Ubuntu 24.04 for portability
**Key packages:** fixest 0.12.1, did 2.1.2 (full list in renv.lock)
**Random seeds:** set.seed(20260609); RNGkind("L'Ecuyer-CMRG") for the bootstrap
**Approx. runtime:** [author confirms — e.g. ~12 min, 8 cores]
**Lockfiles in package:** renv.lock, scripts/R/_outputs/sessionInfo.txt[, Dockerfile]
```

Pre-fill software/package/seed lines from the captured artifacts; leave runtime for the author to confirm.

## Output / artifacts

| Stack | Files written |
|---|---|
| R | `renv.lock`, `scripts/R/_outputs/sessionInfo.txt` |
| Python | `requirements.txt` *or* `environment.yml` *or* `uv.lock` (matching project tooling) |
| Stata | `scripts/stata/_outputs/sessionInfo.txt` (version + ado list) |
| Any (`--docker`) | `Dockerfile` |
| Always | `scripts/<lang>/_outputs/computational_requirements.md` (the paste-ready block) |

## Exit behavior

- **All captures succeeded and isolated restore passed:** report PASS.
- **`--no-verify`, missing runtime, or inaccessible dependency source:** report
  UNVERIFIED for restoreability while retaining the captured artifacts.
- **A missing-seed WARNING on a randomized pipeline:** exit 0 with the warning surfaced — reproducibility is compromised but the snapshot still wrote.
- **Verify FAIL (lockfile will not resolve):** block a pre-release `$commit`.
  Report the unresolvable package; do not silently "fix" the lockfile.
- **No stack detected in Phase 0:** exit 1 with the directories searched.

## Cross-references

- [`replication-protocol.md`](../../references/rules/replication-protocol.md)
  — numeric tolerances.
- [`r-code-conventions.md`](../../references/rules/r-code-conventions.md) — R
  seeding and output paths.
- [`stata-code-conventions.md`](../../references/rules/stata-code-conventions.md)
  — Stata version and package capture.
- [`simulation-conventions.md`](../../references/rules/simulation-conventions.md)
  — reproducible random streams.
- [`confidential-data.md`](../../references/rules/confidential-data.md) —
  environment metadata remains releasable when raw data is not.
- [`$audit-reproducibility`](../audit-reproducibility/SKILL.md) — consumes the
  environment capture.
- [`$data-analysis`](../data-analysis/SKILL.md),
  [`$stata-replication`](../stata-replication/SKILL.md), and
  [`$simulation-study`](../simulation-study/SKILL.md) — producing pipelines.
- [AEA Data Editor checklist](https://aeadataeditor.github.io/) / [openICPSR](https://www.openicpsr.org/) / DCAS — the external standards this skill targets.

## What this skill does NOT do

- **Re-run your analysis or check your numbers.** It captures the environment;
  [`$audit-reproducibility`](../audit-reproducibility/SKILL.md) verifies the
  manuscript's numeric claims.
- **Package or de-identify data.** Lockfiles describe software, not data. Disclosure avoidance, de-identification, and data-availability statements are out of scope — see [`confidential-data.md`](../../references/rules/confidential-data.md).
- **Upgrade or "fix" your dependencies.** It records what the code currently uses. If a verify FAIL surfaces a yanked version, you decide whether to pin an alternative.
- **Pin a Stata binary.** Stata is licensed and not redistributable; the skill records the exact version/flavor/update so a replicator can match it, but cannot containerize it.
