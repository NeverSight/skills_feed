---
name: initiative-tracker
description: |
  Manage product initiatives, epics, and stakeholders through natural language commands.
  Stores data as Logseq-compatible markdown files with YAML frontmatter.

  Use when users need to:
  - Create, update, list, or show initiatives and epics
  - Track completeness of initiative documentation
  - Manage people, teams, and partners
  - Check what information is missing
  - Initialize the repository structure

  Triggers on: /init_repository, /create_initiative, /list_initiatives, /show_initiative,
  /update_initiative, /what_missing, /create_epic, /list_epics, /create_person,
  /create_team, /create_partner, /create_product_area, /list_product_areas,
  /show_product_area, /update_product_area, /help
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*)
---

# Initiative Tracker Skill - Complete Documentation

## Overview

Conversational interface for managing product initiatives as Logseq-compatible markdown files. This skill enables natural language commands to create, update, and track initiatives, epics, and stakeholders with automatic completeness calculation and history tracking.

**Data Storage:** Logseq-compatible markdown files with YAML frontmatter
**Output:** Structured markdown files in `initiatives/` directory

---

## Available Commands

This skill provides natural language commands for managing product initiatives. All commands can be invoked using the `/` prefix.

### Repository Setup
- `/init_repository` - Create folder structure in current directory
- `/help` - List available commands

### Initiative Management
- `/create_initiative <id> <title> [jira_id]` - Create new initiative
- `/list_initiatives [--status=X] [--completeness<N]` - List all with completeness
- `/show_initiative <id|jira_id>` - Display full details
- `/update_initiative <id> <field> <value>` - Modify field
- `/what_missing <id>` - Show incomplete fields

### Epic Management
- `/create_epic <id> <title> <initiative_id> [jira_id]` - Create new epic
- `/list_epics [--initiative=X] [--status=X]` - List epics
- `/show_epic <id|jira_id>` - Display full details

### Entity Management
- `/create_person <id> <name>` - Create person
- `/create_team <id> <name>` - Create team
- `/create_partner <id> <name>` - Create partner
- `/create_product_area <id> <name>` - Create product area
- `/list_product_areas` - List all product areas
- `/show_product_area <id>` - Show product area details
- `/update_product_area <id> <field> <value>` - Update product area field

---

## Data Location

All data stored in `initiatives/` directory:
```
initiatives/
├── _schema/schema-v1.md      # Schema definition
├── _index/jira-mapping.md    # Jira ID lookup
├── initiatives/*.md          # Initiative files
├── epics/*.md               # Epic files
├── people/*.md              # Person files
├── teams/*.md               # Team files
├── partners/*.md            # Partner files
└── product-areas/*.md       # Product area files
```

## File Format

All entities use YAML frontmatter + markdown body + history log:

```yaml
---
id: customer-onboarding
title: Customer Onboarding Simplification
status: Draft
completeness: 45
created_at: 2026-01-21T10:00:00+01:00
updated_at: 2026-01-21T10:00:00+01:00
---

# Customer Onboarding Simplification

## Expected Outcome
(content here)

## History
H-a1b2c3 | 2026-01-21T10:00:00+01:00 | created | | | | user | Initial creation
```

## Wikilinks

Reference other entities with `[[path/id]]` syntax:
- People: `[[people/anna-andersson]]`
- Teams: `[[teams/platform-team]]`
- Partners: `[[partners/partner-alpha]]`
- ProductAreas: `[[product-areas/customer-management]]`
- Epics: `[[epics/qr-scanner]]`

## Completeness Calculation

Auto-calculated percentage based on filled **recommended** fields:
- 90-100%: Complete
- 70-89%: Mostly complete
- 50-69%: Partially complete
- 0-49%: Incomplete

Display format: `92% ████████░░`

## Status Workflow

### Initiative Status
`Draft` → `Defined` → `Planned` → `In Progress` → `Finished` or `Abandoned`

Each transition has required fields - see [status-transitions.md](references/status-transitions.md).

### Epic Status
`Not Started` → `In Progress` → `Done` or `Abandoned`

## History Tracking

Every change creates a history entry:
```
ID | TIMESTAMP | ACTION | FIELD | OLD_VALUE | NEW_VALUE | ACTOR | NOTE
```

History ID format: `H-xxxxxx` (6 alphanumeric characters)

Actions: `created`, `field_updated`, `status_changed`, `stakeholder_added`, etc.

---

## Implementation Instructions

**CRITICAL REQUIREMENTS:**
- This skill MUST persist all data to disk using the Python scripts
- Never simulate operations - always write actual files
- Always build and use the index for queries
- Always get user approval before writing data

### Skill Initialization

**ALWAYS do this when the skill is first invoked:**

1. Build/load the search index for fast querying:
   ```bash
   python .claude/skills/initiative-tracker/scripts/build_index.py
   ```

2. Read the index into memory:
   ```bash
   Read tool: initiatives/_index/index.json
   ```

3. Parse and store the index JSON in memory for the session

This enables instant queries even with hundreds of entities.

---

### Approval Workflow

