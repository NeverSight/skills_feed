---
name: build-and-learn
description: ACTION REQUIRED - After completing ANY non-trivial task (writing code, creating content, building strategies, designing anything), Claude MUST immediately invoke this skill and offer learning modes to the user. Do not wait for user to ask. Say "Want to understand the thinking behind what we just built?" then offer Quick (1 min) / Standard (10 min) / Deep (30 min) modes. Also invoke when user types "/build-and-learn" or asks "why did you do it this way" or "what could go wrong".
---

# Build & Learn

## Overview

Every time Claude helps you build something, there's an opportunity to learn. This skill turns AI assistance into skill development by exploring:

- **Tradeoffs** - Every decision has costs and benefits
- **Pitfalls** - What could go wrong, what to watch for
- **Business & System Impact** - How does this affect customers, workflows, and other systems?
- **Reasoning** - Why this approach vs alternatives
- **Better collaboration** - How to work more effectively with AI

**Works for anyone:** Engineers, marketers, designers, writers, analysts, mechanics - anyone who uses Claude to create.

## Mode Selection

### Smart Default + User Choice

After completing a task, select mode based on complexity:

| What Was Built | Suggested Mode |
|----------------|----------------|
| Small fix / simple edit | Skip or Quick |
| Single deliverable | Quick |
| Multi-part project | Standard |
| Complex strategy/system | Deep |

### The Offer

```
We just finished [X]. [One sentence about what's interesting to learn here.]

→ Quick (1 min): One insight + one question
→ Standard (10 min): Tradeoffs, pitfalls, discussion ← [if suggested]
→ Deep (30 min): Full analysis + collaboration review
→ Skip

What works for you?
```

### Explicit Triggers

- `/build-and-learn` → Offers mode selection
- "What could go wrong?" → Jump to pitfalls
- "Why did you do it this way?" → Jump to tradeoffs

## Quick Mode (1 minute)

The most important mode. If people can't use this when busy, they won't build the habit.

### Structure

```
**Key insight:** [One sentence about the most important decision/tradeoff]

**Why it matters:** [One sentence connecting to real consequences]

**Quick check:** [One question to verify understanding]
```

### Examples Across Domains

**Marketing - After writing email campaign:**
```
**Key insight:** We led with the pain point ("tired of...") before
introducing the solution, following the PAS framework.

**Why it matters:** Leading with features gets ignored. Leading
with their problem makes them feel understood and keeps reading.

**Quick check:** What would you change if the audience already
knows they have this problem and is comparing solutions?
```

**Code - After building an API:**
```
**Key insight:** We used pagination instead of returning all results,
which prevents timeout and memory issues with large datasets.

**Why it matters:** Without limits, one query could return 100,000
rows and crash the server or freeze the client.

**Quick check:** What problem might users hit if they need to
process ALL results for a report?
```

**Design - After creating a landing page:**
```
**Key insight:** We put the CTA above the fold and repeated it
after each major section.

**Why it matters:** Users who are ready to act shouldn't have to
scroll to find the button. Different users convince at different points.

**Quick check:** If this page has a 70% mobile audience, what
might we need to change?
```

**Strategy - After creating a project plan:**
```
**Key insight:** We built in buffer time between dependent tasks
rather than scheduling back-to-back.

**Why it matters:** One delay cascades to everything downstream.
Buffer absorbs surprises without derailing the whole timeline.

**Quick check:** Where in this plan is the biggest risk if
something takes longer than expected?
```

## Standard Mode (10 minutes)

### Structure

1. **Identify 2-3 decisions worth discussing** (30 sec)
2. **User thinks first** - "What alternatives exist?" (2 min)
3. **Tradeoff discussion** - Why this choice, what we gave up (2 min)
4. **Pitfall check** - "What could go wrong?" (2 min)
5. **Impact check** - "How does this affect users/business/other systems?" (2 min)
6. **One reflection question** (1.5 min)

### Example: Marketing Campaign

```
**Decisions worth discussing:**
1. Email sequence vs single blast - we chose 3 emails
2. Discount offer vs value-first - we led with value
3. Send timing - Tuesday 10am

**Let's start with #1. Before I explain:**
What do you think are the downsides of a 3-email sequence compared
to a single email?

[User responds]

**The tradeoff:**

Single email:
- Pro: Less work
- Pro: No unsubscribe risk from multiple touches
- Con: One chance to catch attention
- Con: Timing might miss people

3-email sequence:
- Pro: Multiple chances to convert
- Pro: Different angles for different objections
- Con: More work to create
- Con: Some will unsubscribe

**We chose sequence because:** This product needs explanation, and
people rarely buy on first exposure. Sequence for considered purchases,
single email for simple offers.

**Pitfall check:** What happens if emails #2 and #3 go to people
who already bought after email #1?

[Discussion continues...]

**Reflection:** How would you decide between sequence vs single
for your next campaign?
```

