---
name: extract-tikz
description: "Extract TikZ diagrams from Beamer `.tex` source, compile each to a standalone PDF, and convert to SVG with 0-based indexing. Use when user says \"extract the tikz\", \"regenerate the diagrams\", \"rebuild the SVGs\", \"sync tikz to quarto\", or after editing TikZ blocks in a Beamer deck that also has a Quarto mirror."
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

# Extract TikZ Diagrams to SVG

Extract TikZ diagrams from the Beamer source, compile to multi-page PDF, and convert each page to SVG for use in Quarto slides.

> **Creating a new diagram rather than extracting one?** Use
> [`$new-diagram`](../new-diagram/SKILL.md), which scaffolds from
> [`tikz-snippets`](../../assets/templates/tikz-snippets/).

## Steps

### Step 0: Freshness Check (MANDATORY)

**Before compiling, verify that `extract_tikz.tex` matches the current Beamer source.**

1. Resolve the user-supplied lecture identifier to one unambiguous Beamer
   source under `Slides/`; reject path traversal and ask if multiple files match.
2. Extract all `\begin{tikzpicture}` blocks from Beamer
3. Compare with `Figures/<lecture>/extract_tikz.tex`
4. If ANY difference exists: update extract_tikz.tex from the Beamer source
5. If extract_tikz.tex doesn't exist: create it from scratch

### Step 1: Prevention pre-check (MANDATORY — halt on violation)

Before compiling, verify every TikZ block in
`Figures/<lecture>/extract_tikz.tex` against
[`tikz-prevention.md`](../../references/rules/tikz-prevention.md). The
pre-check is shared with `$new-diagram`:

```bash
python scripts/check-tikz-prevention.py "Figures/<lecture>/extract_tikz.tex"
```

What it checks:

- **P3 — `scale=X` without node scaling.** Bare `scale=` shrinks coordinates but not text. Allowed forms: `scale=X, every node/.style={scale=X}` or `scale=X, transform shape`. The checker parses the full `\begin{tikzpicture}[...]` options block even when it spans multiple lines.
- **P4 — Directional keyword on edge labels.** Every edge label (`node` inside a `\draw`) must carry `above`, `below`, `left`, `right`, or a compound (e.g. `above left`). `midway` alone is a path position, not a direction. The checker scans the full `\draw ...;` statement so `\draw` on one line and `node[...]{...}` on the next line are still linked.

Note what the pre-check does NOT enforce: P1 (boxed-node explicit dimensions) and P2 (coordinate-map comment) are structural and get flagged by `tikz-reviewer` in Step 8, not here.

Exit codes: `0` = all files pass, `1` = one or more P3/P4 violations (stderr lists file, line, snippet, rule), `2` = usage error.

If exit is non-zero: halt, report the offending lines, and ask the user to fix the Beamer source (single source of truth). Do NOT compile.

### Step 2: Navigate to the lecture's Figures directory
```bash
cd Figures/<lecture>
```

### Step 3: Compile the extract_tikz.tex file
```bash
xelatex -interaction=nonstopmode extract_tikz.tex
```

Configure the TeX input path to include `../../Preambles/` while preserving the
existing path, using syntax appropriate to the current shell.

### Step 4: Count the number of pages
```bash
pdfinfo extract_tikz.pdf | grep "Pages:"
```

### Step 5: Convert each page to SVG using 0-BASED INDEXING

**CRITICAL: PDF pages are 1-indexed, but output SVG files are 0-indexed!**

Read the page count from `pdfinfo`. For each PDF page `p` from 1 through the
page count, call `pdf2svg` with page `p` and write
`tikz_exact_<p-minus-one, zero-padded-to-two-digits>.svg`. For example, PDF
page 1 becomes `tikz_exact_00.svg`.

### Step 6: Sync to docs/ for deployment
```bash
scripts/sync_to_docs.sh <lecture>
```

Inspect the sync script first. This step updates the local publication tree
only; it does not authorize commit, push, or live deployment.

### Step 7: Verify SVG files
- Confirm every expected SVG exists, is non-empty, and has valid SVG markup.
- Render or open representative SVGs with a visual capability; markup alone is
  not a visual PASS.
- Reconcile the PDF-page-to-zero-based-filename map and record it.

### Step 8: Visual Quality Review (tikz-reviewer)

Use the project `tikz-reviewer` custom agent, or a bounded isolated subagent
following
[`tikz-reviewer.md`](../../references/agent-roles/tikz-reviewer.md), to inspect
the TikZ source and rendered output. It must use
[`tikz-measurement.md`](../../references/rules/tikz-measurement.md) and cite
specific evidence. If it returns NEEDS REVISION or REJECTED, loop:

1. Apply the recommended fixes to the Beamer `.tex` source (single source of truth).
2. Re-copy the updated block to `extract_tikz.tex`.
3. Re-run the prevention pre-check (Step 1) and compile.
4. Regenerate SVGs, re-sync.
5. Re-invoke tikz-reviewer.

Stop when tikz-reviewer returns **APPROVED** (max 5 rounds).

### Step 9: Report results

Report source path, diagram count, PDF page count, output mapping, prevention
check, compile result, pages/SVGs visually inspected, reviewer verdict, sync
result, and any UNVERIFIED capability. Missing XeLaTeX, `pdfinfo`, `pdf2svg`,
visual inspection, or reviewer capability prevents an overall PASS.

## Source of Truth Reminder
TikZ diagrams must be edited in the Beamer `.tex` source first, then copied
verbatim to `extract_tikz.tex`. See
[`single-source-of-truth.md`](../../references/rules/single-source-of-truth.md).
