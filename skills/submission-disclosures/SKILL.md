---
name: submission-disclosures
description: "Draft a manuscript's submission-time AI-use disclosure, CRediT author roles, conflict-of-interest statement, and data-availability statement against the current target-journal policy. Use for submission or resubmission packages; not for statistical disclosure-control screening."
---

# Submission-Time Disclosure Block

Draft four truthful, journal-aligned statements for author review. This workflow
does not submit them and does not screen statistical outputs; use
`$disclosure-check` for restricted-data disclosure risk.

## Contract

- Current journal policy is unstable. Verify it on the journal or publisher's
  official author-guidance pages and record direct URLs plus retrieval date.
- Use primary sources; a cached profile is orientation, not current proof.
- Never infer an author's contribution, conflict, funding relationship, AI use,
  or data-access condition without evidence or author confirmation.
- An inaccessible policy is `UNVERIFIED`; draft conservative fallback wording
  labeled for manual verification.
- Never write a false “no AI use” statement when project evidence contradicts
  it.
- Output is a draft. Submission, portal entry, or sending requires explicit
  authorization.

## Inputs

Resolve:

- manuscript path;
- target journal or publisher;
- whether the user asserts no AI assistance; and
- whether statements should be chat-only or written locally.

## Phase 1: Verify current policy

Use current web search to locate official author guidelines, publication ethics,
AI policy, contributor policy, conflict disclosure, and data-availability
requirements. Record:

| Topic | Official source | Retrieved | Requirement | Status |
| --- | --- | --- | --- | --- |
| AI use | URL | date | ... | VERIFIED/UNVERIFIED |
| CRediT | URL | date | ... | ... |
| COI | URL | date | ... | ... |
| Data | URL | date | ... | ... |

If no explicit AI policy is found, say so and use transparent fallback wording
that names tools, scope, and human responsibility.

## Phase 2: Evidence-based inventory

Ask the authors to confirm:

- tools and versions, and whether used for prose, code, review, literature
  search, analysis, images, or translation;
- which outputs were independently checked and how;
- the 14 CRediT roles by author;
- funding, employment/advisory positions, data-provider relationships, IRB/DUA
  constraints, and other conflicts; and
- data/code availability, repository/access conditions, and embargoes.

Repository traces can identify questions but are not proof of who performed a
role. If the user asserts no AI use and visible evidence conflicts, stop and
surface the conflict.

## Phase 3: Draft

Write `quality_reports/submission_disclosures_<manuscript-slug>.md`, unless
chat-only output was requested:

1. **AI-use disclosure:** tool/version, precise scope, verification performed,
   and authors' responsibility. Do not claim verification that was not run.
2. **CRediT statement:** map confirmed authors to confirmed roles; flag
   unassigned roles rather than guessing.
3. **Conflict-of-interest statement:** include confirmed funding, positions,
   relationships, and applicable restrictions.
4. **Data-availability statement:** align exactly with the actual replication
   deposit or access process and
   [`confidential-data.md`](../../references/rules/confidential-data.md).

If no-AI mode was confirmed and consistent with available evidence, omit the AI
statement rather than inventing a denial unless the journal explicitly requires
one.

## Phase 4: Manuscript parity

Inspect existing acknowledgments, author-contribution, conflict, ethics, and
data-availability text. Produce a contradiction/difference list. Do not silently
overwrite manuscript language.

## Completion

Return the four drafts, official policy links/dates, all `UNVERIFIED` items, and
the local path if written. Remind the user that every author must review and
approve statements before submission. `$replication-package` handles the
deposit; `$verify-claims` and `$audit-reproducibility` support only disclosure
claims that were actually checked.

## Provenance

Native Codex rewrite of the upstream `submission-disclosures` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
