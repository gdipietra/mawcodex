<!-- Adapted from .claude/rules/orchestrator-research.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 4e39fccb7d71ff512fe24502e21756cbb548017836ff4bbbad31abaf00b42fda. -->

## Applicability

Load this rule for: `scripts/**/*.R`, `explorations/**`, `Figures/**/*.R`.

Routing is explicit: the active skill or project `AGENTS.md` must select this rule.

# Research Project Orchestrator (Simplified)

**For R scripts, simulations, and data analysis** -- use this simplified loop instead of the full multi-agent orchestrator.

## The Simple Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run code, check outputs
  │         R scripts: Rscript runs without error
  │         Simulations: set.seed reproducibility
  │         Plots: PDF/PNG created, correct format
  │         If verification fails → fix → re-verify
  │
  Step 3: SCORE — Apply quality-gates rubric
  │
  └── Score >= 80?
        YES → Done (commit when user signals)
        NO  → Fix blocking issues, re-verify, re-score
```

**No 5-round loops. No multi-agent reviews. Just: write, test, done.**

## Verification Checklist

- [ ] Script runs without errors
- [ ] All packages loaded at top
- [ ] No hardcoded absolute paths
- [ ] `set.seed()` once at top if stochastic
- [ ] Output files created at expected paths
- [ ] Tolerance checks pass (if applicable)
- [ ] Quality score >= 80
