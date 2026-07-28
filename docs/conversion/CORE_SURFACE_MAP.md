# Core provider-surface map

Source boundary: upstream commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`).

The component manifest covers skills, agents, rules, references, and artifact
templates. This map covers the remaining provider runtime surfaces that shape
the original setting. Exact source and target hashes, classifications, and
per-surface revision summaries are in `RUNTIME_SURFACES_MANIFEST.json`.

| Source surface | Codex-native disposition | Classification |
| --- | --- | --- |
| `CLAUDE.md` | Root package `AGENTS.md` plus project-template `AGENTS.md` | composed replacement |
| `.claude/settings.json` | Safe `.codex/config.toml`, trusted hooks, and explicit repository authority rules | native rewrite |
| `.claude/output-styles/academic-writing.md` | Portable writing guidance plus `$humanize` and `$proofread` | composed replacement |
| `.claude/output-styles/referee.md` | `$review-paper` plus the portable domain-referee role | composed replacement |
| `.claude/scripts/statusline.sh` | Codex task/context UI, `$context-status`, and supported compaction state | composed replacement |
| `.claude/WORKFLOW_QUICK_REF.md` | `AGENTS.md`, README, plan-first, and quality-gate rules | composed replacement |

## Material revisions and behavior loss

- Root instructions were split by scope so package maintenance authority does
  not leak into initialized research projects.
- The settings conversion deliberately omits `bypassPermissions` and broad
  shell, filesystem, and network allowlists. User/session policy remains
  authoritative.
- Output-style behavior is loaded through relevant skills and portable
  references rather than a provider-specific global style selector.
- The status line does not parse private session serialization, show provider
  model aliases, or estimate context from undocumented files. Codex's visible
  UI and explicit context workflow replace that behavior.
- The quick reference's plan–execute–verify–report loop remains, but deployment
  and other external actions require explicit authorization.

The seven lifecycle-hook surfaces are documented separately in `HOOK_MAP.md`
and included in the same runtime-surface manifest.
