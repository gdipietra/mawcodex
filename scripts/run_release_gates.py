#!/usr/bin/env python3
"""Run MAW Codex's reproducible local stable-release gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from check_source_clone import (
    BASELINE_COMMIT,
    GitCheckError,
    WINDOWS_DEFAULT,
    inspect,
)
from validate_package import PACKAGED_SKILL_COUNT, release_snapshot


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_VALIDATOR = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "plugin-creator"
    / "scripts"
    / "validate_plugin.py"
)
DEFAULT_SKILL_VALIDATOR = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)
EVIDENCE = (
    ROOT / "docs" / "conversion" / "OFFICIAL_VALIDATION.json"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def run(
    arguments: list[str],
    *,
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=environment,
        timeout=300,
    )


def show(label: str, process: subprocess.CompletedProcess[str]) -> None:
    output = "\n".join(
        part.strip()
        for part in (process.stdout, process.stderr)
        if part and part.strip()
    )
    if output:
        print(f"\n[{label}]\n{output}")


def require_pass(
    label: str,
    process: subprocess.CompletedProcess[str],
) -> None:
    show(label, process)
    if process.returncode:
        raise RuntimeError(
            f"{label} returned exit code {process.returncode}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the fixed-source check, package validator, official Codex "
            "validators, unit tests, and final stable-release validation."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            os.environ.get("MAWCODEX_SOURCE_CLONE", WINDOWS_DEFAULT)
        ),
        help="fixed upstream-tracking clone",
    )
    parser.add_argument(
        "--plugin-validator",
        type=Path,
        default=DEFAULT_PLUGIN_VALIDATOR,
    )
    parser.add_argument(
        "--skill-validator",
        type=Path,
        default=DEFAULT_SKILL_VALIDATOR,
    )
    args = parser.parse_args()

    source = args.source.resolve()
    plugin_validator = args.plugin_validator.resolve()
    skill_validator = args.skill_validator.resolve()
    for label, path in (
        ("official plugin validator", plugin_validator),
        ("official skill validator", skill_validator),
    ):
        if not path.is_file():
            print(f"FAIL  {label} unavailable: {path}", file=sys.stderr)
            return 2

    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["MAWCODEX_SOURCE_CLONE"] = str(source)
    bundled_yaml = Path(os.environ.get("TEMP", "")) / (
        "mawcodex-validation-deps"
    )
    if bundled_yaml.is_dir():
        old_python_path = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            str(bundled_yaml)
            if not old_python_path
            else os.pathsep.join((str(bundled_yaml), old_python_path))
        )

    try:
        source_result = inspect(source, fetch=False)
    except (GitCheckError, OSError, subprocess.SubprocessError) as error:
        print(f"FAIL  source clone check failed: {error}", file=sys.stderr)
        return 2
    if not source_result.get("ok"):
        for error in source_result.get("errors", []):
            print(f"FAIL  {error}", file=sys.stderr)
        return 2
    print(
        "PASS  source clone matches the fork/upstream contract at "
        f"{BASELINE_COMMIT}"
    )

    preliminary = run(
        [sys.executable, str(ROOT / "scripts" / "validate_package.py")],
        environment=environment,
    )
    try:
        require_pass("package validation", preliminary)

        plugin = run(
            [sys.executable, str(plugin_validator), str(ROOT)],
            environment=environment,
        )
        require_pass("official plugin validator", plugin)

        skills = run(
            [
                sys.executable,
                str(ROOT / "scripts" / "run_skill_validators.py"),
                "--validator",
                str(skill_validator),
                "--json",
            ],
            environment=environment,
        )
        require_pass("official skill validator", skills)
        skill_document = json.loads(skills.stdout)
        if (
            not skill_document.get("ok")
            or skill_document.get("passed") != PACKAGED_SKILL_COUNT
            or skill_document.get("failed") != 0
        ):
            raise RuntimeError(
                "official skill validator did not report "
                f"{PACKAGED_SKILL_COUNT}/{PACKAGED_SKILL_COUNT} passes"
            )

        tests = run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-v",
            ],
            environment=environment,
        )
        require_pass("unit tests", tests)
    except (RuntimeError, json.JSONDecodeError) as error:
        print(f"\nFAIL  {error}", file=sys.stderr)
        return 1

    test_output = "\n".join((tests.stdout, tests.stderr))
    count_match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    if not count_match:
        print("FAIL  could not determine unit-test count", file=sys.stderr)
        return 1
    test_count = int(count_match.group(1))
    skipped_match = re.search(r"skipped=(\d+)", test_output)
    skipped = int(skipped_match.group(1)) if skipped_match else 0
    if test_count < 10:
        print(
            f"FAIL  stable evidence requires at least 10 tests, found "
            f"{test_count}",
            file=sys.stderr,
        )
        return 1
    if skipped:
        print(
            f"FAIL  stable evidence requires zero skipped tests, found "
            f"{skipped}",
            file=sys.stderr,
        )
        return 1

    manifest = json.loads(
        (ROOT / ".codex-plugin" / "plugin.json").read_text(
            encoding="utf-8"
        )
    )
    snapshot_digest, snapshot_file_count = release_snapshot()
    evidence = {
        "schema_version": 1,
        "package_version": manifest["version"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plugin_validator": {
            "result": "PASS",
            "path": str(plugin_validator),
            "validator_sha256": digest(plugin_validator),
        },
        "skill_validator": {
            "result": "PASS",
            "passed": PACKAGED_SKILL_COUNT,
            "total": PACKAGED_SKILL_COUNT,
            "path": str(skill_validator),
            "validator_sha256": digest(skill_validator),
        },
        "source_contract": {
            "result": "PASS",
            "commit": BASELINE_COMMIT,
            "path": str(source),
            "origin": source_result["origin"],
            "upstream": source_result["upstream"],
        },
        "unit_tests": {
            "result": "PASS",
            "count": test_count,
            "skipped": skipped,
        },
        "release_snapshot": {
            "algorithm": "sha256",
            "digest": snapshot_digest,
            "file_count": snapshot_file_count,
        },
    }
    previous_evidence = EVIDENCE.read_bytes() if EVIDENCE.is_file() else None
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".OFFICIAL_VALIDATION.",
        suffix=".json",
        dir=EVIDENCE.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(evidence, stream, indent=2)
            stream.write("\n")
        temporary.replace(EVIDENCE)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    print(f"\nPASS  wrote official evidence to {EVIDENCE}")

    release = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_package.py"),
            "--release",
        ],
        environment=environment,
    )
    try:
        require_pass("stable release validation", release)
    except RuntimeError as error:
        if previous_evidence is None:
            EVIDENCE.unlink(missing_ok=True)
        else:
            restore_descriptor, restore_name = tempfile.mkstemp(
                prefix=".OFFICIAL_VALIDATION.restore.",
                suffix=".json",
                dir=EVIDENCE.parent,
            )
            restore = Path(restore_name)
            try:
                with os.fdopen(restore_descriptor, "wb") as stream:
                    stream.write(previous_evidence)
                restore.replace(EVIDENCE)
            except Exception:
                restore.unlink(missing_ok=True)
                raise
        print(f"\nFAIL  {error}", file=sys.stderr)
        return 1
    print("\nPASS  MAW Codex satisfies every local stable-release gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
