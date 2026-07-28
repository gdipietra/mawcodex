# `permission-check` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/permission-check/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `b9c3821d9690483a6b6af4d6e79cc31b828123cae1ec0ede394e74a6bfd46edd`
- Target: `skills/permission-check/SKILL.md`
- Target SHA-256: `612bbf938af3e0a384743702d1e3913929352a7c3692ec052e88dc9f8ccdbd2f`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Reimplemented the diagnostic around current Codex permission profiles,
  legacy sandbox settings, approval policy, reviewer, workspace roots,
  execution rules, trust, app/MCP gates, and managed requirements.
- Added current configuration precedence and mixed-family detection.
- Preserved the repo-local-first privacy boundary and host-global consent and
  redaction protocol.

## Behavior preserved

The skill remains a read-only explanation of why prompts occur, with
layer-by-layer evidence and safe next checks.

## Behavior differences and loss

The source's Claude six-tier settings model, environment variables, statusline,
and bypass semantics are intentionally unsupported. Exact beta permission
profile behavior requires current-client verification.
