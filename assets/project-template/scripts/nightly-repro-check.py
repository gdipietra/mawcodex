#!/usr/bin/env python3
"""Flag passport claims whose recorded inputs changed after verification.

This inexpensive check does not rerun analysis and therefore cannot establish
that a claim is correct. A stale result requires `$audit-reproducibility`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


FIELD = re.compile(
    r"\s*(source_file|output_file|last_verified_on):\s*(.+)"
)
CLAIM = re.compile(r"\s*-\s*id:\s*(.+)")


def parse_iso(value: str) -> float | None:
    value = value.strip().strip("\"'")
    date_only = "T" not in value and ":" not in value
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if date_only:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.timestamp()


def check_passport(passport: Path, root: Path) -> list[str]:
    stale: list[str] = []
    current: dict[str, str | float | None] = {}

    def flush() -> None:
        last_verified = current.get("last_verified_on")
        if not isinstance(last_verified, float):
            return
        for key in ("source_file", "output_file"):
            value = current.get(key)
            if not isinstance(value, str):
                continue
            candidate = root / value
            if candidate.exists() and candidate.stat().st_mtime > last_verified:
                stale.append(
                    f"{passport.name}: {current.get('id', '?')} — "
                    f"{value} is newer than last_verified_on"
                )

    for line in passport.read_text(
        encoding="utf-8", errors="replace"
    ).splitlines():
        claim = CLAIM.match(line)
        if claim:
            flush()
            current = {"id": claim.group(1).strip()}
            continue
        field = FIELD.match(line)
        if field:
            key, value = field.group(1), field.group(2).strip()
            current[key] = (
                parse_iso(value) if key == "last_verified_on" else value
            )
    flush()
    return stale


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project",
        nargs="?",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()
    root = args.project.resolve()
    passport_directory = root / "quality_reports" / "passports"
    if not passport_directory.is_dir():
        print("No quality_reports/passports directory; nothing to check.")
        return 0
    passports = sorted(passport_directory.glob("*.yaml"))
    stale = [
        finding
        for passport in passports
        for finding in check_passport(passport, root)
    ]
    if stale:
        print("STALE claims (run $audit-reproducibility):")
        for finding in stale:
            print(f"  {finding}")
        return 1
    print(
        "No tracked source/output is newer than its passport verification "
        "date. This is a freshness check, not a correctness audit."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