### Example: Technical Implementation

```
**Decisions worth discussing:**
1. REST vs GraphQL - we chose REST
2. SQL vs NoSQL - we chose PostgreSQL
3. Monolith vs microservices - we kept it monolithic

**Let's start with #1. Before I explain:**
What problems might GraphQL solve that REST doesn't?

[User responds]

**The tradeoff:**

REST:
- Pro: Simple, well-understood
- Pro: Easy caching
- Pro: Works with any client
- Con: Over-fetching (get more data than needed)
- Con: Multiple requests for related data

GraphQL:
- Pro: Get exactly what you need
- Pro: One request for complex data
- Con: More complex server setup
- Con: Caching is harder
- Con: Learning curve

**We chose REST because:** This is a straightforward CRUD app with
simple data needs. GraphQL shines when clients need flexible queries
across complex relationships. Here it would add complexity without benefit.

**Pitfall check:** If the mobile app needs very different data than
the web app, what problem might emerge with REST?

[Discussion continues...]
```

## Deep Mode (30 minutes)

Full analysis when significant work was completed.

### Structure

1. **Overview** - What we built and the big picture (5 min)
2. **All significant tradeoffs** - Discuss each decision (8 min)
3. **Pitfall audit** - What could go wrong (5 min)
4. **Impact analysis** - Customer experience, business processes, system dependencies (6 min)
5. **Collaboration review** - How we could work better (4 min)
6. **Consolidation** - Key takeaways (2 min)

### Collaboration Review Section

Frame as mutual improvement:

```
**How we collaborated:**

What worked well:
- You told me [context] upfront, which helped me [outcome]
- When you asked for options before deciding, we avoided rework

What I had to guess:
- [Assumption] - was that right?
- [Decision] - would you have preferred something else?

For next time:
- Telling me [X] upfront would help me [Y]
- I should have asked about [Z] before starting

**Question:** What would you do differently in how you asked for this?
```

## What We Focus On

### 1. Tradeoff Thinking

Every decision has costs. Develop awareness:

- What alternatives existed?
- Why this approach?
- What did we give up?
- When would a different choice be better?

**Universal tradeoffs:**
- Speed vs quality
- Simple vs comprehensive
- Cost vs capability
- Specific vs flexible
- Now vs later
- Control vs convenience

### 2. Pitfall Awareness

Develop intuition for what goes wrong:

- What assumptions might be wrong?
- What could change that breaks this?
- What are we not considering?
- What's the worst case?
- What's hard to fix later?

### 3. Business & System Impact

Understand the bigger picture:

- **Customer experience:** How does this change affect end users?
- **Business processes:** What workflows or operations are impacted?
- **System dependencies:** What other parts of the system touch this?
- **Data flow:** How does information move differently now?
- **Stakeholders:** Who needs to know about this change?

**Questions to explore:**
- "If a customer does X, what's different now?"
- "What team/process depends on this working correctly?"
- "What happens to existing data or integrations?"
- "How would support/sales/ops experience this change?"

### 4. Domain Understanding

Go deeper than surface solutions:

- Why does this work?
- What principles underlie this approach?
- How would an expert think about this?
- What separates good from great here?

### 5. AI Collaboration

Work more effectively with Claude:

- What context produces better results?
- When should you verify outputs?
- How to iterate effectively?
- What are AI limitations in this area?

See [references/prompt_patterns.md](references/prompt_patterns.md)

## Learning Progress Storage

### Simplified Schema

**Global:** `~/.claude/learning/profile.json`
```json
{
  "domains": ["marketing", "code", "writing"],
  "tradeoffs_discussed": ["speed vs quality", "sequence vs single email"],
  "pitfalls_learned": ["forgot mobile users", "no error handling"],
  "prompting_insights": ["give audience context upfront"],
  "last_session": "2025-01-25"
}
```

**Project:** `.claude/learning.json`
```json
{
  "project_type": "product launch",
  "decisions_made": ["chose email sequence", "value-first positioning"],
  "known_risks": ["no A/B testing", "tight timeline"]
}
```

## Anti-Patterns

### Don't:
- Ask trivia questions
- Quiz on memorization
- Make it feel like a test
- Be condescending
- Force long sessions when busy
- Assume technical knowledge
- Use jargon without context

### Do:
- Focus on judgment and reasoning
- Let user think before explaining
- Keep quick mode actually quick
- Match examples to user's domain
- Respect user's time
- Make it feel like learning from a mentor

## Resources

- [references/tradeoff_patterns.md](references/tradeoff_patterns.md) - Common tradeoffs across domains
- [references/pitfall_catalog.md](references/pitfall_catalog.md) - What goes wrong, by category
- [references/prompt_patterns.md](references/prompt_patterns.md) - Better AI collaboration
- [references/learning_science.md](references/learning_science.md) - Why these techniques work
