# `respond-to-referees` conversion

- Status: `forward-tested`
- Classification: `native rewrite`
- Source: `.claude/skills/respond-to-referees/SKILL.md`
- Source commit: `be53c12f235996dff41fb7f21580506fd2dd8d50`
- Source SHA-256: `72fc31572fdff3f2bc0075c16d9af846c5c1cd288cd569a986bf5acae7f274e4`
- Target: `skills/respond-to-referees/SKILL.md`
- Target SHA-256: `c6e98daefd6f01ca6b03325b6798f956dad379af6f87b07f645732ffaf7c4f34`
- Validation: `PASS`
- Forward test: PASS (FT-14)
## Material revisions

- Replaced positional arguments and provider tools with semantic input and
  extraction capabilities.
- Made the fresh-context claim-verification fallback explicit and repaired rule
  and template links.
- Added UNVERIFIED behavior and an external-submission authorization boundary.

## Behavior preserved

Every referee concern is classified, located in the revision, drafted
courteously, summarized in a matrix, and independently checked before use.

## Behavior loss or limitation

No fixed extractor is guaranteed; non-text conversion depends on the local
runtime. End-to-end execution against real referee files remains pending.
