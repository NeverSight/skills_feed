---
name: my-web-plan
description: Planning for React web UI implementation with component design focus
---

# Web UI Implementation Plan Creation

Create an implementation plan in `docs/plans/yyyymmdd-<task-name>.md` with interactive context gathering. This plan is specialized for React web UI work — component decomposition, bottom-up build order, and visual design analysis are first-class concerns.

## Step 0: Parse Intent and Gather Context

Before asking questions, understand what the user is working on:

1. **Parse user's command arguments** to identify intent:
   - "add feature Z" / "implement W" → feature development
   - "fix bug" / "debug issue" → bug fix plan
   - "refactor X" / "improve Y" → refactoring plan
   - "migrate to Z" / "upgrade W" → migration plan
   - generic request → explore current work

2. **Launch Explore agent** (via Task tool with `subagent_type: Explore`) to gather relevant context based on intent:

   **For feature development:**
   - locate related existing code and patterns
   - check project structure (README, config files, existing similar implementations)
   - identify affected components and dependencies
   - find existing UI primitives and shared components that can be reused

   **For bug fixing:**
   - look for error logs, test failures, or stack traces
   - find related code that might be involved
   - check recent git changes in problem areas

   **For refactoring/migration:**
   - identify all files/components affected
   - check test coverage of affected areas
   - find dependencies and integration points

   **For generic/unclear requests:**
   - check `git status` and recent file activity
   - examine current working directory structure
   - identify primary language/framework from file extensions and config files

3. **Synthesize findings** into context summary:
   - what work is in progress
   - which files/areas are involved
   - what the apparent goal is
   - relevant patterns or structure discovered
   - existing components that can be reused or extended

## Step 0.5: Screenshot Analysis (when provided)

When the user provides a screenshot or design reference, this is a **critical planning input**. Do not rush past it.

### Reading the Screenshot

1. **Use the Read tool** to view the image file. Study it carefully.
2. **Identify every distinct visual element** — headers, lists, cards, buttons, inputs, icons, badges, dividers, avatars, status indicators, tooltips, empty states.
3. **Map the visual hierarchy** — what contains what? What are siblings? What repeats?

### Decomposing into Components

Think hard about component structure. Work **outside-in** to understand nesting, then plan **bottom-up** for implementation:

1. **Identify the outermost container** — is this a page, a panel, a modal, a sidebar section?
2. **Find repeating patterns** — any list of similar items means a parent list component + a child item component.
3. **Spot shared primitives** — buttons, badges, avatars, status dots. Check if these already exist in the project's `ui/` folder before planning new ones.
4. **Map the nesting tree** — write out the component tree explicitly:
   ```
   ChannelView
   ├── ChannelHeader
   │   ├── ChannelTitle
   │   └── ChannelActions (pin, search, members)
   ├── MessageList
   │   └── MessageRow (repeats)
   │       ├── Avatar
   │       ├── MessageContent
   │       │   ├── MessageAuthor + timestamp
   │       │   ├── MessageBody (text, attachments)
   │       │   └── ReactionBar
   │       └── MessageActions (hover menu)
   └── Composer
       ├── FileUploadButton
       ├── TextInput
       └── SendButton
   ```
5. **Identify state boundaries** — which components own state vs. receive props? Where do loading/empty/error states live?
6. **Note visual details that affect implementation** — spacing patterns, color usage, typography scale, responsive breakpoints, hover/active states, transitions.

### Bottom-Up Build Order

**CRITICAL: always plan implementation from leaf components upward to page-level containers.**

- Start with the smallest, most self-contained pieces (icons, badges, buttons, primitive UI elements).
- Then build the components that compose those pieces (cards, list items, form groups).
- Then build the containers that arrange those (lists, panels, sections).
- Finally wire up the page/route that orchestrates everything.

This order ensures:
- Each component can be built, tested, and visually verified in isolation (on the dev page).
- No component is blocked waiting for a child that doesn't exist yet.
- Integration bugs surface at composition time, not at the end.

## Step 1: Present Context and Ask Focused Questions

Show the discovered context, then ask questions **one at a time** using the AskUserQuestion tool:

"Based on your request, I found: [context summary]"

**Ask questions one at a time (do not overwhelm with multiple questions):**

1. **Plan purpose**: use AskUserQuestion - "What is the main goal?"
   - provide multiple choice with suggested answer based on discovered intent
   - wait for response before next question

2. **Scope**: use AskUserQuestion - "Which components/files are involved?"
   - provide multiple choice with suggested discovered files/areas
   - wait for response before next question

3. **Constraints**: use AskUserQuestion - "Any specific requirements or limitations?"
   - can be open-ended if constraints vary widely
   - wait for response before next question

4. **Testing approach**: use AskUserQuestion - "Do you prefer TDD or regular approach?"
   - options: "TDD (tests first)" and "Regular (code first, then tests)"
   - store preference for reference during implementation
   - wait for response before next question

5. **Plan title**: use AskUserQuestion - "Short descriptive title?"
   - provide suggested name based on intent