**⚠️ CRITICAL: User Approval Required**

BEFORE writing any data to disk, you MUST:

1. **Show a preview** of what will be written:
   - Display the complete file content (frontmatter + body + history)
   - Show the file path where it will be saved
   - Show the completeness percentage

2. **Ask for user approval** using one of these methods:
   - Use AskUserQuestion tool with options: "Approve", "Modify", "Cancel"
   - Wait for explicit user confirmation

3. **Only proceed** if user approves:
   - If "Approve": Write the file as shown
   - If "Modify": Ask what changes are needed, update preview, ask again
   - If "Cancel": Abort the operation, don't write anything

4. **After writing**: Confirm success and show the actual file path created

**This applies to ALL commands that write data**: `/create_initiative`, `/update_initiative`, `/create_epic`, `/create_person`, `/create_team`, `/create_partner`

---

### Path Conventions

- Python scripts are in: `.claude/skills/initiative-tracker/scripts/`
- Data files are in: `initiatives/` (at project root)
- Always use relative paths from project root
- Use forward slashes in paths for cross-platform compatibility

---

### Index System for Fast Querying

**⚠️ CRITICAL: Performance Requirement**

For performance at scale, this skill uses an in-memory index for fast queries.

#### Index Location

The index is stored at: `initiatives/_index/index.json`

It contains metadata for all entities (initiatives, epics, people, teams, partners, product areas) extracted from their markdown files.

#### Build/Rebuild the Index

**At skill startup, ALWAYS build/load the index:**

1. Build the index from all markdown files:
   ```bash
   python .claude/skills/initiative-tracker/scripts/build_index.py
   ```
   This creates/updates `initiatives/_index/index.json`

2. Load the index into memory using Read tool:
   ```bash
   Read tool: initiatives/_index/index.json
   ```

3. Parse the JSON and keep it in memory for the session

**Rebuild the index AFTER every write operation:**
- After creating/updating initiatives, epics, people, teams, partners, or product areas
- Run the build_index.py script again
- Reload the updated index

#### Using the Index for Queries

**ALWAYS prefer index-based queries over file globbing/reading:**

**For /list_initiatives:**
- Use the index instead of globbing files
- Filter initiatives array by status/completeness in memory
- Much faster, especially with 100+ initiatives

**For /list_epics:**
- Use the epics array from index
- Filter by initiative_id or status in memory

**For searches:**
- Find all initiatives where a person is initiator: filter index by initiator field
- Find all initiatives with a specific stakeholder: filter by stakeholders array
- Find all epics for an initiative: filter epics by initiative_id
- Find all open actions assigned to a person: filter initiatives by actions array
- Find initiatives with overdue actions: filter by actions with due_date < today
- Find initiatives with >3 open questions: filter by open_question_count > 3

**Action queries (using index):**
```python
# Example: Get all my open actions
my_actions = []
for initiative in index['initiatives']:
    for action in initiative.get('actions', []):
        if action.get('assigned_to') == 'my-id' and action['status'] == 'Open':
            my_actions.append({
                'initiative': initiative['id'],
                'action_id': action['id'],
                'description': action['description'],
                'due_date': action.get('due_date'),
            })
```

**When to read actual files:**
- `/show_initiative` - need full body content and history
- `/update_initiative` - need to modify and write back
- `/add_action`, `/complete_action` - need to modify body sections
- Any operation requiring full markdown content or full action descriptions

#### Index Structure

**IMPORTANT**: The index contains ONLY small metadata fields, NOT large text content.

**Indexed fields (small)**:
- IDs, titles, status, completeness, jira_id
- References (initiator, stakeholders, team members as ID lists)
- Small metadata (timestamps, affected_systems, planned_quarter)
- Flags (deleted)
- **Embedded actions** (id, description, status, assigned_to, due_date)
- **Embedded questions** (id, status)
- Counts (action_count, open_action_count, open_question_count)

**NOT indexed (large text)**:
- expected_outcome, outcome_validation (initiatives)
- description, acceptance_criteria (epics)
- notes (all entities)
- Body content, history entries
- Full question text, answers
- Solution details, pros/cons

This keeps the index small (<100KB even with 500+ entities) for fast loading.

```json
{
  "metadata": {
    "generated_at": "2026-01-21 22:00",
    "total_entities": 10
  },
  "initiatives": [
    {
      "id": "app-management",
      "type": "initiative",
      "file_path": "initiatives/initiatives/app-management.md",
      "title": "Application Management",
      "status": "Draft",
      "completeness": 25,
      "jira_id": "PROJ-100",
      "initiator": ["olle-jansson"],
      "stakeholders": ["acme-inc"],
      "intended_users": [],
      "affected_systems": ["agent"],
      "epics": [],
      "actions": [
        {
          "id": "ACT-001",
          "description": "Review security requirements",
          "status": "Open",
          "assigned_to": "olle-jansson",
          "due_date": "2026-01-25"
        },
        {
          "id": "ACT-002",
          "description": "Schedule kickoff meeting",
          "status": "Done"
        }
      ],
      "questions": [
        {
          "id": "Q-001",
          "status": "Open"
        }
      ],
      "action_count": 2,
      "open_action_count": 1,
      "open_question_count": 1,
      "created_at": "2026-01-21 22:32",
      "updated_at": "2026-01-21 22:35",
      "deleted": false
    }
  ],
  "epics": [...],
  "people": [...],
  "teams": [...],
  "partners": [...],
  "product_areas": [...]
}
```

