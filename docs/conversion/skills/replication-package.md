# `replication-package` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/replication-package/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `20597f5ebe29f46042d456ef7471136dc6a3ec5616036ad73e04b2eae448fb64`
- Target: `skills/replication-package/SKILL.md`
- Target SHA-256: `a63966971c9ff1ac5aba97b855303caa5a5eb240b04270d40823abbe1abe1f89`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: PASS (FT-05)
## Material revisions

- Added current official target-requirement checks, data/license
  classification, checksums, immutable raw-data handling, and a self-contained
  tree without fragile machine-local links.
- Preserved environment capture and made the reproducibility audit a strict
  PASS/EXPLAINED/UNVERIFIED/FAIL gate.
- Strengthened restricted-data, redistribution, disclosure, credential, and
  external-upload protections.

## Behavior preserved

README, data manifest, environment, one-command entry, exhibit-to-code map,
DCAS-style checklist, restricted-data note, and local package assembly remain.

## Behavior differences and loss

Unclear redistribution terms now block copying, and inaccessible runs remain
`UNVERIFIED`. No repository upload is performed.
