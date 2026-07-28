# `.maw` profile schema

The canonical contract is
[`manageraw-profile.md`](../../../references/manageraw-profile.md). Read it
before proposing a profile change. This reference shows the exact
machine-readable shape PAW maintains; it does not define a second schema.

Both `.yaml` files use JSON syntax, a valid YAML 1.2 subset. Preserve unknown
fields and serialize deterministically with UTF-8 and a final newline.

## Shared `.maw/profile.yaml`

Schema version 1 contains:

```json
{
  "schema_version": 1,
  "project": {
    "slug": "portable-project-slug",
    "type": "teaching",
    "classification_status": "confirmed",
    "primary_language": "pt-BR"
  },
  "maw": {
    "base_version": "1.2.0",
    "adoption": "thin",
    "governance_owner": "mawcodex",
    "manager_agent": "manageraw"
  },
  "instruction_layers": {
    "global": {"policy": "inherit", "managed": false},
    "project": {
      "path": "AGENTS.md",
      "owner": "team",
      "managed_block": "manageraw"
    },
    "nested": [],
    "personal": {"path": ".maw/local.yaml", "tracked": false}
  },
  "capability_ownership": [
    {
      "capability": "academic_governance",
      "owner": "mawcodex",
      "priority": "primary"
    }
  ],
  "external_plugins": [
    {
      "name": "public-plugin-name",
      "responsibilities": ["bounded responsibility"],
      "status": "optional"
    }
  ],
  "skill_policy": {
    "preferred": ["caw", "jaw", "paw", "law"],
    "explicit_only": ["uaw", "saw"],
    "disabled": [],
    "project_local": []
  },
  "source_roles": [
    {
      "name": "lecture_sources",
      "role": "authoritative",
      "location": "lectures"
    }
  ],
  "build_profiles": [
    {
      "name": "representative_deck",
      "kind": "latex",
      "entrypoint": "lectures/main.tex",
      "artifact": "lectures/main.pdf",
      "verification": ["xelatex compile", "visual PDF inspection"]
    }
  ],
  "protected_material": [
    {
      "category": "answer_keys",
      "location": "solutions",
      "handling": "do-not-export"
    }
  ],
  "personalization": {
    "team": {},
    "personal_file": ".maw/local.yaml"
  }
}
```

Allowed project types are `teaching`, `research`, and `mixed`. Classification
status is `unconfirmed`, `inferred`, or `confirmed`. Adoption is
`plugin-only`, `thin`, `selective`, or `full`.

Capability priority is `primary`, `specialist`, `shared`, or `fallback`.
External-plugin status is `active`, `optional`, `unavailable`, or `disabled`.
Record only a public name and bounded responsibilities, never another
plugin's internal settings.

Source roles are `authoritative`, `mirror`, `import`, `generated`, or
`restricted`. Build kinds are `latex`, `quarto`, `r`, `stata`, `python`,
`julia`, or `other`. Protected-material handling is `local-only`,
`restricted`, `embargoed`, `do-not-export`, or
`institution-controlled`.

When LAW registers an existing nested instruction, it adds a record such as
`{"path": "courses/calculus/AGENTS.md", "owner": "team", "scope":
"calculus course subtree", "managed_block": "manageraw"}`. Use
`"managed_block": null` when the entire file remains human-managed.

LAW, not PAW, changes declared instruction files and the corresponding
`instruction_layers` records. UAW, not PAW, changes `maw.base_version` or the
version lock.

## Personal `.maw/local.yaml`

```json
{
  "schema_version": 1,
  "personal": {
    "preferred_language": "pt-BR",
    "external_plugins": [],
    "settings": {}
  }
}
```

The local file is ignored and may contain non-secret user or machine
preferences. It cannot weaken team safeguards, confidentiality,
reproducibility, verification, or external-action gates. Ignored does not mean
safe for credentials: use the appropriate operating-system or connector
credential store.

## Validation

Run `scripts/manageraw-state.py validate` when the project has the helper.
Otherwise apply the same checks:

- both files parse as JSON-compatible YAML;
- capability, plugin, source-role, and build-profile identifiers are unique;
- UAW and SAW remain explicit-only;
- instruction paths are safe and project-relative;
- source and protected locations are safe relative paths or logical
  `external:<name>` roles;
- `.maw/local.yaml` is ignored and untracked;
- shared state has no secrets, data values, personal identifiers, or absolute
  machine paths;
- profile and lock versions agree;
- missing source authority, build evidence, or protection decisions remain
  UNVERIFIED.
