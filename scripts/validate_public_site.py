#!/usr/bin/env python3
"""Validate the public MAW Codex GitHub Pages source."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PUBLIC_ROOT = "https://dipietra.github.io/mawcodex/"
REPOSITORY = "https://github.com/dipietra/mawcodex"
REQUIRED_HTML = (
    "index.html",
    "capabilities.html",
    "credits.html",
    "privacy.html",
    "terms.html",
    "support.html",
    "404.html",
)
REQUIRED_FILES = REQUIRED_HTML + (
    ".nojekyll",
    "assets/site.css",
    "assets/site.js",
    "assets/capabilities-data.js",
    "assets/brand/maw-icon.png",
)


class SiteParser(HTMLParser):
    """Collect local resource references and duplicate IDs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.has_lang = False
        self.has_charset = False
        self.has_title = False

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = {name: value for name, value in attrs}
        if tag == "html" and values.get("lang") == "en-US":
            self.has_lang = True
        if tag == "meta" and values.get("charset", "").lower() == "utf-8":
            self.has_charset = True
        if tag == "title":
            self.has_title = True
        if values.get("id"):
            self.ids.append(str(values["id"]))
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.references.append((name, value))


def _local_target(source: Path, raw: str) -> Path | None:
    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:", "tel:")):
        return None
    relative = urllib.parse.unquote(parsed.path)
    if not relative:
        return None
    candidate = (source.parent / relative).resolve()
    try:
        candidate.relative_to(DOCS.resolve())
    except ValueError:
        raise ValueError(f"reference escapes docs/: {raw}") from None
    return candidate


def validate(root: Path = ROOT) -> list[str]:
    """Return deterministic public-site problems."""

    global DOCS
    docs = root / "docs"
    previous_docs = DOCS
    DOCS = docs
    problems: list[str] = []
    try:
        for relative in REQUIRED_FILES:
            path = docs / relative
            if not path.is_file():
                problems.append(f"required public-site file missing: docs/{relative}")
            elif relative != ".nojekyll" and path.stat().st_size == 0:
                problems.append(f"required public-site file is empty: docs/{relative}")

        manifest_path = root / ".codex-plugin" / "plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            problems.append(f"plugin manifest unavailable for site validation: {error}")
            manifest = {}
        interface = manifest.get("interface", {})
        expected_urls = {
            "homepage": PUBLIC_ROOT,
            "repository": REPOSITORY,
        }
        for key, expected in expected_urls.items():
            if manifest.get(key) != expected:
                problems.append(f"manifest {key} must be {expected}")
        interface_urls = {
            "websiteURL": PUBLIC_ROOT,
            "privacyPolicyURL": PUBLIC_ROOT + "privacy.html",
            "termsOfServiceURL": PUBLIC_ROOT + "terms.html",
        }
        if not isinstance(interface, dict):
            problems.append("manifest interface must be an object")
            interface = {}
        for key, expected in interface_urls.items():
            if interface.get(key) != expected:
                problems.append(f"manifest interface.{key} must be {expected}")

        for relative in REQUIRED_HTML:
            path = docs / relative
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            parser = SiteParser()
            parser.feed(text)
            if not parser.has_lang:
                problems.append(f"docs/{relative}: html lang must be en-US")
            if not parser.has_charset:
                problems.append(f"docs/{relative}: UTF-8 charset metadata missing")
            if "<title>" not in text or "</title>" not in text:
                problems.append(f"docs/{relative}: title missing")
            duplicates = sorted(
                identifier
                for identifier in set(parser.ids)
                if parser.ids.count(identifier) > 1
            )
            if duplicates:
                problems.append(
                    f"docs/{relative}: duplicate IDs: {', '.join(duplicates)}"
                )
            for attribute, raw in parser.references:
                try:
                    target = _local_target(path, raw)
                except ValueError as error:
                    problems.append(f"docs/{relative}: {error}")
                    continue
                if target is not None and not target.exists():
                    problems.append(
                        f"docs/{relative}: missing {attribute} target {raw}"
                    )

        index = (docs / "index.html").read_text(encoding="utf-8")
        credits = (docs / "credits.html").read_text(encoding="utf-8")
        required_credit_tokens = (
            "Pedro H. C. Sant'Anna",
            "Giovanni Di Pietra",
            "pedrohcgs/claude-code-my-workflow",
            "be53c12f235996dff41fb7f21580506fd2dd8d50",
            "ManageRAW",
            "JAW",
            "CAW",
            "PAW",
            "LAW",
            "UAW",
            "SAW",
            "does not imply",
        )
        combined_credit = index + "\n" + credits
        for token in required_credit_tokens:
            if token not in combined_credit:
                problems.append(f"public credit text omits {token!r}")

        ledger_path = docs / "assets" / "capabilities-data.js"
        ledger = ledger_path.read_text(encoding="utf-8")
        names = re.findall(r'(?m)^\s*name:\s*"([a-z0-9-]+)",$', ledger)
        adapted = len(re.findall(r'(?m)^\s*origin:\s*"adapted",$', ledger))
        native = len(re.findall(r'(?m)^\s*origin:\s*"native",$', ledger))
        if len(names) != 58:
            problems.append(f"capability ledger must contain 58 skills, found {len(names)}")
        if len(set(names)) != len(names):
            problems.append("capability ledger contains duplicate skill names")
        if adapted != 52 or native != 6:
            problems.append(
                "capability ledger origin counts must be 52 adapted and "
                f"6 native, found {adapted} and {native}"
            )

        workflow_path = root / ".github" / "workflows" / "pages.yml"
        if not workflow_path.is_file():
            problems.append("GitHub Pages workflow missing")
        else:
            workflow = workflow_path.read_text(encoding="utf-8")
            required_workflow_tokens = (
                "actions/configure-pages@v5",
                "actions/upload-pages-artifact@v4",
                "actions/deploy-pages@v4",
                "pages: write",
                "id-token: write",
                "path: docs",
                "environment:",
                "name: github-pages",
            )
            for token in required_workflow_tokens:
                if token not in workflow:
                    problems.append(f"GitHub Pages workflow omits {token!r}")

        public_text = "\n".join(
            (docs / relative).read_text(encoding="utf-8")
            for relative in REQUIRED_HTML
            if (docs / relative).is_file()
        ).lower()
        for tracker in ("google-analytics", "gtag(", "plausible.io", "matomo"):
            if tracker in public_text:
                problems.append(f"unexpected analytics/tracker reference: {tracker}")
    finally:
        DOCS = previous_docs
    return problems


def main() -> int:
    problems = validate()
    if problems:
        for problem in problems:
            print(f"FAIL  public-site  {problem}")
        print(f"\nSummary: 0 passed, {len(problems)} failed.")
        return 1
    print(
        "PASS  public-site  static files, local links, credits, manifest URLs, "
        "58-skill ledger, and GitHub Pages workflow are consistent"
    )
    print("\nSummary: 1 passed, 0 failed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
