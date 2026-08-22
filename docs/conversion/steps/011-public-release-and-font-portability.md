# Step 011 - Prepare the public release surface

## Revision

Prepared version `1.2.1` for independent publication. Added an EN-US static
site, a GitHub Pages deployment workflow, public support/privacy/terms pages,
publisher-controlled URL metadata, and a capability ledger that distinguishes
the 52 source-derived skills from six native management skills and the native
ManageRAW agent.

## Attribution treatment

The public site credits Pedro H. C. Sant'Anna as the author of the original
MIT-licensed `claude-code-my-workflow` project and binds the adaptation to
release `v2.1.0`, commit `be53c12f235996dff41fb7f21580506fd2dd8d50`.
MAW Codex contributions are described separately and do not imply upstream
endorsement. Third-party conceptual and code lineage remains linked through
`THIRD_PARTY_NOTICES.md` and the conversion audit.

## XeLaTeX portability revision

The shared project preamble now checks for Lato, Helvetica, Helvetica Neue,
and Arial through `fontspec` before setting document fonts. Missing preferred
families no longer cause an immediate hard-coded-font failure. This is a
target-side portability improvement; it does not change the immutable source
hash. `PROJECT_TEMPLATE_MANIFEST.json` records the reviewed target hash.

The correction remains environment-dependent until an actual consuming deck
is compiled on the target machine. A missing XeLaTeX runtime is UNVERIFIED,
not PASS.

## Publication boundary

The repository-local workflow can deploy `docs/` after the repository is
published and GitHub Pages is configured to use GitHub Actions. This
preparation does not itself authorize or perform commit, push, tag, release
creation, Pages activation, or marketplace submission.
