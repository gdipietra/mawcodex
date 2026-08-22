# Deep audit: MAW Codex 1.2.1 public-release candidate

Date: 2026-08-22
Workspace: `C:\Codex\mawcodex`
Local base commit: `da2e82257265eb114b41d6a75f8307ad6bce8db8`
Package version: `1.2.1`
Fixed upstream baseline: `C:\GitHub\claude-code-my-workflow` at `be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`)

## Scope

This audit covers the locally prepared MAW Codex 1.2.1 plugin, its English-language public site, GitHub Pages workflow, conversion records, deterministic project-template migration, and local release evidence. It does not claim that a GitHub repository, tag, release artifact, marketplace entry, or live Pages deployment exists.

## Release-state conclusion

**CONDITIONALLY CLEAN**

The repository is locally release-ready under its deterministic stable-release contract. No genuine local P0, P1, or P2 defect remained after repairs. The conditional classification preserves four external or environment-dependent evidence gaps: live GitHub Pages behavior, remote CI/tag/artifact alignment, browser-rendered desktop/mobile inspection, and an actual XeLaTeX consumer compile. Three independent reviewer lenses also remained `UNVERIFIED` after the subagent runtime was interrupted; they are not counted as PASS.

## Deterministic evidence

| Gate | Result | Evidence |
|---|---:|---|
| Public-site structural validator | PASS | 1 passed, 0 failed; required pages, internal links, `en-US`, credits, manifest URLs, workflow tokens, and the 58-entry capability ledger were checked. |
| Source clone and fixed baseline | PASS | Local immutable source clone matched the recorded upstream commit. |
| Package validation | PASS | 13 passed, 0 warnings, 0 failures. |
| Official plugin manifest validator | PASS | `.codex-plugin/plugin.json` accepted. |
| Official skill validators | PASS | 58 of 58 packaged skills accepted. |
| Unit and behavioral smoke tests | PASS | 48 of 48 passed, 0 skipped. |
| Stable-release validation | PASS | 14 passed, 0 warnings, 0 failures. |
| Distribution snapshot | PASS | `docs/conversion/OFFICIAL_VALIDATION.json` records the authoritative post-gate release tree; local `quality_reports/` evidence is deliberately excluded from distributable bytes. |
| Whitespace/error scan | PASS | `git diff --check` returned no errors. |
| Credential-pattern review | PASS with documented false positive | The only hit was a deliberately fake token fixture in `tests/test_manageraw_state.py`; no release credential was identified. |
| Brand asset copy | PASS | The site icon and packaged source icon had identical SHA-256 hashes. |

## Independent review lenses

| Lens | State | Finding |
|---|---:|---|
| Provenance and attribution | PASS | No local provenance defect was found. The site distinguishes Pedro H. C. Sant'Anna's original workflow from Giovanni Di Pietra's Codex-native adaptation and native MAW additions, records the fixed baseline, preserves third-party lineage, and disclaims endorsement. |
| Public-site factual/content review | UNVERIFIED | Reviewer runtime was interrupted before producing a result. Deterministic content checks passed, but this independent lens is not promoted to PASS. |
| Release-engineering review | UNVERIFIED | Reviewer runtime was interrupted before producing a result. Local gates passed, but no remote CI, tag, release, or artifact exists to inspect. |
| Frontend/accessibility review | UNVERIFIED | Reviewer runtime was interrupted. Structural accessibility provisions exist, but browser rendering could not be inspected in this environment. |

## Repairs completed during the audit

1. Reconciled the manifest, package metadata, changelog, citation metadata, notice, and conversion records at version 1.2.1.
2. Implemented an English-language Pages site with original credit, a precise adapted-versus-native contribution boundary, detailed capability translation, support, privacy, terms, and a 404 page.
3. Added a GitHub Pages Actions workflow that publishes only `docs/` and uses least-privilege Pages permissions.
4. Converted the Lato/Helvetica XeLaTeX portability fix into a named, deterministic project-template migration and corresponding reconstruction validator.
5. Removed a non-reproducible edit from an imported upstream README; native documentation now records the adaptation outside the immutable imported bytes.
6. Added a dedicated public-site validator and integrated it into package validation.
7. Hardened release-gate dependency discovery against a malformed temporary PyYAML directory and used an isolated workspace validation dependency, without adding it to the plugin runtime.
8. Made the public-site validator importable both as a package module and as a direct script.

## Attribution and capability-accounting checks

- The public ledger contains exactly 58 packaged capabilities.
- Exactly 52 entries are identified as adaptations of the fixed Pedro H. C. Sant'Anna baseline.
- Exactly 6 entries are identified as native MAW Codex capabilities: ManageRAW, JAW, CAW, PAW, LAW, and SAW.
- The site explains the Codex-native translation in execution terms rather than claiming mechanical equivalence or unsupported parity.
- Original authorship, adaptation authorship, upstream URL, fixed commit, licenses, third-party lineage, and no-endorsement language are visible in the public materials.

## Explicitly unverified

- `UNVERIFIED`: the intended Pages URL `https://dipietra.github.io/mawcodex/` is not live and was not inspected.
- `UNVERIFIED`: no Git remote is configured, so remote repository ownership, branch protection, Actions execution, tag, release, and downloadable artifact alignment were not inspected.
- `UNVERIFIED`: desktop and mobile rendering in a real browser; the available browser runtimes could not initialize.
- `UNVERIFIED`: XeLaTeX resolution of Lato, Helvetica, and fallback branches; no usable TeX Live compiler was available in the current environment.

## Publication boundary

No commit, tag, push, repository creation, GitHub Pages activation, GitHub release, marketplace publication, or other external publication was performed. Those actions require a separate explicit authorization. The local source and `docs/conversion/OFFICIAL_VALIDATION.json` are the release-candidate authority until that authorization is provided.