# Roadmap

## Purpose

Phases for diffstat-cli from bootstrap through MVP.

## Phase 1 — Bootstrap and readiness

Goal:
Customize the repository away from the AI workflow template and pass project
readiness.

Outputs:

- Product-facing README and AGENTS.md
- Filled project docs and decision-status table
- Python packaging scaffold (`pyproject.toml`, `src/diffstat/`, `tests/`)
- CI contract validation in project mode

## Phase 2 — Core CLI MVP

Goal:
Ship installable `diffstat` with analyze, text summary, and JSON output for
local git diffs.

Outputs:

- `diffstat analyze` (or equivalent) for working tree and commit ranges
- Human-readable summary (totals, per-file churn, hotspots)
- JSON report with stable ordering
- Review-risk score or ranking (documented heuristics)
- Clear exit codes for error paths
- Tests for happy path and main errors

## Phase 3 — Hardening and CI integration

Goal:
Polish UX, expand edge-case coverage, and document CI usage patterns.

Outputs:

- Additional error-path tests and docs
- Example CI job snippets for size/risk gates
- Performance sanity checks on large repos

## Later phases

- Optional path filters and configurable risk rules
- Additional output formats only when a concrete need appears
