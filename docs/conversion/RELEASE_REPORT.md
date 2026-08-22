# MAW Codex 1.2.1 release report

Release date: 2026-08-22

## Outcome

MAW Codex `1.2.1` satisfies its local stable-package contract. The package
preserves the fixed upstream academic workflow's intent while replacing its
provider-specific runtime surfaces with Codex-native skills, project agents,
portable roles, opt-in hooks, and explicit verification boundaries.

This patch release adds a public EN-US documentation surface and publication
metadata without changing the fixed source boundary. The website gives Pedro
H. C. Sant'Anna direct original-work credit, provides a capability-level map
of the 52 adapted workflows, and documents the six native management skills
plus ManageRAW separately. It also records the portable Lato/Helvetica
fallback added to the shared XeLaTeX preamble.

## Inventory and semantic review

- Skills: 58/58 structurally valid; 52/52 source-derived skills remain
  semantically reviewed and all 6 ManageRAW skills are validated native
  additions.
- Custom agents: 19/19 TOMLs parse and map to 19 portable roles; the fixed
  source boundary remains 18/18 and `manageraw` is native.
- Rules: 32/32 adapted and indexed.
- References: 9 runtime references plus 1 retained historical reference.
- Templates: 21/21 reusable artifact templates.
- Hooks: all 7 upstream intents mapped; 4 use native lifecycle events.
- Other provider surfaces: root instructions, settings, 2 output styles,
  status line, and quick reference all have documented native dispositions.

## Evidence

- The source clone at `C:\GitHub\claude-code-my-workflow` is clean on `main`,
  has Giovanni's fork as `origin`, Pedro's repository as `upstream`, and is
  fixed at commit `be53c12f235996dff41fb7f21580506fd2dd8d50`.
- The official plugin validator passes the `mawcodex` package manifest and
  directory structure.
- The official skill validator passes 58/58 current skills.
- Seventeen independent forward tests pass, including missing-runtime,
  restricted-data, disclosure, publication, Git-scope, and evidence-gap
  scenarios.
- Forty-eight deterministic unit tests pass across executable-asset syntax,
  hook behavior, the POSIX launcher, project initialization, ManageRAW state,
  local installation, provenance, and semantic contracts.
- All source/target component hashes, 18 project-template transformations,
  relative links, attribution records, and provider-residue checks pass.
- The imported TeX sample safely typesets `\$skill`, the Quarto sample keeps
  normal `$skill` code spans, and the TeX, TikZ, YAML, and Quarto samples pass
  their representative syntax or forward-build checks.
- JAW's research, teaching, mixed-project, collision, dependency, authority,
  and rollback contracts pass structural and semantic checks.
- The two initial ManageRAW use cases pass independent review: ongoing
  LaTeX-heavy teaching with protected assessments, and ongoing mixed Stata/R
  research with unresolved source and data roles.
- The project state validator enforces shared versus personal configuration,
  capability ownership, instruction-layer declarations, protected-material
  categories, explicit-only UAW/SAW policy, and version-lock agreement.
- Official evidence is bound to a portable SHA-256 snapshot of the complete
  release-relevant tree; changes to code, tests, docs, or package assets make
  the stable gate stale until it is rerun.

Machine-readable details are in `OFFICIAL_VALIDATION.json`,
`FORWARD_TEST_RESULTS.json`, `SOURCE_MANIFEST.json`, and
`PROJECT_TEMPLATE_MANIFEST.json`. `RUNTIME_SURFACES_MANIFEST.json` separately
binds all 7 hooks and 6 other provider runtime surfaces.
`AUXILIARY_SOURCE_MANIFEST.json` completes exact 211/211 tracked-file coverage
for repository support files that were rewritten, retained, or intentionally
omitted.

## Stable boundary

Stable means the package is installable, its recorded surfaces and safety
contracts pass locally, and the conversion is auditable. It does not claim
that optional R, Stata, Julia, LaTeX, Quarto, browser, journal, data enclave,
or institutional disclosure operations have run in every future project.
Those checks remain `UNVERIFIED` until the required runtime, source, or human
authority is available.

The repository has no configured remote in this local release state. The
GitHub Pages and stable-gates workflows therefore have not run remotely, and
no live-site, remote-CI, GitHub Release, or marketplace-publication result is
claimed by this report.
