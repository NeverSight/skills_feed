---
name: marketing-ops
description: |
  Marketing workflow orchestrator. Composes primitives for pSEO launches, GitHub releases, ad campaigns, and growth tracking.
  Use when: launching pSEO pages, announcing releases, running campaigns, tracking marketing metrics across tools.
  Keywords: marketing workflow, launch, campaign, pSEO, release, announce, metrics
effort: high
---

# /marketing-ops

> You orchestrate. Primitives do the work.

## Your Primitives

| Primitive | Purpose | Invocation |
|-----------|---------|------------|
| pseo-generator | Generate pages at scale | `./scripts/generate.py` |
| github-marketing | OSS distribution | Knowledge skill |
| ads-cli | Campaign management | `./cli.py` |
| marketing-dashboard | Metrics | `./dashboard.py` |
| announce | Social posts | /announce skill |
| post | Quick tweets | /post skill |

## Workflows

### 1. pSEO Launch
Goal: Generate pages → validate → submit to GSC → track.
1. Run pseo-generator: init, generate, validate
2. Deploy (Vercel/manual)
3. Submit sitemap to GSC
4. Track indexation in marketing-dashboard

### 2. GitHub Release  
Goal: Ship → announce → track.
1. Tag release, generate changelog
2. Run /announce for social posts
3. Track traffic spike in marketing-dashboard

### 3. Ad Campaign
Goal: Launch → monitor → optimize.
1. Use ads-cli to create campaign
2. Run marketing-dashboard ads --period 7d daily
3. Adjust budget based on CPA

### 4. Growth Check
Goal: Weekly marketing health.
1. marketing-dashboard status
2. marketing-dashboard seo --period 7d
3. marketing-dashboard revenue --period 30d

## Your Role

Don't execute primitives yourself. You:
1. Route — Pick the right primitive
2. Sequence — Order operations correctly  
3. Monitor — Check outputs between steps
4. Report — Summarize results

## Related Skills

- /delegate — General orchestration pattern
- /launch-strategy — Launch planning
- /growth-sprint — Weekly growth ritual
