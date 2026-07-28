# `interview-me` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/interview-me/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `bd561e04046801c5f4bd131a47e1586af24ad98933e864996c36c81975aa83d5`
- Target: `skills/interview-me/SKILL.md`
- Target SHA-256: `9bd4d5b8da0229883a06bd0813c48231e49de85e48c9ae15cfb1bf506f8e7530`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: PASS (FT-01)
## Material revisions

- Replaced positional arguments and Claude question tooling with a direct,
  multi-turn Codex conversation.
- Added estimand, inference, confidentiality, expectation-versus-result, and
  outcome-access safeguards.
- Ported citation verification to an isolated claim-verifier role and kept
  explicit decision records for live alternatives.

## Behavior preserved

The staged interview, gentle probing, paper-type field, structured research
specification, and decision-record intent remain.

## Behavior differences and loss

No Claude interaction widget is assumed. Literature claims remain
`UNVERIFIED` unless the independent check runs.
