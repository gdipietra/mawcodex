"""Cross-platform provenance contracts for imported project assets."""

from __future__ import annotations

import hashlib
import json
import os
import unittest
from pathlib import Path

from scripts.validate_package import canonical_project_bytes


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
MANIFEST = (
    ROOT / "docs" / "conversion" / "PROJECT_TEMPLATE_MANIFEST.json"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ProjectProvenancePortabilityTests(unittest.TestCase):
    def test_utf8_hashes_are_identical_for_lf_and_crlf(self) -> None:
        lf = b"alpha\nbeta\ngamma\n"
        crlf = lf.replace(b"\n", b"\r\n")
        self.assertEqual(
            canonical_project_bytes(lf, "utf-8-lf"),
            canonical_project_bytes(crlf, "utf-8-lf"),
        )

    def test_manifest_hashes_canonical_source_and_target_bytes(self) -> None:
        document = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(document["schema_version"], 2)
        records = document["files"]
        self.assertEqual(len(records), 18)
        for record in records:
            with self.subTest(source=record["source"]):
                mode = record["hash_mode"]
                source_bytes = canonical_project_bytes(
                    (SOURCE / record["source"]).read_bytes(),
                    mode,
                )
                target_bytes = canonical_project_bytes(
                    (ROOT / record["target"]).read_bytes(),
                    mode,
                )
                self.assertEqual(
                    digest(source_bytes),
                    record["source_sha256"],
                )
                self.assertEqual(
                    digest(target_bytes),
                    record["target_sha256"],
                )
                if mode == "utf-8-lf":
                    crlf_source = source_bytes.replace(b"\n", b"\r\n")
                    crlf_target = target_bytes.replace(b"\n", b"\r\n")
                    self.assertEqual(
                        digest(
                            canonical_project_bytes(
                                crlf_source,
                                mode,
                            )
                        ),
                        record["source_sha256"],
                    )
                    self.assertEqual(
                        digest(
                            canonical_project_bytes(
                                crlf_target,
                                mode,
                            )
                        ),
                        record["target_sha256"],
                    )


if __name__ == "__main__":
    unittest.main()
