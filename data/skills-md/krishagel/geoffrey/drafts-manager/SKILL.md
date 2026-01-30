---
name: drafts-manager
description: Triage Drafts inbox and route notes to OmniFocus tasks or Obsidian documents
triggers:
  - "triage drafts"
  - "process drafts"
  - "check drafts"
  - "what's in drafts"
  - "drafts inbox"
  - "clean up drafts"
  - "export drafts"
allowed-tools: Read, Bash, Write
version: 0.1.0
---

# Drafts Manager Skill

Triage the Drafts inbox using a hybrid AI + human confirmation workflow. Routes content to OmniFocus (tasks) or Obsidian (notes) based on content analysis.

## When to Activate

Use this skill when user wants to:
- Triage or process their Drafts inbox
- Route notes to OmniFocus or Obsidian
- Check what's captured in Drafts
- Clean up old drafts

## Architecture

**Two-Phase Hybrid Triage:**

1. **Export & Analyze** - Drafts exports inbox → Geoffrey analyzes → presents suggestions
2. **Confirm & Process** - User confirms routing → Drafts processes each draft → archives

```
┌─────────┐  URL   ┌─────────┐  JSON   ┌─────────┐  Table  ┌──────┐
│Geoffrey │ ────► │ Drafts  │ ─────► │Geoffrey │ ──────► │ User │
│ trigger │       │ export  │        │ analyze │        │review│
└─────────┘       └─────────┘        └─────────┘        └──┬───┘
                                                           │
                                                     Confirmed
                                                           │
┌─────────┐  URL   ┌─────────┐  Routes  ┌──────────┐   ┌───▼────┐
│Geoffrey │ ────► │ Drafts  │ ───────► │OmniFocus │   │Process │
│ trigger │       │ process │         │ Obsidian │   │  list  │
└─────────┘       └────┬────┘         └──────────┘   └────────┘
                       │
                   Archives
```

## Available Scripts

Scripts are in `./scripts/` directory. Run via:
```bash
bun ./scripts/script-name.js
```

### trigger_export.js

Triggers the Drafts "Geoffrey Export Inbox" action via URL scheme.

**Output:** Path to exported JSON file

**Use when:** Starting triage

### trigger_process.js

Triggers the Drafts "Geoffrey Process Draft" action with routing instructions.

**Parameters:** uuid, destination, project, tags, folder

**Use when:** Processing confirmed drafts

## Required Drafts Actions

**IMPORTANT:** User must install these Drafts actions (found in `./actions/`):

### Geoffrey Export Inbox

Exports all inbox drafts to a JSON file for Geoffrey to analyze.

**Location:** `~/Library/Mobile Documents/iCloud~com~agiletortoise~Drafts5/Documents/geoffrey-export.json`

**Output format:**
```json
{
  "exported": "2025-11-23T10:30:00Z",
  "count": 5,
  "drafts": [
    {
      "uuid": "ABC123",
      "title": "First line of draft",
      "content": "Full content...",
      "tags": ["inbox"],
      "createdAt": "2025-11-22T14:00:00Z",
      "modifiedAt": "2025-11-22T14:00:00Z",
      "isFlagged": false
    }
  ]
}
```

### Geoffrey Process Draft

Processes a single draft based on routing instructions from URL parameters.

**URL Parameters:**
- `uuid` - Draft to process
- `destination` - "omnifocus", "obsidian", "archive", or "trash"
- `project` - OmniFocus project (if destination=omnifocus)
- `tags` - Comma-separated tags (if destination=omnifocus)
- `dueDate` - Due date (if destination=omnifocus)
- `folder` - Obsidian folder (if destination=obsidian)

## Content Analysis Rules

When analyzing drafts, look for these signals:

### Route to OmniFocus (Task)

**Signals:**
- Starts with action verb: "call", "email", "buy", "schedule", "review", "check"
- Contains: "todo", "task", "@due", "@defer"
- Short (< 50 words)
- Contains person names
- Shopping lists or errands

**Apply omnifocus-manager routing rules for project/tag assignment**

### Route to Obsidian (Note)

**Signals:**
- Longer content (> 100 words)
- Meeting notes: "meeting with", "discussed", "attendees"
- Ideas/brainstorms: "idea:", "thought:", "what if"
- Reference material: links, quotes, research
- Journal entries: "today I", feelings, reflections

### Archive in Drafts

**Signals:**
- Reference that may be needed again
- Snippets of code or text
- Temporary notes that are now done

### Delete (Trash)

**Signals:**
- Empty or nearly empty
- Test/scratch content
- Duplicates
- Outdated info no longer needed

## Obsidian Routing Rules

