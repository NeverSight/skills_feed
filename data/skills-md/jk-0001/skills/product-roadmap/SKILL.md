---
name: product-roadmap
description: Build and manage a product roadmap for a solopreneur business. Use when deciding what to build next, prioritizing features, planning product development over quarters, communicating plans to customers or stakeholders, or managing scope and expectations. Covers prioritization frameworks, roadmap structure, customer feedback integration, and saying no to feature requests. Trigger on "product roadmap", "what to build next", "feature prioritization", "roadmap planning", "product strategy", "feature requests".
---

# Product Roadmap

## Overview
A product roadmap is your plan for what to build and when. For solopreneurs, roadmaps prevent scope creep, keep you focused on high-impact work, and help you say no to distractions. This playbook shows you how to build a roadmap that drives business outcomes, not just feature bloat.

---

## Step 1: Understand What a Roadmap Is (and Isn't)

**A roadmap IS:**
- A prioritized list of problems to solve or outcomes to achieve
- A plan for the next 3-12 months
- A tool to communicate direction to customers and stakeholders
- Flexible — it evolves as you learn

**A roadmap is NOT:**
- A promise ("we will ship X on Y date")
- A list of every feature request you've ever received
- Set in stone — expect to revise quarterly

**Key principle:** Roadmaps are about outcomes, not features. Don't say "Build a dashboard." Say "Help users understand their data at a glance."

---

## Step 2: Gather Input (Where Feature Ideas Come From)

Before prioritizing, collect all the inputs. Ideas come from multiple sources:

