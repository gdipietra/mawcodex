# Public release readiness statement: MAW Codex 1.2.2

Statement date: 2026-08-23

Status: **PREPARED LOCALLY; PUBLICATION GATES PENDING**

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

- The canonical repository target is `https://github.com/gdipietra/mawcodex`,
  and the historical deployed site snapshot is available at
  `https://gdipietra.github.io/mawcodex/`.
- For commit `02c76b2c91f673b634c8496b3c49fbd422bbee09`,
  [stable-gates run 32603918490](https://github.com/gdipietra/mawcodex/actions/runs/32603918490)
  passed on Windows and Ubuntu, and
  [Pages run 32603918449](https://github.com/gdipietra/mawcodex/actions/runs/32603918449)
  passed build and deployment.
- Those remote runs apply only to that historical snapshot. The current
  repaired local tree awaits an authorized commit and push plus fresh CI and
  Pages verification.
- The current local tree passes the plugin validator, all 58 skill validators,
  all 51 deterministic unit tests, and all 14 stable-package checks. These
  local results are not yet bound to a pushed commit or fresh remote runs.
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

## Publication prerequisites

Before the repository or site is sent as the reviewed public surface:

1. Obtain explicit authorization to commit and push these documentation and
   evidence changes.
2. Update the GitHub repository Website metadata from the retired `dipietra`
   Pages URL to `https://gdipietra.github.io/mawcodex/`.
3. Verify the pushed content, a fresh Windows/Ubuntu stable-gates run, and a
   fresh Pages deployment against the same head SHA.
4. Optionally create an open GitHub issue for the accepted launcher exception;
   issue creation remains a separately authorized external action.

## Communication sequence

1. After the publication prerequisites pass, send Pedro the repository and
   live-site links, explain the Codex-native
   adaptation and native management additions, and invite corrections or
   collaboration without requesting endorsement.
2. After Pedro has had a reasonable opportunity to respond, share with a
   small group of close colleagues as a preview and request concrete feedback
   on installation, terminology, attribution, and capability discoverability.
3. Decide separately whether to make a broader public announcement. Resolve
   any attribution or safety-critical feedback first; non-blocking UX items
   may remain openly documented.

## Issue tracking boundary

An open GitHub issue is a reasonable way to track the Windows launcher defect,
with a title such as `Windows: maw.cmd can select the non-runnable WindowsApps
Python alias`. No issue is claimed to exist until its creation is explicitly
authorized and confirmed on GitHub.

## Readiness conclusion

**Local package for Pedro's review: READY, with disclosed P1 exception.**

**Repository and site links as the reviewed surface: PENDING PUBLICATION AND
POST-PUSH VERIFICATION.**

**Broad public announcement: NOT READY**, pending the publication gates and
planned human feedback sequence, not additional `1.2.x` engineering.
