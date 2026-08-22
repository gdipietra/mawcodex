window.MAW_CAPABILITIES = [
  {
    name: "audit-reproducibility",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Checks numerical manuscript claims against actual R, Stata, or Python outputs under declared tolerances.",
    translation: "Recasts the upstream audit as an evidence table with PASS, FAIL, EXPLAINED, and UNMATCHED states; an unavailable runtime can never become a pass."
  },
  {
    name: "capture-environment",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Captures software, packages, seeds, and lockfiles for R, Stata, and Python replication work.",
    translation: "Uses local runtime discovery and stack-specific artifacts without installing dependencies or claiming byte reproducibility when a tool is missing."
  },
  {
    name: "checkpoint",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Saves a compact, durable state snapshot before a stop, handoff, or context transition.",
    translation: "Moves continuity from provider transcript assumptions to explicit project files with decisions, line-level pointers, open questions, and next actions."
  },
  {
    name: "coauthor-brief",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Produces a cross-machine collaborator brief covering artifact state, changes, reproduction, and access boundaries.",
    translation: "Uses observable repository evidence and protected-data handoffs while keeping sending, sharing, and coauthor contact outside the skill."
  },
  {
    name: "commit",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Carries out only the precise Git or GitHub action the user authorizes.",
    translation: "Replaces broad provider permissions with action-scoped consent, staged-file review, quality gates, and a hard distinction between commit, push, PR, and merge."
  },
  {
    name: "compile-latex",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds Beamer decks with XeLaTeX passes and bibliography handling from the correct source context.",
    translation: "Discovers the actual compiler and reports missing XeLaTeX or fonts as UNVERIFIED; the shared template now checks Lato and Helvetica fallbacks."
  },
  {
    name: "compress-session",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Distills a noisy task into a structured session log with decisions, dead ends, and continuation points.",
    translation: "Persists only reviewable task state in project files, not private transcript serialization or inferred context telemetry."
  },
  {
    name: "context-status",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Reports the observable plan, checkpoint, session log, working tree, and context-preservation state.",
    translation: "Replaces the upstream private status-line parser with supported UI state and explicit evidence, marking unavailable telemetry as unavailable."
  },
  {
    name: "create-lecture",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds a new Beamer lecture from supplied sources with notation and preamble consistency.",
    translation: "Turns source ingestion, instructor choices, drafting, compilation, and review into explicit phases instead of assuming globally available files or commands."
  },
  {
    name: "data-analysis",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Creates a numbered, reproducible R workflow from an observed dataset through verified tables and figures.",
    translation: "Adds data-sensitivity orientation, descriptive-versus-causal separation, immutable raw-data rules, output routing, and execution evidence."
  },
  {
    name: "data-management-plan",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Drafts a funder-specific data management and sharing plan from current authoritative requirements.",
    translation: "Routes unstable policy claims through primary-source verification and produces a local draft; it never submits a plan or invents institutional facts."
  },
  {
    name: "deep-audit",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Combines deterministic repository validators with independent provenance, behavior, executable, and UX review lenses.",
    translation: "Implements the upstream audit intent with bounded Codex reviewers, typed findings, convergence rules, and explicit CLEAN, CONDITIONALLY CLEAN, or NOT CLEAN states."
  },
  {
    name: "deploy",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Prepares and, only when separately authorized, publishes rendered Quarto teaching material.",
    translation: "Separates render, asset synchronization, verification, commit, push, and deployment so a generic request cannot silently cross publication boundaries."
  },
  {
    name: "devils-advocate",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Challenges slide ordering, prerequisites, notation, motivation, and cognitive load without editing.",
    translation: "Runs as a read-only, evidence-located review and returns bounded questions rather than an untraceable global critique."
  },
  {
    name: "diagnose",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Root-causes wrong or failing empirical results through reproduce, minimize, hypothesize, instrument, and fix.",
    translation: "Preserves the disciplined debugging loop while enforcing data boundaries, explicit edit scope, and a no-fix diagnostic mode."
  },
  {
    name: "did-event-study",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Runs staggered difference-in-differences and event-study work with canonical packages and credibility diagnostics.",
    translation: "Retains Pedro's practitioner standard while requiring an explicit estimand, comparison group, timing, inference, sensitivity suite, and source-backed implementation."
  },
  {
    name: "disclosure-check",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Pre-screens restricted-data outputs for small cells, dominance, exact counts, PII, and unsafe statistics.",
    translation: "Turns disclosure control into a local release gate with CRITICAL, WARNING, and OK findings; it never substitutes for an authorized disclosure officer."
  },
  {
    name: "extract-tikz",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Extracts TikZ blocks from Beamer, compiles standalone diagrams, and converts them to SVG.",
    translation: "Uses project-relative paths, current binaries, deterministic indexing, and explicit compiler/converter checks instead of shell-specific assumptions."
  },
  {
    name: "grant-proposal",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Composes a research specification, evidence base, data plan, and environment plan into a grant scaffold.",
    translation: "Coordinates bounded local outputs and current funder requirements while keeping portal submission and institutional approval strictly external."
  },
  {
    name: "humanize",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Audits academic prose for repetitive, generic, promotional, or LLM-associated style patterns.",
    translation: "Runs as a read-only style diagnosis, avoids authorship inference, and separates evidence-backed findings from any later rewriting request."
  },
  {
    name: "interview-me",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns a fuzzy research idea into a specification for question, estimand, identification, data, inference, and risks.",
    translation: "Uses an explicit multi-turn preflight and writes a local specification rather than conflating ideation with literature search or implementation."
  },
  {
    name: "learn",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns a verified, reusable discovery into a narrowly triggered Codex skill.",
    translation: "Rebuilds skill authoring around Codex metadata, scoped resources, secret checks, and structural validation rather than provider command folders."
  },
  {
    name: "lit-review",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Searches, verifies, clusters, and synthesizes scholarly literature with cautious gap identification.",
    translation: "Uses available web or library capabilities, verifies citations against primary records, and preserves inaccessible evidence as UNVERIFIED."
  },
  {
    name: "new-diagram",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Creates or adapts a standalone TikZ diagram from reusable academic patterns.",
    translation: "Adds coordinate and label-overlap prevention, target-collision checks, actual compilation, visual inspection, and an independent diagram review."
  },
  {
    name: "new-skill",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Designs and scaffolds a Codex skill from a repeated or fuzzy workflow request.",
    translation: "Maps intent to Codex trigger metadata, concise instructions, optional resources, UI metadata, and deterministic validation with no migration placeholders."
  },
  {
    name: "pedagogy-review",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Reviews narrative arc, prerequisites, examples, notation, pacing, and student perspective in a lecture deck.",
    translation: "Runs through a read-only portable reviewer role and reports slide-located evidence without silently rewriting the instructor's source."
  },
  {
    name: "permission-check",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Diagnoses why Codex is or is not requesting approval in the current workspace and session.",
    translation: "Inspects supported workspace, policy, profile, and instruction layers with redaction, rather than recommending permission bypass."
  },
  {
    name: "power-analysis",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Computes power, sample size, or minimum detectable effects for documented experimental and quasi-experimental designs.",
    translation: "Requires design assumptions, reproducible calculations, Monte Carlo uncertainty where needed, and registry-ready reporting without inventing inputs."
  },
  {
    name: "preregister",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Drafts an OSF, AsPredicted, or AEA registry preregistration with estimands, exclusions, inference, and stopping rules.",
    translation: "Creates a prospective local draft and readiness gate; upload, registration, and submission remain separate explicit actions."
  },
  {
    name: "promote-memory",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Reviews candidate reusable lessons for generality, staleness, redundancy, evidence, and format.",
    translation: "Uses independent bounded critics and proposes promotion only after explicit approval, keeping personal and shared memory scopes distinct."
  },
  {
    name: "proofread",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Checks academic TeX and Quarto prose for language, terminology, notation, citations, and render-visible overflow.",
    translation: "Produces a read-only, location-specific report and treats unrendered layout as UNVERIFIED rather than guessing from source."
  },
  {
    name: "qa-quarto",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Runs adversarial parity QA between a rendered Quarto deck and its authoritative Beamer PDF.",
    translation: "Implements a bounded critic-fixer loop with fresh renders, hard content and notation gates, TikZ freshness, and convergence limits."
  },
  {
    name: "r-package-check",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Runs a release gate for R packages across documentation, tests, CRAN checks, coverage, and source review.",
    translation: "Uses the actual R toolchain when available, triages every error, warning, and note, and never bumps or submits a release automatically."
  },
  {
    name: "replication-package",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Assembles a local journal-oriented replication package with manifests, one-command execution, and exhibit mapping.",
    translation: "Separates open, licensed, restricted, and unavailable data; verifies artifacts locally and never uploads a deposit."
  },
  {
    name: "research-ideation",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Generates and ranks research questions with hypotheses, estimands, designs, data needs, and falsification checks.",
    translation: "Makes assumptions explicit, grounds external facts, and keeps one-shot ideation separate from the deeper interview and literature workflows."
  },
  {
    name: "respond-to-eval",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns anonymized course-evaluation evidence into a bounded teaching-improvement plan.",
    translation: "Clusters themes without silencing low-frequency feedback and maps Keep, Change, Investigate, or Out-of-scope decisions to course artifacts."
  },
  {
    name: "respond-to-referees",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Maps every referee concern to revision evidence and drafts a courteous response document.",
    translation: "Requires exact manuscript locations and coverage states, preventing unsupported claims that a requested revision was completed."
  },
  {
    name: "review-paper",
    family: "Writing and review",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Reviews manuscripts in comprehensive, adversarial, or journal-calibrated simulated peer-review modes.",
    translation: "Composes portable editor and referee roles, bounded fresh-context reviewers, typed findings, code linkage, and hallucination checks instead of provider-specific agents."
  },
  {
    name: "review-r",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Performs a read-only review of R code for reproducibility, numerical safety, and domain correctness.",
    translation: "Separates static code review from executing numeric claims and keeps any unavailable project convention or data dependency explicit."
  },
  {
    name: "scaffold-exercises",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Scaffolds analytical, empirical, and coding exercises with separate student and solution artifacts.",
    translation: "Preserves source authority and protected-answer separation while keeping grading, exam administration, and publication outside the workflow."
  },
  {
    name: "seven-pass-review",
    family: "Writing and review",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Runs seven independent manuscript lenses across argument, methods, results, robustness, prose, and citations.",
    translation: "Rebuilds parallel review with bounded Codex contexts and deterministic reduction of typed findings into one prioritized revision plan."
  },
  {
    name: "simulation-study",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Designs and runs seeded Monte Carlo studies with retained raw results and Monte Carlo standard errors.",
    translation: "Requires DGP-to-estimand alignment, reproducible grids, uncertainty reporting, and an independent simulation-specific review."
  },
  {
    name: "slide-excellence",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Coordinates visual, pedagogical, proofreading, diagram, parity, code, and subject-matter slide reviews.",
    translation: "Conditionally fans out only the relevant Codex reviewer roles and reduces evidence without granting review agents editing authority."
  },
  {
    name: "stata-replication",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds a numbered Stata replication pipeline with immutable raw data, logs, outputs, and optional R checks.",
    translation: "Uses local Stata or an explicitly available connector, preserves logs and transformations, and records absent automation as UNVERIFIED."
  },
  {
    name: "submission-disclosures",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Drafts AI-use, CRediT, conflict-of-interest, and data-availability statements for a target journal.",
    translation: "Requires current primary journal policy, produces local text, and separates policy drafting from statistical disclosure-control screening."
  },
  {
    name: "syllabus",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds or restructures a dependency-ordered syllabus with objectives, assessment alignment, and editable policy language.",
    translation: "Uses supplied topics and readings as authority, exposes assumptions, and does not silently create unsupported institutional policy."
  },
  {
    name: "teach-from-paper",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns one paper into a level-calibrated teaching outline, results map, slide skeleton, discussion, and exercise brief.",
    translation: "Keeps the paper authoritative, distinguishes teaching from validity review, and records source gaps instead of filling them from memory."
  },
  {
    name: "translate-to-quarto",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Creates a RevealJS mirror of an authoritative Beamer lecture with diagrams, citations, and environments mapped.",
    translation: "Composes a translator role, actual dual rendering, asset extraction, and slide-level parity checks; deployment remains a separate capability."
  },
  {
    name: "triage-inbox",
    family: "Project operations",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Turns academic email and calendar context into a prioritized digest and referee-obligation tracker.",
    translation: "Uses active Codex connectors when available and proposes human-gated actions; it never sends mail, accepts invitations, or books events automatically."
  },
  {
    name: "validate-bib",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Audits bibliography structure and citation use across LaTeX, Quarto, and Markdown.",
    translation: "Separates structural key checks from optional DOI metadata verification and from the distinct question of whether a citation supports a claim."
  },
  {
    name: "verify-claims",
    family: "Writing and review",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Applies fresh-context Chain-of-Verification to factual, numerical, dataset, entity, and negative-literature claims.",
    translation: "Uses an independent Codex verifier with extracted claims and sources, returning supported, contradicted, explained, or unverifiable states."
  },
  {
    name: "visual-audit",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Inspects every rendered Beamer or Quarto slide for overflow, clipping, contrast, spacing, and consistency.",
    translation: "Requires actual rendered pages and image evidence; absent render tools produce UNVERIFIED rather than a source-only visual pass."
  },
  {
    name: "jaw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Assesses how MAW can safely join a new or ongoing research, teaching, or mixed project.",
    translation: "Starts assessment-only, maps source authority and protected material, tests representative dependencies, and recommends plugin-only, thin, selective, or full adoption."
  },
  {
    name: "caw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Coordinates ownership when MAW coexists with other plugins, connectors, skills, and local instructions.",
    translation: "Produces a short read-only execution contract instead of inventing global plugin precedence; unresolved or unavailable capabilities remain explicit."
  },
  {
    name: "paw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Maintains shared project personalization and separate machine-specific choices.",
    translation: "Stores team decisions in tracked .maw/profile.yaml, personal non-weakening settings in ignored .maw/local.yaml, and records capability ownership without copying another plugin's internals."
  },
  {
    name: "law",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Designs and verifies root and nested Codex instruction layers for an academic project.",
    translation: "Builds a read-only instruction graph first, keeps root invariants separate from subtree differences, and checks effective precedence at representative target paths."
  },
  {
    name: "uaw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Reconciles an explicitly requested MAW update with an existing project's overlays and ownership decisions.",
    translation: "Uses a three-way comparison of old base, project overlay, and candidate base; discovery, planning, applying, installation, and external actions remain distinct gates."
  },
  {
    name: "saw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Exports sanitized, evidence-bounded slices of recorded MAW project state.",
    translation: "Excludes secrets, private transcript internals, data, student information, unpublished content, and external-plugin settings; unsupported inferences are not promoted."
  }
];
