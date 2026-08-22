# `deep-audit` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/deep-audit/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `6227f6bcd3691360b0822e38e9709ca65165c32a4a21576e47c04d3e401b7427`
- Target: `skills/deep-audit/SKILL.md`
- Target SHA-256 after semantic review: `38ed12e1ef2010e9dfd76b6807dd2d743b41873d3ea21efacab3d04cc5902a43`
- Mechanical changes: context isolation, hook path, instruction filename, rule path, runtime name, script path, skill invocation syntax

## Preserved intent

The source trigger intent, workflow body, outputs, and quality gates were
retained as the semantic-review baseline.

## Material revisions

- Rebuilt the audit around MAW Codex manifest, validators, skills, portable
  roles, custom agents, hooks, provenance, and package docs.
- Replaced provider-specific permissions and agents with four isolated,
  read-only review lenses and typed findings.
- Made audit read-only by default; `--fix` is required for repairs.

## Behavior preserved

Deterministic-first validation, parallel specialist review, deduped triage,
loop-until-dry convergence, recurrence escalation, and a final report remain.

## Behavior loss or limitations

Legacy guide pages, permission-frontmatter parity, and private session paths
are intentionally absent. Full-repository forward testing is pending.

- Validation: PASS
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Release 1.2.2 revision

- Corrected the hook validation command to invoke the packaged unittest modules
  instead of the nonexistent `scripts/test_hooks.py` entry point.
- Classification remains a Codex-native rewrite of the upstream audit workflow.