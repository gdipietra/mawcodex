# `manageraw` agent record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex control-plane design; no upstream agent
- Custom agent: `.codex/agents/manageraw.toml`
- Portable role: `references/agent-roles/manageraw.md`

## Intent

The upstream workflow supplies academic execution roles but does not provide a
Codex-native manager for fitting the package into multiple ongoing projects
or coordinating it with unrelated plugins. ManageRAW fills that control-plane
gap without changing the fixed 18-agent upstream conversion boundary.

## Design decisions

- MAW retains academic-governance ownership while named specialist plugins may
  own external operations.
- Actual Codex instruction precedence remains in global, root, and nested
  `AGENTS.md`; `.maw/profile.yaml` records shared routing decisions.
- The agent begins read-only and writes only an exact approved local
  control-plane change.
- JAW, CAW, PAW, LAW, UAW, and SAW remain separate capabilities so
  personalization does not absorb layering, updates, or reusable exports.
- UAW and SAW are explicit-only maintenance operations.
- Teaching with existing LaTeX and research with mixed Stata/R are mandatory
  forward-use-case profiles.

## Behavior loss or limitations

ManageRAW cannot alter global user instructions from a project, merge
same-named skills, or infer the private behavior of an external plugin. It
records explicit ownership and falls back to a documented handoff when a
specialist capability is unavailable.

- Validation: package structure, semantic contracts, deterministic state
  checks, and two forward-use-case fixtures.
