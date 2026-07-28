---
name: data-management-plan
description: "Draft a source-verified Data Management or Data Management and Sharing Plan for the user's named funder, covering data, metadata, storage, access, sharing, preservation, reproducibility, and roles. Use for NSF, NIH, ERC, Horizon Europe, or another supplied scheme. Produces a local draft and checklist; never submits it."
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

# $data-management-plan — Funder-Aligned DMP Draft

Produce a review-ready Data Management Plan and compliance checklist. This
skill writes local prose only; it does not submit anywhere. It composes the
project's restricted-data rules from
[`confidential-data.md`](../../references/rules/confidential-data.md) with
`$capture-environment` and `$replication-package`.

## When to use

- **Writing a grant proposal.** Use the currently applicable solicitation or
  award conditions; `$grant-proposal` can call this skill for the data section.
- **Before data collection on a funded project.** The plan is a commitment you make at award time and report against at renewal.
- **When restricted or human-subjects data is involved.** The access/sharing and preservation sections change materially — see Phase 2.

## When NOT to use

- For a clinical-trial data-sharing statement governed by ICMJE / ClinicalTrials.gov — use the trial sponsor's template.
- As a substitute for IRB protocol text — the DMP *references* IRB constraints; it is not the protocol itself.

## Inputs

- `--funder nsf|nih|erc|horizon|<other>` — target funder or scheme. If
  omitted, infer it only from an authoritative supplied solicitation; otherwise
  ask once.
- `--input <path>` — research specification, grant draft, solicitation, or
  project description.
- `--no-verify` — skip policy-source verification. The draft remains
  UNVERIFIED and must not be labeled compliant.

## Workflow

### Phase 0 — Detect funder + data sensitivity

1. Resolve the funder and specific solicitation or policy version. Use web
   search for current requirements and cite only the funder's official page,
   solicitation, or policy document. If current primary sources cannot be
   accessed, use the user's supplied materials and mark the schema UNVERIFIED.
2. Load the verified section schema. The following mapping is a starting
   orientation, not an authoritative current checklist:

   | Funder | Plan name | Required sections (abridged) |
   |---|---|---|
   | **NSF** | Data Management Plan (2 pp max) | data types · standards · access/sharing · re-use/redistribution · archiving |
   | **NIH** | Data Management and Sharing Plan | data type · tools/software · standards · preservation/access/timelines · access/distribution + reuse · oversight |
   | **ERC** | DMP (Horizon Europe Annex) | FAIR per dataset · data summary · making data FAIR · resource allocation · security · ethics |
   | **Horizon Europe** | DMP (DMP template) | same FAIR-first structure as ERC; open by default, "as open as possible, as closed as necessary" |

3. Classify the data on three axes (drives Phases 2–3):
   - **Public** (open survey, scraped public records, simulated) — minimal restrictions.
   - **Restricted** (admin/tax/Census, proprietary, licensed under DUA) — access procedures dominate.
   - **Human-subjects** (PII, biospecimen-linked, survey with identifiers) — IRB + disclosure avoidance dominate.

   If the data is restricted *or* human-subjects, set `sensitive = true` and run Phase 2. If it is purely public, Phase 2 is a short paragraph.

### Phase 1 — Scaffold sections from the funder profile

Generate the six house sections, mapped onto the funder's required headings:

1. **Data description & types** — what data, source, volume, formats produced. Be specific: panel/admin microdata, RCT outcomes, event-study event files, replication intermediate `.rds`/`.dta`/`.parquet`.
2. **Formats & metadata standards** — open/non-proprietary formats where possible (`.csv`/`.parquet` over `.dta`; codebooks; DDI / Dublin Core / domain schema). Name the standard, don't say "appropriate metadata".
3. **Storage & backup** — during the project: encrypted institutional storage, 3-2-1 backup, version control for code (not raw restricted data in git).
4. **Access & sharing** — who can access, when, under what terms. For restricted data this is the **restricted-data access procedure** (see Phase 2).
5. **Preservation & archiving** — a named repository with a persistent identifier (see Phase 3).
6. **Roles & responsibilities** — PI as data steward, data manager, institutional support, succession plan.

For any required field the input does not supply, write
`[CLARIFY: <specific question>]` rather than fabricating, following
`$preregister`.

### Phase 2 — Fold in disclosure-avoidance + IRB constraints (only if `sensitive = true`)

Pull the relevant rules from
[`confidential-data.md`](../../references/rules/confidential-data.md) and
weave them into the access, sharing, and preservation sections:

