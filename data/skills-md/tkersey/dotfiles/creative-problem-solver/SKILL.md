---
name: creative-problem-solver
description: Lateral-thinking playbook that always returns a five-tier strategy portfolio (Quick Win through Moonshot). Use when you need options, alternatives, or trade-offs; when progress is stalled or failing repeatedly; or when you ask to think creatively, reframe constraints, and choose a strategic path before execution.
---

# Creative Problem Solver

Purpose: generate a five-tier portfolio that compounds (Artifact Spine), then stop for a human choice.

## Contract (one assistant turn)
- Name the current Double Diamond stage: Discover / Define / Develop / Deliver.
- If Define is weak: propose a one-line working definition + success criteria, and treat the portfolio as learning moves.
- Deliver options, then stop and ask for human input before executing.
- Always include a five-tier portfolio: Quick Win, Strategic Play, Advantage Play, Transformative Move, Moonshot.
- For each option: accretive artifact + expected signal + escape hatch.
- Run an Aha Check after reframing.
- Track provenance (technique → Aha Y/N). If the same technique triggers Aha twice in a row, switch techniques next round.
- Keep a short Knowledge Snapshot (facts/risks/assets) + Decision Log.
- Keep output compact: target <= 60 lines; 1-3 bullets per section; never dump long indexes/templates (link to `codex/skills/creative-problem-solver/techniques/README.md` or `codex/skills/creative-problem-solver/TEMPLATES.md` instead).

## When to use
- Progress is stalled or blocked.
- Repeated attempts fail the same way.
- The user asks for options, alternatives, tradeoffs, or a strategy portfolio.
- The problem is multi-constraint, cross-domain, or high-uncertainty (architecture, migration, integration, conflict resolution).

## Quick start
1. Choose Double Diamond stage: Discover / Define / Develop / Deliver.
2. Choose lane: Fast Spark or Full Session.
3. Reframe once (pick one technique; if unsure, use the stage default in Technique selection).
4. Aha Check. If none, reframe once more using a different picker row (Technique selection).
5. Define gate: state a one-line problem statement + success criteria (or mark unknown and ask).
6. Define an Artifact Spine (1–3 shared artifacts) so the tiers can stack.
7. Generate the five-tier portfolio (learning moves in Discover/Define; solution moves in Develop/Deliver).
8. Score options (1–5): Signal, Accretion, Ease, Reversibility, Speed.
9. Ask the user to choose a tier or update constraints.
10. Close with an Insights Summary.

## Double Diamond alignment
- Discover (diverge): broaden context; focus options on learning (research, instrumentation, repro, characterization).
- Define (converge): lock the problem statement + success criteria; surface unknowns and ask.
- Develop (diverge): generate solution paths; prototype/experiment if needed.
- Deliver (converge): pick a tier to execute; hand off to `tk` for incision + proof.

## Mode check
- Pragmatic (default): ship-this-week options only.
- Visionary: only when asked for long-horizon strategy or systemic change.

## Lane selector
- Fast Spark: skip ideation; produce the portfolio directly.
- Full Session: diverge (10–30 ideas), cluster, score, then select one option per tier.

## Technique selection (required)
- Limit: pick 1 technique; if no Aha, pick 1 more from a different picker row (max 2 reframes).
- Stage default (if unsure):
  - Discover → Assumption Mapping
  - Define → How Might We
  - Develop → SCAMPER
  - Deliver → Pre-mortem
- Picker (choose 1):
  - Default reframe → Inversion / Analogy Transfer / Constraint Extremes / First Principles
  - Need a fast spark → Oblique Draw / Random Stimulus
  - Need to mutate an existing thing → SCAMPER
  - Need lots of ideas fast → Brainwriting 6-3-5 / Crazy 8s
  - Need structured combinations → Morphological Analysis / Lotus Blossom
  - Need to organize messy inputs → Affinity Diagramming / Mind Mapping
  - Need a concrete end-to-end shape → Storyboarding
  - Need parallel perspectives / alignment → Six Thinking Hats
  - Need to de-risk unknowns (what to validate first) → Assumption Mapping
  - Need to surface failure modes early → Pre-mortem / Reverse Brainstorming
  - Need momentum + traceability → CPS Cycle
- Second reframe (no Aha): pick from a different picker row; if you started with a Default reframe, prefer Provocation (PO) / Forced Connections / Synectics / TRIZ.
- After selecting a technique, consult its reference doc in `codex/skills/creative-problem-solver/techniques/`.
- Chat disclosure: include only `Reframe used: <technique>` + a one-line “why”.
- Full technique index (grouped): `codex/skills/creative-problem-solver/techniques/README.md`.

## Oblique draw (optional)
Use when framing is stale. Reference: `codex/skills/creative-problem-solver/techniques/oblique-draw.md` (includes a mini-deck).
1. Draw 4 prompts, pick 1, apply it.
2. Translate it into a concrete lever/constraint.

## Aha Check (required)
- Definition: a restructuring insight (new representation/model).
- Output: one-line insight. If none, reframe once more before generating options.

