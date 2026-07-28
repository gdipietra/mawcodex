"""Tests for the POSIX hook runtime resolver."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "hooks" / "scripts" / "maw_hook.sh"


class PosixHookLauncherTests(unittest.TestCase):
    def test_missing_python_is_visible_and_fail_open(self) -> None:
        shell = shutil.which("sh")
        if not shell and os.name == "nt":
            for candidate in (
                Path(r"C:\Program Files\Git\bin\sh.exe"),
                Path(r"C:\Program Files\Git\usr\bin\sh.exe"),
            ):
                if candidate.is_file():
                    shell = str(candidate)
                    break
        if not shell:
            self.skipTest("POSIX sh is unavailable on this host")
        with tempfile.TemporaryDirectory() as empty_path:
            environment = os.environ.copy()
            environment["PATH"] = empty_path
            environment["PLUGIN_ROOT"] = str(ROOT)
            result = subprocess.run(
                [shell, str(LAUNCHER)],
                input=json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Bash",
                        "tool_input": {"command": "git reset --hard"},
                    }
                ),
                text=True,
                capture_output=True,
                check=False,
                env=environment,
                timeout=15,
            )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        output = json.loads(result.stdout)
        self.assertIn("Python 3 is unavailable", output["systemMessage"])
        self.assertIn("inactive", output["systemMessage"])


if __name__ == "__main__":
    unittest.main()
