"""Forward-use-case tests for ManageRAW project state."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_TEMPLATE = ROOT / "assets" / "project-template"


class ManageRawStateTests(unittest.TestCase):
    def make_project(self, parent: Path) -> Path:
        project = parent / "project"
        shutil.copytree(PROJECT_TEMPLATE, project)
        return project

    def run_state(
        self,
        project: Path,
        command: str = "validate",
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(project / "scripts" / "manageraw-state.py"),
                command,
                "--project",
                str(project),
                *arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )

    def read_profile(self, project: Path) -> dict[str, object]:
        return json.loads(
            (project / ".maw" / "profile.yaml").read_text(encoding="utf-8")
        )

    def write_profile(
        self,
        project: Path,
        profile: dict[str, object],
    ) -> None:
        (project / ".maw" / "profile.yaml").write_text(
            json.dumps(profile, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_unclassified_template_is_valid_with_visible_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            result = self.run_state(project)
            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            self.assertIn("project type is unconfirmed", result.stdout)
            self.assertIn("project slug is unconfirmed", result.stdout)
            self.assertIn("0 failed", result.stdout)

    def test_teaching_latex_profile_is_valid_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            (project / "aulas").mkdir()
            (project / "aulas" / "calculo.tex").write_text(
                "\\documentclass{beamer}\\begin{document}\\end{document}\n",
                encoding="utf-8",
            )
            profile = self.read_profile(project)
            profile["project"] = {
                "slug": "mack-calculus",
                "type": "teaching",
                "classification_status": "confirmed",
                "primary_language": "pt-BR",
            }
            profile["maw"]["adoption"] = "thin"  # type: ignore[index]
            profile["source_roles"] = [
                {
                    "name": "lecture_sources",
                    "role": "authoritative",
                    "location": "aulas",
                }
            ]
            profile["build_profiles"] = [
                {
                    "name": "beamer_xelatex",
                    "kind": "latex",
                    "entrypoint": "aulas/calculo.tex",
                    "artifact": "aulas/calculo.pdf",
                    "verification": [
                        "xelatex compile",
                        "bibliography when cited",
                        "visual PDF inspection",
                    ],
                }
            ]
            profile["protected_material"] = [
                {
                    "category": "answer_keys",
                    "location": "solutions",
                    "handling": "do-not-export",
                }
            ]
            self.write_profile(project, profile)

            result = self.run_state(project, "status", "--json")
            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            status = json.loads(result.stdout)
            self.assertTrue(status["ok"])
            self.assertEqual(status["project"]["type"], "teaching")
            self.assertEqual(status["maw"]["adoption"], "thin")
            self.assertEqual(status["build_profiles"][0]["kind"], "latex")

    def test_mixed_stata_r_research_profile_preserves_source_roles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            (project / "code" / "stata").mkdir(parents=True)
            (project / "code" / "r").mkdir(parents=True)
            (project / "code" / "stata" / "master.do").write_text(
                "display \"smoke\"\n",
                encoding="utf-8",
            )
            (project / "code" / "r" / "run.R").write_text(
                "message('smoke')\n",
                encoding="utf-8",
            )
            profile = self.read_profile(project)
            profile["project"] = {
                "slug": "mixed-empirical-project",
                "type": "research",
                "classification_status": "confirmed",
                "primary_language": "en-US",
            }
            profile["maw"]["adoption"] = "selective"  # type: ignore[index]
            profile["source_roles"] = [
                {
                    "name": "raw_data",
                    "role": "restricted",
                    "location": "data/raw",
                },
                {
                    "name": "stata_pipeline",
                    "role": "authoritative",
                    "location": "code/stata",
                },
                {
                    "name": "r_pipeline",
                    "role": "authoritative",
                    "location": "code/r",
                },
                {
                    "name": "idea_sketches",
                    "role": "import",
                    "location": "notes",
                },
            ]
            profile["build_profiles"] = [
                {
                    "name": "stata_master",
                    "kind": "stata",
                    "entrypoint": "code/stata/master.do",
                    "artifact": "outputs/stata",
                    "verification": ["clean isolated run", "log review"],
                },
                {
                    "name": "r_pipeline",
                    "kind": "r",
                    "entrypoint": "code/r/run.R",
                    "artifact": "outputs/r",
                    "verification": ["clean isolated run", "output review"],
                },
            ]
            profile["protected_material"] = [
                {
                    "category": "raw_microdata",
                    "location": "data/raw",
                    "handling": "restricted",
                }
            ]
            profile["external_plugins"] = [
                {
                    "name": "example-operations-plugin",
                    "responsibilities": ["external collaboration handoff"],
                    "status": "optional",
                }
            ]
            self.write_profile(project, profile)

            result = self.run_state(project)
            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            self.assertIn("source role entry 4 is valid", result.stdout)
            self.assertIn("build profile entry 2 is valid", result.stdout)
            self.assertIn("protected-material entry 1 is valid", result.stdout)

    def test_version_drift_and_secret_keys_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            profile = self.read_profile(project)
            profile["api_key"] = "must-not-be-here"
            profile["personalization"]["team"]["note"] = (  # type: ignore[index]
                "ghp_abcdefghijklmnopqrstuvwxyz123456"
            )
            self.write_profile(project, profile)
            lock_path = project / ".maw" / "lock.json"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            lock["maw_version"] = "9.9.9"
            lock_path.write_text(
                json.dumps(lock, indent=2) + "\n",
                encoding="utf-8",
            )

            result = self.run_state(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("secret-bearing keys are forbidden", result.stdout)
            self.assertIn("recognizable secret values are forbidden", result.stdout)
            self.assertIn("lock.maw_version differs", result.stdout)

    @unittest.skipUnless(shutil.which("git"), "Git is required for tracking test")
    def test_personal_overlay_fails_when_forced_into_git(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            local_path = project / ".maw" / "local.yaml"
            local_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "personal": {
                            "preferred_language": "pt-BR",
                            "external_plugins": [],
                            "settings": {},
                        },
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            initialized = subprocess.run(
                [shutil.which("git") or "git", "init", str(project)],
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
            )
            self.assertEqual(initialized.returncode, 0, msg=initialized.stderr)
            added = subprocess.run(
                [
                    shutil.which("git") or "git",
                    "-C",
                    str(project),
                    "add",
                    "-f",
                    ".maw/local.yaml",
                ],
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
            )
            self.assertEqual(added.returncode, 0, msg=added.stderr)

            result = self.run_state(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".maw/local.yaml must not be tracked", result.stdout)


if __name__ == "__main__":
    unittest.main()
