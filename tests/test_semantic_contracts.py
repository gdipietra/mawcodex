"""Read-only contract tests for representative Codex-native skills.

These tests intentionally assert combinations of semantic requirements rather
than whole sentences. This keeps the release gate sensitive to the loss of a
safety boundary while allowing harmless prose and formatting revisions.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def skill_text(name: str) -> str:
    """Return normalized, case-folded skill text without changing the tree."""

    path = ROOT / "skills" / name / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", text).casefold()


def skill_bundle_text(name: str) -> str:
    """Return normalized skill instructions and directly bundled references."""

    directory = ROOT / "skills" / name
    parts = [
        path.read_text(encoding="utf-8")
        for path in sorted(directory.rglob("*.md"))
    ]
    return re.sub(r"\s+", " ", "\n".join(parts)).casefold()


class SemanticContractTests(unittest.TestCase):
    def assert_contract(self, skill: str, *patterns: str) -> None:
        text = skill_text(skill)
        for pattern in patterns:
            with self.subTest(skill=skill, contract=pattern):
                self.assertRegex(text, pattern)

    def test_interview_me_requires_dialogue_and_confirmation(self) -> None:
        self.assert_contract(
            "interview-me",
            r"ask one or two questions.*wait for the response",
            r"write the spec only after.*confirmed",
            r"exact estimand.*comparison group.*identifying assumption",
        )

    def test_jaw_preserves_existing_projects_and_requires_real_builds(
        self,
    ) -> None:
        self.assert_contract(
            "jaw",
            r"begin in assessment-only mode",
            r"research.*teaching.*mixed",
            r"plugin only.*thin project profile.*selective merge.*full initializer",
            r"run a minimal representative forward build.*isolated",
            r"approval to integrate locally does not authorize commit.*push.*publication",
            r"once the initial adoption and readiness report are complete, stop",
        )

    def test_caw_routes_ownership_without_absorbing_plugins(self) -> None:
        text = skill_bundle_text("caw")
        for pattern in (
            r"caw decides ownership.*does not perform the routed work",
            r"stay read-only",
            r"maw priority for academic validity.*only within maw's declared scope",
            r"owner for content is not automatically the owner for transport",
            r"do not create or update the project profile.*paw",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)

    def test_paw_separates_shared_personal_and_instruction_state(self) -> None:
        text = skill_bundle_text("paw")
        for pattern in (
            r"profile\.yaml.*tracked team/project personalization",
            r"local\.yaml.*personal or machine-specific.*gitignored",
            r"paw does not own.*root or nested.*agents\.md",
            r"cannot weaken team safeguards.*confidentiality.*reproducibility.*external-action gates",
            r"preserve the current.*base_version.*uaw owns version changes",
            r"approval for the exact profile diff",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)

    def test_law_owns_minimal_effective_instruction_layers(self) -> None:
        text = skill_bundle_text("law")
        for pattern in (
            r"begin read-only.*instruction graph",
            r"nested instruction file only when its subtree materially differs",
            r"deeper project guidance specializes its own subtree",
            r"preserve human sections.*clearly delimit any maw-managed block",
            r"local edits do not authorize commit.*push.*plugin installation",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)

    def test_uaw_is_explicit_three_way_reconciliation(self) -> None:
        text = skill_bundle_text("uaw")
        for pattern in (
            r"only after an explicit.*uaw.*never poll for updates",
            r"three-way reconciliation",
            r"b0.*old maw base.*o.*project overlay.*b1.*candidate new maw base",
            r"lock\.json.*only after.*validation has passed",
            r"do not commit.*push.*publish.*sync.*send",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)
        metadata = (
            ROOT / "skills" / "uaw" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertRegex(
            metadata,
            r"(?s)policy:\s+allow_implicit_invocation:\s+false",
        )

    def test_saw_is_explicit_sanitized_evidence_export(self) -> None:
        text = skill_bundle_text("saw")
        for pattern in (
            r"only after an explicit.*saw",
            r"never parse private transcript internals",
            r"never include credentials.*secrets.*data.*absolute paths",
            r"project-return slice.*upstream-learning slice",
            r"saw proposes candidates.*does not edit the main maw package",
            r"writing a slice does not authorize committing.*pushing.*transferring",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)
        metadata = (
            ROOT / "skills" / "saw" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertRegex(
            metadata,
            r"(?s)policy:\s+allow_implicit_invocation:\s+false",
        )

    def test_manageraw_is_read_first_control_plane(self) -> None:
        role = (
            ROOT / "references" / "agent-roles" / "manageraw.md"
        ).read_text(encoding="utf-8")
        text = re.sub(r"\s+", " ", role).casefold()
        for pattern in (
            r"start in read-only mode",
            r"routing table",
            r"if .*profile\.yaml.*is absent, route to jaw",
            r"teaching repositories with many latex sources.*do not reorganize",
            r"research repositories with mixed stata and r.*do not move data",
            r"do not install.*commit.*push.*sync.*publish.*submit.*send",
        ):
            with self.subTest(contract=pattern):
                self.assertRegex(text, pattern)

    def test_did_event_study_preserves_estimand_and_twfe_boundaries(self) -> None:
        self.assert_contract(
            "did-event-study",
            r"pick the estimand up front",
            r"if unbalanced.*different estimand",
            r"twfe event study.*benchmark.*never the headline",
            r"unavailable.*runtime.*unverified.*improvising an api",
        )

    def test_commit_limits_each_git_action_to_explicit_scope(self) -> None:
        self.assert_contract(
            "commit",
            r"request to commit does not authorize a push",
            r"stage only the paths.*scope",
            r"never use a catch-all staging",
            r"if push is explicitly authorized",
        )

    def test_disclosure_check_is_local_prescreen_not_clearance(self) -> None:
        self.assert_contract(
            "disclosure-check",
            r"pre-screen, not a substitute",
            r"do not upload values.*remote services",
            r"missing controlling rule.*unverified.*block release",
            r"pass here is not clearance to release",
        )

    def test_replication_package_excludes_restricted_data_and_uploads(self) -> None:
        self.assert_contract(
            "replication-package",
            r"keep raw source data immutable",
            r"never place restricted.*data in the package",
            r"unverified.*prevents a full-pass claim",
            r"never upload to openicpsr.*without.*explicit user request",
        )

    def test_review_paper_requires_current_profile_and_author_approval(self) -> None:
        self.assert_contract(
            "review-paper",
            r"verify unstable journal policy.*current official sources",
            r"unknown or unverified profile blocks a journal-calibrated verdict",
            r"proposed manuscript edit requires author approval",
            r"commit, push, submission, or sharing requires explicit authorization",
        )

    def test_verify_claims_keeps_verifier_independent_and_fails_closed(self) -> None:
        self.assert_contract(
            "verify-claims",
            r"independent verifier that never sees the full draft",
            r"do not give the verifier the draft.*desired conclusion",
            r"inaccessible material source is never downgraded",
            r"material source absent.*unverified",
        )

    def test_translate_to_quarto_preserves_source_and_visual_gate(self) -> None:
        self.assert_contract(
            "translate-to-quarto",
            r"source of truth throughout",
            r"missing compilers.*unverified",
            r"source-only comparison cannot pass visual parity",
            r"proposed patch and wait for approval",
            r"stop before any deployment",
        )

    def test_triage_inbox_stays_minimal_read_only_and_human_gated(self) -> None:
        self.assert_contract(
            "triage-inbox",
            r"default to read-only connector operations",
            r"do not copy full bodies.*personal data.*restricted content",
            r"sending, accepting, declining, booking, and scaffolding.*explicit authorization",
            r"tracker-only.*unverified",
        )

    def test_submission_disclosures_are_current_evidence_based_drafts(self) -> None:
        self.assert_contract(
            "submission-disclosures",
            r"verify it on.*official author-guidance pages",
            r"never infer an author's contribution.*without evidence or author confirmation",
            r"inaccessible policy is.*unverified",
            r"do not claim verification that was not run",
            r"submission, portal entry, or sending requires explicit authorization",
        )

    def test_data_analysis_preserves_raw_data_and_causal_design_gate(self) -> None:
        self.assert_contract(
            "data-analysis",
            r"keep raw inputs immutable",
            r"never turn an association into a causal claim without a stated estimand",
            r"if any input cannot be read.*stop and ask",
            r"missing r, packages, data access.*unverified",
        )

    def test_compile_latex_requires_runtime_log_and_visual_evidence(self) -> None:
        self.assert_contract(
            "compile-latex",
            r"confirm the required engine and bibliography backend",
            r"visually verify the pdf",
            r"do not treat compilation alone as visual pass",
            r"if xelatex.*unavailable.*mark that portion unverified",
        )

    def test_respond_to_referees_requires_evidence_and_no_submission(self) -> None:
        self.assert_contract(
            "respond-to-referees",
            r"never invent a revision.*journal detail",
            r"sending or submitting it requires explicit user authorization",
            r"mandatory independent post-flight",
            r"no verifiable evidence.*author-approved rationale.*unaddressed",
            r"--no-verify.*unverified.*not submission-ready",
        )

    def test_r_package_check_stops_without_runtime_and_never_releases(self) -> None:
        self.assert_contract(
            "r-package-check",
            r"if r or a required package is missing, stop.*unverified",
            r"do not install dependencies without authorization",
            r"do not bump a version.*submit to cran",
            r"do not describe an issue as fixed unless.*rerun",
            r"releasable.*requires 0 errors, 0 warnings",
        )


if __name__ == "__main__":
    unittest.main()
