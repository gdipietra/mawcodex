# `new-diagram` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/new-diagram/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `b3b169137f9ead11ed13ada130d2f101e4001f963d7ec39d69c932fdcd5b7292`
- Target: `skills/new-diagram/SKILL.md`
- Target SHA-256: `5ab4cf8663c904cf4f72fa3687cb83ec70011bea86d5207f0013982cd6840126`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Redirected the snippet gallery to packaged assets and replaced positional
  arguments with semantic inputs.
- Ported the reviewer to a custom-agent or portable-role path with isolated
  visual evidence.
- Added overwrite confirmation, bounded rounds, exact-artifact cleanup, and
  `UNVERIFIED` behavior for missing checker, compiler, renderer, or converter.

## Behavior preserved

Snippet-first authoring, TikZ prevention rules, standalone compilation,
independent review, revision looping, and optional SVG output remain.

## Behavior differences and loss

Shell-specific editing and broad cleanup commands were removed. Deterministic
checker execution and render behavior still require a representative forward
test.
