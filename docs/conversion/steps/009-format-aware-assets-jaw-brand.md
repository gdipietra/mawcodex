# Step 009 — Format-aware assets, JAW, and MAW identity

Date: 2026-07-28

## Scope

This revision promotes the package from `1.0.0` to `1.1.0`. It repairs
executable project assets, adds safe adoption guidance for ongoing projects,
and introduces the original MAW visual identity.

## Translation revision

The upstream Beamer sample used slash-command text such as
`/compile-latex`. A mechanical conversion changed this to `$compile-latex`
inside `\texttt{}`, where TeX interpreted the dollar sign as math mode.

The project-template importer now:

1. converts Claude slash invocations to Codex `$skill` invocations;
2. escapes the sigil as `\$skill` only in typeset TeX content;
3. leaves TeX comments readable and leaves Quarto code spans unescaped;
4. records the contextual TeX operation in project-manifest schema 2 so the
   target can be reproduced from the fixed source, not merely hash-matched.

Shared-template provenance is also extension-aware: TeX uses `%`, YAML uses
`#`, and Markdown uses HTML comments.

## JAW capability

`skills/jaw/` is an original Codex-native addition, not a migrated upstream
component. It defaults to a read-only assessment and distinguishes research,
teaching, and mixed projects. It evaluates source authority, protected
material, collisions, real dependency behavior, proportional integration,
user decisions, verification, and rollback before any MAW files are applied.

The package inventory is therefore 53 skills: 52 source-derived skills plus
JAW. The fixed upstream source manifest remains correctly bounded at 52.

## Visual identity

`assets/brand/` contains an original icon, 16:9 plugin thumbnail, and academic
Codex-pet illustration based on Giovanni Di Pietra's supplied sketch. The
plugin and JAW interface metadata reference these assets. The brand record
documents the palette, generation method, and original-design boundary.

## Verification evidence

- Official plugin validator: PASS.
- Official skill validator: 53/53 PASS.
- Deterministic unit tests: 37/37 PASS.
- Imported project provenance: 18/18 assets reproducible from the fixed
  source and recorded transformations.
- Corrected Beamer sample: XeLaTeX pass, BibTeX pass, two additional XeLaTeX
  passes, no unresolved citation/reference/control-sequence markers.
- Rendered Beamer slide visually shows literal `$compile-latex` and
  `$translate-to-quarto` commands.
- TikZ templates: 8/8 standalone XeLaTeX compiles PASS; representative
  event-study output visually inspected.
- Quarto sample: Reveal render PASS; generated HTML preserves literal
  `$deploy HelloWorld` code spans.
- Complete stable-release gate: 13/13 PASS.

Isolated forward-build evidence is under
`tmp/dependency-audit/format-recheck-20260728a/` and is excluded from the
release snapshot.