- **Restricted data → describe the access path, not the data.** State the data provider, the DUA/restricted-use agreement, and how a replicator obtains access (e.g., FSRDC application, openICPSR restricted-access tier, provider application). The data itself is *not* deposited; the *path to it* is.
- **Human-subjects → IRB + minimization.** Reference the IRB protocol number (or `[CLARIFY:]`), the consent terms governing sharing, and the de-identification plan. Shared outputs are de-identified per the consent.
- **Disclosure avoidance for any released microdata or tables.** Describe only
  techniques and thresholds actually authorized by the signed agreement or IRB
  record. Never invent a minimum cell count. Defer the pre-release scan to
  `$disclosure-check` and retain official provider review as the release gate.

### Phase 3 — Fold in the computational-environment + replication-package plan

The DMP should commit to *reproducibility*, not just data deposit:

- **Environment capture.** State the actual planned artifacts and point to
  `$capture-environment`.
- **Replication package.** Describe what can lawfully be deposited and point to
  `$replication-package`. Do not promise release of restricted inputs.
- **Repository choice** — match the data class:
  - Economics / social science → **openICPSR** (AEA's home; DCAS-compliant) or **Harvard Dataverse**.
  - Restricted data → openICPSR *restricted-access* tier or the provider's enclave (FSRDC); deposit code + metadata, not the microdata.
  - Domain repos → field-specific (e.g., ICPSR proper, GenBank, Zenodo for code) where the funder or community expects them.
- State the persistent identifier and timeline only from the verified
  solicitation/policy or user-confirmed project plan. Use `[CLARIFY:]` for
  unknowns.

### Phase 4 — Post-flight (skip with `--no-verify`)

If the draft cites a funder policy or standard by name or number, use the
project `claim-verifier` custom agent, or a bounded isolated subagent following
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md), to check
each claim against the retrieved primary source. Give the reviewer claims and
sources, not the draft's expected verdict. Surface PASS, PARTIAL, FAIL, and
UNVERIFIED.

### Phase 5 — Output

Write the draft to `quality_reports/dmp/YYYY-MM-DD_<funder>_<slug>.md` and a funder checklist alongside it.

```
✓ DMP draft saved: quality_reports/dmp/<file>.md
  Funder: <nsf|nih|erc|horizon>   Data class: <public|restricted|human-subjects>
  Sections: <count> total — <complete> complete, <clarify> with [CLARIFY:] placeholders
  Disclosure/IRB folded in: <yes (Phase 2) | n/a — public data>
  Repository: <openICPSR | Dataverse | domain repo>   PID: <DOI planned | [CLARIFY:]>
  Policy citations verified: <PASS>/<PARTIAL>/<FAIL>  (or "none to verify")
  Next: resolve [CLARIFY:] items, then paste into <DMPTool | NIH ASSIST | Horizon portal>
```

The **funder checklist** is a table: each required section → present? → complete / `[CLARIFY:]`, so the user sees at a glance whether the plan will pass the funder's compliance check.

## Exit behavior

- **All required sections present, zero `[CLARIFY:]`** → "DMP READY", checklist all green.
- **Any required section unresolved** → "INCOMPLETE — N MUST items unresolved", listed in the checklist. The draft is still written (so the user can fill it in), but not marked ready.
- This skill **does not block** anything — it produces a document. The gate is the funder's, not ours.

## Cross-references

- [`confidential-data.md`](../../references/rules/confidential-data.md) —
  restricted-data, IRB, and disclosure rules.
- [`$disclosure-check`](../disclosure-check/SKILL.md) — pre-release screen.
- [`$capture-environment`](../capture-environment/SKILL.md) — environment
  capture.
- [`$replication-package`](../replication-package/SKILL.md) — deposit builder.
- [`$grant-proposal`](../grant-proposal/SKILL.md) — proposal integration.
- [`$preregister`](../preregister/SKILL.md) — sibling document generator.
- [`replication-protocol.md`](../../references/rules/replication-protocol.md)
  — reproducibility contract.

## What this skill does NOT do

- **Submit the plan.** It writes a Markdown draft; the user pastes it into DMPTool / NIH ASSIST / the Horizon portal.
- **Run the disclosure scan or build the package.** It references
  `$disclosure-check`, `$capture-environment`, and `$replication-package`; it
  does not execute them.
- **Write the IRB protocol.** It references the protocol number and consent terms; the protocol is authored separately.
- **Choose a repository for you when the funder mandates one.** If NIH names a domain repository for your data type, that mandate wins over the defaults in Phase 3 — the skill flags it as `[CLARIFY:]` rather than guessing.
