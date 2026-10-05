# Daily Dev Log

[![Daily learning entry](https://github.com/nur667-7/daily-dev-log/actions/workflows/daily.yml/badge.svg)](https://github.com/nur667-7/daily-dev-log/actions/workflows/daily.yml)

A small, deterministic learning journal maintained by GitHub Actions. Every day it adds one dated software-development prompt to [`data/daily`](data/daily) and refreshes [`data/latest.json`](data/latest.json).

## What the automation does

- Runs every day at **00:23 UTC** on GitHub-hosted infrastructure.
- Generates a short concept, practice challenge, and reflection question.
- Creates at most one entry for each UTC calendar day.
- Commits only when generated content changed.
- Supports a manual run from the Actions tab.

## Run locally

```bash
python generate_daily.py
```

Generate a specific date:

```bash
python generate_daily.py --date 2026-10-05
```

The generator uses only the Python standard library.

> **Automation notice:** entries and commits ending in `[bot]` are generated automatically by the scheduled workflow. They are intentionally labeled so the repository's activity is transparent.