#### Performance Benefits

- Listing 500 epics: ~1ms (index) vs ~5 seconds (file globbing)
- Complex searches: Instant (filter in memory) vs very slow (scan all files)
- Finding relationships: Fast array operations vs nested file reads

### Command: /create_initiative <id> <title> [jira_id]

**Step 1: Prepare the initiative**

1. Generate history ID:
   ```bash
   python .claude/skills/initiative-tracker/scripts/generate_history_id.py
   ```
2. Calculate completeness (will be 0 for new Draft initiative)
3. Build JSON frontmatter with required fields:
   ```json
   {
     "id": "<id>",
     "title": "<title>",
     "status": "Draft",
     "jira_id": "<jira_id or empty>",
     "initiator": "",
     "expected_outcome": "",
     "outcome_validation": "",
     "intended_users": [],
     "stakeholders": [],
     "source_document": "",
     "source_jira_id": "",
     "solution_design": "",
     "epics": [],
     "user_journey": "",
     "ui_design": "",
     "affected_systems": []
   }
   ```
4. Build initial body content (markdown):
   ```markdown
   # <title>

   ## Expected Outcome

   (Describe what success looks like for this initiative)

   ## Outcome Validation

   (How will we measure/verify the outcome was achieved?)

   ## Intended Users

   (Who benefits from this initiative?)

   ## Solutions

   (Proposed approaches - add solutions as subsections)

   ## Actions

   (Action items - use checkbox format)

   ## Open Questions

   (Unresolved questions - use checkbox format)
   ```

**Step 2: Show preview and get approval**

5. Display the complete file preview to user:
   ```
   📄 Preview: initiatives/initiatives/<id>.md
   Completeness: 0% (Draft status)

   ---
   [Show complete YAML frontmatter]
   ---

   [Show complete body content]

   ## History
   [Show history entry]
   ```

6. Ask for user approval using AskUserQuestion:
   - Options: "Approve and create", "Modify content", "Cancel"

**Step 3: Write if approved**

7. If user approves, write the file using Write tool to `initiatives/initiatives/<id>.md`:
   - Combine frontmatter (YAML between ---), body, and history
   - Ensure proper formatting

8. Confirm file was created by reading back: `initiatives/initiatives/<id>.md`
9. **Rebuild the index** to include the new initiative:
   ```bash
   python .claude/skills/initiative-tracker/scripts/build_index.py
   ```
10. **Reload the index** into memory for subsequent queries
11. Report success to user: "✓ Initiative <id> created at initiatives/initiatives/<id>.md (0% complete)"

### Command: /update_initiative <id> <field> <value>

**Step 1: Read and prepare update**

1. Read the initiative file using Read tool: `initiatives/initiatives/<id>.md`
2. Parse YAML frontmatter and body content
3. Identify the change:
   - If field is in frontmatter: update frontmatter
   - If field is in body (expected_outcome, outcome_validation): update markdown section
4. Generate new history ID:
   ```bash
   python .claude/skills/initiative-tracker/scripts/generate_history_id.py
   ```
5. Create history entry with old/new values
6. Update `updated_at` timestamp to current time
7. Recalculate completeness using the completeness script

**Step 2: Show preview of changes**

8. Display a diff preview to user:
   ```
   📄 Updating: initiatives/initiatives/<id>.md

   CHANGES:
   - <field>: "<old_value>" → "<new_value>"
   - updated_at: "<old_timestamp>" → "<new_timestamp>"
   - completeness: <old_%> → <new_%>

   NEW HISTORY ENTRY:
   <history_id> | <timestamp> | field_updated | <field> | <old> | <new> | <actor> | <note>

   [Optionally show full file preview if major change]
   ```

9. Ask for user approval using AskUserQuestion:
   - Options: "Approve changes", "Modify", "Cancel"

**Step 3: Write if approved**

10. If approved, write complete updated file using Write tool to `initiatives/initiatives/<id>.md`
11. Confirm update by reading file back
12. **Rebuild the index** to reflect the changes:
    ```bash
    python .claude/skills/initiative-tracker/scripts/build_index.py
    ```
13. **Reload the index** into memory
14. Report success: "✓ Updated <field> in <id> (completeness: <new_%>)"

### Command: /list_initiatives [--status=X] [--completeness<N] [--product-area=X]

**Use the index for fast querying** (see Index System section above)

1. Ensure index is loaded in memory (if not, load it from `initiatives/_index/index.json`)
2. Filter the `initiatives` array from index:
   - If `--status=X` provided: filter where `status === X`
   - If `--completeness<N` provided: filter where `completeness < N`
   - If `--product-area=X` provided: filter where `product_area` contains `X`
