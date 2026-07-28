---
name: syllabus
description: "Build or restructure a course syllabus from supplied topics or readings, including prerequisites, a dependency-ordered weekly schedule, measurable objectives, aligned assessment, one rubric, editable policy language, and a week-to-lecture work list. Use for course planning, not slide creation or reading discovery."
---

# Build a Course Syllabus

Turn instructor-supplied material into a teachable, auditable course plan. The
instructor retains responsibility for content choices and institutional policy.

## Phase 0: Intake

Resolve before drafting:

1. level and audience (`phd`, `grad`, or `undergrad`, plus sequence/field);
2. teaching weeks and sessions per week; and
3. topic/reading material, supplied directly or by path.

Inventory supplied bibliographies and documents. Do not invent readings or treat
file names as evidence about a paper's content. If material is absent, request a
topic/reading list and stop.

Echo an intake report with level, cadence, topic/reading counts, source paths,
and gaps. Obtain instructor confirmation before sequencing.

## Phase 1: Sequence

1. Build a prerequisite graph and order concepts by dependency rather than
   source-list order.
2. Allocate readings at a realistic level-specific load and flag overloaded or
   thin weeks.
3. Place problem sets, exams, reports, replications, and projects only after
   their prerequisites; surface deadline collisions.
4. Mark breaks and no-class dates from supplied institutional information.
5. Present the week/topic/readings/deliverable table for sign-off before
   continuing.

## Phase 2: Objectives and assessment

- Write course and unit objectives with observable verbs such as derive,
  estimate, replicate, critique, or prove.
- Map every objective to teaching weeks and at least one assessment.
- Choose level-appropriate assessment instruments and verify weights total
  exactly 100%.
- Draft one concise criteria-by-performance-level rubric for the highest-stakes
  deliverable.

Flag any unassessed objective or assessment that lacks a stated objective.

## Phase 3: Output

Write `syllabus.md` or the user-specified path:

```markdown
# [Course title] — [Term, Year]
[level · meeting cadence · units]

## Course description
## Prerequisites
## Learning objectives
## Weekly schedule
| Week | Topic | Readings | Deliverable |

## Assessment
| Component | Weight | Objectives |

### Rubric — [highest-stakes deliverable]
| Criterion | Excellent | Adequate | Weak |

## Policies
[late work · AI use · academic integrity · accessibility · attendance]

## Week → lecture work list
| Week | Deck name | Objectives | Anchor reading |
```

Omit policies when requested. Otherwise label policy language as editable
boilerplate requiring reconciliation with current institutional rules,
collective agreements, accessibility requirements, and local law. Verify
current external policy from official sources when the user asks for
institution-specific wording.

The lecture work list is an input to `$create-lecture`, not a generated deck.
Use `$lit-review` to build or vet a reading list and `$pedagogy-review` after
decks exist.

## Completion gate

Return the syllabus path and a gap summary covering weeks without readings,
unassessed objectives, deadline collisions, unsourced readings, and topics
dropped for time. If none exist, say so explicitly. Do not publish the syllabus,
create course sites, or send it without explicit authorization.

## Provenance

Native Codex rewrite of the upstream `syllabus` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT).
