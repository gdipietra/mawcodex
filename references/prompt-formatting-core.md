<!-- Native rewrite of .claude/references/prompt-formatting-core.md at be53c12f235996dff41fb7f21580506fd2dd8d50; source SHA-256 2350ddbf27122cd4bb2abdcdaf8ae0460b15e82445cc42808028be2facc827f3. -->

# Prompt-formatting core

This reference supports the
[`prompt-shaping`](rules/prompt-shaping.md) rule. It is a standing interaction
habit, not a separate command: turn an ambiguous academic request into a
bounded, evidence-aware task before execution.

The structured-prompt pattern is adapted with attribution from Chris
Blattman's
[`claudeblattman`](https://github.com/chrisblattman/claudeblattman). Vendor
routing and multi-model command syntax are intentionally omitted.

## Six-part task contract

### 1. Role

Name the relevant expertise in one specific sentence. Prefer "applied
econometrics referee evaluating identification" over "helpful assistant."
Roles guide judgment but never substitute for evidence.

### 2. Task

State one verb-first objective and name the finished artifact:

> Identify the three weakest links in this paper's identification strategy and
> return an evidence-located referee memo.

### 3. Context

Provide only facts that affect the task:

- project and artifact;
- target audience or journal;
- controlling source of truth;
- decisions already made;
- claims already verified or ruled out;
- data-access or confidentiality constraints.

Distinguish provided facts from assumptions. Do not manufacture missing
context.

### 4. Constraints

State MUST, SHOULD, and MUST NOT conditions. Academic constraints commonly
include:

- do not invent citations or empirical facts;
- do not change the estimand without naming the change;
- preserve current and comparison versions;
- do not expose restricted data;
- do not commit, submit, send, deploy, or sync externally without explicit
  authorization.

### 5. Evidence and verification

Name the sources the work may rely on and the checks that establish
completion. Require primary sources for current external claims, executed
analysis for numeric claims, and rendered inspection for visual artifacts.
Anything not checked must be labeled UNVERIFIED.

### 6. Output contract

Specify a concrete shape: file, table columns, memo sections, maximum length,
severity vocabulary, and required locations or citations. End with the
blocking ambiguity rule:

> If a missing user decision would materially change the result, ask one
> concise question before proceeding. Otherwise state the assumption and
> continue.

## Depth calibration

Use the lightest contract that makes failure observable.

| Depth | Use when | Required elements |
| --- | --- | --- |
| Light | short, low-risk, single-artifact request | role, task, output |
| Standard | domain-specific work or several constraints | all six parts plus stated assumptions |
| Deep | submission, restricted data, causal design, multiple artifacts, or high-cost execution | all six parts, source inventory, risk register, and verification plan |

The user's requested depth overrides this heuristic. High stakes can require a
deeper contract even when the initial prompt is short.

## Academic example

Informal request:

> Help me answer the referee's measurement-error concern without picking a
> fight.

Shaped contract:

- **Role:** applied econometrician drafting a respectful R&R response.
- **Task:** draft one response paragraph and one proposed robustness check.
- **Context:** treatment is measured with error; the author believes the error
  is classical; one-revision policy; current estimates and cited sources must
  be inspected.
- **Constraints:** acknowledge the concern; do not assert attenuation without
  checking that the classical-error assumptions actually hold; do not invent a
  textbook citation; do not promise an analysis that cannot be run.
- **Evidence:** verify the manuscript's measurement definition, specification,
  and cited econometric result.
- **Output:** five to eight sentences plus a one-line UNVERIFIED list.

This version makes a crucial uncertainty visible: "classical" is an
assumption to substantiate, not a free rebuttal.

## Boundary with `$interview-me`

Prompt shaping is a single-task clarification habit. `$interview-me` is a
multi-turn research-specification workflow that develops the research
question, hypotheses, identification strategy, data needs, and empirical plan.
Use the latter when the project itself is underspecified, not merely the next
task.
