# Shared-resource conversion

- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Status: `validated`
- Inventory: 9 reference(s), 32 rule(s), 21 template(s)

Every rule is classified as a native rewrite because provider routing and
runtime assumptions were replaced with explicit Codex applicability. Each
reference and template retains its own direct-port, native-rewrite, or
retained-reference classification. Per-component classifications, revision
summaries, source/target paths, and hashes are recorded in
`SOURCE_MANIFEST.json`.

## Material revisions

- Converted rule glob frontmatter into an explicit applicability section and generated `references/rules/INDEX.md`.
- Rewrote skill invocations and Claude runtime paths for Codex.
- Replaced the provider-specific model-version table with durable Codex routing principles.
- Retained the upstream backlog as historical conversion evidence.
- Reimplemented the invalid Claude skill template as a Codex skill template while directly porting the remaining academic templates.
- Made template provenance comments extension-aware: TeX uses `%`, YAML uses
  `#`, and Markdown uses HTML comments.
- Preserved `$skill` in Quarto code spans and escaped it as `\$skill` when
  typeset by TeX.

## Known behavior difference

Codex does not auto-route arbitrary glob frontmatter from plugin reference files. Applicable skills and project `AGENTS.md` files must load matching rules from the generated index.
