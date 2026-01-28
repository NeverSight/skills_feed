---
name: dissent
description: Devil's advocate. Seek contrary evidence before locking in. Use when about to make a significant decision, when confidence is high but stakes are higher, or when the team is converging too quickly.
---

# /dissent

Structured disagreement that strengthens decisions. The insight: **find flaws before the one-way door closes.**

Dissent is not attack. It's the practice of actively seeking reasons you might be wrong. The devil's advocate is a role, not a personality.

## When to Use

Invoke `/dissent` when:

- **About to lock in a one-way door** - architecture choices, major hires, public API contracts, anything hard to reverse
- **Confidence is high but stakes are higher** - feeling certain is when you need dissent most
- **Team is converging too quickly** - unanimous agreement without debate is a warning sign
- **You're defending a position** - advocacy mode is the enemy of truth-seeking
- **The path forward seems obvious** - obvious paths have hidden assumptions

**Do not use when:** Gathering initial options, brainstorming, or exploring. Dissent is for stress-testing decisions, not generating them.

## The Dissent Process

### Step 1: Steel-Man the Current Approach

Before attacking, fully articulate the position you're challenging:

> "The current approach is [approach]. The reasoning is [reasoning]. The expected outcome is [outcome]. This is the strongest version of this position."

If you can't state the position charitably, you don't understand it well enough to challenge it.

### Step 2: Seek Contrary Evidence

Actively search for information that contradicts the current approach:

- What data would prove this approach wrong?
- Who disagrees with this? What's their strongest argument?
- What similar approaches have failed elsewhere? Why?
- What are we ignoring because it's inconvenient?

> "If this approach were wrong, what would we expect to see? Are we seeing any of that?"

### Step 3: Pre-Mortem

Imagine it's six months from now and this decision failed. Work backward:

> "This failed because [reason]. The warning signs we ignored were [signs]. The assumption that broke was [assumption]."

Generate at least three plausible failure scenarios:

1. **Technical failure** - It doesn't work as expected
2. **Adoption failure** - It works but nobody uses it / changes nothing
3. **Opportunity cost** - It works but we should have done something else

### Step 4: Surface Hidden Assumptions

Every decision rests on assumptions. Most aren't stated. Find them:

- What are we assuming about the user/customer?
- What are we assuming about the system/codebase?
- What are we assuming about the timeline/resources?
- What are we assuming won't change?

For each assumption:
```
Assumption: [what we're taking for granted]
Evidence: [what supports this assumption]
Risk if wrong: [what happens if this assumption breaks]
Test: [how we could validate this before committing]
```

### Step 5: Decide

Based on the dissent analysis, recommend one of:

- **PROCEED** - Dissent found no critical flaws. Decision strengthened.
- **ADJUST** - Dissent surfaced issues that can be addressed. Modify the approach.
- **RECONSIDER** - Dissent revealed fundamental problems. Go back to solution space.

Always include the reasoning:

> "PROCEED: The strongest counter-argument is [X], but it's addressed by [Y]. The key assumption is [Z], which we've validated by [how]."

### ADR Generation

If the decision is a **one-way door** (hard to reverse) and you recommend PROCEED or ADJUST, offer to create an Architecture Decision Record (ADR). Future team members will ask "why did we do it this way?"

**Offer to create an ADR when:**
- The decision affects system architecture
- Multiple valid approaches were considered and rejected
- The reasoning depends on current context that might not be obvious later
- Someone will likely question this in 6 months

**The dissent report maps directly to ADR format:**

| Dissent Section | ADR Section |
|-----------------|-------------|
| Decision under review | Title |
| Steel-Man Position | Context |
| Contrary Evidence + Pre-Mortem | Options Considered |
| Hidden Assumptions | Consequences |
| Decision + Reasoning | Decision |

