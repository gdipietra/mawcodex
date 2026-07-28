#!/usr/bin/env python3
"""Refresh reviewed target hashes without moving the fixed source boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    os.environ.get(
        "MAWCODEX_SOURCE_CLONE",
        r"C:\GitHub\claude-code-my-workflow",
    )
)
MANIFEST = ROOT / "docs" / "conversion" / "SOURCE_MANIFEST.json"
BASELINE_COMMIT = "be53c12f235996dff41fb7f21580506fd2dd8d50"
FORWARD_TEST_IDS = {
    "interview-me": "FT-01",
    "did-event-study": "FT-02",
    "commit": "FT-03",
    "disclosure-check": "FT-04",
    "replication-package": "FT-05",
    "review-paper": "FT-06",
    "verify-claims": "FT-07",
    "translate-to-quarto": "FT-08",
    "triage-inbox": "FT-09",
    "submission-disclosures": "FT-10",
    "data-analysis": "FT-11",
    "compile-latex": "FT-12",
    "create-lecture": "FT-13",
    "respond-to-referees": "FT-14",
    "r-package-check": "FT-15",
}


def digest(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_relative(value: str, base: Path) -> str:
    path = Path(value)
    if path.is_absolute():
        return path.resolve().relative_to(base.resolve()).as_posix()
    return path.as_posix()


def refresh_target(
    record: dict[str, object],
    path_key: str,
    hash_key: str,
) -> None:
    value = record.get(path_key)
    if not isinstance(value, str):
        raise ValueError(
            f"{record.get('kind')}/{record.get('name')} lacks {path_key}"
        )
    relative = make_relative(value, ROOT)
    target = ROOT / relative
    if not target.is_file():
        raise FileNotFoundError(target)
    record[path_key] = relative
    record[hash_key] = digest(target)


def skill_record_details(
    name: str,
    release_statuses: bool,
) -> tuple[str, str]:
    record_path = ROOT / "docs" / "conversion" / "skills" / f"{name}.md"
    text = record_path.read_text(encoding="utf-8")
    if release_statuses:
        test_id = FORWARD_TEST_IDS.get(name)
        status = "forward-tested" if test_id else "validated"
        forward_result = (
            f"PASS ({test_id})"
            if test_id
            else (
                "not selected for the representative 1.0 matrix; "
                "semantic and structural validation PASS"
            )
        )
        text = re.sub(
            r"(?m)^-\s*Status:\s*`[^`]+`\s*$",
            f"- Status: `{status}`",
            text,
            count=1,
        )
        text = re.sub(
            r"(?mi)^-\s*Forward test:\s*`?[^`\r\n]+`?\s*$",
            f"- Forward test: {forward_result}",
            text,
            count=1,
        )
    match = re.search(r"(?m)^-\s*Status:\s*`([^`]+)`", text)
    if not match:
        raise ValueError(f"conversion status missing: {record_path}")
    classification_match = re.search(
        r"(?m)^-\s*Classification:\s*`([^`]+)`",
        text,
    )
    if not classification_match:
        raise ValueError(f"conversion classification missing: {record_path}")
    target_hash = digest(ROOT / "skills" / name / "SKILL.md")
    updated = re.sub(
        r"(?m)^-\s*Target SHA-256 after [^:]+:\s*`[0-9a-f]+`",
        f"- Target SHA-256 after semantic review: `{target_hash}`",
        text,
    )
    if updated == text and target_hash not in text:
        updated = text.rstrip() + (
            f"\n- Target SHA-256 after semantic review: `{target_hash}`\n"
        )
    record_path.write_text(updated, encoding="utf-8")
    return match.group(1), classification_match.group(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release-statuses",
        action="store_true",
        help=(
            "promote reviewed components and record the representative "
            "forward-test matrix"
        ),
    )
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("source_commit") != BASELINE_COMMIT:
        raise SystemExit("Refusing to move an unexpected source boundary.")
    components = manifest.get("components")
    if not isinstance(components, list):
        raise SystemExit("SOURCE_MANIFEST.json has no component list.")

    for record in components:
        if not isinstance(record, dict):
            raise SystemExit("Invalid component record.")
        source_value = record.get("source")
        if not isinstance(source_value, str):
            raise SystemExit(f"Source missing for {record.get('name')}.")
        source_relative = make_relative(source_value, SOURCE_ROOT)
        source = SOURCE_ROOT / source_relative
        if not source.is_file():
            raise SystemExit(f"Fixed source file missing: {source}")
        source_hash = digest(source)
        if source_hash != record.get("source_sha256"):
            raise SystemExit(
                f"Fixed source hash changed for {record.get('kind')}/"
                f"{record.get('name')}; do not refresh across source drift."
            )
        record["source"] = source_relative

        if record.get("kind") == "agent":
            refresh_target(record, "role_target", "role_target_sha256")
            refresh_target(record, "toml_target", "toml_target_sha256")
        else:
            refresh_target(record, "target", "target_sha256")
        if record.get("kind") == "skill":
            status, classification = skill_record_details(
                str(record["name"]),
                args.release_statuses,
            )
            record["status"] = status
            record["classification"] = classification
            record["revision_record"] = (
                "docs/conversion/skills/"
                f"{record['name']}.md"
            )
            record["revision_summary"] = (
                "The dedicated skill record documents preserved intent, "
                "material Codex revisions, behavior differences, validation, "
                "and representative-test status."
            )
        elif record.get("kind") == "agent":
            record["classification"] = "composed replacement"
            record["revision_record"] = "docs/conversion/AGENT_MAP.md"
            record["revision_summary"] = (
                "Converted the source role into both a project custom-agent "
                "TOML and a portable role file while removing provider model, "
                "tool, and permission assumptions."
            )
        elif record.get("kind") == "rule":
            record["classification"] = "native rewrite"
            record["revision_record"] = (
                "docs/conversion/shared-resources.md"
            )
            record["revision_summary"] = (
                "Replaced provider routing and runtime assumptions with "
                "explicit applicability and Codex-native skill and reference "
                "routing while retaining the research safeguard."
            )
        elif record.get("kind") in {"reference", "template"}:
            if record.get("classification") == (
                "retained historical reference"
            ):
                record["classification"] = "retained reference"
            record["revision_record"] = (
                "docs/conversion/shared-resources.md"
            )
            record["revision_summary"] = (
                "The shared-resource record documents whether this component "
                "was ported, rewritten, or retained and the material routing "
                "and provider-surface changes."
            )
        elif (
            args.release_statuses
            and record.get("status") == "semantic-baseline"
        ):
            record["status"] = "validated"

    manifest["schema_version"] = 3
    manifest["paths"] = {
        "source": "relative to the fixed upstream clone",
        "target": "relative to this package root",
    }
    manifest["counts"] = dict(
        sorted(Counter(record["kind"] for record in components).items())
    )
    if args.release_statuses:
        for record_path in (
            ROOT / "docs" / "conversion" / "AGENT_MAP.md",
            ROOT / "docs" / "conversion" / "shared-resources.md",
        ):
            text = record_path.read_text(encoding="utf-8")
            record_path.write_text(
                text.replace("`semantic-baseline`", "`validated`"),
                encoding="utf-8",
            )
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Refreshed {len(components)} component records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
