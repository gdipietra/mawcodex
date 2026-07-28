# `verify-claims` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/verify-claims/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `971ecc28b4e6d2ca264d0e185d9b9b0e2009f02eed840f51adb58d30384988de`
- Target: `skills/verify-claims/SKILL.md`
- Target SHA-256: `b93e8332e2260da34090e0946909fe4f2c5032bc2e7f5b1551fa56628fcbd007`
- Validation: `PASS`
- Forward test: PASS (FT-07)
## Material revisions

- Replaced the Claude agent call with a project custom agent or fresh bounded
  subagent using the portable claim-verifier role.
- Strengthened claim/citation pairing, primary-source evidence, independence,
  EXPLAINED limits, and explicit UNVERIFIED aggregation.
- Recast the commit block as a documented downstream release gate without
  authorizing a commit.

## Behavior preserved

The four-step CoVe loop, fresh-context independence, claim types, tiered
verdicts, fail-closed default, evidence-based correction, and recovery modes
remain.

## Behavior loss or limitation

Source access and exact evidence extraction depend on available capabilities.
An end-to-end claims corpus forward test remains pending.
- Target SHA-256 after semantic review: `17200dd7a309bb30bfbd11d969039d307121697417f6a085410d29eda6146b19`
