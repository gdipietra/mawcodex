---
name: promote-memory
description: "Review candidate `[LEARN]` entries from a local personal-memory file with five independent critics—generality, staleness, redundancy, evidence, and format—then propose promotion to a shared MEMORY.md only after explicit user approval. Use for requests such as \"promote memory\", \"review my learnings\", \"what should graduate to MEMORY.md?\", \"five-critic council\", or periodic memory maintenance."
---

<!--
Pattern adapted with attribution from Chris Blattman's claudeblattman v2.1
"Five-critic council" continuous-improvement workflow (April 2026). This
Codex-native version preserves independent lenses and an explicit human gate.
-->

# Promote Memory

Decide which local lessons are general, current, nonredundant, evidenced, and
well formed enough to enter shared memory. The council recommends; the user
decides.

## Memory boundary

Default candidate source: `.codex/state/personal-memory.md`.
Default shared target: `MEMORY.md`.

Before reading or writing, inspect applicable `AGENTS.md` and platform memory
instructions. If the active environment requires memory changes through an
update-note mechanism or forbids direct edits, follow that mechanism. Never
bypass host memory governance.

Do not include secrets, personal data, restricted research information,
machine-specific credentials, or confidential paths in critic prompts,
reports, or shared memory.

## Inputs

- `all`: review every `[LEARN:*]` candidate;
- a category or substring: review matching candidates only;
- explicit paths: use only within the authorized scope.

If the candidate source is absent, report that and stop. Preserve entry
boundaries and line references for the audit trail.

## Five independent critics

Prefer the project `promote-memory-council` custom agent definitions. Otherwise
spawn five bounded subagents in parallel, each in an isolated context and using
the applicable section of
[`promote-memory-council.md`](../../references/agent-roles/promote-memory-council.md).
Do not share other critics' verdicts.

Each critic returns `YES` or `NO`, a one-sentence rationale, and evidence:

1. **Generality:** would the lesson help the declared audience beyond one
   machine, project, or discipline?
2. **Staleness:** do referenced paths, functions, settings, and assumptions
   still exist and behave as claimed?
3. **Redundancy:** is the lesson already encoded in shared memory,
   `AGENTS.md`, a rule, or a skill?
4. **Evidence:** does the entry explain the incident or source that supports
   the lesson and the conditions under which it applies?
5. **Format:** does it satisfy
   [`meta-governance.md`](../../references/rules/meta-governance.md) and remain
   concise enough for shared memory?

Give only the minimum context each lens needs. The staleness critic may inspect
referenced project files read-only. The redundancy critic may read the current
shared memory and applicable instructions. Missing evidence yields
`UNVERIFIED`, which counts as `NO`.

## Aggregate

For each candidate:

- five YES: recommend promotion as written;
- four YES: recommend promotion with the dissent noted;
- three YES: recommend revision addressing dissent before promotion;
- two or fewer YES: do not recommend promotion.

A majority is a recommendation, not authorization.

Present:

```markdown
## `[LEARN:category] summary`

**Vote:** 4 of 5 YES

| Critic | Vote | Evidence and rationale |
|---|:---:|---|
| Generality | YES | ... |
| Staleness | YES | ... |
| Redundancy | YES | ... |
| Evidence | NO | ... |
| Format | YES | ... |

**Recommendation:** [...]
**Proposed shared-memory text:** [...]
**Required revision or unresolved check:** [...]
```

Do not silently rewrite the candidate. Make any proposed normalization visible.

## Approval and update

After presenting every verdict, stop and ask which exact entries the user
approves. Only after explicit approval:

1. apply the active environment's authorized memory-update mechanism;
2. add the approved, reconciled text to the appropriate shared section;
3. mark the local candidate promoted with date and target, or remove it only if
   the user explicitly selected removal and the change is recoverable;
4. write
   `quality_reports/memory_promotion_<YYYY-MM-DD>.md` with candidates,
   critic evidence, user decision, and resulting paths;
5. verify there is no duplicate entry and any size limit still holds.

Report proposed changes separately from confirmed changes.

## Boundaries

- Do not auto-promote, even on a unanimous vote.
- Do not demote or delete shared memory through this workflow.
- Do not rerun critics merely to hunt for a preferred vote; revise the evidence
  or leave the item local.
- Do not select a model alias or provider tier in the skill. Use the active
  project's agent policy.
- Do not commit or push memory changes without explicit authorization.
