---
name: client-discovery
description: Sales qualification and client discovery. Use when starting a new client engagement, qualifying leads, identifying pain points, or calculating ROI for automation proposals. Generates discovery forms, qualification scores, and ROI estimates.
---

# Client Discovery

Qualify leads faster and identify high-value automation opportunities.

## Quick Actions

| Need | Action |
|------|--------|
| Discovery call prep | → Questions Below |
| Pain point mapping | → `references/pain-points.md` |
| ROI estimation | → `references/roi-formulas.md` |
| Full questionnaire | → `references/questions.md` |
| Intake form | → `assets/templates/discovery-form.md` |

## Discovery Process

### Phase 1: Pre-Call Research (5 min)

Before the call, gather:
1. **Company**: Size, industry, tech stack (LinkedIn, Crunchbase)
2. **Contact**: Role, tenure, decision authority
3. **Signals**: Recent funding, hiring, complaints on G2/social
4. **Competition**: Who else they might be talking to

### Phase 2: Discovery Call Structure (30 min)

```
[5 min] Rapport & Agenda
[15 min] Pain Discovery
[5 min] Impact Quantification
[5 min] Next Steps
```

### Phase 3: Core Discovery Questions

#### Business Context
1. "Walk me through your typical [process] from start to finish."
2. "Who's involved at each step?"
3. "What tools do you use today?"

#### Pain Identification
4. "What breaks most often?"
5. "What takes longer than it should?"
6. "What would happen if this didn't get done?"

#### Quantification
7. "How many hours per week does this take?"
8. "How many people are involved?"
9. "What's the cost of an error here?"

#### Decision Process
10. "Who else needs to approve this?"
11. "What's your timeline for solving this?"
12. "Have you tried to fix this before?"

## Qualification Framework: BANT+

| Criteria | Question | Green | Yellow | Red |
|----------|----------|-------|--------|-----|
| **Budget** | "What would you pay to solve this?" | Has budget | Can find budget | No budget |
| **Authority** | "Who approves this?" | Decision maker | Influencer | User only |
| **Need** | "How urgent is this?" | Immediate pain | Nice to have | Exploring |
| **Timeline** | "When do you need it?" | This month | This quarter | Someday |
| **Pain Score** | Hours × Cost × Frequency | >$2k/mo waste | $500-2k/mo | <$500/mo |

### Scoring

```
Score each BANT+ criteria: Green=3, Yellow=2, Red=1

Total Score:
- 13-15: HOT - Prioritize, fast proposal
- 9-12: WARM - Nurture, build case
- 5-8: COLD - Qualify out or long-term
```

## Pain Point Discovery

### Universal Pain Signals

| Signal | What They Say | Real Pain |
|--------|---------------|-----------|
| Time waste | "We spend hours on..." | Manual data entry |
| Errors | "Things fall through cracks" | No system of record |
| Delays | "It takes too long to..." | Sequential bottleneck |
| Frustration | "I hate doing..." | Repetitive task |
| Risk | "We worry about..." | Compliance/quality |

### Probing Questions

When they mention a pain:
1. "How often does this happen?"
2. "What do you do when it happens?"
3. "Who gets affected?"
4. "What does it cost you?"
5. "How long has this been going on?"

### Pain Severity Matrix

```
           Low Frequency    High Frequency
High Cost   [AUTOMATE]       [URGENT]
Low Cost    [IGNORE]         [AUTOMATE]
```

## ROI Quick Calculator

### Input Variables
```
Hours/week on task: [H]
People involved: [P]
Hourly cost (fully loaded): [C]
Error rate: [E]%
Cost per error: [EC]
```

### Formulas
```
Monthly Labor Cost = H × P × C × 4.33
Monthly Error Cost = (H × P × 4.33) × E × EC / 100
Total Monthly Waste = Labor + Error Cost

Automation Savings = Total × 80% (conservative)
Your Price Target = Savings × 15-25%
Payback Period = Setup Cost ÷ Monthly Savings
```

### Example
```
Task: Manual invoice processing
Hours: 10/week
People: 2
Rate: $35/hr
Error: 5%
Error cost: $200

Labor: 10 × 2 × $35 × 4.33 = $3,031/mo
Errors: (10 × 2 × 4.33) × 5% × $200 / 100 = $87/mo
Total: $3,118/mo

Automation saves: $2,494/mo (80%)
Your price: $374-$624/mo (15-25%)
```

## Vertical-Specific Discovery

### E-commerce
- "How do you handle out-of-stock notifications?"
- "Walk me through an order from purchase to delivery."
- "What happens when a customer disputes a charge?"

### Professional Services
- "How do you track billable hours?"
- "What's your invoicing process?"
- "How do new clients get onboarded?"

### Logistics
- "How do you notify customers of delays?"
- "What happens when a delivery fails?"
- "How do you optimize routes?"

### Legal/Finance
- "How do you track document versions?"
- "What's your approval process?"
- "How do you ensure compliance?"

See `references/pain-points.md` for complete vertical-specific questions.

## Discovery Output

After call, document:

```markdown
# Discovery Summary: [Company]

## Contact
- Name: [X]
- Role: [X]
- Authority: [Decision Maker / Influencer / User]

## BANT+ Score: [X/15]
- Budget: [G/Y/R] - Notes
- Authority: [G/Y/R] - Notes
- Need: [G/Y/R] - Notes
- Timeline: [G/Y/R] - Notes
- Pain: [G/Y/R] - $X/mo waste

## Top 3 Pain Points
1. [Pain] - [Impact] - [Urgency]
2. [Pain] - [Impact] - [Urgency]
3. [Pain] - [Impact] - [Urgency]

## Recommended Solution
[1-2 sentences on automation]

## ROI Estimate
- Current cost: $X/mo
- Automation saves: $Y/mo
- Price range: $Z/mo
- Payback: N days

## Next Steps
- [ ] Send proposal by [date]
- [ ] Follow-up call [date]
- [ ] [Other action]

## Notes
[Anything else important]
```

## Red Flags (Disqualify)

- No clear problem (just "exploring AI")
- No budget and won't discuss
- No authority and won't intro decision maker
- Bad-mouthed previous vendors
- Wants custom enterprise for SMB price
- Endless "one more question"

## References

| Topic | File |
|-------|------|
| Pain Points by Vertical | `references/pain-points.md` |
| ROI Calculation Details | `references/roi-formulas.md` |
| Full Question Bank | `references/questions.md` |

## Templates

| Template | File |
|----------|------|
| Client Intake Form | `assets/templates/discovery-form.md` |
