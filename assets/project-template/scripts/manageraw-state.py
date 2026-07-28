#!/usr/bin/env python3
"""Validate and summarize a project-local ManageRAW control plane."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
ALLOWED_PROJECT_TYPES = {"teaching", "research", "mixed"}
ALLOWED_CLASSIFICATION_STATUS = {"unconfirmed", "inferred", "confirmed"}
ALLOWED_ADOPTIONS = {"plugin-only", "thin", "selective", "full"}
ALLOWED_PRIORITIES = {"primary", "specialist", "shared", "fallback"}
ALLOWED_SOURCE_ROLES = {
    "authoritative",
    "mirror",
    "import",
    "generated",
    "restricted",
}
ALLOWED_BUILD_KINDS = {
    "latex",
    "quarto",
    "r",
    "stata",
    "python",
    "julia",
    "other",
}
ALLOWED_HANDLING = {
    "local-only",
    "restricted",
    "embargoed",
    "do-not-export",
    "institution-controlled",
}
SENSITIVE_KEY = re.compile(
    r"(?i)(password|passwd|secret|token|credential|api[_-]?key)"
)
SENSITIVE_VALUE = re.compile(
    r"(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})|"
    r"sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|"
    r"AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~+/-]{20,})"
)


class Results:
    def __init__(self) -> None:
        self.passes: list[str] = []
        self.warnings: list[str] = []
        self.failures: list[str] = []

    def require(self, condition: bool, passed: str, failed: str) -> None:
        if condition:
            self.passes.append(passed)
        else:
            self.failures.append(failed)


def load_json_yaml(path: Path) -> dict[str, Any]:
    """Load MAW's deterministic JSON-compatible YAML subset."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"required state file is missing: {path}") from None
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"{path} is not valid JSON-compatible YAML: {error}"
        ) from error
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one mapping object")
    return value


