# Hook instructions

- Hooks are optional defense-in-depth, never the sole enforcement mechanism.
- Use only current Codex hook events and input schemas.
- Parse untrusted hook input defensively and fail safely.
- Do not transmit repository content, prompts, or environment secrets.
- Keep expensive or transcript-dependent checks out of default hooks.
- Any blocking hook must explain the reason and a safe resolution.
- Users must review and trust plugin-bundled hooks before Codex executes them.

