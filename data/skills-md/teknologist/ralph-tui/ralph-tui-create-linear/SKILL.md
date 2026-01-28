---
name: ralph-tui-create-linear
description: "Convert PRDs to Linear issues for ralph-tui execution. Creates a master issue (epic) with sub-issues for each user story. Triggers on: create linear issues, convert prd to linear, linear for ralph, ralph linear."
---

# Ralph TUI - Create Linear Issues

Converts PRDs to Linear issues (epic + child issues) for ralph-tui autonomous execution using the built-in Linear tracker.

> **Note:** This skill uses ralph-tui's built-in `convert` command. No external plugins required.

---

## Prerequisites

- **LINEAR_API_KEY** environment variable set (get from https://linear.app/settings/api)
- Know your Linear team ID (UUID format, found in team settings or API)

---

## The Job

Take a PRD (markdown file or text) and create Linear issues:
1. **Extract Quality Gates** from the PRD's "Quality Gates" section
2. Create a **master issue (epic)** in Linear
3. Create **sub-issues** for each user story as children of the epic
4. Set up **blocking relations** based on story dependencies
5. Output epic ID ready for `ralph-tui run --tracker linear --epic TEAM-123`

---

## Step 1: Extract Quality Gates

Look for the "Quality Gates" section in the PRD:

```markdown
## Quality Gates

These commands must pass for every user story:
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting

For UI stories, also include:
- Verify in browser using dev-browser skill
```

Extract:
- **Universal gates:** Commands that apply to ALL stories (e.g., `pnpm typecheck`)
- **UI gates:** Commands that apply only to UI stories (e.g., browser verification)

**If no Quality Gates section exists:** Ask the user what commands should pass, or use a sensible default like `npm run typecheck`.

---

## Creating Issues

Use ralph-tui's built-in convert command:

```bash
# Convert PRD to Linear issues (prompts for team ID if not provided)
ralph-tui convert --to linear ./tasks/prd-feature.md

# Specify team ID directly
ralph-tui convert --to linear ./tasks/prd-feature.md --team-id "<team-uuid>"

# Verbose output to see issue details
ralph-tui convert --to linear ./tasks/prd-feature.md --team-id "<team-uuid>" --verbose
```

The convert command will:
1. Parse the PRD markdown
2. Create a master issue (epic) in Linear
3. Create sub-issues for each user story as children
4. Set up blocking relations based on `dependsOn` in the PRD
5. Output the epic ID for use with ralph-tui

---

## Story Size: The #1 Rule

**Each story must be completable in ONE ralph-tui iteration (~one agent context window).**

ralph-tui spawns a fresh agent instance per iteration with no memory of previous work. If a story is too big, the agent runs out of context before finishing.

### Right-sized stories:
- Add a database column + migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):
- "Build the entire dashboard" → Split into: schema, queries, UI components, filters
- "Add authentication" → Split into: schema, middleware, login UI, session handling
- "Refactor the API" → Split into one story per endpoint or pattern

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big.

---

## Story Ordering: Dependencies First

