# Hook portability map

Source boundary: upstream commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`).

Exact source hashes, target/replacement hashes, allowed classifications, and
per-hook revision summaries are recorded in
`RUNTIME_SURFACES_MANIFEST.json`.

MAW Codex enables four lifecycle mappings in `hooks/hooks.json`. Plugin hooks
run only after the user trusts the plugin. The Python and PowerShell runners
have the same contract and fail open on internal helper errors.

On POSIX systems, `maw_hook.sh` resolves `python3` and then `python`. If neither
is available, it emits a visible inactive-guardrail notice and exits without
blocking the underlying Codex action. Windows uses the native PowerShell
runner and does not require Python for hooks.

| Upstream hook | Codex-native surface | Status | Preserved intent |
| --- | --- | --- | --- |
| `git-guardrails.py` | `PreToolUse` | Enabled | Deny a narrow set of destructive Git operations; warn about machine-specific paths in research code. |
| `claim-reconcile.py` | `PostToolUse` | Enabled | Mark passport claims potentially stale after a referenced analysis file changes. |
| `pre-compact.py` | `PreCompact` | Enabled | Save active-plan and session-log pointers before compaction. |
| `post-compact-restore.py` | `SessionStart` for `compact` and `resume` | Enabled | Restore durable task pointers and require a fresh status/diff check. |
| `context-monitor.py` | Codex context UI, `$context-status`, and compaction hooks | Native replacement | Preserve context awareness without estimating tokens from an undocumented transcript format. |
| `log-reminder.py` | `$checkpoint`, `$compress-session`, and session-logging rule | Explicit replacement | Keep durable logs intentional and reviewable instead of writing to the project after every stop. |
| `notify.sh` | Codex desktop notifications or an optional user automation | Native replacement | Use the host application's notification surface rather than shell-specific desktop commands. |

## Safety behavior

- Direct `git reset --hard`, forced `git clean`, `git push --force`, blanket
  staging, and mass restore/checkout forms are denied before execution. The
  guardrail tokenizes quoted arguments, supported global Git options, and
  common compound-shell separators before applying the policy.
- `git push --force-with-lease` remains available because it has a distinct,
  reviewable safety contract.
- The hook is defense-in-depth, not a shell interpreter. Git aliases, dynamic
  evaluation, variable expansion, or custom wrappers can obscure intent and
  still require normal Codex approval, sandbox, and review controls.
- Hardcoded `/Users/...`, `/home/...`, and `C:\Users\...` paths in R, Quarto,
  Stata, Python, and Julia files produce a portability warning.
- Set `MAWCODEX_STRICT_PATHS=1` to turn that warning into a denial.
- Claim reconciliation is advisory: it never asserts that a result changed,
  only that a dependent claim must be rechecked.
- Hook state lives under `PLUGIN_DATA` when Codex supplies it, keyed by a hash
  of the project root. No transcript content is stored.

## Verification

`tests/test_hooks.py` runs the same contract against the Python and Windows
PowerShell implementations. It covers quoted and reordered destructive-Git
forms, compound shell commands, `--force-with-lease`, path warnings and strict
mode, claim staleness, and pre/post-compaction restoration.
