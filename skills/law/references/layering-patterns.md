# Academic instruction layering patterns

Use the fewest layers that express real scope differences.

## Shared root

Keep project-wide invariants in the root `AGENTS.md`:

- mission and source authority;
- raw-data or protected-material boundaries;
- research ethics and reproducibility;
- repository map;
- standard verification;
- commit, sync, publication, submission, and sending gates.

## LaTeX teaching tree

Possible nested layers:

```text
AGENTS.md
courses/<course>/AGENTS.md
courses/<course>/exams/AGENTS.md
```

The course layer may define engine, bibliography, notation, PT-BR language,
and representative compile checks. The exams layer may add confidentiality and
solution-key restrictions. Do not repeat root safeguards.

If several courses share identical rules, keep those rules at their nearest
common parent instead of creating duplicate files.

## Stata/R research tree

Possible nested layers:

```text
AGENTS.md
code/stata/AGENTS.md
code/r/AGENTS.md
manuscript/AGENTS.md
```

The Stata layer may define version, log, working-directory, and package rules.
The R layer may define environment, package, seed, and test rules. The
manuscript layer may define bibliography, rendering, and claim-verification
rules. Root guidance should own raw-data immutability, source roles,
confidentiality, and release gates.

Do not impose this layout on an existing project. Map rules to the actual
subtrees and propose directory changes separately.

## Team versus personal

Track shared, collaborator-relevant guidance in repository instructions and
supported project configuration. Keep machine paths, credentials, personal
UI choices, and unrelated global preferences outside tracked files. A
`.maw/local.yaml` entry may document a personal preference, but it does not
become executable project guidance until LAW maps it to an appropriate
supported surface.
