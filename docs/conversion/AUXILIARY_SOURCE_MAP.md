# Auxiliary fixed-source coverage

Source boundary: upstream commit
`be53c12f235996dff41fb7f21580506fd2dd8d50` (`v2.1.0`).

The component, project-template, and runtime-surface manifests cover 163 of
the fixed source repository's 211 tracked files. The remaining 48 files are
repository support rather than skills, agents, rules, references, artifact
templates, or provider runtime surfaces. They are still given an explicit
disposition in `AUXILIARY_SOURCE_MANIFEST.json`, so no fixed-source file is
silently ignored.

## Disposition groups

| Source group | Treatment |
| --- | --- |
| GitHub governance and CI | Rewritten for the independent MAW Codex repository; automatic guide deployment becomes the explicit `$deploy` workflow. |
| Root README, changelog, citation, license, and troubleshooting | Rewritten or directly retained in package documentation, citation, license, notices, installation guidance, and limitations. |
| Empty project-directory markers | Directly retained in the project template or replaced by reviewed starter content in the same directory. |
| Git hook, ignore policy, memory, and editor configuration | Rewritten as safe project assets; editor-specific permission behavior is explicitly unsupported. |
| Generated guide and deployed HTML | Replaced by directly maintained README, installation, and conversion documentation. |
| Source maintenance scripts | Rewritten as cross-platform validators, project helpers, or explicit Codex workflows. |

## Behavior loss

- The generated standalone guide site is not shipped or auto-deployed.
- VS Code/provider permission configuration is not reproduced.
- Shell wrappers whose only purpose was provider validation or documentation
  synchronization are replaced, not emulated.
- Empty markers are omitted where the target directory already contains a
  reviewed starter file.

These losses are deliberate and do not remove academic workflow behavior.
Every record retains the fixed source hash, allowed classification, current
target hashes, and a per-file revision summary.
