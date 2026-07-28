---
name: uaw
description: "Reconcile a user-requested MAW Codex update with an academic project's existing personalization. Use only when the user explicitly asks to check, compare, plan, or apply a MAW update while preserving project overlays, instruction hierarchy, external-plugin ownership, and reproducible project behavior."
---

# UAW - Update Academic Workflow

Update MAW deliberately. Treat an update as a three-way reconciliation, not
as a replacement of the project's effective workflow.

## Safety contract

- Act only after an explicit `$uaw` request. Never poll for updates, schedule
  checks, or initiate a fetch because an update may exist.
- Begin read-only. Checking, planning, applying, installing, committing, and
  publishing are separate actions.
- Never install or update MAW automatically. Show the candidate version,
  affected surfaces, exact changes, validation plan, and rollback before
  requesting approval to apply.
- Preserve other plugins, their configuration, and the capability ownership
  recorded by the project. Do not copy their internals into MAW.
- Preserve dirty worktrees, non-MAW content, raw data, protected teaching
  material, and user-authored instruction sections.
- Report unavailable bases, skipped checks, and missing runtimes as
  UNVERIFIED, never PASS.

Read
[`manageraw-profile.md`](../../references/manageraw-profile.md) before
interpreting or changing project-local MAW state.

## 1. Read the effective project state

Resolve the project root and applicable instructions. Read, when present:

- `.maw/lock.json` for the installed or adopted MAW base;
- `.maw/profile.yaml` for shared personalization and capability ownership;
- the personal/local overlay defined by the project;
- `.maw/history/` for approved JAW, PAW, LAW, and prior UAW decisions;
- root and nested `AGENTS.md` files;
- project-local skills, hooks, build configuration, and plugin declarations.

Do not invent missing state. If the current base cannot be identified
reliably, stop short of an apply plan and describe how to establish or
reconstruct the baseline.

## 2. Obtain update information only as requested

Use already available local release metadata when that answers the request.
Fetch or inspect a remote release only when the user's request includes an
update check or identifies a candidate release. Record the release source,
version, and immutable identifier when available.

Do not mutate the installed plugin, local package cache, project, or lock while
checking.

## 3. Perform the three-way reconciliation

Define:

- **B0:** the old MAW base recorded for this project;
- **O:** the project overlay created through JAW, PAW, LAW, and approved local
  decisions;
- **B1:** the candidate new MAW base.

Read [`reconciliation.md`](references/reconciliation.md) and compare
`B0 -> B1` against `O`. For every affected component, distinguish:

1. unchanged project behavior that can adopt B1 directly;
2. a disjoint overlay that can be reapplied cleanly;
3. a behavioral or textual conflict requiring a user decision;
4. a rename, removal, schema change, or new dependency;
5. overlap with another plugin or project-local capability.

Never infer that MAW may delete or subordinate another plugin merely because
the new base provides a similar skill. Preserve the ownership registry and
route unresolved overlaps through the project's coordination policy.

## 4. Evaluate project impact

Inspect only the capabilities the project actually uses or governs.

- For a LaTeX-heavy teaching project, check engines, bibliography, preambles,
  nested course instructions, language conventions, generated-output paths,
  exercise/solution separation, and representative documents.
- For a research project with Stata and R, check entry points, environment
  assumptions, raw/derived data boundaries, seeds, outputs, manuscript links,
  and any project-specific routing around incomplete or exploratory code.

Do not use an update to reorganize an untidy project unless the user separately
approves that migration.

## 5. Present the update decision

Return:

- B0 and B1 identities and evidence;
- the overlay and instruction scopes consulted;
- an affected-component matrix;
- preserved external-plugin ownership;
- automatic, manual, conflicting, and UNVERIFIED changes;
- the exact proposed file operations;
- representative validation and rollback;
- a verdict: SAFE TO APPLY, NEEDS DECISIONS, NOT APPLICABLE, or UNVERIFIED.

Keep the report in conversation unless the user authorizes a project record.

## 6. Apply only the approved reconciliation

After explicit approval:

1. Capture pre-change Git status and the current lock without modifying either.
2. Apply the smallest approved B1 changes.
3. Reapply only the compatible parts of O.
4. Preserve human-authored and external-plugin sections.
5. Validate structure and each affected representative workflow.
6. Record the approved reconciliation under
   `.maw/history/YYYY-MM-DD_uaw_<old>-to-<new>.md`.
7. Show the resulting diff and unresolved checks.

Do not commit, push, publish, sync, or send as part of an update unless each
action is separately authorized.

## 7. Advance the lock only after success

Update `.maw/lock.json` only after the approved changes are present and every
required validation has passed. Record the adopted B1 identity, ISO update
date, and validation evidence using the ManageRAW profile contract.

If an apply or required check fails, leave the prior lock unchanged, report
the partial state, and either roll back the approved changes or present a
recovery plan. Never label a partially reconciled project as updated.
