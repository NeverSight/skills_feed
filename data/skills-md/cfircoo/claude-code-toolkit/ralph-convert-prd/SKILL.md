---
name: ralph-convert-prd
description: Converts Product Requirements Documents into prd.json format for the Ralph autonomous agent system. Use when preparing PRDs for Ralph execution, breaking down features into atomic user stories, or when the user mentions Ralph, prd.json, or autonomous agent workflows.
model: claude-opus-4-5
context: fork
---

<objective>
Transform existing Product Requirements Documents into the structured `prd.json` format used by the Ralph autonomous agent system. Each story must be completable in one LLM context window to prevent broken code from context overflow.
</objective>

<quick_start>
1. Read the user's PRD or feature requirements
2. Break down into atomic user stories (one context window each)
3. Order stories by dependency (schema → backend → UI → dashboard)
4. Output valid `prd.json` with verifiable acceptance criteria
</quick_start>

<essential_principles>
<principle name="story_size">
**Critical Rule**: Each story must be completable in ONE Ralph iteration (one context window).

Stories that are too large cause the LLM to run out of context before completion, resulting in broken code.

**Right-sized stories**:
- Add a database column
- Create a UI component
- Update server actions
- Implement a filter

**Too large (split these)**:
- Build entire dashboards
- Add authentication systems
- Refactor entire APIs
</principle>

<principle name="story_ordering">
Stories must execute sequentially without forward dependencies:

1. Schema/database changes
2. Server actions and backend logic
3. UI components
4. Dashboard/summary views

Never reference something that doesn't exist yet.
</principle>

<principle name="acceptance_criteria">
Each criterion must be verifiable and specific. Avoid vague language.

**Good criteria**:
- "Add status column with values: 'pending' | 'in_progress' | 'done'"
- "Filter dropdown includes: All, Active, Completed"
- "Clicking delete shows confirmation dialog"

**Bad criteria** (too vague):
- "Works correctly"
- "Good UX"
- "Handles edge cases"
</principle>

<principle name="mandatory_criteria">
Every story MUST include: `"Typecheck passes"`

UI-focused stories MUST also include: `"Verify in browser using dev-browser skill"`
</principle>
</essential_principles>

<output_format>
```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Specific criterion 1",
        "Specific criterion 2",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**Field requirements**:
- `id`: Sequential US-001, US-002, etc.
- `title`: Short, descriptive action
- `description`: User story format (As a... I want... so that...)
- `acceptanceCriteria`: Array of specific, verifiable criteria
- `priority`: Execution order (1 = first)
- `passes`: Always `false` initially
- `notes`: Empty string initially
</output_format>

<workflow>
1. **Understand the PRD**: Read the full requirements document or feature request
2. **Identify components**: List all database changes, backend logic, UI elements
3. **Decompose into stories**: Break each component into atomic, one-iteration tasks
4. **Order by dependency**: Schema first, then backend, then UI, then dashboards
5. **Write acceptance criteria**: Make each criterion specific and verifiable
6. **Add mandatory criteria**: Ensure every story has "Typecheck passes"
7. **Generate prd.json**: Output the complete JSON structure
8. **Run pre-save checklist**: Verify all requirements before finalizing
</workflow>

<pre_save_checklist>
Before outputting the final prd.json, verify:

- [ ] Previous runs archived (if applicable)
- [ ] Each story completable in one iteration
- [ ] Stories ordered by dependency (no forward references)
- [ ] All stories include "Typecheck passes"
- [ ] UI stories include browser verification criterion
- [ ] Acceptance criteria are verifiable, not vague
- [ ] No story depends on later stories
</pre_save_checklist>

<examples>
<example name="database_story">
```json
{
  "id": "US-001",
  "title": "Add task status column to database",
  "description": "As a developer, I want a status column on tasks so that we can track task progress",
  "acceptanceCriteria": [
    "Add status column to tasks table with type enum('pending', 'in_progress', 'done')",
    "Default value is 'pending'",
    "Migration runs without errors",
    "Typecheck passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": ""
}
```
</example>

<example name="ui_story">
```json
{
  "id": "US-003",
  "title": "Add status filter dropdown to task list",
  "description": "As a user, I want to filter tasks by status so that I can focus on relevant tasks",
  "acceptanceCriteria": [
    "Filter dropdown appears above task list",
    "Options: All, Pending, In Progress, Done",
    "Selecting option filters displayed tasks",
    "Filter persists on page refresh",
    "Typecheck passes",
    "Verify in browser using dev-browser skill"
  ],
  "priority": 3,
  "passes": false,
  "notes": ""
}
```
</example>
</examples>

<success_criteria>
Conversion is complete when:

- [ ] All features from PRD are captured as user stories
- [ ] Each story is atomic (one context window)
- [ ] Stories are properly ordered by dependency
- [ ] All acceptance criteria are specific and verifiable
- [ ] Mandatory criteria ("Typecheck passes") present on all stories
- [ ] UI stories include browser verification
- [ ] Valid JSON structure with all required fields
- [ ] Pre-save checklist passes
</success_criteria>
