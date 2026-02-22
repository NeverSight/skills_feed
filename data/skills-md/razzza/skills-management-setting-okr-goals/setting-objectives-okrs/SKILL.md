---
name: setting-objectives-okrs
description: |-
  Guide teams and individuals through setting Objectives, Key Results (OKRs), and annual goals that translate strategy into measurable execution. Use when planning quarterly or annual cycles, setting individual or team goals, aligning on priorities, creating OKRs, writing SMART goals with FROM-TO metrics, reviewing goal cascades, or when the user asks about objectives, key results, goal setting, or planning frameworks. Do not use for purely operational SLA-driven work (use KPIs instead), uncertainty-heavy research (use Discovery OKRs), or reviewing past performance (use a check-in/feedback skill).
metadata:
  author: razzza
  version: 1.0.0
  repository: razzza/skills-management-setting-okr-goals
license: MIT
---

# Setting Objectives & OKRs

Create clear, aligned priorities that translate strategy into execution. Reduce thrash, vague expectations, and "busy but not impactful" work.

## Definitions

| Term | What it is | Critical Question |
|------|-----------|-------------------|
| **Objective (O)** | A meaningful outcome (qualitative, directional) | Where do we want to go? |
| **Key Result (KR)** | Evidence of achievement (quantitative, time-bound, verifiable) | How will we know we got there? |
| **Initiative** | Projects/tasks that influence KRs (not part of the OKR itself) | What will we do to move the numbers? |

## Definition of Done

**Outputs:**
- 1–3 Objectives per team (per quarter), each with 2–4 Key Results
- Clear ownership for each KR
- Baseline + target for each KR
- Each team OKR maps to a higher-level priority
- Initiatives listed separately (optional but recommended)
- Individual goals derived from team KRs, with explicit lineage documented
- Each individual includes: business goals + people goals (managers) + personal development goal
- Manager goal reflection documented (alignment confirmed or redirected)

