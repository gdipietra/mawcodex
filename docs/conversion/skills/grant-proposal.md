# `grant-proposal` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/grant-proposal/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `e5acf6034c047b79409210bead3035b72929e7ad22e3abfa0976d91a4e9c6f07`
- Target: `skills/grant-proposal/SKILL.md`
- Target SHA-256: `dded93032121f691b0d6ef684eec0ccb0a9f156a29fd6fa907c08fc0865f5b24`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced slash commands and Claude task dispatch with sibling Codex skills,
  bounded subagents, and a portable verifier-role fallback.
- Added primary-source checks for current sponsor requirements and explicit
  `UNVERIFIED` handling.
- Strengthened confidentiality, coherence, provenance, and external-submission
  boundaries.

## Behavior preserved

The research-spec prerequisite, funder-shaped scaffold, specialist DMP and
environment composition, coherence pass, checklist, and local draft outputs
remain.

## Behavior differences and loss

Sponsor portals and requirements are not hard-coded as current, and no
submission action is performed. Claude-specific delegation is replaced by
Codex-native composition; environment-dependent delegate execution remains to
be forward-tested.
