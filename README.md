# MAW Codex

> **Verified publication checkpoint:** https://gdipietra.github.io/mawcodex/ from https://github.com/gdipietra/mawcodex. Commit `cc82cede0eed6b721f23cc82862e0ad189db2824` is the verified publication/content checkpoint: stable-gates run `32666609822` and GitHub Pages run `32666609835` succeeded, the public endpoint returned HTTP 200, and the repository homepage metadata uses the canonical Pages URL. Later commits require separate same-SHA verification.

MAW Codex is a Codex-native academic-workflow package derived from
[pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow).
It preserves the original plan-implement-verify discipline, adversarial review
patterns, reproducibility safeguards, and academic teaching workflows while
rebuilding their execution surfaces for Codex.

## Current status

Version `1.2.2` is the current stable package. Its local evidence, historical
deployed snapshot, known limitations, and controlled public-sharing boundary
are documented explicitly. The verified inventory is:

- 58 packaged skills: 52 source-derived workflows plus the Codex-native JAW,
  CAW, PAW, LAW, UAW, and SAW management capabilities;
- 19 project-scoped custom agents plus portable role definitions, including
  the native `manageraw` control-plane agent;
- 32 adapted research and quality rules;
- 13 mapped provider runtime surfaces, including all 7 hook sources;
- Codex-native, opt-in lifecycle hooks;
- reusable academic templates and deterministic validation.

The purple MAW icon, academic pet, and plugin thumbnail in `assets/brand/`
form the package's original visual identity.

The public website content at verified publication checkpoint
`cc82cede0eed6b721f23cc82862e0ad189db2824` is live on
[GitHub Pages](https://gdipietra.github.io/mawcodex/). It gives Pedro H. C.
Sant'Anna prominent credit, separates the 52 source-derived workflows from
MAW Codex's native control-plane work, and exposes a capability-by-capability
provenance ledger. For that checkpoint, stable-gates run `32666609822` and
GitHub Pages run `32666609835` succeeded, the public endpoint returned HTTP
200, and the repository homepage metadata is canonical. Later commits require
separate same-SHA verification.

The stable claim, local and remote evidence, environment-dependent limitations,
and public-sharing sequence are recorded in the
[stability matrix](docs/conversion/STABILITY.md),
[release report](docs/conversion/RELEASE_REPORT.md),
[known limitations](docs/conversion/KNOWN_LIMITATIONS.md), and
[public-release readiness statement](docs/conversion/PUBLIC_RELEASE_READINESS-1.2.2.md).

## Repository roles

`C:\GitHub\claude-code-my-workflow` is the tracked source fork. Its `origin`
points to Giovanni's fork and its `upstream` points to Pedro's repository.
`C:\Codex\mawcodex` is the independent Codex-native implementation.

The source clone is never edited during conversion. This separation makes
upstream changes easy to fetch, compare, and selectively port.

## Architecture

- `skills/` contains installable Codex skills.
- `.codex/agents/` contains local custom-agent optimizations.
- `references/agent-roles/` keeps agent behavior portable when custom agents
  are not installed.
- `references/rules/` contains the adapted academic governance rules.
- `hooks/` contains optional hooks that Codex runs only after user trust.
- `assets/templates/` contains reusable project artifacts.
- `assets/project-template/` contains the installable academic-project
  skeleton: R pipeline, Beamer/Quarto surfaces, governance folders, and
  non-mutating local checks.
- `docs/*.html` and `docs/assets/` contain the public GitHub Pages site.
- `docs/conversion/` contains the auditable conversion record.

ManageRAW keeps shared project decisions in tracked `.maw/profile.yaml`,
personal non-weakening choices in ignored `.maw/local.yaml`, and actual Codex
instruction authority in root and nested `AGENTS.md`.

For an ongoing project, begin with `$mawcodex:jaw`. After readiness is
established, use `$mawcodex:caw` for plugin ownership, `$mawcodex:paw` for
project settings, and `$mawcodex:law` for root or nested instructions.
`$mawcodex:uaw` and `$mawcodex:saw` are explicit-only maintenance
operations. The `manageraw` project agent coordinates these capabilities when
the full or selected agent configuration is installed.

## Initialize an academic project

Preview and install the package through the canonical local marketplace:

```powershell
.\scripts\maw.cmd install
.\scripts\maw.cmd install --apply
```

Known Windows `1.2.2` issue: if `maw.cmd` selects the non-runnable
WindowsApps `python.exe` alias, use the bundled runtime explicitly:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" `
  .\scripts\install_local_plugin.py --apply
```

Restart Codex, enable MAW Codex from the local marketplace shown in the app,
then use the initializer for each research project. See the [installation guide](docs/INSTALL.md) for
the complete workflow, including hook trust and source-role setup.

For the public-repository and GitHub Pages release sequence, see the
[publishing guide](docs/PUBLISHING.md). Preparing these files does not authorize a commit, push,
tag, GitHub release, marketplace submission, or Pages deployment.

Preview the complete file plan:

```powershell
.\scripts\maw.cmd init C:\Codex\my-paper --dry-run
```

Then initialize the project and its local Git repository:

```powershell
.\scripts\maw.cmd init C:\Codex\my-paper --git-init
```

The initializer includes all 19 project custom agents, portable rules and
roles, and the 21 artifact templates by default. It never overwrites a
differing file. Use `--merge` only to add missing files to an existing
project; conflicts abort before any write.

## Development validation

Run the bundled Python validator:

```powershell
.\scripts\maw.cmd all
```

The command validates the exact source-fork contract, runs Codex's official
plugin and skill validators, executes the behavioral tests, records the
evidence, and checks manifest structure, custom-agent TOML, references,
provenance, links, and provider-specific residue.

## Upstream updates

See the [upstream synchronization guide](docs/UPSTREAM_SYNC.md). The short form is: fetch `upstream` in the source
fork, compare the recorded baseline with the new tag or commit, update the
component inventory, and port only reviewed deltas into this repository.

The safe local check is:

```powershell
.\scripts\maw.cmd source-status
```

Add `--fetch` only when you intend to contact GitHub. It updates remote refs
but never merges them or changes the fixed source checkout.

## License and attribution

MAW Codex is distributed under the MIT License. Substantial portions are
adapted from Pedro H. C. Sant'Anna's MIT-licensed workflow. See `NOTICE.md` and
the per-component conversion records for upstream and third-party attribution.
