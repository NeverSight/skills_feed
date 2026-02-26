---
name: solo-metrics-track
description: Set up PostHog metrics plan with event funnel, KPI benchmarks, and kill/iterate/scale decision thresholds. Use when user says "set up metrics", "track KPIs", "PostHog events", "funnel analysis", "when to kill or scale", or "success metrics". Do NOT use for SEO metrics (use /seo-audit).
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "📈"
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, mcp__solograph__kb_search
argument-hint: "<project-name>"
---

# /metrics-track

Set up a metrics tracking plan for a project. Defines PostHog event funnel, KPI benchmarks, and kill/iterate/scale decision thresholds based on lean startup principles.

## MCP Tools (use if available)

- `kb_search(query)` — find PostHog methodology, analytics patterns

If MCP tools are not available, fall back to Grep + Read.

## Methodology Reference

This skill implements metrics tracking based on lean startup principles:
- **Relative metrics vs niche benchmarks** — compare against your own trajectory, not vanity averages
- **Kill/iterate/scale decision rules** — data-driven thresholds for product decisions (see step 7 below)

## Steps

1. **Parse project** from `$ARGUMENTS`.
   - Read PRD for features, ICP, monetization model.
   - Read CLAUDE.md for stack (iOS/Web/both).
   - If empty: ask via AskUserQuestion.

2. **Detect platform:**
   - iOS app → PostHog iOS SDK events
   - Web app → PostHog JS SDK events
   - Both → cross-platform identity (shared user ID across platforms)

3. **Load PostHog methodology:**
   - If MCP available: `kb_search("PostHog analytics events funnel identity")`
   - Otherwise: check project docs for existing analytics configuration
   - Extract: event naming conventions, identity resolution, funnel pattern

4. **Define event funnel** based on PRD features:

   Standard funnel stages (adapt per product):
   ```
   Awareness → Acquisition → Activation → Revenue → Retention → Referral
   ```

   Map to concrete events:

   | Stage | Event Name | Trigger | Properties |
   |-------|-----------|---------|------------|
   | Awareness | `page_viewed` | Landing page visit | `source`, `utm_*` |
   | Acquisition | `app_installed` or `signed_up` | First install/signup | `platform`, `source` |
   | Activation | `core_action_completed` | First key action | `feature`, `duration_ms` |
   | Revenue | `purchase_completed` | First payment | `plan`, `amount`, `currency` |
   | Retention | `session_started` | Return visit (D1/D7/D30) | `session_number`, `days_since_install` |
   | Referral | `invite_sent` | Shared or referred | `channel`, `referral_code` |

5. **Forced reasoning — metrics selection:**
   Before defining KPIs, write out:
   - **North Star Metric:** The ONE number that matters most (e.g., "weekly active users who completed core action")
   - **Leading indicators:** What predicts the North Star? (e.g., "activation rate D1")
   - **Lagging indicators:** What confirms success? (e.g., "MRR", "retention D30")
   - **Vanity metrics to AVOID:** (e.g., total downloads without activation)

6. **Set KPI benchmarks** per stage:

   | KPI | Target | Kill Threshold | Scale Threshold | Source |
   |-----|--------|---------------|-----------------|--------|
   | Landing → Signup | 3-5% | < 1% | > 8% | Industry avg |
   | Signup → Activation | 20-40% | < 10% | > 50% | Product benchmark |
   | D1 Retention | 25-40% | < 15% | > 50% | Mobile avg |
   | D7 Retention | 10-20% | < 5% | > 25% | Mobile avg |
   | D30 Retention | 5-10% | < 2% | > 15% | Mobile avg |
   | Trial → Paid | 2-5% | < 1% | > 8% | SaaS avg |

   Adjust based on product type (B2C vs B2B, free vs paid, mobile vs web).

7. **Define decision rules** (lean startup kill/iterate/scale):

   ```markdown
   ## Decision Framework

   **Review cadence:** Weekly (Fridays)

   ### KILL signals (any 2 = kill)
   - [ ] Activation rate < {kill_threshold} after 2 weeks
   - [ ] D7 retention < {kill_threshold} after 1 month
   - [ ] Zero organic signups after 2 weeks of distribution
   - [ ] CAC > 3x LTV estimate

   ### ITERATE signals
   - [ ] Metrics between kill and scale thresholds
   - [ ] Qualitative feedback suggests product-market fit issues
   - [ ] One stage of funnel is dramatically worse than others

   ### SCALE signals (all 3 = scale)
   - [ ] Activation rate > {scale_threshold}
   - [ ] D7 retention > {scale_threshold}
   - [ ] Organic growth > 10% week-over-week
   ```

8. **Generate PostHog implementation snippets:**

   ### For iOS (Swift):
   ```swift
   // Event tracking examples
   PostHogSDK.shared.capture("core_action_completed", properties: [
       "feature": "scan_receipt",
       "duration_ms": elapsed
   ])
   ```

   ### For Web (TypeScript):
   ```typescript
   // Event tracking examples
   posthog.capture('signed_up', {
       source: searchParams.get('utm_source') ?? 'direct',
       plan: 'free'
   })
   ```

9. **Write metrics plan** to `docs/metrics-plan.md`:

   ```markdown
   # Metrics Plan: {Project Name}

   **Generated:** {YYYY-MM-DD}
   **Platform:** {iOS / Web / Both}
   **North Star:** {north star metric}

   ## Event Funnel

   | Stage | Event | Properties |
   |-------|-------|------------|
   {event table from step 4}

   ## KPIs & Thresholds

   | KPI | Target | Kill | Scale |
   |-----|--------|------|-------|
   {benchmark table from step 6}

   ## Decision Rules

   {framework from step 7}

   ## Implementation

   ### PostHog Setup
   - Project: {project name} (EU region)
   - SDK: {posthog-ios / posthog-js}
   - Identity: {anonymous → identified on signup}

   ### Code Snippets
   {snippets from step 8}

   ## Dashboard Template
   - Funnel: {stage1} → {stage2} → ... → {stageN}
   - Retention: D1 / D7 / D30 cohort chart
   - Revenue: MRR trend + trial conversion

   ---
   *Generated by /metrics-track. Implement events, then review weekly.*
   ```

10. **Output summary** — North Star metric, key thresholds, first event to implement.

## Notes

- PostHog EU hosting for privacy compliance
- Use `$set` for user properties, `capture` for events
- Identity: start anonymous, `identify()` on signup with user ID
- Cross-platform: same PostHog project, same user ID → unified journey
- Review dashboard weekly, make kill/iterate/scale decision monthly

## Common Issues

### Wrong platform detected
**Cause:** Project has both web and iOS indicators.
**Fix:** Skill checks package manifests. If both exist, it generates cross-platform identity setup. Verify the detected platform in the output.

### KPI thresholds too aggressive
**Cause:** Default thresholds are industry averages.
**Fix:** Adjust thresholds in `docs/metrics-plan.md` based on your niche. B2B typically has lower volume but higher conversion.

### PostHog SDK not in project
**Cause:** Metrics plan generated but SDK not installed.
**Fix:** This skill generates the PLAN only. Install PostHog SDK separately: `pnpm add posthog-js` (web) or add `posthog-ios` via SPM (iOS).
