---
name: smart-compaction
description: Manage duoduo's idle auto-compact for channel sessions — enable/disable per conversation, read the measured compaction stats, and retune thresholds with the break-even formula when the owner changes model/backend or asks about idle-session cost. Trigger when the owner mentions 自动压缩/smart compaction/压缩策略, asks why a session was compacted (a compact notice appeared), switches a session to a metered or short-cache-TTL backend, or asks to protect a conversation from compaction. Also use proactively right after the FIRST auto-compaction of a session you manage — that event carries the calibration measurement.
---

# Smart Compaction — idle auto-compact management

## What it is (one paragraph)

Channel sessions accumulate context; after an idle gap longer than the prompt-cache
TTL, the next message re-writes the whole context into cache at a premium. The
daemon ships a deterministic sweeper: when a LIVE session has been idle
`auto_compact_idle_minutes` and its context exceeds `auto_compact_min_context_tokens`,
it silently runs `/compact`. It is **off by default everywhere**; you
(the agent) are the policy layer that enables and tunes it per conversation.
Claude runs that `/compact` in-band on the live streaming subprocess. Grok
uses the same knobs but executes `_x.ai/compact_conversation` (silent, no
channel ack). Pi uses the same two knobs too, and pi compaction is
**two-layer**: pi's own native threshold compaction stays on (inherited from
the user's pi settings) alongside duoduo's idle auto-compact — both layers
coexist by design. Codex remains the only excluded runtime. Grok compact
returns no token counts, so the fuse and the compact notice never
self-calibrate on a grok-only session — do not treat the first grok
idle-compact as a calibration measurement. Pi is in the same boat: its
compact result reports the pre-compaction size only (right after a
compaction pi cannot measure the new resident context yet), so the fuse
never self-calibrates on a pi-only session either. Pi is cheaper in the
worst case, though — a session with nothing worth compacting answers
with a free no-op instead of a paid no-gain compact.

## The knobs (per instance, per kind)

```
duoduo session config <session|alias> get            # merged view + per-key source + measured stats
duoduo session config <session|alias> set auto_compact_idle_minutes=50 auto_compact_min_context_tokens=100000
duoduo session config <session|alias> unset auto_compact_idle_minutes   # back to kind default
duoduo session config --kind <kind> set ...          # kind-wide default (ONLY when the user explicitly says "kind"/"所有会话")
```

- Recommended starting values (signed off for subscription/1h-TTL backends):
  `idle_minutes=50` (fires inside the 1h cache TTL → the compaction read is 10×
  cheaper), `min_context_tokens=100000` (≈2× the measured post-compact floor).
