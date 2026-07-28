# `coauthor-brief` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/coauthor-brief/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `03b54c7573be019b75f6523b77f2bce96c979c6dd184deeca817c60b1c1bac35`
- Target: `skills/coauthor-brief/SKILL.md`
- Target SHA-256 after semantic review: `8cf45022d87f3d42f832ca58ee0fe0267e409d344c63842385f8ea91ac066506`
- Mechanical changes: rule path, skill invocation syntax, state path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Repaired rule and skill links and converted invocations to Codex syntax.
- Tightened replication-ready semantics and restricted-data redaction.
- Separated local brief creation from commit, push, PR, merge, or sending.

## Behavior preserved

Git delta, artifact status, environment restore, open decisions,
restricted-access process, and collaborator-oriented output remain.

## Behavior loss or limitations

The skill will not send or publish the brief. A cross-machine handoff forward
test is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS