# `stata-replication` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/stata-replication/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d3d5a758c2742d2f9633b117cdd412d94479818379f1c93ffd0cda96de605e1e`
- Target: `skills/stata-replication/SKILL.md`
- Target SHA-256: `a35f86d45235defb7013dbc40d6ed5efde2bd0f68d011a3a35214211031eeefe`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced the Claude MCP install command and monitor assumptions with an
  environment-neutral guarded Stata capability and managed waits.
- Added immutable-data, estimand, inference, log, output-freshness, and exact
  sample-parity requirements.
- Preserved explicit no-execute and no-publication behavior.

## Behavior preserved

The numbered `.do` pipeline, one-command runner, Stata execution/logging,
verification, and optional R cross-check remain.

## Behavior loss or limitation

The workflow does not bundle or install Stata integration. Execution is
`UNVERIFIED` until a licensed Stata runtime is connected and tested.
