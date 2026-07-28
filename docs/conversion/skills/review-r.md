# `review-r` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/review-r/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `73d1081a77ce63a66415ff3fb6214c930a6f23fb1b9878f9d4a289e64c43270f`
- Target: `skills/review-r/SKILL.md`
- Target SHA-256: `b3b5324f4117907dfa767f97cab94f82637ed57b22d5d9ad866625433331da4e`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced argument placeholders and agent invocation syntax with explicit
  scope resolution and a portable `r-reviewer` fallback.
- Expanded research-design, data-lineage, inference, and confidentiality checks.
- Made static-review status and no-edit behavior explicit.

## Behavior preserved

The skill remains a read-only, per-script R review with severity-ranked reports
and a batch summary.

## Behavior loss or limitation

It deliberately does not run R; numeric verification still requires
`$audit-reproducibility`. Representative review output is pending.
