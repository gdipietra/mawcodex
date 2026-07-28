# Step 010 — ManageRAW project control plane

Date: 2026-07-28

## Scope

This revision promotes the package from `1.1.0` to `1.2.0`. It adds a native
control plane for adopting and maintaining MAW across heterogeneous academic
projects and alongside unrelated specialist plugins.

## Capability revision

JAW remains the initial project-readiness capability. Five narrow skills join
it:

1. CAW coordinates responsibility across MAW, project-local skills, and
   external plugins.
2. PAW records shared team and untracked personal choices.
3. LAW designs root and nested `AGENTS.md` layers and explains their effective
   precedence.
4. UAW performs a user-invoked three-way reconciliation between the old MAW
   base, project overlay, and new MAW base.
5. SAW exports a user-invoked, sanitized, evidence-backed slice that can be
   reviewed for a future MAW version.

UAW and SAW opt out of implicit invocation. JAW now stops after onboarding and
routes ongoing work to the narrower capability.

## Agent and state model

The native `manageraw` project agent is a control-plane coordinator, not an
academic execution specialist. It begins read-only, loads the applicable
instruction chain, validates the project state, selects the narrow management
skill, and writes only an exact approved local change.

The initializer adds:

- tracked `.maw/profile.yaml` for shared adoption, ownership, source roles,
  build profiles, protected-material categories, and instruction layers;
- ignored `.maw/local.yaml` for non-weakening personal preferences;
- tracked `.maw/lock.json` for version and schema agreement;
- `.maw/history/` and `.maw/slices/` for approved durable records;
- a standard-library state validator.

The profile uses JSON syntax as a YAML 1.2 subset. `AGENTS.md` remains the real
Codex instruction surface; `.maw` only records decisions and routing.

## Fixed-source boundary

The upstream source manifest remains exactly 52 skills and 18 agents. This
release packages 58 skills and 19 agents by adding 6 native management skills
and 1 native control-plane agent. Native additions have separate conversion
records and do not change Pedro's fixed `v2.1.0` provenance counts.

## Initial forward-use cases

The control plane is exercised against:

- an ongoing Math or Econometrics teaching project with many existing LaTeX
  sources, compiler and bibliography requirements, duplicate output surfaces,
  and protected exams or answer keys;
- an ongoing research project with unorganized Stata and R code, raw and
  derived data, multiple empirical entry points, and provisional idea
  sketches.

Both profiles favor proportional adoption, preserve existing layouts, and
require representative builds before a readiness claim.

## Verification

Release evidence must include package and official skill validation,
deterministic state tests, semantic contracts for all management skills,
initializer coverage, two independent forward-use-case reviews, current
provenance hashes, and a snapshot-bound full release gate.
