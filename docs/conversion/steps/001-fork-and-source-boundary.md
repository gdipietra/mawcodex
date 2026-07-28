# Step 001 — Fork and source boundary

**Date:** 2026-07-28  
**Status:** complete

## Goal

Preserve a clean upstream relationship before translation begins.

## Revision

- Forked `pedrohcgs/claude-code-my-workflow` to
  `dipietra/claude-code-my-workflow`.
- Cloned the fork to `C:\GitHub\claude-code-my-workflow`.
- Kept the fork as `origin`.
- Added Pedro's repository as `upstream` and fetched its branches and tags.
- Verified a clean `main` working tree at release `v2.1.0`, commit
  `be53c12f235996dff41fb7f21580506fd2dd8d50`.
- Added `scripts/check_source_clone.py` in MAW Codex to recheck the exact
  remotes, branch, tag, commit, and clean tree. Its optional `--fetch` mode
  updates only upstream refs and reports reviewable commits; it never merges
  or moves the fixed checkout.

## Review

The fork and native implementation are intentionally separate. Future upstream
updates can be inspected as deltas without mixing provider-specific layouts.
The checker passes against the documented local clone and currently reports no
newer commit in the locally visible `upstream/main`.
