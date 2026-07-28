# Skill conversion instructions

- Preserve each upstream skill's trigger intent, inputs, outputs, safety gates,
  and verification behavior.
- Keep frontmatter limited to `name` and `description`.
- Express invocation using `$skill-name` or natural language, not Claude slash
  commands.
- Describe capabilities, not provider-specific tool names. If a capability is
  unavailable, mark the affected result UNVERIFIED and provide a safe next
  step.
- When a named reviewer is needed, prefer a project custom agent with the
  corresponding role. Otherwise spawn a bounded subagent using the role file
  under `../../references/agent-roles/`.
- Do not authorize external publication, commit, push, merge, submission, or
  message sending unless the user explicitly requests that action.
- After editing a skill, update its record in
  `docs/conversion/skills/<skill-name>.md` and run the skill validator.

