<!-- Adapted from .claude/rules/session-logging.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 31d9ac9dba253eba5c77c572f69783c722a57f7bdbf3445822c9aa24ef61c95e. -->

## Applicability

Load this rule for: All academic tasks when relevant.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# Session Logging

**Location:** `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Template:** `templates/session-log.md`

## Three Triggers (all proactive)

### 1. Post-Plan Log

After plan approval, immediately capture: goal, approach, rationale, key context.

### 2. Incremental Logging

Append 1-3 lines whenever: a design decision is made, a problem is solved, the user corrects something, or the approach changes. Do not batch.

### 3. End-of-Session Log

When wrapping up: high-level summary, quality scores, open questions, blockers.

## Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md` using `templates/quality-report.md`.
