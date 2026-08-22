# Changelog

All notable MAW Codex changes are documented here.

## [1.2.2] - 2026-08-22

### Changed

- Migrated the canonical GitHub repository, Pages site, support links, and
  plugin metadata from dipietra to gdipietra.
- Strengthened public-site and release-evidence validation so a redirected Git
  repository cannot mask dead Pages canonicals or stale source remotes.
- Added explicit per-component classification and revision summaries to the
  project-template provenance manifest.
- Corrected the deep-audit hook test command to invoke the packaged unit tests.

## [1.2.1] - 2026-08-22

### Added

- A public EN-US website for GitHub Pages with prominent original-work credit,
  a source-to-Codex translation map, a searchable 58-skill capability ledger,
  detailed ManageRAW/JAW/CAW/PAW/LAW/UAW/SAW explanations, and public support,
  privacy, terms, and credits pages.
- A GitHub Pages workflow that publishes only the static `docs/` site through
  GitHub's supported Pages artifact and OIDC deployment actions.
- Public-release instructions that keep local preparation separate from
  commit, push, tag, release, Pages activation, and marketplace submission.

### Changed

- Added publisher-controlled website, repository, privacy, and terms metadata
  to the plugin manifest.
- Made the shared XeLaTeX preamble tolerant of missing Lato and Helvetica font
  families by selecting an installed fallback instead of failing immediately.
- Expanded attribution language so the 52 source-derived capabilities and the
  Codex-native control plane are visibly distinct.

## [1.2.0] - 2026-07-28

### Added

- ManageRAW (`manageraw`), a project control-plane agent that coordinates MAW
  adoption, configuration, instruction layers, updates, reusable exports, and
  coexistence with specialist plugins.
- CAW, PAW, LAW, UAW, and SAW alongside the revised JAW onboarding skill.
- Tracked `.maw/profile.yaml` and `.maw/lock.json`, ignored personal settings,
  durable update history, sanitized slices, and a standard-library state
  validator.
- Forward-use-case coverage for ongoing LaTeX teaching projects and mixed
  Stata/R research projects.
- Deterministic profile, personal-overlay, instruction-layer, and management
  skill contracts, bringing the unit suite to 48 tests.

### Changed

- Separated onboarding, personalization, instruction layering, upstream
  reconciliation, and reusable-pattern export into narrow skills.
- Made UAW and SAW explicit-only and kept external actions behind separate
  authorization.

## [1.1.0] - 2026-07-28

### Added

- JAW (`$jaw`), a Codex-native readiness skill for joining MAW to ongoing
  research, teaching, or mixed academic projects without overwriting their
  history, instructions, or source authority.
- Research, teaching, and deployment-report profiles for plugin-only, thin,
  selective, and full integrations.
- An original purple MAW icon, academic Codex pet, and plugin thumbnail based
  on Giovanni Di Pietra's sketch.
- Syntax-contract tests for executable TeX, Quarto, TikZ, and YAML assets.

### Fixed

- Made command migration format-aware: TeX typesets `\$skill` safely while
  Quarto keeps normal `$skill` code spans.
- Replaced invalid HTML provenance comments in TeX and YAML templates with
  native `%` and `#` comments.

## [1.0.0] - 2026-07-28

### Added

- 52 Codex-native academic workflow skills with generated interface metadata.
- 18 project custom-agent TOMLs and 18 portable role definitions.
- 32 adapted research-governance rules, 8 runtime references, one retained
  historical reference, and 21 reusable artifact templates.
- A non-overwriting academic project initializer with local Git preflight and
  rollback.
- Preview-first installation through the canonical local Codex marketplace,
  preserving an existing catalog identity and all existing entries.
- Four opt-in lifecycle hooks plus documented replacements for all seven
  upstream hook intents.
- Hash-bound dispositions for all 13 provider runtime surfaces, including
  settings, output styles, status line, and quick reference.
- Exact conversion or disposition coverage for all 211 files tracked at the
  fixed upstream commit.
- Fixed-source, attribution, link, provider-residue, and project-template
  provenance validation.
- Fifteen independent forward tests and fourteen deterministic semantic
  contract tests for high-risk behavior.

### Changed

- Rebuilt provider-specific commands, agents, permissions, hooks, and
  orchestration as Codex-native surfaces.
- Replaced permission bypass and transcript-internal behavior with explicit
  authorization, visible state, and fail-safe local checks.
- Preserved the upstream fork as a separate read-only tracking source so later
  Pedro releases can be compared and selectively ported.
