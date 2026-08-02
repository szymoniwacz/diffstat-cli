# diffstat-cli

Local-first command-line tool for git diff churn statistics and review-risk
signals.

## Purpose

Help developers and reviewers quickly judge whether a local git change set is
large or risky before reading every line. Suitable for interactive use and CI
pipelines that need deterministic JSON output.

## Status

Bootstrap complete; MVP implementation in progress (see `.ai/project/roadmap.md`).

## Current capabilities

- Installable Python package scaffold (`diffstat` entry point with `--help`)
- Project documentation and CI contract validation in project mode
- Product behavior (analyze, summary, JSON) not yet implemented

## Setup

Requires Python 3.11+ and git on PATH.

```bash
python -m pip install -e ".[dev]"
```

## Run

```bash
diffstat --help
```

Analyze commands ship in the MVP phase (see roadmap Phase 2).

## Tests and quality

```bash
pytest
ruff check src tests
```

Optional type checking when configured:

```bash
mypy src
```

## Configuration and environment variables

No environment variables required for bootstrap. MVP may add optional flags only.

## Architecture and context

- `.ai/project/product-context.md`
- `.ai/project/scope.md`
- `.ai/docs/architecture-direction.md`

## Working system

This repository uses `.ai/` as its working system. See `.ai/docs/template-flow.md`
for contributor workflow. This README stays product-focused.

## Limitations

- No remote git platform integration in MVP
- Core analysis not yet implemented (bootstrap scaffold only)
- Large-repo performance not yet optimized

## License

MIT — see `LICENSE` (Copyright Szymon Iwacz).

## Contact and contributions

Maintainer: Szymon Iwacz. Open issues or PRs on GitHub.
