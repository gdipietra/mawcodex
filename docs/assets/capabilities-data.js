window.MAW_CAPABILITIES = [
  {
    name: "audit-reproducibility",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Checks numerical manuscript claims against actual R, Stata, or Python outputs under declared tolerances.",
    translation: "Records each claim and its evidence in a table with PASS, FAIL, EXPLAINED, or UNMATCHED. A missing runtime leaves the claim unverified."
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
    summary: "Saves a checkpoint before a handoff or pause so the next session can pick up the work.",
    translation: "Saves decisions, file and line references, open questions, and next steps in a project file that another session can read."
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
    translation: "Shows exactly which files are staged and checks them before committing. Each action needs its own approval, including pushing, opening a pull request, and merging."
  },
  {
    name: "compile-latex",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds Beamer decks with XeLaTeX passes and bibliography handling from the correct source context.",
    translation: "Finds the compiler on the current machine and marks missing fonts or XeLaTeX as UNVERIFIED. The shared template includes fallbacks for Lato and Helvetica."
  },
  {
    name: "compress-session",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Writes a session log that explains what was decided, what was ruled out, and where to resume.",
    translation: "Saves the log as a project file that the next session can read and review."
  },
  {
    name: "context-status",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Reports the observable plan, checkpoint, session log, working tree, and context-preservation state.",
    translation: "Reads status from supported Codex surfaces and saved project files. It reports which context metrics are available."
  },
  {
    name: "create-lecture",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Builds a new Beamer lecture from supplied sources with notation and preamble consistency.",
    translation: "Checks which sources and tools are available, records the instructor's choices, and then drafts, compiles, and reviews the lecture."
  },
  {
    name: "data-analysis",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Creates a numbered, reproducible R workflow from an observed dataset through verified tables and figures.",
    translation: "Checks data sensitivity first and preserves the raw files. It distinguishes descriptive analysis from causal analysis and records which scripts and outputs were produced."
  },
  {
    name: "data-management-plan",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Drafts a funder-specific data management and sharing plan from current authoritative requirements.",
    translation: "Checks current funder requirements against primary sources and saves a local draft for review."
  },
  {
    name: "deep-audit",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Combines deterministic repository validators with independent provenance, behavior, executable, and UX review lenses.",
    translation: "Gives each reviewer a distinct part of the audit and combines their findings into a verdict: CLEAN, CONDITIONALLY CLEAN, or NOT CLEAN."
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
    translation: "Returns specific questions tied to slides or passages. The review is read-only."
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
    translation: "Screens outputs locally and marks findings CRITICAL, WARNING, or OK. Release still requires the appropriate disclosure approval."
  },
  {
    name: "extract-tikz",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns TikZ figures from a Beamer deck into standalone SVGs.",
    translation: "Finds the compiler and converter on the current machine. It keeps paths relative to the project and assigns each figure a consistent index."
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
    translation: "Flags repetitive phrasing and other style patterns for the author to review. The audit leaves edits to a separate step and makes no judgment about authorship."
  },
  {
    name: "interview-me",
    family: "Research design",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns a fuzzy research idea into a specification for question, estimand, identification, data, inference, and risks.",
    translation: "Asks follow-up questions about the study and saves the resulting research specification locally."
  },
  {
    name: "learn",
    family: "Project operations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Turns a verified, reusable discovery into a narrowly triggered Codex skill.",
    translation: "Writes Codex skill metadata and includes only the resources the skill needs. It checks the structure and screens drafts for secrets."
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
    translation: "Turns a workflow into a usable skill by documenting when to invoke it, which resources it needs, and how to check its structure."
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
    translation: "Returns a read-only report with file and line references. Layout remains UNVERIFIED until the document is rendered."
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
    summary: "Builds a local replication package for a journal submission. One command runs the analysis, and a manifest links each exhibit to the code that produces it.",
    translation: "The manifest records the access status of each dataset. The skill checks the package locally and leaves deposit submission to the user."
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
    translation: "Assigns separate roles to editors and referees. The review ties its findings to the manuscript and checks any relevant code and claims."
  },
  {
    name: "review-r",
    family: "Empirical and reproducibility",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Reviews R scripts for correctness and whether someone else can rerun them.",
    translation: "The review is read-only. It records missing data and project conventions that could affect the findings."
  },
  {
    name: "scaffold-exercises",
    family: "Teaching and presentations",
    origin: "adapted",
    mode: "Native rewrite",
    summary: "Drafts problem sets that can include analytical work, empirical tasks, and coding.",
    translation: "Keeps the student handout separate from the answer key and follows the supplied source material."
  },
  {
    name: "seven-pass-review",
    family: "Writing and review",
    origin: "adapted",
    mode: "Composed replacement",
    summary: "Runs seven independent manuscript lenses across argument, methods, results, robustness, prose, and citations.",
    translation: "Gives seven Codex reviewers separate parts of the manuscript and combines their findings into one prioritized revision plan."
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
    translation: "Selects reviewers based on what the deck contains. They report findings and leave the slides unchanged."
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
    summary: "Builds a syllabus that teaches prerequisites first and links learning objectives to assessments.",
    translation: "Uses the supplied topics and readings, makes assumptions visible, and leaves the policy language open for instructor review."
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
    translation: "Starts with a read-only assessment. It identifies authoritative sources and protected files, checks representative dependencies, and recommends how much of MAW to adopt."
  },
  {
    name: "caw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Coordinates ownership when MAW coexists with other plugins, connectors, skills, and local instructions.",
    translation: "Records who handles each step and identifies tools that are unavailable. It asks the user to resolve choices that affect the project."
  },
  {
    name: "paw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Maintains shared project personalization and separate machine-specific choices.",
    translation: "Stores team decisions in the tracked .maw/profile.yaml. Personal settings live in the ignored .maw/local.yaml and must respect shared safeguards."
  },
  {
    name: "law",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Designs and verifies root and nested Codex instruction layers for an academic project.",
    translation: "First maps the instructions already in place. It then checks which root and folder rules apply at specific paths."
  },
  {
    name: "uaw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Reconciles an explicitly requested MAW update with an existing project's overlays and ownership decisions.",
    translation: "Compares the previous MAW base, the project's settings, and the proposed update. The project owner can review conflicts before applying or installing changes."
  },
  {
    name: "saw",
    family: "MAW control plane",
    origin: "native",
    mode: "Native addition",
    summary: "Exports sanitized, evidence-bounded slices of recorded MAW project state.",
    translation: "Prepares a local summary from recorded project state. It leaves out secrets, private transcript details, data, student information, unpublished content, and other plugins' settings."
  }
];
