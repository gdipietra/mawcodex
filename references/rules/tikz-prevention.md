<!-- Native reimplementation of .claude/rules/tikz-prevention.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 1266134d81547e3f81ade63c8d8aa187b9e0972c30266f33ceda3235769a46a3. The upstream file credits Scott Cunningham's MixtapeTools; no MixtapeTools text is copied here. -->

# TikZ defect-prevention rules

## Applicability

Load for `Slides/**/*.tex`, `Figures/**/*.tex`, and `Preambles/**/*.tex`.

## P1 — Size boxed nodes explicitly

For rectangles, circles, and callouts, set a text width or minimum width plus a minimum height. Account for inner separation. Do not let a long label silently determine geometry shared with other nodes.

## P2 — Declare a coordinate map

Before drawing, list the important node centers or axis coordinates and the intended horizontal and vertical gaps. Reuse named coordinates instead of duplicating numeric positions.

## P3 — Scale shapes and text together

Avoid a bare `scale=` on a `tikzpicture`; it changes coordinates without necessarily scaling node text. Use `transform shape`, or prefer explicit dimensions and coordinates.

## P4 — Place edge labels deliberately

Every non-trivial edge label states a side such as `above`, `below`, `left`, or `right`, plus a position when the midpoint is crowded. For curved edges, put the label on the outside of the bend.

## P5 — Keep one visual claim per picture

Split overloaded diagrams into separate frames or subfigures. Avoid overlay conditionals that make bounding boxes unpredictable.

## Preflight

1. Inspect node dimensions and coordinate gaps.
2. Flag bare `scale=` without `transform shape`.
3. Flag labeled edges with no directional placement.
4. Compile standalone with the project preamble.
5. Render to an image and run the `tikz_reviewer` role.
6. Treat a skipped compile or render as UNVERIFIED.

The packaged snippets in `assets/templates/tikz-snippets/` are starting points, not proof that a modified diagram is collision-free.
