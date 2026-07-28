---
name: learn
description: "Extract a non-obvious, reusable discovery from the current task into a persistent Codex skill. Use after difficult debugging, a misleading error, a verified workaround, a tool integration, repeated trial-and-error, or a multi-step workflow that future tasks should reuse. Do not use for a one-off note, an unverified guess, or a secret-bearing incident."
---

# Learn

Convert a verified session discovery into a small reusable skill. This is the
capture-oriented sibling of [$new-skill](../new-skill/SKILL.md): use `learn`
when the reusable behavior has already emerged from real work; use `new-skill`
when deliberately designing a new interface.

## 1. Decide whether the lesson merits a skill

Write a two-sentence candidate lesson, then test it:

1. What was non-obvious before this task?
2. What evidence showed the final approach works?
3. In what future situation would the same procedure apply?
4. What boundary prevents unsafe or overbroad reuse?

Continue only if at least one future task would materially benefit and the
solution was actually verified. Otherwise return a concise session note
instead of creating a skill.

Never capture credentials, private data, machine-specific secrets, personal
identifiers, restricted-data values, or confidential paths. Generalize a
machine-specific incident only when doing so preserves the evidence and
trigger conditions.

## 2. Check for overlap

Search the current repository's `skills/*/SKILL.md` metadata and bodies for the
trigger, error text, tool, and workflow. If the user wants a personal installed
skill outside the workspace, ask before reading or writing that location.

- Exact overlap: propose a focused update to the existing skill.
- Partial overlap: add a verified variant only if it does not blur the
  existing trigger.
- No overlap: create a new skill.

Do not create near-duplicate skills with different names.

## 3. Define the reusable contract

Before writing, state:

- a lowercase kebab-case name under 64 characters;
- exact trigger phrases, symptoms, or error messages;
- inputs and outputs;
- the verified procedure;
- deterministic verification and expected evidence;
- failure states, including what remains `UNVERIFIED`;
- confidentiality and external-action boundaries.

Ask for the target location if it is not clear. In this package repository,
default to `skills/<name>/`. For an installed personal skill, use the location
selected by the user.

## 4. Create or update the skill

Read and apply the active `$skill-creator` skill completely. For a brand-new
skill, use its `init_skill.py` helper to initialize the directory and generate
`agents/openai.yaml`; do not hand-create an ersatz scaffold when the helper is
available. If the helper cannot be located or run, report that step
`UNVERIFIED` and ask for the safe next action.

Use only this frontmatter:

```yaml
---
name: descriptive-kebab-case-name
description: "What the skill does and the concrete situations that trigger it."
---
```

Keep the body concise and imperative. Include:

- the problem and trigger conditions;
- the verified workflow;
- verification evidence and failure semantics;
- one representative example if it adds information;
- references to primary documentation or project files;
- explicit non-goals.

Move large reference material or repeated deterministic logic into
`references/` or `scripts/` within the skill. Do not add a README, changelog,
installation guide, or migration notes inside the skill directory.

## 5. Validate

Run the active skill creator's `quick_validate.py` against the target folder.
If a new script was added, execute a representative test. For complex or
high-risk behavior, recommend a clean-context forward test; do not claim one
ran unless it did.

The skill is not complete when:

- frontmatter has fields other than `name` and `description`;
- the description lacks concrete trigger conditions;
- placeholders remain;
- the proposed solution was not verified;
- the workflow silently assumes tools, access, or permissions;
- sensitive incident details remain.

## Output

Report the target path, trigger, preserved evidence, validation result, and
any forward test still required. Do not commit, install globally, publish, or
push the skill without an explicit user request for that action.
