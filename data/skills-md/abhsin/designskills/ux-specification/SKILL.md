---
name: ux-specification
description: Translate PRDs into detailed UX specifications including user flows, screen descriptions, components, and interaction patterns. Use when a user has a PRD and needs to define the concrete UI/UX before generating development prompts. Bridges product requirements to implementation details.
---

# UX Spec

Turn product requirements into concrete flows, screens, and interactions that coding agents can implement.

## Why This Exists

Bridges the gap between product requirements and implementation by defining how the product looks and behaves.

## Input Requirements

This skill expects:
- PRD (from `prd-generation` or user-provided)
- Any existing sketches, wireframes, or references (optional)
- Design preferences or constraints (optional)

## Workflow

### Step 1: Ingest PRD

Extract from the PRD:
- User stories (especially Must Have)
- Features and acceptance criteria
- Target user characteristics
- Technical constraints

### Step 2: Map User Flows

For each core user story, define the flow:

**Questions to answer:**
- Where does the user start?
- What's the happy path?
- What are the decision points?
- Where does the user end up?
- What can go wrong?

### Step 3: Define Screens

For each screen in the flows:
- What's the purpose?
- What components are needed?
- What data is displayed?
- What actions are available?
- What states exist?

### Step 4: Specify Interactions

For key interactions:
- What triggers the action?
- What feedback does the user get?
- What changes on screen?
- How long does it take?

### Step 5: Clarify Gaps

Ask targeted questions if needed:
- "Should this be a modal or a new page?"
- "What happens if the list is empty?"
- "How does the user know it's loading?"
- "Any specific layout preference—sidebar, tabs, single page?"

## Output Format

**Automatically save the output to `design/06-ux-spec.md` using the Write tool** while presenting it to the user.

```markdown
# UX Spec: [Project Name]

## Overview
[Brief summary of the product and primary user goal]

---

## Information Architecture

### Navigation Structure
```
[App Name]
├── [Primary Nav Item 1]
│   ├── [Sub-item]
│   └── [Sub-item]
├── [Primary Nav Item 2]
└── [Primary Nav Item 3]
```

### Key User Paths
1. **[Path Name]:** [Start] → [Step] → [Step] → [End]
2. **[Path Name]:** [Start] → [Step] → [End]

---

## User Flows

### Flow 1: [Flow Name]
**Trigger:** [What initiates this flow]
**User goal:** [What they're trying to accomplish]

```
[Start State]
    ↓
[Action/Decision]
    ↓
[Screen/State] ──→ [Alternative path if applicable]
    ↓
[End State]
```

**Steps:**
1. User [action]
2. System [response]
3. User [action]
4. System [response]
5. User reaches [end state]

**Error paths:**
- If [condition]: [what happens]
- If [condition]: [what happens]

### Flow 2: [Flow Name]
[Same structure]

---

## Screens

### Screen: [Screen Name]
**URL/Route:** `/path`
**Purpose:** [What the user accomplishes here]
**Entry points:** [How users get here]

#### Layout
```
┌─────────────────────────────────┐
│ [Header/Nav]                    │
├─────────────────────────────────┤
│                                 │
│ [Main Content Area]             │
│                                 │
│ [Component]     [Component]     │
│                                 │
├─────────────────────────────────┤
│ [Footer/Actions]                │
└─────────────────────────────────┘
```

#### Components
| Component | Description | Behavior |
|-----------|-------------|----------|
| [Name] | [What it displays] | [How it behaves] |
| [Name] | [What it displays] | [How it behaves] |

#### States
| State | Appearance | Trigger |
|-------|------------|---------|
| Default | [Description] | Initial load |
| Loading | [Description] | Data fetching |
| Empty | [Description] | No data exists |
| Error | [Description] | Request failed |
| Success | [Description] | Action completed |

#### Actions
| Action | Trigger | Result |
|--------|---------|--------|
| [Action] | [Click/tap/etc.] | [What happens] |
| [Action] | [Trigger] | [Result] |

### Screen: [Screen Name]
[Same structure]

---

## Components

### Component: [Component Name]
**Used in:** [List of screens]
**Purpose:** [What it does]

#### Props/Inputs
| Prop | Type | Description |
|------|------|-------------|
| [name] | [type] | [what it controls] |

#### Variants
- **[Variant 1]:** [Description]
- **[Variant 2]:** [Description]

#### States
- Default: [Description]
- Hover: [Description]
- Active: [Description]
- Disabled: [Description]

### Component: [Component Name]
[Same structure]

---

## Interactions

### Interaction: [Name]
**Trigger:** [User action]
**Response:** [System behavior]
**Duration:** [Instant / 200ms / async]
**Feedback:** [What user sees/feels]

### Interaction: [Name]
[Same structure]

---

## Responsive Behavior
**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Key adaptations:**
- [Component/layout]: [How it changes]
- [Component/layout]: [How it changes]

---

## Design Notes
[Optional — any specific visual direction, references, or constraints]

- **Style:** [Minimal / Dense / Playful / etc.]
- **Reference:** [Any inspiration or similar products]
- **Constraints:** [Accessibility, brand, etc.]
```

## Adaptation Guidelines

**Simple project (1-3 screens):**
- Skip Information Architecture
- Combine Flows and Screens
- Minimal Components section
- Skip Responsive Behavior

**Medium project (4-8 screens):**
- Full structure as shown
- Focus on core flows, not edge cases

**Complex project (10+ screens):**
- Add screen-by-screen detail
- Document all component variants
- Include edge case flows
- Add Design Notes section

## Writing Guidelines

- **ASCII layouts are sufficient** — Don't overcomplicate, just show structure
- **States are critical** — Loading, empty, error states prevent agent guesswork
- **Be specific about triggers** — "Click" vs "hover" vs "focus" matters
- **Name things consistently** — Use same component names across screens

## Handoff

After presenting the UX spec, ask:
> "Ready to generate prompts.md with `/prompt-export`, or want to refine any screens first?"

**Note:** File is automatically saved to `design/06-ux-spec.md`. This feeds into development prompts.