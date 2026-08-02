# Glossary

## Terms

### Churn

Lines added and removed in a diff, aggregated per file and in totals.

### Hotspot

A file or path with disproportionately high churn relative to the change set.

### Review risk

A deterministic score or ranking derived from churn, number of changed files,
and sensitive-path heuristics (documented in product docs).

### Working tree diff

Uncommitted changes in a local git repository (`git diff` scope).

### Commit range

A sequence of commits between two refs (e.g. `main..HEAD` or explicit SHAs).

### Machine report

JSON output with stable field ordering suitable for CI and scripts.

### Project context

Minimum information to understand what diffstat-cli is, its phase, and constraints.

### Quality gate

A check that must pass before work is considered complete (tests, lint, CI, docs).

### Working system

The reusable `.ai/` structure for planning, documenting, and executing work.
