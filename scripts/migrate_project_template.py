#!/usr/bin/env python3
"""Import the portable academic project assets from the fixed source fork.

This is a conversion-time tool, not an installer. By default it refuses to
overwrite previously reviewed target files. Pass ``--refresh`` only when
starting a documented upstream-refresh cycle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from check_source_clone import GitCheckError, inspect as inspect_source_clone


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
EXPECTED_COMMIT = "be53c12f235996dff41fb7f21580506fd2dd8d50"

SOURCE_TO_TARGET = {
    "Bibliography_base.bib": "assets/project-template/Bibliography_base.bib",
    "Preambles/header.tex": "assets/project-template/Preambles/header.tex",
    "Preambles/README.md": "assets/project-template/Preambles/README.md",
    "Quarto/HelloWorld.qmd": "assets/project-template/Quarto/HelloWorld.qmd",
    "Quarto/theme-template.scss": (
        "assets/project-template/Quarto/theme-template.scss"
    ),
    "Slides/HelloWorld.tex": "assets/project-template/Slides/HelloWorld.tex",
    "scripts/R/00_run_all.R": (
        "assets/project-template/scripts/R/00_run_all.R"
    ),
    "scripts/R/01_load.R": "assets/project-template/scripts/R/01_load.R",
    "scripts/R/02_clean.R": "assets/project-template/scripts/R/02_clean.R",
    "scripts/R/03_analyze.R": (
        "assets/project-template/scripts/R/03_analyze.R"
    ),
    "scripts/R/04_tables.R": "assets/project-template/scripts/R/04_tables.R",
    "scripts/R/05_figures.R": (
        "assets/project-template/scripts/R/05_figures.R"
    ),
    "scripts/R/README.md": "assets/project-template/scripts/R/README.md",
    "scripts/check-palette-sync.py": (
        "assets/project-template/scripts/check-palette-sync.py"
    ),
    "scripts/check-tikz-prevention.py": (
        "assets/project-template/scripts/check-tikz-prevention.py"
    ),
    "scripts/quality_score.py": (
        "assets/project-template/scripts/quality_score.py"
    ),
    "explorations/README.md": (
        "assets/project-template/explorations/README.md"
    ),
    "quality_reports/did_validation.md": (
        "docs/conversion/upstream-evidence/did-event-study-validation.md"
    ),
}

TEXT_REPLACEMENTS = (
    (".claude/rules/quality-gates.md", "references/rules/quality-gates.md"),
    ("/audit-reproducibility", "$audit-reproducibility"),
    ("/translate-to-quarto", "$translate-to-quarto"),
    ("/compile-latex", "$compile-latex"),
    ("/extract-tikz", "$extract-tikz"),
    ("/new-diagram", "$new-diagram"),
    ("/review-r", "$review-r"),
    ("/deploy", "$deploy"),
    (
        "- See `.claude/rules/exploration-folder-protocol.md` for the full "
        "protocol",
        "- Use the MAW Codex exploration-folder protocol for the full rules",
    ),
    (
        "- See `.claude/rules/exploration-fast-track.md` for the lightweight "
        "workflow",
        "- Use the MAW Codex exploration fast track for lightweight work",
    ),
    ("scripts/check-palette-sync.sh", "scripts/check-palette-sync.py"),
    (
        "./scripts/check-palette-sync.py",
        "python scripts/check-palette-sync.py",
    ),
    (
        "./scripts/validate-setup.sh",
        "python scripts/validate-project.py",
    ),
    ("inside Claude Code", "with Codex"),
)

XETEX_FONT_ANCHOR = r"""\ifPDFTeX
  \usepackage[utf8]{inputenc}
\fi

"""
XETEX_FONT_FALLBACK = r"""\ifXeTeX
  \usepackage{fontspec}
  \defaultfontfeatures{Scale=MatchLowercase,Ligatures=TeX}

  % XeLaTeX is strict about font names. Use Lato when available, then Helvetica-family
  % fallbacks, and keep TeX defaults as final fallback (no hard failure).
  \IfFontExistsTF{Lato}{%
    \setmainfont{Lato}%
  }{%
    \IfFontExistsTF{Helvetica}{%
      \setmainfont{Helvetica}%
    }{%
      \IfFontExistsTF{Helvetica Neue}{%
        \setmainfont{Helvetica Neue}%
      }{%
        \IfFontExistsTF{Arial}{%
          \setmainfont{Arial}%
        }{}%
      }%
    }%
  }%

  \IfFontExistsTF{Lato}{%
    \setsansfont{Lato}%
  }{%
    \IfFontExistsTF{Helvetica Neue}{%
      \setsansfont{Helvetica Neue}%
    }{%
      \IfFontExistsTF{Helvetica}{%
        \setsansfont{Helvetica}%
      }{%
        \IfFontExistsTF{Arial}{%
          \setsansfont{Arial}%
        }{}%
      }%
    }%
  }%
\fi

"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(data: bytes, mode: str) -> bytes:
    if mode == "raw-bytes":
        return data
    if mode != "utf-8-lf":
        raise ValueError(f"unsupported hash mode: {mode}")
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


