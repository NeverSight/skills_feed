---
name: replit-plan
description: |
  This skill should be used when the user asks to "create a plan for replit", "break down tasks",
  "create development phases", "checkpoint strategy", or needs to convert a project into iterative
  development phases that Replit Agent can execute step-by-step with checkpoints.
---

# Replit Task Planner

Break down projects into iterative development phases with checkpoints optimized for Replit Agent's workflow.

## When to Use

- Converting a large project into manageable phases
- Planning checkpoint strategy for complex builds
- Creating iterative prompts from a PRD or idea
- Structuring work for Replit Agent's extended autonomy mode

## Replit Agent Modes

### Build Mode (Default)
- Agent writes code directly
- Best for: Implementation, coding, fixing bugs
- Creates checkpoints automatically

### Plan Mode
- Agent discusses without modifying code
- Best for: Architecture decisions, exploring approaches, reviewing PRDs
- Free (no checkpoint charges)

### Edit Mode
- Agent makes targeted changes to specific files
- Best for: Precise modifications, refactoring specific sections

## Checkpoint Strategy

Replit Agent creates checkpoints after each prompt. Effective planning means:

1. **One checkpoint = one logical unit of work**
2. **Each phase should be testable independently**
3. **Phases build on each other sequentially**
4. **Rollback-friendly boundaries**

## Task Breakdown Template

```markdown
# [Project Name] - Development Plan

## Overview
**Project:** [Brief description]
**Total Phases:** [Number]
**Estimated Checkpoints:** [Number]

---

## Phase 1: [Phase Name]
**Goal:** [One sentence describing what's achieved]
**Dependencies:** None (starting point)

### Tasks
1. [Specific task 1]
2. [Specific task 2]
3. [Specific task 3]

### Deliverables
- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]

### Prompt for Replit Agent
```
[Phase goal description]. Specifically:
1. [Task 1 with details]
2. [Task 2 with details]
3. [Task 3 with details]

Stop after completing these tasks so I can review before continuing.
```

### Verification Steps
- [ ] [How to verify task 1]
- [ ] [How to verify task 2]

---

## Phase 2: [Phase Name]
**Goal:** [One sentence]
**Dependencies:** Phase 1 complete

### Tasks
[...]

### Prompt for Replit Agent
[...]

---

## Rollback Points
- After Phase 1: [What's safe to rollback to]
- After Phase 2: [What's safe to rollback to]

## Risk Mitigation
| Risk | Phase | Mitigation |
|------|-------|------------|
| [Risk] | [Phase #] | [How to handle] |
```

## Procedure

### Step 1: Understand the Project

Gather from user:
1. What is being built?
2. What are all the features/requirements?
3. Any dependencies between features?
4. Are there external integrations?

### Step 2: Identify Natural Boundaries

Look for:
- **Setup vs Features** — Config/auth first, then features
- **Independent Features** — Features that don't depend on each other
- **Dependent Features** — Features that require others to exist
- **Polish vs Core** — Error handling, edge cases last

### Step 3: Create Phases

**Phase 1: Foundation**
Always start with:
- Project setup
- Database schema
- Authentication (if needed)
- Basic navigation/layout

**Phase 2-N: Core Features**
Group related functionality:
- One major feature per phase
- Include its UI, API, and data needs
- Keep phases 30-60 minutes of Agent work

**Final Phase: Polish**
Always end with:
- Error handling
- Loading states
- Edge cases
- Responsive fixes
- Final testing

### Step 4: Write Prompts for Each Phase

Each prompt should:
- State the goal clearly
- List specific tasks (numbered)
- Include technical details
- Request a stop point for review

**Template:**
```
Implement [Feature Name].

Requirements:
1. [Specific requirement with details]
2. [Specific requirement with details]
3. [Specific requirement with details]

Technical notes:
- [Relevant constraint or approach]
- [Relevant constraint or approach]

Create a checkpoint when complete so I can review before the next phase.
```

### Step 5: Define Verification Steps

For each phase, include how to verify:
- What to click/test in the UI
- What API calls to make
- What database records to check

### Step 6: Present the Plan

