#!/usr/bin/env python3
"""Deterministic structural checks for a MAW Codex academic project."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md",
    "MEMORY.md",
    ".maw/profile.yaml",
    ".maw/lock.json",
    ".maw/history",
    ".maw/slices",
    "scripts/manageraw-state.py",
    "Preambles/header.tex",
    "Quarto/theme-template.scss",
    "scripts/R/00_run_all.R",
    "scripts/R/01_load.R",
    "scripts/R/02_clean.R",
    "scripts/R/03_analyze.R",
    "scripts/R/04_tables.R",
    "scripts/R/05_figures.R",
    "templates/passport-template.yaml",
    "quality_reports/passports",
    "quality_reports/plans",
    "data/raw",
    "data/derived",
)
RESEARCH_SUFFIXES = {".r", ".rmd", ".qmd", ".do", ".py", ".jl"}
MACHINE_PATH = re.compile(
    r"(/Users/[^/\s'\")]+|/home/[^/\s'\")]+|"
    r"[A-Za-z]:\\Users\\[^\\\s'\"]+)"
)
PROVIDER_ARTIFACTS = (".claude", "CLAUDE.md")
SENSITIVE_NAMES = re.compile(
    r"(?i)(^|/)(\.env($|\.)|.*\.(pem|key)|"
    r"(credentials?|secrets?|tokens?)\.(json|ya?ml|txt))$"
)


class Results:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def require(self, condition: bool, passed: str, failed: str) -> None:
        if condition:
            self.passes.append(passed)
        else:
            self.failures.append(failed)


def research_files() -> list[Path]:
    roots = [
        ROOT / "scripts" / "R",
        ROOT / "Figures",
        ROOT / "explorations",
    ]
    files: list[Path] = []
    for directory in roots:
        if not directory.exists():
            continue
        files.extend(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in RESEARCH_SUFFIXES
        )
    return sorted(files)


def tracked_paths() -> list[str] | None:
    git = shutil.which("git")
    if not git or not (ROOT / ".git").exists():
        return None
    result = subprocess.run(
        [git, "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return [
        item.decode("utf-8", errors="replace").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    ]


def main() -> int:
    results = Results()
    for relative in REQUIRED:
        path = ROOT / relative
        results.require(
            path.exists(),
            f"required path present: {relative}",
            f"required path missing: {relative}",
        )

    for provider_artifact in PROVIDER_ARTIFACTS:
        results.require(
            not (ROOT / provider_artifact).exists(),
            f"no legacy provider artifact: {provider_artifact}",
            f"legacy provider artifact present: {provider_artifact}",
        )

    offenders: list[str] = []
    for path in research_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        match = MACHINE_PATH.search(text)
        if match:
            offenders.append(
                f"{path.relative_to(ROOT).as_posix()} ({match.group(0)})"
            )
    results.require(
        not offenders,
        "research code contains no machine-specific user paths",
        "machine-specific paths found: " + ", ".join(offenders),
    )

    palette_check = ROOT / "scripts" / "check-palette-sync.py"
    if palette_check.is_file():
        palette = subprocess.run(
            [sys.executable, str(palette_check)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        results.require(
            palette.returncode == 0,
            "Beamer and Quarto palettes agree",
            "palette synchronization failed: "
            + (palette.stderr or palette.stdout).strip(),
        )
    else:
        results.failures.append("palette checker is missing")

    manageraw_check = ROOT / "scripts" / "manageraw-state.py"
    if manageraw_check.is_file():
        manageraw = subprocess.run(
            [
                sys.executable,
                str(manageraw_check),
                "validate",
                "--project",
                str(ROOT),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        results.require(
            manageraw.returncode == 0,
            "ManageRAW project state is valid",
            "ManageRAW state validation failed: "
            + (manageraw.stderr or manageraw.stdout).strip(),
        )
    else:
        results.failures.append("ManageRAW state validator is missing")

    tracked = tracked_paths()
    if tracked is None:
        results.warnings.append(
            "Git tracking checks skipped: repository or Git unavailable"
        )
    else:
        sensitive = [path for path in tracked if SENSITIVE_NAMES.search(path)]
        raw_files = [
            path
            for path in tracked
            if path.startswith("data/raw/") and not path.endswith("/.gitkeep")
        ]
        results.require(
            not sensitive,
            "no obvious credential files are tracked",
            "potential credential files tracked: " + ", ".join(sensitive),
        )
        results.require(
            not raw_files,
            "no raw data files are tracked by default",
            "raw data files tracked; document and review explicitly: "
            + ", ".join(raw_files),
        )

    for message in results.passes:
        print(f"PASS  {message}")
    for message in results.warnings:
        print(f"WARN  {message}")
    for message in results.failures:
        print(f"FAIL  {message}")
    print(
        f"\nSummary: {len(results.passes)} passed, "
        f"{len(results.warnings)} warned, "
        f"{len(results.failures)} failed."
    )
    return 1 if results.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
