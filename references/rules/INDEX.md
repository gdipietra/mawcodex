# Rule routing index

Codex plugin references do not auto-apply Claude-style glob frontmatter. The applicable skill or `AGENTS.md` must load every matching rule explicitly.

| Rule | Applies to |
| --- | --- |
| [beamer-quarto-sync](beamer-quarto-sync.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd` |
| [confidential-data](confidential-data.md) | `data/**`, `**/*.dta`, `**/*.sav`, `**/raw/**`, `**/restricted/**`, `**/confidential/**` |
| [content-invariants](content-invariants.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd`, `Quarto/**/*.scss`, `Preambles/header.tex`, `scripts/R/**/*.R` |
| [cross-artifact-review](cross-artifact-review.md) | All academic tasks when relevant |
| [did-conventions](did-conventions.md) | `**/*did*.R`, `**/*did*.do`, `**/*event*study*.R`, `**/*att_gt*.R`, `**/*csdid*.do`, `**/*drdid*`, `scripts/**/*did*.qmd` |
| [exploration-fast-track](exploration-fast-track.md) | `explorations/**` |
| [exploration-folder-protocol](exploration-folder-protocol.md) | `explorations/**` |
| [inference-robustness](inference-robustness.md) | `scripts/**/*.R`, `scripts/**/*.do`, `scripts/**/*.py` |
| [knowledge-base-template](knowledge-base-template.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd`, `scripts/**/*.R` |
| [meta-governance](meta-governance.md) | All academic tasks when relevant |
| [model-routing](model-routing.md) | `.codex/agents/**/*.toml`, `skills/**/SKILL.md` |
| [no-pause-beamer](no-pause-beamer.md) | `Slides/**/*.tex` |
| [orchestrator-protocol](orchestrator-protocol.md) | All academic tasks when relevant |
| [orchestrator-research](orchestrator-research.md) | `scripts/**/*.R`, `explorations/**`, `Figures/**/*.R` |
| [pdf-processing](pdf-processing.md) | `master_supporting_docs/**` |
| [plan-first-workflow](plan-first-workflow.md) | All academic tasks when relevant |
| [post-flight-verification](post-flight-verification.md) | `skills/lit-review/SKILL.md`, `skills/research-ideation/SKILL.md`, `skills/respond-to-referees/SKILL.md`, `skills/review-paper/SKILL.md`, `skills/interview-me/SKILL.md` |
| [prompt-shaping](prompt-shaping.md) | All academic tasks when relevant |
| [proofreading-protocol](proofreading-protocol.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd`, `quality_reports/**` |
| [quality-gates](quality-gates.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd`, `scripts/**/*.R` |
| [r-code-conventions](r-code-conventions.md) | `Figures/**/*.R`, `scripts/**/*.R`, `explorations/**/*.R` |
| [r-package-conventions](r-package-conventions.md) | `R/**/*.R`, `tests/**/*.R`, `man/**/*.Rd`, `vignettes/**`, `DESCRIPTION`, `NAMESPACE`, `NEWS.md` |
| [replication-protocol](replication-protocol.md) | `scripts/**/*.R`, `Figures/**/*.R` |
| [session-logging](session-logging.md) | All academic tasks when relevant |
| [simulation-conventions](simulation-conventions.md) | `**/*simulation*.R`, `**/*_sim.R`, `**/*_mc.R`, `scripts/**/simulations/**`, `explorations/**/*.R` |
| [single-source-of-truth](single-source-of-truth.md) | `Figures/**/*`, `Quarto/**/*.qmd`, `Slides/**/*.tex` |
| [stata-code-conventions](stata-code-conventions.md) | `**/*.do`, `scripts/stata/**` |
| [summary-parity](summary-parity.md) | `CHANGELOG.md`, `README.md`, `**/*.qmd`, `skills/*/SKILL.md`, `references/rules/*.md`, `.codex/agents/*.toml` |
| [tikz-measurement](tikz-measurement.md) | `Slides/**/*.tex`, `Figures/**/*.tex`, `Preambles/**/*.tex`, `scripts/**/*.py`, `scripts/**/*.R` |
| [tikz-prevention](tikz-prevention.md) | `Slides/**/*.tex`, `Figures/**/*.tex`, `Preambles/**/*.tex` |
| [tikz-visual-quality](tikz-visual-quality.md) | `Slides/**/*.tex`, `Figures/**/*.tex` |
| [verification-protocol](verification-protocol.md) | `Slides/**/*.tex`, `Quarto/**/*.qmd`, `docs/**` |
