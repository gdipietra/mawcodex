# Source baseline

| Field | Value |
| --- | --- |
| Upstream repository | `https://github.com/pedrohcgs/claude-code-my-workflow` |
| User fork | `https://github.com/dipietra/claude-code-my-workflow` |
| Local clone | `C:\GitHub\claude-code-my-workflow` |
| Branch | `main` |
| Release | `v2.1.0` |
| Commit | `be53c12f235996dff41fb7f21580506fd2dd8d50` |
| Commit date | `2026-06-10T14:20:18-04:00` |
| Baseline fixed | `2026-07-28` |
| License | MIT |

## Initial Claude artifact inventory

| Surface | Count | Codex target |
| --- | ---: | --- |
| Skills | 52 | `skills/*/SKILL.md` |
| Agents | 18 | `.codex/agents/*.toml` and `references/agent-roles/*.md` |
| Rules | 32 | `references/rules/*.md`, routed through skills and `AGENTS.md` |
| Lifecycle hooks | 7 | `hooks/hooks.json` plus adapted scripts or documented replacement |
| Root instructions | 1 | `AGENTS.md` |
| Settings | 1 | safe `.codex/config.toml`; permission bypass deliberately omitted |
| Output styles | 2 | portable writing/review skills, rules, and roles |
| Status-line script | 1 | Codex UI plus `$context-status` and compaction state |
| Workflow quick reference | 1 | `AGENTS.md`, README, plan-first, and quality-gate rules |

The 132 core component records are in `SOURCE_MANIFEST.json`. The 7 hooks and
6 other provider runtime surfaces are separately hash-bound in
`RUNTIME_SURFACES_MANIFEST.json`. Project imports cover 18 more source files,
and `AUXILIARY_SOURCE_MANIFEST.json` gives each of the remaining 48 repository
support files an explicit disposition. Together the manifests cover all
211/211 files tracked at the fixed commit.

## Source validator result

The upstream `scripts/validate-setup.sh` was run from the fixed clone on
2026-07-28.

- Passed: XeLaTeX, Quarto, Git, Git identity, executable Claude hook scripts,
  executable Git pre-commit gate.
- Warnings: optional R and GitHub CLI were not visible to Git Bash; the
  pre-commit gate was not activated; the palette wrapper could not run.
- Failed: Claude Code was not installed; Git Bash could not find a `python3`
  command.

The Claude failure is expected and defines the main migration requirement. The
Python result is a shell-discovery issue: Codex provides a bundled Python
runtime, which MAW Codex validation will locate explicitly.