| Content Type | Folder | Frontmatter |
|--------------|--------|-------------|
| Meeting notes | `Meetings/` | date, attendees, topics |
| Ideas/brainstorms | `Geoffrey/Inbox/` | tags, created |
| Research | `Reference/` | source, tags, related |
| Journal | `Journal/` | date |
| General notes | `Geoffrey/Inbox/` | tags, created |

**Frontmatter template:**
```yaml
---
created: {{date}}
source: drafts
tags: [from-drafts]
related: []
---
```

## Main Workflow: Triage Drafts

### Phase 1: Export & Analyze

1. **Trigger export:**
   ```bash
   open "drafts://x-callback-url/runAction?action=Geoffrey%20Export%20Inbox"
   ```

2. **Wait for export file** (2-3 seconds)

3. **Read exported JSON:**
   ```bash
   cat ~/Library/Mobile\ Documents/iCloud~com~agiletortoise~Drafts5/Documents/geoffrey-export.json
   ```

4. **Analyze each draft** using content signals above

5. **Present suggestions table:**
   ```markdown
   ## Drafts Inbox Triage

   Found **5 drafts** to process:

   | # | Title | Suggestion | Destination | Details |
   |---|-------|------------|-------------|---------|
   | 1 | Call John about... | Task | OmniFocus | Project: Meetings, Tags: John, Follow Up |
   | 2 | Meeting notes 11/22 | Note | Obsidian | Folder: Meetings/ |
   | 3 | [empty] | Delete | Trash | Empty draft |
   | 4 | Shopping list | Task | OmniFocus | Project: Single Actions, Tags: Chores |
   | 5 | Idea for app... | Note | Obsidian | Folder: Geoffrey/Inbox/ |

   **Questions:**
   - #4: Should this go to a specific store location tag?

   Which numbers need changes? (Or type "process all" to confirm)
   ```

### Phase 2: Process & Archive

1. **For each confirmed draft**, trigger process action:
   ```bash
   # OmniFocus task
   open "drafts://x-callback-url/runAction?action=Geoffrey%20Process%20Draft&uuid=ABC123&destination=omnifocus&project=Meetings&tags=John,Follow%20Up&dueDate=2025-11-30"

   # Obsidian note
   open "drafts://x-callback-url/runAction?action=Geoffrey%20Process%20Draft&uuid=DEF456&destination=obsidian&folder=Meetings"

   # Archive
   open "drafts://x-callback-url/runAction?action=Geoffrey%20Process%20Draft&uuid=GHI789&destination=archive"

   # Delete
   open "drafts://x-callback-url/runAction?action=Geoffrey%20Process%20Draft&uuid=JKL012&destination=trash"
   ```

2. **Report results:**
   ```markdown
   ## Summary
   Processed 5 drafts from inbox

   ## Actions
   - 2 tasks created in OmniFocus
   - 2 notes saved to Obsidian
   - 1 draft deleted

   ## Status
   ✅ Complete

   ## Next Steps
   - Review tasks in OmniFocus inbox
   - Check Obsidian notes in Geoffrey/Inbox/
   ```

## Error Handling

**Drafts not running:**
```
Status: ❌ Failed
Error: Drafts app is not running. Please open Drafts and try again.
```

**Action not installed:**
```
Status: ❌ Failed
Error: Drafts action "Geoffrey Export Inbox" not found.
Please install from: skills/drafts-manager/actions/
```

**Export file not found:**
```
Status: ⚠️ Partial
Error: Export file not created. Drafts may have timed out.
Try running the action manually in Drafts.
```

**OmniFocus not running:**
```
Status: ⚠️ Partial
Warning: OmniFocus not running. Task creation may have failed.
Please verify tasks were created.
```

## Installation

### 1. Install Drafts Actions

Import the action files from `./actions/`:

**Option A: Import from file**
1. Open Drafts
2. Go to Actions → Manage Actions
3. Import from `actions/geoffrey-export-inbox.draftsAction`
4. Import from `actions/geoffrey-process-draft.draftsAction`

**Option B: Create manually**
1. Open Drafts
2. Create new action "Geoffrey Export Inbox"
3. Add Script step with code from `actions/geoffrey-export-inbox.js`
4. Repeat for "Geoffrey Process Draft"

### 2. Verify Installation

Run: `open "drafts://x-callback-url/runAction?action=Geoffrey%20Export%20Inbox"`

Check for export file at:
`~/Library/Mobile Documents/iCloud~com~agiletortoise~Drafts5/Documents/geoffrey-export.json`

## Tips for Best Results

### Tagging in Drafts