**Success signals:**
- People can explain "why this matters" in one sentence
- Progress can be tracked weekly without debate
- Tradeoffs are easier (what we won't do becomes clearer)
- Every individual goal traces to a team KR — no orphan goals

**Failure signals:**
- KRs are tasks ("launch X", "build Y") rather than outcomes
- KRs are unmeasurable ("improve quality" with no metric)
- Too many KRs (looks like a backlog, not a strategy)
- Everyone agrees until week 6, then discovers they meant different things
- Individual goals exist that don't connect to any team KR

## Inputs / Prerequisites

**Required:**
- Planning horizon (quarter/half-year)
- Company/team strategy or priorities for that horizon
- Current baselines (where are we now?)
- Known constraints: budget, headcount, dependencies, compliance

**Nice-to-have:**
- Customer insights (NPS/CSAT, churn reasons, win/loss, support themes)
- Historical metrics (last quarter's performance)
- Stakeholder expectations (sales/ops/product/etc.)

---

## Workflow

### Phase 1: Drafting (Outcomes first)

**Step 1 — Start with outcomes, not activity** (30–60 min)
- What must be different by end of period?
- Who benefits (customer/internal/business)?
- What tradeoff are we making (what won't we prioritize)?

Objective template: *"Improve <thing that matters> for <who> by <direction>."*

**Step 2 — Choose 1–3 Objectives max** (15–30 min)
- If you have 5+, you don't have objectives — you have a wishlist.
- "If we only achieved ONE, which matters most?"

**Step 3 — Draft KRs per Objective** (60–90 min)
- 2–4 KRs each; measurable, time-bound, verifiable, owned.
- Prefer a mix of Leading + Lagging indicators (see [references/examples.md](references/examples.md) for KR formats).

**Step 4 — Add baselines + targets + data sources** (30–60 min)
- Baseline: current value
- Target: end-of-period value
- Data source: dashboard/report
- Owner: who updates/owns movement

### Phase 2: Stress-Testing

**Step 5 — Run Validation Tests** (20–30 min)

| Test | Question |
|------|----------|
| Strategic alignment | Does each Objective map to a top priority? |
| Causality | Would these KRs indicate the Objective is achieved? |
| Controllability | Can the team materially influence these metrics? |
| Focus | Is scope realistic for the time period? |
| Clarity | Would two strangers score progress the same way? |
| Counter-metric | For each KR, name at least one metric you must not degrade. |

Counter-metric example: reduce cycle time (KR) → counter-metric = defect rate or customer complaints.

**Step 6 — Identify initiatives** (optional, 30–60 min)
- List initiatives that influence KRs, kept separate from OKRs.
- Each initiative maps to a KR and has an owner + rough effort.

### Phase 3: Socializing

**Step 7 — Review with stakeholders + dependency owners** (30–60 min)
- Confirm dependencies, commitments, timelines.
- Resolve conflicts: what gets deprioritized?
- Lock version for the cycle.

**Step 8 — Set cadence & scoring** (10 min)
- Weekly: update KR values + confidence score
- Mid-cycle: re-baseline if reality changed (document why)
- End: score KRs + capture learnings

### Phase 4: Cascading to Individual Goals

Team OKRs are set. Now each person derives their individual goals from the team's KRs.

**Step 9 — Map individual goals to team KRs** (30–60 min per person)
- For each team KR, identify who contributes and how
- Each individual goal must trace to a specific team KR (the lineage)
- Use FROM-TO metrics to make the individual's contribution measurable
- Include all three goal categories (see below): Business, People, Personal Development
- Identify barriers to remove and support needed per goal

**Step 10 — Validate the cascade** (15–30 min)
- Every team KR has at least one individual goal feeding it
- No individual goal is orphaned (disconnected from a team KR)
- The sum of individual contributions plausibly covers the team KR target
- No critical gaps: if a KR has no one's goal pointing to it, it won't move

### Phase 5: Manager Goal Reflection

After individuals submit their goals, the manager reviews and responds.

**Step 11 — Manager reflects on submitted goals** (15–30 min per person)
- Confirm alignment with team/org priorities
- Redirect or sharpen goals where there's misalignment
- Add context the individual may be missing (cross-team dependencies, strategic shifts)
- Reinforce what's strong; coach on what needs adjustment
- Document the agreed version — this becomes the contract for the cycle

See [references/examples.md](references/examples.md) for manager goal reflection examples.

### Three Categories of Individual Goals

Individual goals should span **Business Outcomes**, **People Outcomes**, and **Personal Development**.

**Business Outcomes** (what moves the business):
- User Growth & Adoption (e.g., active weekly users FROM 18% → TO 30%)
- Revenue Contribution (e.g., ARR FROM $2.1M → TO $3.0M)
- Quality (e.g., critical defects per KLOC FROM 0.45 → TO 0.20)
- Customer Retention (e.g., logo retention FROM 91% → TO 94%)
- Operational Efficiency (e.g., support cost per case FROM $19 → TO $14)

**People Outcomes** (how you lead and grow others — required for managers/leaders):

Use the **Strategy / Execution / Leadership** expectations to shape people outcomes.

| Expectation | Manager | Senior leader |
|---|---|---|
| **Strategy** | Translating direction into clear goals | Looking around corners and setting direction |
| **Execution** | Delivering business results (team goals) | Delivering business results (org goals) |
| **Leadership** | Inspiring and developing others (within and across team) | Inspiring and developing others (within and across org) |

Examples of measurable people outcomes:
- **Strategy**: team has clarity on direction with documented measurable goals; stakeholders aligned early; fewer priority conflicts
- **Execution**: predictable delivery (hit rate on committed outcomes); reduced cycle time / incidents; improved cross-team predictability
- **Leadership**: scaled through others; built successors; retained critical talent; addressed underperformance with clear feedback

Common people-outcome areas:
- Performance Management: provided clear feedback and addressed underperformance
- Hiring & Scaling: attracted and onboarded top talent
- Engagement: improved engagement scores and created a positive team culture

**Personal Development** (how you grow yourself):
- Skill to develop (e.g., negotiation, coaching, technical depth, public speaking)
- Company Value to embody (which company value you'll focus on demonstrating)
- How you'll develop it (workshops, mentorship, practice, feedback loops)
- How you'll know it worked (observable behavior change, feedback from others, measurable outcome)

### Barriers to Remove

For each goal, identify blockers that stand in the way and your plan to address them:
- What is the barrier? (tech debt, skill gaps, resource constraints, market conditions)
- What will you do about it? (specific actions with timeline)
- What support do you need? (budget, headcount, tools, executive sponsorship)

### Cross-functional Collaboration

Call out key partnerships that enable your goals:
- Which teams/stakeholders are you partnering with?
- What have you committed to together? (SLAs, shared rituals, joint reviews)

### Good Individual Goals Are

| Criteria | What it means |
|----------|---------------|
| **Derived from team KRs** | Explicit lineage to a team-level Key Result |
| **Outcome-focused** | Measured by impact, not effort |
| **SMART** | Specific, Measurable, Attainable, Relevant, Time-Bound |
| **Revisitable** | Can be updated as priorities shift |
| **Three-dimensional** | Covers business + people + personal development |

### Quality Checks for Individual Goals
- Each goal explicitly names which team KR it supports
- Each goal has a FROM → TO metric (not just "improve X")
- Impact statement explains why it matters to the business or people
- At least one goal addresses people outcomes (for managers)
- For managers/leaders: people outcomes cover Strategy, Execution, and Leadership (across the set of goals)
- At least one personal development goal with a Company Value focus
- Barriers and support needed are identified (not left vague)
- Goals are attainable within the fiscal year

---

## Templates

### Team OKR Template

```
Objective:
  Statement:
  Why it matters:
  Owner:

Key Results:
  KR1: <metric> from <baseline> → <target>
    Data source:
    Owner:
    Confidence (0.1–1.0):
    Counter-metric(s):
  KR2: ...
  KR3: ...

Initiatives (not KRs):
  Initiative A → supports KR1 (owner: ___)
  Initiative B → supports KR2 (owner: ___)

Dependencies/Risks:
  Dependency:
  Risk:
  Mitigation:
```

### Individual Goal Template (cascaded from Team OKR)

```
BUSINESS / PEOPLE GOALS (top 3, cascaded from team OKRs):

Goal 1:
  Team Objective: [which team objective this supports]
  Team KR: [which specific KR this goal feeds into]
  Goal: [What I will achieve — outcome, not activity]
  Success Measure: FROM [baseline] → TO [target] by [date]
  Impact: [business and/or people outcome]
  People expectation (if people outcome): [Strategy | Execution | Leadership]
  My role: [what specifically I will do to move this]

Goal 2: ...
Goal 3: ...

BARRIERS TO REMOVE:
  Barrier 1: [what's in the way]
    Action: [what I will do, by when]
    Support needed: [budget, headcount, tools, sponsorship]
  Barrier 2: ...

PERSONAL DEVELOPMENT:
  Skill to develop: [specific capability]
  Company Value: [which company value I will focus on demonstrating]
  How I will develop it: [workshops, mentorship, practice, etc.]
  How I will know it worked: [observable change, feedback, measurable outcome]

CROSS-FUNCTIONAL COLLABORATION:
  Partnership: [team/stakeholder]
  Commitment: [what we agreed to — SLAs, shared rituals, joint reviews]

What I won't do this cycle:
```

---

## Strategic Alignment (How work rolls up)

```
Company Strategy / North Star
        ↓
Org Priorities (this cycle)
        ↓
Team Objectives (why)
        ↓
Team Key Results (how we measure)
        ↓
Individual Goals (my contribution to a team KR, with FROM→TO metrics)
        ↓
Initiatives / Tasks (what we do)
```

Sanity checks:
- If an individual goal doesn't feed a team KR → it's orphaned work.
- If a team KR has no individual goals pointing to it → nobody owns moving it.
- If an initiative doesn't move an individual goal or team KR → probably a distraction.
- If a team KR doesn't support an Objective → probably a random metric.
- If an Objective doesn't map to a priority → probably local optimization.

---

## Additional Resources

- For KR formats (leading vs lagging indicators), quality rubric, discovery OKRs, common pitfalls, goal-setting examples, and success metrics, see [references/examples.md](references/examples.md).
