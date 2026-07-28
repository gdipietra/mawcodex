---
name: devils-advocate
description: "Read-only adversarial review of a slide deck's ordering, prerequisites, cognitive load, notation, motivation, and alternatives. Produces 5–7 evidence-backed questions with affected slides and suggested resolutions. Use for \"devil's advocate\", \"poke holes in this deck\", or a lighter review than pedagogy-review."
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

# Devil's Advocate Review

Critically examine a slide deck and challenge its design with 5-7 specific pedagogical questions.

**Philosophy:** "We arrive at the best possible presentation through active dialogue."

---

## Setup

1. **Read the target file** (the lecture being challenged)
2. **Read the applicable knowledge base and rules** under
   `references/rules/`, especially notation and narrative-arc conventions
3. If applicable, **read adjacent lectures** for narrative continuity
4. If a current PDF or HTML render exists, inspect representative pages. If
   layout evidence is unavailable, mark visual observations UNVERIFIED and
   review source structure only.

---

## Challenge Categories

Generate 5-7 challenges from these categories:

### 1. Ordering Challenges
> "Could students understand this better if we showed X before Y?"

### 2. Prerequisite Challenges
> "Do students have the background for this notation at this point?"

### 3. Gap Challenges
> "Should we include an intuitive example before this formal proof?"

### 4. Alternative Presentation Challenges
> "Here are 2 other ways to visualize/present this concept."

### 5. Notation Conflict Challenges
> "This symbol conflicts with earlier lecture usage."

### 6. Cognitive Load Challenges
> "This slide has too many new symbols. Can we split?"

### 7. Book Vision Challenges
> "If this becomes a book chapter, does this section stand alone?"

---

## Output Format

```markdown
# Devil's Advocate: [Lecture Title]

## Challenges

### Challenge 1: [Category] — [Short title]
**Question:** [The specific pedagogical question]
**Why it matters:** [What could go wrong]
**Suggested resolution:** [Specific action]
**Slides affected:** [Numbers or titles]
**Severity:** [High / Medium / Low]

[Repeat for 5-7 challenges]

## Summary Verdict
**Strengths:** [2-3 things done well]
**Critical changes:** [0-2 changes before teaching]
**Suggested improvements:** [2-3 nice-to-have changes]
```

---

## Principles

- **Be specific:** Reference exact slides and notation
- **Be constructive:** Every challenge has a suggested resolution
- **Be honest:** If the deck is good, say so
- **Prioritize:** Notation conflicts > missed metaphors
- **Think like a student:** Where do they get lost?
- **Remain read-only:** do not edit the deck, knowledge base, or render.
