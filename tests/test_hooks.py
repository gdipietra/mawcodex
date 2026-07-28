"""Behavior tests for both MAW Codex hook implementations."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PYTHON_HOOK = ROOT / "hooks" / "scripts" / "maw_hook.py"
POWERSHELL_HOOK = ROOT / "hooks" / "scripts" / "maw_hook.ps1"


class HookContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.implementations = ["python"]
        if shutil.which("powershell.exe"):
            cls.implementations.append("powershell")

    def run_hook(
        self,
        implementation: str,
        payload: dict[str, Any],
        *,
        environment: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        if implementation == "python":
            command = [sys.executable, str(PYTHON_HOOK)]
        else:
            command = [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(POWERSHELL_HOOK),
            ]
        hook_environment = os.environ.copy()
        if environment:
            hook_environment.update(environment)
        result = subprocess.run(
            command,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
            env=hook_environment,
            timeout=15,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"{implementation} hook failed: {result.stderr}",
        )
        if not result.stdout.strip():
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(
                f"{implementation} emitted invalid JSON: "
                f"{result.stdout!r} ({error})"
            )

    def test_destructive_git_is_denied(self) -> None:
        commands = [
            "git -C repo reset --hard",
            'git reset "--hard" HEAD',
            "git reset HEAD '--hard'",
            (
                '"git" --no-pager -c color.ui=false -C "repo path" '
                '"reset" HEAD "--hard"'
            ),
            'echo ready && git reset HEAD "--hard"',
            'printf ready | git clean "-df"',
            "git clean --exclude cache '--force'",
            'git push origin main "--force"',
            "git --no-pager -c color.ui=false push origin main '-f'",
            'git push --force-with-lease && git push "--force"',
            'git add "--all"',
            'git checkout HEAD -- "."',
            'git restore --source=HEAD --worktree "."',
        ]
        for implementation in self.implementations:
            for command in commands:
                with self.subTest(
                    implementation=implementation,
                    command=command,
                ):
                    output = self.run_hook(
                        implementation,
                        {
                            "hook_event_name": "PreToolUse",
                            "tool_name": "Bash",
                            "tool_input": {"command": command},
                        },
                    )
                    self.assertEqual(
                        output["hookSpecificOutput"]["permissionDecision"],
                        "deny",
                    )

    def test_force_with_lease_is_allowed(self) -> None:
        commands = [
            "git push --force-with-lease",
            'git push "--force-with-lease"',
            (
                "git --no-pager push origin main "
                "'--force-with-lease=refs/heads/main:abc123'"
            ),
            'echo "--force" && git push --force-with-lease',
        ]
        for implementation in self.implementations:
            for command in commands:
                with self.subTest(
                    implementation=implementation,
                    command=command,
                ):
                    self.assertIsNone(
                        self.run_hook(
                            implementation,
                            {
                                "hook_event_name": "PreToolUse",
                                "tool_name": "Bash",
                                "tool_input": {"command": command},
                            },
                        )
                    )

    def test_machine_path_warns_or_denies_in_strict_mode(self) -> None:
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "apply_patch",
            "tool_input": {
                "command": (
                    "*** Begin Patch\n"
                    "*** Update File: scripts/model.R\n"
                    "@@\n"
                    "+data <- read.csv('/Users/alice/data.csv')\n"
                    "*** End Patch\n"
                )
            },
        }
        for implementation in self.implementations:
            with self.subTest(implementation=implementation, strict=False):
                output = self.run_hook(implementation, payload)
                self.assertIn(
                    "breaks portable replication",
                    output["hookSpecificOutput"]["additionalContext"],
                )
            with self.subTest(implementation=implementation, strict=True):
                output = self.run_hook(
                    implementation,
                    payload,
                    environment={"MAWCODEX_STRICT_PATHS": "1"},
                )
                self.assertEqual(
                    output["hookSpecificOutput"]["permissionDecision"],
                    "deny",
                )

    def test_claim_reconciliation_marks_dependent_claims_stale(self) -> None:
        for implementation in self.implementations:
            with self.subTest(implementation=implementation):
                with tempfile.TemporaryDirectory() as project_tmp:
                    with tempfile.TemporaryDirectory() as data_tmp:
                        project = Path(project_tmp)
                        (project / ".git").mkdir()
                        passport_dir = (
                            project / "quality_reports" / "passports"
                        )
                        passport_dir.mkdir(parents=True)
                        (passport_dir / "table-1.yaml").write_text(
                            "source_file: scripts/model.R\n",
                            encoding="utf-8",
                        )
                        payload = {
                            "hook_event_name": "PostToolUse",
                            "tool_name": "apply_patch",
                            "cwd": str(project),
                            "tool_input": {
                                "command": (
                                    "*** Begin Patch\n"
                                    "*** Update File: scripts/model.R\n"
                                    "@@\n+x <- 1\n"
                                    "*** End Patch\n"
                                )
                            },
                        }
                        output = self.run_hook(
                            implementation,
                            payload,
                            environment={"PLUGIN_DATA": data_tmp},
                        )
                        self.assertIn(
                            "may be STALE",
                            output["hookSpecificOutput"][
                                "additionalContext"
                            ],
                        )

    def test_compaction_state_is_restored(self) -> None:
        for implementation in self.implementations:
            with self.subTest(implementation=implementation):
                with tempfile.TemporaryDirectory() as project_tmp:
                    with tempfile.TemporaryDirectory() as data_tmp:
                        project = Path(project_tmp)
                        (project / ".git").mkdir()
                        plans = project / "quality_reports" / "plans"
                        plans.mkdir(parents=True)
                        (plans / "active.md").write_text(
                            "# Plan\n\nStatus: approved\n\n- [ ] Verify result\n",
                            encoding="utf-8",
                        )
                        environment = {"PLUGIN_DATA": data_tmp}
                        saved = self.run_hook(
                            implementation,
                            {
                                "hook_event_name": "PreCompact",
                                "trigger": "auto",
                                "cwd": str(project),
                            },
                            environment=environment,
                        )
                        self.assertTrue(saved["continue"])
                        restored = self.run_hook(
                            implementation,
                            {
                                "hook_event_name": "SessionStart",
                                "source": "compact",
                                "cwd": str(project),
                            },
                            environment=environment,
                        )
                        context = restored["hookSpecificOutput"][
                            "additionalContext"
                        ]
                        self.assertIn("active.md", context)
                        self.assertIn("Verify result", context)


if __name__ == "__main__":
    unittest.main()
