# Project Vision

## One-sentence vision

diffstat-cli is a local-first command-line tool for developers and reviewers that
helps size git change sets and spot review-risk signals before reading every line.

## Problem

Pull requests and local commits vary widely in size and risk. Reviewers waste
time opening large or sensitive diffs without a quick signal. CI jobs lack a
simple, deterministic way to warn or fail on oversized changes.

## Desired outcome

After diffstat-cli exists, a contributor can point the CLI at a local git
repository and immediately see churn totals, per-file breakdowns, hotspots, and
a documented review-risk ranking — in human text or machine JSON — without
network access.

## Non-goals

- Hosted git platform APIs, web UI, or SaaS dashboards
- LLM summarization of diffs
- Cloud services or paid APIs for core analysis
