# `jaw` capability record

- Status: `validated`
- Classification: `native addition`
- Source: original MAW Codex capability; no upstream component
- Target: `skills/jaw/SKILL.md`

## Intent

JAW captures the deployment-readiness knowledge learned while preparing MAW
for new and ongoing academic projects. It assesses a project before any
initializer or project-local control-plane change.

## Design decisions

- Assessment-only behavior is the default.
- Research, teaching, and mixed projects use distinct evidence profiles.
- Existing project instructions, skills, history, source authority, and
  protected material take precedence over a generic scaffold.
- Dependency readiness requires representative forward builds, not version
  discovery alone.
- Plugin-only, thin-profile, selective-merge, and full-initializer options make
  adoption proportional to project maturity.
- Initial shared state uses the ManageRAW profile and lock contract.
- Capability collisions route to CAW, shared configuration to PAW, and
  instruction hierarchy to LAW; JAW stops after onboarding.
- Local integration, environment changes, Git operations, sync, and
  publication remain separate authorization gates.

## Behavior loss or limitations

JAW does not yet provide a universal automated environment doctor. Academic
projects use heterogeneous engines and source roles, so the skill first
discovers project-specific checks and records unavailable checks as
UNVERIFIED.

- Validation: PASS with the official Codex skill validator and MAW package
  structure checks.
