---
name: omnifocus-manager
description: Manage OmniFocus tasks, projects, and inbox with proper tagging and organization
triggers:
  - "add task"
  - "create task"
  - "new task"
  - "follow up with"
  - "triage omnifocus"
  - "triage my omnifocus"
  - "omnifocus inbox"
  - "clean up omnifocus"
  - "check omnifocus"
  - "show tasks"
  - "what's due"
  - "omnifocus review"
allowed-tools: Read, Bash
version: 0.1.0
---

# OmniFocus Manager Skill

Manage OmniFocus tasks with proper project assignment, tagging, and organization based on user preferences.

## When to Activate

Use this skill when user wants to:
- Add/create tasks
- Follow up with someone
- Triage or review inbox
- Clean up or organize tasks
- Check what's due or available
- Query task status

## User Preferences

**Task Creation Philosophy:**
- Always assign to a project (never leave in Inbox)
- Always set expected completion date
- Tag with person + "Follow Up" for 1:1 discussions
- Use location tags for shopping tasks

## Working with OmniFocus Scripting

### JXA vs AppleScript: When to Use Each

**Use JXA (JavaScript for Automation) for:**
- ✅ Reading data (tasks, projects, tags, inbox)
- ✅ Creating/updating individual tasks
- ✅ Adding tags to tasks
- ✅ Moving tasks between projects
- ✅ Fast, single-purpose operations

**Use AppleScript for:**
- ✅ Creating projects inside folders
- ✅ Creating folders
- ✅ Bulk operations on multiple projects
- ✅ Complex nested structures (folder → project → tasks)

**CRITICAL DIFFERENCE:**
- **External JXA scripts** (via `osascript -l JavaScript`) have limitations
- **OmniJS** (built-in JavaScript in OmniFocus app) has more capabilities
- Documentation examples showing `new Project(name, folder)` work in OmniJS but **NOT in external JXA scripts**

### Common Pitfalls & Solutions

| Pitfall | Why It Happens | Solution |
|---------|---------------|----------|
| Projects created at root instead of in folder | JXA `parentFolder` property doesn't work externally | Use AppleScript with `tell folder` blocks |
| Duplicate empty folders | Script creates folder but projects fail to nest | Always verify `count of projects of folder` after creation |
| "Can't convert types" errors | JXA type mismatch between app objects and JavaScript | Use AppleScript for complex operations |
| Projects appear created but aren't | Script reports success but verification shows 0 projects | Always verify after creation, never trust script output alone |
| Can't delete folders via script | Folders don't support deletion commands | Manual cleanup in OmniFocus UI required |

### Verification Patterns

**ALWAYS verify operations that modify structure:**

```applescript
# After creating projects in folder
tell application "OmniFocus"
  tell default document
    set projectCount to count of projects of folder "Folder Name"
    if projectCount is 0 then
      return "ERROR: Projects not in folder!"
    else
      return "SUCCESS: " & projectCount & " projects created"
    end if
  end tell
end tell
```

**NEVER assume success based on:**
- Script completing without errors
- Return value claiming success
- Absence of error messages

**ALWAYS verify by:**
- Counting items created
- Checking container relationships
- Querying actual data structure

### Error Recovery Workflow

**If you create projects incorrectly:**

1. **STOP** - Don't create more until you understand the problem
2. **VERIFY** - Check actual state: `projects of folder "X"`
3. **CLEAN UP** - Drop wrong projects: `mark dropped proj`
4. **NOTE** - Empty folders must be manually deleted in UI
5. **FIX** - Use correct method (AppleScript for folders)
6. **VERIFY AGAIN** - Confirm correction worked

## Available Scripts

Scripts are in `./scripts/` directory.

**For JXA scripts:**
```bash
osascript -l JavaScript ./scripts/script-name.js
```

**For AppleScript:**
```bash
osascript ./scripts/script-name.applescript
```

**IMPORTANT:** Always use pure JXA/AppleScript, NOT Omni Automation URL scheme. The URL scheme triggers security popups for every unique script. Direct scripting runs silently.

### Key JXA Patterns (for individual tasks)

