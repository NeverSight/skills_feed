---
name: second-brain
description: |
  Personal knowledge management for Obsidian combining GTD, Zettelkasten, and PARA. Six workflows: (1) Capture - "capture this", "remember this", "save this thought", "note this down" - saves thoughts/tasks to daily inbox without categorization; (2) Process inbox - "process my inbox", "organize captures", "GTD processing" - clarifies items and routes to projects or permanent notes; (3) Daily plan - "plan my day", "what should I work on", "morning planning" - creates prioritized task list based on energy and context; (4) Daily closeout - "daily closeout", "review my day", "evening reflection" - marks progress and drafts tomorrow's plan; (5) Setup - "set up my second brain", "configure vault" - configures vault path and user goals; (6) Excalidraw - "create a diagram", "visualize this", "draw flowchart", "sketch this" - creates .excalidraw.md files with rectangles, ellipses, diamonds, arrows, lines, and text. Proactively offers to capture valuable insights during research conversations.
---

# Second Brain

A personal knowledge management and productivity system for Obsidian, combining:
- **GTD (Getting Things Done)** - Task and project management
- **Zettelkasten** - Atomic note-taking for knowledge building
- **PARA Method** - Folder organization (Projects, Areas, Resources, Archives)

## Configuration (MEMORY-BASED)

**CRITICAL FIRST STEP:** Before any operation, check for configuration in Claude's Memory.

### How Configuration Works

Configuration is stored in **Claude's Memory feature** and persists across all sessions automatically.

**Why Memory?** Skills in Claude Desktop run in a sandboxed environment with no file system access. Memory is the only way to persist configuration across sessions.

Once set up, Claude remembers:
- Your vault path
- Your name
- Whether setup is complete
- Your preferences

### Configuration Check Flow

1. **Check Claude Memory** for "Second Brain vault path"
2. **If found in Memory**: Use the remembered vault path for all operations
3. **If NOT found in Memory**: This is first-time setup - ask user for vault path

### Checking Memory

At the start of ANY Second Brain operation, check if you remember the vault path:

```
Do I have the user's Second Brain vault path in my memory?
- If YES: Use that path for all operations
- If NO: Ask the user and save to memory
```

### If No Configuration Found (First Time)

Ask the user for their vault path:

```
Welcome to Second Brain!

I need to know where your Obsidian vault is located so I can save and organize your notes.

Please provide the full path to your Obsidian vault folder.

Examples:
- macOS: /Users/yourname/Documents/MyVault
- Windows: C:\Users\yourname\Documents\MyVault
- Linux: /home/yourname/Documents/MyVault

What's the path to your vault?
```

Once you have the path:
1. **Save to Claude Memory**: Remember the vault path for future sessions
2. Run the full [setup workflow](workflows/setup.md) to complete onboarding
3. Save setup completion status to Memory

**Claude Memory persists across ALL sessions automatically.**

### What Gets Saved to Memory

After setup, Claude should remember:
- **Second Brain vault path**: The absolute path to the user's Obsidian vault
- **Second Brain user name**: The user's name
- **Second Brain setup complete**: Whether full setup has been done
- **Second Brain preferences**: User preferences (proactive capture, inbox threshold)

### If Configuration Exists in Memory

Use the remembered `vault path` for ALL file operations.

### Claude Code Fallback

**For Claude Code users only:** If Memory is empty, you may also check for a legacy config file at `~/.second-brain/config.json`. If found, migrate that configuration to Memory for future use.

### Environment Variable Override

Environment variable `SECOND_BRAIN_VAULT_PATH` can override Memory (useful for testing).

---

## Core Capabilities

### 1. Quick Capture

**Trigger phrases:** "capture this", "save this thought", "remember this", "note this down", "add to my inbox"

**What it does:** Instantly captures thoughts, tasks, or ideas to today's inbox without categorization.

**GTD Principle:** "Capture first, clarify later."

See: [Capture Workflow](workflows/capture.md)

---

### 2. Daily Planning

**Trigger phrases:** "plan my day", "what should I work on", "daily planning", "morning planning"

**What it does:**
- Checks inbox (prompts to process if 5+ items)
- Scans all projects for next actions
- Asks about energy, context, time available
- Generates prioritized task list (must-do, should-do, quick-wins)

See: [Daily Plan Workflow](workflows/daily-plan.md)

---

### 3. Inbox Processing

**Trigger phrases:** "process my inbox", "organize my captures", "clarify my tasks", "GTD processing"

