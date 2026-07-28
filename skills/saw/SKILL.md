---
name: saw
description: "Export sanitized, evidence-bounded records of a project's personalized MAW Codex usage. Use only when the user explicitly asks to slice, snapshot, digest, or export MAW project state for returning to the project later or proposing generalized improvements to the main MAW package."
---

# SAW - Slice Academic Workflow

Create a portable digest of recorded MAW usage without exporting the project
itself. Produce two deliberately different views:

- a **project-return slice** for understanding this project's effective MAW
  setup later;
- an **upstream-learning slice** containing generalized candidates that may
  improve a future MAW release.

## Safety contract

- Act only after an explicit `$saw` request. Never export in the background.
- Begin read-only and preview the proposed slice before writing files.
- Use reliable project state and manager history. Never parse private
  transcript internals, hidden assistant state, application caches, memories,
  or conversation databases to reconstruct usage.
- Never include credentials, secrets, data, student information, restricted
  metadata, unpublished content, estimates, solution keys, remote URLs,
  usernames, machine identifiers, or absolute paths.
- Do not copy another plugin's settings. Export only its name, assigned
  capability role, and an approved conflict decision when those are already
  recorded in the MAW profile.
- Treat absent records as unknown. Do not claim complete usage telemetry.

Read
[`manageraw-profile.md`](../../references/manageraw-profile.md) before
interpreting project-local state or proposing an export.

## 1. Establish the evidence boundary

Resolve the project root and applicable instructions. Prefer:

1. `.maw/profile.yaml` and the project's defined personal layer;
2. `.maw/lock.json`;
3. approved entries in `.maw/history/`;
4. root and nested `AGENTS.md`;
5. project-local configuration, build files, Git state, and validation
   evidence needed to confirm a recorded behavior.

Label every exported statement:

- **observed:** directly supported by current project artifacts;
- **declared:** explicitly recorded as a user or team decision;
- **inferred:** a tentative pattern derived from artifacts.

Do not promote an inferred item into upstream learning unless the user confirms
it or independent recorded evidence supports it.

## 2. Sanitize before composing

Read [`slice-schema.md`](references/slice-schema.md). Replace locations with
project-root-relative logical paths or role labels. Remove absolute path
prefixes, remote addresses, identities, data values, manuscript text, code
content, and secrets from commands or configuration.

For a LaTeX teaching project, retain configuration facts such as engine,
language, preamble ownership, instruction scopes, artifact roles, and
exercise/solution separation. Exclude lecture content, assessments, solutions,
student records, and copyrighted source material.

For a Stata/R research project, retain workflow facts such as runtime mix,
entry-point status, raw/derived boundaries, validation gaps, and useful MAW
personalizations. Exclude datasets, variable values, estimates, unpublished
claims, licensed metadata, and code bodies.

If safe sanitization would remove the evidence required to support an item,
omit the item and record the omission category.

## 3. Build the project-return slice

Capture only what is needed to resume MAW governance:

- MAW base identity and project classification;
- shared versus personal layer roles without private values;
- effective root and nested instruction scopes;
- enabled, preferred, replaced, or intentionally unused MAW capabilities;
- capability ownership for other plugins;
- source-of-truth and protected-artifact roles;
- safe build and validation summaries;
- recorded JAW, PAW, LAW, and UAW decisions;
- unresolved conflicts, UNVERIFIED checks, and next review trigger.

Preserve project-specific detail only when it is safe and useful for returning
to this same project.

## 4. Build the upstream-learning slice

Generalize away the project identity. For each candidate record:

- the intent and recurring problem pattern;
- affected MAW surface;
- the generalized behavior or safeguard proposed;
- evidence class and number of independent recorded occurrences;
- applicability to teaching, research, or both;
- confidentiality and migration risks;
- candidate status: observe, evaluate, propose, or reject.

Do not treat one local preference as a package-wide requirement. Separate
personal taste from a reproducibility, safety, routing, or usability lesson.
SAW proposes candidates; it does not edit the main MAW package.

## 5. Preview and write only with authorization

Show:

- evidence sources by safe relative role;
- excluded information categories;
- both slice contents;
- inferred or unresolved items;
- proposed output locations.

Write only after approval under `.maw/slices/`, using
`YYYY-MM-DD_project-return.json` and
`YYYY-MM-DD_upstream-learning.json` unless an existing project convention
requires a collision-safe suffix. Use relative links and the schema-versioned
machine-readable fields. Never write outside the target project's authorized
scope.

Writing a slice does not authorize committing, pushing, transferring it to the
main MAW repository, opening an issue, or publishing it. Those remain separate
actions.
