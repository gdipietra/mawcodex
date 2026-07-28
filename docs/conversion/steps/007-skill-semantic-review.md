# Step 007 — Review all skills and test representative behavior

## Revision

Reviewed all 52 mechanically migrated skills against the fixed upstream source
and current Codex surfaces. Rewrote provider-only paths, tool names, command
syntax, agent orchestration, failure semantics, and authorization boundaries.
Generated an `agents/openai.yaml` interface file for every skill.

## Behavioral preservation

- Preserved the plan–implement–verify discipline, staged author/instructor
  approvals, independent review roles, and explicit post-flight status.
- Preserved applied-micro estimand, identification, inference, staggered
  adoption, reproducibility, restricted-data, and disclosure safeguards.
- Replaced unavailable external operations with an explicit handoff or
  `UNVERIFIED` result rather than an invented success.
- Required explicit authorization for commit scope, push, send, submission,
  upload, publication, deployment, and external synchronization.

## Verification

- Codex's official quick validator passed for 52/52 skills.
- The provider-residue and relative-link gates passed.
- Fourteen deterministic semantic-contract tests guard the highest-risk
  instruction boundaries.
- Fifteen independent subagent forward tests exercised incomplete inputs,
  missing runtimes, restricted data, misleading success requests, and external
  actions. All produced the expected safe decision path.
- A targeted retest confirmed that an inaccessible material source leaves a
  claim `cannot-verify` and the aggregate paper status `UNVERIFIED`.

## Result

All skill conversion records are `validated` or `forward-tested`. The
machine-readable matrix binds each tested scenario to the SHA-256 of the exact
skill text evaluated.
