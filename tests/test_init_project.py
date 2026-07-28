"""Tests for the non-overwriting MAW Codex project initializer."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = ROOT / "scripts" / "init_project.py"


class ProjectInitializerTests(unittest.TestCase):
    def run_initializer(
        self,
        destination: Path,
        *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INITIALIZER),
                str(destination),
                *arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
            timeout=30,
        )

    def test_dry_run_does_not_create_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "project"
            result = self.run_initializer(destination, "--dry-run")
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse(destination.exists())
            self.assertIn("Dry run complete", result.stdout)

    def test_full_initialization_contains_native_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "project"
            result = self.run_initializer(destination)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((destination / "AGENTS.md").is_file())
            self.assertTrue(
                (destination / "templates" / "passport-template.yaml").is_file()
            )
            self.assertTrue(
                (
                    destination
                    / "references"
                    / "rules"
                    / "replication-protocol.md"
                ).is_file()
            )
            agents = list((destination / ".codex" / "agents").glob("*.toml"))
            self.assertEqual(len(agents), 19)
            self.assertTrue(
                (destination / ".maw" / "profile.yaml").is_file()
            )
            self.assertTrue(
                (destination / ".maw" / "lock.json").is_file()
            )
            self.assertTrue(
                (destination / "scripts" / "manageraw-state.py").is_file()
            )

            validator = subprocess.run(
                [
                    sys.executable,
                    str(destination / "scripts" / "validate-project.py"),
                ],
                cwd=destination,
                text=True,
                capture_output=True,
                check=False,
                timeout=60,
            )
            self.assertEqual(
                validator.returncode,
                0,
                msg=validator.stdout + validator.stderr,
            )

    def test_merge_conflict_preflight_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "project"
            destination.mkdir()
            (destination / "AGENTS.md").write_text(
                "existing instructions\n", encoding="utf-8"
            )
            result = self.run_initializer(destination, "--merge")
            self.assertEqual(result.returncode, 2)
            self.assertIn("Conflicts", result.stdout)
            self.assertFalse((destination / "README.md").exists())

    def test_missing_git_preflight_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "project"
            environment = os.environ.copy()
            environment["PATH"] = ""
            result = self.run_initializer(
                destination,
                "--git-init",
                environment=environment,
            )
            self.assertEqual(result.returncode, 3)
            self.assertIn("Git is unavailable", result.stderr)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
