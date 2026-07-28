---
name: translate-to-quarto
description: "Translate a Beamer lecture into a Quarto RevealJS mirror while preserving the Beamer source as the authority, extracting diagrams, mapping citations and environments, rendering both formats, and verifying slide-level parity. Use to create an HTML slide mirror, not to deploy it."
---

# Beamer to Quarto Translation

Create a Quarto mirror without silently changing the authoritative Beamer
source. The requested `.tex` file is the source of truth throughout.

## Contract

- Record the source path and hash before translation.
- Missing compilers, Quarto, diagram extractors, browser inspection, data, or
  bibliography sources make the affected checks `UNVERIFIED`.
- Prefer the project `beamer-translator`; otherwise use a bounded subagent with
  [`beamer-translator.md`](../../references/agent-roles/beamer-translator.md).
- A translation may write the Quarto mirror and its generated local assets.
  Corrections to Beamer require a proposed diff and user approval.
- Commit, push, pull request, web deployment, and publication always require
  explicit authorization.

## Phase 0: Pre-flight

1. Read the complete Beamer source and all included files.
2. Inventory frames, overlays, custom environments, citations, bibliography,
   figures, TikZ blocks, R data/plots, and external assets.
3. Check that the Quarto theme has semantic equivalents for custom
   environments. Add missing local styles before slide translation.
4. Use `$extract-tikz` to regenerate/verify SVGs against the current source.
5. Resolve every citation key and required data file.

Report the source hash, frame count, dependency inventory, available
render/inspection capabilities, and unresolved inputs before translation.

## Phase 1: Create the mirror

Create `Quarto/<lecture>.qmd` with the project's RevealJS configuration,
theme, logo, footer, and bibliography. Add data-loading setup only for files
actually used.

Translate frame by frame:

- preserve mathematical content and citations;
- map one Beamer frame to one logical slide unless an explicit documented
  split is necessary;
- preserve semantic environments rather than visual-only colors;
- retain overlay intent using RevealJS fragments where appropriate;
- reference regenerated SVGs with documented indexing; and
- use interactive plots only when source data and a reproducible construction
  are available; otherwise preserve a static verified figure.

Do not reduce font size to hide layout problems or invent missing source
content.

## Phase 2: Render and parity review

Render the Quarto deck and compile the Beamer source from its unchanged
baseline. Retain logs and inspect every rendered slide in an available browser
or page-image workflow.

Use independent reviewers:

- pedagogy:
  [`pedagogy-reviewer.md`](../../references/agent-roles/pedagogy-reviewer.md);
- parity:
  [`quarto-critic.md`](../../references/agent-roles/quarto-critic.md); and
- proofreading:
  [`proofreader.md`](../../references/agent-roles/proofreader.md).

Check frame/slide mapping, equations, citations, figures, notes, ordering,
semantic environments, and visible overflow. A source-only comparison cannot
PASS visual parity.

## Phase 3: Reconcile

Fix Quarto-only defects and rerender until no Critical/Major parity defect
remains or the iteration cap is reached. If a likely correction belongs in
Beamer, prepare a separate proposed patch and wait for approval; never fold it
silently into translation.

Write a parity report with:

- source and mirror hashes;
- frame-to-slide map;
- render commands and statuses;
- resolved differences;
- intentional documented divergences; and
- `UNVERIFIED` checks.

Update project conversion/session documentation when in scope. Stop before any
deployment or external release.

## Provenance

Native Codex rewrite of the upstream `translate-to-quarto` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
