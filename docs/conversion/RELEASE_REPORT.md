# MAW Codex 1.2.2 release report

Release date: 2026-08-22

## Outcome

MAW Codex `1.2.2` satisfies its local stable-package contract. The package
preserves the fixed upstream academic workflow's intent while replacing its
provider-specific runtime surfaces with Codex-native skills, project agents,
portable roles, opt-in hooks, and explicit verification boundaries.

The public EN-US documentation surface and the portable Lato/Helvetica
fallback were introduced in `1.2.1` and are carried forward unchanged in this
release. The actual `1.2.2` delta is the GitHub identity migration, validation
hardening, expanded project-template provenance, correction of the deep-audit
test command, and pinning plus hash verification of the official Codex skill
validator. The fixed source boundary remains unchanged.

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
- Fifty-one deterministic unit tests pass across executable-asset syntax,
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

The canonical remote is `https://github.com/gdipietra/mawcodex.git`. The remote
runs below are historical deployed-snapshot evidence for commit
`02c76b2c91f673b634c8496b3c49fbd422bbee09`, distinct from the current repaired
local tree pending publication:
[stable-gates run 32603918490](https://github.com/gdipietra/mawcodex/actions/runs/32603918490)
passed on Windows and Ubuntu, and
[GitHub Pages run 32603918449](https://github.com/gdipietra/mawcodex/actions/runs/32603918449)
passed build and deployment. The current readiness-document changes postdate
that commit and require an authorized push plus fresh remote checks before
sharing the repository as the reviewed public surface. No GitHub Release is
claimed by this report.

## GitHub username migration (2026-08-22)

Release `1.2.2` changes the operational repository and Pages identity to
`gdipietra`. The release gates bind current source evidence to the new fork and
Pedro H. C. Sant'Anna's upstream. Live deployment is a separate post-push gate;
a successful local release snapshot does not by itself prove Pages availability.

## Known issue disposition and public sharing

On Windows, `scripts/maw.cmd` can select the non-runnable WindowsApps
`python.exe` alias before the bundled Codex runtime. The explicit-runtime
workaround is verified, and the installed plugin is not affected after Codex
loads it. This operational launcher limitation is documented for `1.2.2`; it
does not imply or promise a `1.2.3` release.

The controlled communication decision and evidence boundary are recorded in
`PUBLIC_RELEASE_READINESS-1.2.2.md`. The local package is ready for review,
first by Pedro H. C. Sant'Anna and then by a small group of close colleagues.
The repository and site links remain pending authorized publication and
post-push verification. Broader announcement remains a deliberate human
decision after that feedback sequence.