3. Format as table:
   ```
   | ID | Title | Status | Product Area | Completeness |
   |---|---|---|---|---|
   | <id> | <title> | <status> | <product_area> | <completeness>% <bar> |
   ```
   Where <bar> is a visual bar like `████████░░` (10 characters, filled proportional to percentage).
4. Display table to user with total count.

**Performance**: This is instant even with 100+ initiatives (no file I/O required).

---

### Command: /show_initiative <id|jira_id>

1. If jira_id provided, read `initiatives/_index/jira-mapping.md` to map to id.
2. Read initiative file: `initiatives/initiatives/<id>.md`
3. Parse frontmatter, body, and history.
4. Display formatted output:
   - Title and basic info
   - All frontmatter fields
   - Body content sections
   - History entries (last 5)
   - Completeness percentage with bar

---

### Command: /what_missing <id>

1. Read initiative file: `initiatives/initiatives/<id>.md`
2. Parse frontmatter.
3. Call: `python scripts/calculate_completeness.py initiative '<json_frontmatter>'`
4. Check which recommended fields are empty:
   - intended_users
   - stakeholders
   - source_document
   - affected_systems
5. Check required fields for current status (see references/status-transitions.md).
6. Display missing fields grouped by category:
   - Missing required fields (blocks status transition)
   - Missing recommended fields (reduces completeness)

---

### Command: /init_repository

1. Run Python script from project root:
   ```bash
   python .claude/skills/initiative-tracker/scripts/init_repository.py
   ```
2. This creates the directory structure in `initiatives/` at project root.
3. Confirm directories exist using Glob or Bash ls.
4. Report success to user.

---

### Command: /create_epic <id> <title> <initiative_id> [jira_id]

1. Generate history ID:
   ```bash
   python .claude/skills/initiative-tracker/scripts/generate_history_id.py
   ```
2. Build JSON frontmatter:
   ```json
   {
     "id": "<id>",
     "title": "<title>",
     "initiative_id": "<initiative_id>",
     "status": "Not Started",
     "jira_id": "<jira_id or empty>",
     "assigned_team": "",
     "planned_quarter": "",
     "description": "",
     "acceptance_criteria": [],
     "dependencies": []
   }
   ```
3. Build body content:
   ```markdown
   # <title>

   ## Description

   (What this epic delivers)

   ## Acceptance Criteria

   - [ ] Criterion 1
   - [ ] Criterion 2
   ```
4. Call write_entity.py to create `initiatives/epics/<id>.md`:
   ```bash
   python .claude/skills/initiative-tracker/scripts/write_entity.py "initiatives/epics/<id>.md" "epic" '<json>' '<body>'
   ```
5. Update parent initiative to add epic wikilink reference: `[[epics/<id>]]`
6. Report success.

---

### Command: /list_epics [--initiative=X] [--status=X] [--product-area=X]

**Use the index for fast querying** (see Index System section above)

1. Ensure index is loaded in memory (if not, load it from `initiatives/_index/index.json`)
2. Filter the `epics` array from index:
   - If `--initiative=X` provided: filter where `initiative_id === X`
   - If `--status=X` provided: filter where `status === X`
   - If `--product-area=X` provided: filter where `product_area` contains `X`
3. Format as table showing: id, title, initiative_id, product_area, status, completeness
4. Display table to user with total count.

**Performance**: Instant even with 500+ epics.

---

### Command: /create_person <id> <name>

1. Build frontmatter with id, name.
2. Create file at `initiatives/people/<id>.md`.
3. Use write_entity.py script.

---

### Command: /create_team <id> <name>

1. Build frontmatter with id, name.
2. Create file at `initiatives/teams/<id>.md`.
3. Use write_entity.py script.

---

### Command: /create_partner <id> <name>

1. Build frontmatter with id, name.
2. Create file at `initiatives/partners/<id>.md`.
3. Use write_entity.py script.

---

### Command: /create_product_area <id> <name>

1. Build frontmatter with id, name.
2. Create file at `initiatives/product-areas/<id>.md`.
3. Use write_entity.py script.

---

### Command: /list_product_areas

**Use the index for fast querying**

1. Ensure index is loaded in memory (if not, load it from `initiatives/_index/index.json`)
2. Get all product areas from the `product_areas` array in index
3. Format as table showing: id, name, product_manager, line_manager, completeness
4. Display table to user with total count.

**Performance**: Instant even with 100+ product areas.

---

### Command: /show_product_area <id>

1. Read product area file: `initiatives/product-areas/<id>.md`
2. Parse frontmatter, body, and history.
3. Display formatted output:
   - Name and basic info
   - All team roles (product_manager, line_manager, product_owner, architect, ux_designer)
   - Focus area
   - Body content sections
   - History entries (last 5)
   - Completeness percentage with bar
   - List of initiatives assigned to this product area (from index)
   - List of epics assigned to this product area (from index)

---

### Command: /update_product_area <id> <field> <value>

Follow the same pattern as `/update_initiative`:

