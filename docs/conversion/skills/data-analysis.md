# `data-analysis` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/data-analysis/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `b9290417bc2f795eb67864fd9c2baf19c3090703c66adf4e08e2079cdb130a9a`
- Target: `skills/data-analysis/SKILL.md`
- Target SHA-256 after semantic review: `cb1a5eb8c59953b335666cadb58a4728a5757f226aa8d33e9d786eec6792c726`
- Mechanical changes: rule path

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Replaced positional input and provider-specific long-job monitoring.
- Made raw-data immutability, derived-output paths, sensitivity classification,
  join/exclusion provenance, and PASS/FAIL/UNVERIFIED explicit.
- Added descriptive/predictive/causal classification and causal-design
  safeguards; mapped R review to the portable role.

## Behavior preserved

Preflight schema inspection, exploration, estimation, tables, figures,
machine-readable objects, review, and reproducible scripts remain.

## Behavior loss or limitations

The workflow will not infer causal meaning or standardization choices from a
bare regression request. Real-data forward testing is pending.

- Validation: PASS
- Forward test: PASS (FT-11)