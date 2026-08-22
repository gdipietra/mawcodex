# Deep audit: GitHub username migration `dipietra` -> `gdipietra`

Date: 2026-08-22
Mode: read-only, no `--fix`
Repository: `C:\Codex\mawcodex`
Target commit: `22a6e123880af30e148b98bf8fb41d3553fffd00`
Package version: `1.2.1`
Final state: **NOT CLEAN**

## Authorization boundary

The audit read local and public state and ran checked-in validators. It made no operational repository edit, remote change, commit, push, deployment, release, marketplace update, or other external mutation. The only new artifact produced by this audit is this checkpoint report. The user-supplied handoff remains preserved as an untracked file.

## Starting state

- Branch: `main`, tracking `origin/main`.
- HEAD and remote `main`: `22a6e123880af30e148b98bf8fb41d3553fffd00`.
- Existing local origin: `https://github.com/dipietra/mawcodex.git`.
- Sole pre-audit worktree change: untracked `quality_reports/github-username-migration-handoff-2026-08-22.md`.
- Git author identity: `Giovanni Di Pietra <30128409+gdipietra@users.noreply.github.com>`.
- GitHub authenticated identity: `gdipietra`, numeric ID `30128409`.
- No tracked `CNAME`.

## Source baseline

The immutable source baseline remains `C:\GitHub\claude-code-my-workflow` at `be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`). Pedro H. C. Sant'Anna's upstream remains `https://github.com/pedrohcgs/claude-code-my-workflow`. The dated baseline recorded Giovanni's fork under the historical `dipietra` namespace.

## Deterministic checks

| Command/check | Result | Evidence |
|---|---:|---|
| `python scripts/validate_package.py` | PASS | 13 passed, 0 warned, 0 failed. |
| `python scripts/run_skill_validators.py` | PASS | 58/58 skills passed. |
| `python -m unittest discover -s tests` | PASS | 48 tests passed. |
| `python -m unittest tests.test_hooks` | PASS | 5 targeted hook tests passed. |
| `python scripts/validate_public_site.py` | PASS, but insufficient | Structural consistency is internally stale and does not test current live endpoints. |
| `python scripts/check_source_clone.py` | FAIL | Actual fork origin is `gdipietra`; checker still requires `dipietra`. |
| `python scripts/validate_package.py --release` | PASS, but contradicted | 14 passed, yet the independently executed required source-clone contract fails. |
| `python scripts/test_hooks.py` | UNAVAILABLE | The deep-audit skill advertises a path that does not exist. Hook behavior was tested through unittest instead. |
| Secret-pattern scan | PASS with false positive | Only the deliberate fake `ghp_...` fail-closed fixture in `tests/test_manageraw_state.py:221`. |
| `git diff --check` | PASS | No tracked whitespace error. |

`run_release_gates.py` was deliberately not executed because it writes tracked official evidence. In read-only mode its component checks were executed separately. It cannot be treated as a clean release gate while `check_source_clone.py` fails.

## GitHub and Pages evidence

- `gdipietra/mawcodex` is public, default branch `main`, repository ID `1342859755`.
- Both old and new Git clone URLs resolve `main` to `22a6e123880af30e148b98bf8fb41d3553fffd00`.
- `https://github.com/dipietra/mawcodex` returns `301` to `https://github.com/gdipietra/mawcodex`.
- `https://dipietra.github.io/mawcodex/`, `/privacy.html`, and `/terms.html` return `404`.
- The corresponding `https://gdipietra.github.io/mawcodex/` endpoints return `200`.
- Pages API reports `build_type=workflow`, no CNAME, and the successful deployment run `32577194556` at HEAD `22a6e12`.
- The live new homepage declares the old, now-404 Pages URL as its canonical URL.
- The remote public plugin manifest still exposes old author, repository, homepage, website, privacy, and terms URLs.

## Namespace inventory and classification

Tracked scan results before changes:

- 15 tracked files contain an old GitHub or Pages URL.
- 16 tracked files contain the broader text `dipietra`.
- 0 tracked files contain `gdipietra`.

### Current operational surfaces: migrate

1. `.codex-plugin/plugin.json`
2. `README.md`
3. `docs/PUBLISHING.md`
4. `docs/UPSTREAM_SYNC.md`
5. `docs/capabilities.html`
6. `docs/credits.html`
7. `docs/index.html`
8. `docs/privacy.html`
9. `docs/support.html`
10. `docs/terms.html`
11. `scripts/check_source_clone.py`
12. `scripts/validate_public_site.py`

Current release-state prose in `docs/conversion/RELEASE_REPORT.md` and `docs/conversion/KNOWN_LIMITATIONS.md` also needs reconciliation even where it does not contain the old username.

### Historical/provenance surfaces: preserve

