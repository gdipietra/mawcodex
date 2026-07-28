<!-- Native replacement for .claude/references/model-versions.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 5af53ec49728cd44a389d4f02c026f8749262b547708c25ac4213d9b02c12390. -->

# Codex model routing

Do not encode retired model aliases in workflow prose. Prefer the parent model unless a narrow custom agent has a measured need for a different model. Express durable intent through `model_reasoning_effort`, sandbox mode, and role instructions.

Before pinning a model, verify the current Codex model catalog and official documentation. If the catalog cannot be verified, inherit the parent model and record the choice as UNVERIFIED rather than guessing.

Suggested durable routing:

- high reasoning: causal-methods review, claim verification, editorial synthesis, adversarial audits;
- medium reasoning: focused proofreading, translation, deterministic fix execution, environment capture;
- low reasoning: mechanical inventory or format checks whose outputs are independently verified.

Model choice never relaxes scientific, provenance, or verification gates.
