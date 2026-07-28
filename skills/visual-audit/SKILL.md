---
name: visual-audit
description: "Perform an adversarial visual-layout audit of a Quarto or Beamer slide deck, checking every rendered slide for overflow, clipping, font inconsistency, box fatigue, spacing, alignment, contrast, and legibility. Use for layout review; not writing, pedagogy, or subject-matter review."
---

# Visual Audit of a Slide Deck

Visual claims require rendered evidence. Source inspection and compiler warnings
are useful diagnostics but cannot by themselves establish a visual PASS.

## Contract

- Require one unambiguous `.qmd` or `.tex` deck path.
- Record source hash, render command, renderer version, exit status, and output
  path.
- If rendering or page-by-page visual inspection is unavailable, write a
  source-only diagnostic labeled `UNVERIFIED`.
- Prefer the project `slide-auditor`; otherwise use a bounded reviewer with
  [`slide-auditor.md`](../../references/agent-roles/slide-auditor.md).
- Review only; do not edit or deploy unless separately requested.

## Workflow

1. Read the complete source and inventory slides, figures, custom styles,
   inline size overrides, and likely overflow hotspots.
2. Render Quarto with the project's configured command or compile Beamer using
   its documented build path. Retain errors, warnings, and overfull/underfull box
   messages.
3. Inspect every rendered slide in a browser, PDF-page image, or equivalent
   visual workflow. Record slide number/title and screenshot/page evidence for
   material findings.
4. Audit:
   - content outside bounds, clipping, overlap, and cut-off fragments;
   - font hierarchy, minimum legibility, and inconsistent overrides;
   - repeated colored-box fatigue and inappropriate semantic box types;
   - vertical/horizontal spacing and figure alignment;
   - grid alignment, margins, whitespace, and transition structure;
   - contrast, color meaning, and grayscale/accessibility risks; and
   - equations, tables, citations, and labels at presentation distance.
5. Write `quality_reports/<deck>_visual_audit.md` with a per-slide table:

```markdown
| Slide | Severity | Evidence | Issue | Recommended fix | Status |
```

Classify `Critical`, `Major`, or `Minor`; include a clean-slide count and list
all uninspected slides.

## Fix order

Recommend changes in this order:

1. reduce unnecessary vertical spacing;
2. consolidate or split overloaded lists;
3. move suitable displayed equations inline;
4. resize/recompose figures or tables;
5. split the slide while preserving narrative; and
6. only as a last resort reduce font size, never below the project's minimum
   (and not below `0.85em` absent a stricter project rule).

The final verdict is `PASS`, `FAIL`, or `UNVERIFIED`. PASS requires successful
rendering, every slide inspected, and no unresolved Critical/Major issue. Use
`$proofread` for language and `$pedagogy-review` for teaching structure.

## Provenance

Native Codex rewrite of the upstream `visual-audit` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
