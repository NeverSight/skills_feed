---
name: bet-sizing
description: >
  Evaluate product bets and shape pitches using Shape Up's appetite
  model and Bezos's Type 1/Type 2 decision framework. Use when asked
  to assess a product bet, evaluate initiative risk, decide resource
  allocation, or shape a pitch for a new feature or project.
---

Size product bets by separating reversible from irreversible decisions and shaping work to fit an appetite. Most product bets are Type 2 decisions — reversible, low-cost to try, high-cost to deliberate. Move fast on those. Save deliberation for Type 1 decisions that are hard to undo.

## Type 1 vs Type 2 Decisions (Bezos)

**Type 1 (Irreversible):** One-way doors. Hard to undo once committed.
- Choosing a core technology/platform
- Pricing model changes that affect existing customers
- Killing a product line
- Public commitments (partnerships, integrations)

**Type 2 (Reversible):** Two-way doors. Easy to undo or iterate.
- Most new features (can ship, measure, remove)
- UI/UX changes (can A/B test or revert)
- Internal tooling decisions
- Most API additions (harder to remove, but additive is safer)

**Rule:** Use lightweight process for Type 2. Use deliberate process for Type 1. Most product teams over-process Type 2 decisions and under-process Type 1 decisions.

## Shape Up Pitch Format

When proposing a bet, structure it as a Shape Up pitch:

### 1. Problem
A specific story showing real pain. Not an abstract need — a concrete situation with a real user.

> "When a PM finishes a customer interview, they spend 45 minutes transcribing notes into a PRD. By the time they're done, the emotional context is gone and the PRD reads like a requirements list."

### 2. Appetite
How much time is this worth? Not how long it will take — how much you're willing to invest.

- Small bet: 1-2 weeks
- Medium bet: 3-4 weeks
- Large bet: 6 weeks (maximum for Shape Up)

If you can't fit the solution in the appetite, reshape or kill it.

### 3. Solution
Breadboard-level, not pixel-perfect. Show the key interactions and flows without getting into visual design. Fat-marker sketches, flow diagrams, or written walkthroughs.

### 4. Rabbit Holes
Known risks and unknowns that could blow up the timeline. For each: what's the risk and how will you mitigate it?

### 5. No-Gos
What's explicitly excluded. This is as important as what's included — it prevents scope creep during execution.

## Expected Value Assessment

For larger bets, estimate expected value:

**EV = (Upside x P(success)) - (Downside x P(failure)) + Learning Value**

- **Upside:** Best-case outcome (metric improvement, revenue, users)
- **P(success):** Probability it works (be honest — most features have 30-50% success rate)
- **Downside:** Cost if it fails (time, opportunity cost, technical debt)
- **Learning value:** What you'll learn even if it fails. High learning value makes negative-EV bets worthwhile for early-stage products.

## Guidelines

- CRITICAL: Classify every decision as Type 1 or Type 2 before deciding how much process to apply.
- NEVER spend 6 weeks deliberating a Type 2 decision. Ship it, measure it, adjust.
- NEVER rush a Type 1 decision because of artificial urgency. These are worth slowing down for.
- ALWAYS include No-Gos in a pitch. Without explicit exclusions, scope will grow.
- ALWAYS include Rabbit Holes. The risks you name are less dangerous than the ones you don't.
- NEVER pitch without a stated appetite. "Build this" without a time budget is an open invitation to over-engineer.

---

*Built on Shape Up (Basecamp) and Jeff Bezos's Type 1/Type 2 decision framework. Skills from [productskills](https://github.com/assimovt/productskills).*
