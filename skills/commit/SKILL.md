---
name: commit
description: "Safely carry out only the Git and GitHub actions the user explicitly authorizes: stage selected files, commit, push, open a pull request, or merge. Use on direct intent such as \"commit these files\", \"push this branch\", \"open a PR\", or \"merge PR 42\"; vague completion language is not authorization. Never use plain force-push or skip hooks."
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

# Commit, Push, Pull Request, and Merge

Execute only the explicitly authorized portion of the publication chain. A
request to commit does not authorize a push; a push does not authorize opening
a pull request; opening a pull request does not authorize merging it.

## Phase 0: Resolve scope and authorization

1. Translate the user's words into the authorized actions:
   `stage`, `commit`, `push`, `open PR`, and/or `merge`.
2. Identify the repository, branch, target files, remote, and base branch.
3. If any externally visible action is not explicit, stop before that action
   and report the exact next command or connector action awaiting approval.
4. Inspect status, staged changes, unstaged changes, recent history, and the
   current branch. Preserve unrelated user changes.

## Phase 1: Run applicable gates

Run repository-provided deterministic checks that apply to the selected
changes. For MAW Codex itself, use the package validation entry point and
surface-sync check documented in `scripts/`. For research artifacts, apply
their compilation, render, reproducibility, disclosure, and citation gates as
applicable.

When independent verification adds value, use the project `verifier` custom
agent or a bounded read-only subagent following
[`verifier.md`](../../references/agent-roles/verifier.md). Give it the exact
diff and checks; do not leak an expected verdict.

- A failed required check blocks the commit.
- A missing tool, inaccessible source, or skipped check is UNVERIFIED, not
  PASS. Ask before overriding a relevant gate.
- If the user explicitly accepts an exception, record the affected check and
  consequence in the commit or pull-request description. Never override
  scientific-validity, confidentiality, or secret-scanning gates.

## Phase 2: Branch and stage intentionally

- Do not commit directly to a protected default branch. If a new branch is
  needed and branch creation is within scope, create a short descriptive one.
- Stage only the paths the user placed in scope; never use a catch-all staging
  command when unrelated changes exist.
- Inspect the staged diff and staged file list before committing.
- Exclude local settings, credentials, tokens, restricted data, derived
  confidential outputs, and other ignored/private state. Stop on any suspected
  secret rather than attempting to sanitize it silently.

## Phase 3: Commit

If commit is authorized, create one coherent commit with a message that
explains why. Use the user's exact message when they supplied one. Do not amend
an existing commit, bypass hooks, or sign on the user's behalf unless that
specific action was requested and supported.

Afterward, report the commit identifier, subject, files included, and gate
results. If commit was the end of the authorization, stop here.

## Phase 4: Push

If push is explicitly authorized:

1. Confirm the destination remote and branch.
2. Push normally and set upstream tracking when needed.
3. Never use plain force-push. `--force-with-lease` is permitted only when the
   user explicitly requests history replacement, the exact rewritten range and
   remote branch have been reviewed, and the lease protects unseen remote work.

Report the remote branch. If push was the end of the authorization, stop.

## Phase 5: Open a pull request

If opening a pull request is explicitly authorized, create it through the
connected GitHub capability when available. Include:

- a concise summary of behavior and provenance changes;
- the exact validation results, separating PASS, FAIL, and UNVERIFIED;
- known limitations and reviewer attention points;
- a test plan that reflects checks actually run.

Open as a draft unless the user asked for a ready-for-review pull request.
Report the URL. Do not merge unless separately authorized.

## Phase 6: Merge

If merge is explicitly authorized:

1. Re-read current pull-request status and required checks.
2. Confirm approvals, mergeability, base branch, and merge method.
3. Refuse to represent failing or pending required checks as green.
4. Merge using the repository's configured policy, not a hard-coded method.
5. Delete the remote branch only when requested or when repository policy
   makes that consequence clear.

Report the merge commit and any cleanup actually completed.

## Invariants

- Never infer authorization from "done", "wrap up", or similar language.
- Never use plain force-push, bypass hooks, hide failures, or stage unrelated
  files. Use force-with-lease only under the Phase 4 gate.
- Never commit secrets, personal data, restricted data, or machine-local
  settings.
- Preserve an auditable separation between validation evidence and human
  overrides.
