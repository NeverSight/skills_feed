---
name: hicks-law
description:
  Optimize decision-making speed by managing choice quantity. Use when designing
  navigation, menus, feature sets, onboarding flows, or any interface where
  users must choose between options.
---

# Hick's Law - Less Choice, Faster Decisions

Hick's Law (also Hick-Hyman Law) states that the time it takes to make a
decision increases logarithmically with the number and complexity of choices.
Named after British psychologist William Edmund Hick and American psychologist
Ray Hyman (1952).

## When to Use This Skill

- Designing navigation menus and information architecture
- Simplifying onboarding and setup flows
- Reducing form field options
- Prioritizing feature exposure
- Optimizing conversion funnels
- Planning dashboard layouts

## Core Concepts

### The Formula

```
RT = a + b * log2(n+1)

Where:
RT = Reaction time
a  = Time not involved in decision (physical movement, etc.)
b  = Empirical constant (~0.155s for choice tasks)
n  = Number of equally probable choices
```

### Practical Impact

| Choices | Relative Decision Time | User Experience       |
| ------- | ---------------------- | --------------------- |
| 2       | Baseline               | Quick, confident      |
| 4       | +1 unit                | Still manageable      |
| 8       | +2 units               | Starting to slow      |
| 16      | +3 units               | Noticeable hesitation |
| 32      | +4 units               | Overwhelm begins      |
| 64+     | +5+ units              | Paralysis likely      |

### The Paradox of Choice

```
       User Satisfaction
            ^
            |      *
            |   *     *
            |  *        *
            | *           *
            |*              *____
            +-----------------------> Number of Choices
                 Sweet spot
                (4-7 items)
```

## Analysis Framework

### Step 1: Audit Decision Points

Map all places users must choose:

| Screen/Flow | Decision Type | Options Count | Complexity |
| ----------- | ------------- | ------------- | ---------- |
| [Screen 1]  | Navigation    | [n]           | [H/M/L]    |
| [Screen 2]  | Selection     | [n]           | [H/M/L]    |
| [Screen 3]  | Configuration | [n]           | [H/M/L]    |

### Step 2: Categorize Choices

```
Essential (keep)     Nice-to-have (maybe)     Remove
       |                    |                    |
       v                    v                    v
   [_______]            [_______]            [_______]
   [_______]            [_______]            [_______]
   [_______]            [_______]            [_______]
```

### Step 3: Apply Reduction Strategies

1. **Chunking**: Group related items (3-4 per group)
2. **Progressive disclosure**: Hide advanced options
3. **Smart defaults**: Pre-select the common choice
4. **Filtering**: Let users narrow options
5. **Recommendations**: Highlight "Most Popular"

## Output Template

```markdown
## Hick's Law Analysis

**Interface/Flow:** [Name] **Analysis Date:** [Date]

### Decision Point Inventory

| Location  | Current Options | Target | Strategy             |
| --------- | --------------- | ------ | -------------------- |
| [Point 1] | [n]             | [n]    | [Chunk/Hide/Default] |
| [Point 2] | [n]             | [n]    | [Chunk/Hide/Default] |

### Reduction Plan

**Quick wins (no functionality loss):**

1. [Change 1]
2. [Change 2]

**Strategic reductions (requires tradeoffs):**

1. [Change with impact analysis]

### Expected Impact

- Decision time reduction: ~[X]%
- Conversion improvement: ~[X]% (estimated)
- Support ticket reduction: ~[X]% (estimated)
```

## Real-World Examples

### Example 1: Netflix vs. Cable

**Cable TV**: 500+ channels = Decision paralysis

- Users spend more time browsing than watching
- Satisfaction decreases despite more options

**Netflix approach**:

- Curated rows (chunking)
- "Top 10" highlights (social proof + reduction)
- "Because you watched..." (personalized filtering)
- Auto-play (eliminates decision entirely)

### Example 2: In-N-Out Burger

Menu has only 4 items vs. competitors' 50+:

- Order time: 30 seconds vs. 2+ minutes
- Customer satisfaction: Higher
- Operation efficiency: Better

The constraint creates confidence in choice quality.

### Example 3: Slack's Onboarding

Original: 15 configuration options upfront

- Completion rate: 62%
- Time to complete: 8 minutes

Redesigned: 3 essential questions, rest defaulted

- Completion rate: 89%
- Time to complete: 2 minutes

## Best Practices

### Do

- Aim for 5-7 options maximum in any grouping
- Use categorization to chunk larger sets
- Provide clear visual hierarchy
- Make the "default" choice obvious
- Offer search/filter for large option sets

### Avoid

- Showing all features at once
- Flat menus with 10+ items
- Requiring decisions without clear benefit
- Equal visual weight for all options
- Removing options users actively need

### When Hick's Law Doesn't Apply

- Expert users with learned shortcuts
- Emergency situations (trained responses)
- When options are not equally weighted
- Sequential vs. parallel choices

## Reduction Techniques

### 1. Smart Defaults

```
Instead of:
[ ] Option A
[ ] Option B
[ ] Option C

Do:
[x] Option B (Recommended)
[ ] Option A
[ ] Option C
```

### 2. Progressive Disclosure

```
Basic Options
[Configure]

v Advanced (click to expand)
  [_] Setting 1
  [_] Setting 2
```

### 3. Chunking

```
Instead of 12 flat options:

Category A        Category B        Category C
- Item 1          - Item 5          - Item 9
- Item 2          - Item 6          - Item 10
- Item 3          - Item 7          - Item 11
- Item 4          - Item 8          - Item 12
```

## Integration with Other Methods

| Method                     | Combined Use                           |
| -------------------------- | -------------------------------------- |
| **Progressive Disclosure** | Hide complexity, reveal on demand      |
| **Cognitive Load**         | Fewer choices = lower cognitive burden |
| **Fogg Behavior Model**    | Simpler choices increase ability       |
| **Jobs-to-be-Done**        | Focus options on user's actual job     |

## Resources

- [On the Rate of Gain of Information - Hick (1952)](https://psycnet.apa.org/record/1953-03853-001)
- [The Paradox of Choice - Barry Schwartz](https://www.amazon.com/Paradox-Choice-Why-More-Less/dp/0060005696)
- [Don't Make Me Think - Steve Krug](https://sensible.com/dont-make-me-think/)
