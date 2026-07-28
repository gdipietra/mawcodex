# `uaw` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/uaw/SKILL.md`

## Intent

UAW reconciles a user-requested MAW update with an academic project's existing
personalization and external-capability ownership.

## Design decisions

- Invocation is explicit-only; UAW never polls for releases.
- Updates use a three-way comparison of the old MAW base, project overlay, and
  candidate MAW base.
- Update discovery, planning, applying, installation, and external actions are
  separate authorization boundaries.
- Other plugins and their recorded responsibilities remain intact.
- The project lock advances only after the approved reconciliation passes all
  required validation.
- Successful reconciliations receive an explicit history record before the
  new lock is reported as current.
- LaTeX teaching and mixed Stata/R research projects receive distinct impact
  checks without being reorganized incidentally.

## Behavior loss or limitations

UAW depends on a reliable old-base identity and recorded project overlay. When
those are missing, it reports the reconciliation as UNVERIFIED rather than
guessing at historical behavior.

- Validation: PASS with local structural inspection of frontmatter, naming,
  explicit-invocation metadata, and linked references.
- Forward testing: not yet performed.
