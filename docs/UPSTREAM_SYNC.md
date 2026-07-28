# Upstream synchronization

The source fork lives at `C:\GitHub\claude-code-my-workflow`.

## Remote contract

- `origin`: `https://github.com/dipietra/claude-code-my-workflow.git`
- `upstream`: `https://github.com/pedrohcgs/claude-code-my-workflow.git`

## Review-first update procedure

1. Check the fixed clone and the locally visible upstream ref:

   ```powershell
   .\scripts\maw.cmd source-status
   ```

2. When network access is authorized, fetch upstream refs without merging:

   ```powershell
   .\scripts\maw.cmd source-status --fetch
   ```

   The checker validates the exact `origin`, `upstream`, `main` branch,
   baseline commit, tag, and clean working tree. `--fetch` changes only remote
   refs and reports how many commits are available for review; it never merges
   or moves the conversion baseline.

3. Identify the new upstream tag or commit.
4. Compare it with the commit in
   `docs/conversion/SOURCE_BASELINE.md`.
5. Generate a changed-component list for skills, agents, rules, hooks,
   templates, scripts, and project guidance.
6. Classify each delta as direct port, native rewrite, composed replacement,
   retained reference, or unsupported.
7. Port reviewed changes only into `C:\Codex\mawcodex`.
8. Update source hashes, per-component revision records, attribution, and the
   stability matrix.
9. Run the full validation suite before advancing the baseline.

Do not merge upstream directly into MAW Codex. The repositories intentionally
have different runtimes and layouts.
