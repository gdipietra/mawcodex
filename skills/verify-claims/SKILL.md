---
name: verify-claims
description: "Run Chain-of-Verification on factual claims in a draft using an independent fresh-context verifier. Classify citation, numerical, dataset, named-entity, and negative-literature claims as supported, contradicted, explained, or unverifiable. Use for fact-checking, not grammar or broad manuscript review."
---

# Chain-of-Verification

Fact-check a draft using
[`post-flight-verification.md`](../../references/rules/post-flight-verification.md)
and an independent verifier that never sees the full draft.

## Inputs and contract

Require a readable draft path or supplied text plus one or more source pointers.
Sources may be local files or current primary-source URLs. If sources cannot be
identified or accessed, stop or mark the affected claims `UNVERIFIED`; never
search until a preferred answer appears.

Prefer the project `claim-verifier`. Otherwise start a bounded isolated
subagent using
[`claim-verifier.md`](../../references/agent-roles/claim-verifier.md).
Independence is load-bearing: do not give the verifier the draft, prior verdicts,
or desired conclusion.

## Phase 1: Extract claims

Read the draft and enumerate checkable assertions:

| Type | Capture |
| --- | --- |
| Citation | cited work plus the exact attributed result |
| Numerical | value, units, sample/specification, and claimed source |
| Negative literature | the bounded universe implied by “no prior work” |
| Named entity | person, title, venue, package, estimator |
| Dataset | variable, coverage, population, timing, provenance |

Skip opinions, recommendations, and definitions introduced by the draft.
Record an `author_alternative` only when the author supplies a concrete
different edition, sample, specification, or rounding rule.

Produce a claims table with stable IDs and source hints. Keep attributed text to
the minimum needed for verification.

## Phase 2: Verification questions

Write one source-answerable question per claim. For citation claims, ask whether
the source supports the attributed direction and scope—not merely whether the
paper exists.

## Phase 3: Independent verification

Give the isolated verifier only:

- claims table;
- questions;
- source pointers;
- applicable evidence rules; and
- required structured output.

The verifier should use primary material where possible and return exact
page/section/table/equation or official-URL evidence, retrieval status, and one
verdict per claim. Inaccessible evidence must remain `cannot-verify`.

## Phase 4: Reconcile

Use these tiers:

- `HIGH-WARN`: fabricated citation or direct contradiction; blocks a PASS.
- `MED-WARN`: partial evidence or a transient retrieval failure that prevents a
  material check.
- `LOW-WARN`: genuinely inaccessible evidence for a claim that is explicitly
  non-material to the draft's argument, results, or release decision, or other
  low-consequence uncertainty. An inaccessible material source is never
  downgraded to Low.
- `EXPLAINED`: a real discrepancy accounted for by a concrete, verified
  author-supplied alternative. Fabricated citations and vague alternatives can
  never be explained away.
- `SUPPORTED`: source directly supports the claim at its stated scope.

Aggregate:

| Evidence | Outcome |
| --- | --- |
| no High/Medium; supported plus any non-material Low/Explained | PASS, with Low caveats retained |
| no High; at least one Medium | PARTIAL |
| at least one High | FAIL |
| verification capability or any material source absent | UNVERIFIED |

If the user explicitly accepts `--no-fail-closed`, retain FAIL findings and
record the exception and consequence; never relabel them PASS. Any later
release/commit gate should treat unresolved High findings as blocking unless the
user explicitly authorizes a documented override.

## Output

Write or return:

```markdown
## Post-Flight Verification — [draft]
**Claims extracted:** N · **Independently checked:** M
**Outcome:** PASS / PARTIAL / FAIL / UNVERIFIED
## Contradictions
## Partial or inaccessible evidence
## Explained discrepancies
## Supported claims
| ID | Verdict | Evidence | Location |
## Required corrections
```

Only edit the draft when the user asks for correction; preserve the report and
show the evidence for every change. A verifier timeout or no-claims result is
reported explicitly, never silently treated as PASS.

## Provenance

Native Codex rewrite of the upstream `verify-claims` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT). The verification design
preserves the Chain-of-Verification pattern from Dhuliawala et al. (2023),
arXiv:2309.11495.
