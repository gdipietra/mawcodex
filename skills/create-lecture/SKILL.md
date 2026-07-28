---
name: create-lecture
description: "Create a new Beamer lecture `.tex` from supplied papers and materials, with notation consistency, source verification, iterative instructor approval, and the project's preamble. Use for a new lecture or full deck scaffold; use compile-latex for an existing deck."
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

# Lecture Creation Workflow

Create a beautiful, pedagogically excellent Beamer lecture deck.

**This is a collaborative, iterative process. The instructor drives the vision; Codex is a thinking partner.**

---

## CONSTRAINTS (Non-Negotiable)

1. **Read the knowledge base FIRST** — notation registry, narrative arc, applications database
2. Every new symbol MUST be checked against the notation registry
3. Motivation before formalism — no exceptions
4. Worked example within 2 slides of every definition
5. Max 2 colored boxes per slide
6. No `\pause` or overlay commands (check project rules)
7. Transition slides at major conceptual pivots
8. Thread at least 1 running empirical application throughout
9. All citations verified against the bibliography
10. **Work in batches of 5-10 slides** — share for feedback, don't bulk-dump

---

## WORKFLOW

### Phase 0: Intake & Context (Pre-Flight Report required)

Read the inputs, then produce a Pre-Flight Report in your response before Phase 1 starts.

Inputs to read:
- [`knowledge-base-template.md`](../../references/rules/knowledge-base-template.md)
  — notation registry, narrative arc, and applications
- [`content-invariants.md`](../../references/rules/content-invariants.md) —
  slide-content invariants
- Any source papers / existing slides the user provided
- The previous lecture's `.tex` (last section + ending slide) if one exists

Required Pre-Flight Report block:

```markdown
## Pre-Flight Report

**Sources read:**
- [source 1]: [one-line takeaway — what notation, what result, what diagram]
- [source 2]: ...

**Notation registry check:**
- New symbols this lecture will introduce: [list]
- Symbols reused from prior lectures: [list, with the lecture each was introduced in]
- Conflicts detected: [none / specific clashes]

**Narrative position:** [Where does this lecture sit in the course arc? What did the previous lecture end on? What does the next lecture need you to set up?]

**Pedagogical goal:** [one sentence]

**Running application:** [which real-world example threads through this deck]
```

State the pedagogical goal, get user confirmation, then proceed.

**First-lecture fallback (fresh fork, empty knowledge base).** If `references/rules/knowledge-base-template.md` still has unfilled placeholder tables (no notation registry entries, no applications, no prior lectures in `Slides/`), do NOT halt waiting for it. Instead:

1. Acknowledge the template is empty and we're creating the course's first lecture.
2. Propose a **minimal starter knowledge base** from the user's topic: 5-8 key symbols with conventions, 1-2 running applications, a short narrative arc (intro → main idea → implications). Present for approval.
3. Write the approved stub into the knowledge base template so subsequent lectures inherit it.
4. Continue to Phase 1.

This prevents `$create-lecture` from deadlocking in a fresh project.

### Phase 1: Paper Analysis (When Papers Provided)
- Read each supplied source directly; for PDFs use a PDF-capable workflow and
  inspect pages when equations, figures, or layout matter
- Verify bibliographic facts and substantive claims against the supplied paper
  or another primary source; missing access is UNVERIFIED
- Map paper notation → course notation
- Identify slide-worthy content
- Present summary for approval

### Phase 2: Structure Proposal
- Propose outline (5-Act or 3-Part template)
- List TikZ diagrams and R figures needed
- List new notation to introduce
- **GATE: User approves before Phase 3**

### Phase 3: Draft Slides (Iterative)
- Work in batches of 5-10 slides
- Check notation, apply creation patterns
- Quality checks during drafting

### Phase 4: Figures & Code
- R scripts following conventions
- TikZ diagrams in Beamer source (single source of truth)
- Save RDS for future Quarto integration

### Phase 5: Polish & Compile
- Run `$compile-latex` and visually inspect representative pages
- Run `$devils-advocate`
- Use the project `domain-reviewer` custom agent, or a bounded isolated
  subagent following
  [`domain-reviewer.md`](../../references/agent-roles/domain-reviewer.md)
- Update knowledge base with new notation

---

## Post-Creation Checklist

```
[ ] Lecture compiles without errors
[ ] No overfull hbox > 10pt
[ ] All citations resolve
[ ] Every definition has motivation + worked example
[ ] Max 2 colored boxes per slide
[ ] 2-3 Socratic questions embedded
[ ] Transition slides between sections
[ ] At least 1 running application threaded throughout
[ ] New notation added to knowledge base
[ ] Session log updated
[ ] Devil's Advocate run
```

## Cross-references

- [`$translate-to-quarto`](../translate-to-quarto/SKILL.md) — create the Quarto
  mirror.
- [`$qa-quarto`](../qa-quarto/SKILL.md) — adversarial Beamer↔Quarto parity.
- [`$deploy`](../deploy/SKILL.md) — publish only with explicit authorization.
- [`$scaffold-exercises`](../scaffold-exercises/SKILL.md) — accompanying
  exercises and solutions.
