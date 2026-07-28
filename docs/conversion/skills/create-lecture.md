# `create-lecture` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/create-lecture/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `eeebf07eabd63b86534d8fef50556709f4bc49f20d9b7ed9b59a71be0f42da1a`
- Target: `skills/create-lecture/SKILL.md`
- Target SHA-256 after semantic review: `6a0ea79f9a9650f6c302bd344e8694b83985efec019c3b4acf61d1849db28bea`
- Mechanical changes: rule path, runtime name

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Repaired assets, rules, and skill links and removed source-specific
  invocations.
- Required direct source reading and primary-source verification.
- Mapped substantive review to the portable `domain-reviewer` role and visual
  verification to `$compile-latex`.

## Behavior preserved

Knowledge-base preflight, notation consistency, motivation-first pedagogy,
outline approval, small drafting batches, figures, review, and knowledge-base
update remain.

## Behavior loss or limitations

No inaccessible paper or unrendered deck can be treated as verified. A full
lecture forward test is pending.

- Validation: PASS
- Forward test: PASS (FT-13)