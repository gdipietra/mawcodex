# Public release readiness statement: MAW Codex 1.2.2

Statement date: 2026-08-23

Status: **PUBLISHED AND POST-PUSH VERIFIED AT CHECKPOINT `cc82cede0eed6b721f23cc82862e0ad189db2824`**

## Decision

MAW Codex `1.2.2` is technically ready to be shared first with Pedro H. C.
Sant'Anna and then with a small group of close colleagues. This statement does
not announce a new version, promise a `1.2.3` release, create a GitHub Release,
or authorize an email, message, issue, deployment, or broader announcement.

The recommended sequence is intentional: give the original author the first
opportunity to check attribution, behavioral fidelity, and possible
collaboration; then ask trusted colleagues to test whether the package and its
documentation are understandable without conversion history in hand.

## Verified basis

- Commit `cc82cede0eed6b721f23cc82862e0ad189db2824` is the verified
  publication/content checkpoint on the canonical repository
  `https://github.com/gdipietra/mawcodex`.
- [Stable-gates run 32666609822](https://github.com/gdipietra/mawcodex/actions/runs/32666609822)
  passed on Windows and Ubuntu.
- [GitHub Pages run 32666609835](https://github.com/gdipietra/mawcodex/actions/runs/32666609835)
  passed build and deployment.
- The public site at `https://gdipietra.github.io/mawcodex/` returned HTTP 200,
  and the repository homepage metadata uses that canonical URL.
- This remote evidence validates checkpoint
  `cc82cede0eed6b721f23cc82862e0ad189db2824` only. Later commits, including
  documentation evidence updates, require fresh same-SHA remote verification.
- The public site gives Pedro H. C. Sant'Anna direct original-work credit and
  distinguishes 52 source-derived capabilities from MAW Codex's native
  management and control-plane additions.
- Source baseline, source and target hashes, license notices, capability
  classifications, and the GitHub identity migration are recorded in the
  conversion evidence.

## Known issue accepted for 1.2.2

On Windows, `scripts/maw.cmd` can accept the WindowsApps `python.exe` alias as
if it were a runnable Python interpreter. The resulting maintenance command
fails before falling back to the bundled Codex runtime.

The scope is bounded: installed skills and the loaded `1.2.2` plugin are not
affected. Before this audit and under separate authorization, the
personal-store update succeeded by invoking the installer with the bundled
Python explicitly. This audit performs no personal-store update or other
external action. The issue is therefore an accepted P1 launcher and
installation-UX limitation with a verified workaround, not a scientific,
provenance, confidentiality, or installed-runtime failure.

No fix is planned for this `1.2.2` review sequence, and no `1.2.3` release is
promised. The exception and exact workaround must accompany any preview. If
future maintenance is authorized, the launcher should probe candidate
executables and include a regression test for a non-runnable PATH alias.

## Completed publication verification

- Commit `cc82cede0eed6b721f23cc82862e0ad189db2824` was pushed to `main`
  under separate explicit authorization.
- Stable-gates run `32666609822` succeeded.
- GitHub Pages run `32666609835` succeeded.
- The public Pages endpoint returned HTTP 200.
- Repository homepage metadata uses the canonical Pages URL.
- GitHub issue `#1` is open with no milestone.
- These facts establish the verified publication/content checkpoint; they do
  not remotely validate later commits.

## Communication sequence

1. Send Pedro the repository and live-site links, explain the Codex-native
   adaptation and native management additions, and invite corrections or
   collaboration without requesting endorsement.
2. After Pedro has had a reasonable opportunity to respond, share with a
   small group of close colleagues as a preview and request concrete feedback
   on installation, terminology, attribution, and capability discoverability.
3. Decide separately whether to make a broader public announcement. Resolve
   any attribution or safety-critical feedback first; non-blocking UX items
   may remain openly documented.

## Issue tracking boundary

GitHub [issue #1](https://github.com/gdipietra/mawcodex/issues/1) tracks the
Windows launcher defect and is open with no milestone.

## Readiness conclusion

**Local package for Pedro's review: READY, with disclosed P1 exception.**

**Repository and site links at verified publication/content checkpoint
`cc82cede0eed6b721f23cc82862e0ad189db2824`: PUBLISHED AND VERIFIED.**

**Broad public announcement: NOT READY**, pending the planned human-feedback
sequence rather than publication infrastructure or additional `1.2.x`
engineering.
