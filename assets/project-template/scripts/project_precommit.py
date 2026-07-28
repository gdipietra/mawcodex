#!/usr/bin/env python3
"""Non-mutating pre-commit checks for an academic project.

Unlike stash-based hooks, this helper never changes the working tree. It
examines staged content for sensitive files and machine paths, checks the
staged palette pair directly, and runs quality scoring only when the staged
file is identical to the working-tree file.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE_SUFFIXES = {".r", ".rmd", ".qmd", ".do", ".py", ".jl"}
SCORE_SUFFIXES = {".r", ".qmd", ".tex"}
MACHINE_PATH = re.compile(
    r"(/Users/[^/\s'\")]+|/home/[^/\s'\")]+|"
    r"[A-Za-z]:\\Users\\[^\\\s'\"]+)"
)
SENSITIVE_NAMES = re.compile(
    r"(?i)(^|/)(\.env($|\.)|.*\.(pem|key)|"
    r"(credentials?|secrets?|tokens?)\.(json|ya?ml|txt))$"
)
TEX_COLOR = re.compile(
    r"\\definecolor\{([^}]+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}"
)
SCSS_COLOR = re.compile(
    r"(?m)^\s*\$([A-Za-z0-9_-]+)\s*:\s*#([0-9A-Fa-f]{6})\s*;"
)


def git(*arguments: str) -> subprocess.CompletedProcess[bytes]:
    executable = shutil.which("git")
    if not executable:
        raise SystemExit("pre-commit: Git is unavailable")
    return subprocess.run(
        [executable, "-C", str(ROOT), *arguments],
        capture_output=True,
        check=False,
    )


def staged_paths() -> list[str]:
    result = git(
        "diff",
        "--cached",
        "--name-only",
        "--diff-filter=ACMR",
        "-z",
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.decode(errors="replace").strip())
    return [
        value.decode("utf-8", errors="replace").replace("\\", "/")
        for value in result.stdout.split(b"\0")
        if value
    ]


def staged_text(path: str) -> str:
    result = git("show", f":{path}")
    if result.returncode != 0:
        return ""
    return result.stdout.decode("utf-8", errors="replace")


def has_unstaged_changes(path: str) -> bool:
    return git("diff", "--quiet", "--", path).returncode != 0


def palette(text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    return {
        name.replace("_", "-").lower(): value.upper()
        for name, value in pattern.findall(text)
    }


def main() -> int:
    paths = staged_paths()
    if not paths:
        return 0
    failures: list[str] = []
    warnings: list[str] = []

    for path in paths:
        if SENSITIVE_NAMES.search(path):
            failures.append(f"potential credential file is staged: {path}")
        if path.startswith("data/raw/") and path != "data/raw/.gitkeep":
            failures.append(
                f"raw data is staged: {path}; review and authorize explicitly"
            )
        if Path(path).suffix.lower() in CODE_SUFFIXES:
            match = MACHINE_PATH.search(staged_text(path))
            if match:
                failures.append(
                    f"machine-specific path in {path}: {match.group(0)}"
                )

    tex_path = "Preambles/header.tex"
    scss_path = "Quarto/theme-template.scss"
    if tex_path in paths or scss_path in paths:
        tex_colors = palette(staged_text(tex_path), TEX_COLOR)
        scss_colors = palette(staged_text(scss_path), SCSS_COLOR)
        shared = set(tex_colors) & set(scss_colors)
        drift = [
            name
            for name in sorted(shared)
            if tex_colors[name] != scss_colors[name]
        ]
        if drift:
            failures.append(
                "staged Beamer/Quarto palette values differ: "
                + ", ".join(drift)
            )

    scorer = ROOT / "scripts" / "quality_score.py"
    for path in paths:
        candidate = ROOT / path
        if Path(path).suffix.lower() not in SCORE_SUFFIXES:
            continue
        if not candidate.is_file():
            continue
        if has_unstaged_changes(path):
            warnings.append(
                f"quality score skipped for partially staged file: {path}"
            )
            continue
        result = subprocess.run(
            [sys.executable, str(scorer), str(candidate), "--summary"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
        if result.returncode != 0:
            detail = (result.stdout or result.stderr).strip().splitlines()
            tail = detail[-1] if detail else f"exit {result.returncode}"
            failures.append(f"quality score failed for {path}: {tail}")

    for warning in warnings:
        print(f"WARN  {warning}")
    for failure in failures:
        print(f"FAIL  {failure}", file=sys.stderr)
    if failures:
        print(
            "Commit blocked. Fix the staged content or use --no-verify only "
            "with an explicit, documented reason.",
            file=sys.stderr,
        )
        return 1
    print(f"PASS  pre-commit checks for {len(paths)} staged path(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
