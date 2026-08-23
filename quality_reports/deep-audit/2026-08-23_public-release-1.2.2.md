# Deep audit: MAW Codex 1.2.2 public-release readiness

Date: 2026-08-23
Scope: repository-wide release readiness, GitHub identity migration, plugin packaging, Pages, attribution, installation, and known limitations
Repository head before local repairs: `02c76b2c91f673b634c8496b3c49fbd422bbee09`
Final classification: **NOT CLEAN for broad public announcement**

## Executive decision

The local `1.2.2` package remains suitable for a controlled private review by Pedro if the accepted Windows launcher defect and exact workaround accompany the invitation. Subsequent separately authorized actions established commit `cc82cede0eed6b721f23cc82862e0ad189db2824` as the verified publication/content checkpoint: stable-gates run `32666609822` and GitHub Pages run `32666609835` succeeded, the public endpoint returned HTTP 200, and the repository homepage metadata is canonical. Those later actions do not change this audit's own no-external-action boundary.

This audit does not create a `1.2.3` plan. The `maw.cmd` defect is retained as an accepted P1 exception for `1.2.2`; no implementation repair is included.

No commit, push, GitHub issue, repository-metadata update, store update, deployment, message, or other external action was performed by this audit.

## Deterministic evidence

| Gate | Result |
|---|---:|
| Auxiliary-source manifest | PASS: 48 files; 211/211 upstream source files covered |
| Runtime surfaces | PASS: 13 |
| Package gates | PASS: 13/13; 0 warnings; 0 failures |
| Public-site validator | PASS: 1/1 |
| Official plugin validation | PASS |
| Packaged skills | PASS: 58/58 |
| Unit tests | PASS: 51/51 |
| Stable-release gates | PASS: 14/14; 0 warnings; 0 failures |
| Source clone contract | PASS against baseline `be53c12f235996dff41fb7f21580506fd2dd8d50` |
| `git diff --check` | PASS: no whitespace errors |

The validators used the bundled Codex Python runtime and the pinned local PyYAML validation dependency. One incomplete unrelated default dependency directory was ignored. Git diagnostics required command-local `safe.directory` because Windows reported dubious ownership; repository configuration was not changed.

Commit `cc82cede0eed6b721f23cc82862e0ad189db2824` is now the verified publication/content checkpoint for the repaired documentation. Stable-gates run `32666609822` and GitHub Pages run `32666609835` succeeded, and the public Pages endpoint returned HTTP 200. This evidence applies only to that checkpoint and does not validate later commits.

Four independent first-round lenses and targeted second-round reviewers produced the findings below. After the last three documentation repairs, the reviewer that raised them returned `RESOLVED`. One additional fresh-context spot check is `UNVERIFIED` because its command helper failed during process initialization before reading any file; this is an evidence limitation, not a PASS.

## Closed findings

| Finding | Severity | Disposition |
|---|---:|---|
| Current local tree was conflated with the previously deployed snapshot | P1 | Repaired across README, release report, and readiness statement |
| Windows launcher defect was described as non-blocking/P2 | P1 | Reclassified as an explicit accepted P1 exception |
| Canonical installation guide omitted exact explicit-runtime fallbacks | P2 | Repaired for preview, initial apply, and update |
| Packaged skill examples used bare rather than namespaced identifiers | P1 | Repaired to `$mawcodex:*` forms |
| Release chronology assigned 1.2.1 features to 1.2.2 | P2 | Repaired; actual 1.2.2 delta is stated |
| Historical `dipietra` source-fork identity was not labeled historical | P2 | Repaired without changing the immutable baseline |
| Critical Markdown contained literal escape artifacts and grammar errors | P2/P3 | Repaired |
| Personal-store evidence lacked an authorization-time boundary | P1 | Clarified as an earlier separately authorized action, not part of this audit |
| GitHub repository homepage metadata was stale | P1 | Resolved separately; the canonical Pages URL is configured and publicly verified |
| Publication lacked same-SHA remote evidence | P1 | Resolved at checkpoint `cc82cede0eed6b721f23cc82862e0ad189db2824`; both workflows succeeded and Pages returned HTTP 200 |

## Open findings

| ID | Severity | Surface | Finding | Required disposition |
|---|---:|---|---|---|
| OPEN-001 | P1 | `scripts/maw.ps1` / `maw.cmd` | The launcher accepts the first PATH Python candidate without probing it; a `WindowsApps\python.exe` alias can terminate the advertised command before bundled-Python fallback. | Accepted exception for `1.2.2`; use the documented direct bundled-Python command. No `1.2.3` is promised. |
| OPEN-002 | P1 | `skills/deep-audit/SKILL.md` | The skill calls default mode read-only but unconditionally requires a workspace report file. | Reconcile inline reporting with an explicit write authorization in a future maintenance cycle. |
| OPEN-003 | P1 | `.codex/agents/r-package-reviewer.toml` and portable role | The reviewer uses `workspace-write`, while its intended review contract is read-only and the portable wording is contradictory. | Align both surfaces in a future maintenance cycle. |
| OPEN-004 | P1 | `references/rules/orchestrator-research.md` | “Commit when user signals” is weaker than the repository's separate explicit-authorization rule. | Require a separate explicit commit request routed through `$mawcodex:commit`. |
| OPEN-006 | P2 | `references/rules/verification-protocol.md` | Quarto wording says a sync helper can “render and deploy” without a clear external-action authorization boundary. Actual external behavior remains UNVERIFIED. | Clarify local staging versus authorized deployment. |
| OPEN-007 | P2 | `hooks/scripts/maw_hook.sh` | POSIX hook launch selects the first visible Python without probing compatibility; broken-candidate fail-open behavior lacks a representative test. | Probe compatible Python 3 candidates and add regression tests in a future maintenance cycle. |

## Public-release sequence

1. Commit `cc82cede0eed6b721f23cc82862e0ad189db2824` was pushed under separate explicit authorization and is the verified publication/content checkpoint.
2. Repository homepage metadata was separately updated to the canonical Pages URL.
3. Stable-gates run `32666609822` and GitHub Pages run `32666609835` succeeded, and the public endpoint returned HTTP 200.
4. Send Pedro a private invitation that discloses the accepted P1 launcher limitation and direct bundled-Python workaround.
5. Incorporate Pedro's considerations before sharing with close colleagues.
6. Reassess the open governance P1s before a broad public announcement.

GitHub [issue #1](https://github.com/gdipietra/mawcodex/issues/1) tracks the accepted `maw.cmd` launcher defect and is open with no milestone.

## Working-tree checkpoint

The audit updated public and release documentation plus generated validation manifests. The pre-existing untracked file `quality_reports/github-username-migration-handoff-2026-08-22.md` was neither edited nor included in any Git action.

Post-publication verification is complete for checkpoint `cc82cede0eed6b721f23cc82862e0ad189db2824`; later commits require fresh same-SHA remote verification, and broader communication remains subject to the planned human-feedback sequence.
