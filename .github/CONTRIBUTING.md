# Contributing

MAW Codex is a general academic-workflow package. Contributions should
preserve scientific safeguards and work across more than one project or
discipline unless they are explicitly labeled as a domain-specific extension.

## Before changing a component

1. Read `AGENTS.md` and the applicable nested instructions.
2. Fix the source boundary. If this is an upstream refresh, follow
   `docs/UPSTREAM_SYNC.md`.
3. Record the behavioral intent, authorization boundaries, and verification
   plan.
4. Preserve user changes and never use provider permission bypasses.

## Required checks

Run:

```text
scripts\maw.cmd all
```

That command checks the fixed source clone, runs Codex's official plugin and
skill validators, executes the full test suite, writes current validation
evidence, and applies the stable package gate. For a skill change, also update
`docs/conversion/skills/<name>.md` and the bound forward-test hash when the
skill is in the representative matrix. For hook changes, test both the Python
and PowerShell contracts. For rendered academic artifacts, inspect the
rendered result rather than relying on source review.

## Pull requests

- Keep one coherent concern per pull request.
- Explain why behavior changed, not only which lines changed.
- Include actual check results and remaining UNVERIFIED items.
- Update counts, maps, hashes, stability evidence, and third-party notices when
  their source changes.
- Do not include project data, credentials, personal settings, generated
  conversion output from a different baseline, or unpublished research
  material.
