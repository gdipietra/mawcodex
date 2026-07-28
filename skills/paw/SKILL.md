---
name: paw
description: "Personalize MAW for an academic project by maintaining its shared `.maw/profile.yaml` and personal `.maw/local.yaml` overlays. Use to record project type, source roles, active MAW capabilities, build targets, protected paths, terminology, capability ownership across external plugins, or durable preferences after JAW adoption. Delegate AGENTS.md and Codex configuration layering to LAW."
---

# PAW - Personalize Academic Workflow

Maintain the project's MAW overlay without forking or rewriting the packaged
MAW base.

## Ownership boundary

PAW owns:

- `.maw/profile.yaml`: tracked team/project personalization;
- `.maw/local.yaml`: personal or machine-specific personalization, normally
  gitignored;
- durable capability ownership, including external plugin names,
  responsibilities, and conflict rules;
- the project's active MAW capability set, terminology, source roles, build
  targets, protected paths, and validation expectations.

PAW does not own:

- root or nested `AGENTS.md`;
- `.codex/config.toml` or global Codex configuration;
- the `instruction_layers` registry inside the shared profile;
- plugin internals or another plugin's settings;
- MAW installation, version updates, or portable exports.

Send instruction and configuration layering to `$law`, version reconciliation
to `$uaw`, and exportable usage slices to `$saw`.

## Default contract

- Inspect and propose before writing.
- Preserve unknown fields and human-authored notes.
- Never store credentials, tokens, personal data, restricted data, student
  records, unpublished results, or another plugin's internal configuration.
- Keep the packaged MAW base immutable; record only project differences.
- Require approval for the exact profile diff.
- Do not commit, push, sync, publish, or install.

Read
[`manageraw-profile.md`](../../references/manageraw-profile.md) before
interpreting or changing project-local MAW state.

## 1. Establish current state

Read, when available:

1. The JAW readiness decision and adopted integration shape.
2. Existing `.maw/profile.yaml` and `.maw/local.yaml`.
3. Applicable project instructions and build documentation.
4. Git status and ignore rules for `.maw/local.yaml`.
5. Relevant CAW ownership contracts.

Classify the project as research, teaching, or mixed from evidence. Load
[`use-case-overlays.md`](references/use-case-overlays.md) for the matching
profile prompts.

If no profile exists, propose the smallest valid initial profile. Do not infer
remote source authority, data sensitivity, solution-key policy, or publication
authority from folder names.

## 2. Separate shared and personal settings

Write to the shared profile only when a collaborator should inherit the
setting. Examples include:

- controlling source and mirror roles;
- standard build targets and expected artifacts;
- shared terminology and language;
- protected or immutable paths;
- active project skills and ownership contracts;
- reproducibility and review requirements.

Write to the local overlay only when the setting belongs to one user or
machine. Examples include:

- executable paths and local runtime locations;
- preferred personal helper plugin;
- local cache or scratch directories;
- non-secret UI or workflow preferences.

If `.maw/local.yaml` is not ignored, propose the ignore change and hand its
instruction implications to `$law`. Never place a secret in the file merely
because it is ignored.

## 3. Maintain the profile

Use [`profile-schema.md`](references/profile-schema.md). For every change:

1. Preserve the current `maw.base_version`; UAW owns version changes.
2. Update only fields supported by project evidence or an explicit user
   decision.
3. Give each capability one owner and one supported priority.
4. Record external capabilities by public name and responsibility only.
5. Keep one-off conflicts in the CAW contract unless the user approves a
   durable ownership change.
6. Record material ownership, adoption, source-role, or protection changes
   under `.maw/history/YYYY-MM-DD_paw_<intent>.md`.
7. Validate the JSON-compatible YAML and check referenced paths without
   creating them.

When CAW found a one-off routing choice, promote it only if the user wants that
choice to recur.

## 4. Propose, apply, and verify

Before writing, show:

- target file;
- exact fields added, changed, or removed;
- team versus personal classification;
- expected effects;
- any LAW follow-up;
- rollback method.

After approval, apply the smallest diff, parse both YAML files, show the
resulting effective overlay, and report unresolved fields as `UNVERIFIED`.
Preserve the pre-change version in Git or a user-approved backup.

## Use-case emphasis

- **Existing LaTeX teaching tree:** preserve the tree; map course roots,
  engines, bibliographies, PT-BR terminology, deliverables, and the separation
  of public material from exams or solutions.
- **Unorganized Stata/R research project:** mark raw data immutable; inventory
  entry points without pretending an execution order exists; separate derived
  data and outputs; record Stata/R environments, manuscript authority,
  sensitivity, estimands, and verification gaps.
