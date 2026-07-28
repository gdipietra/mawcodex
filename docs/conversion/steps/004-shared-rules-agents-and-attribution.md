# Step 004 — Shared rules, agents, and attribution

**Date:** 2026-07-28  
**Status:** `validated`

## Goal

Preserve the original rule and reviewer intent on Codex-native surfaces with a
reviewable rights chain.

## Revision

- Converted 32 rule files into portable references with explicit applicability
  and a generated routing index.
- Converted all 18 agents into project custom-agent TOML plus portable role
  definitions.
- Assigned read-only sandboxes to reviewers and workspace-write only to roles
  that compile, check, translate, or implement.
- Replaced provider model aliases with durable reasoning-effort routing.
- Migrated nine shared references and 21 academic templates.
- Audited upstream third-party credits and added package notices.
- Cleanly reimplemented the MixtapeTools-derived TikZ rules and the
  CC-BY-NC Material Passport-derived replication concept.

## Review

The main behavior difference is rule routing: plugin reference files cannot
auto-apply Claude glob frontmatter. Applicable skills and project
`AGENTS.md` must load matching rules through `references/rules/INDEX.md`.

## Verification

All 18 custom-agent TOMLs parse and map to portable roles. All 32 rules, 9
references, and 21 templates have current source/target hashes, allowed
classifications, and per-component revision summaries in
`SOURCE_MANIFEST.json`. Attribution and provider-residue gates pass.