1. Read the product area file
2. Parse YAML frontmatter and body
3. Update the specified field
4. Generate new history entry
5. Recalculate completeness
6. Show preview and get user approval
7. Write updated file if approved
8. Rebuild index

---

## Embedded Entity Commands

These commands manage actions, questions, and solutions within initiatives.

---

### Command: /add_action <initiative_id> <description> [--assigned=person_id] [--due=YYYY-MM-DD]

Add an action item to an initiative.

**Step 1: Prepare the action**

1. Read initiative file: `initiatives/initiatives/<initiative_id>.md`
2. Parse current content (frontmatter, body, history)
3. Generate unique action ID (auto-increment: ACT-001, ACT-002, etc.)
4. Generate history ID for this change
5. Build action entry:
   ```markdown
   - [ ] ACT-XXX: <description>
     assigned:: [[people/<person_id>]]
     due:: YYYY-MM-DD
     status:: Open
     created_at:: YYYY-MM-DD HH:MM
   ```

**Step 2: Show preview**

6. Display preview of the action to be added:
   ```
   📄 Adding action to: <initiative_id>

   NEW ACTION:
   - [ ] ACT-003: Schedule UX review session with design team
     assigned:: [[people/anna-andersson]]
     due:: 2026-01-28
     status:: Open
     created_at:: 2026-01-21 23:15

   This will be added to the "## Actions" section.
   Completeness will change: 45% → 50%
   ```

7. Ask for approval: "Add this action?", "Modify", "Cancel"

**Step 3: Write if approved**

8. Insert action into "## Actions" section of body
9. Add history entry: `action_added | ACT-XXX | | | <actor> | <description>`
10. Update `updated_at` timestamp
11. Recalculate completeness (actions with assignee and due_date improve score)
12. Write updated file
13. Rebuild index
14. Report success: "✓ Added action ACT-003 to <initiative_id>"

---

### Command: /complete_action <initiative_id> <action_id>

Mark an action as complete.

**Step 1: Prepare completion**

1. Read initiative file
2. Find action by ID in "## Actions" section
3. Generate history ID
4. Update action:
   - Change checkbox: `- [ ]` → `- [x]`
   - Update status: `status:: Open` → `status:: Done`
   - Add `completed_at:: YYYY-MM-DD HH:MM`

**Step 2: Show preview**

5. Display change preview:
   ```
   📄 Completing action in: <initiative_id>

   ACTION: ACT-003
   Status: Open → Done
   Completed: 2026-01-22 10:30

   - [x] ACT-003: Schedule UX review session
     status:: Done
     completed_at:: 2026-01-22 10:30
   ```

6. Ask for approval

**Step 3: Write if approved**

7. Update action in body
8. Add history entry: `action_completed | ACT-XXX | Open | Done | <actor> |`
9. Update timestamps, recalculate completeness
10. Write, rebuild index, report success

---

### Command: /list_actions [--initiative=X] [--assigned=person_id] [--status=Open|Done] [--overdue]

List actions using the index for instant results.

**Use the index for fast querying:**

1. Ensure index is loaded in memory
2. Filter initiatives and extract actions:
   ```python
   results = []
   for initiative in index['initiatives']:
       for action in initiative.get('actions', []):
           # Apply filters
           if initiative_filter and initiative['id'] != initiative_filter:
               continue
           if assigned_filter and action.get('assigned_to') != assigned_filter:
               continue
           if status_filter and action['status'] != status_filter:
               continue
           if overdue_flag:
               due = action.get('due_date')
               if not due or due >= today:
                   continue

           results.append({
               'initiative': initiative['id'],
               'initiative_title': initiative['title'],
               'action_id': action['id'],
               'description': action['description'],
               'status': action['status'],
               'assigned_to': action.get('assigned_to', ''),
               'due_date': action.get('due_date', ''),
           })
   ```

3. Format as table:
   ```
   | Initiative | Action | Description | Assigned | Due | Status |
   |------------|--------|-------------|----------|-----|--------|
   | customer-onboarding | ACT-001 | Review security... | olle-jansson | 2026-01-25 | Open |
   ```

4. Display table with total count

**Performance**: Instant even with 1000+ actions across hundreds of initiatives (no file I/O).

**Examples:**
```
/list_actions --assigned=anna-andersson --status=Open
/list_actions --initiative=customer-onboarding
/list_actions --overdue
```

---

### Command: /add_question <initiative_id> <question> [--asked_by=person_id]

Add an open question to an initiative.

**Step 1: Prepare question**

1. Read initiative file
2. Generate question ID (Q-001, Q-002, etc.)
3. Generate history ID
4. Build question entry:
   ```markdown
   - [ ] Q-003: What's the fallback if Bluetooth is disabled?
     asked_by:: [[people/anna-andersson]]
     asked_at:: 2026-01-21 23:20
     status:: Open
   ```

**Step 2: Show preview and get approval**

5. Display preview:
   ```
   📄 Adding question to: <initiative_id>

   NEW QUESTION:
   - [ ] Q-003: What's the fallback if Bluetooth is disabled?
     asked_by:: [[people/anna-andersson]]
     asked_at:: 2026-01-21 23:20
     status:: Open

   This will be added to "## Open Questions" section.
   Note: >3 open questions will trigger warning on "In Progress" status transition.
   ```