**Input sources:**
1. **Customer feedback** (support tickets, feature requests, user interviews)
2. **Your vision** (where you want the product to go long-term)
3. **Competitive gaps** (features competitors have that you don't)
4. **Data/analytics** (usage patterns, drop-off points, low-adoption features)
5. **Business goals** (what needs to happen for revenue/growth targets?)

**Collection method:**
- Create a backlog (a running list of all ideas). Use Notion, Trello, Linear, or even a Google Sheet.
- For each idea, note: source, problem it solves, who requested it, and rough estimate (small/medium/large).

**Rule:** Don't prioritize while collecting. Just capture everything first.

---

## Step 3: Prioritize Using a Framework

You can't build everything. Prioritization is about choosing what NOT to build.

### Framework: RICE Score
**RICE = Reach × Impact × Confidence ÷ Effort**

For each feature or project, score:

**Reach:** How many users will this affect in a given time period?
- Example: 100 users/month = 100

**Impact:** How much will this impact those users?
- Massive = 3, High = 2, Medium = 1, Low = 0.5, Minimal = 0.25

**Confidence:** How confident are you in your Reach and Impact estimates?
- High = 100%, Medium = 80%, Low = 50%

**Effort:** How many person-weeks will this take?
- Example: 2 weeks = 2

**RICE Score = (Reach × Impact × Confidence) / Effort**

Example:
```
Feature: "Add bulk export"
Reach: 200 users/month
Impact: 2 (high)
Confidence: 80%
Effort: 1 week

RICE = (200 × 2 × 0.8) / 1 = 320
```

**Sort your backlog by RICE score. Highest score = highest priority.**

### Alternative Framework: Value vs Effort Matrix
Simpler than RICE. Plot each feature on a 2×2 grid:

```
        High Value
            |
  Quick Wins | Big Bets
------------|------------
 Time Sinks | Low Priority
            |
        Low Value
```

- **Quick Wins** (high value, low effort) → Do these first
- **Big Bets** (high value, high effort) → Do these after quick wins
- **Time Sinks** (low value, high effort) → Never do these
- **Low Priority** (low value, low effort) → Do these if you have free cycles (usually don't)

**When to use which:**
- Use RICE when you have data on reach and impact
- Use Value vs Effort when you're early and estimates are rough

---

## Step 4: Structure Your Roadmap

Organize your roadmap into time horizons. Solopreneurs should plan in quarters, not months (too much changes too fast for monthly roadmaps to stay accurate).

**Roadmap structure:**

```
NOW (Current Quarter)
  Theme: [What's the focus this quarter?]
  Features/Projects:
    1. [Highest priority item from Step 3]
    2. [Second highest priority]
    3. [Third highest — only if capacity allows]

NEXT (Next Quarter)
  Theme: [What's the likely focus?]
  Features/Projects:
    - [Top 3-5 candidates, but not committed]

LATER (6-12 months out)
  Theme: [Strategic direction]
  Features/Projects:
    - [High-level goals, not specific features]
```

**Why themes matter:** Themes give your quarter focus. "Improve retention" is a theme. It helps you evaluate whether a feature request fits the current priority or should wait.

**How many features per quarter?** For a solo builder: 2-4 meaningful features or projects. Don't overcommit. Expect only 60-70% of your plan to ship — bugs, customer issues, and life happen.

---

## Step 5: Communicate the Roadmap

A roadmap in your head is useless. Share it with customers and stakeholders.

**Where to share:**
- **Public roadmap** (Trello, Notion, or a dedicated roadmap tool like Canny, ProductBoard)
- **In-product** (link to roadmap from your app's menu or help section)
- **Email updates** (quarterly email to customers: "Here's what we're building next")
- **Social media** (share progress updates, celebrate shipped features)

**What to share publicly vs privately:**
- **Public:** Themes, top priorities, rough timelines (Q1, Q2, not specific dates)
- **Private (internal only):** Detailed specs, technical decisions, rejected ideas

**Language for roadmap items:**
- Instead of: "We will launch X on March 15"
- Say: "We're planning to ship X in Q1. Timelines may shift based on learnings."

**Why this matters:** Overpromising and underdelivering kills trust. Underpromise and overdeliver builds it.

---

## Step 6: Integrate Customer Feedback

Customers will ask for features. Some requests are gold. Most are noise. Your job is to filter.

**How to handle feature requests:**

1. **Acknowledge and thank them.** "Thanks for the suggestion! We're tracking this."
2. **Ask clarifying questions.** "What problem are you trying to solve with this?" (Often the requested feature isn't the best solution to their actual problem.)
3. **Log it in your backlog.** Don't commit to building it, but track it.
4. **Look for patterns.** If 10 people ask for the same thing, it's signal. If 1 person asks, it might be noise (or an edge case).

**When to prioritize a request:**
- Multiple customers ask for it (signal of demand)
- It aligns with your product vision and business goals
- It scores high on RICE or Value vs Effort

**When to say no:**
- It's a one-off request with no pattern
- It pulls you away from your theme or strategic focus
- It benefits a tiny minority at the expense of the majority
- It would add complexity that's not worth the value

**How to say no:**
```
"Thanks for the suggestion! We're focused on [current theme] right now, so this
won't make it into the next few months. We'll keep it on the radar and revisit
as priorities evolve."
```

**Rule:** Every "yes" is a "no" to something else. Protect your roadmap ruthlessly.

---

## Step 7: Review and Adjust Quarterly

Roadmaps are living documents. Review and update every quarter.

**Quarterly roadmap review (60-90 min):**

1. **Look back:** What shipped this quarter? What didn't? Why?
2. **Measure impact:** Did the features we shipped move the metrics we cared about? (retention, revenue, activation, etc.)
3. **Collect new inputs:** What feedback came in? What changed in the market? What did we learn?
4. **Re-prioritize:** Re-run your prioritization framework on the backlog. What should move into "Now" for next quarter?
5. **Set the theme:** What's the focus for next quarter?
6. **Communicate:** Share the updated roadmap with customers.

**Red flags to watch for:**
- You're shipping tons of features but none are moving key metrics (you're building the wrong things)
- Your roadmap hasn't changed in 6 months (you're not learning or adapting)
- You're constantly reacting to the loudest customer voice (you've lost strategic direction)

---

## Step 8: Balance Fast Iteration with Strategic Vision

As a solopreneur, you can move faster than big companies. Use that advantage.

**How to stay nimble:**
- Ship small, test fast. Don't wait 3 months to launch a "perfect" feature. Ship a small version in 2 weeks, learn, iterate.
- Build MVPs of new features before committing to the full version.
- Use feature flags or beta access to test with a small group before rolling out to everyone.

**How to stay strategic:**
- Don't chase every shiny object. Stick to your quarterly theme unless something major changes.
- Protect 20-30% of your time for foundational work (refactoring, performance, UX polish). These don't go on the customer-facing roadmap but they matter.

**Balance:** 70% execution on the roadmap, 30% exploration and learning.

---

## Product Roadmap Mistakes to Avoid
- **Building everything customers request.** You're not a feature factory. Focus on solving problems, not collecting features.
- **Not saying no.** Every yes is a no to something else. Learn to decline feature requests that don't align with your vision.
- **Committing to specific dates too far in advance.** Roadmaps are plans, not promises. Give quarters, not dates.
- **Not measuring impact after shipping.** If you don't check whether a feature moved the needle, you'll keep building low-impact stuff.
- **Keeping the roadmap secret.** Customers appreciate transparency. Share what you're working on (at a high level).
- **Letting the roadmap go stale.** If you haven't updated it in 6+ months, it's useless. Review quarterly.
