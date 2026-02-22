---
name: charted-design
description: Interviews the user section by section to collaboratively produce design documents. Use when creating a design doc, starting feature design, or when the user invokes the design command.
---

# Collaborative Design Document

## Goal

Interview the user section by section to produce a design document.
IMPORTANT: Write the current state to `design-docs/` after each section.
Adapt the interview to feature complexity.

## Output File

- **Path**: `design-docs/`
- **Name**: `NNN-short-kebab-title.md` — `NNN` is zero-padded (e.g. `001`, `002`)
- **Sequence**: List files in `design-docs/`, take highest number, increment. Empty folder → start at `001`
- **Title**: Derive short kebab-case title from the feature description (ask user first)

## Interview Process

For **each section**:

1. Explain the section and what information is needed
2. Ask targeted questions to gather it
3. Summarize and propose draft content
4. Ask user to confirm or correct before moving on

If the user answers something that belongs to a later section, acknowledge it and say you'll add it when you reach that section.

## Section Order and Prompts

### 1. Goals

Ask: _What problem are we solving? Why does this feature matter?_

### 2. Non-Goals

Ask: _What is explicitly out of scope? What might people assume is included but is not?_

### 3. Desired Behavior

Ask: _Describe the user-visible behavior. What does the user see, click, or experience? Walk through the scenarios step by step._

Format as a bullet list of concrete, observable behaviors.

### 4. Design

Ask: _How should this be implemented at a high level? What components, services, or data structures are involved?_

#### 4a. Diagram

Produce a Mermaid `flowchart` of key components and interactions.

**Legend**:

- Square corners = Angular components
- Round corners = Angular services
- Arrows: `methodName({param1: Type1}): ReturnType`
- `[input1: Type1]` = Angular inputs
- `(output1: Type1)` = Angular outputs
- Use `<br>` in labels to avoid truncation

Show diagram to user and ask for corrections.

#### 4b. Implementation Details

Ask: _Any algorithms, edge cases, or conventions?_ Leave empty if nothing to add.

### 5. Testing Strategy

Ask: _For each component or unit from the design, what behaviors are important to test?_

Format: grouped by component/unit, each scenario with a descriptive name and arrange/act/assert steps.

**Example**:

```markdown
## Cart component

### Displays cart items:

- Arrange fake cart repository to return 3 items: keyboard, mouse, monitor.
- Mount `Cart` component.
- Assert 3 items displayed with labels: "Keyboard", "Mouse", "Monitor".
```

### 6. PR Plan

Propose ordered, incremental PRs that:

- Never break existing behavior
- Are independently reviewable and mergeable
- Keep diffs focused

**Rules**:

- **Scaffolding PR**: If many new files, put WIP scaffolding in its own PR
- **Pre-tidy-up PR**: If interfaces must change, do backward-compatible changes first (optional params, deprecations)
- **Feature PRs**: Each adds one slice of user-visible or testable functionality

Include a Mermaid `flowchart` of PR dependencies. List each PR with a short description. Ask for feedback.

### 7. Alternatives Considered

Ask: _Did we consider other approaches? Why were they rejected?_

### 8. Kitchen Sink

Ask: _Anything else — open questions, risks, future ideas?_ Leave empty if nothing.

## Final Step

Assemble the full doc from the template below, write to the output file, show the user the path.

## Template

````markdown
# Goals

{goals}

# Non-Goals

{non_goals}

# Desired Behavior

{desired_behavior}

# Design

{design}

## Diagram

```mermaid
{diagram}
```

## Implementation Details

{implementation_details}

# Testing Strategy

{testing_strategy}

# PR Plan

```mermaid
{pr_dependency_diagram}
```

{pr_details}

# Alternatives Considered

{alternatives}

# Kitchen Sink

{kitchen_sink}
````
