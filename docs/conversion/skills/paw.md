# `paw` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/paw/SKILL.md`

## Intent

PAW maintains a durable project personalization overlay for MAW, including a
complete capability-ownership registry that can name external plugins without
copying their internal settings.

## Design decisions

- `.maw/profile.yaml` stores shared, tracked team/project personalization
  using the canonical ManageRAW schema rather than a parallel PAW schema.
- `.maw/local.yaml` stores gitignored personal or machine-specific settings.
- The profile records differences from the immutable MAW base.
- Material shared-profile revisions receive an evidence-backed PAW history
  record rather than undocumented schema fields.
- Existing LaTeX teaching trees and unorganized Stata/R research projects have
  separate assessment prompts.
- AGENTS.md and Codex configuration layering are delegated to LAW.
- LAW also owns the shared profile's `instruction_layers` registry; PAW owns
  the remaining personalization fields.

## Behavior loss or limitations

PAW does not automatically infer source authority, data sensitivity, build
order, or publication rights. It proposes profile changes and requires user
approval before writing.

- Validation: PASS with the official Codex skill structure validator.
