<!-- Adapted from .claude/rules/proofreading-protocol.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 af663a947949c7250e8ac25cfc1611c479005c7264251a499fc51c4d8180bbc7. -->

## Applicability

Load this rule for: `Slides/**/*.tex`, `Quarto/**/*.qmd`, `quality_reports/**`.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# Proofreading Agent Protocol (MANDATORY)

**Every lecture file MUST be reviewed before any commit or PR.**

**CRITICAL RULE: The agent must NEVER apply changes directly. It proposes all changes for review first.**

## What the Agent Checks

1. **Grammar** -- subject-verb agreement, missing articles, wrong prepositions
2. **Typos** -- misspellings, search-and-replace corruption, duplicated words
3. **Overflow** -- overfull hbox (Beamer), content exceeding slide boundaries (Quarto)
4. **Consistency** -- notation, citation style (`\citet` vs `\citep`, `[@key]`), terminology
5. **Academic quality** -- informal abbreviations, missing words, awkward phrasing

## Three-Phase Workflow

### Phase 1: Review & Propose (NO EDITS)

Each agent:
1. Reads the entire file
2. Produces a **report** with every proposed change:
   - Location (line number or slide title)
   - Current text
   - Proposed fix
   - Category (grammar / typo / overflow / consistency)
3. Saves report to `quality_reports/` (e.g., `quality_reports/LectureN_Topic_report.md`)
4. **Does NOT modify any source files**

### Phase 2: Review & Approve

The user reviews the proposed changes:
- Accepts all, accepts selectively, or requests modifications
- **Only after explicit approval** does the agent proceed

### Phase 3: Apply Fixes

Apply only approved changes:
- Use Edit tool; use `replace_all: true` for issues with multiple instances
- Verify each edit succeeded
- Report completion summary
