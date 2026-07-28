#!/usr/bin/env python3
"""Run Codex's official quick validator against every packaged skill."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATOR = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validator",
        type=Path,
        default=DEFAULT_VALIDATOR,
        help="path to Codex skill-creator's quick_validate.py",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validator = args.validator.resolve()
    if not validator.is_file():
        raise SystemExit(
            "Codex quick validator not found; pass --validator with its "
            "current installed path."
        )
    skills = sorted(
        path
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    results: list[dict[str, str | int]] = []
    child_environment = os.environ.copy()
    child_environment.setdefault("PYTHONUTF8", "1")
    for skill in skills:
        process = subprocess.run(
            [sys.executable, str(validator), str(skill)],
            text=True,
            capture_output=True,
            check=False,
            env=child_environment,
            timeout=30,
        )
        results.append(
            {
                "skill": skill.name,
                "returncode": process.returncode,
                "output": (process.stdout or process.stderr).strip(),
            }
        )
    failed = [result for result in results if result["returncode"] != 0]
    if args.json:
        print(
            json.dumps(
                {
                    "ok": not failed,
                    "passed": len(results) - len(failed),
                    "failed": len(failed),
                    "results": results,
                },
                indent=2,
            )
        )
    else:
        for result in results:
            status = "PASS" if result["returncode"] == 0 else "FAIL"
            print(f"{status}  {result['skill']}: {result['output']}")
        print(
            f"\nSummary: {len(results) - len(failed)}/{len(results)} passed."
        )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
