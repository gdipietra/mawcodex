#!/usr/bin/env python3
"""Preview or install MAW Codex in the canonical local marketplace."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "mawcodex"
INCLUDED_DIRECTORIES = (
    ".codex",
    ".codex-plugin",
    ".github",
    "assets",
    "docs",
    "hooks",
    "references",
    "scripts",
    "skills",
    "tests",
)
INCLUDED_FILES = (
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "THIRD_PARTY_NOTICES.md",
)


class InstallError(RuntimeError):
    """Raised when installation cannot preserve the user's existing state."""


def default_plugin_parent() -> Path:
    return Path.home() / "plugins"


def default_agents_home() -> Path:
    return Path.home() / ".agents"


def read_manifest() -> dict[str, Any]:
    path = ROOT / ".codex-plugin" / "plugin.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InstallError(f"plugin manifest is unreadable: {error}") from error
    if value.get("name") != PLUGIN_NAME:
        raise InstallError(
            f"plugin manifest name is {value.get('name')!r}, "
            f"expected {PLUGIN_NAME!r}"
        )
    return value


def canonical_entry() -> dict[str, Any]:
    return {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Education",
    }


def prepare_marketplace(path: Path, update: bool) -> dict[str, Any]:
    if path.exists():
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise InstallError(
                f"personal marketplace is unreadable: {error}"
            ) from error
        if not isinstance(value, dict):
            raise InstallError("personal marketplace root must be an object")
        if not isinstance(value.get("name"), str) or not value["name"].strip():
            raise InstallError(
                "the local marketplace must have a non-empty string name"
            )
        plugins = value.get("plugins")
        if not isinstance(plugins, list):
            raise InstallError("personal marketplace plugins must be an array")
    else:
        value = {
            "name": "personal",
            "interface": {"displayName": "Personal"},
            "plugins": [],
        }
        plugins = value["plugins"]

    matches = [
        (index, item)
        for index, item in enumerate(plugins)
        if isinstance(item, dict) and item.get("name") == PLUGIN_NAME
    ]
    if len(matches) > 1:
        raise InstallError("personal marketplace contains duplicate mawcodex entries")
    entry = canonical_entry()
    if matches:
        index, existing = matches[0]
        if existing != entry:
            if not update:
                raise InstallError(
                    "an incompatible mawcodex marketplace entry exists; "
                    "preview and rerun with --update to replace only that entry"
                )
            plugins[index] = entry
    else:
        plugins.append(entry)
    return value


def ignore_runtime_noise(
    _directory: str,
    names: list[str],
) -> set[str]:
    ignored = {
        name
        for name in names
        if name in {"__pycache__", ".pytest_cache", ".ruff_cache"}
        or name.endswith((".pyc", ".pyo"))
    }
    return ignored


def copy_package(stage: Path) -> None:
    for relative in INCLUDED_DIRECTORIES:
        source = ROOT / relative
        if not source.is_dir():
            raise InstallError(f"required package directory is missing: {relative}")
        shutil.copytree(
            source,
            stage / relative,
            dirs_exist_ok=True,
            ignore=ignore_runtime_noise,
        )
    for relative in INCLUDED_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise InstallError(f"required package file is missing: {relative}")
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def install(
    plugin_parent: Path,
    agents_home: Path,
    *,
    apply: bool,
    update: bool,
) -> dict[str, Any]:
    manifest = read_manifest()
    version = str(manifest.get("version", ""))
    expected_parent = agents_home.parent / "plugins"
    if plugin_parent.resolve() != expected_parent.resolve():
        raise InstallError(
            "plugin parent must resolve to the marketplace's ./plugins "
            f"directory: {expected_parent}"
        )
    destination = plugin_parent / PLUGIN_NAME
    marketplace = agents_home / "plugins" / "marketplace.json"
    marketplace_value = prepare_marketplace(marketplace, update)
    exists = destination.exists()
    if exists and not update:
        raise InstallError(
            f"plugin destination already exists: {destination}; "
            "rerun with --update for a recoverable replacement"
        )

    plan = {
        "ok": True,
        "mode": "apply" if apply else "preview",
        "version": version,
        "source": str(ROOT),
        "destination": str(destination),
        "marketplace": str(marketplace),
        "existing_plugin": exists,
        "update": update,
        "included_directories": list(INCLUDED_DIRECTORIES),
        "included_files": list(INCLUDED_FILES),
    }
    if not apply:
        return plan

    plugins_dir = destination.parent
    plugins_dir.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(prefix=f".{PLUGIN_NAME}-stage-", dir=plugins_dir)
    )
    backup: Path | None = None
    marketplace_backup: Path | None = None
    installed = False
    try:
        copy_package(stage)
        staged_manifest = json.loads(
            (stage / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        if staged_manifest.get("name") != PLUGIN_NAME:
            raise InstallError("staged plugin manifest changed unexpectedly")

        if exists:
            backup = plugins_dir / f"{PLUGIN_NAME}.backup-{timestamp()}"
            if backup.exists():
                raise InstallError(f"backup path already exists: {backup}")
            destination.replace(backup)
        stage.replace(destination)
        installed = True

        if marketplace.exists():
            marketplace_backup = marketplace.with_name(
                f"{marketplace.name}.backup-{timestamp()}"
            )
            shutil.copy2(marketplace, marketplace_backup)
        write_json_atomic(marketplace, marketplace_value)
    except Exception:
        if installed and destination.exists():
            shutil.rmtree(destination)
        if backup and backup.exists() and not destination.exists():
            backup.replace(destination)
        raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)

    plan["plugin_backup"] = str(backup) if backup else None
    plan["marketplace_backup"] = (
        str(marketplace_backup) if marketplace_backup else None
    )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Preview or install MAW Codex into the canonical local Codex "
            "plugin marketplace."
        )
    )
    parser.add_argument(
        "--plugin-parent",
        type=Path,
        default=default_plugin_parent(),
        help="plugin parent resolved by ./plugins/ (default: ~/plugins)",
    )
    parser.add_argument(
        "--agents-home",
        type=Path,
        default=default_agents_home(),
        help=(
            "agents home containing plugins/marketplace.json "
            "(default: ~/.agents)"
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the displayed installation; default is preview only",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="replace an existing install after making timestamped backups",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = install(
            args.plugin_parent.expanduser().resolve(),
            args.agents_home.expanduser().resolve(),
            apply=args.apply,
            update=args.update,
        )
    except (InstallError, OSError, UnicodeError, json.JSONDecodeError) as error:
        if args.json:
            print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        else:
            print(f"ERROR  {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        verb = "Installed" if args.apply else "Would install"
        print(f"{verb} MAW Codex {result['version']}:")
        print(f"  plugin:      {result['destination']}")
        print(f"  marketplace: {result['marketplace']}")
        if not args.apply:
            print("Preview complete; rerun with --apply to write these paths.")
        else:
            print(
                "Restart Codex or begin a new task, then install/enable "
                "mawcodex from the local marketplace shown in the app."
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
