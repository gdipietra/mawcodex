# Research project deployment profile

Use this profile in addition to the core JAW workflow when research artifacts
are material.

## Source and data roles

- Identify the current manuscript, any historical mirror, and which local or
  remote copy controls publication.
- Separate raw, derived, temporary, and final data. Raw data stays immutable.
- Identify restricted, licensed, human-subjects, or enclave-bound data before
  running code or proposing sync.
- Locate data dictionaries, access agreements, exclusion rules, and
  disclosure requirements.

## Analysis and inference

- Detect all analysis languages and their true entry points.
- Locate lockfiles, session information, seeds, caches, expected outputs, and
  runtime notes.
- Map headline claims to scripts, tables, figures, or machine-readable
  intermediate results when possible.
- For causal work, identify the estimand, treatment timing, comparison group,
  identifying assumptions, inference method, and diagnostics. Readiness does
  not certify those choices; it records whether the relevant safeguards exist.

## Manuscript and collaboration

- Identify bibliography authority, citation keys, journal templates, response
  letters, appendices, and supplementary materials.
- Preserve current and comparison versions during revision.
- Record collaborator-facing, Overleaf, Drive, or Dropbox roles before moving
  files.
- Keep publication, submission, repository deposit, and coauthor handoff as
  separate authorization gates.

## Minimum research readiness evidence

| Area | Evidence |
| --- | --- |
| Repository | real Git state, instructions, protected paths |
| Data | raw/derived roles and sensitivity classification |
| Environment | actual stacks and dependency artifacts |
| Execution | representative analysis entry point or a documented UNVERIFIED |
| Manuscript | current source and bibliography authority |
| Reproducibility | seeds, outputs, and claim provenance status |
| Disclosure | export/publication constraints and responsible approver |
