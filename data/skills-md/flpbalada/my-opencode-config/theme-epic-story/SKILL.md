---
name: theme-epic-story
description:
  Structure product work hierarchically using themes, epics, and stories. Use
  when organizing backlogs, planning releases, communicating with stakeholders,
  or breaking down large initiatives into manageable work.
---

# Theme, Epic, Story - Hierarchical Product Work Structure

A framework for organizing product work at multiple levels of granularity. This
hierarchy helps teams plan strategically while maintaining clear, actionable
work items that can be completed within sprints.

## When to Use This Skill

- Organizing product backlogs
- Planning releases and roadmaps
- Breaking down large initiatives
- Communicating with stakeholders at different levels
- Estimating effort for large features
- Prioritizing work across teams

## Hierarchy Overview

```
PRODUCT WORK HIERARCHY

Theme (Strategic)
│
├── Epic (Tactical)
│   ├── Story (Operational)
│   ├── Story
│   └── Story
│
├── Epic
│   ├── Story
│   ├── Story
│   └── Story
│
└── Epic
    ├── Story
    └── Story

Time scope:
Theme: Quarters/Year
Epic:  Weeks/Months
Story: Days/Sprint
```

## Theme

### Definition

```
THEME = Strategic Goal or Focus Area

Characteristics:
┌──────────────────────────────────────────────────┐
│  • Broad business or user objective              │
│  • Spans multiple epics and stories              │
│  • Aligns with company vision/strategy           │
│  • May take quarters to fully address            │
│  • Guides prioritization decisions               │
└──────────────────────────────────────────────────┘

Examples:
├── "Improve Mobile Experience"
├── "Increase User Retention"
├── "Expand to Enterprise Market"
├── "Reduce Customer Support Load"
└── "Enable Self-Service"
```

### Theme Structure

| Component     | Description                         |
| ------------- | ----------------------------------- |
| Name          | Clear, memorable identifier         |
| Objective     | What success looks like             |
| Key Results   | Measurable outcomes                 |
| Related Epics | Work that contributes to this theme |
| Owner         | Strategic accountable person        |

## Epic

### Definition

```
EPIC = Large Feature or Initiative

Characteristics:
┌──────────────────────────────────────────────────┐
│  • Too large for single sprint                   │
│  • Delivers significant user value               │
│  • Contains multiple related stories             │
│  • Can be released incrementally                 │
│  • Has clear start and end                       │
└──────────────────────────────────────────────────┘

Examples:
├── "User Authentication System"
├── "Document Management Module"
├── "Payment Processing Integration"
├── "Search and Discovery Feature"
└── "Onboarding Flow Redesign"
```

### Epic Structure

```
Epic Template:

EPIC: [Name]
├── Theme: [Parent theme]
├── Objective: [What this epic achieves]
├── Success Metrics: [How we measure completion]
├── Stories:
│   ├── Story 1
│   ├── Story 2
│   └── Story 3...
├── Dependencies: [Other epics/external factors]
├── Estimated Duration: [Sprints/weeks]
└── Owner: [Product owner or lead]
```

## Story (User Story)

### Definition

```
STORY = Smallest Unit of User Value

Characteristics:
┌──────────────────────────────────────────────────┐
│  • Completable within single sprint              │
│  • Delivers tangible user value                  │
│  • Written from user's perspective               │
│  • Testable with clear acceptance criteria       │
│  • Independent enough to be prioritized          │
└──────────────────────────────────────────────────┘

Format: "As a [user], I want [goal] so that [benefit]"

Examples:
├── "As a user, I want to reset my password via email
│    so that I can regain access to my account"
├── "As an admin, I want to view user activity logs
│    so that I can audit system usage"
└── "As a customer, I want to save my cart
     so that I can complete purchase later"
```

### Story Structure (INVEST Criteria)

| Criterion       | Meaning                                        |
| --------------- | ---------------------------------------------- |
| **I**ndependent | Can be worked on separately from other stories |
| **N**egotiable  | Open to discussion on implementation           |
| **V**aluable    | Delivers value to user or business             |
| **E**stimable   | Team can estimate effort required              |
| **S**mall       | Fits within single sprint                      |
| **T**estable    | Has clear acceptance criteria                  |

## Hierarchy Example

```
THEME: Document Management
│
│  "Enable users to efficiently manage and
│   collaborate on documents within our platform"
│
├── EPIC: Document Storage System
│   │
│   │  "Users can upload, organize, and
│   │   retrieve documents securely"
│   │
│   ├── STORY: Design database schema for documents
│   │   └── AC: Schema supports metadata, versioning, permissions
│   │
│   ├── STORY: Implement file upload functionality
│   │   └── AC: Users can upload files up to 100MB
│   │
│   ├── STORY: Create folder organization UI
│   │   └── AC: Users can create, rename, delete folders
│   │
│   └── STORY: Add document search capability
│       └── AC: Users can search by name, content, date
│
├── EPIC: Document Sharing
│   │
│   ├── STORY: Implement share link generation
│   ├── STORY: Add permission levels (view/edit)
│   └── STORY: Create sharing notification system
│
└── EPIC: Document Collaboration
    │
    ├── STORY: Implement real-time co-editing
    ├── STORY: Add commenting functionality
    └── STORY: Create version history view
```

