# Architecture Direction

## System shape

Local-first Python CLI (`diffstat`) that shells out to or invokes `git` for diff
data, parses churn statistics, applies deterministic review-risk heuristics, and
formats text or JSON reports.

## Main boundaries

| Component | Responsibility |
|---|---|
| CLI layer | Argument parsing, exit codes, stdout/stderr contracts |
| Git adapter | Resolve repo, ranges, and raw diff stats from local git |
| Analysis | Aggregate churn, hotspots, per-file breakdown |
| Risk engine | Deterministic score from churn, file count, path heuristics |
| Reporters | Human text and JSON serializers with stable ordering |

## Design principles

- Simple first version: one primary analyze command path
- Explicit boundaries between git IO, analysis, and output
- Deterministic core: stable sort order in text and JSON
- Small reviewable changes per goal
- No network calls in core analysis path

## Open questions

- None blocking MVP after Phase 2 core CLI

## Resolved during Phase 2

- Sensitive-path heuristics: documented in README (substring/suffix list)
- Git access: `git` subprocess only (no extra runtime dependency)

