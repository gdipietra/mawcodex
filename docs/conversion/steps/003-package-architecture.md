# Step 003 — Codex package architecture

**Date:** 2026-07-28  
**Status:** `validated`

## Goal

Choose the smallest Codex-native surfaces that preserve the workflow's intent.

## Revision

- Scaffolded a Codex plugin at `C:\Codex\mawcodex`.
- Added repository `AGENTS.md` instructions with research and conversion
  safeguards.
- Reserved packaged `skills/`, optional trusted `hooks/`, reusable `assets/`,
  and deterministic `scripts/`.
- Reserved `.codex/agents/` for native local roles and
  `references/agent-roles/` for portable equivalents.
- Added safe multi-agent/hook feature configuration without permission bypass.
- Initialized an independent Git repository on branch `main`.

## Review

This split preserves installable skills and hooks while acknowledging that
project custom agents are a repository configuration surface. Portable role
files prevent a hard runtime dependency on those TOML files.

## Verification

The official plugin validator passes at version `1.0.0`; package validation
confirms the manifest, 52-skill inventory, agent configuration, hooks,
provider-residue scan, and relative links.
