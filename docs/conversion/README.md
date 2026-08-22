# Conversion record

This directory is the audit trail for translating the upstream Claude Code
workflow into MAW Codex.

## Required record for each component

- fixed source path, commit, and SHA-256;
- target path;
- portability classification;
- material revisions and rationale;
- preserved behavior and known loss;
- validation and forward-test status;
- upstream and third-party attribution.

## Status vocabulary

- `mechanical-baseline`: syntax/path conversion only; not release-ready.
- `semantic-review`: a reviewer is reconciling behavior with current Codex.
- `validated`: structure and component checks pass.
- `forward-tested`: a representative use case produced the expected behavior.
- `stable`: all required gates pass and no blocking limitation remains.

The component map and stability report are generated from the repository and
the per-component records; they are not substitutes for those records.

## Current stable baseline

Version `1.2.1` records 58 validated packaged skills: the 52 semantically
reviewed source-derived skills plus JAW, CAW, PAW, LAW, UAW, and SAW. It adds
the native ManageRAW agent, deterministic project state, two initial
forward-use-case profiles, and a public EN-US documentation surface while
retaining the existing evidence gates and fixed upstream boundary.

The baseline also records all 13 provider runtime surfaces outside the core
skill/agent/rule/reference/template inventory. The auxiliary coverage ledger
ensures every one of the fixed source commit's 211 tracked files has exactly
one conversion or disposition record. Future upstream refreshes begin from
the fixed `v2.1.0` source boundary and must create a new reviewed baseline;
they do not silently change this release record.