**If user accepts, write to:** `docs/adr/NNNN-<decision-slug>.md` (or project's ADR location)

```markdown
# ADR NNNN: [Decision Title]

## Status
Accepted

## Context
[From Steel-Man Position - why this decision needed to be made]

## Decision
[From Decision section - what we decided and why]

## Options Considered
[From Contrary Evidence - what alternatives were evaluated]

## Consequences
[From Hidden Assumptions - what we're accepting by making this decision]

## Notes
Generated from /dissent on [date]
```

## Output Format

Always produce a dissent report in this structure:

```
## Dissent Report

**Decision under review:** [what's being challenged]
**Stakes:** [why this matters]
**Confidence before dissent:** [HIGH/MEDIUM/LOW]

### Steel-Man Position
[The strongest version of the current approach]

### Contrary Evidence
1. [Evidence point 1]
2. [Evidence point 2]
3. [Evidence point 3]

### Pre-Mortem Scenarios
1. **[Failure mode]:** [How this could fail]
2. **[Failure mode]:** [How this could fail]
3. **[Failure mode]:** [How this could fail]

### Hidden Assumptions
| Assumption | Evidence | Risk if Wrong | Test |
|------------|----------|---------------|------|
| [Assumption 1] | [Evidence] | [Risk] | [Test] |
| [Assumption 2] | [Evidence] | [Risk] | [Test] |

### Decision

**Recommendation:** [PROCEED / ADJUST / RECONSIDER]

**Reasoning:** [Why this recommendation]

**If ADJUST:** [Specific modifications]

**Confidence after dissent:** [HIGH/MEDIUM/LOW]

**Create ADR?** [Yes - offer to write docs/adr/NNNN-slug.md / No - not a one-way door]
```

## Examples

### Example 1: Architecture Decision

```
/dissent

We're about to adopt a microservices architecture for the new
payments system. The team agrees this is the right approach.
```

**Output:**
```
## Dissent Report

**Decision under review:** Microservices architecture for payments
**Stakes:** 6+ month commitment, affects entire system
**Confidence before dissent:** HIGH (team unanimous)

### Steel-Man Position
Microservices will allow independent scaling of payment processing,
enable different teams to deploy independently, and provide fault
isolation so one service failure doesn't bring down payments.

### Contrary Evidence
1. We have 4 engineers. Netflix had 100+ when they went microservices.
2. Our deployment pipeline takes 45 minutes. We'll multiply that by N services.
3. The "independent teams" benefit requires teams we don't have.

### Pre-Mortem Scenarios
1. **Distributed systems complexity:** We spend 60% of time debugging
   cross-service issues instead of building features.
2. **Operational overhead:** We can't hire SREs fast enough. System
   is down because nobody understands the full architecture.
3. **Premature optimization:** The "scaling" benefit never materializes
   because we never got enough users to need it.

### Hidden Assumptions
| Assumption | Evidence | Risk if Wrong | Test |
|------------|----------|---------------|------|
| We'll need to scale components independently | None - projected | Waste of complexity | Check actual load patterns |
| Team will grow to support this | Hiring plan exists | Stuck with complexity, no staff | Validate funding/timeline |
| Network latency acceptable | Not measured | Payment failures | Prototype and benchmark |

### Decision

**Recommendation:** RECONSIDER

**Reasoning:** The benefits of microservices assume scale and team
size we don't have. The strongest argument for microservices (independent
scaling) has no evidence supporting the need. A modular monolith gives
us the code organization benefits without the operational complexity.

**Confidence after dissent:** HIGH (clear mismatch)

**Create ADR?** No - we're reconsidering, not committing
```

### Example 2: Feature Decision

```
/dissent

We're about to ship a recommendation system that suggests similar
items based on purchase history. Built over 3 sprints.
```

**Output:**
```
## Dissent Report

**Decision under review:** Ship purchase-history recommendation system
**Stakes:** 3 sprints invested, prominent homepage placement
**Confidence before dissent:** MEDIUM

### Steel-Man Position
Users who bought X often want Y. Amazon proved this works. We have
the purchase data. The model is trained and performs well in testing.

### Contrary Evidence
1. Our testing used historical data. Users might behave differently
   when seeing recommendations in real-time.
2. We have 10K users. Amazon's model works with billions of data points.
3. Competitor tried this, removed it after 6 months (no lift).

### Pre-Mortem Scenarios
1. **Cold start problem:** New users see garbage recommendations,
   leave before making a purchase we could learn from.
2. **Filter bubble:** System recommends what users already buy,
   doesn't drive discovery of new product categories.
3. **Wrong metric:** Recommendations get clicks but not purchases.
   We optimized for engagement, needed revenue.

### Hidden Assumptions
| Assumption | Evidence | Risk if Wrong | Test |
|------------|----------|---------------|------|
| Purchase history predicts intent | Industry standard | Wasted real estate | A/B test against simple "popular items" |
| 10K users is enough data | None | Poor recommendations | Check minimum viable data in literature |
| Homepage placement is right | None | Users ignore it | Heatmap existing traffic patterns |

### Decision

**Recommendation:** ADJUST

**Reasoning:** The approach is sound but we're shipping without
validation. Risk is manageable with modifications.

**Modifications:**
1. Ship with A/B test against "popular items" baseline
2. Add fallback to curated picks for users with <5 purchases
3. Define success metric (revenue lift, not clicks) before launch

**Confidence after dissent:** MEDIUM (reduced risk with A/B)

**Create ADR?** Yes - shall I write `docs/adr/0012-recommendation-system-rollout.md`? Documents why we chose A/B testing and what success metrics we committed to.
```

## Session Persistence

When invoked with a session name (`/dissent <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read **Aim**, **Problem Statement**, **Solution Space** to understand the decision being challenged.

**Writing:** After producing the dissent report:

```markdown
## Dissent
**Updated:** <timestamp>
**Decision:** [PROCEED | ADJUST | RECONSIDER]

[dissent report content]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces dissent report for manual review. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for context on the decision
- Writes dissent report to the session file
- Subsequent skills see that dissent was performed

### With .wm/ (working memory)
- Also reads/writes `.wm/sessions/`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries past decisions on similar topics
- Retrieves relevant guardrails and tribal knowledge
- Logs dissent decision for future reference
- Session file serves as local cache

### With Team Input
- Aggregates dissent from multiple reviewers
- Tracks which assumptions different team members question

## Leads To

After dissent, typically:
- **PROCEED** - Continue to `/execute` or `/ship` with strengthened confidence
- **ADJUST** - Update the approach, then `/review` the modifications
- **RECONSIDER** - Return to `/solution-space` with new constraints

---

**Remember:** Dissent is not doubt. It's the discipline of seeking truth before comfort. The goal isn't to stop decisions—it's to make better ones.
