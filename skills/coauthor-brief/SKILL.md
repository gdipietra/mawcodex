---
name: coauthor-brief
description: "Generate a co-author / collaborator handoff brief for a multi-author, multi-machine project — summarizing what changed since the last brief (git delta), the current state of each artifact (manuscript, analysis, slides), open questions, how to reproduce locally, and any restricted-data access steps. Use when user says \"coauthor brief\", \"handoff brief\", \"bring my coauthor up to speed\", \"what changed since last week\", \"onboard a collaborator\", \"write a handoff for [name]\", or before sending a co-author the repo. NOT a commit or a checkpoint — it is the cross-machine, cross-person summary `meta-governance.md` only partially covers."
---

## Codex execution contract

- Treat the user's request and applicable `AGENTS.md` files as authoritative.
- Resolve referenced resources relative to this skill first.
- Use bounded, isolated subagents for independent review roles; when a
  project custom agent is unavailable, use the matching portable role in
  `../../references/agent-roles/`.
- Treat missing tools, inaccessible sources, and skipped checks as
  UNVERIFIED rather than PASS.
- Require explicit user authorization for commit, push, merge, deploy,
  submission, sending, or other external publication.

# $coauthor-brief — Collaborator Handoff Brief

Produce a single Markdown brief a co-author (or your future self on another machine) can read in a few minutes to know **what changed, where each artifact stands, what's blocked, and how to run the pipeline locally** — including restricted-data access steps a new collaborator needs. [`meta-governance.md`](../../references/rules/meta-governance.md) covers the *memory* side of cross-machine work (what syncs via git, what stays in gitignored `personal-memory.md`); this skill covers the *human* side: the per-person, per-session handoff.

**Core principle:** `$checkpoint` is for you resuming; `$coauthor-brief` is for
someone else starting. The first answers "where am I?"; the second answers
"what do I need to know to take over a piece of this?"

## When to use

- **Before sending a co-author the repo** (or a PR / branch) and you want them oriented, not archaeologizing the git log.
- **Onboarding a new RA / collaborator** who needs the reproduce-locally and restricted-data steps in one place.
- **Periodic sync** on a long multi-author project — "here's the delta since the last brief."
- **Cross-machine handoff** — finishing on the office desktop, picking up on the laptop, or handing the analysis half to a co-author who runs Stata while you run R.

## When NOT to use

- For your own resume point, use [`$checkpoint`](../checkpoint/SKILL.md).
- For distilling a noisy task before compaction, use
  [`$compress-session`](../compress-session/SKILL.md).
- For a commit, use [`$commit`](../commit/SKILL.md).

## Phases

### Phase 0 — Determine the "since" point

Resolve the delta window, in this priority order:

1. `--since <arg>` if given — a git tag, an ISO date, or `Ndays` (e.g. `--since v1.2`, `--since 2026-05-01`, `--since 14days`).
2. Else, the **last brief** — `ls -t quality_reports/handoffs/*.md | head -1`; use the date in its filename as the floor.
3. Else, fall back to **14 days** and say so in the brief (an unbounded `git log` is noise, not signal).

Echo the resolved window back before gathering ("Brief covers changes since `<tag/date>` …").

### Phase 1 — Gather the delta + project state

Read-only collection. Skip any source that doesn't apply (R-only, Stata-only, no slides) rather than fabricating.

1. **Git delta** — `git log --oneline --since=<point>` (or `<tag>..HEAD`), `git diff --stat <point>..HEAD`, `git branch --show-current`, and `git log --all --oneline -15` to see co-authors' parallel branches. Group commits by area (manuscript / analysis / slides / infra).
2. **Reproducibility status** — if a passport exists at
   `quality_reports/passports/<slug>.yaml`, read the PASS, FAIL, EXPLAINED,
   STALE, and UNVERIFIED roll-up
   ([`$audit-reproducibility`](../audit-reproducibility/SKILL.md),
   [`replication-protocol.md`](../../references/rules/replication-protocol.md)).
   Claim replication-ready only if every required check is PASS.
3. **Open plan items** — most recent `quality_reports/plans/*.md` (status + any "Open questions" / "Next" lines) and the latest `quality_reports/session_logs/*.md` blockers.
4. **Environment / lockfiles** — locate the capture a collaborator needs:
   `renv.lock`, `requirements.txt`, `environment.yml`, `uv.lock`, or Stata
   version/package records produced by
   [`$capture-environment`](../capture-environment/SKILL.md). Record the exact
   restore command and label it UNVERIFIED if it was not tested.
5. **Restricted-data steps** *(skip if `--no-data-section`)* — if the repo
   touches restricted data, read
   [`confidential-data.md`](../../references/rules/confidential-data.md) and
   summarize the authorized access process. Never copy confidential values,
   live extract paths, credentials, or provider-confidential thresholds into
   the brief.

