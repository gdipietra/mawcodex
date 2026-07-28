---
name: scaffold-exercises
description: "Scaffold a graded problem set with analytical, empirical, and coding problems, a clean student version, and a separate worked-solution key. Use to create practice or homework materials from a topic, lecture, paper, or dataset; not to grade submissions or run an exam."
---

# Problem Set Scaffolder

Create a student problem set and a separately controlled solution key. Preserve
the notation and learning objectives of the supplied teaching material.

## Safety and verification

- Never place answers or revealing hints in the student file.
- Never invent variables in a supplied dataset. Inspect its schema first.
- Use fixed, recorded seeds for simulated data.
- Execute coding solutions when the relevant runtime is available. Otherwise
  label them `DRAFTED — NOT RUN` and the affected answer `UNVERIFIED`.
- Do not install tools, publish materials, deploy, or share them without
  explicit authorization.

## Inputs

Resolve from the user's request:

- topic or source material;
- difficulty: `intro`, `core`, or `advanced` (default `core`);
- total count (default 6);
- requested subset of `analytical`, `empirical`, and `coding`;
- optional dataset path; and
- whether to omit solutions.

Read any lecture, paper, or dataset metadata supplied. If the topic is too vague
to define observable learning objectives, ask one focused question and stop.

## Phase 0: Pre-flight

Before generation, report:

```markdown
## Pre-Flight Report — Problem Set
**Topic:** [...]
**Sources read:** [...]
**Difficulty:** [...]
**Counts:** analytical=N, empirical=N, coding=N
**Dataset:** [path | seeded simulation | none]
**Learning objectives:** [...]
```

Resolve all choices here rather than interrupting later generation.

## Phase 1: Problems

For every problem include a number, section, motivation sentence, prompt, and
all required notation/data. Apply these rules:

- reuse source notation and define any new symbol;
- intro problems test one concept, core problems chain two or three steps, and
  advanced problems require an identification argument or non-obvious insight;
- state assumptions locally so every problem is self-contained;
- for empirical work without supplied data, specify a transparent DGP and
  generate data with seed `YYYYMMDD`;
- do not fabricate empirical results.

## Phase 2: Solutions

For each problem provide:

1. a complete derivation, expected estimate and interpretation, or runnable
   reference code; and
2. a one- or two-sentence “why this matters” explanation.

Coding output must be captured from an actual run before it is called verified.
If execution fails, retain the code, error evidence, and `DRAFTED — NOT RUN`
status.

## Phase 3: Separation check and output

Write:

- `exercises/<topic-slug>_problems.md`; and
- `exercises/<topic-slug>_solutions.md`, unless solutions were omitted.

The student file contains problems and required data only. Before completion,
scan it for solution headings, final numeric answers, answer-only code, and
explanatory text copied from the key. A detected leak is FAIL and must be
removed.

Report absolute output paths, counts by type, any simulation seed, and whether
each code solution was executed or remains unverified.

Use `$create-lecture` for the corresponding deck, `$data-analysis` for a full
empirical pipeline, and `$simulation-study` for finite-sample demonstrations.

## Provenance

Native Codex rewrite of the upstream `scaffold-exercises` skill from
`pedrohcgs/claude-code-my-workflow` at commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (MIT), preserving the
economics adaptation of the exercise-plus-explainer pattern attributed upstream
to `mattpocock/skills`.
