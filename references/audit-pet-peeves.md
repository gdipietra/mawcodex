<!-- Native rewrite of .claude/references/audit-pet-peeves.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 9d3c9c059a008d184a4ae91e684c6c4fe47e254ef515d74bb9365fa2a301ee83. -->

# Codex migration and audit pet peeves

Use this catalogue during `$deep-audit` and package review.

1. **Declared behavior without an available capability.** A skill must identify missing connectors, compilers, or runtimes as UNVERIFIED.
2. **Body/frontmatter trigger drift.** The description must state the real workflow and concrete trigger situations.
3. **Flags documented in one surface only.** Every advertised flag must be handled consistently in the body and linked rules.
4. **Broken relative references.** Resolve links from the file that contains them, especially `../../skills/` from rule and role files.
5. **Provider syntax surviving as behavior.** Operational slash commands, Claude paths, tool allowlists, and retired model aliases are release blockers; provenance mentions are allowed.
6. **Reviewers that can edit.** Review roles default to read-only. Workspace-write requires an explicit implementation or verification need.
7. **Same-context self-verification.** Claim and adversarial checks need isolated inputs or a fresh subagent.
8. **Skipped checks reported as clean.** Missing sources, renderers, or web access produce UNVERIFIED, never PASS.
9. **Hooks presented as complete enforcement.** Tool hooks have coverage gaps and are defense-in-depth only.
10. **Transcript parsing treated as stable.** Codex transcript format is not a stable hook interface.
11. **External actions hidden inside workflow verbs.** Commit, push, deploy, send, submit, share, and delete need explicit authorization.
12. **Source and adaptation mixed.** Upstream remains read-only and every target retains a source hash.
13. **Counts updated without enumeration.** Verify all 52 source-derived skills, any native additions, 18 source-derived agents, any native agents, 32 rules, shared references, and hook mappings by path.
14. **False-precision quality scores.** A numeric score is advisory; hard correctness, provenance, and disclosure failures remain blocking regardless of score.
15. **Documentation claims ahead of tests.** Stable status follows validators and representative forward tests, not the other way around.