6. Ask for approval

**Step 3: Write if approved**

7. Insert into "## Open Questions" section
8. Add history entry: `question_added | Q-XXX | | | <actor> | <question_text>`
9. Update timestamps
10. Write, rebuild index, report success

---

### Command: /answer_question <initiative_id> <question_id> <answer> [--answered_by=person_id]

Resolve an open question.

**Step 1: Prepare answer**

1. Read initiative file
2. Find question by ID
3. Generate history ID
4. Update question:
   - Change checkbox: `- [ ]` → `- [x]`
   - Add `answer:: <answer_text>`
   - Add `answered_by:: [[people/<person_id>]]`
   - Add `answered_at:: YYYY-MM-DD HH:MM`
   - Update `status:: Open` → `status:: Answered`

**Step 2: Show preview**

5. Display change:
   ```
   📄 Answering question in: <initiative_id>

   QUESTION: Q-002
   Status: Open → Answered

   - [x] Q-002: What's the fallback if Bluetooth is disabled?
     answer:: Manual entry via QR code or NFC tag
     answered_by:: [[people/erik-svensson]]
     answered_at:: 2026-01-22 11:00
     status:: Answered
   ```

6. Ask for approval

**Step 3: Write if approved**

7. Update question in body
8. Add history entry: `question_answered | Q-XXX | Open | Answered | <actor> |`
9. Update timestamps
10. Write, rebuild index, report success

---

### Command: /add_solution <initiative_id> <solution_id> <title> <description>

Add a solution proposal to an initiative.

**Step 1: Prepare solution**

1. Read initiative file
2. Generate history ID
3. Build solution subsection:
   ```markdown
   ### <solution_id>: <title>
   status:: Proposed
   proposed_by:: [[people/<current_user>]]
   proposed_at:: YYYY-MM-DD HH:MM

   <description>

   **Pros:**
   - (add pros here)

   **Cons:**
   - (add cons here)
   ```

**Step 2: Show preview**

5. Display preview:
   ```
   📄 Adding solution to: <initiative_id>

   NEW SOLUTION:
   ### bluetooth-discovery: Bluetooth Auto-Discovery
   status:: Proposed
   proposed_by:: [[people/anna-andersson]]
   proposed_at:: 2026-01-21 23:30

   Automatic discovery via Bluetooth Low Energy.

   **Pros:**
   - (to be filled)

   **Cons:**
   - (to be filled)

   This will be added to "## Solutions" section.
   Note: Complete pros/cons to improve completeness.
   ```

6. Ask for approval

**Step 3: Write if approved**

7. Insert into "## Solutions" section
8. Add history entry: `solution_added | <solution_id> | | | <actor> | <title>`
9. Update timestamps, recalculate completeness
10. Write, rebuild index, report success

---

### Command: /decide_solution <initiative_id> <solution_id> <decision>

Accept or reject a solution proposal.

Where `<decision>` is "accept" or "reject".

**Step 1: Prepare decision**

1. Read initiative file
2. Find solution by ID in "## Solutions" section
3. Generate history ID
4. Update solution:
   - Change `status:: Proposed` → `status:: Accepted` or `status:: Rejected`
   - Add `decided_at:: YYYY-MM-DD HH:MM`

**Step 2: Show preview**

5. Display change:
   ```
   📄 Deciding on solution in: <initiative_id>

   SOLUTION: qr-code-approach
   Decision: Proposed → Accepted

   ### qr-code-approach: QR Code Based
   status:: Accepted
   decided_at:: 2026-01-22 12:00

   Selected as primary approach after team review.
   ```

6. Ask for approval

**Step 3: Write if approved**

7. Update solution status in body
8. Add history entry: `solution_decided | <solution_id> | Proposed | <Accepted|Rejected> | <actor> | <note>`
9. Update timestamps
10. Write, rebuild index, report success

---

## Planning and Query Commands

These commands provide high-level views and queries across initiatives, epics, and actions.

---

### Command: /prepare_meeting <person_id|partner_id>

Prepare context for a meeting with a person or partner. Uses index for instant results.

**Implementation:**

1. Identify entity type (person or partner) from ID
2. Query index for all initiatives where this entity is involved:
   ```python
   relevant_initiatives = []
   for initiative in index['initiatives']:
       # Check if person/partner is involved
       if entity_id in initiative.get('initiator', []):
           relevant_initiatives.append(initiative)
       elif entity_id in initiative.get('stakeholders', []):
           relevant_initiatives.append(initiative)
       elif entity_id in initiative.get('intended_users', []):
           relevant_initiatives.append(initiative)

       # Also check if assigned to any actions
       for action in initiative.get('actions', []):
           if action.get('assigned_to') == entity_id:
               relevant_initiatives.append(initiative)
               break
   ```

3. For each initiative, extract:
   - Current status and completeness
   - Recent changes (last 7 days from updated_at)
   - Open questions
   - Actions assigned to this person
   - Incomplete recommended fields