After all questions answered, synthesize responses into plan context.

## Step 1.5: Explore Approaches

Once the problem is understood, propose implementation approaches:

1. **Propose 2-3 different approaches** with trade-offs for each
2. **Lead with recommended option** and explain reasoning
3. **Present conversationally** - not a formal document yet

For UI work, approaches often differ in:
- Component granularity (fewer large components vs. many small composable ones)
- State management strategy (local state vs. store vs. URL state)
- Existing component reuse vs. building from scratch
- Animation/interaction complexity

Example format:
```
I see three approaches:

**Option A: [name]** (recommended)
- How it works: ...
- Pros: ...
- Cons: ...

**Option B: [name]**
- How it works: ...
- Pros: ...
- Cons: ...

Which direction appeals to you?
```

Use AskUserQuestion tool to let user select preferred approach before creating the plan.

**Skip this step** if:
- the implementation approach is obvious (single clear path)
- user explicitly specified how they want it done
- it's a bug fix with clear solution

## Step 2: Create Plan File

Check `docs/plans/` for existing files, then create `docs/plans/<task-name>.md`:

### Plan Structure

```markdown
# [Plan Title]

## Overview
- Clear description of the feature/change being implemented
- Problem it solves and key benefits
- How it integrates with existing system

## Context (from discovery)
- Files/components involved: [list from step 0]
- Related patterns found: [patterns discovered]
- Dependencies identified: [dependencies]
- Existing components to reuse: [list from ui/ and domain folders]

## Component Design
<!-- Include this section for any UI work -->

### Component Tree
```
[Visual tree from screenshot analysis or design thinking]
PageComponent
├── SectionA
│   ├── LeafComponent1
│   └── LeafComponent2
└── SectionB
    └── ListComponent
        └── ListItem (repeats)
```

### New Components
| Component | File | Props | Notes |
|-----------|------|-------|-------|
| ComponentName | `components/domain/ComponentName.tsx` | `items`, `onSelect` | Renders list of... |

### Reused Components
- `Avatar` from `components/ui/` — for user avatars
- `Badge` from `components/ui/` — for status indicators
- [etc.]

## Development Approach
- **Build order**: bottom-up (leaf components first, containers last)
- **Testing approach**: [TDD / Regular - from user preference in planning]
- Complete each task fully before moving to the next
- Make small, focused changes
- **CRITICAL: every task MUST include new/updated tests** for code changes in that task
  - tests are not optional - they are a required part of the checklist
  - write unit tests for new functions/methods
  - write unit tests for modified functions/methods
  - add new test cases for new code paths
  - update existing test cases if behavior changes
  - tests cover both success and error scenarios
- **CRITICAL: all tests must pass before starting next task** - no exceptions
- **CRITICAL: update this plan file when scope changes during implementation**
- Run tests after each change
- Maintain backward compatibility

## Testing Strategy
- **Unit tests**: required for every task (see Development Approach above)
- **Visual verification**: after each component task, add it to the dev page and use `agent-browser` to screenshot and verify appearance
- **E2E tests**: if project has UI-based e2e tests (Playwright, Cypress, etc.):
  - UI changes → add/update e2e tests in same task as UI code
  - Backend changes supporting UI → add/update e2e tests in same task
  - Treat e2e tests with same rigor as unit tests (must pass before next task)
  - Store e2e tests alongside unit tests (or in designated e2e directory)

## Progress Tracking
- Mark completed items with `[x]` immediately when done
- Add newly discovered tasks with ➕ prefix
- Document issues/blockers with ⚠️ prefix
- Update plan if implementation deviates from original scope
- Keep plan in sync with actual work done

## What Goes Where
- **Implementation Steps** (`[ ]` checkboxes): tasks achievable within this codebase - code changes, tests, documentation updates
- **Post-Completion** (no checkboxes): items requiring external action - manual testing, changes in consuming projects, deployment configs, third-party verifications

## Implementation Steps

<!--
Task structure guidelines:
- BUILD BOTTOM-UP: first tasks are leaf/primitive components, last tasks are page-level wiring
- Each task = ONE component (or one tightly coupled group)
- Use specific descriptive names: "Build MessageRow component", not "Implement message UI"
- Aim for ~5 checkboxes per task (more is OK if logically atomic)
- **CRITICAL: Each task MUST end with writing/updating tests before moving to next**
- **CRITICAL: Each UI component task should include dev page entry for visual verification**

Example (bottom-up order):

### Task 1: Build MessageBubble component
- [ ] create `components/messages/MessageBubble.tsx` with text content + timestamp
- [ ] handle long text wrapping and link detection
- [ ] add to dev page with sample messages (short, long, with links, empty)
- [ ] screenshot dev page with agent-browser to verify appearance
- [ ] write tests for MessageBubble rendering and edge cases
- [ ] run project tests - must pass before task 2

### Task 2: Build MessageRow component
- [ ] create `components/messages/MessageRow.tsx` composing Avatar + MessageBubble
- [ ] handle own-message vs other-message alignment
- [ ] add to dev page with both variants
- [ ] screenshot dev page with agent-browser to verify appearance
- [ ] write tests for MessageRow rendering
- [ ] run project tests - must pass before task 3

### Task 3: Build MessageList container
- [ ] create `components/messages/MessageList.tsx` rendering list of MessageRow
- [ ] implement auto-scroll to bottom on new messages
- [ ] handle empty state and loading skeleton
- [ ] add to dev page with populated, empty, and loading states
- [ ] write tests for MessageList rendering and scroll behavior
- [ ] run project tests - must pass before task 4

### Task 4: Wire up ChannelView page
- [ ] create `components/channels/ChannelView.tsx` composing ChannelHeader + MessageList + Composer
- [ ] connect to store/API for real data
- [ ] update route file to render ChannelView
- [ ] write integration tests
- [ ] run project tests - must pass before task 5
-->

### Task 1: [leaf component - smallest building block]
- [ ] [create component file with props interface]
- [ ] [implement rendering logic]
- [ ] add to dev page with representative states
- [ ] screenshot with agent-browser to verify
- [ ] write tests for rendering and edge cases
- [ ] run tests - must pass before next task

### Task N-2: [page/container - composes all pieces]
- [ ] [create page component composing child components]
- [ ] [connect to data (store/API/loader)]
- [ ] [wire up in route file]
- [ ] write integration tests
- [ ] run tests - must pass before next task

### Task N-1: Verify acceptance criteria
- [ ] verify all requirements from Overview are implemented
- [ ] verify edge cases are handled
- [ ] run full test suite (unit tests)
- [ ] run e2e tests if project has them
- [ ] run linter - all issues must be fixed
- [ ] screenshot final result with agent-browser and compare to reference design
- [ ] verify test coverage meets project standard (80%+)

### Task N: [Final] Update documentation
- [ ] update README.md if needed
- [ ] update project knowledge docs if new patterns discovered

## Technical Details
- Data structures and changes
- Parameters and formats
- Processing flow

## Post-Completion
*Items requiring manual intervention or external systems - no checkboxes, informational only*

**Manual verification** (if applicable):
- Manual UI/UX testing scenarios
- Cross-browser verification
- Responsive breakpoint testing
- Performance testing under load

**External system updates** (if applicable):
- Consuming projects that need updates after this library change
- Configuration changes in deployment systems
- Third-party service integrations to verify
```

