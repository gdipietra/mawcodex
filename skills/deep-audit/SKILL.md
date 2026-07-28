---
name: deep-audit
description: "Run a repository-wide consistency and release-readiness audit with deterministic validators plus four independent review lenses. Use after broad changes, before a release, or when asked to find inconsistencies. Read-only by default; use `--fix` only when the user explicitly asks to repair findings."
---

# $deep-audit — Repository Infrastructure Audit

Audit package structure, executable behavior, documentation, provenance, and
cross-surface consistency. Deterministic checks run first; four bounded
reviewers then inspect failure modes that static scripts cannot prove.

Missing tools, inaccessible sources, skipped renders, and unexecuted tests are
UNVERIFIED. They never count as PASS.

## Inputs and modes

- **Target repository** — defaults to the current repository.
- `--fix` — authorize local repairs inside the stated scope. Without it, make
  no edits and return an evidence-backed report.
- `--max-rounds N` — cap for repair/review cycles; default 5.

This skill never authorizes commit, push, pull-request creation, merge,
deployment, or release publication.

## Phase 0: Orient

1. Read all applicable `AGENTS.md` files.
2. Identify the manifest, package version, source-baseline record, validation
   entry points, expected surfaces, and dirty working-tree paths.
3. Preserve unrelated user changes. In `--fix` mode, stop if a required repair
   overlaps an ambiguous user edit.
4. Read [`audit-pet-peeves.md`](../../references/audit-pet-peeves.md) and give
   it to every reviewer as a checklist, not as an expected verdict.

## Phase 1: Deterministic checks

Run the repository's checked-in validation commands. For MAW Codex, start with:

```text
python scripts/validate_package.py
python scripts/run_skill_validators.py
python scripts/test_hooks.py
python -m unittest discover -s tests
```

Use the available Python executable for the current platform. Do not install
dependencies without authorization. Record command, exit status, and relevant
output. Classify unavailable commands as UNVERIFIED.

The deterministic layer must cover, at minimum:

- plugin manifest schema and package version;
- exact on-disk counts derived rather than copied from prose;
- skill frontmatter, links, metadata, and native-residue checks;
- custom-agent TOML parsing and portable-role mapping;
- hook schema, safe failure behavior, and executable smoke tests;
- source path, commit, source hashes, target hashes, license, and attribution;
- absence of secrets, migration placeholders, stale operational paths, and
  provider-specific execution syntax;
- internal links and referenced assets.

Do not patch a validator merely to silence a genuine finding. A false positive
may be corrected only with a documented minimal case.

## Phase 2: Four independent review lenses

Launch four bounded reviewers concurrently in isolated contexts. Prefer the
project's read-only custom agents when their roles fit; otherwise create
read-only subagents with these exact scopes. Give each the deterministic
results and relevant files, but do not give it another reviewer's conclusions.

### Reviewer 1 — Source and provenance

- Reconcile the immutable source baseline, source paths, source hashes,
  conversion classifications, target hashes, license, and third-party notices.
- Confirm unsupported or unclear-redistribution components are documented
  rather than copied.
- Check that source-specific historical names occur only in provenance records.

### Reviewer 2 — Skills, roles, and rules

- Check every packaged skill's trigger intent, input semantics, safety gates,
  output contract, cross-links, and PASS/FAIL/UNVERIFIED behavior.
- Reconcile each named agent with a portable role and local custom-agent file.
- Check rule-to-skill routing and contradictions across `AGENTS.md`,
  `references/rules/`, and skill bodies.

### Reviewer 3 — Executables and hooks

- Inspect all scripts and hooks for schema correctness, bounded inputs,
  path-safety, deterministic behavior, encoding errors, secret leakage, and
  documented exit semantics.
- Verify command hooks consume current Codex JSON input, write diagnostics to
  the correct stream, fail safely as documented, and never claim a blocked or
  skipped action succeeded.
- Compare docstrings and configuration maps to implementation.

### Reviewer 4 — Documentation and package UX

- Derive counts from disk and reconcile current user-facing documentation.
- Check install, update, upstream-sync, validation, and rollback instructions.
- Validate links, examples, platform assumptions, generated-versus-source
  artifacts, and release-status claims.
- Do not rewrite historical changelog entries merely because old counts differ.

Each reviewer returns typed findings:

```text
{id, severity, file, line, invariant, evidence, recommendation, confidence}
```

Reviewers must report `CLEAN` only after checking every item in their scope.

## Phase 3: Triage

Deduplicate on file, invariant, and evidence. Classify each item as:

- **Genuine finding** — supported by a reproducible example or direct evidence.
- **False positive** — contradicted by code, schema, or authoritative docs;
  record why.
- **UNVERIFIED** — evidence could not be obtained.

Use severity:

- **P0:** confidentiality, destructive behavior, scientific-invalidity, or
  release-integrity failure.
- **P1:** broken packaged behavior, schema failure, or false PASS claim.
- **P2:** maintainability or documentation defect with a safe workaround.
- **P3:** minor clarity or polish issue.

## Phase 4: Repair only with `--fix`

For each authorized finding:

1. Re-read the exact target and preserve unrelated changes.
2. Make the smallest coherent repair.
3. Run the narrow deterministic check.
4. Record the file, rationale, evidence, and result.

Never auto-repair restricted-data policy, citations, empirical specifications,
or human judgment calls. Stage those for the responsible researcher.

## Phase 5: Loop until dry

After repairs, rerun Phase 1 and launch fresh isolated reviewers for the
affected lenses.

- Converge only when a round yields zero new genuine findings and every
  required deterministic check passes.
- Stop at `--max-rounds`.
- Escalate a finding that persists across non-adjacent rounds; do not keep
  oscillating between patches.
- A clean review with UNVERIFIED required checks is `CONDITIONALLY CLEAN`, not
  release-ready.

## Report

Write `quality_reports/deep-audit/YYYY-MM-DD_<slug>.md` with:

- source baseline and target commit/working-tree state;
- exact commands and results;
- findings by severity with evidence;
- repairs made, if authorized;
- false positives and rationale;
- UNVERIFIED checks and concrete next steps;
- final state: `CLEAN`, `CONDITIONALLY CLEAN`, or `NOT CLEAN`.

The package can be called stable only when the repository's `AGENTS.md`
definition of stable is satisfied. This audit does not commit or publish the
result.

## Cross-references

- [`orchestrator-protocol.md`](../../references/rules/orchestrator-protocol.md)
  — bounded fan-out and convergence.
- [`summary-parity.md`](../../references/rules/summary-parity.md) — recurrence
  and disagreement handling.
- [`verifier.md`](../../references/agent-roles/verifier.md) — portable
  verification role.
