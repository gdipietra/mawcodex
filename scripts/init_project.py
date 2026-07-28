#!/usr/bin/env python3
"""Initialize an academic project from the MAW Codex stable template.

The initializer never overwrites a differing file. Existing non-empty
destinations require ``--merge`` and still receive a complete conflict
preflight before any write occurs.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_TEMPLATE = ROOT / "assets" / "project-template"
ARTIFACT_TEMPLATES = ROOT / "assets" / "templates"
AGENTS = ROOT / ".codex" / "agents"
CONFIG = ROOT / ".codex" / "config.toml"
REFERENCES = ROOT / "references"


@dataclass(frozen=True)
class Copy:
    source: Path
    relative_target: Path


def hash_file(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def collect_tree(source_root: Path, target_root: Path) -> list[Copy]:
    return [
        Copy(path, target_root / path.relative_to(source_root))
        for path in sorted(source_root.rglob("*"))
        if path.is_file()
    ]


def build_plan(
    *,
    include_agents: bool,
    include_references: bool,
) -> list[Copy]:
    copies = collect_tree(PROJECT_TEMPLATE, Path())
    copies.extend(collect_tree(ARTIFACT_TEMPLATES, Path("templates")))
    if include_agents:
        copies.extend(
            Copy(path, Path(".codex") / "agents" / path.name)
            for path in sorted(AGENTS.glob("*.toml"))
        )
        copies.append(Copy(CONFIG, Path(".codex") / "config.toml"))
    if include_references:
        copies.extend(collect_tree(REFERENCES, Path("references")))
    return sorted(copies, key=lambda item: item.relative_target.as_posix())


def require_git() -> str:
    git = shutil.which("git")
    if not git:
        raise RuntimeError(
            "Git is unavailable; no project files were written."
        )
    check = subprocess.run(
        [git, "--version"],
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode != 0:
        raise RuntimeError(
            "Git could not run; no project files were written: "
            + (check.stderr or check.stdout).strip()
        )
    return git


def initialize_git(destination: Path, git: str) -> None:
    result = subprocess.run(
        [git, "init", "-b", "main", str(destination)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        result = subprocess.run(
            [git, "init", str(destination)],
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        raise RuntimeError(
            "git init failed: "
            + result.stderr.strip()
        )


def rollback_created(
    destination: Path,
    created_files: list[Path],
    *,
    remove_git: bool,
    destination_preexisted: bool,
) -> None:
    if remove_git:
        git_directory = destination / ".git"
        if git_directory.is_dir() and git_directory.parent == destination:
            shutil.rmtree(git_directory)
    for path in reversed(created_files):
        path.unlink(missing_ok=True)
    directories = sorted(
        {
            parent
            for path in created_files
            for parent in path.parents
            if parent != destination and destination in parent.parents
        },
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        try:
            directory.rmdir()
        except OSError:
            pass
    if not destination_preexisted:
        try:
            destination.rmdir()
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    parser.add_argument(
        "--merge",
        action="store_true",
        help="allow adding missing files to a non-empty destination",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show the complete copy plan without writing",
    )
    parser.add_argument(
        "--without-agents",
        action="store_true",
        help="omit the 19 project custom-agent definitions and config",
    )
    parser.add_argument(
        "--without-references",
        action="store_true",
        help="omit portable rules and agent-role references",
    )
    parser.add_argument(
        "--git-init",
        action="store_true",
        help="initialize a local Git repository after copying",
    )
    args = parser.parse_args()

    destination = args.destination.resolve()
    if destination.exists() and not destination.is_dir():
        raise SystemExit(f"destination is not a directory: {destination}")
    nonempty = (
        destination.exists()
        and any(destination.iterdir())
    )
    if nonempty and not args.merge:
        raise SystemExit(
            "destination is not empty; use --merge to add only missing files"
        )

    plan = build_plan(
        include_agents=not args.without_agents,
        include_references=not args.without_references,
    )
    conflicts: list[Path] = []
    identical: list[Path] = []
    pending: list[Copy] = []
    for item in plan:
        target = destination / item.relative_target
        if not target.exists():
            pending.append(item)
        elif target.is_file() and hash_file(target) == hash_file(item.source):
            identical.append(item.relative_target)
        else:
            conflicts.append(item.relative_target)

    print(f"Destination: {destination}")
    print(f"Planned files: {len(plan)}")
    print(f"New files: {len(pending)}")
    print(f"Identical files skipped: {len(identical)}")
    if conflicts:
        print("Conflicts (no files written):")
        for conflict in conflicts:
            print(f"  {conflict.as_posix()}")
        return 2
    if args.dry_run:
        for item in pending:
            print(f"ADD  {item.relative_target.as_posix()}")
        print("Dry run complete; no files written.")
        return 0

    git: str | None = None
    git_preexisted = (destination / ".git").exists()
    if args.git_init and not git_preexisted:
        try:
            git = require_git()
        except RuntimeError as error:
            print(f"ERROR  {error}", file=sys.stderr)
            return 3

    destination_preexisted = destination.exists()
    created_files: list[Path] = []
    try:
        destination.mkdir(parents=True, exist_ok=True)
        for item in pending:
            target = destination / item.relative_target
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item.source, target)
            created_files.append(target)
        if git is not None:
            initialize_git(destination, git)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        rollback_created(
            destination,
            created_files,
            remove_git=git is not None and not git_preexisted,
            destination_preexisted=destination_preexisted,
        )
        print(
            f"ERROR  initialization rolled back: {error}",
            file=sys.stderr,
        )
        return 3
    print(
        f"Initialized {destination} with {len(pending)} new file(s). "
        "Review AGENTS.md and README.md before beginning research."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
