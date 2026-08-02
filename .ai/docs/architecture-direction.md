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

- Exact sensitive-path heuristic list (define during MVP implementation goal)
- Whether to use `git` subprocess only vs. a thin library wrapper (prefer
  subprocess for minimal deps unless library clearly wins)
