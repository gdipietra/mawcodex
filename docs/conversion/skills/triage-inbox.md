# `triage-inbox` conversion

- Status: `forward-tested`
- Classification: `composed replacement`
- Source: `.claude/skills/triage-inbox/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `2f89cc3d3dffa8933d70620f9681b3ec23f5fabca94622198cbc823c48fdcd7b`
- Target: `skills/triage-inbox/SKILL.md`
- Target SHA-256: `3c756763e0a1db58f836ce9472cedb75787583f1ff82822ada9819a8a6535710`
- Validation: `PASS`
- Forward test: PASS (FT-09)
## Material revisions

- Replaced generic MCP language with purpose-built connected Gmail and Calendar
  capabilities and read-only probes.
- Tightened drafts, labels, archives, invites, and events to explicit
  post-preview authorization.
- Added data-minimization, tracker evidence, dry-run semantics, and graceful
  UNVERIFIED scheduled runs.

## Behavior preserved

Academic buckets, one proposed action per thread, referee-load cap, digest,
tracker, calendar conflict awareness, and no-auto-send boundary remain.

## Behavior loss or limitation

This port does not stage drafts during ordinary triage without a separate
explicit request. Live connector forward testing remains pending.
