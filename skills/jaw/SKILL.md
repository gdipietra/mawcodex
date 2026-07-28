---
name: jaw
description: "Assess and safely join MAW Codex to a new or ongoing research, teaching, or mixed academic project. Use for onboarding readiness, dependency checks, source-of-truth mapping, collision analysis, adoption choice, or before creating project-local MAW state."
---

# JAW — Join Academic Workflow

Fit MAW to the project that already exists or is about to start. Preserve its
history, working conventions, source authority, and usable toolchain while
adding only MAW surfaces that provide clear value. JAW owns onboarding and
readiness; it hands ongoing configuration to ManageRAW's other skills.

## Default contract

- Begin in assessment-only mode. Read and test; do not install, initialize,
  overwrite, commit, push, sync, publish, or change an environment.
- Treat the user's request and every applicable `AGENTS.md` as authoritative.
- Preserve dirty worktrees and existing project-specific skills or
  instructions.
- Run builds in a temporary or ignored output directory. Never leave smoke-test
  artifacts beside the user's source files.
- Record missing tools, inaccessible sources, and skipped checks as
  UNVERIFIED, not PASS.
- Require explicit authorization before applying the proposed integration and
  again before any external action.

Read [`manageraw-profile.md`](../../references/manageraw-profile.md) before
proposing project-local MAW state.

## 1. Establish the target

Resolve the project root, current repository state, and applicable
instructions. Classify the project from evidence:

- **Research:** data, analysis code, manuscripts, empirical outputs, or a
  replication workflow dominate. Load
  [`research-project.md`](references/research-project.md).
- **Teaching:** course notes, slides, exercise lists, exams, solutions, or
  classroom publishing dominate. Load
  [`teaching-project.md`](references/teaching-project.md).
- **Mixed:** both sets are material. Load both profiles and state which source
  controls each output.

Do not force a label from the folder name. If the classification changes the
integration and the evidence is ambiguous, ask one focused question.

## 2. Map the project before proposing changes

Inspect:

1. Git state, tracked and untracked files, remotes, default branch, and whether
   the directory is a real repository.
2. Root and nested instructions, existing skills, automation, hooks, CI, and
   local conventions.
3. Existing `.maw/profile.yaml`, `.maw/lock.json`, ignored personal overlay,
   and managed instruction blocks, if any.
4. The source-of-truth role of local Git, GitHub, Overleaf, Drive, Dropbox, or
   another mirror. Never infer that a synchronized copy is authoritative.
5. Build entry points and representative artifacts for every detected stack:
   LaTeX engines, Quarto/Pandoc, R, Python/Jupyter, Stata, bibliography tools,
   and PDF inspection.
6. Sensitive or restricted inputs, credentials, solution keys, embargoed
   materials, and outputs that must not be exported.
7. Naming or path collisions with MAW's proposed `AGENTS.md`, `.maw/`,
   `.codex/`, `skills/`, `references/`, `scripts/`, `assets/`, and report
   directories.

Summarize findings as evidence, not guesses.

## 3. Choose an integration shape

Recommend the smallest coherent option:

| Option | Best fit | What changes |
| --- | --- | --- |
| Plugin only | User wants MAW skills without repository files | Install or enable the plugin; preserve the project tree |
| Thin project profile | Mature ongoing project; default recommendation | Add tailored `.maw` state, one managed root instruction block, and only necessary helpers |
| Selective merge | Project needs several MAW templates or checks | Merge an explicit file list with collision-by-collision review |
| Full initializer | New or nearly empty project | Add the complete project scaffold after approval |

Never replace an existing project skill merely because MAW has a similar one.
Prefer composition, project-local routing, or a documented choice of authority.
Route overlapping plugin or skill responsibilities to `$caw`.

## 4. Prove dependency readiness

For every intended capability, check both discovery and behavior:

1. Resolve the executable and version.
2. Check wrappers separately from the underlying binary.
3. Run a minimal representative forward build in an isolated directory.
4. Inspect the produced artifact when rendering or layout matters.
5. Remove or retain the isolated evidence according to the user's request.

For LaTeX, test the engine actually required by the project plus bibliography
and any material packages. For Quarto, render the actual target format rather
than relying on `quarto check`. For R, Python, or Stata, test the project's
entry point or a representative script without mutating raw data.

Use PASS, FAIL, and UNVERIFIED per component. A version string alone is not a
forward test.

## 5. Ask only for decisions the project cannot answer

Ask the user when a choice materially changes the result:

- Which local or remote copy controls each artifact?
- Should MAW be plugin-only, thin, selective, or full?
- May JAW initialize Git, add a remote, install software, or alter an
  environment?
- Are there restricted data, solution keys, embargoes, or publication limits?
- May MAW create project instructions, hooks, CI, or ignored output folders?
- Who may authorize sync, publication, submission, or collaborator handoff?

Do not ask the user to run a check that Codex can safely run read-only.

## 6. Produce the readiness decision

Use the schema in
[`readiness-report.md`](references/readiness-report.md). Unless the user asks
for a file, deliver the report in conversation. When authorized to write it,
use:

`quality_reports/jaw/YYYY-MM-DD_<project-slug>_deployment-readiness.md`

The report must include:

- project type and source-role map;
- detected instructions and protected materials;
- compatibility and collision matrix;
- dependency evidence with exact forward tests;
- recommended integration option;
- exact proposed additions, edits, and untouched paths;
- user decisions still needed;
- verification and rollback plan;
- verdict: READY, READY WITH DECISIONS, NOT READY, or UNVERIFIED.

For a thin, selective, or full adoption, include the proposed initial
`.maw/profile.yaml` fields and version lock. Keep the file in JSON-compatible
YAML. Route shared project choices to `$paw` and root or nested instruction
design to `$law`.

## 7. Apply only after approval

After the user approves an exact plan:

1. Capture the pre-change Git status and any relevant checksums.
2. Apply the smallest approved file set.
3. Preserve existing content and merge instructions deliberately. Use LAW
   for exact managed blocks and PAW for the initial shared profile.
4. Run structural validation and the representative project builds again.
5. Show the final diff, evidence, and remaining manual actions.

Approval to integrate locally does not authorize commit, push, installation,
sync, publication, submission, or sending.

Once the initial adoption and readiness report are complete, stop. Do not use
JAW for routine personalization, instruction-layer maintenance, upstream
updates, or reusable-pattern exports; route those to PAW, LAW, UAW, or SAW.

## Cross-references

- [`$capture-environment`](../capture-environment/SKILL.md) — snapshot research
  runtimes after the integration plan is approved.
- [`$caw`](../caw/SKILL.md) — resolve overlapping plugin or skill ownership.
- [`$paw`](../paw/SKILL.md) — record shared and personal project settings.
- [`$law`](../law/SKILL.md) — design root and nested instruction layers.
- [`$compile-latex`](../compile-latex/SKILL.md) — project LaTeX forward tests.
- [`$deploy`](../deploy/SKILL.md) — publication remains a separate authorized
  action.
- [`$audit-reproducibility`](../audit-reproducibility/SKILL.md) — research
  reproducibility after readiness is established.
- [`$pedagogy-review`](../pedagogy-review/SKILL.md) — teaching-material review
  after readiness is established.
