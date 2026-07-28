# ManageRAW project profile

ManageRAW is MAW Codex's project-level control plane. It records how MAW
coexists with the project, its instruction hierarchy, and other plugins. It
does not replace `AGENTS.md`: Codex behavior still comes from the applicable
global, root, and nested instruction files.

## State files

| Path | Audience | Git policy | Purpose |
| --- | --- | --- | --- |
| `.maw/profile.yaml` | Team | Track | Shared adoption, ownership, layers, source roles, and build profiles |
| `.maw/local.yaml` | Individual | Ignore | Personal preferences that cannot weaken shared rules |
| `.maw/lock.json` | Team | Track | Installed MAW version and profile schema |
| `.maw/history/` | Team | Track selected records | Approved update and migration decisions |
| `.maw/slices/` | Team | Track selected exports | Sanitized reusable patterns prepared by `$saw` |

The `.yaml` files deliberately use JSON syntax, which is a valid YAML 1.2
subset. This lets the standard-library validator parse them deterministically
without installing a YAML package in every academic project.

## Shared profile contract

`schema_version` is currently `1`. The top-level fields are:

- `project`: portable slug, `teaching`, `research`, or `mixed` type,
  classification status, and primary working language.
- `maw`: base version, adoption shape, governance owner, and manager agent.
  Adoption is `plugin-only`, `thin`, `selective`, or `full`.
- `instruction_layers`: global inheritance policy, the team root instruction
  file, optional nested instruction files, and the untracked personal layer.
  Each nested record uses a safe `path`, `owner: team`, a short `scope`, and
  `managed_block: manageraw` or `null` for an entirely human-managed file.
- `capability_ownership`: one unique record per responsibility. Each record
  names an owner and uses `primary`, `specialist`, `shared`, or `fallback`
  priority.
- `external_plugins`: named plugins only, with `responsibilities` and a status
  of `active`, `optional`, `unavailable`, or `disabled`. Do not copy private
  plugin internals into the profile.
- `skill_policy`: preferred, explicit-only, disabled, and project-local skill
  names. UAW and SAW must remain explicit-only.
- `source_roles`: authoritative, mirror, import, generated, and restricted
  locations. Each record has a unique `name`, a `role`, and a `location`
  expressed as a project-relative path or a logical external role such as
  `external:overleaf`.
- `build_profiles`: records with a unique `name`, `kind`, `entrypoint`,
  expected `artifact`, and non-empty `verification` list for LaTeX, Quarto, R,
  Stata, Python, Julia, or another actual stack.
- `protected_material`: records with `category`, `location`, and `handling`.
  Handling is `local-only`, `restricted`, `embargoed`, `do-not-export`, or
  `institution-controlled`. Never store the protected contents here.
- `personalization`: shared team choices and the personal overlay path.

Never place credentials, tokens, passwords, raw data, personal identifiers,
solution content, or machine-specific absolute paths in shared MAW state.

## Effective precedence

For a file being worked on, ManageRAW keeps these authority levels distinct:

1. higher-authority platform, session, and developer instructions always
   control;
2. applicable global and project `AGENTS.md` instructions form a chain from
   broadest to closest, with deeper project files taking precedence over
   broader project files where that chain conflicts;
3. the user's current request selects the outcome and grants only compatible,
   explicitly stated authorization;
4. the selected skill supplies its bounded workflow contract;
5. shared `.maw/profile.yaml` supplies routing and ownership records;
6. `.maw/local.yaml` supplies only non-weakening personal preferences;
7. MAW defaults fill remaining non-material gaps.

Global Codex instructions may also apply before the project chain. LAW maps
the chain; it does not claim to rewrite global instructions. Same-named skills
do not merge automatically, so CAW records which skill or plugin owns an
overlapping responsibility.

## Capability registry

MAW's native management responsibilities are:

| Capability | Default owner |
| --- | --- |
| Academic governance | `mawcodex` |
| Project onboarding and readiness | `mawcodex:jaw` |
| Plugin and skill coordination | `mawcodex:caw` |
| Shared and personal project settings | `mawcodex:paw` |
| Root and nested instruction layers | `mawcodex:law` |
| Upstream workflow reconciliation | `mawcodex:uaw` |
| Sanitized reusable-pattern export | `mawcodex:saw` |

External capabilities may be assigned to another named plugin. MAW remains
the academic-governance owner, while a specialist plugin may own operations
such as email, calendars, cloud files, Git hosting, or Overleaf publication.
CAW must record overlaps, delegation, unavailable fallbacks, and external
authorization boundaries.

## Teaching starter profile

For an ongoing Math or Econometrics course:

- prefer `thin` adoption;
- inventory existing `.tex`, `.bib`, `.sty`, `.cls`, `.qmd`, and generated
  PDFs before adding folders;
- record the canonical lecture source and any duplicate Beamer or Quarto
  surfaces;
- identify answer keys, exams, student data, and embargoed materials as
  protected;
- make a representative XeLaTeX or Quarto build a readiness gate;
- use LAW only when a course, term, lecture, exam, or solutions subtree needs
  narrower instructions.

## Research starter profile

For an ongoing project with mixed Stata and R code:

- prefer `thin` or `selective` adoption;
- map raw, intermediate, derived, output, manuscript, and sketch locations
  before reorganizing anything;
- identify actual entry points, package/runtime versions, seeds, and output
  dependencies without assuming the existing numbering is authoritative;
- keep raw and restricted data immutable and avoid opening large sensitive
  files merely to classify them;
- record whether R or Stata controls each table, figure, and estimate;
- use LAW only for subtrees whose data access, execution environment, or
  output-disclosure rules genuinely differ.

## Safe changes

Before writing shared state or a managed instruction block:

1. validate the current state and preserve a pre-change copy or diff;
2. show the exact proposed fields and files;
3. obtain approval for that local change;
4. write atomically where the host permits it;
5. validate again and record a concise history entry when the change affects
   ownership, precedence, adoption, or the MAW base version.

Approval for a local control-plane edit never authorizes commit, push, remote
sync, dependency installation, publication, submission, or messaging.
