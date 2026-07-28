## Summary

<!-- What changed and why? -->

## Portability and research safety

- [ ] No provider-only runtime dependency was introduced.
- [ ] External actions still require explicit authorization.
- [ ] Missing evidence or unavailable tools are reported as UNVERIFIED.
- [ ] Data, citation, inference, and disclosure safeguards are preserved.
- [ ] Attribution and source hashes are updated when applicable.

## Verification

- [ ] `python scripts/validate_package.py --release`
- [ ] `python -m unittest discover -v`
- [ ] Changed skills pass Codex `quick_validate.py`
- [ ] Complex behavior received a representative forward test
- [ ] Rendered artifacts were visually inspected when applicable

## Remaining limitations

<!-- State unresolved or deliberately unsupported behavior. -->
