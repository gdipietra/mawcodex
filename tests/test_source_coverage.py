"""Ensure every file at the fixed upstream commit has a disposition."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
CONVERSION = ROOT / "docs" / "conversion"


class FixedSourceCoverageTests(unittest.TestCase):
    def test_every_tracked_source_file_is_in_exactly_one_manifest(self) -> None:
        tracked = set(
            subprocess.check_output(
                [
                    "git",
                    "-c",
                    f"safe.directory={SOURCE.as_posix()}",
                    "-C",
                    str(SOURCE),
                    "ls-files",
                ],
                text=True,
            ).splitlines()
        )
        component = json.loads(
            (CONVERSION / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        project = json.loads(
            (CONVERSION / "PROJECT_TEMPLATE_MANIFEST.json").read_text(
                encoding="utf-8"
            )
        )
        runtime = json.loads(
            (CONVERSION / "RUNTIME_SURFACES_MANIFEST.json").read_text(
                encoding="utf-8"
            )
        )
        auxiliary = json.loads(
            (CONVERSION / "AUXILIARY_SOURCE_MANIFEST.json").read_text(
                encoding="utf-8"
            )
        )
        groups = [
            {record["source"] for record in component["components"]},
            {record["source"] for record in project["files"]},
            {record["source"] for record in runtime["surfaces"]},
            {record["source"] for record in auxiliary["files"]},
        ]
        union: set[str] = set()
        for group in groups:
            self.assertTrue(union.isdisjoint(group))
            union.update(group)
        self.assertEqual(union, tracked)
        self.assertEqual(len(union), 211)


if __name__ == "__main__":
    unittest.main()
