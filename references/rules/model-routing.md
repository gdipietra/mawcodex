<!-- Native rewrite of .claude/rules/model-routing.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 bff448d47407f9c053194f36940890d118e3e20c14f98a1bbe01d5b202a36eab. -->

# Model and reasoning routing

## Applicability

Load this rule when defining or revising skills, custom agents, or multi-agent workflows.

## Durable rule

Route by cognitive demand, independence needs, and sandbox scope. Do not preserve upstream provider aliases or price tables: model catalogs and pricing drift, while the task classes remain stable.

| Work class | Reasoning default | Examples |
| --- | --- | --- |
| Mechanical | low or medium | inventory, format conversion, deterministic checks |
| Focused review or implementation | medium or high | proofreading, translation, bounded fixes |
| High judgment | high or xhigh | identification review, claim verification, editorial synthesis, adversarial audit |

Prefer the parent model. Pin a different model only after verifying the current official Codex model catalog and documenting a measured benefit. If current availability cannot be verified, inherit rather than guess.

Use isolated subagents when error independence matters. Different roles, evidence sets, or fresh contexts matter more than cosmetic model diversity. A lower-cost model never weakens the output schema, scientific checks, or PASS/FAIL/UNVERIFIED semantics.
