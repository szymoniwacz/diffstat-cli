# Project Requirements

## Purpose

Requirements for diffstat-cli — a local-first CLI that reports git diff churn and
review-risk signals.

## Project summary

diffstat-cli helps developers and reviewers quickly judge whether a local git
change set is large or risky before reading every line. Users point the tool at a
working tree or commit range and receive a human-readable summary or JSON report
with totals, per-file churn, hotspots, and a deterministic review-risk ranking.

The first useful version is installable from this repository, runs offline against
local git, and supports scriptable exit codes and stdout/stderr contracts.

## Users

| User | Needs | Notes |
|---|---|---|
| Developer | Size local changes before push | Primary CLI user |
| Reviewer | Prioritize large or sensitive diffs | Text summary |
| CI job | Fail or warn on oversized diffs | JSON output |

## Problems to solve

- Change sets are hard to judge without structured metrics
- Reviewers lack a quick risk signal before deep review
- CI lacks a simple deterministic diff-size gate

## Goals

- Installable `diffstat` CLI for local git analysis
- Text and JSON reports with stable ordering
- Documented review-risk heuristics
- Clear errors for invalid input

## Non-goals

- Remote git platform APIs
- Web UI, SaaS, LLM summarization
- Network dependency for core analysis

## Core workflows

### Workflow 1 — Analyze local diff

1. User installs the package and runs `diffstat` against a repo path
2. CLI resolves git context (working tree or range)
3. CLI prints summary or JSON; non-zero exit on errors

### Workflow 2 — CI size gate

1. CI clones repo and runs `diffstat` with JSON output
2. Job parses totals and applies threshold policy
3. Job fails or warns based on configured limits

## Functional requirements

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| FR-001 | Analyze local git working tree or range | must | MVP |
| FR-002 | Human-readable summary output | must | MVP |
| FR-003 | JSON report output | must | Stable ordering |
| FR-004 | Review-risk score or ranking | must | Documented heuristics |
| FR-005 | Clear errors for invalid/empty input | must | Non-zero exit |

## Data and inputs

| Input | Source | Format | Notes |
|---|---|---|---|
| Git repo path | CLI flag or cwd | filesystem path | Local only |
| Commit range | CLI flags | git ref syntax | e.g. `main..HEAD` |
| Working tree | default mode | git index | Uncommitted |

## Outputs

| Output | Consumer | Format | Notes |
|---|---|---|---|
| Summary report | Human reviewer | text | stdout |
| Machine report | CI / scripts | JSON | stdout |
| Errors | Shell / CI | stderr | Non-zero exit |

## Integrations

| Integration | Purpose | Required now? | Notes |
|---|---|---|---|
| Local `git` | Diff source | yes | subprocess or library |
| Hosted git APIs | Remote PR fetch | no | Out of scope |

## Constraints

- Local-first; core analysis offline
- Deterministic output for same git input
- Python 3.11+; minimal dependencies
- Scriptable flags and exit codes

## Technical preferences

- Python CLI per `.ai/stack-profiles/python-cli.md`
- `src/diffstat/` package layout
- `pytest`, `ruff`, optional `mypy` for quality

## Active stack profile

| Active profile | Applies to | Notes |
|---|---|---|
| .ai/stack-profiles/python-cli.md | CLI package, tests, tooling | diffstat-cli commands recorded in profile |

## Quality requirements

- Unit tests for changed modules; CLI tests for commands
- `ruff check` on Python sources
- CI runs validator and fixture tests on PRs and main

## Security and privacy requirements

- No secrets in repo; no network for core analysis
- Diff content processed locally only

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Git edge cases | Wrong stats | Tests on common ref formats |
| Large repos | Slow runs | Document scope; optimize later |
| Sensitive path heuristics wrong | Mis-ranked risk | Document rules; tune in follow-ups |

## Assumptions

