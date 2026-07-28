# `commit` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/commit/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `a342f2ccf5fcd932615074119d6dbb507fb9ae8cd8df2bf6fc2b24c0b9c10419`
- Target: `skills/commit/SKILL.md`
- Target SHA-256 after semantic review: `e255af5d070b43c7999852c6519fcd83803f695cec5a41ebe97d5efafef37cb7`
- Mechanical changes: instruction filename, runtime name

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced the automatic commit-push-PR-merge chain with action-by-action
  authorization and current GitHub capability routing.
- Added staged-diff, secret, restricted-data, dirty-tree, and gate-result
  checks.
- Plain force-push is prohibited; force-with-lease requires explicit,
  branch-scoped history-rewrite authorization.

## Behavior preserved

Intentional staging, quality gates, descriptive commits, branch workflow,
pull-request evidence, and merge verification remain.

## Behavior loss or limitations

One command no longer implicitly authorizes every external action. A disposable
repository forward test is pending.

- Validation: PASS
- Forward test: PASS (FT-03)