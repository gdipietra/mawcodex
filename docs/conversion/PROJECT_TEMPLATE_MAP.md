# Academic project-template map

Source boundary: upstream commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`).

The starter project is distributed through `scripts/init_project.py`. Imported
files and exact hashes are recorded in
`docs/conversion/PROJECT_TEMPLATE_MANIFEST.json`.

## Directly adapted source assets

| Source surface | MAW Codex destination | Treatment |
| --- | --- | --- |
| `Preambles/` | `assets/project-template/Preambles/` | Preserve shared LaTeX palette and TikZ conventions; use `$skill-name` syntax. |
| `Quarto/` | `assets/project-template/Quarto/` | Preserve the RevealJS theme and working sample; use Codex skill invocation. |
| `Slides/` | `assets/project-template/Slides/` | Preserve the self-contained Beamer sample and bibliography smoke test. |
| `scripts/R/` | `assets/project-template/scripts/R/` | Preserve the seeded, numbered, project-relative analysis pipeline. |
| `Bibliography_base.bib` | project root | Preserve the starter bibliography. |
| `scripts/check-palette-sync.py` | project `scripts/` | Direct deterministic port. |
| `scripts/check-tikz-prevention.py` | project `scripts/` | Direct deterministic port with Codex skill names. |
| `scripts/quality_score.py` | project `scripts/` | Preserve the artifact scoring gate and route its rule reference natively. |
| `explorations/README.md` | project `explorations/` | Preserve graduate/archive discipline; replace Claude rule paths. |
| `quality_reports/did_validation.md` | `docs/conversion/upstream-evidence/` | Retain as source-validation evidence, not as a new project's result. |
| `templates/` (21 files) | `assets/templates/` then project `templates/` | Preserve all reusable records and TikZ snippets; rewrite the skill-authoring template natively. |

## Native project additions

- An academic `AGENTS.md` with explicit Orient, Specify, Plan, Implement,
  Verify, and Release modes.
- Applied-microeconomics safeguards covering estimands, treatment timing,
  comparison groups, staggered adoption, clustering, pre-trend interpretation,
  attrition, and alternative estimands.
- Local/cloud/Overleaf source-role rules and an explicit sync authorization
  boundary.
- A clean `MEMORY.md`, data roles, quality-report routing, safe `.gitignore`,
  and empty durable directories.
- A tracked ManageRAW profile and version lock, ignored personal overlay,
  history and sanitized-slice folders, and a standard-library state checker.
- Cross-platform standard-library project validation and passport-freshness
  checks.
- A non-mutating pre-commit gate plus an installer that previews its
  repository-local Git setting before applying it.
- Optional project-local copies of all 19 custom-agent TOMLs and all portable
  role/rule references.

## Replaced or intentionally omitted

| Upstream surface | Disposition | Reason |
| --- | --- | --- |
| `CLAUDE.md` | Replaced by academic `AGENTS.md` | Codex discovers hierarchical `AGENTS.md`. |
| `.claude/settings*.json` and `.vscode/settings.json` | Omitted | The source enables permission bypass; a package must not expand user authority. |
| `.claude/skills`, agents, rules, references, and hooks | Converted to package-native surfaces | Mapped separately in the component, agent, rule, and hook records. |
| `MEMORY.md` populated with upstream release lessons | Replaced by a clean template | Source history is evidence, not a new project's memory. |
| `validate-setup.sh` | Replaced by package and project validators | The original checks Claude availability and depends on Git Bash path behavior. |
| model/surface/skill integrity scripts | Replaced by `validate_package.py` | Their asserted surfaces and provider metadata no longer match MAW Codex. |
| stash-based `.githooks/pre-commit` | Native non-mutating rewrite | The new gate never stashes, pops, or alters a researcher's working tree. |
| `nightly-repro-check.sh` | Native Python rewrite | Cross-platform, no Claude/runtime dependency. |
| guide renderer, rendered HTML, and deploy workflow | Omitted | MAW Codex documentation is maintained directly; generated guide output is not runtime behavior. |
| `sync_to_docs.sh` | Routed through `$deploy` | Deployment layout and publication authority are project-specific. |

## Initializer safety

The initializer performs a complete collision preflight. It skips byte-identical
files, refuses differing targets, and writes nothing when any conflict exists.
Existing non-empty projects require `--merge`; this flag does not authorize
overwrites. Git initialization is separately opt-in with `--git-init`, and
Git hooks are never activated automatically.
