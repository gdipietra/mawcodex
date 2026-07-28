# `extract-tikz` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/extract-tikz/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `2ac1c8027bb4a1eb09746ebe7a7726d3020dcbae1ddef69f452172f15122c097`
- Target: `skills/extract-tikz/SKILL.md`
- Target SHA-256 after semantic review: `f9832da0b311aa4c86aebcc43eeb47bec928918d60943858eedd77cd82f69dd8`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced positional lecture arguments and provider-specific agent calls with
  validated path resolution and the portable TikZ reviewer role.
- Made TeX environment setup cross-shell and preserved PDF-page to zero-based
  SVG mapping without shell positional placeholders.
- Added rendered SVG inspection, local-sync boundary, and UNVERIFIED handling.

## Behavior preserved

Beamer source-of-truth freshness, prevention gate, standalone compilation,
page counting, SVG conversion, local docs sync, reviewer loop, and maximum
rounds remain.

## Behavior loss or limitations

The workflow does not deploy or publish. Full compile/convert/reviewer forward
testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS