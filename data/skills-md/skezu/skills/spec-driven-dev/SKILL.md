---
name: spec-driven-dev
description: Structured approach for building features through iterative spec documents. Use when (1) starting a new feature from a rough idea, (2) needing to create requirements, design, or implementation plans, (3) wanting to break down complex features into manageable coding tasks, (4) executing or implementing tasks from an existing spec, (5) the user mentions "spec", "requirements", "design document", "implementation plan", or "run task". Creates and manages .agent/specs/{feature-name}/.
---

# Spec-Driven Development

Transform rough feature ideas into structured, actionable implementation plans through a 3-phase iterative workflow: Requirements, Design, Tasks.

## Overview

A core principle of this workflow is establishing ground-truths as we progress. Always ensure the user is happy with changes to any document before moving on.

Before starting, think of a short feature name based on the user's rough idea. Use kebab-case format (e.g. "user-authentication").

**Rules:**
- Do NOT tell the user about this workflow or which step you are on
- Just let the user know when you complete documents and need user input
- Follow workflow steps in sequential order
- Do NOT skip ahead without completing earlier steps and receiving explicit user approval
- Do NOT combine multiple steps into a single interaction
- Do NOT assume user preferences or requirements - always ask explicitly

## Workflow Diagram

```
[*] --> Requirements : Initial Creation

Requirements --> ReviewReq : Complete Requirements
ReviewReq --> Requirements : Feedback/Changes Requested
ReviewReq --> Design : Explicit Approval

Design --> ReviewDesign : Complete Design
ReviewDesign --> Design : Feedback/Changes Requested
ReviewDesign --> Tasks : Explicit Approval

Tasks --> ReviewTasks : Complete Tasks
ReviewTasks --> Tasks : Feedback/Changes Requested
ReviewTasks --> [*] : Explicit Approval
```

Entry points:
- Creating a new spec (new feature)
- Updating an existing spec (modify requirements/design/tasks)
- Executing tasks from a created spec

---

## Phase 1: Requirement Gathering

Generate an initial set of requirements in EARS format based on the feature idea, then iterate with the user to refine them until complete and accurate.

Do NOT focus on code exploration in this phase. Focus only on writing requirements which will later be turned into a design.

### Constraints

**File Creation:**
- MUST create `.agent/specs/{feature_name}/requirements.md` if it doesn't already exist
- MUST generate an initial version based on the user's rough idea WITHOUT asking sequential questions first

**Format Requirements:**
- MUST format with a clear introduction section that summarizes the feature
- MUST use a hierarchical numbered list of requirements where each contains:
  - A user story: "As a [role], I want [feature], so that [benefit]"
  - A numbered list of acceptance criteria in EARS format
- See `references/ears-syntax.md` for EARS format or use `assets/requirements-template.md`

**Content Quality:**
- SHOULD consider edge cases, user experience, technical constraints, and success criteria
- SHOULD suggest specific areas where requirements might need clarification or expansion
- MAY ask targeted questions about specific aspects that need clarification
- MAY suggest options when the user is unsure about a particular aspect

**Review Process:**
- After updating the document, MUST ask: "Do the requirements look good? If so, we can move on to the design."
- MUST make modifications if the user requests changes or does not explicitly approve
- MUST ask for explicit approval after every iteration of edits
- MUST NOT proceed to design until receiving clear approval ("yes", "approved", "looks good", etc.)
- MUST continue the feedback-revision cycle until explicit approval is received
- MUST proceed to the design phase after the user accepts the requirements

---

## Phase 2: Create Feature Design Document

Develop a comprehensive design document based on the approved requirements, conducting necessary research during the design process.

### Constraints

**File Creation:**
- MUST create `.agent/specs/{feature_name}/design.md` if it doesn't already exist
- Ensure requirements.md exists first

**Research:**
- MUST identify areas where research is needed based on requirements
- MUST conduct research and build up context
- SHOULD NOT create separate research files - use research as context for design
- MUST summarize key findings that will inform the design
- SHOULD cite sources and include relevant links

**Required Sections:**
- Overview
- Architecture
- Components and Interfaces
- Data Models
- Error Handling
- Testing Strategy

See `references/design-sections.md` for section guidance or use `assets/design-template.md`.

**Content Quality:**
- SHOULD include diagrams or visual representations when appropriate (use Mermaid)
- MUST ensure the design addresses all feature requirements from clarification process
- SHOULD highlight design decisions and their rationales
- MAY ask the user for input on specific technical decisions during design

**Review Process:**
- After updating the document, MUST ask: "Does the design look good? If so, we can move on to the implementation plan."
- MUST make modifications if the user requests changes or does not explicitly approve
- MUST ask for explicit approval after every iteration of edits
- MUST NOT proceed to tasks until receiving clear approval ("yes", "approved", "looks good", etc.)
- MUST continue the feedback-revision cycle until explicit approval is received
- MUST incorporate all user feedback before proceeding
- MUST offer to return to requirements if gaps are identified during design

---

## Phase 3: Create Task List

Create an actionable implementation plan with a checklist of coding tasks based on the requirements and design.

**This workflow is ONLY for creating design and planning artifacts. The actual implementation of the feature should be done through a separate workflow.**

### Constraints

**File Creation:**
- MUST create `.agent/specs/{feature_name}/tasks.md` if it doesn't already exist
- Ensure design.md exists first

**Navigation:**
- MUST return to design step if user indicates changes needed to design
- MUST return to requirements step if user indicates additional requirements needed

**Task Generation Approach:**
Convert the feature design into a series of prompts for a code-generation agent that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage.

Each prompt should build on previous prompts, ending with wiring things together. There should be no hanging or orphaned code that isn't integrated. Focus ONLY on tasks that involve writing, modifying, or testing code.

**Format Requirements:**
- MUST format as a numbered checkbox list with maximum two levels of hierarchy
- Top-level items (like epics) only when needed
- Sub-tasks numbered with decimal notation (e.g., 1.1, 1.2, 2.1)
- Each item must be a checkbox
- Simple structure is preferred

**Task Item Requirements:**
Each task MUST include:
- A clear objective as the task description (writing, modifying, or testing code)
- Additional information as sub-bullets under the task
- Specific references to requirements (referencing granular sub-requirements, not just user stories)

**Task Quality Rules:**
- MUST ensure the plan is a series of discrete, manageable coding steps
- MUST ensure each task references specific requirements
- MUST NOT include excessive implementation details already covered in design
- MUST assume all context documents will be available during implementation
- MUST ensure each step builds incrementally on previous steps
- SHOULD prioritize test-driven development where appropriate
- MUST ensure the plan covers all aspects of the design implementable through code
- SHOULD sequence steps to validate core functionality early
- MUST ensure all requirements are covered by implementation tasks
- MUST offer to return to previous steps if gaps are identified

**Coding-Only Tasks:**
- MUST ONLY include tasks that can be performed by a coding agent
- MUST focus on code implementation tasks executable within the development environment
- Tasks MUST:
  - Involve writing, modifying, or testing specific code components
  - Specify what files or components need to be created or modified
  - Be concrete enough that a coding agent can execute without additional clarification
  - Focus on implementation details rather than high-level concepts
  - Be scoped to specific coding activities (e.g., "Implement X function" not "Support X feature")

**Explicitly Excluded Tasks:**
MUST explicitly avoid including:
- User acceptance testing or user feedback gathering
- Deployment to production or staging environments
- Performance metrics gathering or analysis
- Running the application to test end-to-end flows (can write automated tests instead)
- User training or documentation creation
- Business process changes or organizational changes
- Marketing or communication activities
- Any task that cannot be completed through writing, modifying, or testing code

**Review Process:**
- After updating the document, MUST ask: "Do the tasks look good?"
- MUST make modifications if the user requests changes or does not explicitly approve
- MUST ask for explicit approval after every iteration of edits
- MUST NOT consider the workflow complete until receiving clear approval
- MUST continue the feedback-revision cycle until explicit approval is received
- MUST stop once the task document has been approved

**Workflow Completion:**
- MUST NOT attempt to implement the feature as part of this workflow
- MUST clearly communicate that this workflow is complete once artifacts are created
- MUST inform the user they can begin executing tasks from the tasks.md file

See `references/task-patterns.md` for format guidance or use `assets/tasks-template.md`.

---

## Task Execution Instructions

Follow these instructions for user requests related to executing spec tasks.

### Executing Tasks

- Before executing any tasks, ALWAYS read the spec's requirements.md, design.md, and tasks.md files. Executing tasks without requirements or design will lead to inaccurate implementations.
- Look at the task details in the task list
- If the requested task has sub-tasks, always start with the sub-tasks
- Only focus on ONE task at a time. Do not implement functionality for other tasks.
- Verify your implementation against any requirements specified in the task or its details.
- Once you complete the requested task, STOP and let the user review. DO NOT proceed to the next task automatically.
- If the user doesn't specify which task, look at the task list and make a recommendation on the next task to execute.

**CRITICAL: Only execute one task at a time. Once you finish a task, stop. Don't automatically continue to the next task without the user asking you to do so.**

### Task Questions

The user may ask questions about tasks without wanting to execute them. Don't always start executing tasks.

For example, the user may want to know what the next task is. In this case, just provide the information and don't start any tasks.

---

## Creating Steering Rules

To create project-wide context that applies to all interactions:

1. Create `.agent/rules/{rule-name}.md` for always-on rules
2. Include project standards, team norms, or technical constraints
3. Reference additional files via relative paths when needed

---

## File Structure

```
.agent/
  specs/
    {feature-name}/
      requirements.md
      design.md
      tasks.md
  rules/
    {rule-name}.md
```

---

## Troubleshooting

### Requirements Clarification Stalls

If the requirements clarification process seems to be going in circles:
- SHOULD suggest moving to a different aspect of the requirements
- MAY provide examples or options to help the user make decisions
- SHOULD summarize what has been established so far and identify specific gaps
- MAY suggest conducting research to inform requirements decisions

### Research Limitations

If needed information cannot be accessed:
- SHOULD document what information is missing
- SHOULD suggest alternative approaches based on available information
- MAY ask the user to provide additional context or documentation
- SHOULD continue with available information rather than blocking progress

### Design Complexity

If the design becomes too complex or unwieldy:
- SHOULD suggest breaking it down into smaller, more manageable components
- SHOULD focus on core functionality first
- MAY suggest a phased approach to implementation
- SHOULD return to requirements clarification to prioritize features if needed