```
## Development Plan: [Project Name]

**Phases:** [Number]
**Approach:** [Brief strategy explanation]

---

[Full plan with all phases]

---

## How to Use This Plan

1. **Start with Plan Mode**: Copy Phase 1 prompt, select Plan Mode
2. **Review Agent's approach**: Ensure it aligns with expectations
3. **Switch to Build Mode**: Approve and let Agent implement
4. **Verify at checkpoint**: Test deliverables before continuing
5. **Proceed to next phase**: Copy next prompt and repeat

## Iteration Strategy
If issues arise:
- Minor issues: Describe and ask Agent to fix in current phase
- Major issues: Rollback to previous checkpoint, refine prompt, retry

Ready to start?
```

## Phase Sizing Guidelines

| Phase Size | Work Amount | Example |
|------------|-------------|---------|
| Small | 15-30 min | Add a single form with validation |
| Medium | 30-60 min | Full CRUD for one entity |
| Large | 60-90 min | Feature with UI + API + data |

**Ideal phase:** Medium (30-60 minutes)

**Signs phase is too large:**
- More than 5 major tasks
- Touches more than 4-5 files
- Multiple unrelated features
- "Build the entire X" language

**Signs phase is too small:**
- Single task that takes < 10 minutes
- No testable deliverable
- Could easily be combined with adjacent phase

## Common Phase Patterns

### Pattern 1: CRUD Feature
```
Phase N: [Entity] Management
1. Database model and migrations
2. API endpoints (list, create, read, update, delete)
3. List view with table/cards
4. Create/edit form (modal or page)
5. Delete with confirmation

Deliverables:
- [ ] Can create new [entity]
- [ ] Can view list of [entities]
- [ ] Can edit existing [entity]
- [ ] Can delete [entity]
```

### Pattern 2: Authentication
```
Phase 1: Authentication Setup
1. Configure auth provider (Supabase/Clerk/etc.)
2. Create signup page with form
3. Create login page with form
4. Add protected route wrapper
5. Add user context/hook
6. Add logout functionality

Deliverables:
- [ ] New user can sign up
- [ ] Existing user can log in
- [ ] Protected pages redirect to login
- [ ] User can log out
```

### Pattern 3: Dashboard
```
Phase N: Dashboard
1. Create dashboard layout
2. Add metric cards with data fetching
3. Add recent activity list
4. Add quick action buttons
5. Implement responsive grid

Deliverables:
- [ ] Dashboard loads with correct data
- [ ] Metrics update when data changes
- [ ] Recent activity shows latest items
- [ ] Layout works on mobile
```

### Pattern 4: External Integration
```
Phase N: [Service] Integration
1. Set up environment variables for API keys
2. Create service wrapper/client
3. Implement core integration function
4. Add error handling for API failures
5. Connect to UI trigger point

Deliverables:
- [ ] API key configuration works
- [ ] Integration function returns expected data
- [ ] Errors handled gracefully
- [ ] UI reflects integration state
```

## Example: Full Task Breakdown

### Project: Todo App with Categories

```markdown
# Todo App - Development Plan

## Overview
**Project:** Todo app with categories, due dates, and search
**Total Phases:** 4
**Estimated Checkpoints:** 5

---

## Phase 1: Foundation
**Goal:** Set up project with database and basic structure
**Dependencies:** None

### Tasks
1. Initialize React + Vite project with TailwindCSS
2. Set up SQLite database with Prisma
3. Create Todo and Category models
4. Set up Express API with basic structure
5. Create app shell with header and main area

### Deliverables
- [ ] Project runs without errors
- [ ] Database creates successfully
- [ ] Empty app shell renders

### Prompt
```
Set up a Todo app with React, Vite, TailwindCSS, Express, and SQLite with Prisma.

1. Initialize React + Vite project
2. Add TailwindCSS configuration
3. Create Express backend with /api prefix
4. Set up Prisma with SQLite
5. Create models:
   - Category: id (uuid), name (string), color (string)
   - Todo: id (uuid), title (string), completed (boolean), due_date (date nullable), category_id (uuid nullable, FK)
6. Create basic app layout with header showing "Todo App"

Stop when the shell runs and database migrates successfully.
```

---

## Phase 2: Category Management
**Goal:** Full CRUD for categories
**Dependencies:** Phase 1

### Tasks
1. API endpoints for categories
2. Category list sidebar
3. Add/edit category modal
4. Delete category with confirmation
5. Color picker for categories

### Deliverables
- [ ] Can create category with name and color
- [ ] Categories display in sidebar
- [ ] Can edit category
- [ ] Can delete category

### Prompt
```
Implement category management for the Todo app.

1. Create API endpoints:
   - GET /api/categories - list all
   - POST /api/categories - create new
   - PUT /api/categories/:id - update
   - DELETE /api/categories/:id - delete

