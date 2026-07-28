---
name: caw
description: "Coordinate capability ownership when MAW coexists with project-local instructions, other plugins, skills, connectors, or overlapping academic workflows. Use to resolve workflow conflicts, route mixed tasks, decide which capability owns each step, or define a short execution contract before work begins."
---

# CAW - Coordinate Academic Workflow

Route work without absorbing another plugin or weakening the project's
instructions. CAW decides ownership; it does not perform the routed work.

## Default contract

- Stay read-only. Do not edit instructions, profiles, settings, code, data, or
  academic artifacts.
- Treat higher-authority instructions, the user's current request, and every
  applicable project instruction as binding.
- Treat explicit skill invocation as a strong routing signal, not permission to
  bypass scientific, confidentiality, or external-action gates.
- Give MAW priority for academic validity, reproducibility, and project
  governance only within MAW's declared scope.
- Let external plugins retain their own connectors, personal style, and
  operational surfaces. Record responsibilities; never copy their internal
  settings into MAW.
- Surface unresolved conflicts. Do not invent a universal plugin priority
  order.

Read
[`manageraw-profile.md`](../../references/manageraw-profile.md) before using
the project's capability registry.

## 1. Resolve the task and effective context

Identify:

1. The requested outcome and its separable task dimensions.
2. Explicitly named skills, plugins, agents, or connectors.
3. Applicable root and nested project instructions.
4. The current `.maw/profile.yaml`, when present.
5. Scientific, confidentiality, publication, communication, and external
   action gates.

If a missing user choice changes ownership materially, ask one focused
question. Otherwise make a reversible routing assumption and label it.

## 2. Build the capability map

For each task dimension, name:

- **owner:** produces or controls the result;
- **contributors:** provide inputs or a specialized operation;
- **verifier:** checks the result independently when warranted;
- **gate:** authorization required before a state-changing or external action;
- **evidence:** instruction, profile entry, explicit invocation, or detected
  capability supporting the assignment.

Use [`ownership-contract.md`](references/ownership-contract.md) for the
decision rules and output schema.

Prefer these defaults when the project provides no narrower rule:

| Dimension | Default owner |
| --- | --- |
| Academic validity, source authority, and reproducibility | MAW |
| Project-local specialization | The applicable project-local skill or instruction |
| Personal communication style | The user's personal operations capability |
| Email, calendar, cloud-file, or other connector action | The relevant connected capability |
| Commit, push, publication, submission, sync, or send | No capability until the user authorizes the exact action |

An owner for content is not automatically the owner for transport. For
example, MAW may verify an academic handoff while another plugin drafts in the
user's preferred style and Gmail performs the send.

## 3. Resolve conflicts explicitly

Classify each conflict:

- **authority:** instructions disagree;
- **scope:** two capabilities claim the same task;
- **state:** profiles or files describe different current behavior;
- **safety:** a proposed action crosses a scientific, privacy, or release gate;
- **format:** capabilities expect incompatible inputs or outputs.

Resolve in this order:

1. Obey higher-authority and more specifically applicable instructions.
2. Preserve the user's explicit invocation and outcome where safe.
3. Prefer project-local specialization for its subtree.
4. Preserve MAW's academic safeguards.
5. Split content, verification, and transport ownership when that removes the
   conflict.
6. Ask the user if two valid choices remain materially different.

Do not silently choose the newest, broadest, or most feature-rich capability.

## 4. Return an execution contract

Produce a compact contract before handing work off:

```text
Outcome:
Effective project context:
Ownership:
- <dimension>: owner; contributors; verifier; gate
Conflict decisions:
Assumptions:
Execution order:
```

Report `NO MATERIAL CONFLICT` when coordination is straightforward. Report
`DECISION REQUIRED` when the user must choose. Do not create or update the
project profile; hand durable ownership changes to `$paw`.

## Handoffs

- Use `$jaw` when MAW has not yet assessed or joined the project.
- Use `$paw` when a routing decision should become durable in
  `.maw/profile.yaml`.
- Use `$law` when the conflict concerns root or nested `AGENTS.md`, project
  configuration, team versus personal settings, or effective precedence.
- Return to the requested academic or operational skill after the contract is
  clear.
