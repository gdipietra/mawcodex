<!-- Native rewrite of .claude/references/scheduled-routines.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 21b3480ac84c94671e392c9d67485730e0c1e90de6904736822aa7a89d5e936b. -->

# Scheduled academic routines in Codex

Use a Codex Automation only when the user explicitly asks to create a recurring or scheduled task. Keep the repository workflow useful without automation.

Good candidates include nightly reproducibility checks, monthly memory review, dependency-drift reports, and pre-deadline disclosure audits. Each automation must define the repository, cadence and timezone, inputs, allowed mutations, stop conditions, result location, and notification behavior.

Scheduled work does not broaden authority. It must not submit, send, deploy, merge, publish, delete, or export restricted outputs unless the user explicitly authorized that action. Missing credentials or tools produce a report marked UNVERIFIED rather than an inferred success.
