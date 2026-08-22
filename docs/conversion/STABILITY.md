# Stability matrix

Current target: `1.2.1` stable.

| Gate | Required result | Current result |
| --- | --- | --- |
| Plugin manifest | PASS | PASS |
| Skill inventory | 58/58 | PASS |
| Skill structure | 58/58 PASS | PASS |
| Skill semantic review | 52/52 source-derived plus 6 ManageRAW additions | PASS |
| Custom agents | 19/19 parse and map | PASS |
| Adapted rules | 32/32 indexed | PASS |
| Enabled hooks | schema-valid and fail-safe | PASS |
| Attribution | complete | PASS |
| Provider residue | no operational Claude dependencies | PASS |
| Source and target provenance | all recorded hashes current | PASS |
| Provider runtime surfaces | 13/13 mapped and hash-bound | PASS |
| Fixed-source file coverage | 211/211 exactly once | PASS |
| Representative forward tests | all required scenarios PASS | PASS |
| Deterministic unit tests | all local tests PASS | PASS |
| Official Codex validators | plugin and 58 skills PASS | PASS |
| Known limitations | documented, no blockers | PASS |
| Public-site structure | static site, legal pages, and Pages workflow present | PASS |

The evidence behind this matrix is in `OFFICIAL_VALIDATION.json`,
`FORWARD_TEST_RESULTS.json`, and `RELEASE_REPORT.md`. The stable claim covers
the package and its safety contracts; operations that require optional
academic runtimes or institution-specific clearance retain their documented
`UNVERIFIED` boundary until run in the target project.