| Assumption | Why it matters | Confirm by |
|---|---|---|
| `git` available on PATH | Core input source | MVP docs and tests |
| Python 3.11+ on dev/CI | Runtime | pyproject.toml, CI |

## Open questions

- [ ] None blocking MVP after bootstrap

## First useful version

Installable CLI that analyzes a local git diff and prints text + JSON reports with
review-risk ranking and clear errors.

## Later versions

Configurable risk rules, extra output formats, performance tuning for huge repos.

## Project decision status

| Area | Status | Value / notes | Link / location / return trigger |
|---|---|---|---|
| Product purpose | decided | Local-first git diff stats and review signals | `.ai/project/vision.md` |
| Users | decided | Developers, reviewers, CI jobs | `.ai/docs/project-requirements.md` |
| Outcomes | decided | Faster sizing and risk triage | `.ai/project/vision.md` |
| Success criteria | decided | MVP criteria in parent issue #1 | GitHub issue #1 |
| First useful version | decided | Local analyze + text + JSON | `.ai/project/roadmap.md` Phase 2 |
| Non-goals | decided | No remote APIs, UI, LLM | `.ai/project/scope.md` |
| Interfaces | decided | CLI `diffstat` with flags | README.md |
| Inputs and outputs | decided | Git paths/ranges in; text/JSON out | This document |
| Architecture shape | decided | CLI → git → parse → report | `.ai/docs/architecture-direction.md` |
| Boundaries | decided | CLI owns reporting; git owns diffs | `.ai/docs/architecture-direction.md` |
| Storage and data ownership | not-applicable | No persistent store in MVP | Ephemeral stdout only |
| Retention and migrations | not-applicable | No stored data | |
| Integrations and failure handling | decided | Local git only; clear stderr on failure | FR-005 |
| Authentication and authorization | not-applicable | No auth in local CLI | |
| Secrets, privacy, and sensitive data | decided | No secrets; local diff only | `.ai/policies/security-policy.md` |
| Language, framework, and dependencies | decided | Python 3.11+, minimal deps | `pyproject.toml` |
| Environments and deployment | decided | pip install; GitHub Actions CI | README.md |
| Configuration | decided | CLI flags only for MVP | README.md |
| Logging, monitoring, and errors | decided | stderr + exit codes | FR-005 |
| Tests, lint, typecheck, performance | decided | pytest, ruff; perf deferred | README.md |
| Scale, reliability, and cost | deferred | Large-repo perf unknown | Revisit Phase 3 roadmap |
| Supported platforms and compatibility | decided | Linux/macOS dev; git 2.x | README.md |
| Accessibility and localization | not-applicable | CLI text tool; English MVP | |
| Compliance, backup, and recovery | not-applicable | No persistent data | |
| Branching, CI, release, and rollback | decided | PR to main; CI on PR and main | `.ai/git/branch-and-pr-workflow.md` |
| License, ownership, and documentation expectations | decided | MIT; Szymon Iwacz; README + .ai docs | LICENSE |

## Project readiness

| Check | Result | Notes |
|---|---|---|
| Definition coverage complete | pass | All decision areas recorded above |
| No `blocking-question` remains | pass | No open blocking rows |
| All `deferred` items have reason and return trigger | pass | Scale deferred to Phase 3 |
| Template customization complete | pass | README, AGENTS, project docs updated |
| Stack profile selected or marked N/A | pass | `.ai/stack-profiles/python-cli.md` |
| Real project commands recorded | pass | Commands in README.md and python-cli profile |
| Root README describes the product | pass | Product-facing README.md |
| `AGENTS.md` describes repository role | pass | Product repository role recorded |
| Bootstrap markers removed | pass | No bootstrap placeholder markers in product files |
| License and ownership decided | pass | MIT; Szymon Iwacz in LICENSE |
| CI, branch rules, and approvals decided | pass | PR workflow; validate-workflow-contracts CI |
| Project ready for first product task | yes | Bootstrap goal #2 completes readiness |