### Phase 2 — Write the brief

Use the template below. Keep it tight (~1–2 screens). Concrete `path:line` pointers beat prose.

```markdown
---
date: YYYY-MM-DD
for: [collaborator name or "all coauthors"]
since: [tag | date | Ndays]
branch: [current branch]
---

# Co-Author Brief — [project / paper short name]

## What changed since [since-point]
[3–8 bullets, grouped by area. Each: what changed + why it matters to a reader, not raw commit subjects.]
- **Analysis:** re-estimated the event-study with not-yet-treated controls (Callaway–Sant'Anna); main ATT now −1.19 — see `scripts/R/03_analyze.R:147`.
- **Manuscript:** Table 2 + §4.2 rewritten to match; Figure 3 regenerated.
- **Slides:** untouched.

## Current state of each artifact
| Artifact | Path | State | Notes |
|---|---|---|---|
| Manuscript | `manuscript.tex` | drafting §5 | robustness section is a stub |
| Analysis | `scripts/R/` | replication-ready | passport: 11 PASS, 1 EXPLAINED, 0 FAIL |
| Slides | `Slides/` | current | matches latest results |

## Open questions / decisions needed
[Things the co-author should weigh in on. Mark Q1, Q2…; flag which block progress.]

## Reproduce locally
1. Clone + branch: `git checkout <branch>`
2. Restore environment: `Rscript -e 'renv::restore()'` (or `pip install -r requirements.txt` / Stata `do _setup.do`).
3. Run the pipeline: `Rscript scripts/R/00_run_all.R` (or `00_master.do` / `make all`).
4. Verify: `$audit-reproducibility manuscript.tex` should report PASS with no
   FAIL, EXPLAINED, STALE, or UNVERIFIED claims.

## Restricted-data access (if applicable)
[Process to obtain access — DUA/IRB/enclave/openICPSR-restricted steps. NO actual data, paths to live extracts, or credentials. See confidential-data.md.]

## Recommended git topology for this project
- One **feature branch per author** (`feat/<author>-<topic>`); reconcile with
  `main`, then request the separately authorized commit, push, PR, and merge
  actions through `$commit`.
- `MEMORY.md` is **committed** — generic learnings sync to everyone.
- `personal-memory.md` and `.codex/state/` stay **local** (gitignored) — never expect a co-author to have yours (see meta-governance.md).
- Pull before you brief; brief before you hand off.
```

### Phase 3 — Save and summarize

1. Write to `quality_reports/handoffs/YYYY-MM-DD_coauthor-brief.md` (create `quality_reports/handoffs/` if missing). If `--for` is set, suffix the slug (`…_coauthor-brief_<name>.md`).
2. Print to chat: saved path, the resolved since-window, counts (commits summarized / open questions / artifacts), and whether the data section was included or skipped.

## Output / report format

A single Markdown handoff doc at `quality_reports/handoffs/YYYY-MM-DD_coauthor-brief.md` matching the Phase 2 template, plus a one-line chat summary. No edits to any other file.

## Exit behavior

- **Brief written:** exit 0 with the saved path and summary line.
- **No "since" resolvable and no git history in window:** still write the brief with an explicit "no changes in window" note rather than failing — a co-author starting fresh still needs the state + reproduce + data sections.
- **Restricted-data repo detected but `confidential-data.md` missing:** write
  the brief with `[CLARIFY: complete the access process from the controlling
  DUA]` and warn; do not guess the process.

## Flags

- `--since` `<tag|date|Ndays>` — Baseline to diff against — a git tag, an ISO date, or `Ndays` (e.g. `14days`). Default: the previous brief in `quality_reports/handoffs/`, else the last tag.
- `--for` `<name>` — Tailor the brief to a specific collaborator (e.g. surface the restricted-data access steps they still need).

## Cross-references

- [`meta-governance.md`](../../references/rules/meta-governance.md) — the
  cross-machine state model.
- [`$capture-environment`](../capture-environment/SKILL.md) — produces the
  lockfiles the brief points at.
- [`$checkpoint`](../checkpoint/SKILL.md) — self-resume companion.
- [`$compress-session`](../compress-session/SKILL.md) — distils a noisy task
  before compaction.
- [`confidential-data.md`](../../references/rules/confidential-data.md) —
  restricted-data handling.

## What this skill does NOT do

- **Push, open a PR, merge, or send the brief.** It writes a local document;
  each external action requires separate explicit authorization.
- **Run the pipeline or audit numbers.** It reports recorded status;
  [`$audit-reproducibility`](../audit-reproducibility/SKILL.md) performs the
  audit.
- **Capture the environment.** It locates existing lockfiles;
  [`$capture-environment`](../capture-environment/SKILL.md) generates them.
- **Expose restricted data.** It describes the *access process* only — never copies confidential values, live data paths, or credentials into a brief that may be emailed or committed.
