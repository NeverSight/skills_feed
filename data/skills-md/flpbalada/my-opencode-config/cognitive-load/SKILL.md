---
name: cognitive-load
description:
  Design experiences that optimize mental resources using Cognitive Load Theory.
  Use when designing interfaces, creating onboarding flows, planning information
  architecture, or improving task completion rates.
---

# Cognitive Load - Designing for Human Memory

Cognitive Load Theory (CLT), developed by John Sweller, provides a framework for
designing experiences that work with human working memory limitations.
Understanding the three types of cognitive load helps create interfaces that
feel effortless and intuitive.

## When to Use This Skill

- Designing complex forms or workflows
- Creating onboarding experiences
- Simplifying feature-rich interfaces
- Improving task completion rates
- Planning information architecture
- Reviewing designs for usability

## Working Memory Limitations

```
Human Processing Capacity:

┌─────────────────────────────────────────────────────┐
│              WORKING MEMORY                          │
│                                                      │
│    Capacity: 7 ± 2 items simultaneously             │
│    Duration: ~20 seconds without rehearsal          │
│    Processing: Serial, not parallel                 │
│                                                      │
│    When exceeded → Errors, frustration, abandonment │
└─────────────────────────────────────────────────────┘

Design goal: Stay WITHIN capacity limits.
```

## Three Types of Cognitive Load

```
Total Cognitive Load = Intrinsic + Extraneous + Germane

┌─────────────────────────────────────────────────────────────────┐
│                    WORKING MEMORY CAPACITY                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   INTRINSIC     │   EXTRANEOUS    │          GERMANE            │
│                 │                 │                             │
│   Task          │   Bad design    │   Learning &                │
│   complexity    │   noise         │   schema building           │
│                 │                 │                             │
│   Can't reduce  │   ELIMINATE     │   MAXIMIZE                  │
│   without       │   THIS          │   THIS                      │
│   changing task │                 │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### 1. Intrinsic Load

**What it is:** The inherent difficulty of the task itself.

| Characteristic                | Example                                |
| ----------------------------- | -------------------------------------- |
| Determined by task complexity | Filing taxes vs. sending email         |
| Varies by user expertise      | Expert finds it easy, novice struggles |
| Cannot be eliminated          | Only managed through design            |

**Design strategies:**

- Break complex tasks into smaller steps
- Provide progressive disclosure
- Build on existing mental models
- Offer different paths for different expertise levels

### 2. Extraneous Load

**What it is:** Unnecessary mental effort from poor design.

```
Common Sources of Extraneous Load:

Visual:
├── Cluttered layouts
├── Poor typography
├── Inconsistent patterns
└── Distracting animations

Interaction:
├── Unclear navigation
├── Unexpected behaviors
├── Too many options
└── Hidden functionality

Content:
├── Jargon and complexity
├── Redundant information
├── Missing context
└── Poor information hierarchy
```

**Design strategies:**

- Eliminate decorative elements without purpose
- Use consistent design patterns
- Apply strong visual hierarchy
- Remove redundant information

### 3. Germane Load

**What it is:** Productive mental effort that builds understanding.

| Benefit                        | Example                       |
| ------------------------------ | ----------------------------- |
| Builds mental models           | User learns system behavior   |
| Enables efficiency             | Experienced user works faster |
| Creates transferable knowledge | Skills apply to similar tasks |

**Design strategies:**

- Provide clear feedback on actions
- Create learnable, consistent patterns
- Design onboarding that builds foundations
- Use progressive enhancement for power features

## Load Analysis Framework

### Step 1: Map the Task

```
Task Decomposition:

[Main Task]
├── Step 1: [Action] → Load type: [I/E/G]
│   └── Decisions required: [count]
├── Step 2: [Action] → Load type: [I/E/G]
│   └── Decisions required: [count]
├── Step 3: [Action] → Load type: [I/E/G]
│   └── Decisions required: [count]
└── Completion
```

### Step 2: Identify Load Sources

For each step, categorize the cognitive demands:

| Step | Intrinsic Load    | Extraneous Load | Germane Load     |
| ---- | ----------------- | --------------- | ---------------- |
| 1    | [Task complexity] | [Design issues] | [Learning value] |
| 2    | [Task complexity] | [Design issues] | [Learning value] |
| 3    | [Task complexity] | [Design issues] | [Learning value] |

### Step 3: Design Interventions

```
Intervention Strategy:

High Intrinsic Load?
├── YES → Break into smaller steps
├── YES → Add progressive disclosure
├── YES → Provide scaffolding/help
└── YES → Offer simplified path

High Extraneous Load?
├── YES → Remove unnecessary elements
├── YES → Improve visual hierarchy
├── YES → Simplify navigation
└── YES → Fix inconsistent patterns

Low Germane Load?
├── YES → Add meaningful feedback
├── YES → Create learnable patterns
├── YES → Design for skill building
└── YES → Connect to existing knowledge
```

## Output Template

After completing analysis, document as:

```markdown
## Cognitive Load Analysis

