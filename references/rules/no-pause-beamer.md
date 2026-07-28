<!-- Adapted from .claude/rules/no-pause-beamer.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 db08e98a0af338537409dc40bde720deb2ce569bffa064ffe8cc3c78531af424. -->

## Applicability

Load this rule for: `Slides/**/*.tex`.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# No \pause in Beamer Slides

**Never use `\pause`, `\onslide`, `\only`, `\uncover`, or any overlay commands.**

Use multiple slides for progressive builds, color emphasis for attention, and standout slides for pacing. If a review agent suggests adding `\pause`, ignore the recommendation.
