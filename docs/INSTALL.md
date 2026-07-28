# Install and use MAW Codex

MAW Codex has two layers:

1. the plugin supplies 58 reusable skills and optional lifecycle hooks;
2. the project initializer supplies a local academic layout, 19 project-scoped
   custom agents, portable role/rule references, and reusable templates.

Using both layers provides the closest Codex-native equivalent of the fixed
upstream workflow.

## 1. Validate the package

From `C:\Codex\mawcodex`:

```powershell
.\scripts\maw.cmd all
```

The release validator must pass before installing a development checkout as a
stable package. The wrapper uses Python from `PATH` when available and
otherwise locates the Python bundled with the Codex desktop runtime. It does
not install dependencies or change global settings.

## 2. Preview the local-marketplace installation

The supported local path uses Codex's canonical local marketplace catalog.
Preview the plugin and marketplace destinations:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd install
```

The preview writes nothing. It uses `~/plugins/mawcodex` for the plugin and
`~/.agents/plugins/marketplace.json` for the canonical local catalog. The
catalog entry `./plugins/mawcodex` therefore resolves to the exact copied
directory.

Apply the reviewed plan:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd install --apply
```

The installer copies the stable package into `~/plugins/mawcodex`, preserves
the existing catalog name, interface, and every marketplace entry, and adds
one canonical `mawcodex` entry. When no catalog exists, it creates one
displayed as **Personal**. It refuses an existing install unless `--update` is
explicit; update mode makes timestamped backups.

Restart Codex or begin a new task, open **Plugins**, select the local
marketplace name shown in the app (for example **Personal** or an existing
custom display name), and install or enable **MAW Codex**. Confirm that the 58
skills and bundled hooks are listed.

The hooks are non-managed local code. Codex requires a separate review and
trust decision for their exact definitions. The package works without trusted
hooks, but automatic git guardrails, claim-staleness notices, and compaction
continuity remain inactive.

Windows hooks use PowerShell. macOS and Linux hooks require Python 3; their
launcher checks `python3` and `python` and emits a visible inactive-guardrail
notice when neither is available.

## 3. Preview a new academic project

Choose an empty destination and preview every file:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd init C:\Codex\my-paper --dry-run
```

Review the printed plan. A preview never creates the destination.

## 4. Initialize the project

Create the academic workspace and a local Git repository:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd init C:\Codex\my-paper --git-init
```

The initializer performs a complete collision preflight, never overwrites a
differing file, and does not activate Git hooks. Use `--merge` only to add
missing files to an existing project after reviewing collisions.

Before importing research materials, edit the generated `AGENTS.md` to record:

- the controlling local source;
- the role of Drive, Dropbox, or other shared storage;
- the role of Overleaf and its local mirror;
- raw, derived, restricted, and publishable data locations;
- required estimation, rendering, and disclosure checks.

Then use `$jaw` for initial readiness, `$paw` for shared and personal settings,
and `$law` only when root or nested instruction layers need specialization.
Shared choices live in `.maw/profile.yaml`; `.maw/local.yaml` is ignored and
cannot weaken team requirements. The project-local `manageraw` agent may
coordinate these skills after its TOML and portable role have been reviewed.

## 5. Start work in the initialized project

Open `C:\Codex\my-paper` as the Codex workspace and begin a new task. Trust the
project configuration only after reviewing `.codex/config.toml` and the 19
files under `.codex/agents/`.

Invoke a workflow naturally or name its skill, for example:

```text
Use $interview-me to turn this idea into a research specification.
Use $did-event-study to plan the staggered-adoption analysis.
Use $review-paper for an adversarial manuscript review.
Use $replication-package to assemble a local deposit package.
```

The skills require separate authorization before commit, push, submission,
upload, email, publication, deployment, or external synchronization.

## 6. Track Pedro's updates

Check the source relationship without contacting GitHub:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd source-status
```

When network access is intended, fetch refs without merging:

```powershell
C:\Codex\mawcodex\scripts\maw.cmd source-status --fetch
```

Review and port deltas through `docs/UPSTREAM_SYNC.md`; never merge the
provider-specific source repository directly into MAW Codex.
