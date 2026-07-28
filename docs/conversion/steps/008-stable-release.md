# Step 008 — Establish the stable package gate

## Revision

Added one release runner that validates the immutable source-fork contract,
package structure, provenance, official Codex plugin and skill schemas,
behavioral unit tests, and final release documentation. Added
machine-readable official-validation and forward-test evidence.

## Safety and distribution changes

- Added a preview-first personal-marketplace installer with explicit apply and
  update modes, collision refusal, staging, rollback, and timestamped backups.
- Made the project initializer transactional when Git is unavailable or
  initialization fails.
- Hardened Git guardrails against quoted, reordered, and compound commands;
  added a visible fail-open POSIX launcher when Python is absent.
- Added Windows runtime discovery through the Codex desktop bundled Python
  without changing system configuration.
- Fixed CI provenance by checking out the exact upstream source commit before
  validating the portable stable evidence.

## Verification

The local gate requires:

1. the exact clean fork/upstream source clone and recorded commit;
2. a current component and project-template provenance manifest;
3. Codex's official plugin validator;
4. Codex's official quick validator for 52/52 skills;
5. all deterministic tests, including hooks on Python and PowerShell,
   installer, initializer, launcher, and semantic contracts;
6. all representative forward-test records and current skill hashes;
7. release metadata, limitations, attribution, installation guidance, and the
   stability matrix.

The source-coverage gate also reconciles the four provenance manifests against
Git's fixed 211-file inventory, so an upstream file cannot be silently omitted
or counted twice.

## Result

Version `1.0.0` satisfies the local stable-package contract. Remote CI remains
future publication evidence and is not implied by the local result.
