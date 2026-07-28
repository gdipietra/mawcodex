#!/usr/bin/env python3
"""Preview or install the project's version-controlled Git hooks."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_git(*arguments: str) -> subprocess.CompletedProcess[str]:
    git = shutil.which("git")
    if not git:
        raise SystemExit("Git is unavailable.")
    return subprocess.run(
        [git, "-C", str(ROOT), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the repository-local core.hooksPath setting",
    )
    args = parser.parse_args()
    if not (ROOT / ".git").exists():
        raise SystemExit("Initialize this project as a Git repository first.")
    hook = ROOT / ".githooks" / "pre-commit"
    if not hook.is_file():
        raise SystemExit(f"Version-controlled hook is missing: {hook}")
    current = run_git("config", "--local", "--get", "core.hooksPath")
    current_value = current.stdout.strip() if current.returncode == 0 else ""
    print(f"Current local core.hooksPath: {current_value or '(unset)'}")
    print("Proposed local core.hooksPath: .githooks")
    if not args.apply:
        print("Preview only. Re-run with --apply to make this local change.")
        return 0
    result = run_git("config", "--local", "core.hooksPath", ".githooks")
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "Git configuration failed.")
    if os.name != "nt":
        hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    print("Installed the repository-local hook path.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
