# Academic project instructions

<!-- manageraw:begin -->
## MAW control plane

- Treat `.maw/profile.yaml` as the shared, tracked record of MAW adoption,
  capability ownership, source roles, build profiles, and instruction layers.
- Treat `.maw/local.yaml`, when present, as an untracked personal overlay. It
  may choose personal preferences but may not weaken team, safety,
  confidentiality, verification, or release requirements.
- MAW owns academic governance. Route overlapping plugin or skill behavior
  through `$caw`, onboarding through `$jaw`, shared personalization through
  `$paw`, and root or nested instruction design through `$law`.
- Invoke `$uaw` and `$saw` only when the user names or clearly requests those
  maintenance operations. Neither runs automatically.
- Preserve existing project files and instructions. Any edit to this managed
  block or `.maw/` shared state requires an exact preview and approval.
- External actions remain separately authorized even when a local MAW change
  is approved.
<!-- manageraw:end -->

## Mission

Maintain a local-first, reproducible academic-research project. Treat
scientific validity, provenance, confidentiality, and clear uncertainty as
hard requirements. A polished artifact is not complete when its underlying
claim or build remains unverified.

## Source roles

Before moving or syncing material, document which location is authoritative
for each source:

- local Git repository: analysis, writing, and revision source of truth;
- raw-data origin: immutable input, possibly access-restricted;
- Overleaf, Drive, or another collaboration surface: mirror, consultation
  source, or controlled import/export;
- generated outputs: reproducible products, never substitutes for source code.

Do not overwrite a collaborator-facing or cloud version until the user
explicitly authorizes that sync. Preserve a comparison version and unresolved
checks when handing work off.

## Operating modes

- **Orient:** inspect instructions, git state, source roles, data sensitivity,
  active plans, and relevant MAW Codex skills.
- **Specify:** for ambiguous work, record MUST, SHOULD, and MAY requirements in
  `quality_reports/specs/`.
- **Plan:** define inputs, outputs, estimands or content invariants, risks, and
  verification in `quality_reports/plans/`.
- **Implement:** make the smallest coherent change within the authorized
  project scope.
- **Verify:** execute deterministic checks and visually inspect rendered
  artifacts when layout matters. Report PASS, FAIL, and UNVERIFIED separately.
- **Release:** reconcile code, prose, tables, figures, citations, disclosures,
  and provenance. External sharing still requires explicit authorization.

## Research safeguards

- Never invent a citation, dataset, estimate, sample definition, institutional
  fact, or source quotation.
- Verify unstable or externally sourced claims with primary sources. Record
  inaccessible evidence as UNVERIFIED.
- Keep `data/raw/` immutable. Put transformations in scripts and derived data
  in a documented non-raw location.
- Never expose credentials, personal identifiers, restricted microdata, or
  enclave-controlled material. Review disclosure risk before export.
- Record exclusions, joins, variable construction, missing-data handling,
  seeds, software versions, and inference choices.
- A skipped command, unavailable package, inaccessible source, unrendered
  document, or failed test is not a pass.
- Do not silently weaken a research or verification gate. Record any explicit
  exception and its consequences.

## Applied microeconomics and econometrics

For every causal result, identify:

1. estimand and unit of observation;
2. treatment definition, timing, and exposure window;
3. comparison group and identifying variation;
4. identifying assumptions and their substantive meaning;
5. sample restrictions, missingness, attrition, and weighting;
6. inference method, clustering level, and small-cluster concerns;
7. diagnostics, sensitivity analyses, and threats to external validity.

For staggered adoption, do not treat an unqualified two-way fixed-effects
coefficient as the default causal estimand. Use cohort/time-aware methods or
justify the design explicitly. Treat pre-trend tests as diagnostics, not proof
of parallel trends. Keep alternative estimands and balanced-sample results
clearly labeled rather than presenting them as interchangeable.

## File routing

- `scripts/R/`: reproducible numbered R pipeline; run `00_run_all.R`.
- `data/raw/`: immutable inputs; never edit in place.
- `data/derived/`: reproducibly generated analysis inputs.
- `Figures/`: generated or source figure assets with traceable scripts.
- `Slides/` and `Quarto/`: presentation sources.
- `Preambles/`: shared LaTeX conventions and palette.
- `templates/`: reusable project records and artifact templates.
- `explorations/`: provisional work with an explicit graduate/archive decision.
- `quality_reports/`: plans, specifications, decisions, audits, passports,
  checkpoints, diagnoses, and session logs.

## Artifact parity

- Name the source of truth before editing duplicate Beamer, Quarto, manuscript,
  table, or figure surfaces.
- Keep numeric claims traceable to scripts and output fields through a passport
  or equivalent provenance record.
- When changing analysis code, identify affected tables, figures, prose, and
  passport entries before declaring completion.
- Render and inspect PDFs, slides, documents, charts, and tables; source review
  alone cannot establish visual correctness.

## Codex workflow

- Read the selected MAW Codex skill completely and follow its linked
  references.
- Use bounded, isolated reviewer agents when independent judgment is valuable.
  Reviewers should not edit unless their role explicitly requires it.
- Use current primary documentation for changing tools, packages, policies,
  journal requirements, and external facts.
- Keep plans and session state on disk so work survives compaction and handoff.
- Do not commit, push, deploy, submit, email, publish, sync to Overleaf, or
  share externally without explicit authorization for that action.

## Completion evidence

Finish every non-trivial task with:

- files changed and the controlling source of truth;
- checks executed and their actual results;
- rendered/visual checks where applicable;
- claims or artifacts still UNVERIFIED;
- known limitations and the safest next action.
