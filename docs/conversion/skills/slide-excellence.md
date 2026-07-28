# `slide-excellence` conversion

- Status: `validated`
- Classification: `composed replacement`
- Source: `.claude/skills/slide-excellence/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `620729704ce6b6bd1537c6b21fe8e74d86722f98ba823fc16132842f8b71d1d5`
- Target: `skills/slide-excellence/SKILL.md`
- Target SHA-256: `1cac123d3e9178066348726f24f91027d46b8b93a946348ab12f876c4a608f3b`
- Validation: `PASS`
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Replaced conditional Claude agent dispatch with project-agent/portable-role
  routing in isolated contexts.
- Made rendering and page-by-page inspection mandatory for visual PASS.
- Replaced false-precision score thresholds with evidence-based readiness and
  explicit required-lens UNVERIFIED behavior.

## Behavior preserved

Visual, pedagogy, proofread, TikZ, parity, R, and domain lenses still dispatch
only when relevant, with a mandatory domain-template gate.

## Behavior loss or limitation

Fast mode no longer claims equivalence to independent fanout. A rendered
multi-agent deck review remains pending.
