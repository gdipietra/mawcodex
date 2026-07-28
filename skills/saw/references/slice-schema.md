# SAW slice schema

Use these fields as a semantic schema. Follow the manager workflow's current
serialization format when it defines one.

## Project-return slice

```yaml
slice_kind: project-return
schema_version: 1
generated_at: YYYY-MM-DDTHH:MM:SSZ
evidence_cutoff: YYYY-MM-DDTHH:MM:SSZ
maw_base:
  version: value
  identity: safe immutable identifier
project:
  class: teaching | research | mixed
  language_roles: []
layers:
  shared: []
  personal_roles: []
instruction_scopes: []
capabilities:
  active: []
  preferred: []
  replaced: []
  intentionally_unused: []
ownership: []
source_roles: []
protected_roles: []
validation_summary: []
manager_decisions: []
unresolved: []
next_review_trigger: value
omissions: []
evidence: []
```

Do not place personal-layer values in the slice. Record only that a safe local
override exists and which non-sensitive behavior category it controls.

## Upstream-learning slice

```yaml
slice_kind: upstream-learning
schema_version: 1
generated_at: YYYY-MM-DDTHH:MM:SSZ
maw_base:
  version: value
candidates:
  - candidate_id: stable local identifier
    intent: value
    problem_pattern: value
    affected_surface: value
    proposed_general_behavior: value
    applies_to: teaching | research | both
    evidence_class: observed | declared
    independent_occurrences: number
    safety_constraints: []
    migration_risks: []
    status: observe | evaluate | propose | reject
omissions: []
```

The upstream-learning slice must not contain the project name, local path,
repository URL, institution, collaborators, course identifiers, data
descriptions, substantive findings, or verbatim project content.

## Evidence records

Use safe evidence records:

```yaml
- class: observed | declared | inferred
  source_role: profile | lock | manager-history | instruction | build-evidence
  relative_scope: safe project-relative scope or logical role
  supports: item identifier
  recorded_at: timestamp or unknown
```

Do not include raw excerpts when a structural fact or digest is sufficient.
Do not export transcript identifiers or reconstruct decisions from private
conversation history.

## Sanitization checklist

Before previewing either slice, reject or transform:

- absolute paths and machine-specific environment values;
- usernames, email addresses, remote URLs, tokens, credentials, and connector
  metadata;
- raw, derived, restricted, licensed, or student data;
- estimates, unpublished claims, idea text, manuscript passages, assessment
  content, solutions, and code bodies;
- command arguments containing paths, secrets, or private identifiers;
- external-plugin configuration beyond recorded ownership;
- inferred usage presented as confirmed history.

For teaching projects, safe examples include `latex_engine: xelatex`,
`working_language: pt-BR`, and `solutions: protected-separate-role`. For
research projects, safe examples include `runtime_mix: [stata, r]`,
`raw_data: immutable-role`, and `pipeline_status: partially-mapped`.