SKILL_INVOCATION = re.compile(r"(?<!\\)\$([a-z][a-z0-9-]*)\b")


def split_tex_comment(line: str) -> tuple[str, str]:
    """Split a TeX line before its first unescaped comment marker."""

    for index, character in enumerate(line):
        if character != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index], line[index:]
    return line, ""


def escape_tex_skill_invocations(text: str) -> str:
    """Escape Codex skill sigils in TeX content, but not TeX comments."""

    converted: list[str] = []
    for line in text.splitlines(keepends=True):
        content, comment = split_tex_comment(line)
        converted.append(SKILL_INVOCATION.sub(r"\\$\1", content) + comment)
    return "".join(converted)


def insert_xetex_font_fallback(text: str) -> tuple[str, int]:
    """Insert the reviewed XeLaTeX font fallback after the pdfTeX guard."""

    count = text.count(XETEX_FONT_ANCHOR)
    if count != 1:
        raise ValueError(
            "Preambles/header.tex must contain exactly one engine guard"
        )
    return (
        text.replace(
            XETEX_FONT_ANCHOR,
            XETEX_FONT_ANCHOR + XETEX_FONT_FALLBACK,
        ),
        count,
    )


def adapt_text(
    text: str,
    target_relative: str | None = None,
) -> tuple[str, list[dict[str, int | str]]]:
    applied: list[dict[str, int | str]] = []
    for old, new in TEXT_REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            applied.append({"from": old, "to": new, "count": count})
    if target_relative == "assets/project-template/Preambles/header.tex":
        text, count = insert_xetex_font_fallback(text)
        applied.append(
            {
                "operation": "insert-xetex-font-fallback",
                "from": "pdfTeX inputenc engine guard",
                "to": "guarded fontspec Lato/Helvetica/Arial fallback",
                "count": count,
            }
        )
    if target_relative and Path(target_relative).suffix.lower() == ".tex":
        before = text
        text = escape_tex_skill_invocations(text)
        count = text.count(r"\$") - before.count(r"\$")
        if count:
            applied.append(
                {
                    "operation": "escape-tex-skill-invocations",
                    "from": "$skill in TeX content",
                    "to": r"\$skill",
                    "count": count,
                }
            )
    return text, applied


def convert(
    source_root: Path,
    *,
    refresh: bool,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for source_relative, target_relative in SOURCE_TO_TARGET.items():
        source = source_root / Path(source_relative)
        target = ROOT / Path(target_relative)
        if not source.is_file():
            raise FileNotFoundError(f"required source asset missing: {source}")
        if target.exists() and not refresh:
            raise FileExistsError(
                f"reviewed target exists: {target}; use --refresh only in "
                "an upstream-refresh cycle"
            )
        source_bytes = source.read_bytes()
        replacements: list[dict[str, int | str]] = []
        try:
            decoded = source_bytes.decode("utf-8")
        except UnicodeDecodeError:
            hash_mode = "raw-bytes"
            target_bytes = source_bytes
        else:
            hash_mode = "utf-8-lf"
            decoded = canonical_bytes(source_bytes, hash_mode).decode("utf-8")
            adapted, replacements = adapt_text(decoded, target_relative)
            target_bytes = adapted.replace("\r\n", "\n").encode("utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(target_bytes)
        records.append(
            {
                "source": source_relative,
                "source_sha256": digest(
                    canonical_bytes(source_bytes, hash_mode)
                ),
                "target": target_relative,
                "target_sha256": digest(
                    canonical_bytes(target_bytes, hash_mode)
                ),
                "hash_mode": hash_mode,
                "replacements": replacements,
                "classification": (
                    "direct port" if not replacements else "native rewrite"
                ),
                "revision_summary": (
                    f"Imported {target_relative} unchanged from the fixed baseline."
                    if not replacements
                    else f"Adapted {target_relative} for Codex-native paths, syntax, and project behavior."
                ),
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="path to the read-only upstream-tracking clone",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="overwrite imported targets during a documented refresh",
    )
    args = parser.parse_args()
    source_root = args.source.resolve()
    try:
        source_contract = inspect_source_clone(source_root, fetch=False)
    except (GitCheckError, OSError, ValueError) as error:
        raise SystemExit(f"source contract check failed: {error}") from error
    if not source_contract["ok"]:
        raise SystemExit(
            "source contract check failed: "
            + "; ".join(str(item) for item in source_contract["errors"])
        )
    records = convert(source_root, refresh=args.refresh)
    manifest = {
        "schema_version": 3,
        "source_repository": (
            "https://github.com/pedrohcgs/claude-code-my-workflow"
        ),
        "source_commit": EXPECTED_COMMIT,
        "generated_by": "scripts/migrate_project_template.py",
        "files": records,
    }
    manifest_path = (
        ROOT / "docs" / "conversion" / "PROJECT_TEMPLATE_MANIFEST.json"
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Imported {len(records)} source assets.")
    print(f"Wrote {manifest_path.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
