# Effective precedence report

Compute precedence for one concrete target path at a time.

## Instruction chain

Report the chain in this order:

1. Higher-authority runtime instructions.
2. Global and project guidance from broadest scope toward the target path.
3. The user's requested outcome and compatible explicit authorization.
4. Project Codex configuration applicable to the trusted repository.
5. The invoked skill's bounded workflow instructions.
6. Shared MAW routing records.
7. Personal preferences that do not conflict with the layers above.

Deeper project guidance specializes its own subtree. It does not supersede
higher-authority runtime instructions or extend outside that subtree.

## Report schema

```text
Target path:
Working directory:
Project root:
Applicable instruction files, broadest to closest:
Applicable project configuration:
Invoked skills:
Effective requirements:
Shadowed or narrowed requirements:
Conflicts:
Personal-only settings omitted from shared state:
Verdict: CLEAR | CONFLICT | UNVERIFIED
```

For every conflict, quote or precisely paraphrase both instructions and name
the files or authority levels involved. Do not report `CLEAR` when an
applicable file could not be read.

Test at least one representative path per instruction subtree after a change,
plus one sibling path to confirm the nested rule does not leak.
