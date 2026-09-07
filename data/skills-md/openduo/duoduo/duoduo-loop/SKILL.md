---
name: duoduo-loop
description: "Set up, manage, and troubleshoot recurring loops on a duoduo install — the /loop command and the background jobs it creates. Use when the user wants duoduo to do something repeatedly or on a schedule, watch something until it finishes, run a long-term tracker, or inspect/stop/pause/re-pace an existing loop. Also trigger for Chinese: 定时任务, 循环任务, 周期任务, 每天帮我, 每小时, 盯着…直到, 持续跟进, 长期跟踪, 看看我的循环, 停掉那个 loop, 暂停循环, 改一下节奏, 让多多定期做某事."
---

# Duoduo Loop

`/loop` turns a one-line request into a recurring background task. Type
`/loop <what you want done, in your own words>` in any foreground duoduo
chat — a Feishu DM, the stdio CLI, or an editor (ACP) session. The agent
reads cadence, engine, and delivery wishes straight from your prose, drafts
an execution plan, and creates the task once you confirm. Loops run in
their own background job sessions; your chat stays a human conversation and
receives results as messages.

## The confirmation flow

Every `/loop` goes plan-first:

> **You**: `/loop check the staging deploy every 20 minutes and tell me the moment something breaks`
> **Agent**: Plan — check every 20 minutes in a background task; message
> you only on anomalies; task id `staging-watch`; say "stop staging-watch"
> to end it. Confirm?
> **You**: confirmed

The plan always shows the cadence, the engine/model, how results arrive,
and how to stop — read it as your cost receipt before saying yes. To create
in one step, put the waiver in the request itself:
`/loop no need to confirm — every 20 minutes, …`.

## Three loop shapes, by example

**1. Fixed cadence** — the same light work every tick (digests, sweeps,
health pings).

> `/loop every morning at 8 send me a Hacker News digest`

Each run starts fresh, does the job, and messages you the result. Calendar
times and intervals both work ("every Monday at 9", "every 2 hours"). Interval
durations can combine units without spaces (`2h30m`, `1d6h4m`; units:
`s`/`m`/`h`/`d`/`w`). An invalid or impossible schedule is rejected when the
loop is created instead of being accepted and then silently never firing.

**2. Self-paced** — a short-lived mission that decides its own next check.

> `/loop watch the CI on example/repo#123, rerun it when it fails, and tell me once it's green and merged — pace yourself`

The loop picks its next wake time from what it just observed — checking
often while things are hot, backing off when quiet — and ends itself when
the goal completes, with a final report.

**3. Long-term tracker** — months-long topics, heavy reading, accumulated
judgment.

> `/loop track developments on <topic> long-term; ping me daily only when there are real highlights, and hand the heavy reading to background helpers`

A long-lived coordinator carries the running judgment across weeks while
short-lived helpers do the heavy fetching and reading; the agent orchestrates
that fan-out, the per-round quality checks, and the delivery for you. What you
control in plain words is the shape: how often to hear from it, what counts as
a real highlight, and that the heavy work goes to helpers. Each round arrives
either complete or with any gap named rather than hidden, and the tracker can
sleep indefinitely and wake again — see "pause" below.

## Choosing engine and model in plain words

Name them in the request; they pass through as-is:

> `/loop using codex with gpt-5.4-mini, check every hour whether <site> is up`

Cheap models suit high-frequency checks; save strong models for the daily
synthesis loops. The plan echoes your choice back before anything is
created.

## Managing running loops

All management happens in chat, with the host CLI as the inspection
fallback:

- **List** — "show me my loops" → ids, schedules, and the last result of
  each. On the host, each loop is one markdown file under
  `<runtime_dir>/var/jobs/active/`.
- **Stop** — "stop <id>" → the job is archived to
  `<runtime_dir>/var/jobs/archive/` and can be restored from there.
- **Pause / wake (trackers)** — a long-term tracker pauses by simply
  sleeping past its next wake; mention it in chat ("pick that <topic>
  tracker back up") to wake it with its memory intact.
- **Re-pace** — "make <id> daily instead" → the agent reschedules it in
  place.

## Cost notes

The interval is the spend rate: every fire is a real model run. The
confirmation plan is the moment to tighten cadence and pick a cheaper
model. For "watch until done" needs, prefer the self-paced shape — it
spends checks where the action is and stops by itself.

## Troubleshooting, by scenario

- **"The schedule came and went, nothing happened"** — run
  `duoduo daemon status` first; the scheduler lives in the daemon, so a
  stopped daemon means a silent calendar. Then ask the agent to read the
  job ("what's the state of <id>?") — the listing's last result and last
  error say what happened on the most recent fire.
- **"It pings me too much"** — ask for signal-only delivery: "switch that
  loop to alerting me only on anomalies". Monitoring loops created through
  the plan default to signal-only; every-run reports are the opt-in.
- **"It failed once and went quiet"** — transient startup failures retry on
  their own; a loop that hit a real error tells you so and stops. Either way,
  reply "bring it back up" and the agent re-arms or recreates it.
- **"What did it do historically?"** — archived loops stay readable: ask
  "read me the archived record of <id>", or open the file under
  `<runtime_dir>/var/jobs/archive/`.
