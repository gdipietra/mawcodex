#!/usr/bin/env python3
"""Provision the pinned official OpenAI Codex skill validator for CI.

Source: openai/codex@5e32f728f1f86a967c6be057351f12505778df8f
License: Apache-2.0
"""

from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path


PINNED_URL = (
    "https://raw.githubusercontent.com/openai/codex/"
    "5e32f728f1f86a967c6be057351f12505778df8f/"
    "codex-rs/skills/src/assets/samples/skill-creator/scripts/quick_validate.py"
)
PINNED_SHA256 = "1fd66498c219616fd9249eacdf16c458412ea9065a9d887fd716aeef03907762"


def verify_payload(
    payload: bytes, expected_sha256: str = PINNED_SHA256
) -> bytes:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256:
        raise ValueError(
            f"validator SHA-256 mismatch: found {actual}, expected {expected_sha256}"
        )
    return payload


def download_validator(url: str = PINNED_URL) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "MAW-Codex-validator-provisioner"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def install_validator(
    destination: Path,
    payload: bytes,
    expected_sha256: str = PINNED_SHA256,
) -> Path:
    verified = verify_payload(payload, expected_sha256)
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(verified)
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path(
            os.environ.get(
                "CODEX_SKILL_VALIDATOR",
                tempfile.gettempdir() + "/mawcodex-quick_validate.py",
            )
        ),
    )
    args = parser.parse_args()
    installed = install_validator(args.destination, download_validator())
    print(f"PASS  pinned OpenAI Codex skill validator: {installed}")
    print(f"      sha256: {PINNED_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
