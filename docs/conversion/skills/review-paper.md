# `review-paper` conversion

- Status: `forward-tested`
- Classification: `composed replacement`
- Source: `.claude/skills/review-paper/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `7b73e89e1da1fb4977ef5e4f859bcb314098f2559597a0a842271d6fbddee67d`
- Target: `skills/review-paper/SKILL.md`
- Target SHA-256: `26d5f85dd3cd10b8641e3bf9ac886b92c54b8bdb8fc886d6463d7dac981c068e`
- Validation: `PASS`
- Forward test: PASS (FT-06)
## Material revisions

- Recast default, adversarial, peer, R&R, stress, and variance branches around
  Codex isolated subagents and portable roles.
- Removed model-tier assumptions and false token/probability precision.
- Added current-source journal checks, independent novelty verification,
  cross-artifact UNVERIFIED semantics, and explicit edit/release authorization.

## Behavior preserved

The three principal modes, journal calibration, blinded referees, variance
sampling, critic-fixer convergence, cross-artifact integration, and
post-judge hallucination gate remain.

## Behavior loss or limitation

Agent-cost routing is runtime-dependent rather than tied to upstream model
aliases. Journal profiles and full multi-agent acceptance tests remain pending.