**Feature/Flow:** [Name]

**Date:** [Date]

### Task Map

| Step | Description | Intrinsic    | Extraneous   | Germane      |
| ---- | ----------- | ------------ | ------------ | ------------ |
| 1    | [Step]      | High/Med/Low | High/Med/Low | High/Med/Low |
| 2    | [Step]      | High/Med/Low | High/Med/Low | High/Med/Low |

### Load Issues Identified

#### Intrinsic Load Problems

- [Issue]: [Location]
- [Issue]: [Location]

#### Extraneous Load Problems

- [Issue]: [Location]
- [Issue]: [Location]

### Recommendations

| Priority | Change            | Expected Impact       |
| -------- | ----------------- | --------------------- |
| High     | [Specific change] | [Reduces X load by Y] |
| Medium   | [Specific change] | [Reduces X load by Y] |

### Success Metrics

| Metric               | Current | Target |
| -------------------- | ------- | ------ |
| Task completion rate | X%      | Y%     |
| Time to complete     | X min   | Y min  |
| Error rate           | X%      | Y%     |
| User satisfaction    | X       | Y      |
```

## Real-World Examples

### Google Search

```
Load Optimization:

Intrinsic:  Minimal - just type what you want
Extraneous: Near zero - white space + search box
Germane:    Focus on learning query refinement

Result: 2-3x faster searches than competitors
```

### Slack Progressive Disclosure

```
New User Experience:
├── Basic: Messaging interface only
├── Intermediate: Threading, channels
├── Advanced: Integrations, workflows
└── Enterprise: Admin controls

Each level builds on previous knowledge (germane load)
without overwhelming new users (extraneous load).
```

### Apple iOS Consistency

```
System-wide Patterns:

Gestures:
├── Swipe from left = back (everywhere)
├── Pull down = refresh (everywhere)
├── Long press = more options (everywhere)
└── Pinch = zoom (everywhere)

Consistency eliminates extraneous load.
Users learn once, apply everywhere.
```

## Design Strategies by Load Type

### Reducing Intrinsic Load

| Strategy               | Implementation            |
| ---------------------- | ------------------------- |
| Task chunking          | Max 3-5 items per screen  |
| Mental model alignment | Use familiar metaphors    |
| Smart defaults         | Pre-select common choices |
| Contextual help        | Show info when needed     |

### Eliminating Extraneous Load

| Strategy               | Implementation                        |
| ---------------------- | ------------------------------------- |
| Visual hierarchy       | Size, color, position guide attention |
| Consistent patterns    | Same action = same interaction        |
| Content prioritization | Most important info first             |
| Distraction removal    | No unnecessary animations/elements    |

### Optimizing Germane Load

| Strategy                | Implementation                     |
| ----------------------- | ---------------------------------- |
| Clear feedback          | Show results of every action       |
| Pattern consistency     | Create learnable behaviors         |
| Progressive enhancement | Reveal features as expertise grows |
| Knowledge transfer      | Design transferable skills         |

## Measurement Approaches

### Quantitative

- Task completion time
- Error rate and recovery time
- Number of help requests
- Tab/window switches during task
- Abandonment points

### Qualitative

- Think-aloud testing (confusion points)
- Cognitive walkthroughs (step-by-step effort)
- Post-task interviews (perceived difficulty)
- Eye tracking (scanning patterns)

## Integration with Other Methods

| Method                     | Combined Use                                 |
| -------------------------- | -------------------------------------------- |
| **Cognitive Fluency**      | Fluency is one way to reduce extraneous load |
| **Hick's Law**             | Fewer choices = lower load                   |
| **Progressive Disclosure** | Manage intrinsic load over time              |
| **Graph Thinking**         | Map load relationships across system         |
| **Five Whys**              | Why are users struggling/abandoning?         |

## Quick Reference

```
COGNITIVE LOAD CHECKLIST

Intrinsic Load Management:
□ Tasks broken into 3-5 step chunks
□ Progressive disclosure for complexity
□ Different paths for different expertise
□ Builds on familiar concepts

Extraneous Load Elimination:
□ Clear visual hierarchy
□ Consistent interaction patterns
□ No unnecessary decorative elements
□ Logical information architecture

Germane Load Optimization:
□ Clear feedback on all actions
□ Patterns that transfer across features
□ Onboarding builds mental models
□ Advanced features reward learning

Testing:
□ Task completion measured
□ Error rates tracked
□ User confusion points identified
□ Learning curve improving over time
```

## Resources

- [Cognitive Load Theory - John Sweller](https://www.instructionaldesign.org/theories/cognitive-load/)
- [Don't Make Me Think - Steve Krug](https://sensible.com/dont-make-me-think/)
- [Laws of UX](https://lawsofux.com/)
- [Nielsen Norman Group - Cognitive Load](https://www.nngroup.com/articles/minimize-cognitive-load/)