## Breaking Down Work

### Theme → Epics

```
Decomposition Questions:

Theme: "Improve Mobile Experience"
       │
       ▼
Ask: What major initiatives contribute to this?

Epics:
├── "Responsive Design Overhaul"
├── "Mobile-Specific Features"
├── "Performance Optimization for Mobile"
├── "Touch Gesture Implementation"
└── "Offline Mode Support"
```

### Epic → Stories

```
Decomposition Techniques:

1. BY WORKFLOW STEPS
   Epic: User Registration
   └── Stories: Enter details → Verify email → Set preferences → Complete

2. BY USER ROLES
   Epic: Admin Dashboard
   └── Stories: Super admin view → Manager view → Standard admin view

3. BY DATA TYPES
   Epic: Import Functionality
   └── Stories: CSV import → JSON import → Excel import

4. BY OPERATIONS (CRUD)
   Epic: Contact Management
   └── Stories: Create contact → Read/list → Update → Delete

5. BY ACCEPTANCE CRITERIA
   Epic: Search Feature
   └── Stories: Basic search → Filters → Sort → Save searches
```

## Estimation Guidance

```
SIZE REFERENCE

Theme:
├── Duration: Quarters to year
├── Team effort: Multiple teams possible
└── Story count: 50-200+ stories

Epic:
├── Duration: 2-8 weeks typically
├── Team effort: 1-2 teams
├── Story count: 5-20 stories
└── Story points: 40-150 points

Story:
├── Duration: 1-5 days
├── Team effort: 1-3 developers
├── Story points: 1-13 points (Fibonacci)
└── If > 13 points → Break down further
```

## Stakeholder Communication

| Audience         | Focus Level  | Key Information                   |
| ---------------- | ------------ | --------------------------------- |
| Executives       | Themes       | Strategic alignment, OKRs, ROI    |
| Product Leaders  | Epics        | Roadmap, dependencies, timelines  |
| Development Team | Stories      | Acceptance criteria, tech details |
| Customers        | Themes/Epics | Benefits, release timelines       |

## Analysis Template

```markdown
## Work Breakdown Structure

**Initiative:** [Name] **Date:** [Date]

### Theme Definition

**Theme:** [Name] **Objective:** [What we're trying to achieve] **Key Results:**

- [ ] KR1: [Measurable outcome]
- [ ] KR2: [Measurable outcome]

### Epic Breakdown

| Epic   | Stories | Est. Sprints | Priority     |
| ------ | ------- | ------------ | ------------ |
| Epic 1 | X       | Y            | High/Med/Low |
| Epic 2 | X       | Y            | High/Med/Low |

### Story Inventory (per Epic)

**Epic:** [Name]

| Story             | Points | Sprint   | Status |
| ----------------- | ------ | -------- | ------ |
| As a... I want... | X      | Sprint N | To Do  |
| As a... I want... | X      | Sprint N | To Do  |

### Dependencies

| Item         | Depends On   | Risk Level   |
| ------------ | ------------ | ------------ |
| [Epic/Story] | [Dependency] | High/Med/Low |

### Release Plan

| Release | Epics Included | Target Date |
| ------- | -------------- | ----------- |
| v1.0    | Epic 1, 2      | [Date]      |
| v1.1    | Epic 3         | [Date]      |
```

## Common Pitfalls

```
ANTI-PATTERNS TO AVOID

❌ Epics that never end
   → Set clear scope and acceptance criteria

❌ Stories too large
   → If can't complete in sprint, break down

❌ Themes too vague
   → Must have measurable outcomes

❌ Skipping hierarchy levels
   → Theme → Story directly loses context

❌ Over-decomposition
   → Stories like "add button" lack value context

❌ Rigid structure
   → Allow refinement as learning happens
```

## Integration with Other Methods

| Method                      | Combined Use                            |
| --------------------------- | --------------------------------------- |
| **User Story Fundamentals** | Story writing format and criteria       |
| **Kanban**                  | Visualizing work flow across levels     |
| **Jobs to Be Done**         | Themes aligned with user jobs           |
| **Five Whys**               | Understanding why theme matters         |
| **Hypothesis Tree**         | Breaking down theme into testable parts |

## Quick Reference

```
HIERARCHY CHECKLIST

Theme:
□ Aligns with company strategy
□ Has measurable key results
□ Spans multiple epics
□ Clear owner assigned

Epic:
□ Delivers significant user value
□ Has defined start and end
□ Contains 5-20 stories
□ Fits in roadmap timeline

Story:
□ Follows "As a... I want... so that..." format
□ Meets INVEST criteria
□ Has acceptance criteria
□ Completable in single sprint
□ Estimable by team
```

## Resources

- [User Story Mapping - Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)
- [Agile Estimating and Planning - Mike Cohn](https://www.mountaingoatsoftware.com/books/agile-estimating-and-planning)
- [Essential Scrum - Kenneth Rubin](https://www.innolution.com/essential-scrum)
