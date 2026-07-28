# `learn` conversion

- Status: `validated`
- Classification: `native rewrite`
- Source: `.claude/skills/learn/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `29ffe046877f096f43dcf1070291594c08905f40ad2a3400fc2121d5e6bcd446`
- Target: `skills/learn/SKILL.md`
- Target SHA-256: `1f1b7949ba9e391249c66b2d0c7b285559a152f31e08d8eddc3e2fb2e4240d78`
- Validation: `PASS` — official skill validator, native-residue scan, and relative-link check
- Forward test: not selected for the representative 1.0 matrix; semantic and structural validation PASS
## Material revisions

- Routed new-skill initialization, UI metadata, and validation through the
  active Codex `$skill-creator`.
- Replaced `.claude` discovery and unsupported metadata with current
  `skills/`, two-field frontmatter, and `agents/openai.yaml`.
- Added evidence, overlap, confidentiality, target-location, and external
  publication gates.

## Behavior preserved

The workflow still converts a verified, non-obvious session discovery into a
reusable skill after checking for overlap.

## Behavior differences and loss

Author/version metadata and Claude-specific scaffolding are intentionally
absent. A missing official initializer remains `UNVERIFIED`.
