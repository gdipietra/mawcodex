# UAW three-way reconciliation

Use this reference after identifying the old base, project overlay, and
candidate base.

## Required inputs

| Symbol | Meaning | Minimum evidence |
| --- | --- | --- |
| B0 | Previous MAW base | Version plus immutable hash, manifest digest, or equivalent lock evidence |
| O | Project overlay | Shared profile, personal layer, instruction scopes, ownership decisions, and approved history |
| B1 | Candidate MAW base | Version plus immutable release or source identity |

If B0 is absent or ambiguous, do not simulate a precise three-way merge.
Classify the update as UNVERIFIED and propose baseline reconstruction.

## Component decisions

| B0 to B1 | Overlay relationship | Default decision |
| --- | --- | --- |
| No relevant change | Any compatible overlay | Retain effective project behavior |
| Base change, no overlay | None | Adopt B1 after validation |
| Base change, disjoint overlay | Compatible | Adopt B1 and reapply O |
| Base change touches overlay | Conflict | Require a user decision |
| Rename or removal | Overlay refers to old surface | Map explicitly or retain the old behavior temporarily |
| New dependency | Project uses affected surface | Forward-test before adoption |
| Capability overlaps another plugin | Ownership already recorded | Preserve ownership; do not replace the plugin |

Compare behavior, not merely filenames. A clean textual merge can still change
scientific, teaching, authorization, or routing semantics.

## Impact lenses

### Existing LaTeX teaching material

- Preserve the actual engine, preamble, theme, bibliography, and PT-BR or
  bilingual conventions.
- Check root and course-level instructions separately.
- Keep exams, solutions, student information, and publication targets within
  their existing protection boundaries.
- Compile representative source documents outside the source directories and
  inspect rendered output when layout can change.

### Existing Stata and R research material

- Preserve raw data and current analysis entry points, even when organization
  is incomplete.
- Check Stata ado dependencies, R package/environment assumptions, seeds,
  relative paths, and generated-output roles.
- Treat exploratory scripts and idea sketches as evidence of ongoing work, not
  as a reproducible pipeline unless the project records that status.
- Re-run only approved representative analyses; never reorganize or overwrite
  data as an incidental update.

## Reconciliation report fields

For each affected component record:

- component and active project use;
- B0 behavior;
- B1 behavior;
- overlay behavior and scope;
- external owner, if any;
- decision: adopt, reapply, retain, map, ask, or skip;
- exact proposed change;
- validation and rollback;
- status: PASS, FAIL, or UNVERIFIED.

An update is complete only when all required component decisions are resolved,
the approved changes validate, and the project lock advances last.

