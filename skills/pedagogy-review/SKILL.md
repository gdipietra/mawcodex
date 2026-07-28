---
name: pedagogy-review
description: "Perform a read-only pedagogical review of a lecture deck in `.qmd` or `.tex`, covering narrative arc, prerequisite assumptions, worked examples, notation, cognitive load, pacing, and student perspective. Use for requests such as \"pedagogy review\", \"does this teach well?\", \"is the flow right?\", \"will students follow?\", \"review the narrative\", or a pre-teaching deck review. Produces a report without editing the deck."
---

# Pedagogy Review

Review whether a lecture teaches its intended ideas, not merely whether it
looks polished.

## Workflow

1. Resolve the user-supplied deck. If only a name is given, search `Quarto/`
   and `Slides/`. If several files match, ask which is controlling.
2. Read the full source and any stated learning objectives or syllabus context.
   If a render exists, inspect it for pacing-relevant evidence; a missing
   renderer or stale render is `UNVERIFIED`, not a visual pass.
3. Prefer the project `pedagogy-reviewer` custom agent. Otherwise spawn a
   bounded, read-only subagent in an isolated context using
   [`pedagogy-reviewer.md`](../../references/agent-roles/pedagogy-reviewer.md).
   Give it the complete deck, learning objectives, audience, session length,
   and only the prerequisite context the user supplied.
4. Require the reviewer to assess all thirteen patterns defined by the role,
   plus deck-level:
   - narrative arc and motivation;
   - prerequisite assumptions and notation introduction;
   - concept-to-example sequencing;
   - worked-example completeness;
   - opportunities for retrieval, practice, or prediction;
   - cognitive load and pacing;
   - transitions and recap;
   - likely student objections or misconceptions.
5. Deduplicate findings and map each to a slide title, frame, or source line.
   Separate observed evidence from inferred student difficulty.
6. Save
   `quality_reports/<filename-without-extension>_pedagogy_report.md` with:
   - scope and audience assumptions;
   - pattern-by-pattern status: `PASS`, `PARTIAL`, `FAIL`, or `UNVERIFIED`;
   - deck-level assessment;
   - prioritized findings with location, evidence, consequence, and suggested
     teaching change;
   - top three to five recommendations;
   - unresolved questions.
7. Summarize counts and the highest-priority recommendations in conversation.

## Boundaries

- The deck remains unchanged. The report may recommend edits but must not
  apply them.
- Use $visual-audit for layout and clipping, and $slide-excellence for a
  combined review.
- Do not infer student preparation, accessibility needs, or course constraints
  that were not supplied; label those assumptions.
- Do not commit, publish, or distribute the report without explicit user
  authorization.
