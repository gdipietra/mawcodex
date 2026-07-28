<!-- Adapted from .claude/rules/exploration-fast-track.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 9bba57672571e9b773735c2763ab4b91abe679fdf5874a99ab36ee790f21bc53. -->

## Applicability

Load this rule for: `explorations/**`.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# Exploration Fast-Track

**Lightweight workflow for experimental work.** Quality threshold: 60/100 (vs 80 for production). No planning needed.

## Steps

1. **Research value check** -- Does this improve the project? If NO, don't build it.
2. **Create folder** -- `mkdir -p explorations/[name]/{R,scripts,output}` + README + SESSION_LOG.md
3. **Code immediately** -- no plan needed. Must-haves: code runs, results correct, goal documented. Not needed: Roxygen docs, full tests, perfect style.
4. **Log progress** -- append 2-3 lines to SESSION_LOG.md as you work
5. **Decision point** -- keep exploring, graduate to production (upgrade to 80/100), or archive with brief explanation

## When to Stop (Kill Switch)

At any point: stop, archive with note ("Attempted X, hit blocker Y"), move on. No guilt -- exploration is inherently uncertain.