1. `docs/conversion/SOURCE_BASELINE.md`
2. `docs/conversion/OFFICIAL_VALIDATION.json`
3. `docs/conversion/steps/001-fork-and-source-boundary.md`
4. `quality_reports/deep-audit/2026-08-22_public-release.md`

Do not mechanically rewrite these dated records. Add a dated superseding migration record that identifies `gdipietra` as the successor namespace and records old repository redirect versus old Pages 404 behavior.

## Genuine findings

### P1

- **GHM-001, broken current plugin URLs:** `.codex-plugin/plugin.json:7` and lines 9-10, 36-38 expose old Pages endpoints that return 404 and the old publisher namespace.
- **GHM-002, broken source-fork contract:** `scripts/check_source_clone.py:16` and `docs/UPSTREAM_SYNC.md:7` require the old fork URL, causing the live source check to fail.
- **GHM-003, false PASS in public-site validation:** `scripts/validate_public_site.py:16` positively requires old URLs and does not reject retired operational namespaces or verify canonical/live endpoint behavior.
- **GHM-004, incomplete release gate:** `scripts/validate_package.py:1719` accepts stale checked-in source/validator evidence without reconciling current origin/upstream; `.github/workflows/gates.yml` does not execute the live source checker. Release validation therefore passes while a required contract fails.
- **GHM-005, current status claims ahead of evidence:** `README.md:11` and current release/limitations prose still describe a stable or pre-publication state inconsistent with the failed source contract and already-renamed live repository.
- **DA-001, nonexistent advertised command:** `skills/deep-audit/SKILL.md:42` points to missing `scripts/test_hooks.py`.
- **DA-002, incomplete per-component conversion records:** all 18 entries in `docs/conversion/PROJECT_TEMPLATE_MANIFEST.json:7` have paths, hashes, modes, and replacements but no allowed classification or component-specific revision record required by `AGENTS.md`.

### P2

- **GHM-006, stale deployed metadata and links:** `docs/index.html:11` and the other public pages declare old 404 canonicals and old source/clone/support links.
- **GHM-007, stale publishing lifecycle:** `docs/PUBLISHING.md:5` targets old endpoints and still instructs creation of a repository that already exists under `gdipietra`.
- **DA-003, invisible fail-open hook failures:** `hooks/scripts/maw_hook.py:579` and the PowerShell counterpart swallow internal exceptions and exit 0 without a sanitized warning that enforcement was skipped.
- **DA-004, unbounded hook passport scan:** `hooks/scripts/maw_hook.py:366` can enumerate/read unbounded passport content under a five-second hook timeout.
- **DA-005, source/target overlap risk:** `scripts/migrate_from_claude.py:282` and related migration executables do not reject equal or ancestor-overlapping source and target roots before writes.

## False positives and resolved reviewer gaps

- `.codex/agents/r-package-reviewer.toml` uses `workspace-write`, but its role explicitly permits scoped report writes and instructs saving a report under `quality_reports/`; this is an explicit verification-write need, not an unbounded editor role.
- One reviewer could not inspect the handoff because its own runtime failed. The parent audit read the handoff completely and reproduced its HEAD, remote, occurrence counts, and stop boundary.
- The fake GitHub token in `tests/test_manageraw_state.py:221` is a deliberate secret-detection test fixture, not a credential.
- Old URLs in the four classified historical records are evidence, not stale current metadata.

## UNVERIFIED

- Browser-rendered visual behavior of the renamed Pages site was not inspected; HTTP, canonical metadata, Pages API, and Actions state were inspected.
- Post-migration local and remote state is not verified because no migration edit, remote change, commit, push, or deployment was authorized in this audit.
- Marketplace metadata outside this repository was not changed or revalidated against a migrated package because no migrated package exists yet.

## Pre-change checkpoint and proposed repair sequence

1. Preserve HEAD `22a6e123880af30e148b98bf8fb41d3553fffd00` and the supplied handoff as rollback evidence.
2. With explicit local-fix authorization, update local `origin` only after confirming its exact old value; preserve any unrelated remotes.
3. Migrate the 12 current operational surfaces to `gdipietra`; preserve the four historical records and add a dated superseding conversion/migration record.
4. Strengthen source, public-site, release, and CI validators so retired operational URLs fail while historical allowlisted records remain valid.
5. Reconcile current release-state prose and decide whether the metadata change requires patch version `1.2.2`.
6. Address or explicitly defer the collateral deep-audit P1/P2 findings before calling the package clean.
7. Rerun source check, package/release checks, 58 skill validators, hooks, 48 unit tests, public-site structural checks, secret scan, and live endpoint checks.
8. Stop again before commit, push, Pages deployment, release, or marketplace update unless each external action receives fresh explicit authorization.

No repair was made in this audit.