## Portfolio rule
- Every response must include all five tiers.
- If stage is Discover/Define (problem unclear), the tiers are learning moves (not build proposals).
- If stage is Develop/Deliver (problem clear), the tiers are solution moves.

## Accretion (required)
- Accretive artifact: a durable asset you keep even if the option is wrong (measurement, harness, spec, test, automation, interface, dataset, doc).
- Rule: every tier must name one accretive artifact.
- Artifact Spine: define 1-3 named artifacts shared across tiers; each tier’s artifact must be one of these or an extension of one (otherwise explicitly state why it is a different spine).
- Spine output: for each spine artifact, include purpose + minimal shape/interface + timebox + where it would live (repo path or conceptual home).
- Ladder: prefer stacking (Quick Win builds the base; higher tiers reuse/extend it). If it doesn’t ladder, say so explicitly.

## Option template
```
Quick Win:
- Accretive artifact (spine):
- Expected signal:
- Escape hatch:

Strategic Play:
- Accretive artifact (spine):
- Expected signal:
- Escape hatch:

Advantage Play:
- Accretive artifact (spine):
- Expected signal:
- Escape hatch:

Transformative Move:
- Accretive artifact (spine):
- Expected signal:
- Escape hatch:

Moonshot:
- Accretive artifact (spine):
- Expected signal:
- Escape hatch:
```

## Scoring rubric (1–5, no weights)
- Signal: how much new information this yields.
- Accretion: durable value you keep even if you're wrong.
- Ease: effort/complexity to try.
- Reversibility: ease of undoing.
- Speed: time-to-learn.

Preference: high Signal + Accretion + Reversibility, then Ease + Speed.

## Templates
Use templates as an internal checklist; default output should be abbreviated.

Full templates: `codex/skills/creative-problem-solver/TEMPLATES.md`.

## Deliverable format
- Lane (Fast Spark / Full Session).
- Double Diamond stage (Discover / Define / Develop / Deliver).
- Problem statement + success criteria (or marked unknown).
- Reframe used.
- Aha Check (one line).
- Artifact Spine (1-3 shared artifacts; purpose + minimal interface + where it lives).
- Five-tier portfolio with accretive artifacts + signals + escape hatches.
- Scorecard + brief rationale.
- Knowledge Snapshot (facts/risks/assets; 1-3 bullets).
- Decision Log + Assumptions/Constraints.
- Human Input Required (choose tier or update constraints).
- If execution is chosen: hand off to `tk`.
- Insights Summary.

## Fast Spark example (compact)
```text
Lane: Fast Spark
Stage: Develop

Problem: Search API p95 latency is ~800ms; target <= 200ms at current infra cost.
Success: p95<=200ms, p99<=400ms, CPU +<=10%, no relevancy regression.

Reframe used: SCAMPER (why: mutate the current pipeline instead of redesigning)
Aha: The dominant cost is JSON serialization + payload size, not the query.

Artifact Spine:
- bench/search/ (perf harness + fixed dataset; outputs: p50/p95/p99 + diff)
- perf/tracing/ (capture scripts + flamegraphs; timebox: 30m per hypothesis)

Quick Win:
- Accretive artifact (spine): baseline run + 3 worst traces captured in perf/tracing/
- Expected signal: stable baseline + top-3 hotspot list within 1 day
- Escape hatch: disable extra tracing if overhead/noise

Strategic Play:
- Accretive artifact (spine): harness-backed PR reducing payload/serialization (bench/search/ diffs)
- Expected signal: p95 improves >= 30% on harness with no regression
- Escape hatch: guard behind flag; revert commit

Advantage Play:
- Accretive artifact (spine): cache experiment wired into harness (hit-rate + tail tracked)
- Expected signal: p95 meets target for warm traffic; CPU stays flat
- Escape hatch: kill-switch cache and keep harness

Transformative Move:
- Accretive artifact (spine): response contract + streaming plan validated by harness
- Expected signal: tail latency collapses under large result sets
- Escape hatch: ship streaming as opt-in client capability

Moonshot:
- Accretive artifact (spine): evaluation kit (dataset + harness) to compare engines/architectures
- Expected signal: order-of-magnitude tail improvement in a bakeoff
- Escape hatch: keep kit as decision tool; no migration until winner is clear

Scores (S/A/E/R/Sp):
- Quick Win: 5/5/5/5/5
- Strategic: 4/4/4/4/4
- Advantage: 4/4/3/3/3
- Transformative: 4/5/2/3/2
- Moonshot: 3/5/1/2/1

Human Input Required: pick a tier (Quick Win .. Moonshot) or update constraints.
```

## Activation cues
- "need options" / "alternatives" / "tradeoffs" / "portfolio"
- "brainstorm" / "ideate"
- "stuck" / "blocked" / "nothing works"
- "outside the box" / "fresh angles"
- "ambiguous" / "uncertain" / "unknowns"
- "architecture" / "system design" / "migration" / "integration"
