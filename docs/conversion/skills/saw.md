# `saw` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/saw/SKILL.md`

## Intent

SAW creates sanitized, evidence-bounded project-return and upstream-learning
slices from recorded MAW project state.

## Design decisions

- Invocation and file export are explicit-only.
- Reliable configuration, manager history, instructions, and validation
  evidence control; private transcript internals are excluded.
- Every statement is observed, declared, or inferred, and unconfirmed
  inference is not promoted upstream.
- Project-return slices retain safe project-specific governance, while
  upstream-learning slices remove project identity and generalize candidate
  improvements.
- Absolute paths, secrets, data, student information, unpublished content,
  code bodies, and external-plugin settings are excluded.
- Teaching and Stata/R research projects have concrete, conservative
  sanitization examples.
- Approved exports use schema version 1 and remain inside `.maw/slices/`.

## Behavior loss or limitations

SAW is not telemetry and cannot reconstruct unrecorded usage. Missing manager
history remains unknown, and the skill omits items that cannot be supported
after sanitization.

- Validation: PASS with local structural inspection of frontmatter, naming,
  explicit-invocation metadata, and linked references.
- Forward testing: not yet performed.
