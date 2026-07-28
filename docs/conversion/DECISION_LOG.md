# Conversion decision log

## D-001 — Separate tracked fork and native implementation

**Decision:** Keep the upstream-tracking fork at
`C:\GitHub\claude-code-my-workflow` and the Codex-native package at
`C:\Codex\mawcodex`.

**Reason:** Directly translating inside the fork would make upstream merges
noisy and obscure which changes are provider migration versus upstream work.

## D-002 — Package as a Codex plugin

**Decision:** Use a root `.codex-plugin/plugin.json` with packaged skills,
optional hooks, assets, and scripts.

**Reason:** This is the smallest current Codex distribution surface that
preserves reusable skills and lifecycle behavior.

## D-003 — Dual representation for agents

**Decision:** Convert each upstream agent into both a project custom-agent TOML
and a portable role Markdown file.

**Reason:** `.codex/agents/` provides native local execution and sandbox
defaults, while role files let packaged skills preserve the behavior when
custom agent configuration is not installed with the plugin.

## D-004 — Safe settings instead of permission bypass

**Decision:** Do not port Claude's `bypassPermissions` or broad `Bash(*)`,
write, and network allowlists.

**Reason:** Permission behavior belongs to the user's active Codex policy.
MAW Codex enables multi-agent and hook features but does not silently expand
filesystem, network, or external-action authority.

## D-005 — Mechanical conversion is not acceptance

**Decision:** Generate a one-to-one mechanical baseline, then semantically
review every skill in explicit batches.

**Reason:** Tool-name substitution alone cannot preserve context isolation,
agent orchestration, verification gates, or failure semantics.

## D-006 — Port hook intent, not Claude transcript internals

**Decision:** Enable four Codex-native lifecycle mappings and represent the
other three upstream hooks through native UI, skills, and explicit workflows.
Do not read or estimate tokens from Codex transcript files.

**Reason:** Codex exposes stable hook inputs for tool use, compaction, and
session start. Transcript serialization is not a compatibility contract.
Depending on it would make context monitoring brittle and could expose session
content unnecessarily.

## D-007 — Ship a safe project initializer

**Decision:** Package the reusable research-project structure under
`assets/project-template/` and install it through `scripts/init_project.py`.
Copy portable references and custom-agent definitions into initialized
projects by default.

**Reason:** The original workflow's value includes its directory conventions,
analysis pipeline, presentation parity, and durable quality records. A
non-overwriting initializer preserves those features without forcing users to
fork the provider-specific source repository or silently changing an existing
project.

## D-008 — Install through the personal marketplace

**Decision:** Provide a preview-first local installer that copies the curated
package to the user's Codex plugin area and adds one canonical entry to the
existing local marketplace (or creates a Personal catalog when none exists).
Require `--apply` for installation and `--update` for replacement.

**Reason:** A repository path alone is not a documented plugin-discovery
contract. The installer preserves the existing catalog identity and entries,
makes timestamped update backups, and leaves project initialization separate.

## D-009 — Make stability evidence reproducible

**Decision:** Promote the package to stable only after the fixed source clone,
official plugin validator, all 52 official skill validations, deterministic
unit tests, provenance hashes, and independent forward tests agree.

**Reason:** A self-declared conversion status cannot establish behavioral
portability. Machine-readable evidence binds representative observations to
the exact skill text and makes later drift visible.

## D-010 — Separate the ManageRAW control plane

**Decision:** Add the native `manageraw` agent and six narrow management
skills: JAW for joining, CAW for coordination, PAW for personalization, LAW
for instruction layers, UAW for updates, and SAW for reusable slices.

**Reason:** A single personalization capability would quickly absorb
onboarding, instruction precedence, plugin collisions, updates, and export
policy. Separate skills keep authority and verification boundaries legible.

## D-011 — Record configuration without replacing instructions

**Decision:** Track shared routing decisions in JSON-compatible
`.maw/profile.yaml`, keep personal choices in ignored `.maw/local.yaml`, and
retain actual Codex behavior in global, root, and nested `AGENTS.md`.

**Reason:** The project needs durable ownership and adoption state, but a
parallel instruction engine would create ambiguous precedence. The JSON
compatible YAML subset also permits deterministic validation without adding a
package dependency to every academic project.
