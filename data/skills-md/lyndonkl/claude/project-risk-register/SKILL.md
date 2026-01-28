---
name: project-risk-register
description: Use when managing project uncertainty through structured risk tracking, identifying and assessing risks with probability×impact scoring (risk matrix), assigning risk owners and mitigation plans, tracking contingencies and triggers, monitoring risk evolution over project lifecycle, or when user mentions risk register, risk assessment, risk management, risk mitigation, probability-impact matrix, or asks "what could go wrong with this project?".
---
# Project Risk Register

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It?](#what-is-it)
4. [Workflow](#workflow)
5. [Common Patterns](#common-patterns)
6. [Risk Scoring Framework](#risk-scoring-framework)
7. [Guardrails](#guardrails)
8. [Quick Reference](#quick-reference)

## Purpose

Proactively identify, assess, prioritize, and monitor project risks to reduce likelihood of surprises, enable informed decision-making, and ensure stakeholders understand uncertainty. Transform vague concerns ("this might not work") into actionable risk management (probability×impact scores, named owners, specific mitigations, measurable triggers).

## When to Use

**Use this skill when:**

- **Project kickoff**: Establishing risk baseline before significant work begins
- **High uncertainty**: New technology, unfamiliar domain, complex dependencies, regulatory constraints
- **Stakeholder pressure**: Execs/board want visibility into "what could go wrong"
- **Critical path concerns**: Delays, dependencies, or single points of failure threaten timeline
- **Gate reviews**: Quarterly check-ins, milestone reviews, go/no-go decisions require risk assessment
- **Incident response**: Major issue occurred, need to identify related risks to prevent recurrence
- **Portfolio management**: Comparing risk profiles across multiple projects for resource allocation
- **Change requests**: Scope/timeline/budget changes require risk re-assessment

**Common triggers:**
- "What are the biggest risks to this project?"
- "What could cause us to miss the deadline?"
- "How confident are we in this estimate/plan?"
- "What's our backup plan if X fails?"
- "What dependencies could block us?"

## What Is It?

**Project Risk Register** is a living document tracking all identified risks with:

1. **Risk identification**: What could go wrong (threat) or go better than expected (opportunity)
2. **Risk assessment**: Probability (how likely?) × Impact (how bad/good if it happens?) = Risk Score
3. **Risk prioritization**: Focus on high-score risks (red/high) first, monitor medium (yellow), accept low (green)
4. **Risk ownership**: Named individual responsible for monitoring and mitigation
5. **Risk response**: Mitigation (reduce probability), contingency (reduce impact if occurs), acceptance (do nothing)
6. **Risk triggers**: Early warning indicators that risk is materializing (time to activate contingency)
7. **Risk monitoring**: Regular updates (status changes, new risks, retired risks)

**Risk Matrix (5×5 Probability×Impact):**

```
Impact →     1         2         3         4         5
Prob ↓    Minimal   Minor   Moderate  Major   Severe

5 High   │ Medium │ Medium │  High  │  High  │ Critical│
         │   5    │   10   │   15   │   20   │   25    │
4        │  Low   │ Medium │ Medium │  High  │  High   │
         │   4    │    8   │   12   │   16   │   20    │
3 Medium │  Low   │  Low   │ Medium │ Medium │  High   │
         │   3    │    6   │    9   │   12   │   15    │
2        │  Low   │  Low   │  Low   │ Medium │ Medium  │
         │   2    │    4   │    6   │    8   │   10    │
1 Low    │  Low   │  Low   │  Low   │  Low   │ Medium  │
         │   1    │    2   │    3   │    4   │    5    │
```

**Risk Thresholds:**
- **Critical (≥20)**: Escalate to exec, immediate mitigation required
- **High (12-19)**: Active management, weekly review, documented mitigation
- **Medium (6-11)**: Monitor closely, monthly review, contingency plan
- **Low (1-5)**: Accept or minimal mitigation, quarterly review

**Example: Software Migration Project**

| Risk ID | Risk | Prob | Impact | Score | Owner | Mitigation | Contingency |
|---------|------|------|--------|-------|-------|------------|-------------|
| R-001 | Third-party API deprecated mid-project | 3 | 4 | **12 (Medium)** | Eng Lead | Contact vendor for deprecation timeline | Build abstraction layer for quick swap |
| R-002 | Key engineer leaves during critical phase | 2 | 5 | **10 (Medium)** | EM | Knowledge sharing, pair programming | Contract backup engineer |
| R-003 | Data migration takes 3× longer than estimated | 4 | 4 | **16 (High)** | Data Lead | Pilot migration on 10% data first | Extend timeline, reduce scope |

## Workflow

Copy this checklist and track your progress:

```
Risk Register Progress:
- [ ] Step 1: Identify risks across categories
- [ ] Step 2: Assess probability and impact
- [ ] Step 3: Calculate risk scores and prioritize
- [ ] Step 4: Assign owners and define responses
- [ ] Step 5: Monitor and update regularly
```

**Step 1: Identify risks across categories**

Brainstorm what could go wrong using structured categories (technical, schedule, resource, external, scope). See [Common Patterns](#common-patterns) for category checklists. Use [resources/template.md](resources/template.md) for register structure.

**Step 2: Assess probability and impact**

Score each risk on probability (1-5: rare to almost certain) and impact (1-5: minimal to severe). Involve subject matter experts for accuracy. See [Risk Scoring Framework](#risk-scoring-framework) for definitions.

**Step 3: Calculate risk scores and prioritize**

Multiply Probability × Impact for each risk. Plot on risk matrix (5×5 grid) to visualize risk profile. Focus mitigation on Critical/High risks first. See [resources/methodology.md](resources/methodology.md) for advanced techniques like Monte Carlo simulation.

**Step 4: Assign owners and define responses**

For each High/Critical risk, assign named owner (not "team"), define mitigation (reduce probability), contingency (reduce impact), and triggers (when to activate contingency). See [resources/template.md](resources/template.md) for response planning structure.

**Step 5: Monitor and update regularly**

Review risk register weekly (active projects) or monthly (longer projects). Update probabilities/impacts as context changes, add new risks, retire closed risks, track mitigation progress. See [Guardrails](#guardrails) for monitoring cadence.

## Common Patterns

**Risk categories (use for brainstorming):**

- **Technical risks**: Technology failure, integration issues, performance problems, security vulnerabilities, technical debt, complexity underestimated
- **Schedule risks**: Dependencies delayed, estimation errors, scope creep, resource unavailability, critical path blocked
- **Resource risks**: Key person leaves, skill gaps, budget overrun, vendor/contractor issues, equipment unavailable
- **External risks**: Regulatory changes, market shifts, competitor actions, economic downturn, natural disasters, vendor bankruptcy
- **Scope risks**: Unclear requirements, changing priorities, stakeholder disagreement, gold-plating, mission creep
- **Organizational risks**: Lack of executive support, competing priorities, insufficient funding, organizational change, political conflicts

**By project type:**

- **Software projects**: Third-party API changes, dependency vulnerabilities, cloud provider outages, data migration issues, browser compatibility, scaling problems, security breaches
- **Construction projects**: Weather delays, material shortages, permit issues, labor strikes, soil conditions, cost overruns, safety incidents
- **Product launches**: Manufacturing delays, supply chain disruption, competitor launch, pricing miscalculation, market demand lower than expected, quality issues
- **Organizational change**: Employee resistance, communication breakdown, training inadequate, budget cuts, leadership turnover, cultural misalignment

**By risk response type:**

- **Mitigate (reduce probability)**: Training, prototyping, process improvements, redundancy, quality checks, early testing
- **Contingency (reduce impact if occurs)**: Backup plans, insurance, reserves (time/budget), alternative suppliers, rollback procedures
- **Accept (do nothing)**: Low-score risks not worth mitigation cost, residual risks after mitigation
- **Transfer (shift to others)**: Insurance, outsourcing, contracts (penalty clauses), warranties

**Typical risk profile evolution:**
- **Project start**: Many medium risks (uncertainty high), few critical (pre-mitigation)
- **Mid-project**: Critical risks mitigated to medium/low, new risks emerge (dependencies, integration)
- **Near completion**: Low risks dominate (most issues resolved), few high (last-minute surprises)
- **Red flag**: Risk score increasing over time (mitigation not working, new issues emerging faster than resolution)

## Risk Scoring Framework

**Probability Scale (1-5):**
- **5 - Almost Certain (>80%)**: Expected to occur, historical data confirms, no mitigation in place
- **4 - Likely (60-80%)**: Probably will occur, similar projects had this issue, weak mitigation
- **3 - Possible (40-60%)**: May or may not occur, depends on circumstances, some mitigation in place
- **2 - Unlikely (20-40%)**: Probably won't occur, mitigation in place, low historical precedent
- **1 - Rare (<20%)**: Very unlikely, strong mitigation, no historical precedent

**Impact Scale (1-5) - adjust dimensions for project context:**

**For Schedule Impact:**
- **5 - Severe**: >20% delay (e.g., 3-month project delayed 3+ weeks), miss critical deadline, cascading delays
- **4 - Major**: 10-20% delay, miss milestone, affects dependent projects
- **3 - Moderate**: 5-10% delay, timeline buffer consumed, no external impact
- **2 - Minor**: <5% delay, absorbed within sprint/phase, minor schedule pressure
- **1 - Minimal**: <1% delay or no delay, negligible schedule impact

**For Budget Impact:**
- **5 - Severe**: >20% budget overrun, requires new funding approval, project viability threatened
- **4 - Major**: 10-20% overrun, contingency exhausted, scope cuts required
- **3 - Moderate**: 5-10% overrun, contingency partially used, no scope cuts
- **2 - Minor**: <5% overrun, absorbed within budget flexibility
- **1 - Minimal**: <1% overrun or no budget impact

**For Scope/Quality Impact:**
- **5 - Severe**: Core functionality lost, customer-facing quality issue, regulatory violation
- **4 - Major**: Important feature cut, significant quality degradation, customer complaints
- **3 - Moderate**: Nice-to-have feature cut, minor quality issue, internal workarounds needed
- **2 - Minor**: Edge case feature cut, cosmetic quality issue
- **1 - Minimal**: No scope or quality impact

**Composite Impact** (when multiple dimensions affected):
- Use **maximum** of any single dimension (pessimistic, conservative)
- OR use **weighted average**: Schedule 40%, Budget 30%, Scope/Quality 30%

**Example Scoring:**

Risk: "Key engineer leaves mid-project"
- Probability: 2 (Unlikely - 20% based on tenure, satisfaction, retention rate)
- Impact Schedule: 4 (Major - 3-week delay to onboard replacement, knowledge transfer)
- Impact Budget: 2 (Minor - recruiter fees, some overtime)
- Impact Scope: 3 (Moderate - may cut advanced features)
- **Composite Impact**: 4 (take maximum: schedule impact is worst)
- **Risk Score**: 2 × 4 = **8 (Medium)**

## Guardrails

**Ensure quality:**

1. **Identify risks proactively, not reactively**: Run risk workshops before problems occur
   - ✓ Brainstorm risks at project kickoff, use checklists (technical, schedule, resource, etc.)
   - ❌ Add risks only after incidents occur (reactive)

2. **Be specific, not vague**: "Integration fails" is vague, "Vendor API rate limits block migration" is specific
   - ✓ "Third-party payment gateway rejects 10% of transactions due to fraud rules"
   - ❌ "Payment issues"

3. **Separate probability and impact**: Don't conflate "bad if it happens" with "likely to happen"
   - ✓ Asteroid hits office: Prob=1 (rare), Impact=5 (severe), Score=5 (low priority)
   - ❌ Conflating: "This is really bad so it must be high priority" (ignoring low probability)

4. **Assign named owners, not teams**: "Engineering team" is not accountable, "Sarah (Tech Lead)" is
   - ✓ Owner: Sarah (Tech Lead), responsible for monitoring and activating contingency
   - ❌ Owner: Engineering Team (diffused responsibility)

5. **Define mitigation AND contingency**: Mitigation reduces probability, contingency handles if it occurs anyway
   - ✓ Mitigation: Prototype integration early (reduce prob). Contingency: Build abstraction layer for quick swap (reduce impact)
   - ❌ Only mitigation, no backup plan

6. **Update regularly**: Stale risk register is worse than none (false confidence)
   - ✓ Weekly review for active projects (High/Critical risks), monthly for longer projects
   - ❌ Create register at kickoff, never update (probabilities/impacts change as project progresses)

7. **Retire closed risks**: Don't let register grow indefinitely, archive mitigated/irrelevant risks
   - ✓ Mark risk "Closed" with resolution date, move to archive section
   - ❌ Keep all risks forever (signal-to-noise ratio degrades)

8. **Escalate critical risks immediately**: Don't wait for weekly meeting if Critical risk emerges
   - ✓ Prob=5 Impact=5 Score=25 → Escalate to exec same day, emergency mitigation
   - ❌ Wait for scheduled review (risk could materialize)

## Quick Reference

**Resources:**
- **Quick start**: [resources/template.md](resources/template.md) - Risk register template with scoring table, response planning, monitoring log
- **Advanced techniques**: [resources/methodology.md](resources/methodology.md) - Monte Carlo simulation, decision trees, sensitivity analysis, risk aggregation, earned value management
- **Quality check**: [resources/evaluators/rubric_project_risk_register.json](resources/evaluators/rubric_project_risk_register.json) - Evaluation criteria

**Success criteria:**
- ✓ Identified 15-30 risks across all categories (technical, schedule, resource, external, scope, org)
- ✓ All High/Critical risks (score ≥12) have named owners, mitigation plans, and contingencies
- ✓ Risk scores differentiated (not all scored 6-9; use full 1-25 range)
- ✓ Mitigation and contingency plans are specific and actionable (not "monitor closely")
- ✓ Triggers defined for when to activate contingencies (quantifiable thresholds)
- ✓ Register updated regularly (weekly for active projects, monthly for longer projects)
- ✓ Risk profile matches project phase (high uncertainty at start, decreasing over time)

**Common mistakes:**
- ❌ Too few risks identified (<10) → incomplete risk picture, false confidence
- ❌ All risks scored medium (6-9) → not differentiated, unclear prioritization
- ❌ Vague risks ("things might not work") → not actionable
- ❌ No risk owners assigned → diffused accountability, mitigation doesn't happen
- ❌ Mitigation without contingency → no backup plan if mitigation fails
- ❌ Created once, never updated → stale data, risks evolve
- ❌ Only negative risks (threats) → missing opportunities (positive risks)
- ❌ Risk register separate from project plan → not integrated into workflow

**When to use alternatives:**
- **Pre-mortem**: When project hasn't started, want to imagine failure scenarios (complements risk register)
- **FMEA (Failure Mode Effects Analysis)**: Manufacturing/engineering projects needing detailed failure analysis
- **Monte Carlo simulation**: When need probabilistic timeline/budget forecasting (use methodology.md)
- **Decision tree**: When risks involve sequential decisions with branch points
- **Scenario planning**: When risks are strategic/long-term (market shifts, competitor actions)
