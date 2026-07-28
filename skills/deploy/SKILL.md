---
name: deploy
description: "Prepare and, when explicitly authorized, publish Quarto slides through the repository's configured deployment path. Renders locally, syncs `docs/`, verifies HTML/assets/TikZ and visual output, then stops before any required commit or push unless those actions were separately authorized. Use for deploy or publish requests, not a render-only check."
---

## Codex execution contract

- Treat the user's request and applicable `AGENTS.md` files as authoritative.
- Resolve referenced resources relative to this skill first.
- Use bounded, isolated subagents for independent review roles; when a
  project custom agent is unavailable, use the matching portable role in
  `../../references/agent-roles/`.
- Treat missing tools, inaccessible sources, and skipped checks as
  UNVERIFIED rather than PASS.
- Require explicit user authorization for commit, push, merge, deploy,
  submission, sending, or other external publication.

# Deploy Slides to GitHub Pages

Render Quarto slides, sync the local publication tree, verify it, and perform
only the externally visible actions the user explicitly authorized.

## Steps

1. **Resolve scope and deployment mechanism.**
   - Use the user-supplied lecture identifier when present; otherwise confirm
     whether the request covers all lectures.
   - Read the repository's Pages configuration and sync script before running
     it. Do not assume that updating `docs/` publishes automatically.
   - Distinguish local render, local sync, commit, push, and live publication.
     A deploy request authorizes deployment, but does not silently authorize a
     required Git commit or push under this package's repository rules.

2. **Render and sync locally.**
   - Run `scripts/sync_to_docs.sh <lecture>` or its platform-appropriate
     equivalent only after inspecting its behavior.
   - If no lecture was specified and all-lecture scope is clear, run the
     documented all-lecture mode.

3. **Verify the local publication tree:**
   - Check that HTML files exist in `docs/slides/`
   - Check that `_files/` directories were copied (RevealJS assets)
   - Check that `docs/Figures/` was synced from `Figures/`

4. **Verify interactive charts** (if applicable):
   - Grep rendered HTML for interactive widget count
   - Confirm count matches expected

5. **Verify TikZ SVGs** (if applicable):
   - Check that all referenced SVG files exist in `docs/Figures/LectureN/`

6. **Preview in a browser.**
   Use the available browser-control capability to open the local HTML and
   inspect representative slides, images, navigation, fonts, and interactive
   elements. Compilation alone is not visual PASS.

7. **Publish only through the configured path.**
   - If live publication requires commit or push and that action was not
     explicit, stop with the verified local tree and request that authorization.
   - If the configured deployment uses another external service, confirm its
     exact target and use the supported deployment capability.
   - Inspect the live URL after the deployment reaches a terminal state.

8. **Report results.**
   Separate local render PASS, visual PASS, publication status, and any
   UNVERIFIED checks. Include the live URL only when deployment is confirmed.

## What the sync script does:
- Renders all `.qmd` files in `Quarto/` (skips `*_backup*` files)
- Copies HTML and `_files/` directories to `docs/slides/`
- Copies Beamer PDFs from `Slides/` to `docs/slides/`
- Syncs `Figures/` to `docs/Figures/` using rsync

If Quarto, the sync utility, browser preview, deployment credentials, or live
URL is unavailable, mark the affected stage UNVERIFIED. Never call a local
`docs/` update a successful deployment.
