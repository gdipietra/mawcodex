# `deploy` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/deploy/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `ed89f54692ba7541926621e756bb6638e8c08d235f7477c524391240649316b4`
- Target: `skills/deploy/SKILL.md`
- Target SHA-256 after semantic review: `decdfe4bc777aafa84c0aef592bf780e6f991c06662202259e707f04f5f7f78b`
- Mechanical changes: frontmatter normalization only

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced positional input and OS-specific browser commands with validated
  scope and browser-capability preview.
- Separated local render/sync, visual verification, commit, push, and live
  publication.
- A local `docs/` update can no longer be reported as deployment success.

## Behavior preserved

Quarto render, local publication-tree sync, widget/asset/TikZ checks, browser
preview, and deployment reporting remain.

## Behavior loss or limitations

The workflow pauses for separately required Git authorization. Live Pages
forward testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS