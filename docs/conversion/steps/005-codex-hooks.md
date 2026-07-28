# Step 005 — Convert lifecycle hooks

## Revision

Reviewed all seven upstream hooks against the current Codex hook events and
JSON contracts. Consolidated the four portable lifecycle behaviors into one
small runner per operating-system family:

- `hooks/scripts/maw_hook.py` for POSIX environments;
- `hooks/scripts/maw_hook.ps1` for Windows.

Registered `PreToolUse`, `PostToolUse`, `PreCompact`, and `SessionStart`
handlers in `hooks/hooks.json`. Recorded the complete seven-hook disposition
in `docs/conversion/HOOK_MAP.md`.

## Compatibility decisions

- Replaced Claude-specific environment variables with `PLUGIN_ROOT`,
  `PLUGIN_DATA`, and event-supplied `cwd`.
- Emitted Codex `hookSpecificOutput` fields for denials and added context.
- Removed reliance on Claude transcript paths and context-window estimates.
- Kept notification and automatic stop-time logging out of the default hook
  set because Codex already provides native notification and explicit durable
  workflow surfaces.
- Retained the original Git guardrail intent with attribution while narrowing
  denial to commands with clear destructive semantics.

## Verification

The five contract scenarios in `tests/test_hooks.py` pass against both
implementations on Windows. Internal hook failures return success without
blocking Codex.

## Result

All seven upstream hooks have a documented Codex disposition: four enabled
lifecycle ports and three native replacements. Hook behavior is cross-platform
and no operational Claude hook dependency remains.

`RUNTIME_SURFACES_MANIFEST.json` binds each of the seven source files to the
fixed upstream hash, its allowed classification, its current Codex target or
replacement hashes, and this revision record.
