<!-- Adapted from .claude/rules/prompt-shaping.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 899dafe5a71ae20c31d2a12c37a73757770881b18c8508560b74333ddd5e68a2. -->

## Applicability

Load this rule for: All academic tasks when relevant.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# Prompt Shaping (a standing habit, not a skill)

**When a request arrives informal, dictated, or ambiguous, shape it before
you act on it—silently, every time.** The upstream workflow once exposed
prompt formatting as explicit commands. MAW Codex treats it as a standing
habit: every fuzzy ask should resolve into a clear goal and observable gates.

## The shape

Before executing a non-trivial informal request, resolve these five things (the sixth, the bookend, is for the *output*):

1. **Role** — whose expertise answers this? (econometrician, referee, instructor, data engineer)
2. **Task** — the single concrete deliverable, stated as a verb + object.
3. **Context** — which files, datasets, prior decisions, and constraints bear on it.
4. **Constraints** — what must hold (journal style, tolerance, reproducibility, no hardcoded paths).
5. **Output format** — exactly what to return (a report? a diff? a table? a plan?).
6. **Bookend** — restate the goal at the end and confirm it was met.

Full elaboration and examples: [`references/prompt-formatting-core.md`](../prompt-formatting-core.md).

## How to apply it

- **Mostly silent.** Resolve the shape and proceed; do not narrate a six-section preamble back to the user. The point is a better answer, not a visible form.
- **Surface only the genuine ambiguity.** If a *decision* is the user's to
  make (which journal? which estimator? overwrite or append?), ask it briefly
  through the active Codex input surface instead of guessing. Everything else,
  infer and state your assumption in one line.
- **For multi-turn project specification** (a fuzzy research idea → a full spec), that is still a real skill: use [`$interview-me`](../../skills/interview-me/SKILL.md). Prompt-shaping is the single-shot habit; `$interview-me` is the conversation.

## Why this is a rule rather than a separate skill

Earlier source commands reformatted an informal ask into a six-section
prompt. In a goal-first, verification-gated workflow the lever is the *goal and
the gates*, not command ceremony. Shaping is ambient, and the reusable-artifact
case is served by saving a spec through `$interview-me` or a plan in
`quality_reports/plans/`.

## Cross-references

- [`references/prompt-formatting-core.md`](../prompt-formatting-core.md) — the six-section elaboration.
- [`skills/interview-me/SKILL.md`](../../skills/interview-me/SKILL.md) — multi-turn specification (the surviving, heavier sibling).
- [`references/rules/plan-first-workflow.md`](plan-first-workflow.md) — for non-trivial tasks, shaping feeds the plan.
