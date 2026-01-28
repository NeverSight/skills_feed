---
name: eisenhower
description: Eisenhower Matrix prioritization categorizing tasks by urgency and importance into Do, Schedule, Delegate, Eliminate quadrants. Use for task prioritization, time management, or when overwhelmed.
user-invocable: true
---

# Eisenhower Matrix Prioritization

Categorize tasks by urgency and importance to clarify what to do, schedule, delegate, or eliminate.

## Instructions

Take the list of tasks provided and sort them into the four quadrants. Be honest about what's truly important (moves you toward goals) versus just urgent (feels pressing but may not matter).

### Output Format

**Context**
What role/area are we prioritizing for? What's the time horizon?

**The Matrix**

```
                    URGENT              NOT URGENT
              ┌─────────────────┬─────────────────┐
   IMPORTANT  │    Q1: DO       │   Q2: SCHEDULE  │
              │                 │                 │
              ├─────────────────┼─────────────────┤
NOT IMPORTANT │   Q3: DELEGATE  │   Q4: ELIMINATE │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

### Q1: DO (Urgent + Important)
*Handle these immediately—real deadlines, crises, problems*

| Task | Why Urgent? | Why Important? | Do By |
|------|-------------|----------------|-------|
| [task] | [urgency] | [importance] | [when] |

### Q2: SCHEDULE (Not Urgent + Important)
*Block time for these—they don't scream but they matter most*

| Task | Why Important? | Schedule For | Time Needed |
|------|----------------|--------------|-------------|
| [task] | [importance] | [when] | [duration] |

### Q3: DELEGATE (Urgent + Not Important)
*Someone else can do these—or reduce their urgency*

| Task | Why Urgent? | Who Can Handle? | Delegation Plan |
|------|-------------|-----------------|-----------------|
| [task] | [urgency] | [who] | [how] |

### Q4: ELIMINATE (Not Urgent + Not Important)
*Stop doing these—or radically reduce time spent*

| Task | Why Are You Doing This? | Elimination Strategy |
|------|-------------------------|---------------------|
| [task] | [reason] | [how to stop] |

**Time Distribution Analysis**

| Quadrant | % of Time | Ideal % |
|----------|-----------|---------|
| Q1: Do | X% | 20-25% |
| Q2: Schedule | X% | 60-70% |
| Q3: Delegate | X% | 10-15% |
| Q4: Eliminate | X% | <5% |

**First Actions**
1. Do now: [Q1 task]
2. Schedule this week: [Q2 task with specific time block]
3. Delegate today: [Q3 task with handoff plan]

## Guidelines

- "Urgent" = external deadline or consequence for delay
- "Important" = contributes to goals, values, long-term success
- Other people's urgency isn't automatically yours
- Q2 tasks become Q1 if neglected—that's how fires start
- Be honest: Q4 tasks often feel productive but aren't

$ARGUMENTS
