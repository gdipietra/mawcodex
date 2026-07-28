<!-- Adapted from .claude/rules/tikz-visual-quality.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 21d0ec7a1c10b716b8cf284de56408aea7c3b348754de378cdc3160ab7fe38a9. -->

## Applicability

Load this rule for: `Slides/**/*.tex`, `Figures/**/*.tex`.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# TikZ Visual Quality Standards

**Every TikZ diagram must be visually polished before it is considered complete.**

## Label Positioning

- Labels must NEVER overlap with curves, lines, dots, braces, or other labels
- When two labels are near the same vertical position, stagger them
- Group labels: right of final data point
- Axis labels: at arrow tips
- Annotation labels: adjacent to braces/arrows, outside data area
- Use consistent font size

## Visual Semantics

- **Solid dots/lines** = observed outcomes, realized paths
- **Hollow circles/dashed lines** = counterfactual outcomes, unrealized paths
- Use consistent colors for semantic meaning (positive, negative, neutral)
- Define colors in your Beamer theme for reuse

### Line Weights
- Axes: `thick`
- Data lines: `thick`
- Annotation arrows: `thick` (NOT `very thick`)
- Grid/reference lines: `dashed, gray!40`

## Spacing and Proportions

- Standard scale: `[scale=1.1, every node/.style={scale=1.1}]` for full-width diagrams — always scale nodes together with coordinates (bare `[scale=X]` is banned by [`tikz-prevention.md` P3](tikz-prevention.md) because it shrinks coordinates but not text)
- Dot radius: `4pt` for data points
- Minimum 0.2 units between any label and nearest graphical element
- Axes extend beyond all data points

## Checklist

```
[ ] No label-label overlaps
[ ] No label-curve overlaps
[ ] Consistent dot style (solid=observed, hollow=counterfactual)
[ ] Consistent line style (solid=observed, dashed=counterfactual)
[ ] Color semantics correct
[ ] Arrow annotations point FROM label TO feature
[ ] Axes extend beyond all data points
[ ] Labels legible at presentation size
```

## Single Source of Truth

**The Beamer `.tex` file is the authoritative source for ALL TikZ diagrams.**
Edit TikZ in the Beamer file FIRST, then copy verbatim to `extract_tikz.tex`.
