# Python CLI Stack Profile

Stack-specific guidance for diffstat-cli. Global workflow rules still apply.

## Common structure

```txt
src/diffstat/
tests/
pyproject.toml
README.md
```

## Project commands

```bash
python -m pip install -e ".[dev]"
pytest
ruff check src tests
diffstat --help
diffstat analyze --help
diffstat analyze --json
```

Optional when mypy is installed:

```bash
mypy src
```

## Testing expectations

- Unit tests for changed modules
- CLI tests for new flags or commands
- Snapshot tests only when stable output is intentional

## Documentation expectations

- Update CLI help text and README when commands change
- Document config and flags in README or `.ai/docs/`

## AI-specific risks

- Packaging and entry-point misconfiguration
- Silent exception swallowing in CLI paths
- Breaking stdout/stderr contracts used by scripts
- Adding dependencies without lockfile update
- Path and filesystem assumptions across OS environments

## What agents should avoid

- Broad `ruff format` on unrelated modules
- Changing `pyproject.toml` optional deps without justification
- Executing arbitrary shell from CLI without sandbox review
- Bundling library API changes with CLI-only tasks
- Committing virtualenvs or local `.env` files

## References

- `.ai/workflows/test-writing.md`
- `.ai/policies/security-policy.md`
