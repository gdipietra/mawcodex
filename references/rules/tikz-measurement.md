<!-- Native reimplementation of .claude/rules/tikz-measurement.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 d2ab926f23e1af032fb3374608aeb6adca57f51087c1a8c119b63d133a0f83d7. The upstream file credits Scott Cunningham's MixtapeTools; no MixtapeTools text is copied here. -->

# TikZ measurement protocol

## Applicability

Load for TikZ authoring, extraction, and visual review.

## Geometry model

Treat each node as an axis-aligned box after TeX layout. Its usable half-width is `(text width + 2 * inner xsep) / 2`; its usable half-height is `(text height + text depth + 2 * inner ysep) / 2`. For two horizontally adjacent boxes, the clear gap is the center distance minus both half-widths. The vertical formula is analogous.

A label fits in a gap only when its rendered extent plus a safety margin is smaller than that clear gap. Do not infer fit from source character count; compile and measure the rendered result.

## Review procedure

1. Compile a standalone crop with the same fonts and preamble as the target deck.
2. Convert the crop to a high-resolution bitmap or SVG.
3. Inspect every node box, arrow shaft, arrowhead, label, brace, and axis annotation at normal slide scale.
4. For suspected collisions, record the two objects, their measured or estimated extents, the available gap, and the required move.
5. Recompile after the smallest geometry change and compare before and after renders.
6. Verify the exported SVG/PDF has a tight, non-clipping bounding box and remains legible in both Beamer and Quarto.

## Common failure patterns

- wide labels centered between wide boxes;
- timeline labels at adjacent dates with identical vertical offsets;
- labels placed on the inside of curved edges;
- `scale=` shrinking coordinates but not text;
- arrowheads or braces clipped by a tight crop;
- a diagram readable in isolation but too small on the final slide.

A source-only inspection cannot produce a visual PASS. Without a successful compile and rendered inspection, report UNVERIFIED.
