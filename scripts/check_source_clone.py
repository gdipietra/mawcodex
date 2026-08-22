#!/usr/bin/env python3
"""Check the immutable upstream-tracking clone and report newer Pedro changes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


BASELINE_COMMIT = "be53c12f235996dff41fb7f21580506fd2dd8d50"
EXPECTED_TAG = "v2.1.0"
EXPECTED_ORIGIN = "https://github.com/gdipietra/claude-code-my-workflow"
EXPECTED_UPSTREAM = "https://github.com/pedrohcgs/claude-code-my-workflow"
WINDOWS_DEFAULT = Path(r"C:\GitHub\claude-code-my-workflow")


class GitCheckError(RuntimeError):
    """Raised when the source clone does not satisfy its tracking contract."""


def run_git(source: Path, *arguments: str) -> str:
    command = [
        "git",
        "-c",
        f"safe.directory={source.as_posix()}",
        "-C",
        str(source),
        *arguments,
    ]
    process = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    if process.returncode:
        detail = (process.stderr or process.stdout).strip()
        raise GitCheckError(
            f"`git {' '.join(arguments)}` failed: {detail or 'no detail'}"
        )
    return process.stdout.strip()


def normalized_url(value: str) -> str:
    return value.strip().removesuffix(".git").rstrip("/")


def inspect(source: Path, fetch: bool) -> dict[str, object]:
    if not source.is_dir():
        raise GitCheckError(f"source clone does not exist: {source}")
    if fetch:
        run_git(source, "fetch", "upstream", "--tags", "--prune")

    origin = run_git(source, "remote", "get-url", "origin")
    upstream = run_git(source, "remote", "get-url", "upstream")
    head = run_git(source, "rev-parse", "HEAD")
    branch = run_git(source, "branch", "--show-current")
    dirty = run_git(source, "status", "--porcelain")
    tags = run_git(source, "tag", "--points-at", "HEAD").splitlines()

    errors: list[str] = []
    if normalized_url(origin) != EXPECTED_ORIGIN:
        errors.append(f"origin is {origin!r}, expected Giovanni's fork")
    if normalized_url(upstream) != EXPECTED_UPSTREAM:
        errors.append(f"upstream is {upstream!r}, expected Pedro's repository")
    if head != BASELINE_COMMIT:
        errors.append(f"HEAD is {head}, expected fixed baseline {BASELINE_COMMIT}")
    if branch != "main":
        errors.append(f"branch is {branch!r}, expected 'main'")
    if dirty:
        errors.append("source working tree contains local changes")
    if EXPECTED_TAG not in tags:
        errors.append(
            f"baseline tag {EXPECTED_TAG!r} does not point at HEAD"
        )

    upstream_head: str | None = None
    commits_available: int | None = None
    try:
        upstream_head = run_git(source, "rev-parse", "upstream/main")
        commits_available = int(
            run_git(
                source,
                "rev-list",
                "--count",
                f"{BASELINE_COMMIT}..upstream/main",
            )
        )
    except (GitCheckError, ValueError):
        # A fresh clone may not have fetched the upstream namespace yet.
        pass

    return {
        "ok": not errors,
        "source": str(source.resolve()),
        "origin": origin,
        "upstream": upstream,
        "branch": branch,
        "head": head,
        "baseline": BASELINE_COMMIT,
        "tags_at_head": tags,
        "working_tree_clean": not dirty,
        "upstream_main": upstream_head,
        "commits_available_since_baseline": commits_available,
        "fetched": fetch,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the read-only conversion source and optionally fetch "
            "upstream refs without merging them."
        )
    )
    default_source = (
        Path(os.environ["MAWCODEX_SOURCE_CLONE"])
        if "MAWCODEX_SOURCE_CLONE" in os.environ
        else WINDOWS_DEFAULT if os.name == "nt" else None
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=default_source,
        help=(
            "source clone path; defaults to MAWCODEX_SOURCE_CLONE or the "
            "documented Windows location"
        ),
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="fetch upstream refs and tags; never merge or change HEAD",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.source is None:
        parser.error(
            "source path is required outside Windows unless "
            "MAWCODEX_SOURCE_CLONE is set"
        )

    try:
        result = inspect(args.source.resolve(), args.fetch)
    except (GitCheckError, OSError, subprocess.SubprocessError) as error:
        result = {"ok": False, "errors": [str(error)]}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("ok"):
            print("PASS  source clone matches the fixed tracking contract")
            print(f"      origin:   {result['origin']}")
            print(f"      upstream: {result['upstream']}")
            print(f"      baseline: {result['head']}")
            available = result.get("commits_available_since_baseline")
            if available is None:
                print(
                    "INFO  upstream/main is not available locally; rerun with "
                    "--fetch when network access is authorized"
                )
            elif available:
                print(
                    f"INFO  {available} upstream commit(s) are available for "
                    "review; the fixed source was not changed"
                )
            else:
                print("PASS  no newer upstream commits are visible")
        else:
            for error in result.get("errors", []):
                print(f"FAIL  {error}")
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