4. Format output:
   ```
   📋 Meeting Preparation: <Name>
   Role: <role> at <organization>

   INITIATIVES (<count>)

   1. <title> (Status: <status>, <completeness>%)
      - Your role: <Initiator|Stakeholder|Intended User>
      - Last updated: <days> ago
      - Open actions assigned to you: <count>
      - Open questions: <count>
      - ⚠️ Missing: <list if completeness < 80%>

   ACTIONS ASSIGNED (<count>)
   - ACT-001 in <initiative>: <description> (Due: <date>)
   - ACT-002 in <initiative>: <description> (⚠️ Overdue)

   OPEN QUESTIONS TO DISCUSS
   - Q-001 in <initiative>: <first 50 chars>...

   TALKING POINTS
   - <initiative> needs stakeholder input on <field>
   - <initiative> has 3 open questions
   ```

5. **Performance**: Instant (all data from index)

**Example:**
```
/prepare_meeting anna-andersson
```

---

### Command: /my_work [person_id]

Show all work items for a person (defaults to current user).

**Implementation:**

1. Query index for all open actions assigned to person:
   ```python
   my_actions = []
   for initiative in index['initiatives']:
       for action in initiative.get('actions', []):
           if action.get('assigned_to') == person_id and action['status'] == 'Open':
               my_actions.append({
                   'initiative': initiative,
                   'action': action,
               })
   ```

2. Group by due date:
   - Overdue (due_date < today)
   - This week (due_date within 7 days)
   - Later (due_date > 7 days)
   - No due date

3. Also show initiatives where person is initiator

4. Format output:
   ```
   📊 My Work: <Name>

   OVERDUE ACTIONS (2)
   ⚠️ ACT-001: Review security requirements (customer-onboarding)
      Due: 2026-01-20 (2 days ago)
   ⚠️ ACT-003: Schedule kickoff (app-management)
      Due: 2026-01-19 (3 days ago)

   THIS WEEK (3)
   - ACT-005: Finalize design (customer-onboarding) - Due: 2026-01-24
   - ACT-007: Update docs (reduce-resource) - Due: 2026-01-26
   - ACT-009: Review proposal (app-management) - Due: 2026-01-27

   LATER (1)
   - ACT-012: Q2 planning (roadmap-2026) - Due: 2026-02-15

   NO DUE DATE (2)
   - ACT-002: Research alternatives (customer-onboarding)
   - ACT-008: Gather feedback (app-management)

   MY INITIATIVES AS INITIATOR (2)
   - customer-onboarding (In Progress, 85%)
   - app-management (Draft, 25% - needs attention)
   ```

**Performance**: Instant

---

### Command: /overdue

Show all overdue actions across all initiatives.

**Implementation:**

1. Get current date
2. Query index for actions with due_date < today and status = Open:
   ```python
   import datetime
   today = datetime.date.today().isoformat()

   overdue = []
   for initiative in index['initiatives']:
       for action in initiative.get('actions', []):
           if action['status'] == 'Open' and action.get('due_date'):
               if action['due_date'] < today:
                   overdue.append({
                       'initiative': initiative,
                       'action': action,
                       'days_overdue': calculate_days(action['due_date'], today),
                   })

   # Sort by days overdue (most overdue first)
   overdue.sort(key=lambda x: x['days_overdue'], reverse=True)
   ```

3. Format output:
   ```
   ⚠️ OVERDUE ACTIONS (5)

   5 days overdue:
   - ACT-001: Review security requirements
     Initiative: customer-onboarding
     Assigned: anna-andersson
     Due: 2026-01-16

   3 days overdue:
   - ACT-003: Schedule kickoff meeting
     Initiative: app-management
     Assigned: olle-jansson
     Due: 2026-01-18

   [... more ...]

   Total: 5 overdue actions across 3 initiatives
   ```

**Performance**: Instant

---

### Command: /quarter_plan <quarter> [--team=team_id]

Show work planned for a specific quarter.

**Implementation:**

1. Parse quarter (e.g., "2026-Q1")
2. Query index for epics with planned_quarter matching:
   ```python
   epics_in_quarter = [
       epic for epic in index['epics']
       if epic.get('planned_quarter') == quarter
   ]

   # Optional: filter by team
   if team_filter:
       epics_in_quarter = [
           epic for epic in epics_in_quarter
           if team_filter in epic.get('assigned_team', [])
       ]
   ```

3. Group by initiative and status

4. Calculate totals:
   - Total epics in quarter
   - By status (Not Started, In Progress, Done)
   - By team (if multiple teams)

5. Format output:
   ```
   📅 Quarter Plan: 2026-Q1

   SUMMARY
   - Total epics: 12
   - Not Started: 5
   - In Progress: 4
   - Done: 3

   BY INITIATIVE

   customer-onboarding (3 epics)
   ✓ qr-scanner (Done, platform-team)
   → backend-preregistration (In Progress, platform-team)
   - mobile-integration (Not Started, mobile-team)

   app-management (2 epics)
   → api-refactor (In Progress, platform-team)
   - security-hardening (Not Started, platform-team)

   [... more ...]

   TEAM WORKLOAD
   - platform-team: 8 epics
   - mobile-team: 3 epics
   - backend-team: 1 epic
   ```

