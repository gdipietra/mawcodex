"""Tests for the preview-first personal marketplace installer."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_local_plugin.py"


class LocalInstallerTests(unittest.TestCase):
    def run_installer(
        self,
        plugin_parent: Path,
        agents_home: Path,
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--plugin-parent",
                str(plugin_parent),
                "--agents-home",
                str(agents_home),
                *arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )

    def test_preview_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_parent = root / "plugins"
            agents_home = root / ".agents"
            result = self.run_installer(plugin_parent, agents_home)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse(plugin_parent.exists())
            self.assertFalse(agents_home.exists())
            self.assertIn("Preview complete", result.stdout)

    def test_apply_creates_plugin_and_personal_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_parent = root / "plugins"
            agents_home = root / ".agents"
            result = self.run_installer(
                plugin_parent,
                agents_home,
                "--apply",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            plugin = plugin_parent / "mawcodex"
            self.assertTrue((plugin / ".codex-plugin" / "plugin.json").is_file())
            self.assertEqual(
                len(
                    [
                        path
                        for path in (plugin / "skills").iterdir()
                        if path.is_dir() and (path / "SKILL.md").is_file()
                    ]
                ),
                58,
            )
            self.assertTrue((plugin / "hooks" / "hooks.json").is_file())
            snapshot = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import sys;"
                        f"sys.path.insert(0, {str(plugin / 'scripts')!r});"
                        "from validate_package import release_snapshot;"
                        "print(release_snapshot()[0])"
                    ),
                ],
                text=True,
                capture_output=True,
                check=False,
                env=os.environ.copy(),
                timeout=30,
            )
            self.assertEqual(snapshot.returncode, 0, msg=snapshot.stderr)
            from scripts.validate_package import release_snapshot

            self.assertEqual(
                snapshot.stdout.strip(),
                release_snapshot()[0],
            )
            marketplace = json.loads(
                (
                    agents_home / "plugins" / "marketplace.json"
                ).read_text(encoding="utf-8")
            )
            entry = next(
                item
                for item in marketplace["plugins"]
                if item["name"] == "mawcodex"
            )
            self.assertEqual(entry["source"]["path"], "./plugins/mawcodex")
            resolved_source = (
                agents_home.parent / entry["source"]["path"]
            ).resolve()
            self.assertEqual(resolved_source, plugin.resolve())
            self.assertEqual(entry["policy"]["installation"], "AVAILABLE")

    def test_existing_install_requires_explicit_update(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_parent = root / "plugins"
            agents_home = root / ".agents"
            first = self.run_installer(
                plugin_parent,
                agents_home,
                "--apply",
            )
            self.assertEqual(first.returncode, 0, msg=first.stderr)
            second = self.run_installer(
                plugin_parent,
                agents_home,
                "--apply",
            )
            self.assertEqual(second.returncode, 2)
            self.assertIn("already exists", second.stderr)

    def test_existing_named_catalog_and_entries_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_parent = root / "plugins"
            agents_home = root / ".agents"
            marketplace_path = (
                agents_home / "plugins" / "marketplace.json"
            )
            marketplace_path.parent.mkdir(parents=True)
            original_entry = {
                "name": "existing-plugin",
                "source": {
                    "source": "local",
                    "path": "./plugins/existing-plugin",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
            marketplace_path.write_text(
                json.dumps(
                    {
                        "name": "giovanni-local-marketplace",
                        "interface": {
                            "displayName": "Giovanni Local Plugins"
                        },
                        "plugins": [original_entry],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = self.run_installer(
                plugin_parent,
                agents_home,
                "--apply",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            marketplace = json.loads(
                marketplace_path.read_text(encoding="utf-8")
            )
            self.assertEqual(
                marketplace["name"],
                "giovanni-local-marketplace",
            )
            self.assertEqual(
                marketplace["interface"]["displayName"],
                "Giovanni Local Plugins",
            )
            self.assertEqual(marketplace["plugins"][0], original_entry)
            self.assertEqual(
                [item["name"] for item in marketplace["plugins"]],
                ["existing-plugin", "mawcodex"],
            )


if __name__ == "__main__":
    unittest.main()
