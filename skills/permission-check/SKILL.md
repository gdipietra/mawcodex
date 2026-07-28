---
name: permission-check
description: "Diagnose why Codex is or is not requesting approval by inspecting the active workspace boundary, project configuration, session mode, CLI overrides, profiles, rules, and managed requirements. Use for requests such as \"why is it asking me to approve?\", \"permission check\", \"why am I getting prompts?\", \"full access is not working\", \"bypass is not working\", or \"check my Codex permissions\". Read-only; host-global configuration is inspected only with explicit consent and sensitive keys are redacted."
---

# Permission Check

Explain the effective Codex permission state without changing it. Keep three
questions separate:

1. **Sandbox or permission profile:** what local commands can technically read,
   write, or reach?
2. **Approval policy and reviewer:** which attempted actions pause, are
   rejected, or go to automatic review?
3. **Action-specific policy:** do exec rules, app or MCP approvals, managed
   requirements, or external-side-effect gates impose an additional check?

Changing who reviews a request does not expand the sandbox.

## Privacy boundary

Run the repository-local phase automatically. Before reading user, system, or
organization-delivered configuration outside the workspace, ask for explicit
consent and name the exact paths or diagnostics. Extract only permission,
sandbox, approval, rule, network, trust, and reviewer keys. Never print an
entire host configuration file, token, MCP credential, provider setting,
telemetry payload, unrelated path, or secret.

This workflow is read-only. It never changes configuration, trust, rules, or
the active mode.

## Current Codex configuration model

For ordinary configuration values, diagnose this precedence order from highest
to lowest:

1. CLI flags and `--config` overrides;
2. trusted project `.codex/config.toml` files from project root toward the
   current directory, with the closest winning;
3. a selected `~/.codex/<profile>.config.toml`;
4. user `~/.codex/config.toml`;
5. system config such as `/etc/codex/config.toml` on Unix;
6. built-in defaults.

Managed requirements constrain what lower layers may select and must be
reported separately rather than treated as another ordinary override.
Untrusted projects do not load project `.codex/` config, hooks, or rules.

Codex supports two configuration families that must not be mixed:

- permission profiles: `default_permissions` plus `[permissions.<name>]`;
- legacy sandbox settings: `sandbox_mode`, `approval_policy`, and optional
  `[sandbox_workspace_write]`.

If a loaded layer or CLI flag selects legacy `sandbox_mode`, it can supersede
the local permission-profile selection. Report mixed-family configuration as a
specific conflict. Permission profiles are evolving; when exact behavior
matters, verify it against the installed client's current official
documentation.

## Phase A: repository-local inspection

1. Resolve the project root and current working directory.
2. Record whether the project is trusted. If trust cannot be observed, mark it
   `UNVERIFIED`; do not assume project config loaded.
3. From root to current directory, inspect only existing
   `.codex/config.toml` files and relevant `.codex/rules/*.rules`.
4. Extract:
   - `default_permissions`;
   - `[permissions.*]` filesystem, workspace-root, and network policy;
   - `sandbox_mode`, `approval_policy`, `approvals_reviewer`;
   - `[sandbox_workspace_write].network_access`;
   - any project rule that matches the command at issue.
5. Record the effective runtime workspace roots when visible. In a live Codex
   client, use the permissions control or `/status`; do not infer roots solely
   from the repository path.
6. Check whether the attempted action is:
   - outside a writable root;
   - networked;
   - destructive or externally visible;
   - an app or MCP mutation;
   - matched by an execution rule;
   - a skill script requiring its own approval.

If this phase explains the prompt, stop and report the diagnosis without
reading host-global files.

## Phase B: host and managed layers

If Phase A is inconclusive, ask permission to inspect only the relevant
locations. Depending on platform and invocation, these may include:

- the selected CLI command and flags;
- `~/.codex/config.toml`;
- `~/.codex/<selected-profile>.config.toml`;
- system Codex configuration;
- managed requirements diagnostics.

Prefer the client's `/debug-config` output because it shows layer order,
enabled state, and policy sources. Ask the user to run or authorize it if the
surface cannot be invoked directly. Redact unrelated content.

## Compute and report the effective state

For each relevant setting, identify the winning ordinary layer and any managed
constraint. Then compare it with the live session:

- selected permission mode or profile;
- workspace roots and their read/write/deny status;
- network state and domain rules;
- approval policy;
- approval reviewer (`user` versus automatic review);
- matching execution rule;
- app or MCP side-effect approval;
- trust state;
- client/version caveat.

Common diagnoses include:

- the target is outside the active workspace;
- the project is untrusted, so its `.codex/` layer is ignored;
- a CLI flag overrides a project or profile setting;
- a closer nested project config wins;
- legacy `sandbox_mode` and permission-profile settings are mixed;
- `deny` overrides a broader read or write grant;
- network is disabled or the domain is not allowlisted;
- automatic review is enabled but the sandbox still blocks the action;
- a managed requirement disallows the requested mode;
- an execution rule or app/MCP mutation requires approval independently;
- the user changed config after the session began and must start a new task or
  client session for startup-loaded settings to refresh.

## Output

```text
PERMISSION DIAGNOSIS

Runtime
- client/surface:
- project trust:
- active workspace roots:
- selected mode/profile:

Effective controls
- filesystem:
- network:
- approval policy:
- approval reviewer:
- matching rule or external-action gate:

Precedence evidence
- winning layer per key:
- managed constraints:
- mixed-family conflict:

Diagnosis
- cause:
- evidence:
- safe next check:
- status: CONFIRMED / PARTIAL / UNVERIFIED
```

Never recommend dangerous full access as the default fix. Prefer the narrowest
workspace root, domain rule, command rule, or one-turn escalation that enables
the requested action. Offer a configuration change only after the read-only
diagnosis, and make it a separate explicitly authorized task.
