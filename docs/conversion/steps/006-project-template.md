# Step 006 — Package the academic project template

## Revision

Imported 18 portable source assets through the deterministic
`scripts/migrate_project_template.py` conversion and retained all 21 reusable
artifact templates from the shared-resource conversion. Added a native
academic project scaffold, cross-platform validation, safe local Git checks,
and `scripts/init_project.py`.

## Semantic changes

- Replaced Claude command syntax and rule paths with Codex-native skill
  invocation and package references.
- Replaced inherited upstream memory with an empty evidence-oriented project
  memory.
- Replaced provider permission settings with no project-level permission
  expansion.
- Reimplemented the pre-commit gate without stash/pop mutations.
- Moved the source DiD validation report into conversion evidence so a new
  project cannot mistake it for its own result.
- Added explicit applied-micro research-design safeguards and external-sync
  boundaries to the generated `AGENTS.md`.

## Verification

`tests/test_init_project.py` verifies:

1. dry-run creates nothing;
2. a full initialization includes 18 agents, rules, templates, and passes the
   generated project's validator;
3. a merge conflict aborts before any partial write;
4. a missing Git runtime is detected before any file is created when
   `--git-init` is requested.

All four scenarios pass with the bundled Python runtime.

## Result

The package now preserves the original repository's usable academic-project
setting in addition to its skills, agents, rules, and hooks. Provider-specific
configuration and generated documentation are explicitly mapped rather than
silently copied.
