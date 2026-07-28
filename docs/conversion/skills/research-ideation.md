# `research-ideation` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/research-ideation/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `b580aaa7d3e07339ed1ddb10192e28bd603eb254cc0cb14fb4d5c2f14e7a3685`
- Target: `skills/research-ideation/SKILL.md`
- Target SHA-256: `630e265a57f119bbc2c2506084476579d17f7b91132c7cdd99045b88323eb190`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Added estimands, inference, falsification, ethics, disclosure risk, and
  cheapest-decisive-check fields to each candidate.
- Replaced Claude references and web tools with current primary-source search,
  portable paper-type definitions, and an isolated claim-verifier role.
- Bounded novelty claims and required official dataset codebooks and policy
  sources.

## Behavior preserved

Three-to-five one-shot ideas, paper-type tags, hypotheses, designs, data
requirements, threats, ranking, and local report remain.

## Behavior differences and loss

Creative breadth is constrained by evidence status. Unverified datasets,
literature, or designs are labeled rather than presented as feasible facts.
