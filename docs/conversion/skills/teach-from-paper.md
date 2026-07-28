# `teach-from-paper` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/teach-from-paper/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `484374933e8dccef0c2e7001cb708e7c81c3dd8b4a9240bf38cd19f03bbd491d`
- Target: `skills/teach-from-paper/SKILL.md`
- Target SHA-256: `4379a9af60294aa25a6685db1be1a84e393d9bbd2e8a9fd4da7522d419a262a2`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced positional arguments and fixed context-size claims with semantic
  inputs, complete-source coverage, and extraction status.
- Added evidence locations, notation remapping, unsupported-interpretation
  handling, and explicit handoffs to Codex skills.
- Added local-write versus external-sharing boundary.

## Behavior preserved

Audience calibration, three-to-five results, intuition/failure modes, lecture
arc, slide skeleton, discussion questions, and exercise brief remain.

## Behavior loss or limitation

PDF extraction is runtime-dependent, and the workflow does not validate the
paper's correctness. Representative teaching-package output is pending.