- OFF = `set auto_compact_idle_minutes=0`. This RETAINS the calibrated
  threshold — the on/off switch and the calibration are separate fields
  (thermostat rule: switching off doesn't forget the set-point). A fresh start
  is an explicit `unset`.
- Scope discipline: default to the CURRENT instance. Touch `--kind` only when
  the user explicitly widens scope.
- `set`/`unset` take effect on the session's NEXT drain or the next 60s sweep —
  no restart. `get` never mutates anything.

## Reading the stats — never mental-arithmetic what the kernel precomputed

`session config get` prints the session's `compact_stats` after each
compaction (any origin — manual, auto, or the model's own reactive compact):

| field | meaning |
| --- | --- |
| `post_total` | measured S_total: the floor compaction cannot go below (prompt chain + summary) |
| `history_post` | the compacted history size — this is the summary's OUTPUT cost (formula's `O`) |
| `p_estimate` | fixed prompt-chain overhead (compaction can never reclaim this) |
| `suggested_min_context_tokens` | kernel-computed 2 × post_total — your default retune target |
| `g_gt1h_since_prev_compact` | cold (>1h-gap) returns between the last two compactions — the measured G |
| `g_5m1h_since_prev_compact` | mid-gap returns — becomes cold too on 5-minute-TTL backends |
| `idle_ms` | how long the session had been idle when the auto fire happened (absent for manual) |
| `threshold_at_fire` | the `min_context_tokens` in effect when the auto fire triggered (absent for manual/reactive) |

## The compact notice (kernel → you)

On a smart-compaction-enabled session (and only there — sessions with the
feature off get no injection), the first real turn after ANY compaction
carries a `<smart-compact-notice>` block:

- **data line** — `compacted <ts>: ctx <pre>→<post>, history <pre>→<post>`.
  `post` is the measured floor; no need to query stats for the basics.
- **mismatch line** (only when mis-calibrated) — `threshold <T> < suggested
  <S> — re-calibrate via smart-compaction skill`. This is your retune signal:
  apply guardrail 4 immediately. It also means the kernel FUSE is now armed:
  auto-compact refuses to fire again while the threshold sits at or below the
  measured floor (a fire there can never get under the threshold — a pure
  no-gain loop), so retuning is what re-arms auto-compaction.
- **transcript line** — the full pre-compact transcript path on disk.
  Compaction summarizes your context but deletes nothing: for lost RECENT
  detail, spawn a cheap subagent (haiku/sonnet) to search that file — do not
  read it whole into your freshly-slimmed context. memory/dossiers lag hours
  behind live chat; they are the long-term layer, not the recent-recall layer.

## The break-even algorithm (only for the judgment the arithmetic can't make)

```
C* = (5·O + 1.25·G·S) / (1.25·G − w)
```

- `S` ← `compact_stats.post_total` (measured, this session — never assume)
- `O` ← the summarization OUTPUT size, i.e. the tokens the compact summary
  itself costs: `compact_stats.history_post` (the compacted history — ~4K
  typical). Do NOT use the history SHRINK (`history_pre − history_post`, which
  can be ~50K); that is what was removed, not what the summary costs, and using
  it inflates C* by an order of magnitude.
- `G` ← `g_gt1h_since_prev_compact` (add `g_5m1h` too when the backend TTL is
  5-minute-class). These are kernel-measured from the ledger — read them.
- `w` ← trigger warmth: 0.1 if the backend cache TTL exceeds `idle_minutes`
  (subscription = 1h TTL), else 1.0 (metered API default, Bedrock, Vertex)

Domain: the formula is only valid when `1.25·G > w`. When `1.25·G ≤ w` the
denominator is zero or negative — there are too few cold returns per cycle for
compaction to pay for itself at any context size; that region is governed by
guardrail 2 (raise the threshold or disable), not by C*.

Sessions with context above C* profit from compaction; below it, compaction
loses money. TTL is a fact about the backend you must know or ask — it is
deliberately NOT in the kernel.

**G is a feedback variable, not a fixed input.** The threshold you set
determines how often the session compacts, which sets the length of each
compaction cycle, which changes how many cold returns fall inside it — i.e.
the very G you will measure next time. Treat each retune as one step of a loop:
set → observe the next `compact_stats` (new G) → re-evaluate. Don't over-fit to
a single cycle's G; watch the trend across a few compactions.

## Guardrails (hard rules)

1. **Never set the threshold below 1.2 × measured `post_total`** — below the
   physical floor, compaction is meaningless churn plus fidelity loss.
2. **Metered / short-TTL backends**: keep `100000` only if measured G ≥ 2.
   For G≈1 sessions (one heavy task, one overnight return, re-fattened next
   day) the cold break-even is ≈305K — raise the threshold there or disable.
3. **Retune = act-then-inform**: apply the change, then tell the owner in ONE
   line what changed and why (e.g. "已把这个会话的压缩阈值从 100K 调到 76K —
   实测压缩地板是 38K"). Never silently, never with a wall of text.
4. **First auto-compaction IS the calibration** (Claude, which writes
   `compact_stats`): when the first compact notice arrives, read
   `suggested_min_context_tokens` and retune the instance to it.
   No pre-calibration ritual is needed for new kinds. Grok does not
   emit that notice; skip this step on grok. Pi does not emit it either
   (its compact result has no post-compaction total) — skip on pi too,
   and tune pi thresholds by the break-even formula alone.
5. When the owner says a conversation is precious ("这个会话的上下文别动"),
   set `auto_compact_idle_minutes=0` on that instance and confirm.
6. After any compaction, if you are unsure of an earlier detail: for recent
   specifics, have a cheap subagent search the transcript path the notice
   gives you; for long-term knowledge, consult memory/dossiers. Never
   reconstruct from the summary alone.
7. **Configure a kind AFTER installing its channel.** `--kind <kind>` on a kind
   whose channel is not yet installed CREATES the kind config file; a later
   channel install then SKIPS its seed (the file already exists), so the
   channel comes up without its shipped defaults. Prefer instance-scope
   (`config <session>`) for anything but a deliberate kind-wide rollout.

## Cache-less compatible backends

If the session runs on an endpoint with no prompt caching at all, every turn
pays full input price on the whole context — compaction helps MORE there, not
less. Same knobs, same formula with w=1 and cache premiums read as plain
input cost.
