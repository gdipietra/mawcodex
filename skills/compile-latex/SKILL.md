---
name: compile-latex
description: "Compile a Beamer LaTeX slide deck with XeLaTeX (3 passes + bibtex). Use when user says \"compile\", \"build the slides\", \"rebuild the PDF\", \"run latex\", \"render the tex\", or asks why a `.tex` file isn't producing a PDF. Operates on `Slides/*.tex`."
---

## Codex execution contract

- Treat the user's request and applicable `AGENTS.md` files as authoritative.
- Resolve referenced resources relative to this skill first.
- Use bounded, isolated subagents for independent review roles; when a
  project custom agent is unavailable, use the matching portable role in
  `../../references/agent-roles/`.
- Treat missing tools, inaccessible sources, and skipped checks as
  UNVERIFIED rather than PASS.
- Require explicit user authorization for commit, push, merge, deploy,
  submission, sending, or other external publication.

# Compile Beamer LaTeX Slides

Compile a Beamer slide deck using XeLaTeX with full citation resolution.

## Steps

1. Resolve the requested deck name to one unambiguous file under `Slides/`.
   Reject path traversal and ask if more than one file matches.
2. Read the deck and project configuration to confirm the required engine and
   bibliography backend. Default to XeLaTeX plus BibTeX only when the project
   does not declare otherwise.
3. From `Slides/`, compile with the resolved deck basename:

```bash
xelatex -interaction=nonstopmode <deck>.tex
bibtex <deck>
xelatex -interaction=nonstopmode <deck>.tex
xelatex -interaction=nonstopmode <deck>.tex
```

**Alternative (latexmk):**
```bash
latexmk -xelatex -interaction=nonstopmode <deck>.tex
```

Set `TEXINPUTS` to include `../Preambles/` and `BIBINPUTS` to include the
repository root using syntax appropriate to the current shell. Preserve the
existing search path rather than overwriting it.

4. **Check the log:**
   - Search for `Overfull \\hbox` warnings and report their measured overflow.
   - Search for undefined citations, undefined references, missing files, and
     rerun warnings.
   - Report any issues found

5. **Visually verify the PDF.** Render representative pages with the available
   PDF capability and inspect them for clipping, overflow, missing glyphs,
   broken figures, and blank pages. Do not treat compilation alone as visual
   PASS.

6. **Report results:**
   - Compilation success/failure
   - Number of overfull hbox warnings
   - Any undefined citations
   - PDF page count
   - Pages inspected and any visual defects

If XeLaTeX, the bibliography backend, PDF inspection, or page-count tooling is
unavailable, identify the missing capability and mark that portion UNVERIFIED.

## Why 3 passes?
1. First xelatex: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: Incorporates bibliography
4. Third xelatex: Resolves all cross-references with final page numbers

## Important
- Use XeLaTeX for this workflow unless the deck's authoritative project
  configuration explicitly selects a different engine.
- **TEXINPUTS** is required: your Beamer theme lives in `Preambles/`
- **BIBINPUTS** is required: your `.bib` file lives in the repo root