Use these tags for manual pre-routing:
- `task` - Force route to OmniFocus
- `note` - Force route to Obsidian
- `archive` - Keep in Drafts archive
- `delete` - Trash without review

### Quick Capture Patterns

When capturing to Drafts, these patterns help AI routing:
- Start tasks with verbs: "Call", "Email", "Buy"
- Start notes with context: "Meeting:", "Idea:", "Note:"
- Use @ for OmniFocus hints: "@due(tomorrow)", "@project(Work)"

### Regular Triage

Best practice: Triage Drafts daily to keep inbox small
- Morning: Process yesterday's captures
- Evening: Quick review of day's notes

## Learned Routing Patterns

These patterns were learned through actual triage sessions with the user.

### Content Type → Destination

| Content Type | Destination | Obsidian Folder | OmniFocus Details |
|--------------|-------------|-----------------|-------------------|
| Meeting notes | Obsidian | `Meetings/2025/` | - |
| Conference notes | Obsidian | `Meetings/2025/` | - |
| Development roadmap | Obsidian | `Work/[Project]/Roadmap.md` | Format as checklist |
| API keys/credentials | **Delete** | - | Security risk |
| Error logs/JSON junk | **Delete** | - | Cruft |
| Random passwords | **Delete** | - | Cruft |
| Contact info | Contacts app | - | Also create follow-up task |
| Book recommendations | OmniFocus | - | Tags: Reading |
| Gift ideas | OmniFocus | - | Tags: Chores, Shopping |
| Action items from meetings | OmniFocus | - | Tags: Follow Up |
| Reference links (AI, UDL) | Obsidian | `Reference/` | - |
| Personal project ideas | OmniFocus | - | Tags: Coding |
| Presentation schedules | Obsidian | `Work/Presentations/` | Future dates → tasks |
| Survey links | OmniFocus | - | Include links in notes |

### Signals for Each Destination

**→ OmniFocus Task:**
- Starts with action verbs: "Submit", "Call", "Email", "Build", "Add"
- Contains due date context: "first week of December", "by end of year"
- Travel approvals, surveys to send, podcasts to record
- Book to read, thing to buy, project to build
- Multiple action items → single task with checklist in notes

**→ Obsidian Note:**
- Meeting notes (look for date, attendees, discussion points)
- Conference notes (look for session titles, speakers, links)
- Development docs with code/commands (wrap in code blocks)
- Reference material with links to external resources
- Topic brainstorms and idea lists

**→ Contacts App:**
- Contains name + phone/email
- Create contact AND follow-up task if there's an action

**→ Delete:**
- Empty or nearly empty
- JSON/error logs
- API keys (security)
- Random strings/passwords
- Test data that's no longer needed

**→ Archive in Drafts:**
- Outdated but potentially useful later
- Reference that may be needed again

### Project/Folder Mappings

**Obsidian Folders:**
- `Meetings/2025/` - All meeting and conference notes
- `Work/AI-Studio/` - AI Studio development docs
- `Work/Jocular-Kangaroo/` - Jocular Kangaroo project
- `Work/Presentations/` - Presentation archives
- `Geoffrey/` - Geoffrey roadmap and ideas
- `Reference/` - Reference materials and links

**OmniFocus Projects (go to Inbox if not found):**
- CoSN Work - CoSN-related tasks
- Meetings - Follow-ups with people
- Research for Future Plans - Books, research tasks

**OmniFocus Tags:**
- Follow Up - Tasks requiring follow-up
- Reading - Books to read
- Chores - Shopping, errands
- Coding - Development tasks
- Geoffrey - AI-assistable tasks
- Email - Tasks requiring email

### Special Handling

**Multi-item notes:**
- If note contains multiple distinct items, either:
  - Create single task with items as checklist in notes
  - Split into separate tasks (ask user preference)

**Development roadmaps:**
- Format as Obsidian file with checkboxes
- Use `- [ ]` for pending items
- Use `- [x]` for completed items
- Include code blocks for commands

**Sensitive data:**
- API keys → Delete immediately
- Student investigation data → Archive carefully, don't expose
- Credentials → Delete or move to secure storage

**Contact + Task pattern:**
- Add to Contacts app via add_contact.js
- Create follow-up task with contact details in notes
- Example: "Send maps to Kim Crowder" with email in notes

## Future Enhancements

- [ ] Batch processing without confirmation for tagged drafts
- [ ] Smart date extraction from draft content
- [ ] Template matching for common note types
- [ ] Sync with omnifocus-manager tag hierarchy
- [ ] Obsidian template application
- [ ] Draft content search/query
- [ ] Auto-detect project roadmaps and format as checklists
- [ ] Recognize CoSN, ACPE, Kiwanis contexts for project routing
