# Custom-agent instructions

- One TOML file defines one narrow role.
- `name`, `description`, and `developer_instructions` are required.
- Reviewers default to `sandbox_mode = "read-only"`.
- Only roles whose job explicitly requires editing may use
  `sandbox_mode = "workspace-write"`.
- Avoid pinned model names unless behavior cannot be expressed through role
  instructions and reasoning effort.
- Keep the portable role definition in `references/agent-roles/` semantically
  aligned with the TOML instructions.