**What it does:**
- Asks clarifying questions for vague items (batched, not one-by-one)
- Routes actionable items to Projects/Areas
- Routes knowledge items to Permanent Notes
- Reviews all active projects
- Archives completed projects

See: [Process Inbox Workflow](workflows/process-inbox.md)

---

### 4. Daily Closeout

**Trigger phrases:** "daily closeout", "review my day", "end of day review", "evening reflection"

**What it does:**
- Reads today's plan
- Asks what was accomplished
- Marks completed/partial/deferred items
- Asks about tomorrow's priorities
- Creates tomorrow's DRAFT plan

See: [Daily Closeout Workflow](workflows/daily-closeout.md)

---

### 5. Setup & Configuration

**Trigger phrases:** "set up my second brain", "configure my vault", "second brain setup", "reconfigure"

**What it does:**
- First-time: Full interactive setup (goals, relationships, first project)
- Re-run: Update existing configuration

See: [Setup Workflow](workflows/setup.md)

---

### 6. Excalidraw Diagrams

**Trigger phrases:** "create a diagram", "draw a flowchart", "make an excalidraw", "visualize this", "sketch this out", "diagram showing"

**What it does:**
- Creates `.excalidraw.md` files compatible with Obsidian Excalidraw plugin
- Generates flowcharts, concept maps, system diagrams, mind maps
- Supports shapes (rectangles, ellipses, diamonds), arrows, lines, and text
- Full JSON structure with proper element properties

**Output location:** `{{vaultPath}}/` (user specifies location or defaults to appropriate folder)

See: [Excalidraw Reference](references/excalidraw-diagrams.md)

---

## Proactive Capture

**IMPORTANT:** When you notice the user:
- Discovering valuable information during research
- Having insights or realizations
- Discussing ideas worth preserving
- Solving problems in interesting ways

**Offer to capture:**
```
That's an interesting insight about [topic]. Would you like me to capture this to your Second Brain?
```

If they agree:
- Use the capture workflow
- Add context about where the insight came from
- Suggest relevant tags or connections

---

## Vault Structure

The system uses PARA + Zettelkasten organization:

```
{{vaultPath}}/
├── 00-Inbox/
│   ├── Daily/              # Captures go here (YYYY-MM-DD.md)
│   └── Fleeting-Notes/     # Knowledge items during processing
├── 01-Projects/            # Multi-step outcomes with deadlines
├── 02-Areas/               # Ongoing responsibilities
│   ├── Career-Development.md
│   ├── Health-Fitness.md
│   ├── Personal-Development.md
│   ├── Errands.md
│   ├── Personal-Todos.md
│   └── Relationships/      # Individual notes per person
├── 03-Resources/
│   └── Reference-Notes/    # Summaries of external sources
├── 04-Archives/            # Completed/inactive projects
├── Daily Plans/            # Generated daily plans
├── Meeting Notes/          # Meeting documentation
├── Permanent Notes/        # Zettelkasten - synthesized insights
│   └── Assisting-User-Context.md  # User's goals & context
└── Templates/              # Reusable templates
```

See: [PARA + Zettelkasten Guide](references/para-zettelkasten.md)

---

## Unified Task Structure

**ALL Projects, Areas, and Relationship notes use identical priority sections:**

```markdown
## High Priority / Critical
- Urgent/important items (scanned FIRST by daily planning)

## Next Actions / Current Tasks
- Regular priority items (scanned SECOND)

## Someday/Maybe
- Lower priority/exploratory (SKIPPED by daily planning)

## Waiting On
- Blocked by external dependencies

## Completed
- Finished tasks with dates
```

---

## Templates

Use these templates when creating new notes:

| Template | Use When |
|----------|----------|
| [project.md](templates/project.md) | Creating a new project (multi-step outcome) |
| [area.md](templates/area.md) | Creating a new area of responsibility |
| [permanent-note.md](templates/permanent-note.md) | Creating a Zettelkasten permanent note |
| [fleeting-note.md](templates/fleeting-note.md) | Quick knowledge capture for later processing |
| [relationship.md](templates/relationship.md) | Tracking an important person |
| [meeting-note.md](templates/meeting-note.md) | Meeting documentation |
| [daily-plan.md](templates/daily-plan.md) | Daily execution plan |
| [daily-inbox.md](templates/daily-inbox.md) | Daily capture file |
| [user-context.md](templates/user-context.md) | User goals and preferences |
| [excalidraw-diagram.md](templates/excalidraw-diagram.md) | Visual diagrams and flowcharts |

