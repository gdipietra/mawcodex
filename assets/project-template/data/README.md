# Data roles

- `raw/`: immutable inputs or small public examples. Restricted data should
  remain in its approved environment and be represented here only by access
  documentation.
- `derived/`: reproducibly generated analysis inputs. Every file must have a
  creating script and documented upstream source.

Never edit a raw file in place. Record checksums or source-version identifiers
when feasible.
