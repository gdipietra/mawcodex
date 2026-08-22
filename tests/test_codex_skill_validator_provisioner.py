from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.provision_codex_skill_validator import install_validator, verify_payload


class CodexSkillValidatorProvisionerTests(unittest.TestCase):
    def test_matching_payload_is_accepted_and_installed_atomically(self) -> None:
        payload = b"pinned validator fixture\n"
        expected = hashlib.sha256(payload).hexdigest()
        self.assertEqual(verify_payload(payload, expected), payload)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "nested" / "quick_validate.py"
            installed = install_validator(destination, payload, expected)
            self.assertEqual(installed, destination.resolve())
            self.assertEqual(destination.read_bytes(), payload)

    def test_hash_mismatch_fails_closed_without_writing(self) -> None:
        payload = b"unexpected validator\n"
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "quick_validate.py"
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                install_validator(destination, payload, "0" * 64)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
