# `translate-to-quarto` conversion

- Status: `forward-tested`
- Classification: `composed replacement`
- Source: `.claude/skills/translate-to-quarto/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `d77c0e80eec0f73121bbc78d67c43561aef1aa217924e1dacde69957610d59a8`
- Target: `skills/translate-to-quarto/SKILL.md`
- Target SHA-256: `31ac4d8b928a99268810b5f8b35a13ca556bd5150d236bbaafd9b8d9e9b0ac7e`
- Validation: `PASS`
- Forward test: PASS (FT-08)
## Material revisions

- Mapped translation, pedagogy, parity, and proofreading to Codex custom-agent
  roles with portable fallbacks.
- Made source hashes, complete dependency inventory, dual rendering, and
  page-by-page visual inspection explicit.
- Changed automatic Beamer sync and deployment into proposed, user-authorized
  actions.

## Behavior preserved

Beamer remains the source of truth; environment, TikZ, data, citation, slide
mapping, parity, render, and documentation phases remain.

## Behavior loss or limitation

No deployment is bundled, and Beamer corrections are no longer silently
back-propagated. A real paired-deck forward test remains pending.
