# Product Context

## Project identity

- **Project name:** diffstat-cli
- **Project type:** local-first CLI for git diff statistics and review signals
- **Target users:** developers sizing PRs; reviewers prioritizing work; CI jobs
  gating oversized diffs
- **Core problem:** change sets are hard to judge quickly without structured
  churn and risk metrics
- **Current phase:** MVP hardening (Phase 3 — CI quality gates and usage docs)
- **Important constraints:** offline core analysis, deterministic output,
  scriptable UX, minimal dependencies

## Current phase

MVP hardening (Phase 3)

## Working assumptions

- Documentation and project readiness precede product features
- Changes stay small and reviewable (one goal per PR)
- Core analysis uses local `git` only; no network for MVP
- Python 3.11+ with minimal dependencies
- Human or authorized auto-merge after review per repository policy

## Out of scope

- GitHub/GitLab remote PR fetch by number
- Web UI, desktop app, hosted backends
- Auth, multi-tenant storage, LLM features
- Rewriting the AI workflow template beyond bootstrap customization

## Links to important files

- `.ai/project/scope.md`
- `.ai/project/roadmap.md`
- `.ai/project/decisions.md`
- `.ai/docs/project-requirements.md`
- `.ai/docs/architecture-direction.md`
