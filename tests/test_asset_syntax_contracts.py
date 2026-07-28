"""Syntax contracts for executable and renderable imported assets."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AssetSyntaxContractTests(unittest.TestCase):
    def test_tex_sample_escapes_codex_skill_sigils_in_typeset_text(self) -> None:
        sample = (
            ROOT
            / "assets"
            / "project-template"
            / "Slides"
            / "HelloWorld.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\texttt{\$compile-latex}", sample)
        self.assertIn(
            r"\texttt{\$translate-to-quarto HelloWorld.tex}",
            sample,
        )
        self.assertNotIn(r"\texttt{$", sample)

    def test_quarto_sample_keeps_normal_codex_skill_sigil(self) -> None:
        sample = (
            ROOT
            / "assets"
            / "project-template"
            / "Quarto"
            / "HelloWorld.qmd"
        ).read_text(encoding="utf-8")
        self.assertIn("`$deploy HelloWorld`", sample)
        self.assertNotIn(r"`\$deploy", sample)

    def test_tex_templates_use_tex_provenance_comments(self) -> None:
        template_root = ROOT / "assets" / "templates" / "tikz-snippets"
        templates = sorted(template_root.glob("*.tex"))
        self.assertGreater(len(templates), 0)
        for template in templates:
            with self.subTest(template=template.name):
                first = next(
                    line
                    for line in template.read_text(
                        encoding="utf-8"
                    ).splitlines()
                    if line.strip()
                )
                self.assertTrue(first.startswith("% "))
                self.assertNotIn("<!--", first)

    def test_yaml_template_uses_yaml_provenance_comment(self) -> None:
        template = ROOT / "assets" / "templates" / "passport-template.yaml"
        first = next(
            line
            for line in template.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        )
        self.assertTrue(first.startswith("# "))
        self.assertNotIn("<!--", first)


if __name__ == "__main__":
    unittest.main()