- `doc.inboxTasks.push(task)` - create new tasks
- `app.add(tag, {to: task.tags})` - add existing tags (not push!)
- `task.assignedContainer = project` - move to project

### get_inbox.js
Returns remaining inbox tasks (matches OmniFocus Inbox perspective).

**Filter logic:** Tasks with no project + not completed + not dropped + not deferred to future

**Output:** JSON with count and task array (id, name, note, tags, dueDate)

**Use when:** Starting inbox triage

### get_tags.js
Returns full tag hierarchy with groupings.

**Output:** JSON with all 129 tags organized by parent/children

**Use when:** Need to find correct tags for a task

### get_projects.js
Returns full project/folder structure.

**Output:** JSON with projects and folder paths

**Use when:** Need to find correct project for a task

### add_task.js
Creates a new task with proper tags and project.

**Parameters:** name, project, tags[], dueDate, deferDate, note, flagged

**Use when:** Creating new tasks

### update_task.js
Updates any existing task (not just inbox).

**Parameters:** name or id, project, tags[], dueDate, deferDate

**Use when:** Triaging/moving tasks, adding tags

### create_tag.js
Creates a new tag, optionally under a parent.

**Parameters:** name, parent (optional)

**Use when:** Tag doesn't exist for a person or category

### create_projects_in_folder.applescript
**CRITICAL:** Creates projects INSIDE folders (not at root level).

**WHY APPLESCRIPT, NOT JXA:**
External JXA scripts (osascript -l JavaScript) **cannot reliably create projects in folders**. Projects appear created but end up at root level, not in the folder. This creates duplicate folders and organizational mess.

**CORRECT PATTERN (AppleScript):**
```applescript
tell application "OmniFocus"
  tell default document
    set myFolder to make new folder with properties {name:"Folder Name"}
    tell myFolder
      set proj to make new project with properties {name:"Project Name", note:"Description"}
      tell proj
        make new task with properties {name:"Task Name"}
      end tell
    end tell
  end tell
end tell
```

**WRONG PATTERNS (DO NOT USE):**
- ❌ JXA: `new Project(name, folderNamed('X'))` - only works in OmniJS, not external scripts
- ❌ JXA: `project.folder = folder` - sets property but doesn't move
- ❌ JXA: `project.parentFolder = folder` - projects still at root level
- ❌ JXA: `folder.projects.push(project)` - fails silently

**DELETION NOTES:**
- Projects: Use AppleScript `mark dropped proj` command
- Folders: **Cannot be deleted via script** - must delete manually in OmniFocus UI
- Always verify folder contents before assuming success

**Use when:** Creating multiple projects organized in folders (annual planning, strategic priorities, etc.)

## Interface for Other Skills

If another skill needs to create OmniFocus projects/tasks, use these patterns:

### Creating Individual Tasks

**Call directly from other skill:**
```bash
osascript -l JavaScript /path/to/omnifocus-manager/scripts/add_task.js '{
  "name": "Task name",
  "project": "Project Name",
  "tags": ["Tag1", "Tag2"],
  "dueDate": "2026-01-15",
  "note": "Optional note"
}'
```

### Creating Folder with Multiple Projects

**Build AppleScript dynamically:**

1. **Generate AppleScript string** with folder + projects + tasks structure
2. **Write to temp file:** `/tmp/create_projects_TIMESTAMP.applescript`
3. **Execute:** `osascript /tmp/create_projects_TIMESTAMP.applescript`
4. **Verify:** Check `count of projects of folder "Folder Name"` returns expected count
5. **Clean up:** Remove temp file

**Example structure:**
```applescript
tell application "OmniFocus"
  tell default document
    set targetFolder to make new folder with properties {name:"FOLDER_NAME"}
    tell targetFolder
      # Repeat for each project:
      set proj to make new project with properties {name:"PROJECT_NAME", note:"NOTE"}
      tell proj
        # Repeat for each task:
        make new task with properties {name:"TASK_NAME"}
      end tell
    end tell
  end tell
end tell
```

**CRITICAL:** Always verify after creation. Don't trust return values.

## Best Practices for Folder/Project Creation

### Pre-Creation Checklist

**BEFORE creating projects in folders:**