---

## Key References

- [GTD Methodology](references/gtd-methodology.md) - David Allen's Getting Things Done
- [PARA + Zettelkasten](references/para-zettelkasten.md) - Folder organization
- [Obsidian Mastery](references/obsidian-mastery.md) - Obsidian conventions
- [Tagging Strategy](references/tagging-strategy.md) - Tag taxonomy
- [Excalidraw Diagrams](references/excalidraw-diagrams.md) - Visual diagrams and flowcharts

---

## ADHD-Friendly Principles

The system is designed for users who may have ADHD:

1. **Read entire documents first** - Understand existing structure
2. **Make targeted edits** - Update specific sections, don't append
3. **Never just add to bottom** - Unless explicitly asked
4. **Keep it concise** - Remove redundancy
5. **One plan, not many** - Replace old plans, don't add "revised" sections

**Bad:** Adding "REVISED PLAN" below "TODAY'S PLAN"
**Good:** Replacing "TODAY'S PLAN" content with updated tasks

---

## Daily Workflow Summary

**The Complete Loop:**

1. **Throughout day:** Capture thoughts (30 sec each)
2. **3x per week:** Process inbox - Clarify + Organize (15 min)
3. **Every morning:** Daily plan - Choose what to work on (5 min)
4. **Every evening:** Daily closeout - Reflect + Prep tomorrow (5 min)

**Total time:** ~20-25 min/day + 45 min/week processing = Sustainable!

---

## Examples

### Example 1: Quick Capture

**User:** "Capture: Need to call the dentist and also research new project management tools"

**You:**
1. Read config to get vault path
2. Find/create today's inbox file at `{{vaultPath}}/00-Inbox/Daily/YYYY-MM-DD.md`
3. Append the capture with timestamp
4. Confirm: "Captured at 14:32. You have 3 captures today."

### Example 2: Daily Planning

**User:** "What should I work on today?"

**You:**
1. Check inbox count (process if 5+ items)
2. Scan all projects in `01-Projects/` for next actions
3. Ask: "How's your energy today? Any context constraints?"
4. Generate prioritized list based on goals from user context
5. Create/update `Daily Plans/YYYY-MM-DD.md`

### Example 3: Proactive Capture

**During conversation about a topic:**

**You:** "That insight about [topic] seems valuable. Would you like me to capture it to your Second Brain? I can add it to your inbox for later processing, or create a permanent note if it's already well-formed."

---

## Tool Usage

**Always use the vault path from Claude Memory for all operations.**

### Claude Desktop (with Filesystem Extension)

Claude Desktop requires the **Filesystem Desktop Extension** to read/write files. Once installed, these tools are available:

| Skill Operation | Filesystem Extension Tool |
|-----------------|---------------------------|
| Read files | `read_file` |
| Write new files | `write_file` |
| Edit existing files | `edit_file` |
| Find files by pattern | `list_directory` + `search_files` |
| Create directories | `create_directory` |

**Prerequisites for Claude Desktop:**
1. Install the **Filesystem** extension from the built-in extension store
2. Grant access to your Obsidian vault folder when prompted
3. Claude will then be able to read/write files in your vault

### Claude Code

Claude Code has built-in file system access. These tools are available:
- **Read** - Check files, load context
- **Write** - Create new files
- **Edit** - Update existing files
- **Glob** - Find files by pattern
- **Bash** - Create directories, run commands

### Capability Comparison

| Capability | Claude Desktop | Claude Code |
|------------|----------------|-------------|
| File operations in vault | ✅ Yes (with extension) | ✅ Yes (built-in) |
| Claude Memory | ✅ Yes | ✅ Yes |
| Config file fallback | ❌ No | ✅ Yes |
| Bash commands | ❌ No | ✅ Yes |

**Important:** The skill is designed to work in BOTH environments:
- **Configuration** is stored in Claude Memory (works everywhere)
- **File operations** use the filesystem extension (Desktop) or built-in tools (Code)

---

## Version History

**Version 4.1** (2025-12-11)
- Switched to Claude Memory for configuration persistence
- Added Claude Desktop compatibility (sandboxed skills)
- Legacy config file fallback for Claude Code

**Version 4.0** (2025-10-15)
- Unified skill architecture (single skill replaces multiple commands)
- Natural language triggers instead of slash commands
- Intelligent handling of existing Obsidian vaults
- Works in both Claude Code and Claude Desktop