**Performance**: Instant

**Example:**
```
/quarter_plan 2026-Q1
/quarter_plan 2026-Q2 --team=platform-team
```

---

### Command: /roadmap <start_quarter> <end_quarter> [--team=team_id]

Multi-quarter roadmap view.

**Implementation:**

1. Parse quarter range (e.g., "2026-Q1" to "2026-Q4")
2. Query all epics in range
3. Group by quarter and initiative
4. Format as timeline:
   ```
   🗺️ Roadmap: 2026-Q1 to 2026-Q4

   2026-Q1 (12 epics)
   ├─ customer-onboarding: 3 epics
   ├─ app-management: 2 epics
   └─ reduce-resource: 1 epic

   2026-Q2 (8 epics)
   ├─ customer-onboarding: 1 epic
   ├─ api-v2: 4 epics
   └─ security-initiative: 2 epics

   2026-Q3 (6 epics)
   └─ [...]

   2026-Q4 (4 epics)
   └─ [...]

   TOTAL: 30 epics across 4 quarters
   ```

**Performance**: Instant

---

### Command: /incomplete [entity_type] [--threshold=N]

Show entities below completeness threshold.

**Implementation:**

1. Default threshold = 70%
2. Filter index by completeness:
   ```python
   incomplete = []
   for entity in index[entity_type]:
       if entity['completeness'] < threshold:
           incomplete.append(entity)

   # Sort by completeness (lowest first)
   incomplete.sort(key=lambda x: x['completeness'])
   ```

3. Format output:
   ```
   📉 Incomplete Initiatives (threshold: 70%)

   25% - app-management (Draft)
      Missing: stakeholders, affected_systems, source_document

   45% - reduce-resource (Draft)
      Missing: intended_users, source_document

   65% - auth-refactor (Defined)
      Missing: stakeholders, 1 solution missing pros/cons

   Total: 3 initiatives below 70% completeness
   ```

**Performance**: Instant

**Examples:**
```
/incomplete
/incomplete initiative --threshold=80
/incomplete epic --threshold=90
```

---

## Reference Documentation

### Embedded Entity Format Reference

These formats are used in the body content of initiative markdown files.

#### Actions Format

```markdown
## Actions

- [ ] ACT-001: Finalize QR code payload format specification
  assigned:: [[people/erik-svensson]]
  due:: 2026-01-25
  status:: In Progress
  created_at:: 2026-01-19 11:00

- [x] ACT-002: Get sign-off from Partner Alpha on timeline
  assigned:: [[people/anna-andersson]]
  status:: Done
  created_at:: 2026-01-16 14:00
  completed_at:: 2026-01-20 16:45
```

#### Questions Format

```markdown
## Open Questions

- [x] Q-001: Can we use existing QR code format?
  asked_by:: [[people/anna-andersson]]
  asked_at:: 2026-01-15 14:00
  answered_by:: [[people/erik-svensson]]
  answered_at:: 2026-01-18 11:20
  answer:: Use existing format with extended payload
  status:: Answered

- [ ] Q-002: What's the fallback if Bluetooth is disabled?
  asked_by:: [[people/anna-andersson]]
  asked_at:: 2026-01-20 10:30
  status:: Open
```

#### Solutions Format

```markdown
## Solutions

### qr-code-approach: QR Code Based
status:: Accepted
proposed_by:: [[people/erik-svensson]]
proposed_at:: 2026-01-16 10:00
decided_at:: 2026-01-18 15:30

Use QR codes on customer packaging that link directly to pre-configured setup flows.

**Pros:**
- Familiar pattern for users
- Low implementation cost

**Cons:**
- Requires packaging changes
- QR codes can be damaged

### bluetooth-discovery: Bluetooth Auto-Discovery
status:: Rejected
proposed_by:: [[people/anna-andersson]]
proposed_at:: 2026-01-16 10:00
decided_at:: 2026-01-18 15:30

Automatic discovery via Bluetooth Low Energy.

**Pros:**
- No physical artifacts needed

**Cons:**
- Battery drain concerns
- Platform permission complexity
```

---

## Helper Functions

Utility functions for formatting and data processing.

### Format Completeness Bar

```python
def format_bar(percentage):
    filled = int(percentage / 10)
    empty = 10 - filled
    return '█' * filled + '░' * empty
```

### Escape JSON for Bash

When passing JSON to bash commands, escape quotes properly:
- Single quotes around JSON
- Escape single quotes in content as '\''

---

## Additional Resources

### Reference Documentation

- [Schema Definitions](references/schema-definitions.md) - All entity fields and requirement levels
- [Status Transitions](references/status-transitions.md) - Workflow rules and required fields
- [Command Reference](references/command-reference.md) - Detailed command documentation

### Templates

Templates for new entities are in `assets/templates/`.
