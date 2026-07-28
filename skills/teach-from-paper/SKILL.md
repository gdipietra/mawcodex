---
name: teach-from-paper
description: "Turn one research paper into a level-calibrated teaching package: lecture outline, three to five teachable results with intuition and failure modes, slide skeleton, discussion questions, and an exercise brief. Use to plan teaching from a paper; not to review validity or create the finished deck."
---

# Teach From Paper

Extract the teachable core of one paper without pretending that a summary proves
the paper correct.

## Inputs and contract

Require one paper path plus an audience level (`undergrad`, `phd`, or `seminar`)
and time budget. Accept readable text formats directly; use a trusted extractor
for PDF. If extraction fails, request an accessible text version and mark the
package `UNVERIFIED`.

Read the full paper, including methods, results, limitations, notes, and
appendices relevant to the selected results. Do not infer the paper from its
abstract. Keep quotations short and attribute them.

## Phase 0: Pre-flight

After reading, report:

```markdown
## Pre-Flight Report
**Paper:** [title, authors, year]
**Source:** [path and pages/sections read]
**One-line thesis:** [...]
**Audience:** undergrad | phd | seminar
**Time budget:** N minutes; target approximately N/2 slides
**Prerequisites:** [...]
**Running example:** [...]
**Unverified sections:** [none/list]
```

Obtain confirmation of audience and thesis before producing the package.
Undergraduate treatment prioritizes intuition; PhD treatment preserves
identifying assumptions and a key derivation; seminar treatment foregrounds
contribution and evidence.

## Phase 1: Teachable core

Select three to five results worth remembering. For each record:

- a level-appropriate formal statement;
- one-breath intuition;
- evidence and location in the paper;
- the assumption or method that supports it; and
- a concrete failure mode or limitation.

Map notation into a consistent teaching notation and flag every remapping.
Distinguish method from substantive takeaway. Unsupported interpretation is
`UNVERIFIED`, not a teaching fact.

## Phase 2: Outline and slide skeleton

Build a motivation → setup → key result → method → takeaways arc. Target roughly
two minutes per slide, with motivation before formalism, a worked example near
each new definition, and transition slides at act breaks.

Each skeleton row contains only a title, one-line content note, evidence/source
pointer, and figure/diagram placeholder. It is ready for `$create-lecture` but
is not a finished deck.

## Phase 3: Questions and exercises

- Write four to six questions progressing from comprehension through
  application to critique.
- Unless omitted, sketch two to four exercises with prompt, skill practiced,
  expected answer shape, and source result. Do not include full solutions.
  `$scaffold-exercises` converts this brief into a separate student set and key.

## Output

Write `quality_reports/teach_from_paper_<title-slug>.md`:

```markdown
# Teaching Package: [Paper]
**Audience:** [...] · **Budget:** [...] · **Date:** [...]
## 1. Lecture outline
## 2. Results worth presenting
## 3. Slide skeleton
| # | Title | Content note | Evidence | Figure/diagram |
## 4. Discussion questions
## 5. Exercise brief
## 6. Unverified or omitted material
```

Report the output path and explicit handoffs to `$create-lecture` and
`$scaffold-exercises`. Use `$review-paper` separately if validity is in doubt
and `$lit-review` for multi-paper field coverage. Do not publish or share
teaching materials without explicit authorization.

## Provenance

Native Codex rewrite of the upstream `teach-from-paper` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
