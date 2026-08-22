# Known limitations

These limitations define the boundary of the `1.2.2` stability claim. None
weakens the package's research-governance gates; each identifies behavior that
depends on the host environment or an explicit user choice.

## Installation and discovery

- Codex discovers 58 packaged skills (52 source-derived skills plus the 6
  ManageRAW skills) and
  the bundled lifecycle hooks from the plugin. Project-scoped custom agents
  are a separate Codex configuration
  surface, so the plugin also ships portable role files and the project
  initializer copies all 19 agent TOMLs into a project's `.codex/agents/`
  directory.
- ManageRAW state records ownership and routing but is not an instruction
  engine. Global, root, and nested `AGENTS.md` remain the effective Codex
  instruction chain, and same-named skills do not merge automatically.
- Plugin and project hooks are non-managed code. Codex skips them until the
  user reviews and trusts their current definitions. The skills remain usable
  when hooks are not trusted, but automatic git checks, claim-staleness notes,
  and compaction continuity do not run.
- Initialized projects receive files only. The initializer does not install
  the plugin globally or change the user's Codex configuration.

## Optional academic runtimes

- LaTeX, Quarto, R, Stata, Julia, Pandoc, and journal-specific utilities are
  external dependencies. A workflow must report the relevant operation as
  `UNVERIFIED` when its runtime is absent; it must never convert a skipped
  compile, render, estimation, or package check into a pass.
- Stata automation may use a separately installed MCP server, but MAW Codex
  does not bundle, authorize, or configure that server.
- Gmail, Drive, Calendar, GitHub, browser, and other connected services depend
  on capabilities available in the active Codex session. Skills must degrade
  to an exact handoff or a documented manual step when a connector is absent.

## Behavior intentionally not reproduced

- The package does not read private transcript serialization or estimate the
  remaining token count from undocumented session files. Context-management
  skills use visible task state, explicit checkpoints, and Codex compaction
  hooks.
- The package does not silently enable desktop notifications, background
  logging, scheduled jobs, permission bypasses, broad network access, or
  destructive Git operations.
- Scheduled routines require a user-created Codex automation or an explicit
  recurring task. Installing the plugin alone does not schedule work.
- Upstream synchronization is review-first. Fetching Pedro's repository can be
  automated, but changes are never auto-merged into MAW Codex because the two
  repositories have intentionally different runtimes and layouts.
- UAW's three-way reconciliation and SAW's sanitization boundaries have
  deterministic semantic contracts, but no future MAW base or real project
  slice exists yet to forward-test those maintenance operations. Their first
  project use must preserve unresolved behavior as `UNVERIFIED` and inspect
  the exact update or export before adoption.

## Verification boundary

- Structural, provenance, hook, initializer, and representative workflow
  checks are local release gates. The included GitHub Actions workflow has not
  run remotely until this independent repository is published to GitHub.
- The GitHub Pages URL in public metadata is the intended publisher-controlled
  endpoint. It is not verified live until the repository exists at the stated
  URL, Pages uses GitHub Actions as its source, and the deployment completes.
- Representative forward tests exercise high-risk decisions and failure
  semantics. They do not substitute for compiling every possible manuscript,
  running every supported statistical package, or validating every
  institution's disclosure regime.
- Journal policies, software releases, submission rules, and other unstable
  facts require current primary-source verification at the time of use.
- Restricted-data clearance is institution-specific. The disclosure workflow
  helps identify and document risks; it does not replace an authorized
  disclosure officer or enclave review.

## Deferred hardening after the username migration

The 2026-08-22 deep audit identified three non-blocking hardening opportunities
that are intentionally outside release `1.2.2`: make optional hook failures
more observable, bound hook passport discovery, and add stronger source/target
overlap rejection to migration helpers. They require separate behavioral tests
and are not represented as resolved by the GitHub identity migration.

GitHub Pages availability remains externally verified after each authorized
push. Repository redirects from `dipietra` are compatibility behavior only; the
retired Pages namespace is not a supported endpoint.
### Local marketplace state after release 1.2.2

Publishing the repository and GitHub Pages does not update the canonical
personal-store copy or an existing Codex cache. Those external local surfaces
may remain on `1.2.0` until a separately authorized installer update is run;
release `1.2.2` does not claim otherwise.