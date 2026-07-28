"""Provenance contracts for the 13 provider runtime surfaces."""

from __future__ import annotations

import hashlib
import json
import os
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
MANIFEST = (
    ROOT / "docs" / "conversion" / "RUNTIME_SURFACES_MANIFEST.json"
)


def digest_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class RuntimeSurfaceManifestTests(unittest.TestCase):
    def test_all_runtime_surfaces_have_current_source_and_targets(self) -> None:
        document = json.loads(MANIFEST.read_text(encoding="utf-8"))
        surfaces = document["surfaces"]
        self.assertEqual(len(surfaces), 13)
        self.assertEqual(
            Counter(record["kind"] for record in surfaces),
            Counter({"hook": 7, "core": 6}),
        )
        for record in surfaces:
            with self.subTest(surface=record["name"]):
                self.assertEqual(record["status"], "validated")
                self.assertEqual(
                    digest_text(SOURCE / record["source"]),
                    record["source_sha256"],
                )
                self.assertGreaterEqual(len(record["revision_summary"]), 60)
                self.assertTrue(
                    (ROOT / record["revision_record"]).is_file()
                )
                self.assertTrue(record["targets"])
                for target in record["targets"]:
                    path = ROOT / target["path"]
                    self.assertEqual(
                        digest_text(path),
                        target["sha256"],
                    )


if __name__ == "__main__":
    unittest.main()
