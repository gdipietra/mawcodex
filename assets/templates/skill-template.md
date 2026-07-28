# Codex skill template

Use Codex's `skill-creator` for new skills. This file is a compact review
reference, not a replacement for that scaffolder.

```markdown
---
name: descriptive-kebab-case-name
description: Describe what the skill does and concrete phrases or situations
  that should trigger it.
---

# Workflow title

## Inputs

State required inputs, defaults, and the smallest blocking questions.

## Workflow

1. Inspect applicable `AGENTS.md` and source-of-truth artifacts.
2. Define outputs, invariants, and verification.
3. Execute the bounded workflow.
4. Verify outputs and distinguish PASS, FAIL, and UNVERIFIED.

## Safety and external actions

State data, permission, and publication boundaries. Require explicit user
authorization before commit, push, deploy, send, submit, or delete.

## Resources

Reference only resources this skill actually needs, with paths relative to
the skill directory.
```

Keep frontmatter limited to `name` and `description`, add
`agents/openai.yaml`, run `quick_validate.py`, and forward-test complex skills
with realistic prompts.