1. **Check for existing folders:**
   ```applescript
   tell application "OmniFocus"
     tell default document
       set folderNames to name of every folder
       return folderNames
     end tell
   end tell
   ```

2. **Verify folder doesn't already exist** to avoid duplicates

3. **Plan the complete structure** - folder name, all project names, all tasks

### During Creation

**CRITICAL RULES:**

1. **Use AppleScript, NOT JXA** for external scripts creating projects in folders
2. **Create folder FIRST** using `make new folder`
3. **Use `tell folder` block** for all project creation
4. **Nest `tell project` blocks** for task creation

### Post-Creation Verification

**ALWAYS verify projects are in folder:**

```applescript
tell application "OmniFocus"
  tell default document
    set folderProjects to projects of folder "Folder Name"
    return "Found " & (count of folderProjects) & " projects"
  end tell
end tell
```

**If count is 0:**
- Projects created at root level (wrong!)
- Need to delete and recreate using correct AppleScript pattern

### Cleanup After Errors

**If you create projects incorrectly:**

1. **Drop projects:** `mark dropped proj` for each wrong project
2. **Empty folders cannot be deleted via script** - must delete manually in OmniFocus UI
3. **Always verify** after cleanup before recreating

### Complete Example: Creating Folder with Projects

```bash
# Build AppleScript dynamically
cat > /tmp/create_folder_projects.applescript << 'EOF'
tell application "OmniFocus"
  tell default document
    set myFolder to make new folder with properties {name:"Project Folder"}
    tell myFolder
      set proj1 to make new project with properties {name:"Project 1", note:"Description"}
      tell proj1
        make new task with properties {name:"Task 1"}
        make new task with properties {name:"Task 2"}
      end tell
    end tell
  end tell
end tell
EOF

# Execute
osascript /tmp/create_folder_projects.applescript

# Verify
osascript << 'VERIFY'
tell application "OmniFocus"
  tell default document
    set projectCount to count of projects of folder "Project Folder"
    return "Created " & projectCount & " projects in folder"
  end tell
end tell
VERIFY
```

## Tag Hierarchy Reference

**Top-level categories:**
- **Activity** - What type of work (Creative, Coding, Writing, Reading, Research, etc.)
- **Energy** - Required mental state (Full Focus, Short Dashes, Brain Dead, Low, High)
- **Location** - Where to do it (Home, Grocery Stores, PSD Sites, Other Shopping)
- **People** - Who's involved (Personal family, PSD staff by department)
- **Groups** - Team meetings (Cabinet, Engineering Team, DLI Admin, etc.)
- **Time** - When to do it (Morning, Afternoon, Evening)
- **Communications** - How to communicate (Email, Phone, In Person, etc.)
- **Online** - Online tools (Freshservice, Github, Google Docs)
- **Standalone** - Follow Up, Waiting For, Waiting, Kiwanis

**People → PSD breakdown:**
- Tech: Mel, Bill, Reese, Mark, Brad, Mason, Jordan, etc.
- DCRC: Jodi, Terri, Laura
- Comms: Danielle, Jake, Shana
- ESC: Ashley, John Y, Patrick, Krestin, James, Wendy, Janna, etc.
- SSOs: Moose, Brent

**Special tags:**
- Geoffrey - tasks that AI can assist with
- Full Focus - requires dedicated focus time

## Task Routing Rules

### By Task Type → Project

| Task Type | Project | Default Due |
|-----------|---------|-------------|
| Discussions with people | Meetings | 7 days |
| Phone calls | Meetings | 7 days |
| CoSN-related | CoSN Work | 7 days |
| Digital Promise work | Digital Promise | 7 days |
| AI/automation projects | AI Studio | 7 days |
| Coding/development | Coding Projects | 7 days |
| Research/learning | Research for Future Plans | 7 days |
| SOP/process development | Standard Operating Procedures | 14 days |
| Form/procedure updates | Department Procedures | 7 days |
| District reimbursements | Purchasing & Acquisitions | 7 days |
| Travel approvals | (appropriate project) | 14 days |
| Data governance | Data Governance | 14 days |
| Tech support issues | → Freshservice ticket | N/A |

### By Task Type → Tags

