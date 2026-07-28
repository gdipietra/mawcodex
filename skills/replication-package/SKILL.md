---
name: replication-package
description: "Assemble a local, submission-oriented research replication package with a standard README, data and license manifest, environment capture, one-command run entry point, exhibit-to-code map, reproducibility gate, and restricted-data access plan. Use for requests such as \"build the replication package\", \"prepare the openICPSR deposit\", \"make the AEA data and code package\", \"DCAS compliance\", or \"assemble the journal deposit\". Packages verified artifacts but never uploads them."
---

# Replication Package

Build a deposit that an independent researcher can understand and run without
tacit instructions. Every table and figure must map to code and an expected
output; every dataset must have source, access, and redistribution status.

Use the
[Data and Code Availability Standard](https://datacodestandard.org/) and the
intended repository or journal's current official instructions as primary
requirements. Because deposit rules change, record URLs and access dates.
Unavailable current guidance makes conformance `UNVERIFIED`.

## Inputs

- manuscript source or PDF;
- analysis-output location, if it cannot be inferred;
- intended deposit target, if known;
- optional existing research passport or exhibit map.

Default output is `replication_package/` inside the authorized workspace. If it
exists, preserve it and ask whether to update in place, create a comparison
version, or stop.

## 1. Orient and classify

1. Read applicable `AGENTS.md`, data-use, IRB, enclave, and license
   instructions.
2. Detect all analysis languages and environment files.
3. Locate the controlling one-command entry point and expected outputs.
4. Inventory manuscript exhibits and trace them to scripts and output files.
5. Classify every input:
   - public and redistributable;
   - public but not redistributable;
   - restricted under DUA or enclave;
   - proprietary;
   - personally identifying or disclosure-sensitive;
   - derived and disclosure-reviewed.
6. Record source, version, checksum where allowed, access procedure, license,
   and package inclusion decision.

Never assume public availability implies redistribution permission. Do not copy
an input whose terms are unclear; mark it `[FILL]` or `BLOCKED` and provide an
access pointer.

## 2. Draft the README and manifests

Create `replication_package/README.md` with:

- paper title, authors if supplied, citation, and overview;
- data availability statement;
- dataset manifest:
  `file | description | source | version/checksum | access | license |
  included? | reason`;
- computational requirements: OS, software versions, packages, runtime, RAM,
  storage, and cluster needs;
- clean-environment setup;
- one-command run instructions;
- expected outputs and approximate runtime;
- known discrepancies;
- support/contact field left `[FILL]` unless the user supplied it;
- exhibit map:
  `Exhibit | output file | program | function or line | input provenance`.

Use an existing research passport as evidence when present. Otherwise trace
`\input`, `\includegraphics`, Quarto inclusions, and code writes. Do not invent
program-line mappings.

## 3. Capture the environment

Apply [$capture-environment](../capture-environment/SKILL.md) when available.
Capture the actual environment for each language:

- R lockfile and `sessionInfo()`;
- Python lock or environment export and interpreter version;
- Stata version and pinned `version` statements;
- system libraries, fonts, TeX/Quarto versions, and container image when they
  affect outputs.

Do not mutate the researcher's primary environment merely to create a lockfile
without explaining and authorizing the effect. A missing capture is
`UNVERIFIED`, not a completed requirement.

## 4. Reproducibility gate

Apply
[$audit-reproducibility](../audit-reproducibility/SKILL.md) to the manuscript,
outputs, and passport.

- Any unexplained numeric or exhibit `FAIL` blocks assembly of a
  submission-ready package.
- A named, evidenced alternative may be `EXPLAINED`; carry it into the README.
- Missing software, data access, or an unrun pipeline is `UNVERIFIED` and
  prevents a full-pass claim.

Do not relabel `UNVERIFIED` as `PASS` merely because the files are organized.

## 5. Assemble a portable tree

Create:

```text
replication_package/
├── README.md
├── LICENSES/
├── data/
│   ├── raw/          # redistributable as-obtained inputs only
│   ├── analysis/     # documented derived inputs
│   └── access-restricted-data.md
├── code/             # ordered scripts and one-command entry point
├── output/
│   ├── tables/
│   ├── figures/
│   ├── logs/
│   └── environment/
└── DCAS_checklist.md
```

Copy only files whose inclusion is authorized and licensed. Prefer a
self-contained copy over fragile machine-local symlinks. Keep raw source data
immutable; never rewrite it during packaging. Replace restricted or
nonredistributable data with a documented acquisition or enclave procedure.

Check code for absolute paths, credentials, personal names, local drive
letters, undeclared randomness, and undocumented manual steps. Set and record
seeds for stochastic work.

## 6. Confidentiality and disclosure

Follow
[`confidential-data.md`](../../references/rules/confidential-data.md).

- Never place restricted, proprietary, PII-bearing, or enclave-only data in
  the package.
- Ship runnable code when terms permit, with a realistic access path.
- Document provider, application or DUA process, expected environment, and any
  synthetic or test data.
- Review every public derived table, figure, log, and intermediate for
  disclosure risk. If formal disclosure review was not performed, mark it
  `UNVERIFIED`.

This workflow does not de-identify raw microdata or override an IRB, DUA,
provider, or enclave rule.

## 7. Validate and report

The checklist must cover:

- current target requirements and access date;
- data availability statement;
- source/access/license for every dataset;
- one-command entry point;
- environment and runtime;
- exhibit-to-code map;
- no machine-specific paths or credentials;
- seeds and stochastic-output provenance;
- reproducibility audit;
- confidential-data access note and disclosure review;
- code and data licenses;
- open `[FILL]`, `BLOCKED`, and `UNVERIFIED` items.

Write
`quality_reports/replication_package_<paper-slug>.md` with checklist status,
tree path, copied-file inventory, omitted restricted files, and blockers.

## Exit behavior

- `PASS`: all applicable checks ran and no blockers remain.
- `INCOMPLETE`: local skeleton exists but `[FILL]` or `UNVERIFIED` items remain.
- `BLOCKED`: reproducibility failed, restricted data would be exposed, or
  redistribution terms are absent.

Never upload to openICPSR, Zenodo, Dataverse, a journal portal, or any other
external system without a separate explicit user request and final content
review.
