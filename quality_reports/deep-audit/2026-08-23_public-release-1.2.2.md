# Deep audit: MAW Codex 1.2.2 public-release readiness

Date: 2026-08-23
Scope: repository-wide release readiness, GitHub identity migration, plugin packaging, Pages, attribution, installation, and known limitations
Repository head before local repairs: `02c76b2c91f673b634c8496b3c49fbd422bbee09`
Final classification: **NOT CLEAN for broad public announcement**

## Executive decision

The local `1.2.2` package is suitable for a controlled private review by Pedro if the accepted Windows launcher defect and exact workaround accompany the invitation. The repository and Pages links are not yet the reviewed surface: the documentation repairs remain local, the GitHub repository Website metadata still points to the retired `dipietra` Pages URL, and fresh same-commit CI and Pages verification have not occurred.

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

The existing successful remote stable-gates and Pages runs apply only to commit `02c76b2c91f673b634c8496b3c49fbd422bbee09`. They do not validate this repaired local documentation tree.

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

## Open findings

| ID | Severity | Surface | Finding | Required disposition |
|---|---:|---|---|---|
| OPEN-001 | P1 | `scripts/maw.ps1` / `maw.cmd` | The launcher accepts the first PATH Python candidate without probing it; a `WindowsApps\python.exe` alias can terminate the advertised command before bundled-Python fallback. | Accepted exception for `1.2.2`; use the documented direct bundled-Python command. No `1.2.3` is promised. |
| OPEN-002 | P1 | `skills/deep-audit/SKILL.md` | The skill calls default mode read-only but unconditionally requires a workspace report file. | Reconcile inline reporting with an explicit write authorization in a future maintenance cycle. |
| OPEN-003 | P1 | `.codex/agents/r-package-reviewer.toml` and portable role | The reviewer uses `workspace-write`, while its intended review contract is read-only and the portable wording is contradictory. | Align both surfaces in a future maintenance cycle. |
| OPEN-004 | P1 | `references/rules/orchestrator-research.md` | “Commit when user signals” is weaker than the repository's separate explicit-authorization rule. | Require a separate explicit commit request routed through `$mawcodex:commit`. |
| OPEN-005 | P1 | GitHub repository metadata | The Website field still uses `https://dipietra.github.io/mawcodex/`. | After explicit authorization, set it to `https://gdipietra.github.io/mawcodex/` and verify remotely. |
| OPEN-006 | P2 | `references/rules/verification-protocol.md` | Quarto wording says a sync helper can “render and deploy” without a clear external-action authorization boundary. Actual external behavior remains UNVERIFIED. | Clarify local staging versus authorized deployment. |
| OPEN-007 | P2 | `hooks/scripts/maw_hook.sh` | POSIX hook launch selects the first visible Python without probing compatibility; broken-candidate fail-open behavior lacks a representative test. | Probe compatible Python 3 candidates and add regression tests in a future maintenance cycle. |
| OPEN-008 | P1 | Publication state | Current repairs are uncommitted/unpushed and lack fresh same-SHA CI and Pages evidence. | Commit and push only after explicit authorization, then verify CI, Pages, and the exact remote SHA. |

## Public-release sequence

1. Obtain explicit authorization for a scoped commit and push that excludes the user's untracked migration handoff unless separately requested.
2. Obtain explicit authorization to update the GitHub repository Website metadata.
3. Verify the remote content, stable-gates workflow, Pages workflow, canonical site URL, and exact shared commit SHA.
4. Send Pedro a private invitation that discloses the accepted P1 launcher limitation and direct bundled-Python workaround.
5. Incorporate Pedro's considerations before sharing with close colleagues.
6. Reassess the open governance P1s before a broad public announcement.

Creating an open GitHub issue for `maw.cmd` is reasonable for discoverability, but it is an external mutation and remains separately unauthorized.

## Working-tree checkpoint

The audit updated public and release documentation plus generated validation manifests. The pre-existing untracked file `quality_reports/github-username-migration-handoff-2026-08-22.md` was neither edited nor included in any Git action.

Stop condition reached: local fixes and full deterministic validation are complete; external publication actions are pending explicit authorization.