| Task Type | Tags |
|-----------|------|
| Discussion with person | [Person name], Follow Up |
| Phone call | Phone, Follow Up |
| Research tasks | Research |
| AI-assistable tasks | Geoffrey |
| Focus time needed | Full Focus |
| Admin/organizational | Organization |
| Safety/security related | (relevant ESC person) |

### Routing Signals

**Goes to Meetings project:**
- "talk to [person]"
- "discuss with"
- "follow up with"
- "check with"
- "call [person/org]"
- "get [thing] to [person]"

**Goes to Research for Future Plans:**
- "look at/into"
- "what about"
- CISA resources
- Training to consider
- External resources to review

**Goes to Coding Projects or AI Studio:**
- AI/automation ideas
- "build a program"
- Geoffrey capabilities
- Technical tools to explore

**Needs Freshservice (skip for now):**
- User-reported issues
- Equipment requests
- "doesn't work/load"
- Form rebuild requests

## Common Workflows

### Add a Task

1. Parse user request for: task name, person (if any), context clues

2. Apply routing rules above to determine:
   - **Project** - based on task type
   - **Tags** - person + communication method + activity type
   - **Due date** - based on task type timing

3. If tag doesn't exist, create it with `create_tag.js`

4. Run `add_task.js` with parameters

5. Return standardized output

**Example:**
```
User: "Follow up with Mel about the drone program"

Actions:
- Task: "Follow up with Mel about the drone program"
- Project: PSD > General Technology > Digital Innovation Leads
- Tags: Mel, Follow Up
- Due: Next 1:1 date or 7 days
```

### Triage Inbox

1. **Get inbox tasks:**
   ```bash
   osascript -l JavaScript ./scripts/get_inbox.js
   ```
   This returns only remaining tasks (no project, not completed, not dropped, not deferred)

2. **Present assumptions in batches (10-15 tasks):**
   - Read task notes for context clues
   - Apply routing rules to suggest project, tags, due date
   - Flag unclear tasks that need user input

3. **Ask clarifying questions:**
   - Who is [person/acronym]?
   - Which project for [ambiguous task]?
   - Should this be skipped (needs email context)?

4. **Batch update confirmed tasks:**
   ```bash
   osascript -l JavaScript ./scripts/update_task.js '{"name":"...", "project":"...", "tags":[...], "dueDate":"..."}'
   ```

5. **Create missing tags/projects as needed:**
   ```bash
   osascript -l JavaScript ./scripts/create_tag.js '{"name":"PersonName", "parent":"ESC"}'
   ```

6. **Skip tasks that need:**
   - Email context (user needs to read first)
   - Freshservice ticket creation
   - More information to route properly

**Triage output format:**
```markdown
## My assumptions on remaining tasks:

| # | Task | Project | Tags | Notes |
|---|------|---------|------|-------|
| 1 | task name | Meetings | Person, Follow Up | context |

**Questions:**
- #X: Who is [person]?
- #Y: Which project for this?

Which numbers need correction?
```

### Clean Up Tasks

1. Find tasks that are:
   - Overdue
   - Stale (no activity)
   - Missing tags
   - In wrong project
2. Suggest actions:
   - Complete
   - Defer
   - Delete
   - Re-tag
   - Move

## Error Handling

**If OmniFocus not running:**
```
Status: ❌ Failed
Error: OmniFocus is not running. Please open OmniFocus and try again.
```

**If tag not found:**
- Check for similar tags (fuzzy match)
- Suggest creating new tag
- Ask user to clarify

**If project not found:**
- List available projects in that domain
- Suggest closest match
- Ask user to specify

## Output Format

Always use standardized format:

```markdown
## Summary
Created task with proper tags and project assignment

## Actions
- Created task: "[task name]"
- Project: [full project path]
- Tags: [tag1, tag2, tag3]
- Due: [date]
- Notes: [if any]

## Status
✅ Complete

## Next Steps
- Task appears in [relevant perspective]
- Follow up scheduled for [date if applicable]
```

## Future Enhancements

- [ ] Batch task creation
- [ ] Smart project suggestion based on content
- [ ] Calendar integration for due dates
- [ ] Recurring task patterns
- [ ] Perspective queries
- [ ] Task completion tracking