## Step 3: Offer to Start

After creating the file, tell user:

"Created plan: `docs/plans/<task-name>.md`

Ready to start implementation?"

If yes, begin with task 1 (the leaf-most component).

## Execution Enforcement

**CRITICAL testing rules during implementation:**

1. **After completing code changes in a task**:
   - STOP before moving to next task
   - Add tests for all new functionality
   - Update tests for modified functionality
   - Add component to dev page for visual verification
   - Screenshot with agent-browser to confirm appearance
   - Run project test command
   - Mark completed items with `[x]` in plan file
   - **Use TodoWrite tool to track progress and mark todos completed immediately (do not batch)**

2. **If tests fail**:
   - Fix the failures before proceeding
   - Do NOT move to next task with failing tests
   - Do NOT skip test writing

3. **Only proceed to next task when**:
   - All task items completed and marked `[x]`
   - Tests written/updated
   - All tests passing
   - Visual appearance verified (for UI tasks)

4. **Plan tracking during implementation**:
   - Update checkboxes immediately when tasks complete
   - Add ➕ prefix for newly discovered tasks
   - Add ⚠️ prefix for blockers
   - Modify plan if scope changes significantly

5. **On completion**:
   - Verify all checkboxes marked
   - Run final test suite
   - Take final screenshot and compare to reference design

6. **Partial implementation exception**:
   - If a task provides partial implementation where tests cannot pass until a later task:
     - Still write the tests as part of this task (required)
     - Add TODO comment in test code noting the dependency
     - Mark the test checkbox as completed with note: `[x] write tests ... (fails until Task X)`
     - Do NOT skip test writing or defer until later
   - When the dependent task completes, remove the TODO comment and verify tests pass

This ensures each task is solid before building on top of it.

## Key Principles

- **Bottom-up always** - build leaves first, compose upward, wire pages last
- **Screenshot-driven** - when a reference design exists, study it deeply before writing any code; verify against it after each component
- **One question at a time** - do not overwhelm user with multiple questions in a single message
- **Multiple choice preferred** - easier to answer than open-ended when possible
- **YAGNI ruthlessly** - remove unnecessary features from all designs, keep scope minimal
- **Lead with recommendation** - have an opinion, explain why, but let user decide
- **Explore alternatives** - always propose 2-3 approaches before settling (unless obvious)
- **Reuse before creating** - check existing `ui/` components and project primitives before building new ones
- **Duplication vs abstraction** - when code repeats, ask user: prefer duplication (simpler, no coupling) or abstraction (DRY but adds complexity)? explain trade-offs before deciding
