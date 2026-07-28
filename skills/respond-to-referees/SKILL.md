---
name: respond-to-referees
description: "Generate a structured response-to-referees document from a referee report and revised manuscript. Map every concern to evidence in the revision, classify coverage, draft courteous responses, and verify all revision-location claims. Use during a revise-and-resubmit."
---

# Respond to Referees

Cross-reference a referee report against a revised manuscript and produce an
auditable response document. Never invent a revision, location, manuscript ID,
or journal detail.

## Codex execution contract

- Treat the user's request and applicable `AGENTS.md` files as authoritative.
- Resolve referenced resources relative to this skill.
- Missing extractors, unreadable inputs, or skipped checks are `UNVERIFIED`,
  never PASS.
- Use a bounded, isolated `claim-verifier` subagent for the independent
  post-flight check. If that custom agent is unavailable, give a fresh subagent
  the role in
  [`claim-verifier.md`](../../references/agent-roles/claim-verifier.md).
- Writing a local draft is allowed. Sending or submitting it requires explicit
  user authorization.

## Inputs

Require:

1. the referee-report path; and
2. the revised-manuscript path.

Accept `.tex`, `.qmd`, `.md`, and `.txt` directly. For `.pdf`, `.docx`, or
`.html`, use an available trusted extractor and a securely created temporary
file. Retain the original for page references. If extraction is unavailable or
fails, ask for plain text and stop with the affected input `UNVERIFIED`.

## Workflow

### 1. Parse the full report

Read the report end to end. Decompose explicit and implicit concerns, including
major, minor, and typographic sections. For each concern record:

- ID `R{referee}.{comment}`;
- referee-assigned severity;
- a representative quote of no more than about 25 words; and
- a one-line neutral summary.

### 2. Locate evidence in the revised manuscript

For each concern, search the extracted manuscript text using key terms and
reasonable synonyms, inspect the surrounding context, and map the evidence back
to a page, section, line range, table, or figure in the original. Do not treat a
keyword hit as evidence without reading its context.

### 3. Classify coverage

Use exactly one classification:

| Classification | Evidence standard |
| --- | --- |
| Addressed | A specific revision directly resolves the concern. |
| Partially addressed | The revision moves toward the request but leaves part unresolved. |
| Deferred | No revision was made and a concrete, author-approved rationale is supplied. |
| Disagreement | The response respectfully explains why the premise or requested change is not accepted. |
| UNADDRESSED — REQUIRES AUTHOR INPUT | No revision evidence or defensible author decision is available. |

Never infer a defer/disagree rationale on the authors' behalf.

### 4. Draft responses

For every concern, write three to six sentences that:

1. acknowledge the concern without flattery;
2. state the change or the author-approved reason for not changing;
3. cite the verified manuscript location; and
4. explain any divergence from the exact request.

Use a courteous, firm, non-defensive voice and author-team “we” only where
appropriate.

### 5. Produce the document

Write `response-to-referees.md` or the user-specified path using
[`response-to-referees.md`](../../assets/templates/response-to-referees.md):

- journal, manuscript ID, revision round, and date;
- a concise cover paragraph;
- numbered per-referee responses; and
- a complete concern matrix.

Optionally write `response-to-referees-matrix.csv`.

### 6. Mandatory independent post-flight

Follow
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md).
Extract every claim that the authors added, modified, or moved something at a
specific location. Turn each into an answerable verification question. Give
only the claims, questions, manuscript path, and source pointers to the isolated
verifier—never the response draft.

Reconcile the evidence:

- correct revision and location: retain `Addressed`;
- revision at another location: correct the location;
- partial evidence: downgrade to `Partially addressed`;
- no verifiable evidence: downgrade to `Deferred` only with an author-approved
  rationale, otherwise mark `UNADDRESSED — REQUIRES AUTHOR INPUT`.

If the user explicitly requests `--no-verify`, label all revision-location
claims `UNVERIFIED` and warn that the draft is not submission-ready.

## Completion report

Confirm that every concern has one classification, every addressed/partial item
has a verified location, and the header matches the supplied metadata. In the
chat response list all unresolved concerns, or state:
`All concerns addressed or explicitly classified.`

For a pre-submission rehearsal, suggest `$review-paper --peer --r2 <journal>`.
For a first-pass manuscript review, use `$review-paper`.

## Provenance

Native Codex rewrite of the upstream `respond-to-referees` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT). See the per-skill
conversion record for the source hash and revision notes.
