# diffstat-cli

Local-first command-line tool for git diff churn statistics and review-risk
signals.

## Purpose

Help developers and reviewers quickly judge whether a local git change set is
large or risky before reading every line. Suitable for interactive use and CI
pipelines that need deterministic JSON output.

## Status

Core MVP analyze command is available (roadmap Phase 2).

## Setup

Requires Python 3.11+ and `git` on PATH.

```bash
python -m pip install -e ".[dev]"
```

## Run

```bash
diffstat --help
diffstat analyze --help
```

### Analyze working tree (vs HEAD)

Includes staged and unstaged changes:

```bash
diffstat analyze
diffstat analyze --path /path/to/repo
```

### Analyze a commit range

```bash
diffstat analyze --base main --head HEAD
diffstat analyze --base HEAD~1 --head HEAD --json
```

### Output

- Default: human-readable text on stdout (totals, languages, hotspots, files,
  review-risk).
- `--json`: machine-readable JSON (`schema_version: 1`) with stable key ordering.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Report produced for a non-empty diff |
| 1 | Empty diff (no file changes) |
| 2 | Usage / path / not a git repository |
| 3 | Invalid git range or git command failure |

Errors are written to stderr.

## Review-risk heuristics

Deterministic score from 0–100 with levels `low` (0–24), `medium` (25–59),
`high` (60–100):

- Churn (added + deleted lines), up to 40 points
- Files changed, up to 30 points
- Sensitive-path matches, up to 30 points

Sensitive-path rules (case-insensitive) include substrings such as `.env`,
`id_rsa`, `credentials`, `secret`, `passwd`, `password`, `/auth/`, `token`,
`private_key`, and suffixes `.pem`, `.key`, `.p12`, `.pfx`.

## JSON schema (v1)

Top-level keys: `schema_version`, `tool`, `mode`, `repo`, `range`, `totals`,
`languages`, `files`, `hotspots`, `review_risk`.

`totals` includes `files_changed`, `lines_added`, `lines_deleted`,
`total_churn`. `review_risk` includes `score`, `level`, `reasons`,
`sensitive_files`. Files are ordered sensitive-first, then by churn, then path.

## Tests and quality

```bash
pytest
ruff check src tests
```

## Configuration and environment variables

No environment variables required. Flags only for MVP.

## Architecture and context

- `.ai/project/product-context.md`
- `.ai/project/scope.md`
- `.ai/docs/architecture-direction.md`

## Working system

This repository uses `.ai/` as its working system. See `.ai/docs/template-flow.md`
for contributor workflow. This README stays product-focused.

## Limitations

- No remote git platform integration in MVP
- Risk rules are fixed heuristics (not yet configurable)
- Large-repo performance not yet optimized

## License

MIT — see `LICENSE` (Copyright Szymon Iwacz).

## Contact and contributions

Maintainer: Szymon Iwacz. Open issues or PRs on GitHub.
