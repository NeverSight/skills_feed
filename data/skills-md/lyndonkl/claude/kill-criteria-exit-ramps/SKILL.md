---
name: kill-criteria-exit-ramps
description: Use when defining stopping rules for projects, avoiding sunk cost fallacy, setting objective exit criteria, deciding whether to continue/pivot/kill initiatives, or when users mention kill criteria, exit ramps, stopping rules, go/no-go decisions, project termination, sunk costs, or need disciplined decision-making about when to quit.
---

# Kill Criteria & Exit Ramps

## Purpose

Kill criteria are pre-defined, objective conditions that trigger stopping a project, product, or initiative. Exit ramps are specific decision points where you evaluate whether to continue, pivot, or kill. This skill helps avoid sunk cost fallacy and opportunity cost by establishing discipline around quitting.

Use this skill when:
- **Starting new projects**: Define kill criteria upfront before emotional/financial investment
- **Evaluating ongoing initiatives**: Decide whether to continue, pivot, or stop
- **Avoiding sunk cost trap**: "We've invested too much to quit now"
- **Portfolio management**: Which projects to kill to free resources for winners
- **Setting go/no-go gates**: Milestone-based decision points
- **Managing risk**: Exit before losses escalate

The hardest decision is often knowing when to quit. Kill criteria remove emotion and politics from stopping decisions.

---

## Common Patterns

### Pattern 1: Upfront Kill Criteria (Before Launch)

**When**: Starting new project, experiment, or product

**Process**: (1) Define success metrics ("10% conversion"), (2) Set time horizon ("6 months"), (3) Establish kill criteria ("If <5% after 6 months, kill"), (4) Assign decision rights (specific person), (5) Document formally (signed PRD)

**Example**: New feature — Success: 20% adoption in 3 months, Kill: <10% adoption, Decision: Product VP makes call

### Pattern 2: Go/No-Go Gates (Milestone-Based)

**When**: Multi-stage projects with increasing investment

**Structure**: Stage 1 (cheap, concept) → Go/No-Go → Stage 2 (moderate, MVP) → Go/No-Go → Stage 3 (expensive, launch) → Go/No-Go

**Example**: Gate 1 (4wk, $10k): 15+ customer interviews show interest → GO. Gate 2 (3mo, $50k): 40% weekly active (got 25%) → NO-GO, kill

**Benefit**: Small investments first, kill before expensive stages

### Pattern 3: Trigger-Based Exit Ramps

**When**: Ongoing projects with uncertain outcomes

**Common triggers**: Time-based ("not profitable by Month 18"), Metric-based ("churn >8% for 2 months"), Market-based ("competitor launches"), Resource-based ("budget overrun >30%"), Opportunity-based ("better option emerges")

**Example**: SaaS — Trigger 1: MRR growth <10%/mo for 3 months → Evaluate. Trigger 2: CAC payback >24mo → Evaluate. Trigger 3: Competitor raises >$50M → Evaluate

**Note**: Triggers prompt evaluation, not automatic kill

### Pattern 4: Pivot vs. Kill Decision

**When**: Project isn't working as planned — should you pivot or kill?

**Framework**:

**Pivot if**:
- Core insight is valid but execution is wrong
- Customer pain is real, solution is wrong
- Market exists, go-to-market is wrong
- Learning rate is high (discovering new insights rapidly)
- Resource burn is sustainable (not desperation mode)

