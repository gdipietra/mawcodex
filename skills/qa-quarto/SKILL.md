---
name: qa-quarto
description: "Run adversarial parity QA between a rendered Quarto HTML deck and its Beamer PDF reference using independent critic and bounded fixer roles, repeated rendering, and hard content, notation, overflow, and visual checks. Use for requests such as \"QA the Quarto\", \"check parity\", \"does the HTML match the PDF?\", \"Quarto matches Beamer?\", or after $translate-to-quarto. Requires source and current renders; missing render capability is reported UNVERIFIED."
---

# QA Quarto

Treat the Beamer deck as the declared reference baseline while allowing
documented, intentional improvements in Quarto. Preserve content and meaning;
do not require pixel identity across formats.

## Hard gates

| Gate | Requirement |
|---|---|
| Content | No unexplained missing or added slide, equation, text, citation, or reveal state |
| Notation | Mathematical symbols, subscripts, signs, and definitions preserve meaning |
| Overflow | No clipped, hidden, or unreachable content at target viewport sizes |
| Figures | Every plot, table, image, and diagram is present, legible, and correctly labeled |
| Navigation | Slide order, fragments, links, notes, and incremental reveals behave as intended |
| Layout | Alignment, centering, and visual hierarchy are stable and instructionally usable |
| Provenance | Every intentional divergence from Beamer is recorded |

`APPROVED` requires every hard gate to pass. A missing renderer, browser, PDF
page image, font, or dependency makes the affected gate `UNVERIFIED`.

## 0. Pre-flight

1. Resolve the controlling Beamer `.tex` and PDF and the Quarto `.qmd` and HTML.
2. Record hashes or modification times and ensure both renders correspond to
   the current sources. Re-render stale artifacts when authorized.
3. Record render commands, versions, target viewport sizes, and any expected
   intentional differences.
4. Inventory slide/frame mapping, equations, figures, and generated TikZ/SVG
   assets.
5. Preserve the Beamer source and render unchanged. Before fixing, preserve a
   comparison version or diff of the Quarto source.

If either source or render is missing and cannot be generated, report the
affected checks `UNVERIFIED` and stop before the critic/fixer loop.

## 1. Independent critic

Prefer the project `quarto-critic` custom agent. Otherwise spawn a bounded,
read-only subagent in an isolated context using
[`quarto-critic.md`](../../references/agent-roles/quarto-critic.md). Give it:

- both sources and renders;
- the slide/frame map;
- hard gates and target viewports;
- documented intentional differences.

Do not give it the fixer's conclusions. Require typed findings with severity,
gate, location in each version, evidence, and acceptance test. Save round one
to `quality_reports/<lecture>_qa_critic_round1.md`.

## 2. Bounded fixer

If findings remain, prefer the project `quarto-fixer` custom agent. Otherwise
spawn a workspace-write subagent using
[`quarto-fixer.md`](../../references/agent-roles/quarto-fixer.md).

Limit its write scope to the Quarto source and explicitly named Quarto-owned
style or asset files. It must:

1. address critical, then major, then minor findings;
2. preserve content and notation;
3. avoid editing Beamer or unrelated shared assets;
4. explain each change and its acceptance test;
5. re-render Quarto and inspect the result;
6. return a diff plus unresolved findings.

## 3. Re-audit

Launch a fresh critic context on the new artifacts. Deduplicate findings by
stable location plus finding. Continue until:

- a round adds zero new critical or major findings; and
- all existing critical and major findings are resolved; and
- every hard gate is `PASS`.

Follow
[`orchestrator-protocol.md`](../../references/rules/orchestrator-protocol.md)
and
[`summary-parity.md`](../../references/rules/summary-parity.md). If the same
gate fails in rounds N and N+2, stop patching that issue and escalate it with
evidence. Cap the workflow at five rounds.

## Final report

Write `quality_reports/<lecture>_qa_final.md` with:

- source and render identities;
- environment and viewport matrix;
- hard-gate status;
- round-by-round findings and fixes;
- intentional divergence register;
- unresolved or unverified checks;
- final verdict: `APPROVED`, `NEEDS REVISION`, or `UNVERIFIED`.

Report changed files and retain the comparison diff. Do not commit, publish,
deploy, or replace a hosted deck without explicit user authorization.
