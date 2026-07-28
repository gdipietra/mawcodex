#!/usr/bin/env python3
"""Record dispositions for every remaining fixed-source repository file."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from check_source_clone import (
    BASELINE_COMMIT,
    GitCheckError,
    inspect,
    run_git,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
CONVERSION = ROOT / "docs" / "conversion"
MANIFEST = CONVERSION / "AUXILIARY_SOURCE_MANIFEST.json"


def digest_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def mapped_sources() -> set[str]:
    component = json.loads(
        (CONVERSION / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
    )
    project = json.loads(
        (CONVERSION / "PROJECT_TEMPLATE_MANIFEST.json").read_text(
            encoding="utf-8"
        )
    )
    runtime = json.loads(
        (CONVERSION / "RUNTIME_SURFACES_MANIFEST.json").read_text(
            encoding="utf-8"
        )
    )
    return {
        *(record["source"] for record in component["components"]),
        *(record["source"] for record in project["files"]),
        *(record["source"] for record in runtime["surfaces"]),
    }


def disposition(source: str) -> tuple[str, str, tuple[str, ...], str]:
    if source == ".githooks/pre-commit":
        return (
            "native rewrite",
            "non-mutating project Git gate",
            (
                "assets/project-template/.githooks/pre-commit",
                "assets/project-template/scripts/project_precommit.py",
                "assets/project-template/scripts/install_git_hooks.py",
            ),
            (
                "Reimplemented the repository hook without stash or pop "
                "mutations and kept activation preview-first and explicitly "
                "project-local."
            ),
        )
    if source == ".gitignore":
        return (
            "native rewrite",
            "package and project ignore policies",
            (".gitignore", "assets/project-template/.gitignore"),
            (
                "Split provider-repository ignore rules into package and "
                "initialized-project policies, retaining generated-file and "
                "secret exclusions without provider cache paths."
            ),
        )
    if source == ".vscode/settings.json":
        return (
            "unsupported",
            "editor-specific settings intentionally omitted",
            ("docs/conversion/PROJECT_TEMPLATE_MAP.md",),
            (
                "Omitted editor-specific and provider permission behavior; "
                "Codex authority remains user-controlled and the project map "
                "records the intentional behavior loss."
            ),
        )
    if source.startswith(".github/"):
        if source == ".github/workflows/deploy.yml":
            return (
                "composed replacement",
                "explicit deployment workflow",
                (
                    "skills/deploy/SKILL.md",
                    "docs/conversion/PROJECT_TEMPLATE_MAP.md",
                ),
                (
                    "Replaced automatic provider-guide deployment with an "
                    "explicit deployment skill and project-specific authority "
                    "gate; no publication occurs during installation."
                ),
            )
        target = ROOT / source
        if target.is_file():
            return (
                "native rewrite",
                "independent repository governance or validation",
                (source,),
                (
                    "Rewrote repository governance or CI for the independent "
                    "Codex-native package while retaining contribution, "
                    "security, and validation intent."
                ),
            )
    if source.endswith(".gitkeep"):
        candidate = f"assets/project-template/{source}"
        if (ROOT / candidate).is_file():
            return (
                "direct port",
                "initialized-project empty-directory marker",
                (candidate,),
                (
                    "Preserved the source repository's durable empty "
                    "directory so initialized academic projects retain the "
                    "same organization and artifact routing."
                ),
            )
        fallbacks = {
            "Preambles/.gitkeep": (
                "assets/project-template/Preambles/README.md",
            ),
            "Slides/.gitkeep": (
                "assets/project-template/Slides/HelloWorld.tex",
            ),
            "scripts/R/.gitkeep": (
                "assets/project-template/scripts/R/README.md",
            ),
        }
        if source in fallbacks:
            return (
                "composed replacement",
                "populated initialized-project directory",
                fallbacks[source],
                (
                    "The empty marker became unnecessary because the "
                    "initialized project ships reviewed starter content in "
                    "the same durable directory."
                ),
            )
    root_files = {
        "CHANGELOG.md": (
            "composed replacement",
            "independent package history",
            ("CHANGELOG.md", "NOTICE.md"),
            (
                "Started an independent package changelog while retaining "
                "the upstream release and attribution boundary in notices and "
                "conversion records."
            ),
        ),
        "CITATION.cff": (
            "native rewrite",
            "package citation with upstream reference",
            ("CITATION.cff",),
            (
                "Rewrote citation metadata for MAW Codex and retained Pedro's "
                "workflow as an explicit referenced software source."
            ),
        ),
        "LICENSE": (
            "direct port",
            "MIT package license",
            ("LICENSE",),
            (
                "Retained the permissive MIT distribution basis and added "
                "separate notices for upstream and third-party attribution."
            ),
        ),
        "MEMORY.md": (
            "native rewrite",
            "clean initialized-project memory",
            ("assets/project-template/MEMORY.md",),
            (
                "Replaced source release history with an empty evidence-"
                "oriented project memory so new projects do not inherit "
                "unrelated conclusions."
            ),
        ),
        "README.md": (
            "composed replacement",
            "Codex-native package guide",
            ("README.md", "docs/INSTALL.md"),
            (
                "Rewrote installation, architecture, validation, and update "
                "guidance for the two-repository Codex-native workflow."
            ),
        ),
        "TROUBLESHOOTING.md": (
            "composed replacement",
            "installation and limitations guidance",
            (
                "docs/INSTALL.md",
                "docs/conversion/KNOWN_LIMITATIONS.md",
            ),
            (
                "Integrated supported troubleshooting into the installation "
                "guide and stable-boundary limitations instead of retaining "
                "provider-specific remedies."
            ),
        ),
    }
    if source in root_files:
        return root_files[source]
    if source.startswith(("docs/", "guide/")):
        return (
            "composed replacement",
            "directly maintained package documentation",
            (
                "README.md",
                "docs/INSTALL.md",
                "docs/conversion/README.md",
            ),
            (
                "Replaced the generated provider guide and deployed HTML with "
                "directly maintained package, installation, and auditable "
                "conversion documentation."
            ),
        )
    script_targets = {
        "scripts/check-model-versions.sh": (
            "references/model-versions.md",
            "scripts/validate_package.py",
        ),
        "scripts/check-palette-sync.sh": (
            "assets/project-template/scripts/check-palette-sync.py",
        ),
        "scripts/check-skill-integrity.py": (
            "scripts/run_skill_validators.py",
            "scripts/validate_package.py",
        ),
        "scripts/check-surface-sync.py": (
            "scripts/validate_package.py",
            "scripts/refresh_source_manifest.py",
        ),
        "scripts/check-surface-sync.sh": (
            "scripts/validate_package.py",
            "scripts/refresh_source_manifest.py",
        ),
        "scripts/install-hooks.sh": (
            "assets/project-template/scripts/install_git_hooks.py",
        ),
        "scripts/nightly-repro-check.sh": (
            "assets/project-template/scripts/nightly-repro-check.py",
        ),
        "scripts/sync_to_docs.sh": ("skills/deploy/SKILL.md",),
        "scripts/validate-setup.sh": (
            "scripts/validate_package.py",
            "scripts/check_source_clone.py",
            "assets/project-template/scripts/validate-project.py",
        ),
    }
    if source in script_targets:
        classification = (
            "composed replacement"
            if source in {
                "scripts/sync_to_docs.sh",
                "scripts/validate-setup.sh",
            }
            else "native rewrite"
        )
        return (
            classification,
            "cross-platform Codex validation or explicit workflow",
            script_targets[source],
            (
                "Replaced the shell or provider-specific maintenance helper "
                "with cross-platform deterministic validation or an explicit "
                "Codex workflow preserving the original operational intent."
            ),
        )
    raise ValueError(f"no auxiliary disposition for {source}")


def main() -> int:
    source_root = SOURCE_ROOT.resolve()
    try:
        contract = inspect(source_root, fetch=False)
    except (GitCheckError, OSError, ValueError) as error:
        raise SystemExit(f"source contract check failed: {error}") from error
    if not contract["ok"]:
        raise SystemExit(
            "source contract check failed: "
            + "; ".join(str(item) for item in contract["errors"])
        )
    tracked = run_git(source_root, "ls-files").splitlines()
    covered = mapped_sources()
    auxiliary = [source for source in tracked if source not in covered]
    if len(auxiliary) != 48:
        raise SystemExit(
            f"expected 48 auxiliary files at the fixed baseline, found "
            f"{len(auxiliary)}"
        )
    records: list[dict[str, object]] = []
    for source_value in auxiliary:
        classification, action, target_values, summary = disposition(
            source_value
        )
        source = source_root / source_value
        targets = []
        for target_value in target_values:
            target = ROOT / target_value
            if not target.is_file():
                raise SystemExit(f"auxiliary target missing: {target}")
            targets.append(
                {
                    "path": target_value,
                    "sha256": digest_text(target),
                }
            )
        records.append(
            {
                "name": source_value,
                "source": source_value,
                "source_sha256": digest_text(source),
                "classification": classification,
                "status": "validated",
                "disposition": action,
                "targets": targets,
                "revision_record": (
                    "docs/conversion/AUXILIARY_SOURCE_MAP.md"
                ),
                "revision_summary": summary,
            }
        )
    document = {
        "schema_version": 1,
        "source_repository": (
            "https://github.com/pedrohcgs/claude-code-my-workflow"
        ),
        "source_commit": BASELINE_COMMIT,
        "generated_by": "scripts/refresh_auxiliary_source_manifest.py",
        "tracked_source_files": len(tracked),
        "previously_mapped_files": len(covered),
        "auxiliary_files": len(records),
        "files": records,
    }
    MANIFEST.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Recorded {len(records)} auxiliary files; "
        f"{len(covered) + len(records)}/{len(tracked)} source files covered."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
