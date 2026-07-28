# `new-skill` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/new-skill/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `82cf90bbf203460b7744c87912cea315ace25ea25c0af61c06d70a51d9bc0e40`
- Target: `skills/new-skill/SKILL.md`
- Target SHA-256: `2c78a51d51c49af050aae0f615a8256c45f01614b00ebcc6741afaec66cb6943`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Preserved the attributed mattpocock design pattern while replacing the
  Claude surface with the current Codex skill creator.
- Limited frontmatter to `name` and `description`; added deterministic
  `agents/openai.yaml`, progressive-disclosure resources, and official
  validation.
- Replaced provider tool parity and slash-command table gates with
  capability, package, script, link, and forward-test gates.

## Behavior preserved

Name resolution, collision checks, design interview, small interface, deep
workflow, dry-run mode, and validated output remain.

## Behavior differences and loss

Claude-only metadata and repository table-row registration are not reproduced.
Plugin or repository discovery is handled by Codex-native package surfaces.
