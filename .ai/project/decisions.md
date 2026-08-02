# Decisions

## Purpose

This file is a lightweight decision log and ADR index.

Record short decisions here directly.
For significant architecture decisions, create a full ADR in `.ai/architecture/` and link it below.

The goal is not bureaucracy.
The goal is memory.

## Decision log

### 2026-08-02 — Python CLI stack for diffstat-cli

**Decision:** Use Python 3.11+ with `src/diffstat/` layout, `pytest` and `ruff`
for quality, and local `git` for diff input. Minimal dependencies for MVP.

**Kept:** local-first analysis, deterministic output, scriptable CLI contracts.

### 2026-08-01 — Self-correcting `auto-merge` option

**Decision:** Squash merge by Goal Executor requires an explicit
`auto-merge` suffix on top of self-correcting review:

- `/execute-goal self-correcting-review auto-merge`
- `/execute-project self-correcting-review auto-merge`

Bare `self-correcting-review` still skips human CR when eligible but leaves
merge to a human.

**Kept:** material-decision, dangerous-action, and high/security-sensitive stops;
default modes still never agent-merge; no GitHub auto-merge queue; no
force-push or protection bypass.

**Supersedes:** idea 001 “human merge still mandatory / auto-merge out of
scope”. See `.ai/ideas/implemented/002-self-correcting-auto-merge.md`.

> Reusable workflow rules (for example, documentation before implementation)
> live in the canonical workflow documents under `.ai/`, not in this product
> decision log.

## Architecture decision index

Link full ADRs here when they exist.

| ADR | File | Status |
|---|---|---|
| — | — | — |