2. Create sidebar showing category list with colored dots
3. Add "New Category" button that opens modal
4. Modal has: name input, color picker (preset colors), save/cancel
5. Category item has edit and delete buttons
6. Delete shows confirmation before removing

Use a simple color picker with 8 preset colors.

Stop when categories can be created, edited, and deleted.
```

---

## Phase 3: Todo Management
**Goal:** Full todo functionality with categories and due dates
**Dependencies:** Phase 2

### Tasks
1. API endpoints for todos
2. Todo list component with checkboxes
3. Add todo form
4. Edit todo modal
5. Category assignment dropdown
6. Due date picker
7. Filter todos by category (click sidebar)

### Deliverables
- [ ] Can create todo with optional category and due date
- [ ] Can mark todo complete/incomplete
- [ ] Can edit todo details
- [ ] Can delete todo
- [ ] Clicking category filters todos

### Prompt
```
Implement todo management with category assignment and due dates.

1. Create API endpoints:
   - GET /api/todos?category_id=x - list todos, optional filter
   - POST /api/todos - create
   - PUT /api/todos/:id - update
   - DELETE /api/todos/:id - delete

2. Main area shows todo list:
   - Checkbox to toggle complete (strikethrough when done)
   - Title text
   - Category badge (colored)
   - Due date badge (red if overdue)
   - Edit/delete buttons on hover

3. Add todo form at top:
   - Title input (required)
   - Category dropdown (optional)
   - Due date picker (optional)

4. Click category in sidebar to filter todos (highlight selected)
5. Edit todo opens modal with all fields editable

Sort todos: incomplete first, then by due date (soonest first).

Stop when todos can be fully managed with categories and dates.
```

---

## Phase 4: Search and Polish
**Goal:** Add search and polish UX
**Dependencies:** Phase 3

### Tasks
1. Search input in header
2. Search filters todos by title (client-side)
3. Empty states for no todos / no results
4. Loading states
5. Error handling with toast messages
6. Responsive design adjustments

### Deliverables
- [ ] Search filters todos in real-time
- [ ] Empty states display appropriately
- [ ] Errors show user-friendly messages
- [ ] Works on mobile screens

### Prompt
```
Add search functionality and polish the UX.

1. Add search input in header (right side)
2. Search filters todos by title (case-insensitive, client-side)
3. Add empty states:
   - No todos: "No todos yet. Add one above!"
   - No results: "No todos match your search"
   - No category selected + no todos: "Select a category or add a todo"

4. Add loading spinner for initial data fetch
5. Add error toast for API failures
6. Responsive adjustments:
   - Mobile: hide sidebar, add hamburger menu
   - Sidebar overlays on mobile when menu open

Test all flows and fix any visual issues.

This is the final phase - ensure everything works smoothly.
```

---

## Rollback Points
- After Phase 1: Clean slate with just structure
- After Phase 2: Categories work, can redo todo implementation
- After Phase 3: Full functionality, can redo polish

## Risk Mitigation
| Risk | Phase | Mitigation |
|------|-------|------------|
| Prisma schema issues | 1 | Test migration before proceeding |
| Filter state complexity | 3 | Use URL params for filter state |
| Mobile responsive issues | 4 | Test each breakpoint individually |
```

## Output Format

```
# Development Plan: [Project Name]

## Summary
| Metric | Value |
|--------|-------|
| Total Phases | [Number] |
| Estimated Build Time | [Range] |
| Checkpoint Strategy | [Brief] |

---

[Phase-by-phase breakdown with prompts]

---

## Quick Reference

### Phase Prompts (Copy-Paste Ready)

**Phase 1:**
```
[Prompt]
```

**Phase 2:**
```
[Prompt]
```

[Continue for all phases]

---

## Verification Checklist

After each phase, verify:
- [ ] Phase 1: [Key items]
- [ ] Phase 2: [Key items]
[...]

Ready to begin?
```

## Rules

1. **ALWAYS start with foundation phase** — Setup, schema, auth first
2. **ALWAYS end with polish phase** — Error handling, edge cases last
3. **ALWAYS include verification steps** — Testable deliverables per phase
4. **ALWAYS size phases appropriately** — 30-60 minutes ideal
5. **NEVER combine unrelated features** — One major feature per phase
6. **NEVER skip rollback planning** — Document safe rollback points
7. **PREFER explicit prompts** — Include technical details in each phase prompt
