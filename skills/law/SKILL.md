---
name: law
description: "Layer an academic project's durable Codex instructions and configuration. Use to design, inspect, or safely revise root and nested `AGENTS.md`, project `.codex/config.toml`, team versus personal settings, subtree-specific rules, and the effective precedence seen from a target path. Use when PAW personalization must become executable project guidance."
---

# LAW - Layer Academic Workflow

Keep durable instructions minimal, correctly scoped, and explainable from any
working directory.

## Ownership boundary

LAW owns the design and maintenance of:

- root and nested `AGENTS.md`;
- project `.codex/config.toml` when the current Codex surface supports the
  intended setting;
- the `instruction_layers` section of `.maw/profile.yaml`;
- the mapping between shared project guidance and personal/global defaults;
- effective-precedence reports for a specific target path.

PAW owns other `.maw/profile.yaml` fields and `.maw/local.yaml`. LAW may update
only the shared `instruction_layers` registry needed to describe an approved
layer change; it must not edit other personalization fields.

## Default contract

- Begin read-only and show the proposed instruction graph before editing.
- Preserve all human-authored and non-MAW sections.
- Add a nested instruction file only when its subtree materially differs.
- Put reusable procedures in skills, project facts in the PAW profile, and
  only automatically applicable guidance in `AGENTS.md`.
- Do not copy personal global guidance into the repository.
- Never weaken higher-authority instructions, scientific safeguards, or
  release gates.
- Require approval for every instruction or configuration file changed.

Read
[`manageraw-profile.md`](../../references/manageraw-profile.md) before using
profile state to design instruction layers.

## 1. Inventory the instruction graph

For the project root and each relevant target path, inspect:

1. Root and intervening nested `AGENTS.md` files.
2. Existing project `.codex/config.toml`.
3. Applicable user/global guidance that is visible and authorized for
   inspection.
4. Relevant `.maw/profile.yaml` and `.maw/local.yaml` decisions.
5. Existing skills, hooks, CI, build documentation, and local conventions.

Do not assume the repository root is the working directory. Do not search
outside the authorized project or expose personal settings in a shared report.

## 2. Compute effective precedence

Use [`effective-precedence.md`](references/effective-precedence.md). Always
separate:

- higher-authority runtime instructions;
- the user's current request;
- project guidance from root toward the target path;
- project configuration;
- skill-specific workflow instructions;
- personal preferences that remain outside the repository.

Closer nested project guidance specializes its subtree; it does not grant
permission to contradict higher-authority instructions. When two applicable
instructions remain incompatible, report the exact conflict and request a
decision rather than selecting silently.

## 3. Design the smallest useful layer set

Use [`layering-patterns.md`](references/layering-patterns.md).

The root `AGENTS.md` should contain only project-wide invariants:

- mission and controlling sources;
- scientific, confidentiality, and provenance safeguards;
- repository map and raw/derived boundaries;
- standard verification and authorization gates.

A nested `AGENTS.md` should contain only subtree differences, such as:

- a course-specific LaTeX engine or output convention;
- an exams/solutions confidentiality rule;
- Stata-specific execution and log rules;
- R-specific environment, testing, or package rules;
- manuscript-specific citation and rendering expectations.

Avoid duplicated prose. State what the nested layer adds or narrows and rely on
the root for unchanged invariants.

Use project `.codex/config.toml` only for supported trusted-repository Codex
settings, not academic prose or secrets. Keep machine paths and personal
preferences outside tracked project configuration.

## 4. Propose an exact change plan

For each proposed file, report:

- scope and target subtree;
- content source: existing instruction, PAW profile, or explicit user choice;
- preserved sections;
- additions, removals, and collision handling;
- whether the file is shared or personal;
- target paths used to test effective precedence;
- rollback method.

If a requested rule belongs in a skill or the PAW profile instead, say so and
route it rather than forcing it into `AGENTS.md`.

## 5. Apply and verify after approval

After the user approves the exact plan:

1. Capture Git status and the original file contents.
2. Edit only the approved files.
3. Preserve human sections and clearly delimit any MAW-managed block.
4. Parse project configuration with an appropriate TOML parser.
5. Update only the approved `instruction_layers` records and run
   `scripts/manageraw-state.py validate` when available.
6. Recompute the effective instruction chain from representative target paths.
7. Confirm that teaching or research subtree rules do not leak into siblings.
8. Show the final diff and unresolved conflicts.

Local edits do not authorize commit, push, plugin installation, environment
changes, sync, publication, submission, or sending.

## Handoffs

- Use `$caw` when more than one plugin or skill claims a task.
- Use `$paw` when the underlying personalization or ownership profile changes.
- Use `$jaw` when the project has not completed deployment readiness.
- Use `$uaw` when a new MAW base changes instruction requirements.
