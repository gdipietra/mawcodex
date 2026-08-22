# Publish MAW Codex and its GitHub Pages site

This repository is prepared for publication at:

- source: `https://github.com/dipietra/mawcodex`
- website: `https://dipietra.github.io/mawcodex/`

These are intended publisher-controlled endpoints. They are not evidence of a
live release until the external steps below have completed and been verified.

## Local release gate

Run from the repository root:

```powershell
.\scripts\maw.cmd all
```

The command checks the fixed upstream source contract, package structure,
provenance, official Codex plugin and skill schemas, unit tests, and the final
stable-release evidence. Do not continue while any required check is FAIL or
UNVERIFIED.

## External publication sequence

Each state-changing Git or GitHub action requires explicit authorization.

1. Create the public `dipietra/mawcodex` repository with no generated starter
   files.
2. Add it as this checkout's `origin`, inspect the exact diff, and push the
   reviewed `main` branch.
3. In GitHub **Settings > Pages**, choose **GitHub Actions** as the publishing
   source.
4. Confirm that `stable-gates` passes on Linux and Windows.
5. Confirm that `github-pages` deploys `docs/` and reports the expected URL.
6. Inspect the homepage, capability filters, credits, support, privacy, terms,
   mobile layout, and all internal links on the live site.
7. Create the signed or annotated `v1.2.1` tag and GitHub Release only after
   the remote evidence is clean.
8. Treat any Codex marketplace submission as a separate publication action;
   verify publisher identity, listing metadata, and installation in a fresh
   Codex thread.

## Rollback

If Pages deploys incorrect content, disable the Pages source or revert the
publication commit through a normal reviewed change. Do not rewrite published
history or force-push as a routine rollback.

## Evidence language

- Local gates passing means **locally release-ready**.
- Remote workflows passing means **remote CI verified**.
- A successful Pages job plus live inspection means **site deployed**.
- A GitHub Release or marketplace listing exists only after that separate
  external action succeeds.

Never collapse these states into a single "published" claim.
