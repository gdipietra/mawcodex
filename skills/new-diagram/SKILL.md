---
name: new-diagram
description: "Create or adapt a standalone TikZ diagram from the packaged snippet gallery, enforce coordinate and edge-label prevention rules, compile it, inspect the rendered result, and iterate with an independent TikZ reviewer. Use when a user asks for a new causal diagram, timeline, event-study figure, flowchart, supply-demand diagram, or other TikZ visual. Never overwrite an existing target without confirmation."
---

# New Diagram

Start from a tested snippet instead of writing TikZ from a blank file. Preserve
the upstream workflow's core guarantees: explicit geometry, prevention checks,
standalone compilation, visual inspection, and a bounded critic/fix loop.

## Inputs

- A snippet name, if the user has one in mind.
- An output path; default to `Figures/new_diagram.tex`.
- A plain-language statement of what the diagram must communicate.

The packaged gallery is expected at
`../../assets/templates/tikz-snippets/`. Typical snippets include
`dag-basic`, `dag-mediation`, `did-two-period`, `event-study`, `timeline`,
`regression-scatter`, `flowchart-3step`, and `supply-demand`.

If the gallery or requested snippet is unavailable, list the available assets
and ask the user whether to choose one or authorize a new design. Mark the
snippet baseline `UNVERIFIED`; do not silently substitute a different visual.

## Workflow

### 1. Resolve the source and target

1. List actual `.tex` snippets in the gallery.
2. If no snippet was specified, show the choices and ask.
3. Resolve the output path to an absolute path inside the authorized
   workspace.
4. If the target exists, stop and ask whether to overwrite, create a variant,
   or cancel. Preserve the existing version when requested.

### 2. Adapt the snippet

Copy the chosen snippet, then change only what the user's intent requires:

- update the intent comment at the top;
- keep the coordinate-map comment synchronized with geometry;
- rename nodes and labels;
- retain tested node styles unless the semantic role changes;
- give nodes explicit dimensions where the prevention rules require them;
- give every new edge label an explicit direction such as `above`, `below`,
  `left`, or `right`.

Do not add a bare `scale=<x>` that shrinks coordinates but not node contents.
If scaling is necessary, use a form that also transforms nodes. Follow:

- [`tikz-prevention.md`](../../references/rules/tikz-prevention.md)
- [`tikz-visual-quality.md`](../../references/rules/tikz-visual-quality.md)

### 3. Run deterministic prevention checks

Run the repository's TikZ prevention checker against the target:

```text
python scripts/check-tikz-prevention.py <target.tex>
```

Resolve the actual Python launcher for the environment. Treat:

- exit `0` as structural prevention `PASS`;
- exit `1` as reported violations to fix and rerun;
- missing script, Python, or unsupported invocation as `UNVERIFIED`.

Do not replace an unavailable checker with an improvised regular expression
and call it equivalent.

### 4. Compile standalone

Run `xelatex -interaction=nonstopmode <target.tex>` from the target directory,
capture the log to a task-specific temporary file, and check:

- process exit code;
- non-empty PDF;
- page count;
- compilation warnings relevant to clipping or missing fonts.

If XeLaTeX or required packages are unavailable, report compilation
`UNVERIFIED` and provide the exact next check. Do not claim the diagram passes.

### 5. Inspect and review

Render the PDF page to an image when possible and inspect it. Then prefer the
project `tikz-reviewer` custom agent; otherwise spawn a bounded, read-only
subagent in an isolated context using
[`tikz-reviewer.md`](../../references/agent-roles/tikz-reviewer.md). Give it:

- the intent sentence;
- the `.tex` source;
- the compiled PDF or page image;
- the measurement rules in
  [`tikz-measurement.md`](../../references/rules/tikz-measurement.md).

Require every critical or major finding to name the applicable pass or formula
and a precise location. Reject vague findings.

For `NEEDS REVISION` or `REJECTED`, fix the target, rerun prevention, recompile,
and re-review. Converge when no new critical or major findings appear and all
hard visual gates pass. Cap the loop at five rounds; then report remaining
issues to the user rather than continuing indefinitely.

### 6. Optional SVG

When the user needs Quarto output and `pdf2svg` is available, convert the
single-page PDF to an SVG with the same basename. Verify that the SVG is
non-empty and visually consistent. A missing converter makes SVG output
`UNVERIFIED`, not the PDF itself.

### 7. Clean and report

Remove only build intermediates derived from this target's basename, such as
its `.aux`, `.log`, `.out`, and `.synctex.gz`. Never use a broad deletion that
could remove another document's artifacts.

Report the snippet, output paths, structural check, compile status, reviewer
verdict and rounds, PDF page count, and optional SVG status.

## Boundaries

- Use $extract-tikz to extract diagrams from an existing Beamer deck.
- This skill creates local assets only. It does not commit, publish, or insert
  the diagram into another document unless the user explicitly requests that
  additional change.