**Kill if**:
- No customer pain (nice-to-have, not must-have)
- Market too small (can't sustain business)
- Burn rate too high relative to progress
- Team doesn't believe in vision
- Better opportunities available (opportunity cost)
- Regulatory/legal blockers

**Example**: Mobile app with low engagement
- **Situation**: Launched fitness app, 10k downloads, 5% weekly active (target was 40%)
- **Pivot option**: Interviews reveal users want meal tracking not workout tracking → Pivot to nutrition app
- **Kill option**: Users don't care about fitness tracking at all, market saturated → Kill, reallocate team

**Decision**: Pivot if hypothesis valid but execution wrong. Kill if hypothesis invalid.

### Pattern 5: Portfolio Kill Criteria (Multiple Projects)

**When**: Managing portfolio of projects, need to kill some to focus

**Process**:
1. **Rank by expected value**: ROI, strategic fit, resource efficiency
2. **Define minimum threshold**: "Top 70% of portfolio gets resources"
3. **Kill bottom 30%**: Projects below threshold, regardless of sunk cost
4. **Reallocate resources**: Winners get resources from killed projects

**Example**: Company with 10 projects, capacity for 7
- Rank by: (Expected Revenue × Probability of Success) / Resource Cost
- Kill: Projects ranked #8, #9, #10 (even if they're "almost done")
- Reallocate: Engineers from killed projects to top 3

**Principle**: Opportunity cost matters more than sunk cost. "Almost done" doesn't justify continuing if better alternatives exist.

### Pattern 6: Sunk Cost Trap Avoidance

**When**: Team resists killing project due to past investment

**Technique**: **Pre-mortem inversion**
1. Ask: "If we were starting today with zero investment, would we start this project?"
2. If answer is "No" → Kill (sunk costs are irrelevant)
3. If answer is "Yes, but differently" → Pivot
4. If answer is "Yes, exactly as-is" → Continue

**Example**: Failed enterprise sales push
- **Situation**: 18 months, $2M spent, 2 customers (need 50 for viability)
- **Inversion**: "If starting today, would we pursue enterprise sales?" → "No, we'd focus on self-serve SMB"
- **Decision**: Kill enterprise sales, pivot to SMB (sunk $2M is irrelevant)

**Trap**: "We've invested so much, we can't quit now" → This is sunk cost fallacy
**Escape**: Only future costs and benefits matter. Past is gone.

---

## Workflow

Use this structured approach when defining or applying kill criteria:

```
□ Step 1: Define success metrics and time horizon
□ Step 2: Establish objective kill criteria
□ Step 3: Assign decision rights and governance
□ Step 4: Set milestone gates or trigger points
□ Step 5: Document formally (signed agreement)
□ Step 6: Monitor metrics regularly
□ Step 7: Evaluate at gates/triggers
□ Step 8: Execute kill decision (if triggered)
```

**Step 1: Define success metrics and time horizon** ([details](#1-define-success-metrics-and-time-horizon))
Specify quantifiable success criteria (e.g., "20% conversion") and evaluation period (e.g., "6 months post-launch").

**Step 2: Establish objective kill criteria** ([details](#2-establish-objective-kill-criteria))
Set numeric thresholds that trigger stop decision (e.g., "If <10% conversion after 6 months"). Make criteria objective, not subjective.

**Step 3: Assign decision rights and governance** ([details](#3-assign-decision-rights-and-governance))
Name specific person who makes kill decision. Define escalation process. Avoid "team consensus" (leads to paralysis).

**Step 4: Set milestone gates or trigger points** ([details](#4-set-milestone-gates-or-trigger-points))
For multi-stage projects: define go/no-go gates. For ongoing projects: define triggers that prompt evaluation.

**Step 5: Document formally** ([details](#5-document-formally))
Write kill criteria in PRD, project charter, or investment memo. Get stakeholders to sign/approve before launch (prevents moving goalposts).

**Step 6: Monitor metrics regularly** ([details](#6-monitor-metrics-regularly))
Track metrics weekly/monthly. Dashboard with kill criteria thresholds clearly marked. Automate alerts when approaching thresholds.

**Step 7: Evaluate at gates/triggers** ([details](#7-evaluate-at-gatestriggers))
When gate or trigger hit, conduct formal evaluation. Use pre-mortem inversion: "Would we start this today?" Decide: continue, pivot, or kill.

**Step 8: Execute kill decision** ([details](#8-execute-kill-decision))
If kill triggered: communicate decision, wind down project, reallocate resources, conduct postmortem. Execute quickly (avoid zombie projects).

---

## Critical Guardrails

### 1. Set Kill Criteria Before Launch (Not After)

**Danger**: Defining kill criteria after project starts leads to moving goalposts

**Guardrail**: Write kill criteria in initial project document, before emotional/financial investment. Get stakeholder sign-off.

**Red flag**: "We'll figure out when to stop as we go" — this leads to sunk cost trap

### 2. Make Criteria Objective (Not Subjective)

**Danger**: Subjective criteria ("team feels it's not working") are easy to ignore

**Guardrail**: Use quantifiable metrics (numbers, dates, milestones). "5% conversion" not "low adoption". "6 months" not "reasonable time".

**Test**: Could two people independently evaluate criteria and reach same conclusion? If not, too subjective.

### 3. Assign Clear Decision Rights

**Danger**: "Team decides" or "we'll discuss" leads to paralysis (everyone has sunk cost)

**Guardrail**: Name specific person who makes kill decision. Define what data they need. Escalation path for overrides.

**Example**: "Product VP makes kill decision based on 6-month metrics. Can be overridden only by CEO with written justification."

### 4. Don't Move the Goalposts

**Danger**: When kill criteria approached, team lowers bar or extends timeline

**Guardrail**: Kill criteria are fixed at launch. Changes require formal process (written justification, senior approval, new document).

**Red flag**: "Let's give it another 3 months" when 6-month criteria not met

### 5. Sunk Costs Are Irrelevant

**Danger**: "We've invested $2M, can't stop now" — sunk cost fallacy

**Guardrail**: Use pre-mortem inversion: "If starting today with $0 invested, would we do this?" Only future matters.

**Principle**: Past costs are gone. Only question: "Is future investment better here or elsewhere?"

### 6. Kill Quickly (Avoid Zombie Projects)

**Danger**: Projects that should be killed linger, draining resources ("zombie projects")

**Guardrail**: Kill decision → immediate wind-down. Announce within 1 week, reallocate team within 1 month.

**Red flag**: Project in "wind-down" for >3 months — this is zombie mode, not killing

### 7. Opportunity Cost > Sunk Cost

**Danger**: Continuing project because "almost done" even if better opportunities exist

**Guardrail**: Portfolio thinking. Ask: "Is this the best use of these resources?" If not, kill even if 90% done.

**Principle**: Opportunity cost of *not* pursuing better option often exceeds benefit of finishing current project

### 8. Postmortem, Don't Blame

**Danger**: Kill decisions seen as "failure", teams avoid them

**Guardrail**: Normalize killing projects. Celebrate disciplined stopping. Postmortem focuses on learning, not blame.

**Culture**: "We killed 3 projects this quarter" = good (freed resources for winners), not bad (failures)

---

## Quick Reference

### Kill Criteria Checklist

Before launching project, answer:
- [ ] Success metrics defined? (quantifiable, e.g., "20% conversion")
- [ ] Time horizon set? (e.g., "6 months post-launch")
- [ ] Kill criteria established? (e.g., "If <10% conversion after 6 months, kill")
- [ ] Decision rights assigned? (specific person, not "team")
- [ ] Documented formally? (in PRD, signed by stakeholders)
- [ ] Monitoring plan? (who tracks, how often, dashboard)
- [ ] Wind-down plan? (how to kill if criteria triggered)

### Go/No-Go Gate Template

| Gate | Investment | Timeline | Success Criteria | Decision |
|------|-----------|----------|------------------|----------|
| Gate 1: Concept | $10k | 4 weeks | 15+ customer interviews showing strong interest | GO / NO-GO |
| Gate 2: MVP | $50k | 3 months | 40% weekly active users (50 beta users) | GO / NO-GO |
| Gate 3: Launch | $200k | 6 months | 10% conversion, <$100 CAC | GO / NO-GO |

### Pivot vs. Kill Decision Framework

| Factor | Pivot | Kill |
|--------|-------|------|
| Customer pain | Real but solution wrong | No pain, nice-to-have |
| Market size | Large enough | Too small |
| Learning rate | High (new insights) | Low (stuck) |
| Burn rate | Sustainable | Too high |
| Team belief | Believes with changes | Doesn't believe |
| Opportunity cost | Pivot is best option | Better options exist |

---

## Resources

### Navigation to Resources

- [**Templates**](resources/template.md): Kill criteria document, go/no-go gate template, pivot/kill decision framework, wind-down plan
- [**Methodology**](resources/methodology.md): Sunk cost psychology, portfolio management, decision rights frameworks, postmortem processes
- [**Rubric**](resources/evaluators/rubric_kill_criteria_exit_ramps.json): Evaluation criteria for kill criteria quality (10 criteria)

### Related Skills

- **expected-value**: For quantifying opportunity cost of continuing vs. killing
- **hypotheticals-counterfactuals**: For pre-mortem analysis ("what if we had killed earlier?")
- **decision-matrix**: For comparing continue/pivot/kill options
- **postmortem**: For learning from killed projects
- **portfolio-roadmapping-bets**: For portfolio-level kill decisions

---

## Examples in Context

### Example 1: Startup Feature Kill

**Context**: SaaS launched "Advanced Analytics", kill criteria: <15% adoption after 3 months

**Result**: 12% adoption → Killed feature, reallocated 2 engineers to core. Saved 6 months maintenance.

### Example 2: Enterprise Sales Pivot

**Context**: B2B SaaS, pivot trigger: <10 customers by Month 12

**Result**: 7 customers → Pivoted to self-serve SMB. Hit 200 SMB customers in 6 months, 4× faster growth.

### Example 3: R&D Portfolio Kill

**Context**: 8 R&D projects, capacity for 5. Ranked by EV/Cost: A(3.5), B(2.8), C(2.5), D(2.1), E(1.8), F(1.5), G(1.2), H(0.9)

**Decision**: Killed F, G, H despite F being "80% done". Top 3 projects shipped 4 months earlier.
