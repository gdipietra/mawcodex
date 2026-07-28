---
name: slide-excellence
description: "Orchestrate a comprehensive slide-deck review using independent visual, pedagogy, proofreading, and conditionally relevant TikZ, parity, R-code, and subject-matter lenses. Use before teaching or releasing a Beamer, Quarto, or Markdown deck; use a single-lens skill for a narrower audit."
---

# Slide Excellence Review

Fan out only to reviewers that can produce evidence for the detected deck.
Render-based claims require inspection of rendered output; source inspection
alone is not a visual PASS.

## Inputs and contract

- Require one `.tex`, `.qmd`, or slide-oriented `.md` path.
- Resolve paths explicitly; do not guess between multiple matches.
- Reviewers operate in separate bounded contexts and write typed findings.
- Prefer project custom agents. If unavailable, use the corresponding role in
  `../../references/agent-roles/`.
- Missing compilers, renderers, browsers, counterparts, or runtimes make only
  the affected lens `UNVERIFIED`; do not convert a skipped lens into zero
  findings.
- This skill reviews and writes reports. It does not publish or deploy.

## Phase 0: Detect conditions

Inspect the source and report:

- type: Beamer, Quarto RevealJS, or Markdown;
- TikZ block count;
- paired Beamer/Quarto counterpart, if uniquely identifiable;
- embedded or referenced R code;
- available render/compile and visual-inspection capabilities; and
- existing same-source reports that could be reused.

Offer reuse only when the prior report records the same source hash and relevant
configuration.

## Domain-review gate

For a Beamer deck, subject-matter review is required unless the user explicitly
chooses `--skip-substance`. Check the project `domain-reviewer` definition and
[`domain-reviewer.md`](../../references/agent-roles/domain-reviewer.md) for
template markers or generic placeholders. If not customized, stop before fanout
and ask the user to customize it, skip substance, or explicitly accept a generic
review. Never silently present generic feedback as field-specific validation.

## Conditional review plan

Run independent reviews in parallel when capacity allows:

| Lens | Condition | Portable role | Output suffix |
| --- | --- | --- | --- |
| Visual/layout | always | [`slide-auditor`](../../references/agent-roles/slide-auditor.md) | `_visual_audit.md` |
| Pedagogy | always | [`pedagogy-reviewer`](../../references/agent-roles/pedagogy-reviewer.md) | `_pedagogy_report.md` |
| Proofreading | always | [`proofreader`](../../references/agent-roles/proofreader.md) | `_proofread_report.md` |
| TikZ | TikZ present | [`tikz-reviewer`](../../references/agent-roles/tikz-reviewer.md) | `_tikz_review.md` |
| Cross-format parity | counterpart found | [`quarto-critic`](../../references/agent-roles/quarto-critic.md) | `_parity_report.md` |
| R code | R present | [`r-reviewer`](../../references/agent-roles/r-reviewer.md) | `_r_review.md` |
| Substance | gated as above | [`domain-reviewer`](../../references/agent-roles/domain-reviewer.md) | `_substance_review.md` |

Each reviewer receives the source path, source hash, rendered artifact where
applicable, its single lens, and a unique report path under `quality_reports/`.
Every Critical/Major finding needs a location, evidence, consequence, and
recommended fix.

With `--fast`, use one bounded reviewer across the applicable lenses and state
that independence was not tested. Do not call this equivalent to full fanout.

## Render and inspect

Compile Beamer and retain warnings/logs. Render Quarto and inspect every slide
through an available browser or page-image workflow. When layout cannot be
visually inspected, visual, TikZ, and parity conclusions are `UNVERIFIED`.

## Synthesis

Reduce the typed findings without rereviewing or averaging skipped lenses.
Write `quality_reports/<file>_slide_excellence.md`:

```markdown
# Slide Excellence Review: [file]
**Source hash:** [...]
**Detected:** TikZ=N · pair=[path/none] · R=[yes/no]
**Lenses:** [PASS/FAIL/UNVERIFIED and report path]

## Readiness: READY / REVISE / BLOCKED / UNVERIFIED
## Critical issues
## Major issues
## Cross-lens conflicts
## Recommended next steps
```

`READY` requires no unresolved Critical/Major finding and no required
unverified lens. Report observed reviewer count and elapsed time only when
measured; avoid fabricated token/cost estimates.

Use `$visual-audit`, `$pedagogy-review`, or `$proofread` for one lens and
`$qa-quarto` for an iterative Beamer–Quarto parity loop.

## Provenance

Native Codex rewrite of the upstream `slide-excellence` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
