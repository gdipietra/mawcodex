# Agent portability map

All 18 source agent conversions are `composed replacement`: each source role maps to
both a project custom-agent TOML and a portable role Markdown file. The
per-component source/target hashes and revision summaries are recorded in
`SOURCE_MANIFEST.json`.

| Upstream role | Codex custom agent | Sandbox | Status |
| --- | --- | --- | --- |
| `beamer-translator` | `beamer_translator` | `workspace-write` | `validated` |
| `claim-verifier` | `claim_verifier` | `read-only` | `validated` |
| `domain-referee` | `domain_referee` | `read-only` | `validated` |
| `domain-reviewer` | `domain_reviewer` | `read-only` | `validated` |
| `editor` | `editor` | `read-only` | `validated` |
| `humanize-auditor` | `humanize_auditor` | `read-only` | `validated` |
| `methods-referee` | `methods_referee` | `read-only` | `validated` |
| `pedagogy-reviewer` | `pedagogy_reviewer` | `read-only` | `validated` |
| `promote-memory-council` | `promote_memory_council` | `read-only` | `validated` |
| `proofreader` | `proofreader` | `read-only` | `validated` |
| `quarto-critic` | `quarto_critic` | `read-only` | `validated` |
| `quarto-fixer` | `quarto_fixer` | `workspace-write` | `validated` |
| `r-package-reviewer` | `r_package_reviewer` | `workspace-write` | `validated` |
| `r-reviewer` | `r_reviewer` | `read-only` | `validated` |
| `sim-reviewer` | `sim_reviewer` | `read-only` | `validated` |
| `slide-auditor` | `slide_auditor` | `read-only` | `validated` |
| `tikz-reviewer` | `tikz_reviewer` | `read-only` | `validated` |
| `verifier` | `verifier` | `workspace-write` | `validated` |

## Native control-plane agent

| Native role | Codex custom agent | Sandbox | Status |
| --- | --- | --- | --- |
| ManageRAW | `manageraw` | `workspace-write` | `validated` |

The packaged inventory is therefore 19 custom agents and 19 portable roles:
18 source-derived pairs plus the native ManageRAW pair. Its separate design
record is [`agents/manageraw.md`](agents/manageraw.md).
