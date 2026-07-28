# `compile-latex` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/compile-latex/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `6784e39c6cfe37363b4e2c90818d6fad83307e2b70348d5624eef28048f979ff`
- Target: `skills/compile-latex/SKILL.md`
- Target SHA-256 after semantic review: `1011f06123f949199022f84adf8440afa5939d20d2e9d4341e2e80b95a5489bb`
- Mechanical changes: frontmatter normalization only

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced the positional basename and OS-specific open command with validated
  path resolution and visual PDF inspection.
- Preserved XeLaTeX default while honoring an authoritative project engine and
  bibliography backend.
- Missing compile or render capabilities now produce UNVERIFIED.

## Behavior preserved

Multi-pass citation/reference resolution, preamble search paths, warning scan,
page count, and PDF reporting remain.

## Behavior loss or limitations

The skill no longer assumes BibTeX or a particular desktop open command.
Compilation and visual forward testing are pending.

- Validation: PASS
- Forward test: PASS (FT-12)