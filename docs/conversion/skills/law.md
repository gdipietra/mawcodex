# `law` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/law/SKILL.md`

## Intent

LAW specializes project instruction layering: root and nested `AGENTS.md`,
supported project Codex configuration, team versus personal settings, and the
effective precedence for a concrete target path.

## Design decisions

- LAW begins with a read-only instruction graph and exact change plan.
- Root guidance contains project-wide invariants; nested guidance contains
  only material subtree differences.
- PAW profiles remain the source for personalization and ownership facts.
- LAW may update only the shared profile's `instruction_layers` registry when
  it applies an approved layer change.
- Teaching and mixed-language research trees use separate layering patterns.
- Post-change checks include representative subtree and sibling paths.

## Behavior loss or limitations

LAW can only verify configuration fields supported by the active Codex
surface. Inaccessible global instructions or project files make the effective
precedence UNVERIFIED rather than clear.

- Validation: PASS with the official Codex skill structure validator.
