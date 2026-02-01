---
name: kanban
description:
  Visualize and optimize workflow with Kanban boards. Use when managing team
  work, identifying bottlenecks, improving delivery flow, or implementing
  continuous improvement in product development.
---

# Kanban - Visualize Work, Limit WIP, Optimize Flow

Kanban is a visual workflow management method originating from Toyota's
manufacturing system. It focuses on visualizing work, limiting work-in-progress
(WIP), and optimizing the flow of work through a system.

## When to Use This Skill

- Managing team workflow and task prioritization
- Identifying and resolving bottlenecks
- Improving delivery predictability
- Balancing team capacity with demand
- Implementing continuous improvement
- Transitioning from chaotic to structured work

## Core Concepts

### The Kanban Board

```
+----------+----------+----------+----------+
|  TO DO   |  DOING   |  REVIEW  |   DONE   |
|          |  (WIP:3) |  (WIP:2) |          |
+----------+----------+----------+----------+
| [Task 1] | [Task 4] | [Task 6] | [Task 8] |
| [Task 2] | [Task 5] |          | [Task 9] |
| [Task 3] |          |          |          |
+----------+----------+----------+----------+
```

### Six Core Practices

| Practice                     | Description                        |
| ---------------------------- | ---------------------------------- |
| **Visualize workflow**       | Make all work visible on the board |
| **Limit WIP**                | Cap items in each stage            |
| **Manage flow**              | Track and optimize throughput      |
| **Make policies explicit**   | Document rules for moving work     |
| **Implement feedback loops** | Regular reviews and retrospectives |
| **Improve collaboratively**  | Evolve process based on data       |

### Key Metrics

| Metric         | Definition                  | Why It Matters       |
| -------------- | --------------------------- | -------------------- |
| **Lead Time**  | Request → Delivery          | Customer perspective |
| **Cycle Time** | Work Started → Done         | Team efficiency      |
| **Throughput** | Items completed per period  | Capacity planning    |
| **WIP**        | Items currently in progress | Flow health          |

### Little's Law

```
Lead Time = WIP / Throughput

To reduce lead time:
- Reduce WIP (easier)
- Increase throughput (harder)
```

## Analysis Framework

### Step 1: Map Current Workflow

Identify all stages work passes through:

```
Idea → Backlog → Analysis → Development → Testing → Deploy → Done
```

### Step 2: Set WIP Limits

Start with: WIP limit = Team size - 1

| Stage  | Team Members | Initial WIP Limit |
| ------ | ------------ | ----------------- |
| Dev    | 4            | 3                 |
| Review | 2            | 2                 |
| Test   | 2            | 2                 |

### Step 3: Identify Bottlenecks

Look for columns where work accumulates:

```
+------+------+------+------+
| Dev  |Review| TEST | Done |
+------+------+------+------+
| [1]  | [4]  | [8]  | [9]  |
| [2]  | [5]  | [10] |      |
| [3]  | [6]  |      |      |
|      | [7]  |      |  ← Bottleneck in Review
+------+------+------+------+
```

### Step 4: Optimize Flow

Actions to address bottlenecks:

- Add capacity to bottleneck stage
- Reduce WIP in preceding stages
- Improve efficiency at bottleneck
- Change policies (batch size, etc.)

## Output Template

```markdown
## Kanban Board Setup

**Team/Project:** [Name] **Date:** [Date]

### Workflow Stages

| Stage     | WIP Limit | Entry Criteria | Exit Criteria |
| --------- | --------- | -------------- | ------------- |
| [Stage 1] | [n]       | [Criteria]     | [Criteria]    |
| [Stage 2] | [n]       | [Criteria]     | [Criteria]    |

### Current Metrics

| Metric     | Current  | Target   |
| ---------- | -------- | -------- |
| Lead Time  | [X days] | [Y days] |
| Cycle Time | [X days] | [Y days] |
| Throughput | [X/week] | [Y/week] |

### Bottleneck Analysis

**Current bottleneck:** [Stage] **Root cause:** [Analysis] **Action plan:**
[Steps to resolve]

### Improvement Experiments

| Experiment | Hypothesis         | Measure  | Duration |
| ---------- | ------------------ | -------- | -------- |
| [Change 1] | [Expected outcome] | [Metric] | [Time]   |
```

## Real-World Examples

### Example 1: Software Development Team

**Before**: 15 items in progress, 3-week average delivery **After**: 6 WIP
limit, 5-day average delivery

Changes:

- Visualized all work (including hidden tasks)
- Set WIP limits (forced focus)
- Daily standups at the board
- Swarming on blocked items

### Example 2: Content Marketing Team

```
+--------+--------+--------+--------+--------+
| Ideas  | Draft  | Edit   | Design | Publish|
| (10)   | WIP:3  | WIP:2  | WIP:2  |        |
+--------+--------+--------+--------+--------+
```

Bottleneck discovered: Design stage Solution: Created template library, reduced
design dependency

## Best Practices

### Do

- Start with current process, evolve gradually
- Make WIP limits visible and enforced
- Track metrics consistently
- Review board in daily standups
- Celebrate flow improvements

### Avoid

- Treating Kanban as just a task board
- Setting WIP limits too high (defeats purpose)
- Ignoring blocked items
- Skipping retrospectives
- Comparing team throughput to others

### WIP Limit Guidelines

| Situation                  | Adjustment         |
| -------------------------- | ------------------ |
| Items stuck too long       | Lower WIP          |
| Team has idle time         | Raise WIP slightly |
| Too much context switching | Lower WIP          |
| Bottleneck forming         | Address root cause |

## Integration with Other Methods

| Method              | Combined Use                                |
| ------------------- | ------------------------------------------- |
| **Hypothesis Tree** | Investigate flow problems                   |
| **Five Whys**       | Find root cause of bottlenecks              |
| **Cognitive Load**  | Justify WIP limits (context switching cost) |

## Resources

- [Kanban - David J. Anderson](https://www.amazon.com/Kanban-Successful-Evolutionary-Technology-Business/dp/0984521402)
- [Making Work Visible - Dominica DeGrandis](https://www.amazon.com/Making-Work-Visible-Exposing-Optimize/dp/1942788150)
