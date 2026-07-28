# `promote-memory` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/promote-memory/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `24fe98d78b80ee30784c5690e3600bb3501e9919363d847d7106692b93792a6a`
- Target: `skills/promote-memory/SKILL.md`
- Target SHA-256: `10aa758ef6b1f1e6bbfe345a42fb642d0363fd4b5664f3240d304de55904c14b`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Preserved attribution for the five-critic council and converted each critic
  to an independent Codex subagent or portable-role lens.
- Removed provider model tiers and added active-environment memory-governance,
  confidentiality, evidence, and user-approval gates.
- Distinguished proposed from confirmed memory changes and retained an audit
  record.

## Behavior preserved

Generality, staleness, redundancy, evidence, and format votes; majority
recommendations; and the final human promotion decision remain.

## Behavior differences and loss

Direct memory edits may be replaced by the host's required update-note
mechanism. No scheduled loop or provider model alias is assumed.