Stories execute in dependency order. Earlier stories must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
1. ❌ UI component (depends on schema that doesn't exist yet)
2. ❌ Schema change

---

## Dependencies

Dependencies are handled automatically by the convert command:

1. **Parent-child relationships**: All user story issues are created as children of the epic
2. **Blocking relations**: The `dependsOn` array in your PRD creates "blocks" relations in Linear

Example PRD with dependencies:
```markdown
### US-001: Add schema
**Depends on:** (none)

### US-002: Create API
**Depends on:** US-001

### US-003: Build UI
**Depends on:** US-002
```

This creates:
- `US-001` has no blockers
- `US-002` is blocked by `US-001`
- `US-003` is blocked by `US-002`

ralph-tui will:
- Show blocked issues as unavailable until dependencies complete
- Never select an issue for execution while its dependencies are open
- Include dependency context in the prompt when working on an issue

---

## Priority Mapping

ralph-tui maps PRD priorities to Linear's priority scale:

| PRD Priority | TaskPriority | Linear Priority | Linear Display |
|--------------|--------------|-----------------|----------------|
| P0           | 0 (critical) | 1               | Urgent         |
| P1           | 1 (high)     | 2               | High           |
| P2           | 2 (medium)   | 3               | Normal         |
| P3           | 3 (low)      | 4               | Low            |
| P4           | 4 (backlog)  | 0               | No Priority    |

**Note:** Linear's priority 0 means "no priority set" (backlog), while 1 is the highest (urgent).

To set priority in your PRD:
```markdown
### US-001: Critical security fix
**Priority:** P0

### US-002: Regular feature
**Priority:** P2
```

---

## Acceptance Criteria: Quality Gates + Story-Specific

Each issue's description should include acceptance criteria with:
1. **Story-specific criteria** from the PRD (what this story accomplishes)
2. **Quality gates** from the PRD's Quality Gates section (appended at the end)

### Good criteria (verifiable):
- "Add `investorType` column to investor table with default 'cold'"
- "Filter dropdown has options: All, Cold, Friend"
- "Clicking toggle shows confirmation dialog"

### Bad criteria (vague):
- ❌ "Works correctly"
- ❌ "User can do X easily"
- ❌ "Good UX"
- ❌ "Handles edge cases"

---

## Linear Anti-Patterns (Avoid These)

### ❌ Not specifying `--team-id`

```bash
# BAD: Will prompt interactively (blocks automation)
ralph-tui convert --to linear ./prd.md

# GOOD: Specify team ID
ralph-tui convert --to linear ./prd.md --team-id "<team-uuid>"
```

### ❌ Creating issues directly in Linear

Don't create issues manually in Linear's UI - use `ralph-tui convert` to ensure:
- Proper parent-child relationships
- Blocking relations match PRD dependencies
- Consistent formatting for ralph-tui parsing

### ❌ Using Linear's native sub-issues incorrectly

ralph-tui uses Linear's parent-child relationships for epic→story hierarchy. Don't:
- Create nested sub-sub-issues (keep it one level deep)
- Mix manually created sub-issues with ralph-tui managed ones

### ❌ Manually editing issue hierarchy after creation

If you need to restructure:
1. Delete the epic and all children in Linear
2. Update your PRD
3. Re-run `ralph-tui convert --to linear`

### ❌ Using duplicate story IDs

Each story ID must be unique within the PRD:
```markdown
### US-001: First story   ✅
### US-002: Second story  ✅
### US-001: Third story   ❌ Duplicate!
```

---

## Example

**Input PRD (`./tasks/friends-outreach-prd.md`):**
```markdown
# PRD: Friends Outreach

Add ability to mark investors as "friends" for warm outreach.

## Quality Gates

These commands must pass for every user story:
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting

For UI stories, also include:
- Verify in browser using dev-browser skill

## User Stories

### US-001: Add investorType field to investor table
**Priority:** P1
**Description:** As a developer, I need to categorize investors as 'cold' or 'friend'.

**Acceptance Criteria:**
- [ ] Add investorType column: 'cold' | 'friend' (default 'cold')
- [ ] Generate and run migration successfully

### US-002: Add type toggle to investor list rows
**Priority:** P2
**Depends on:** US-001
**Description:** As Ryan, I want to toggle investor type directly from the list.

**Acceptance Criteria:**
- [ ] Each row has Cold | Friend toggle
- [ ] Switching shows confirmation dialog
- [ ] On confirm: updates type in database

### US-003: Filter investors by type
**Priority:** P3
**Depends on:** US-002
**Description:** As Ryan, I want to filter the list to see just friends or cold.

**Acceptance Criteria:**
- [ ] Filter dropdown: All | Cold | Friend
- [ ] Filter persists in URL params
```

**Command:**
```bash
ralph-tui convert --to linear ./tasks/friends-outreach-prd.md --team-id "<team-uuid>" --verbose
```

**Output:**
```
Parsing PRD: ./tasks/friends-outreach-prd.md
Creating epic: Friends Outreach
  Created: TEAM-456

Creating user stories:
  US-001: Add investorType field to investor table
    Created: TEAM-457 (priority: High)
  US-002: Add type toggle to investor list rows
    Created: TEAM-458 (priority: Normal)
    Added blocking relation: blocked by TEAM-457
  US-003: Filter investors by type
    Created: TEAM-459 (priority: Low)
    Added blocking relation: blocked by TEAM-458

Epic ID: TEAM-456
Run with: ralph-tui run --tracker linear --epic TEAM-456
```

---

## Running with ralph-tui

After creating issues, run ralph-tui with the Linear tracker:

```bash
# Option 1: Specify epic directly
ralph-tui run --tracker linear --epic TEAM-456

# Option 2: Initialize first, then run
ralph-tui init --tracker linear --epicId TEAM-456
ralph-tui run

# Option 3: Use project ID instead of epic
ralph-tui init --tracker linear --projectId "project-uuid"
ralph-tui run
```

ralph-tui will:
1. Fetch issues from the specified epic/project
2. Select the highest-priority unblocked issue
3. Generate a prompt with issue details + acceptance criteria
4. Run the agent to implement the story
5. **Update the issue status to "Done" in Linear when completed**
6. Repeat until all stories are done
7. Output `<promise>COMPLETE</promise>` when the epic is finished

> **Note:** ralph-tui automatically updates Linear issue status. No manual status changes or workflow skills needed.

---

## Conversion Rules

1. **Extract Quality Gates** from PRD first
2. **Each user story → one Linear issue**
3. **First story**: No blocking relations (creates foundation)
4. **Subsequent stories**: Blocked by their dependencies
5. **Priority**: Mapped from PRD priority (see Priority Mapping table)
6. **All stories**: Created with "unstarted" workflow state
7. **Acceptance criteria**: Story criteria + quality gates appended
8. **UI stories**: Also append UI-specific gates (browser verification)

---

## Checklist Before Converting

- [ ] Extracted Quality Gates from PRD (or asked user if missing)
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema → backend → UI)
- [ ] Quality gates included in PRD for all stories
- [ ] UI stories have browser verification (if specified in Quality Gates)
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story (dependencies flow forward)
- [ ] No circular dependencies
- [ ] `--team-id` ready for the convert command
- [ ] LINEAR_API_KEY environment variable is set
