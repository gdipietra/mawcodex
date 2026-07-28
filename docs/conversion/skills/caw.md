# `caw` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/caw/SKILL.md`

## Intent

CAW coordinates ownership when MAW coexists with project-local capabilities,
other plugins, skills, or connectors. It separates academic content,
verification, transport, and release actions instead of imposing a fictitious
global plugin priority.

## Design decisions

- Routing is read-only and produces a compact execution contract.
- MAW owns academic validity and reproducibility only within its scope.
- External plugins retain their connector, personal-style, and operational
  responsibilities.
- Explicit invocation, project instructions, scientific safeguards, and user
  authorization remain distinct signals.
- Durable ownership changes are handed to PAW.

## Behavior loss or limitations

CAW cannot inspect undocumented plugin internals or create a runtime-wide
plugin precedence stack. Unavailable capabilities are reported as UNVERIFIED,
and material unresolved choices return to the user.

- Validation: PASS with the official Codex skill structure validator.
