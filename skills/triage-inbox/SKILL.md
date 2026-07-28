---
name: triage-inbox
description: "Triage academic Gmail and Google Calendar context into a prioritized digest and referee-obligations tracker. Classify review requests, editorial correspondence, coauthor threads, invitations, and deadlines, then propose one human-gated action per item. Never sends mail, responds to invitations, or books events automatically."
---

# Academic Inbox and Calendar Triage

Read, classify, and propose. Outbound actions remain user-controlled, including
when this workflow runs on a schedule.

## Contract

- Use connected Gmail and Google Calendar capabilities; never request or store
  raw account credentials.
- Default to read-only connector operations. Creating a draft, changing labels,
  archiving, accepting/declining, or creating an event requires an explicit
  user request for that action after the exact change is shown.
- Store only sender, subject, short gist, deadline, bucket, and action. Do not
  copy full bodies, attachments, personal data, or restricted content into the
  repository.
- If connectors are unavailable, write a tracker-only digest and mark mail and
  calendar fetches `UNVERIFIED`.

## Phase 0: Pre-flight

Resolve:

- lookback window from the user's date/number of days, the last digest, or seven
  days;
- concurrent referee cap from the request, tracker header, or three;
- calendar on/off; and
- dry-run status.

Probe connector access with read-only operations and report the window, cap,
calendar status, dry-run status, and connector availability before fetching.

## Phase 1: Fetch and classify

Search recent email threads and, unless disabled, read relevant calendar
availability/deadlines. Put each thread in exactly one bucket:

| Bucket | Signals |
| --- | --- |
| Referee request | journal/editor invitation, manuscript ID, review request |
| R&R/editor | decision, revision language, explicit due date |
| Coauthor | known collaboration and concrete project asks |
| Seminar/conference | talk invitation, call, scheduling poll |
| Grant/admin | funder, compliance, IRB/DUA, reporting deadline |
| Noise | newsletters, receipts, automated notifications |

Record explicit deadlines exactly; do not infer a date from vague urgency.

## Phase 2: Propose one action

For every non-noise thread choose one:

- draft-reply proposal;
- calendar-hold proposal with conflict evidence;
- referee-project proposal if accepted/leaning yes and under the cap;
- decline-draft proposal when over the cap;
- concise ask summary with an offer to run `$coauthor-brief`; or
- snooze proposal with a resurfacing date.

For an R&R, offer `$respond-to-referees`. For an accepted review, offer
`$new-referee-project`. These are proposals, not automatic invocations.

Dry-run means no connector or local state changes beyond displaying the proposed
digest. In all modes, sending, accepting, declining, booking, and scaffolding
wait for explicit authorization.

## Phase 3: Digest and tracker

Unless dry-run, write:

- `quality_reports/inbox/YYYY-MM-DD_triage.md`; and
- `quality_reports/inbox/referee-obligations.md`.

Refresh tracker rows only from verified evidence of accepted, declined, or
completed reviews. Recompute open count versus cap and flag overdue items.

Digest structure:

```markdown
# Inbox Triage — YYYY-MM-DD
**Window:** [...] · **Referee cap:** K · **Fetch:** VERIFIED/UNVERIFIED
## Needs a decision
- **[bucket]** sender — gist; deadline. → Proposed action; conflict/cap evidence.
## FYI or snoozed
## Noise
## Referee load
## Unverified items
```

Return the digest path, counts by bucket, open reviews/cap, connector status, and
the exact list of proposed—not executed—actions.

## Scheduled use

A Codex schedule may run this read/classify workflow, but it must retain
the same no-outbound-action boundary. Scheduled connector failure is a normal
tracker-only `UNVERIFIED` run, not a reason to fabricate an empty inbox.

## Provenance

Native Codex rewrite of the upstream `triage-inbox` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
