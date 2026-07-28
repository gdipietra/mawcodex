---
name: new-skill
description: "Design and scaffold a Codex skill from a fuzzy workflow request, including trigger-focused metadata, a concise SKILL.md, optional reusable resources, deterministic UI metadata, and structural validation. Use for requests such as \"write a skill\", \"scaffold a skill\", \"create a new skill\", \"I keep doing X, make it a skill\", or \"turn this workflow into a skill\". Use $learn instead when capturing a discovery already verified in the current task."
---

# New Skill

Create a deep module behind a small interface: the user supplies the intent,
and the skill hides the detailed workflow behind clear triggers and a compact
body.

This workflow is adapted from the `write-a-skill` pattern in
[mattpocock/skills](https://github.com/mattpocock/skills) and rewritten for
Codex's current skill structure.

## 1. Resolve scope and destination

Ask for or infer only when unambiguous:

- purpose and representative user requests;
- exact trigger phrases or contexts;
- inputs, flags, outputs, and read-only versus writing behavior;
- required capabilities, tools, scripts, references, or assets;
- safety, confidentiality, and external-action boundaries;
- target location.

In this package repository, default to `skills/<name>/`. For a personal skill,
use the user-selected Codex skills directory. Ask before reading or writing
outside the active workspace.

Normalize the name to lowercase kebab-case under 64 characters. Reject a name
that collides with an existing skill or creates a confusing near-duplicate.
Search relevant sibling skills before designing a new one.

Echo a short design brief and resolve any material ambiguity before writing.

## 2. Plan reusable contents

Choose the smallest useful package:

- `SKILL.md` for essential workflow guidance;
- `agents/openai.yaml` for UI metadata;
- `scripts/` for deterministic, repeated logic;
- `references/` for detailed knowledge loaded only when needed;
- `assets/` for output templates or media.

Do not add an internal README, changelog, installation guide, or conversion
record. Keep detailed examples or schemas out of `SKILL.md` when a directly
linked resource provides better progressive disclosure.

## 3. Initialize

Read and apply the active `$skill-creator` skill completely. For a brand-new
skill, use its `init_skill.py` helper with the chosen destination and only the
resource directories actually needed. Supply deterministic interface values:

- `display_name`;
- `short_description`;
- `default_prompt`.

If the active helper cannot be found or executed, mark initialization
`UNVERIFIED` and ask for a safe next step. Do not claim a manually improvised
folder is equivalent to the current generator.

## 4. Write the skill

Frontmatter must contain exactly:

```yaml
---
name: skill-name
description: "What the skill does and the specific contexts that trigger it."
---
```

Put all trigger guidance in `description`; the body loads only after a trigger.
Write the body in imperative language and keep it under 500 lines. Include only
information another Codex instance needs to perform the task:

- inputs and scope;
- ordered workflow and decision points;
- capability-unavailable behavior;
- validation and observable evidence;
- output contract;
- failure semantics;
- explicit boundaries.

Use `$skill-name` or natural language for sibling skill invocation. Refer to
capabilities rather than provider-specific tool labels. For an independent
review role, prefer the project custom agent and provide a portable role-file
fallback in `references/agent-roles/`.

Treat inaccessible sources, missing tools, skipped render checks, and unrun
tests as `UNVERIFIED`. Require explicit authorization for commit, push, merge,
deployment, submission, sending, or publication.

## 5. Regenerate and validate

After editing:

1. Regenerate `agents/openai.yaml` with the active skill creator's
   `generate_openai_yaml.py`, passing all interface values explicitly.
2. Run `quick_validate.py <skill-directory>`.
3. Test every new script on a representative safe case.
4. Resolve broken relative links and remove every template placeholder.
5. For complex or high-risk behavior, propose a clean-context forward test.
   Do not claim forward testing unless it actually ran.

In this repository, also run the package's relevant surface, provenance, and
skill-count checks. A structural validator passing does not prove behavioral
parity.

## Output

Report:

- created or updated path;
- trigger summary;
- resources added;
- UI metadata generation result;
- structural and script-test results;
- any forward test or environment check still required.

With `--dry-run`, present the proposed contents without writing. With
`--from-learn`, use an existing $learn discovery as evidence, but still perform
the full design and validation workflow.

## Boundaries

- Use [$learn](../learn/SKILL.md) for a discovery already demonstrated during
  the current task.
- Create agent definitions, hooks, plugins, and MCP integrations with their
  dedicated current tooling; do not disguise them as skills.
- Do not modify repository discovery tables, manifests, or `AGENTS.md` unless
  that change is part of the user's authorized scope.
- Do not commit, install globally, publish, or push without explicit
  authorization.
