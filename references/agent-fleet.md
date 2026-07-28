<!-- Native rewrite of .claude/references/agent-fleet.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 76093c2a512a78eb7e10c7eb2bd8f7a51a365b6bc540fdfaeac2047b504df608. -->

# Codex academic agent fleet

The project defines 18 narrow custom agents in `.codex/agents/` and portable equivalents under `references/agent-roles/`. Model names are intentionally inherited; the durable routing controls are reasoning effort, sandbox, role scope, and evidence independence.

## High-judgment reviewers

`claim_verifier`, `domain_referee`, `domain_reviewer`, `editor`, `methods_referee`, `quarto_critic`, `sim_reviewer`, and `tikz_reviewer` use high reasoning and read-only sandboxes.

## Focused reviewers

`humanize_auditor`, `pedagogy_reviewer`, `proofreader`, `r_reviewer`, and `slide_auditor` are read-only roles with focused review schemas. `promote_memory_council` is a low-reasoning, read-only voting role.

## Workspace-writing roles

`beamer_translator`, `quarto_fixer`, `r_package_reviewer`, and `verifier` may write only within their assigned workspace scope. The latter two need workspace writes because package checks and render/compile verification create artifacts.

All agents return evidence to the parent for synthesis. None may commit, push, deploy, submit, send, or publish externally.

See `docs/conversion/AGENT_MAP.md`, `references/orchestration-schemas.md`, and `references/rules/model-routing.md`.
