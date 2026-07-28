# Capability ownership contracts

Use this reference to route a mixed task without editing project state.

## Decision rules

1. Resolve higher-authority and project-local instructions first.
2. Split the task into content, verification, transport, and release actions.
3. Assign exactly one primary owner to each dimension.
4. Add contributors only when their input has a distinct purpose.
5. Use an independent verifier for high-risk academic claims or releases.
6. Record a gate for every external or difficult-to-reverse action.
7. Treat an absent, unavailable, or unauthenticated capability as UNVERIFIED.

MAW normally owns scientific validity, source authority, reproducibility, and
academic verification. A project-local capability may specialize those
functions under its subtree. External plugins keep their connectors, personal
style, and operational surfaces.

## Contract schema

```yaml
outcome: "<requested result>"
context:
  project_type: "research | teaching | mixed | unclassified"
  target_path: "<path>"
assignments:
  - dimension: "<bounded task dimension>"
    owner: "<skill, plugin, agent, user, or none>"
    contributors: []
    verifier: "<capability or none>"
    gate: "<authorization or none>"
    evidence: "<instruction, profile, or invocation>"
conflicts:
  - type: "authority | scope | state | safety | format"
    decision: "<resolution or DECISION REQUIRED>"
assumptions: []
execution_order: []
```

The contract is conversational by default. Do not create this YAML unless the
user asks for a file or PAW is authorized to make it durable.

## Teaching example

Request: revise a PT-BR econometrics lecture and email the PDF.

- MAW teaching skills own mathematical accuracy and pedagogy.
- The project-local LaTeX rule owns the build entry point.
- A personal communication capability owns message style.
- The email connector owns transport.
- MAW verifies the final PDF.
- The user gates sending.

## Research example

Request: organize an unstructured Stata/R analysis and share results.

- MAW owns source-role mapping, raw-data immutability, reproducibility, and
  interpretation safeguards.
- Project-local Stata and R instructions own runtime-specific execution.
- A cloud connector may locate files but does not decide which copy controls.
- A disclosure check verifies export safety.
- The user gates synchronization or sharing.
