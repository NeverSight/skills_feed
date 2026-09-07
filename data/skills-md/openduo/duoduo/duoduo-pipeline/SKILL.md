---
name: duoduo-pipeline
description: "Build event-driven pipelines that connect a zero-LLM mechanical layer to a duoduo brain job via session notify. Use when the user wants to monitor an external data source (feeds, prices, files, webhooks) and only wake an agent when something worth acting on actually arrives — keeping LLM costs at zero during idle periods. Also trigger for: 机械采集, 事件驱动, 按需唤醒, 数据监控, keepalive job, 外部触发, 只在有料时干活, 省 token."
---

# Duoduo Pipeline

Connect a zero-cost mechanical layer to a duoduo brain job so the LLM
only runs when there is something worth acting on. During idle periods the
brain job stays dormant — no polling, no token spend.

## The three-layer model

```
Mechanical layer  (shell / Python script — zero LLM)
      │
      │  duoduo session notify  ← fires only when new data arrives
      ▼
Brain job  (keepalive — dormant by default)
      │
      │  Notify  ← fires only when signal meets your threshold
      ▼
Main session  (your foreground chat)
```

- **Mechanical layer** — a plain script scheduled by launchd, cron, or a
  systemd timer. It polls the source, compares against last-seen state, and
  calls `duoduo session notify` only when something new is detected. No LLM
  involved at any point.
- **Brain job** — a `keepalive` duoduo job. It wakes on notify, processes
  the incoming data, decides whether the result is worth surfacing, and
  sends a Notify to your main session only when the signal clears your
  threshold. Then it goes dormant again.
- **Main session** — your regular foreground chat. It receives a single,
  pre-filtered brief only when the brain has found something actionable.

## Typical use cases

- **Feed / account monitoring** — check a public feed every few minutes;
  wake the brain only on new posts.
- **Price or metric alerts** — poll an API for a number; wake the brain
  only when it crosses a threshold.
- **File or repo change detection** — watch a directory or git remote;
  wake the brain only on new commits or file changes.
- **Webhook relay** — a lightweight receiver script forwards payloads to
  the brain via notify, keeping the brain dormant between events.
- **Data-source health watch** — detect when an upstream source goes stale
  and surface an alert without running a full LLM cycle just to check.

## References

- [Pattern: mechanical layer + brain job](references/pattern-mechanical-brain.md) —
  how to build the two-layer setup end-to-end.
- [Notify routing and signal filtering](references/notify-routing.md) —
  how the brain decides what to surface, how to format briefs, and how to
  route them without flooding your main session.
