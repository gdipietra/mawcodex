# `simulation-study` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/simulation-study/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `ca5b247ebbb6784430cb149b92f664dcaeed4a192c07e9d804f44c6f1b345921`
- Target: `skills/simulation-study/SKILL.md`
- Target SHA-256: `a39b078659cf6d4aa7c7fd195bb2939d1c0ee0884c4869babd0aa9911b951bdc`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Reframed execution around capabilities and managed waits rather than
  provider-specific shell monitoring.
- Strengthened estimand/truth alignment, per-grid grouping, failure retention,
  MCSE interpretation, and rerun-after-fix requirements.
- Mapped simulation review to the portable `sim-reviewer` role.

## Behavior preserved

Parameterized DGP, estimator grid, deterministic replications, raw-result
retention, bias/RMSE/coverage/size/power metrics, figures, and review remain.

## Behavior loss or limitation

No R runtime or large Monte Carlo job is assumed. An executed study remains
pending.
