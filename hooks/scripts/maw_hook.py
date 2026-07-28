#!/usr/bin/env python3
"""Cross-platform POSIX hook runner for MAW Codex.

The Windows-equivalent implementation is ``maw_hook.ps1``. Hooks are
defense-in-depth and fail open on internal errors. Denials are limited to a
small, reviewable set of destructive Git commands.

The git guardrail pattern is adapted from mattpocock/skills through the fixed
MIT-licensed upstream source. See THIRD_PARTY_NOTICES.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GIT_DENIALS = {
    "reset": (
        "git reset --hard irreversibly discards uncommitted work.",
        "Use a stash or reset only explicitly named paths.",
    ),
    "clean": (
        "git clean with force deletes untracked files, including untracked data.",
        "Inspect with git clean -n and remove only verified targets.",
    ),
    "push": (
        "git push --force can clobber remote history.",
        "Use --force-with-lease only after reviewing the exact branch state.",
    ),
    "add": (
        "Blanket staging can include data, secrets, or local settings.",
        "Stage explicit reviewed paths.",
    ),
    "restore": (
        "Mass working-tree discard is difficult to recover.",
        "Restore explicit files or preserve changes in a stash.",
    ),
}
GLOBAL_GIT_OPTIONS_WITH_VALUE = {
    "-c",
    "--config-env",
    "--exec-path",
    "--git-dir",
    "--namespace",
    "--super-prefix",
    "--work-tree",
}
MACHINE_PATH = re.compile(
    r"(/Users/[^/\s'\")]+|/home/[^/\s'\")]+|"
    r"[A-Za-z]:\\Users\\[^\\\s'\"]+)"
)
CODE_EXTENSIONS = {".r", ".rmd", ".qmd", ".do", ".py", ".jl"}
ANALYSIS_PATH = re.compile(
    r"(^|/)scripts/.*\.(r|rmd|do|py|jl)$|"
    r"(^|/)scripts/.*/_outputs/",
    re.IGNORECASE,
)
PATCH_PATH = re.compile(
    r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$",
    re.MULTILINE,
)
THROTTLE_SECONDS = 300


def emit(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False)


def read_input() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}
    return value if isinstance(value, dict) else {}


def project_root(cwd: str) -> Path:
    path = Path(cwd or os.getcwd()).resolve()
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path


def state_directory(root: Path) -> Path:
    data_root = os.environ.get("PLUGIN_DATA")
    base = (
        Path(data_root)
        if data_root
        else Path(tempfile.gettempdir()) / "mawcodex-plugin-data"
    )
    project_hash = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    directory = base / "sessions" / project_hash
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def changed_paths(tool_input: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    explicit = tool_input.get("file_path")
    if isinstance(explicit, str) and explicit.strip():
        paths.append(explicit.strip())
    command = tool_input.get("command")
    if isinstance(command, str):
        paths.extend(match.strip() for match in PATCH_PATH.findall(command))
    normalized: list[str] = []
    for path in paths:
        portable = path.replace("\\", "/").lstrip("./")
        if portable and portable not in normalized:
            normalized.append(portable)
    return normalized


def added_patch_text(command: str) -> str:
    return "\n".join(
        line[1:]
        for line in command.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def shell_segments(command: str) -> list[str]:
    """Split common shell compounds without splitting inside quotes."""
    segments: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False
    for character in command:
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character in {"\\", "`"}:
            current.append(character)
            escaped = True
            continue
        if quote is not None:
            current.append(character)
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            current.append(character)
            quote = character
            continue
        if character in ";&|\r\n()":
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            current = []
            continue
        current.append(character)
    segment = "".join(current).strip()
    if segment:
        segments.append(segment)
    return segments


def shell_tokens(segment: str) -> list[str]:
    """Tokenize the command forms needed by the Git guardrail."""
    tokens: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False
    for character in segment:
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character in {"\\", "`"}:
            escaped = True
            continue
        if quote is not None:
            if character == quote:
                quote = None
            else:
                current.append(character)
            continue
        if character in {"'", '"'}:
            quote = character
            continue
        if character.isspace():
            if current:
                tokens.append("".join(current))
                current = []
            continue
        current.append(character)
    if current:
        tokens.append("".join(current))
    return tokens


def is_git_executable(token: str) -> bool:
    leaf = token.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return leaf in {"git", "git.exe"}


def parse_git_invocation(
    tokens: list[str],
    git_index: int,
) -> tuple[str, list[str]] | None:
    """Return the Git subcommand and arguments after supported global options."""
    index = git_index + 1
    while index < len(tokens):
        token = tokens[index]
        lowered = token.lower()
        if lowered in GLOBAL_GIT_OPTIONS_WITH_VALUE:
            index += 2
            continue
        if (
            (lowered.startswith("-c") and len(token) > 2)
            or any(
                lowered.startswith(option + "=")
                for option in GLOBAL_GIT_OPTIONS_WITH_VALUE
                if option.startswith("--")
            )
        ):
            index += 1
            continue
        if token.startswith("-"):
            index += 1
            continue
        return lowered, tokens[index + 1 :]
    return None


def has_short_flag(arguments: list[str], flag: str) -> bool:
    return any(
        argument.startswith("-")
        and not argument.startswith("--")
        and flag.lower() in argument[1:].lower()
        for argument in arguments
    )


def git_denial(command: str) -> tuple[str, str] | None:
    """Find a directly expressed destructive Git operation."""
    for segment in shell_segments(command):
        tokens = shell_tokens(segment)
        for index, token in enumerate(tokens):
            if not is_git_executable(token):
                continue
            invocation = parse_git_invocation(tokens, index)
            if invocation is None:
                continue
            subcommand, arguments = invocation
            lowered_arguments = [argument.lower() for argument in arguments]
            if subcommand == "reset" and "--hard" in lowered_arguments:
                return GIT_DENIALS["reset"]
            if subcommand == "clean" and (
                "--force" in lowered_arguments
                or has_short_flag(arguments, "f")
            ):
                return GIT_DENIALS["clean"]
            if subcommand == "push" and (
                "--force" in lowered_arguments
                or has_short_flag(arguments, "f")
            ):
                return GIT_DENIALS["push"]
            if subcommand == "add" and any(
                argument in {"-a", "--all", ".", ":/"}
                for argument in lowered_arguments
            ):
                return GIT_DENIALS["add"]
            if subcommand in {"checkout", "restore"} and "." in arguments:
                return GIT_DENIALS["restore"]
    return None


def deny(reason: str) -> None:
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


def pre_tool_use(data: dict[str, Any]) -> None:
    tool = str(data.get("tool_name", ""))
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    command = tool_input.get("command")
    command = command if isinstance(command, str) else ""

    if tool == "Bash":
        denial = git_denial(command)
        if denial is not None:
            reason, alternative = denial
            deny(
                "Blocked by MAW Codex guardrails: "
                f"{reason} {alternative}"
            )
            return

    if tool in {"apply_patch", "Edit", "Write"}:
        candidates = changed_paths(tool_input)
        content_parts: list[str] = []
        for key in ("content", "new_string"):
            value = tool_input.get(key)
            if isinstance(value, str):
                content_parts.append(value)
        if command:
            content_parts.append(added_patch_text(command))
        content = "\n".join(content_parts)
        match = MACHINE_PATH.search(content)
        code_targets = [
            path
            for path in candidates
            if Path(path).suffix.lower() in CODE_EXTENSIONS
        ]
        if match and code_targets:
            message = (
                f"Hardcoded machine path {match.group(0)!r} in "
                f"{', '.join(code_targets)} breaks portable replication. "
                "Use project-relative paths or a documented configuration."
            )
            if os.environ.get("MAWCODEX_STRICT_PATHS") == "1":
                deny(f"Blocked by MAWCODEX_STRICT_PATHS=1: {message}")
            else:
                emit(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "additionalContext": message,
                        }
                    }
                )


def relative_path(path: str, root: Path) -> str:
    candidate = Path(path)
    try:
        if candidate.is_absolute():
            return candidate.resolve().relative_to(root).as_posix()
    except (OSError, ValueError):
        pass
    return path.replace("\\", "/").lstrip("./")


def post_tool_use(data: dict[str, Any]) -> None:
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return
    root = project_root(str(data.get("cwd", "")))
    paths = [
        relative_path(path, root)
        for path in changed_paths(tool_input)
    ]
    watched = [path for path in paths if ANALYSIS_PATH.search(path)]
    if not watched:
        return
    passport_dir = root / "quality_reports" / "passports"
    passports = sorted(passport_dir.glob("*.yaml"))
    if not passports:
        return

    state_file = state_directory(root) / "claim-reconcile-state.json"
    try:
        throttle = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        throttle = {}
    now = time.time()
    messages: list[str] = []
    for changed in watched:
        if now - float(throttle.get(changed, 0)) < THROTTLE_SECONDS:
            continue
        affected: list[tuple[str, int]] = []
        for passport in passports:
            try:
                text = passport.read_text(
                    encoding="utf-8", errors="replace"
                )
            except OSError:
                continue
            hits = sum(
                1
                for line in text.splitlines()
                if (
                    "source_file" in line or "output_file" in line
                )
                and changed in line
            )
            if hits:
                affected.append((passport.name, hits))
        if not affected:
            continue
        throttle[changed] = now
        total = sum(count for _, count in affected)
        locations = ", ".join(
            f"{name} ({count})" for name, count in affected
        )
        messages.append(
            f"{changed} changed; {total} passport claim(s) may be STALE "
            f"in {locations}."
        )
    if not messages:
        return
    try:
        state_file.write_text(
            json.dumps(throttle, indent=2), encoding="utf-8"
        )
    except OSError:
        pass
    message = " ".join(messages)
    emit(
        {
            "systemMessage": message,
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"{message} Run $audit-reproducibility before relying on "
                    "or publishing affected numeric claims."
                ),
            },
        }
    )


def active_plan(root: Path) -> dict[str, Any] | None:
    plans_dir = root / "quality_reports" / "plans"
    try:
        plans = sorted(
            plans_dir.glob("*.md"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return None
    for plan in plans[:5]:
        try:
            content = plan.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            continue
        status_match = re.search(
            r"^\s*\**\s*status\s*\**\s*:\s*\**\s*"
            r"(draft|approved|completed|implemented|in[ -]?progress)",
            content,
            re.IGNORECASE | re.MULTILINE,
        )
        status = (
            status_match.group(1).lower().replace(" ", "_")
            if status_match
            else "in_progress"
        )
        if status in {"completed", "implemented"}:
            continue
        task = next(
            (
                line.split("- [ ]", 1)[1].strip()
                for line in content.splitlines()
                if "- [ ]" in line
            ),
            None,
        )
        return {
            "path": str(plan),
            "name": plan.name,
            "status": status,
            "current_task": task,
        }
    return None


def recent_session_log(root: Path) -> Path | None:
    logs_dir = root / "quality_reports" / "session_logs"
    try:
        logs = sorted(
            logs_dir.glob("*.md"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return None
    return logs[0] if logs else None


def pre_compact(data: dict[str, Any]) -> None:
    root = project_root(str(data.get("cwd", "")))
    plan = active_plan(root)
    session_log = recent_session_log(root)
    state = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "trigger": data.get("trigger"),
        "plan": plan,
        "session_log": str(session_log) if session_log else None,
    }
    state_file = state_directory(root) / "pre-compact-state.json"
    state_file.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    emit(
        {
            "continue": True,
            "systemMessage": (
                "MAW Codex saved the active plan and session-log pointers "
                "before compaction."
            ),
        }
    )


def session_start(data: dict[str, Any]) -> None:
    if data.get("source") not in {"compact", "resume"}:
        return
    root = project_root(str(data.get("cwd", "")))
    state_file = state_directory(root) / "pre-compact-state.json"
    try:
        saved = json.loads(state_file.read_text(encoding="utf-8"))
        state_file.unlink(missing_ok=True)
    except (OSError, json.JSONDecodeError):
        saved = {}
    plan = active_plan(root) or saved.get("plan")
    session_log = recent_session_log(root)
    if not plan and not session_log and not saved:
        return
    lines = [
        "MAW Codex context restoration:",
        "- Re-read the applicable AGENTS.md and active workflow skill.",
    ]
    if isinstance(plan, dict):
        lines.append(
            f"- Active plan: {plan.get('path') or plan.get('name')} "
            f"({plan.get('status', 'unknown')})."
        )
        if plan.get("current_task"):
            lines.append(f"- Next unchecked item: {plan['current_task']}")
    if session_log:
        lines.append(f"- Most recent session log: {session_log}")
    elif saved.get("session_log"):
        lines.append(
            f"- Saved session-log pointer: {saved['session_log']}"
        )
    lines.append(
        "- Inspect current git status and diff before continuing; do not "
        "assume saved state is current."
    )
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(lines),
            }
        }
    )


def main() -> int:
    data = read_input()
    event = str(data.get("hook_event_name", ""))
    if event == "PreToolUse":
        pre_tool_use(data)
    elif event == "PostToolUse":
        post_tool_use(data)
    elif event == "PreCompact":
        pre_compact(data)
    elif event == "SessionStart":
        session_start(data)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        raise SystemExit(0)
