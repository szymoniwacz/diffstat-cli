# Scope

## Purpose

Define what is currently allowed and what is intentionally deferred for
diffstat-cli.

## In scope now

- Bootstrap and project readiness (completed via goal #2)
- Local git diff analysis CLI (`diffstat` command)
- Human-readable summary and JSON report output
- Review-risk scoring from churn, file count, and sensitive-path heuristics
- Error handling for invalid repos, ranges, and empty diffs
- Automated tests, lint, and CI for the Python package
- Documentation for install, commands, and limitations

## Out of scope by default

- Hosted git platform API integrations
- Web UI, SaaS, or desktop applications
- LLM or AI summarization
- Network calls required for core analysis
- Large rewrites without explicit approval
- New frameworks without a decision record

## Scope levels

| Level | Meaning |
|---|---|
| Idea | rough concept only |
| Expanded idea | clear problem, goal, scope, risks |
| Ready for planning | packet or brief complete enough to plan |
| Planned | implementation plan exists in `.ai/plans/` |
| Implementation-ready | full gate passed; work may change files |
| Implemented | code exists and docs were updated |
| Archived | intentionally rejected or deferred |

## Rule

If a task changes scope, update this file or add a decision record before continuing.