def walk_sensitive_keys(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if SENSITIVE_KEY.search(str(key)):
                findings.append(path)
            findings.extend(walk_sensitive_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(walk_sensitive_keys(child, f"{prefix}[{index}]"))
    return findings


def walk_sensitive_values(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            findings.extend(walk_sensitive_values(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(walk_sensitive_values(child, f"{prefix}[{index}]"))
    elif isinstance(value, str) and SENSITIVE_VALUE.search(value):
        findings.append(prefix)
    return findings


def walk_unsafe_locations(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            findings.extend(walk_unsafe_locations(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(walk_unsafe_locations(child, f"{prefix}[{index}]"))
    elif isinstance(value, str) and (
        value.startswith(("/", "\\", "~"))
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or re.match(r"(?i)^[a-z][a-z0-9+.-]*://", value)
    ):
        findings.append(prefix)
    return findings


def is_relative_project_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if (
        value.startswith(("/", "\\", "~"))
        or re.match(r"^[A-Za-z]:[\\/]", value)
    ):
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def is_safe_location(value: Any) -> bool:
    return is_relative_project_path(value) or (
        isinstance(value, str)
        and bool(
            re.fullmatch(
                r"external:[a-z0-9]+(?:[._-][a-z0-9]+)*",
                value,
            )
        )
    )


def tracked(project: Path, relative: str) -> bool | None:
    git = shutil.which("git")
    if not git or not (project / ".git").exists():
        return None
    process = subprocess.run(
        [git, "-C", str(project), "ls-files", "--error-unmatch", relative],
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode == 0:
        return True
    if process.returncode == 1:
        return False
    return None


def validate(project: Path) -> tuple[Results, dict[str, Any] | None]:
    results = Results()
    state_root = project / ".maw"
    profile_path = state_root / "profile.yaml"
    lock_path = state_root / "lock.json"
    try:
        profile = load_json_yaml(profile_path)
        lock = load_json_yaml(lock_path)
    except ValueError as error:
        results.failures.append(str(error))
        return results, None

    results.require(
        profile.get("schema_version") == 1,
        "profile schema version is 1",
        "profile schema_version must be 1",
    )
    project_record = profile.get("project")
    results.require(
        isinstance(project_record, dict),
        "project identity mapping is present",
        "profile.project must be a mapping",
    )
    if isinstance(project_record, dict):
        project_type = project_record.get("type")
        if project_type is None:
            results.warnings.append(
                "project type is unconfirmed; run $jaw before relying on "
                "this adoption profile"
            )
        else:
            results.require(
                project_type in ALLOWED_PROJECT_TYPES,
                f"project type is {project_type}",
                "project.type must be teaching, research, mixed, or null",
            )
        results.require(
            project_record.get("classification_status")
            in ALLOWED_CLASSIFICATION_STATUS,
            "project classification status is valid",
            "project.classification_status must be unconfirmed, inferred, "
            "or confirmed",
        )
        slug = project_record.get("slug")
        if slug is None:
            results.warnings.append(
                "project slug is unconfirmed; set it with $paw"
            )
        else:
            results.require(
                isinstance(slug, str)
                and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)),
                "project slug is portable",
                "project.slug must be lowercase hyphen-case or null",
            )

    maw = profile.get("maw")
    results.require(
        isinstance(maw, dict),
        "MAW base mapping is present",
        "profile.maw must be a mapping",
    )
    if isinstance(maw, dict):
        base_version = maw.get("base_version")
        results.require(
            isinstance(base_version, str) and bool(SEMVER.fullmatch(base_version)),
            "MAW base version is valid semver",
            "maw.base_version must be strict semver",
        )
        results.require(
            maw.get("adoption") in ALLOWED_ADOPTIONS,
            f"adoption mode is {maw.get('adoption')}",
            "maw.adoption must be plugin-only, thin, selective, or full",
        )
        results.require(
            maw.get("governance_owner") == "mawcodex",
            "academic governance owner is mawcodex",
            "maw.governance_owner must be mawcodex",
        )
        results.require(
            maw.get("manager_agent") == "manageraw",
            "manager agent is manageraw",
            "maw.manager_agent must be manageraw",
        )

    layers = profile.get("instruction_layers")
    results.require(
        isinstance(layers, dict),
        "instruction-layer mapping is present",
        "profile.instruction_layers must be a mapping",
    )
    if isinstance(layers, dict):
        global_layer = layers.get("global")
        project_layer = layers.get("project")
        personal_layer = layers.get("personal")
        results.require(
            isinstance(global_layer, dict)
            and global_layer.get("policy") == "inherit"
            and global_layer.get("managed") is False,
            "global instruction policy is inherited and unmanaged",
            "instruction_layers.global must use policy=inherit and "
            "managed=false",
        )
        results.require(
            isinstance(project_layer, dict)
            and is_relative_project_path(project_layer.get("path"))
            and project_layer.get("owner") == "team"
            and project_layer.get("managed_block") == "manageraw",
            "project instruction path is relative",
            "project instruction layer must be a safe team-owned path with "
            "managed_block=manageraw",
        )
        if (
            isinstance(project_layer, dict)
            and is_relative_project_path(project_layer.get("path"))
        ):
            instruction_path = project / project_layer["path"]
            results.require(
                instruction_path.is_file(),
                "project instruction file exists",
                "declared project instruction file is missing",
            )
            if (
                instruction_path.is_file()
                and project_layer.get("managed_block") == "manageraw"
            ):
                instruction_text = instruction_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
                results.require(
                    "<!-- manageraw:begin -->" in instruction_text
                    and "<!-- manageraw:end -->" in instruction_text,
                    "ManageRAW instruction block markers are present",
                    "declared ManageRAW instruction block markers are missing",
                )
        results.require(
            isinstance(personal_layer, dict)
            and personal_layer.get("path") == ".maw/local.yaml"
            and personal_layer.get("tracked") is False,
            "personal layer is local and untracked",
            "personal layer must be .maw/local.yaml with tracked=false",
        )
        nested = layers.get("nested")
        results.require(
            isinstance(nested, list),
            "nested instruction layers are an array",
            "instruction_layers.nested must be an array",
        )
        if isinstance(nested, list):
            nested_paths: list[str] = []
            for index, layer in enumerate(nested):
                valid_path = (
                    isinstance(layer, dict)
                    and is_relative_project_path(layer.get("path"))
                    and layer.get("owner") == "team"
                    and isinstance(layer.get("scope"), str)
                    and bool(layer["scope"].strip())
                    and layer.get("managed_block") in {None, "manageraw"}
                )
                results.require(
                    valid_path,
                    f"nested layer {index + 1} has a safe relative path",
                    f"nested layer {index + 1} must have a safe team-owned "
                    "path, scope, and supported managed_block",
                )
                if valid_path:
                    nested_paths.append(layer["path"])
                    nested_path = project / layer["path"]
                    results.require(
                        nested_path.is_file(),
                        f"nested layer {index + 1} exists",
                        f"nested layer {index + 1} file is missing",
                    )
                    if (
                        nested_path.is_file()
                        and layer.get("managed_block") == "manageraw"
                    ):
                        nested_text = nested_path.read_text(
                            encoding="utf-8",
                            errors="replace",
                        )
                        results.require(
                            "<!-- manageraw:begin -->" in nested_text
                            and "<!-- manageraw:end -->" in nested_text,
                            f"nested layer {index + 1} markers are present",
                            f"nested layer {index + 1} ManageRAW markers "
                            "are missing",
                        )
            results.require(
                len(nested_paths)
                == len({path.casefold() for path in nested_paths}),
                "nested instruction registry has no duplicates",
                "nested instruction registry contains duplicate paths",
            )

    ownership = profile.get("capability_ownership")
    results.require(
        isinstance(ownership, list) and bool(ownership),
        "capability ownership is declared",
        "capability_ownership must be a non-empty array",
    )
    capabilities: list[str] = []
    if isinstance(ownership, list):
        for index, record in enumerate(ownership):
            valid = (
                isinstance(record, dict)
                and isinstance(record.get("capability"), str)
                and bool(record["capability"].strip())
                and isinstance(record.get("owner"), str)
                and bool(record["owner"].strip())
                and record.get("priority") in ALLOWED_PRIORITIES
            )
            results.require(
                valid,
                f"ownership entry {index + 1} is valid",
                f"ownership entry {index + 1} is malformed",
            )
            if isinstance(record, dict) and isinstance(
                record.get("capability"), str
            ):
                capabilities.append(record["capability"])
    results.require(
        len(capabilities) == len(set(capabilities)),
        "capability ownership has no duplicates",
        "capability ownership contains duplicate capabilities",
    )

    for field in (
        "external_plugins",
        "source_roles",
        "build_profiles",
        "protected_material",
    ):
        results.require(
            isinstance(profile.get(field), list),
            f"{field} is an array",
            f"profile.{field} must be an array",
        )

    plugins = profile.get("external_plugins")
    if isinstance(plugins, list):
        plugin_names: list[str] = []
        for index, record in enumerate(plugins):
            valid = (
                isinstance(record, dict)
                and isinstance(record.get("name"), str)
                and bool(record["name"].strip())
                and isinstance(record.get("responsibilities"), list)
                and bool(record.get("responsibilities"))
                and all(
                    isinstance(item, str) and bool(item.strip())
                    for item in record.get("responsibilities", [])
                )
                and record.get("status")
                in {"active", "optional", "unavailable", "disabled"}
            )
            results.require(
                valid,
                f"external plugin entry {index + 1} is valid",
                f"external plugin entry {index + 1} is malformed",
            )
            if isinstance(record, dict) and isinstance(record.get("name"), str):
                plugin_names.append(record["name"])
        results.require(
            len(plugin_names)
            == len({name.casefold() for name in plugin_names}),
            "external plugin registry has no duplicates",
            "external plugin registry contains duplicate names",
        )

    source_roles = profile.get("source_roles")
    if isinstance(source_roles, list):
        source_names: list[str] = []
        for index, record in enumerate(source_roles):
            valid = (
                isinstance(record, dict)
                and isinstance(record.get("name"), str)
                and bool(record["name"].strip())
                and record.get("role") in ALLOWED_SOURCE_ROLES
                and is_safe_location(record.get("location"))
            )
            results.require(
                valid,
                f"source role entry {index + 1} is valid",
                f"source role entry {index + 1} is malformed",
            )
            if isinstance(record, dict) and isinstance(record.get("name"), str):
                source_names.append(record["name"])
        results.require(
            len(source_names)
            == len({name.casefold() for name in source_names}),
            "source-role registry has no duplicates",
            "source-role registry contains duplicate names",
        )

    build_profiles = profile.get("build_profiles")
    if isinstance(build_profiles, list):
        build_names: list[str] = []
        for index, record in enumerate(build_profiles):
            valid = (
                isinstance(record, dict)
                and isinstance(record.get("name"), str)
                and bool(record["name"].strip())
                and record.get("kind") in ALLOWED_BUILD_KINDS
                and is_relative_project_path(record.get("entrypoint"))
                and is_safe_location(record.get("artifact"))
                and isinstance(record.get("verification"), list)
                and bool(record["verification"])
                and all(
                    isinstance(item, str) and bool(item.strip())
                    for item in record.get("verification", [])
                )
            )
            results.require(
                valid,
                f"build profile entry {index + 1} is valid",
                f"build profile entry {index + 1} is malformed",
            )
            if isinstance(record, dict) and isinstance(record.get("name"), str):
                build_names.append(record["name"])
        results.require(
            len(build_names)
            == len({name.casefold() for name in build_names}),
            "build-profile registry has no duplicates",
            "build-profile registry contains duplicate names",
        )

    protected = profile.get("protected_material")
    if isinstance(protected, list):
        for index, record in enumerate(protected):
            valid = (
                isinstance(record, dict)
                and isinstance(record.get("category"), str)
                and bool(record["category"].strip())
                and is_safe_location(record.get("location"))
                and record.get("handling") in ALLOWED_HANDLING
            )
            results.require(
                valid,
                f"protected-material entry {index + 1} is valid",
                f"protected-material entry {index + 1} is malformed",
            )

    policy = profile.get("skill_policy")
    results.require(
        isinstance(policy, dict),
        "skill policy mapping is present",
        "profile.skill_policy must be a mapping",
    )
    if isinstance(policy, dict):
        policy_sets: dict[str, set[str]] = {}
        for field in ("preferred", "explicit_only", "disabled", "project_local"):
            values = policy.get(field)
            results.require(
                isinstance(values, list)
                and all(
                    isinstance(item, str) and bool(item.strip())
                    for item in (values if isinstance(values, list) else [])
                )
                and (
                    len(values)
                    == len({item.casefold() for item in values})
                    if isinstance(values, list)
                    and all(isinstance(item, str) for item in values)
                    else False
                ),
                f"skill_policy.{field} is an array",
                f"skill_policy.{field} must be a duplicate-free array of names",
            )
            policy_sets[field] = (
                {item.casefold() for item in values}
                if isinstance(values, list)
                and all(isinstance(item, str) for item in values)
                else set()
            )
        results.require(
            {"uaw", "saw"} <= policy_sets["explicit_only"],
            "UAW and SAW are explicit-only",
            "skill_policy.explicit_only must include uaw and saw",
        )
        results.require(
            not (
                policy_sets["preferred"] & policy_sets["explicit_only"]
                or policy_sets["disabled"]
                & (
                    policy_sets["preferred"]
                    | policy_sets["explicit_only"]
                    | policy_sets["project_local"]
                )
            ),
            "skill policy categories do not conflict",
            "skill policy categories contain conflicting names",
        )

    personalization = profile.get("personalization")
    results.require(
        isinstance(personalization, dict)
        and isinstance(personalization.get("team"), dict)
        and personalization.get("personal_file") == ".maw/local.yaml",
        "personalization layers are structurally valid",
        "personalization must contain team mapping and "
        "personal_file=.maw/local.yaml",
    )

    sensitive = walk_sensitive_keys(profile)
    results.require(
        not sensitive,
        "profile contains no secret-bearing keys",
        "secret-bearing keys are forbidden in shared profile: "
        + ", ".join(sensitive),
    )
    sensitive_values = walk_sensitive_values(profile)
    results.require(
        not sensitive_values,
        "profile contains no recognizable secret values",
        "recognizable secret values are forbidden in shared profile at: "
        + ", ".join(sensitive_values),
    )
    unsafe_locations = walk_unsafe_locations(profile)
    results.require(
        not unsafe_locations,
        "profile contains no absolute paths or URLs",
        "shared profile must use safe relative paths or logical external "
        "roles; unsafe values at: " + ", ".join(unsafe_locations),
    )

    results.require(
        lock.get("schema_version") == 1,
        "lock schema version is 1",
        "lock.schema_version must be 1",
    )
    results.require(
        lock.get("profile_schema_version") == profile.get("schema_version"),
        "lock and profile schema versions agree",
        "lock.profile_schema_version differs from profile schema_version",
    )
    results.require(
        lock.get("source") == "mawcodex",
        "lock source is mawcodex",
        "lock.source must be mawcodex",
    )
    last_update = lock.get("last_update")
    results.require(
        last_update is None
        or (
            isinstance(last_update, str)
            and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", last_update))
        ),
        "lock update date is null or ISO formatted",
        "lock.last_update must be null or an ISO date",
    )
    if isinstance(maw, dict):
        results.require(
            lock.get("maw_version") == maw.get("base_version"),
            "lock and profile MAW versions agree",
            "lock.maw_version differs from maw.base_version",
        )

    local_path = state_root / "local.yaml"
    if local_path.exists():
        try:
            local = load_json_yaml(local_path)
        except ValueError as error:
            results.failures.append(str(error))
        else:
            results.require(
                local.get("schema_version") == 1
                and isinstance(local.get("personal"), dict),
                "personal local layer is structurally valid",
                "local.yaml must contain schema_version 1 and personal mapping",
            )
            local_sensitive = walk_sensitive_keys(local)
            results.require(
                not local_sensitive,
                "personal layer contains no secret-bearing keys",
                "local.yaml is not a credential store; forbidden keys: "
                + ", ".join(local_sensitive),
            )
            local_sensitive_values = walk_sensitive_values(local)
            results.require(
                not local_sensitive_values,
                "personal layer contains no recognizable secret values",
                "local.yaml is not a credential store; recognizable secret "
                "values at: " + ", ".join(local_sensitive_values),
            )
        tracked_result = tracked(project, ".maw/local.yaml")
        if tracked_result is True:
            results.failures.append(".maw/local.yaml must not be tracked")
        elif tracked_result is False:
            results.passes.append(".maw/local.yaml is not tracked")
        else:
            results.warnings.append(
                "Git unavailable; local-layer tracking could not be verified"
            )

    ignore_path = project / ".gitignore"
    ignore_text = (
        ignore_path.read_text(encoding="utf-8", errors="replace")
        if ignore_path.is_file()
        else ""
    )
    results.require(
        ".maw/local.yaml" in ignore_text,
        ".maw/local.yaml is ignored",
        ".gitignore must exclude .maw/local.yaml",
    )
    return results, profile


def print_results(results: Results) -> None:
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("validate", "status"),
        nargs="?",
        default="validate",
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=DEFAULT_ROOT,
        help="project root; defaults to the parent of this script directory",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a machine-readable status document",
    )
    args = parser.parse_args()
    project = args.project.resolve()
    results, profile = validate(project)
    if args.command == "status" and args.json:
        document = {
            "ok": not results.failures,
            "project": profile.get("project") if profile else None,
            "maw": profile.get("maw") if profile else None,
            "capability_ownership": (
                profile.get("capability_ownership") if profile else []
            ),
            "instruction_layers": (
                profile.get("instruction_layers") if profile else None
            ),
            "external_plugins": (
                profile.get("external_plugins") if profile else []
            ),
            "skill_policy": profile.get("skill_policy") if profile else None,
            "source_roles": profile.get("source_roles") if profile else [],
            "build_profiles": (
                profile.get("build_profiles") if profile else []
            ),
            "protected_material": (
                profile.get("protected_material") if profile else []
            ),
            "warnings": results.warnings,
            "failures": results.failures,
        }
        print(json.dumps(document, ensure_ascii=False, indent=2))
    else:
        print_results(results)
    return 1 if results.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
