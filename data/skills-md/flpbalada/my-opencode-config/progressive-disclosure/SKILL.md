---
name: progressive-disclosure
description:
  Reduce complexity by revealing information progressively. Use when designing
  onboarding, complex forms, feature-rich interfaces, or any experience where
  showing everything at once would overwhelm users.
---

# Progressive Disclosure - Show the Right Thing at the Right Time

Progressive Disclosure is an interaction design technique that sequences
information and actions across time, showing users only what they need when they
need it. It reduces cognitive load by deferring complexity until the user is
ready for it.

## When to Use This Skill

- Designing onboarding for complex products
- Simplifying feature-rich interfaces
- Creating multi-step forms and wizards
- Building admin panels and settings pages
- Introducing new features to existing users
- Reducing support requests and confusion

## Core Concepts

### The Hierarchy of Disclosure

```
Level 0: Essential (always visible)
    |
    v
Level 1: Important (one click away)
    |
    v
Level 2: Useful (accessible but hidden)
    |
    v
Level 3: Advanced (buried intentionally)
```

### 80/20 Rule Applied

80% of users need 20% of features. Show that 20% prominently, progressively
reveal the rest.

```
+------------------------------------------+
|  Primary Actions (20%)                   |
|  [Action 1] [Action 2]                   |
+------------------------------------------+
|  v Advanced Options                      |
|    +------------------------------------+|
|    | Secondary (30%)                    ||
|    | [Option 3] [Option 4]              ||
|    +------------------------------------+|
|    |  v More Options                    ||
|    |    +------------------------------+||
|    |    | Tertiary (50%)              |||
|    |    | [Rare settings...]          |||
|    |    +------------------------------+||
|    +------------------------------------+|
+------------------------------------------+
```

### Types of Progressive Disclosure

| Type                 | Mechanism            | Example               |
| -------------------- | -------------------- | --------------------- |
| **Click to reveal**  | Expand/collapse      | "Show more" sections  |
| **Hover to reveal**  | Tooltip/popover      | Help text on hover    |
| **Scroll to reveal** | Below the fold       | Long-form content     |
| **Time-based**       | Delayed introduction | Feature announcements |
| **Skill-based**      | Unlock with usage    | Advanced features     |
| **Role-based**       | Permission levels    | Admin controls        |

## Analysis Framework

### Step 1: Audit Current Interface

List all elements users see:

| Element     | User Need | Frequency           | Current Visibility        |
| ----------- | --------- | ------------------- | ------------------------- |
| [Element 1] | [Need]    | [Daily/Weekly/Rare] | [Always/Sometimes/Hidden] |
| [Element 2] | [Need]    | [Daily/Weekly/Rare] | [Always/Sometimes/Hidden] |

### Step 2: Categorize by Priority

```
                    HIGH
                     |
    +----------------+----------------+
    |                |                |
    |  ESSENTIAL     |  CONTEXTUAL    |
    |  Always show   |  Show when     |
    |                |  relevant      |
FREQUENCY           |                NEED
    |                |                |
    |  ACCESSIBLE    |  HIDE          |
    |  One click     |  Deep menus    |
    |  away          |                |
    +----------------+----------------+
                     |
                    LOW
```

### Step 3: Design Disclosure Pattern

| Stage        | What to Show         | How to Reveal Next   |
| ------------ | -------------------- | -------------------- |
| Initial view | [Core elements]      | [Trigger to Level 1] |
| Level 1      | [Secondary elements] | [Trigger to Level 2] |
| Level 2      | [Advanced elements]  | [Trigger to Level 3] |

### Step 4: Test Understanding

- Can users complete primary tasks without expanding?
- Can users find advanced features when needed?
- Is the "expand" affordance clear?

## Output Template

```markdown
## Progressive Disclosure Design

**Interface:** [Name] **Date:** [Date]

### Element Inventory

| Element | Priority  | Disclosure Level | Reveal Trigger |
| ------- | --------- | ---------------- | -------------- |
| [E1]    | Essential | Always visible   | -              |
| [E2]    | Important | Level 1          | [Trigger]      |
| [E3]    | Advanced  | Level 2          | [Trigger]      |

### Disclosure Hierarchy

**Level 0 (Always visible):**

- [Element list]

**Level 1 (One interaction):**

- Trigger: [How user reveals]
- Contents: [Element list]

**Level 2 (Two interactions):**

- Trigger: [How user reveals]
- Contents: [Element list]

### User Flow

1. User sees: [Initial state]
2. To access [feature], user: [Action]
3. System reveals: [New state]

### Success Metrics

| Metric               | Before  | After Target |
| -------------------- | ------- | ------------ |
| Task completion rate | [X%]    | [Y%]         |
| Time to complete     | [X sec] | [Y sec]      |
| Support tickets      | [X/mo]  | [Y/mo]       |
```

## Real-World Examples

### Example 1: Gmail Compose

**Level 0**: To, Subject, Body, Send **Level 1**: CC, BCC (click "Cc" to reveal)
**Level 2**: Formatting toolbar (click "A" to reveal) **Level 3**: Confidential
mode, schedule send (menu)

Most users never need CC/BCC, so it's hidden by default.

### Example 2: Notion Properties

**Level 0**: Page title and content **Level 1**: Basic properties (click to
expand) **Level 2**: Add property, configure property **Level 3**: Database
views, relations, rollups

New users see a simple page; power users unlock complexity.

### Example 3: iPhone Camera

**Level 0**: Shutter button, switch camera **Level 1**: Swipe for modes (Video,
Portrait, etc.) **Level 2**: Tap for exposure/focus controls **Level 3**:
Settings app for advanced options

## Best Practices

### Do

- Make primary actions immediately visible
- Use clear affordances for expanding ("Show more", arrows)
- Remember user preferences for disclosure state
- Provide search/filter for deeply hidden features
- Test with both new and experienced users

### Avoid

- Hiding essential functionality
- Requiring many clicks for common tasks
- Inconsistent disclosure patterns across the product
- Mystery meat navigation (unclear expand triggers)
- Over-hiding to the point of unfindability

### Disclosure Affordances

| Pattern          | When to Use                 |
| ---------------- | --------------------------- |
| "Show more" link | Text content, lists         |
| Chevron/arrow    | Expandable sections         |
| "..." menu       | Actions, options            |
| Tabs             | Parallel content categories |
| Hover reveal     | Tooltips, secondary actions |
| Modal/drawer     | Complex sub-flows           |

## Integration with Other Methods

| Method              | Combined Use                         |
| ------------------- | ------------------------------------ |
| **Hick's Law**      | Reduce visible choices at each level |
| **Cognitive Load**  | Manage working memory limits         |
| **Halo Effect**     | Polish the essential elements first  |
| **Jobs-to-be-Done** | Organize by user jobs                |

## Resources

- [Progressive Disclosure - Nielsen Norman Group](https://www.nngroup.com/articles/progressive-disclosure/)
- [Designing Web Interfaces - Bill Scott](https://www.amazon.com/Designing-Web-Interfaces-Principles-Interactions/dp/0596516258)
