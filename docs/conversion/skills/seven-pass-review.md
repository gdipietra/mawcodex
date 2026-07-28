# `seven-pass-review` conversion

- Status: `validated`
- Classification: `composed replacement`
- Source: `.claude/skills/seven-pass-review/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d473dcb40f274edf5c2c7aa61a6849025b6cb0e29bd726d06511e21703c8a1b9`
- Target: `skills/seven-pass-review/SKILL.md`
- Target SHA-256: `8c0e4baeb9e7d74f419013e27ec73e2bf5d337e1be4ae325e0392616f3b51ab2`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Mapped seven forked reviews to bounded, blind Codex subagents and portable
  roles.
- Preserved typed fanout/reduce semantics and strengthened missing-report
  handling and synthesis traceability.
- Removed speculative token/runtime figures and made submission authority
  explicit.

## Behavior preserved

All seven lenses, parallel independence, typed scorecards, contradiction
surfacing, revision ordering, and the post-judge hallucination gate remain.

## Behavior loss or limitation

Actual parallelism depends on runtime capacity. A seven-agent forward run has
not yet been performed.
