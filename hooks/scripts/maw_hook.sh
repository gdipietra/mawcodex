#!/bin/sh
# Resolve a supported Python runtime for MAW Codex POSIX hooks.

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$PLUGIN_ROOT/hooks/scripts/maw_hook.py"
fi

if command -v python >/dev/null 2>&1; then
    exec python "$PLUGIN_ROOT/hooks/scripts/maw_hook.py"
fi

printf '%s' '{"systemMessage":"MAW Codex hook skipped: Python 3 is unavailable. Research guardrails and continuity automation are inactive for this hook run."}'
exit 0
