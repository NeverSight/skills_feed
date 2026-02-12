---
name: yc-sv-development-framework
description: |
  Decision-making framework for software development, Y Combinator / Silicon Valley style.
  Based on real principles from Paul Graham, Sam Altman, Michael Seibel, Patrick Collison, and Brian Chesky.

  Use when:
  - Developing features or products
  - Making technical decisions (what to do, how, when)
  - Prioritizing work (P0, P1, P2)
  - Evaluating whether to refactor or patch
  - Deciding on technical debt
  - Evaluating whether to add tests, CI/CD, or automation
  - Any architecture or engineering decision

  Triggers: development, code, feature, refactor, architecture, prioritize, technical decision,
  what to do first, technical debt, tests, CI/CD, sprint, backlog
---

# YC/SV Development Framework

Decision-making framework based on principles from Y Combinator founders and Silicon Valley leaders.

## THE CENTRAL QUESTION

Before any technical decision, ask:

> "Does this help us make something people want?" (Paul Graham, YC motto)
> "Will this help the next customer pay?"

If the answer isn't clearly YES, you probably shouldn't do it.

---

## CORE PRINCIPLES

### 1. Ship > Perfect (Michael Seibel)

```
"Launch something bad quickly" - Michael Seibel, YC
"If you walk away with one thing: launch something bad quickly"
```

- Launch MVP in days, not weeks
- Iterate based on real feedback
- Your first version MUST be embarrassing

### 2. Validation > Architecture (Patrick Collison)

```
Patrick Collison built Stripe with Ruby + MongoDB, not "elegant" technology.
"Every time there's a super elegant way to do things and a practical, pragmatic way,
we're just gonna cut the corner—at least until we validate there's actual user value."
```

- Ugly code that works > elegant code that doesn't exist
- Don't optimize prematurely
- Solve the problem first, refactor later (if necessary)

### 3. Do Things That Don't Scale (Paul Graham)

```
Brian Chesky at Airbnb: do things manually until it hurts, then automate.
Stripe founders installed the product in person ("Collison installation").
```

- Manual processes are FINE at the start
- Don't automate until the manual process is a real bottleneck
- Use "Collison installation": set up customers manually one by one

### 4. Default Alive or Dead (Paul Graham)

```
Ask yourself: "If I don't raise more money, will I reach profitability before running out of runway?"
```

- If you're "default dead", NOTHING matters except changing that
- Fancy features are irrelevant if the business dies

### 5. Founder Mode (Brian Chesky)

```
Brian Chesky at his YC 2024 talk: the best founders are in the details.
Great leadership is presence, not absence. Know the work, not just "manage people".
```

- Being in the details is NOT micromanagement
- Know the code, the product, the customers

---

## DECISION FRAMEWORK

### Question 1: Is it currently working?

```
YES it works → DON'T TOUCH IT
"If it works, don't touch it"
```

### Question 2: Are users/customers complaining?

```
NO complaints → Not a priority
YES complaints → Evaluate revenue impact
```

### Question 3: Does it block revenue?

```
YES blocks revenue → P0 (do it TODAY)
NO doesn't block → P1 or P2
```

### Question 4: How many users does it affect?

```
10 users who LOVE the product > 1000 who "kinda like it"
- Michael Seibel
```

---

## PRIORITIES (P0/P1/P2)

### P0 - Do TODAY
- Bug losing money/customers
- System down
- Exploitable security vulnerability
- Feature blocking first payment

### P1 - This week
- Bug reported by paying customer
- Feature requested by multiple customers
- Technical debt causing recurring bugs

### P2 - When there's time
- Refactoring "to clean up"
- Tests for code that works
- CI/CD improvements
- Documentation

### NEVER
- Rewrite something that works
- Add features nobody asked for
- "Improvements" without a real problem to solve

---

## TECHNICAL DEBT

### When to ACCEPT technical debt

```
Technical debt is leverage - most startups need it.
```

- To ship faster
- To validate hypotheses
- When the cost of NOT having it is greater than the interest

### When to PAY technical debt

- When it becomes a bottleneck for new features
- When it causes recurring bugs (high "interest")
- When 20% of the code causes 80% of the pain (Pareto)

### When to IGNORE technical debt

- If the code works and nobody touches it
- If the business might die before it matters
- If it doesn't affect customers

---

## QUICK TECHNICAL DECISIONS

### Add tests?

```
Tests for critical payment code: YES
Tests for UI that changes every week: NO
Tests after production bug: YES
Tests "for best practices": NO
```

### Refactor?

```
If current code blocks needed feature: YES
If it "looks ugly" but works: NO
If it causes recurring bugs: YES
If it "would be more elegant": NO
```

### Add CI/CD?

```
If manual deploy takes >30min: YES
If there are <10 deploys/month: NO
If deploy errors are common: YES
If the team is 1-2 people: PROBABLY NO
```

### New dependency/framework?

```
Solves real problem you have TODAY: YES
"Would be useful in the future": NO
Team already knows it: BONUS
Nobody knows it: CAUTION
```

---

## COMMUNICATING DECISIONS

### With non-technical stakeholders (Sam Altman)

```
"Listen to everyone. Then make your own decision."
"It's better to make a decision and be wrong than to equivocate."
```

1. Listen to the business problem
2. Propose simple technical solution
3. Give realistic timeline (and meet it)
4. DON'T ask permission for technical decisions

### When to say NO

- "That would require rewriting X, which works fine"
- "We can do it, but it would delay Y which is more important"
- "The simple version takes 2 days, the 'correct' one takes 2 weeks"

---

## METRICS THAT MATTER

```
"Choose 1-2 key metrics. Decide based nearly exclusively on how tasks impact those metrics"
- Michael Seibel
```

### For B2B SaaS:
1. MRR (Monthly Recurring Revenue)
2. Churn rate

### For Marketplace:
1. GMV (Gross Merchandise Value)
2. Take rate

### For Consumer:
1. DAU/MAU
2. Retention D7/D30

### DON'T measure:
- Lines of code
- Test coverage (except as a signal)
- Team "velocity"
- Story points

---

## EXECUTIVE SUMMARY

```yaml
do:
  - Ship fast, iterate based on data
  - Solve real problems for real users
  - Ugly code that works > elegant code that doesn't exist
  - Manual first, automate when it hurts

dont:
  - Refactor code that works
  - Add features nobody asked for
  - Optimize before having users
  - "Best practices" without a real problem

guiding_questions:
  - "Will this help the next customer pay?"
  - "How many users are complaining about this?"
  - "What happens if we DON'T do this?"
  - "What's the simplest version that solves the problem?"
```

---

## SOURCES

Principles extracted from:
- Paul Graham (YC Co-founder): paulgraham.com
- Sam Altman (ex-YC President): blog.samaltman.com
- Michael Seibel (YC Partner Emeritus, Former CEO): michaelseibel.com
- Patrick Collison (Stripe CEO): Interviews and Stripe culture
- Brian Chesky (Airbnb CEO): "Founder Mode" talk at YC 2024
