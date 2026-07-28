# Academic research project

This project was initialized from the MAW Codex academic workflow. It combines
a reproducible analysis skeleton, Beamer and Quarto teaching surfaces, durable
research records, and Codex project instructions.

## Start here

1. Run `$jaw` to confirm whether this is a teaching, research, or mixed
   project and to test the capabilities the project will actually use.
2. Use `$paw` to record team settings in `.maw/profile.yaml`.
3. Use `$law` only when root or nested `AGENTS.md` files need specialization.
4. Replace this README's project title and research question or teaching goal.
5. Record local, raw-data, Drive, and Overleaf source roles in
   `.maw/profile.yaml` and the applicable `AGENTS.md`.
6. Put immutable inputs under `data/raw/` or document the secure external
   location when data cannot be copied here.
7. Replace the demonstration data generator in `scripts/R/01_load.R`.
8. Run `scripts/R/00_run_all.R`, inspect all outputs, and capture the
   environment.
9. Create a requirements specification or plan in `quality_reports/` before
   substantial work.

## Main folders

- `scripts/R/`: numbered reproducible analysis pipeline.
- `data/`: raw and derived data roles.
- `Figures/`: figures and diagram sources.
- `Slides/`: Beamer sources.
- `Quarto/`: RevealJS sources and shared theme.
- `Preambles/`: shared LaTeX setup.
- `templates/`: plans, passports, decisions, and other reusable records.
- `quality_reports/`: durable project governance and verification evidence.
- `explorations/`: provisional analyses isolated from production work.
- `.maw/`: tracked workflow profile, version lock, revision history, and
  sanitized reusable slices; personal settings stay in ignored
  `.maw/local.yaml`.

## Checks

Run:

```powershell
python scripts/validate-project.py
```

On systems where `python` is not the launcher, use the available Python 3
executable. The validator is standard-library only.

Inspect only the MAW control-plane state with:

```powershell
python scripts/manageraw-state.py status --json
```

Git hooks are optional and never installed silently. Preview the local change:

```powershell
python scripts/install_git_hooks.py
```

Then apply it explicitly:

```powershell
python scripts/install_git_hooks.py --apply
```

## MAW Codex

Invoke a workflow with `$skill-name`, for example `$data-analysis`,
`$review-paper`, `$audit-reproducibility`, or `$coauthor-brief`. Read the
project's `AGENTS.md` and `.maw/profile.yaml` before relying on any default.
