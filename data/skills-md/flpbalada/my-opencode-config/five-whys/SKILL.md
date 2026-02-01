---
name: five-whys
description:
  Conduct root cause analysis using the Five Whys technique. Use when
  investigating problems, debugging issues, understanding failures, analyzing
  churn, or finding the underlying cause of any issue.
---

# Five Whys - Root Cause Analysis

Systematic guide to uncovering root causes through iterative questioning,
originally developed by Sakichi Toyoda for Toyota Motor Corporation.

## When to Use This Skill

- Investigating recurring problems
- Debugging system failures
- Understanding customer churn
- Analyzing project delays or budget overruns
- Post-mortem analysis
- Process improvement initiatives

## Core Concepts

### The Method

```
Problem Statement
    ↓
Why? → Answer 1
    ↓
Why? → Answer 2
    ↓
Why? → Answer 3
    ↓
Why? → Answer 4
    ↓
Why? → Answer 5
    ↓
Root Cause Identified
    ↓
Solution Implementation
```

### Key Principles

| Principle                    | Description                          |
| ---------------------------- | ------------------------------------ |
| **Facts over assumptions**   | Base questions on data, not guesses  |
| **Systems over individuals** | Focus on process failures, not blame |
| **Flexibility**              | Go beyond 5 questions if needed      |
| **Verification**             | Validate findings with evidence      |

## Questioning Techniques

### Standard Approach

For each iteration, ask:

- Why did this happen?
- What caused this situation?
- What led to this outcome?

### Alternative Phrasing (Less Confrontational)

When direct "why" questions feel threatening, use softer alternatives:

#### Root Cause Investigation

| Instead of...        | Try...                                |
| -------------------- | ------------------------------------- |
| Why did this happen? | What was going on when this happened? |
| Why did you do that? | What were you trying to accomplish?   |
| Why is this broken?  | How do you suppose we ended up here?  |

#### Understanding Motivation

| Instead of...         | Try...                                     |
| --------------------- | ------------------------------------------ |
| Why do you want this? | What happens if we don't get this done?    |
| Why does this matter? | What problems does this solve?             |
| Why is this urgent?   | What do you think will happen if we delay? |

#### Understanding Decisions

| Instead of...                   | Try...                                        |
| ------------------------------- | --------------------------------------------- |
| Why did leadership decide this? | What were the reasons we went this direction? |
| Why this approach?              | How do you see this working long term?        |

## Analysis Framework

### Step 1: Define the Problem

Be specific and measurable:

```
❌ Bad:  "The system is slow"
✅ Good: "Page load time increased from 2s to 8s after the March release"

❌ Bad:  "Customers are unhappy"
✅ Good: "Customer churn increased by 40% over three months"
```

### Step 2: Iterate Through Whys

Document each level clearly:

```
Problem: Customer churn increased by 40%

1. Why? → Customers canceling after free trial
2. Why? → Not seeing enough value during trial
3. Why? → Not completing the onboarding process
4. Why? → Onboarding too complex, requires too much setup
5. Why? → Product lacks automation and intelligent defaults

Root Cause: Poor onboarding experience due to lack of automation
```

### Step 3: Identify Solutions

Target the root cause, not symptoms:

```
Symptom-level fix (avoid):
├── Offer discounts to retain customers
└── Send more reminder emails

Root cause fix (preferred):
├── Build automated data import
├── Create intelligent defaults by industry
├── Simplify onboarding to 3 steps
└── Add progress indicators
```

## Output Template

After completing analysis, document as:

```markdown
## Five Whys Analysis

**Problem Statement:** [Clear, measurable problem description]

**Analysis Date:** [Date]

**Participants:** [Who was involved]

### Question Chain

1. **Why?** [First answer with evidence]
2. **Why?** [Second answer with evidence]
3. **Why?** [Third answer with evidence]
4. **Why?** [Fourth answer with evidence]
5. **Why?** [Fifth answer with evidence]

### Root Cause

[Identified root cause - the systemic issue to address]

### Recommended Solutions

| Priority | Solution     | Expected Impact | Effort   |
| -------- | ------------ | --------------- | -------- |
| High     | [Solution 1] | [Impact]        | [Effort] |
| Medium   | [Solution 2] | [Impact]        | [Effort] |
| Low      | [Solution 3] | [Impact]        | [Effort] |

### Success Metrics

- [How will we measure if the solution worked?]
```

## Classic Examples

### Manufacturing Example (Toyota Original)

```
Problem: Machine stopped operating

1. Why? → Motor overheated
2. Why? → Wasn't lubricated enough
3. Why? → Oil pump failed
4. Why? → Filter was clogged
5. Why? → No regular maintenance schedule

Root Cause: Lack of preventive maintenance procedures
Solution: Implement maintenance schedule and checklist
```

### SaaS Example

```
Problem: Customer churn increased 40%

1. Why? → Customers canceling after free trial
2. Why? → Not seeing enough value during trial
3. Why? → Not completing onboarding
4. Why? → Onboarding too complex
5. Why? → Lacks automation and smart defaults

Root Cause: Poor onboarding experience
Solutions:
- Automated data import from popular tools
- Intelligent defaults based on industry
- Simplified 3-step onboarding
- In-app progress indicators

Result: 60% decrease in churn, 35% increase in trial conversion
```

### Software Bug Example

```
Problem: Production API returning 500 errors

1. Why? → Database queries timing out
2. Why? → Query taking 30+ seconds
3. Why? → Missing index on frequently queried column
4. Why? → Index was dropped during migration
5. Why? → Migration script lacked index recreation step

Root Cause: Incomplete migration testing process
Solutions:
- Add index verification to migration checklist
- Implement automated index coverage tests
- Create pre-production performance benchmarks
```

## Best Practices

### Do

- **Use data** - Support answers with evidence and metrics
- **Involve diverse perspectives** - Different viewpoints reduce blind spots
- **Focus on systems** - Ask "what process failed?" not "who failed?"
- **Document everything** - Create audit trail for future reference
- **Verify root cause** - Test that fixing it would prevent recurrence

### Avoid

- **Stopping too early** - Surface answers are usually symptoms
- **Personal blame** - "John made a mistake" is never the root cause
- **Single path** - Complex problems may have multiple root causes
- **Assumptions** - Always verify with data
- **Skipping steps** - Each "why" should logically follow the previous

## Communication Tips

- Give people time to respond - embrace silence
- Ask one question at a time
- Resist the urge to clarify before they answer
- Focus on curiosity rather than interrogation
- Frame as collaborative problem-solving

## Integration with Other Methods

The Five Whys works well alongside:

| Method               | Combined Use                           |
| -------------------- | -------------------------------------- |
| **Kaizen**           | Continuous improvement cycles          |
| **Six Sigma**        | DMAIC problem-solving                  |
| **Fishbone Diagram** | Visualizing multiple cause categories  |
| **Pareto Analysis**  | Prioritizing which problems to analyze |
| **Post-mortem**      | Incident review sessions               |

## Resources

- [Toyota Production System](https://en.wikipedia.org/wiki/Toyota_Production_System)
- [Taiichi Ohno's Workplace Management](https://www.goodreads.com/book/show/843519.Workplace_Management)
- [The Lean Startup - Eric Ries](https://theleanstartup.com/)
