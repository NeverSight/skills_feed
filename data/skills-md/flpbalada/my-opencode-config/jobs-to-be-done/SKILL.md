---
name: jobs-to-be-done
description:
  Understand customer motivations through job theory. Use when defining product
  strategy, conducting user research, identifying competitors, writing user
  stories, or reframing features around customer progress.
---

# Jobs-to-be-Done - What Are Customers Really Hiring?

Jobs-to-be-Done (JTBD) is a framework developed by Clayton Christensen and Bob
Moesta that focuses on the progress customers are trying to make in their lives.
Instead of asking "who is the customer?" it asks "what job are they hiring this
product to do?"

## When to Use This Skill

- Defining product strategy and positioning
- Conducting customer research interviews
- Writing user stories and requirements
- Identifying true competitors (often surprising)
- Finding innovation opportunities
- Understanding why customers switch products

## Core Concepts

### The Hiring Metaphor

```
Customer has a "job" to get done
           |
           v
    +-------------+
    | "Hires" a   |
    | product to  |
    | do the job  |
    +-------------+
           |
           v
   If it does well → keeps using
   If it fails → "fires" it, tries another
```

### The Milkshake Story

Clayton Christensen's famous example:

**Traditional approach**: "Who buys milkshakes? Demographics, preferences..."

**JTBD approach**: "What job is the milkshake being hired to do?"

Discovery: Morning milkshake buyers had a completely different job than
afternoon buyers.

| Time      | Job to Be Done                                                       | Competition                      |
| --------- | -------------------------------------------------------------------- | -------------------------------- |
| Morning   | "Make my boring commute more interesting + keep me full until lunch" | Bagels, bananas, coffee          |
| Afternoon | "Treat my child after a long day"                                    | Toys, playground time, ice cream |

### Types of Jobs

| Type           | Description                  | Example                                    |
| -------------- | ---------------------------- | ------------------------------------------ |
| **Functional** | Practical task to accomplish | "Help me file my taxes correctly"          |
| **Emotional**  | How I want to feel           | "Make me feel confident about my finances" |
| **Social**     | How I want to be perceived   | "Show others I'm responsible"              |

### Job Statement Format

```
When [situation/context]
I want to [motivation/job]
So I can [expected outcome]
```

## Analysis Framework

### Step 1: Identify the Job

Interview questions to uncover jobs:

| Question                                     | Purpose                |
| -------------------------------------------- | ---------------------- |
| "Walk me through the last time you [action]" | Get specific context   |
| "What were you trying to accomplish?"        | Uncover functional job |
| "How did that make you feel?"                | Uncover emotional job  |
| "What did you try before this?"              | Identify competition   |

### Step 2: Map the Forces

```
+------------------+------------------+
|   PUSH           |    PULL          |
|   (away from)    |    (toward)      |
|                  |                  |
| - Current pain   | - Better outcome |
| - Frustration    | - Emotional gain |
+------------------+------------------+
        |                   |
        v                   v
+------------------+------------------+
|   ANXIETY        |   HABITS         |
|   (of new)       |   (of old)       |
|                  |                  |
| - Will it work?  | - "I've always   |
| - Learning curve |    done it this  |
+------------------+    way"          |
                   +------------------+
```

For customers to switch: **Push + Pull > Anxiety + Habits**

### Step 3: Define True Competition

True competitors are anything hired for the same job:

**Job**: "Help me fall asleep faster"

| JTBD View   |
| ----------- |
| Sleep apps  |
| Melatonin   |
| White noise |
| Reading     |
| Exercise    |
| Wine        |

## Output Template

```markdown
## Jobs-to-be-Done Analysis

**Product/Feature:** [Name]

### Core Job Statement

When [situation] I want to [motivation] So I can [outcome]

### Job Dimensions

**Functional:** [What they're trying to accomplish] **Emotional:** [How they
want to feel] **Social:** [How they want to be perceived]

### Forces Analysis

**Push:** [Pain points driving change] **Pull:** [Benefits of new solution]
**Anxieties:** [Concerns about switching] **Habits:** [Behaviors keeping them in
place]

### True Competition

| Competitor | Job Performance |
| ---------- | --------------- |
| [Alt 1]    | [How well]      |
| [Alt 2]    | [How well]      |
```

## Real-World Examples

### Example 1: Snickers vs. Milky Way

| Product   | Job                                             | Competitors        |
| --------- | ----------------------------------------------- | ------------------ |
| Snickers  | "I'm hungry and need a quick, filling snack"    | Protein bars, nuts |
| Milky Way | "I want to treat myself to something indulgent" | Ice cream, cookies |

### Example 2: LinkedIn Learning

**Not hired for**: "I want to learn Python" (Udemy does this) **Hired for**: "I
want to show my employer I'm developing professionally"

## Best Practices

### Do

- Interview actual users about real past behavior
- Focus on the "hiring moment" and context
- Look for workarounds and "non-consumption"
- Identify emotional and social jobs

### Avoid

- Asking what features users want
- Taking stated preferences at face value
- Ignoring context and situation
- Focusing only on functional jobs

## Integration with Other Methods

| Method                  | Combined Use                       |
| ----------------------- | ---------------------------------- |
| **Hypothesis Tree**     | Structure job discovery hypotheses |
| **Five Whys**           | Dig into underlying motivations    |
| **Fogg Behavior Model** | Design for job completion          |

## Resources

- [Competing Against Luck - Clayton Christensen](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612)
- [The Jobs to be Done Playbook - Jim Kalbach](https://www.amazon.com/Jobs-Be-Done-Playbook-Organization/dp/1933820683)
