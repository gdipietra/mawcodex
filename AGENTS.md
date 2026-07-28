# MAW Codex repository instructions

## Mission

Build and maintain a Codex-native academic-workflow package. Preserve the
substantive intent of Pedro H. C. Sant'Anna's
`claude-code-my-workflow` while replacing Claude-specific execution surfaces
with current Codex primitives.

## Source boundary

- The immutable conversion baseline is
  `C:\GitHub\claude-code-my-workflow` at the commit recorded in
  `docs/conversion/SOURCE_BASELINE.md`.
- Never edit the source clone as part of a conversion. Update it only through
  the documented upstream-sync procedure and only when the user asks to sync.
- All adapted implementation belongs in `C:\Codex\mawcodex`.
- Preserve upstream and third-party attribution. Do not copy a component whose
  redistribution terms are unclear; record it as blocked or reimplement its
  behavior from public specifications.

## Priorities

When priorities conflict, use this order:

1. Scientific validity and research ethics.
2. Reproducibility and provenance.
3. Confidentiality and disclosure control.
4. Behavioral fidelity to the upstream workflow.
5. Clear, maintainable Codex-native design.
6. Speed.

## Operating modes

- **Orient:** inspect only; identify source-of-truth files, data sensitivity,
  project instructions, tools, and unresolved assumptions.
- **Plan:** define inputs, outputs, invariants, verification, and rollback
  before non-trivial changes.
- **Implement:** make the smallest coherent change inside the authorized scope.
- **Verify:** run deterministic checks, inspect rendered artifacts when layout
  matters, and distinguish PASS, FAIL, and UNVERIFIED.
- **Release:** reconcile documentation and provenance, run the complete
  validation suite, and require explicit user authorization before commit,
  push, publication, submission, email, or other external action.

## Research safeguards

- Never invent citations, datasets, estimates, sample definitions, or
  institutional facts. Verify unstable or externally sourced claims using
  primary sources.
- Treat a missing tool, inaccessible source, skipped render, or unexecuted
  analysis as UNVERIFIED, never as PASS.
- Keep raw data immutable. Write derived data and outputs to documented,
  reproducible locations.
- Record transformations, exclusions, joins, seeds, software versions, and
  inference choices.
- For causal claims, state the estimand, identifying assumptions, treatment
  timing, comparison group, inference method, and diagnostics.
- For restricted data, inspect output-disclosure risks before export or
  sharing. Never expose credentials, personal data, or enclave-restricted
  material.
- Preserve current and comparison versions when revising manuscripts or
  collaborator-facing artifacts. Surface unresolved checks explicitly.

## Codex execution rules

- Read the applicable skill completely before using it. Resolve referenced
  resources relative to that skill.
- Use bounded subagents for independent review lenses or genuinely parallel
  work. Give each agent a non-overlapping scope, use read-only sandboxes for
  reviewers, and synthesize conflicts in the parent task.
- Named roles in `references/agent-roles/` define the portable behavior. Local
  project equivalents in `.codex/agents/` provide optimized execution.
- Use web search for current or niche facts and cite primary sources. Use
  purpose-built connectors when available.
- Do not silently weaken a gate. A user may explicitly accept a documented
  exception; record the exception and its consequences.
- Do not commit, push, open or merge a pull request, deploy, submit, send, or
  share externally without explicit authorization for that action.

## Conversion discipline

Every migrated component must have:

1. A fixed upstream path and source hash.
2. A classification: direct port, native rewrite, composed replacement,
   retained reference, or unsupported.
3. A revision record describing semantic changes and behavior loss.
4. Structural validation.
5. A representative forward test for complex or high-risk behavior.

Mechanical conversion is only a baseline. Remove Claude-only tool names,
permission assumptions, model aliases, slash-command syntax, and stale paths
during semantic review. Keep historical names only in provenance records.

## Repository map

- `skills/`: packaged Codex skills.
- `.codex/agents/`: project-scoped custom agents.
- `references/agent-roles/`: portable role definitions used by skills.
- `references/rules/`: adapted research and quality rules.
- `hooks/`: optional lifecycle hooks; users must review and trust them.
- `assets/templates/`: reusable academic templates and diagram snippets.
- `scripts/`: migration, validation, packaging, and deterministic helpers.
- `docs/conversion/`: source boundary, component map, decisions, and revisions.
- `tests/`: structural and behavioral smoke tests.

## Definition of stable

The package may be labeled stable only when:

- the manifest validates;
- all 58 packaged skill directories validate and contain no migration
  placeholders (52 source-derived skills plus the 6 ManageRAW skills);
- all 19 agent definitions parse and map to portable role files (18
  source-derived roles plus native `manageraw`);
- enabled hooks match current Codex schemas and fail safely;
- provenance and license checks pass;
- representative workflows pass forward tests;
- known limitations are documented without claiming unsupported parity.
