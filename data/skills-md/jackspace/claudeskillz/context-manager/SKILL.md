---
name: context-manager
description: Manages permanent memory storage for decisions, blockers, context, preferences, and procedures. Use when user says "remember", "save this decision", "what did we decide", "recall", "search memories", "any blockers", or when making important architectural decisions. Provides SDAM compensation through external memory.
---

# Context Manager

## Purpose

Permanent external memory system that compensates for SDAM (no episodic memory). Saves and recalls:
- **DECISION**: Architectural choices, tech stack selections, design decisions
- **BLOCKER**: Active obstacles preventing progress
- **CONTEXT**: Project background, requirements, constraints
- **PREFERENCE**: User preferences, coding style, patterns
- **PROCEDURE**: How-to guides, workflows, processes
- **NOTE**: General information, observations, reminders

**For SDAM users**: Complete external memory - never forget decisions or context.
**For ADHD users**: Eliminates decision fatigue - past choices automatically recalled.
**For dyschronometria**: All memories time-anchored with explicit timestamps.

## Activation Triggers

- User says: "remember", "save this", "don't forget"
- User asks: "what did we decide", "recall", "search for"
- User mentions: "decision", "blocker", "preference"
- Making important architectural decision (proactive save)
- Encountering obstacle (proactive blocker tracking)

## Core Workflow

### 1. Save Memory

When user says "remember [something]":

**Step 1**: Classify memory type
```
DECISION: "remember we're using PostgreSQL"
BLOCKER: "remember I can't access the API yet"
CONTEXT: "remember this is for BOOSTBOX project"
PREFERENCE: "remember I prefer functional components"
PROCEDURE: "remember how to deploy: npm run build then rsync"
NOTE: "remember to update docs after this feature"
```

**Step 2**: Extract metadata
- Content: The actual memory
- Tags: Auto-generate from keywords (e.g., "PostgreSQL" → ["database", "postgresql", "backend"])
- Project: Infer from current directory or explicit mention
- Timestamp: ISO 8601 format

**Step 3**: Read current index
```bash
# Cross-platform: Use $HOME (Linux/macOS) or %USERPROFILE% (Windows)
cat ~/.claude-memories/index.json
# Windows PowerShell alternative:
# Get-Content "$env:USERPROFILE\.claude-memories\index.json"
```

**Step 4**: Add to index
```json
{
  "version": "1.0.0",
  "created": "2025-10-17T17:45:00Z",
  "last_updated": "{current_timestamp}",
  "total_memories": N + 1,
  "memories_by_type": {
    "DECISION": X + 1,
    ...
  },
  "memories": [
    {
      "id": "{uuid}",
      "type": "DECISION",
      "content": "Using PostgreSQL as primary database",
      "timestamp": "{current_timestamp}",
      "tags": ["database", "postgresql", "backend"],
      "project": "boostbox",
      "context": {
        "file": "{current_file_if_relevant}",
        "conversation_id": "{if_available}"
      }
    },
    ...existing memories
  ],
  "tags_index": {
    "database": ["{uuid1}", "{uuid2}"],
    "postgresql": ["{uuid}"]
  },
  "project_index": {
    "boostbox": ["{uuid1}", "{uuid2}"],
    "toolhub": ["{uuid3}"]
  }
}
```

**Step 5**: Create detailed memory file
```bash
# Save to category-specific directory
# Linux/macOS: ~/.claude-memories/decisions/{uuid}.md
# Windows: %USERPROFILE%\.claude-memories\decisions\{uuid}.md
~/.claude-memories/decisions/{uuid}.md
```

```markdown
# DECISION: Using PostgreSQL

**Date**: 2025-10-17T17:45:00Z (2 hours ago)
**Project**: BOOSTBOX
**Tags**: database, postgresql, backend

## Decision

Using PostgreSQL as primary database instead of MongoDB.

## Rationale

{if provided by user or inferred from conversation}

## Context

{surrounding conversation context}

## Related Memories

{if any related memories found by tag/project match}

## Last Updated

2025-10-17T17:45:00Z
```

**Step 6**: Confirm to user
```
✅ Remembered: Using PostgreSQL as primary database
📁 Saved to: decisions/{uuid}.md
🏷️ Tags: database, postgresql, backend
📊 Total memories: {N+1}
```

### 2. Recall Memory

When user asks "what did we decide about [topic]":

**Step 1**: Parse query
- Extract keywords: "decide" → search DECISION type
- Extract topic: "database" → search tags/content

**Step 2**: Search index
```javascript
// Priority order:
1. Exact tag match in requested project
2. Exact tag match in any project
3. Partial content match in requested project
4. Partial content match in any project

// Sort by:
1. Relevance (exact match > partial)
2. Recency (newer > older)
3. Type priority (BLOCKER > DECISION > others)
```

**Step 3**: Load detailed memory files
```bash
# For each matching UUID
cat ~/.claude-memories/decisions/{uuid}.md
# Windows PowerShell:
# Get-Content "$env:USERPROFILE\.claude-memories\decisions\{uuid}.md"
```

**Step 4**: Present results
```
🔍 Found 3 memories about "database":

1. DECISION: Using PostgreSQL (2 days ago)
   📁 Project: BOOSTBOX
   💡 Using PostgreSQL as primary database instead of MongoDB
   🔗 decisions/abc-123.md

2. DECISION: Database schema design (5 days ago)
   📁 Project: BOOSTBOX
   💡 User table with UUID primary keys
   🔗 decisions/def-456.md

3. PREFERENCE: Prefer migrations over raw SQL (1 week ago)
   📁 All projects
   💡 Always use migration files, never direct SQL schema changes
   🔗 preferences/ghi-789.md

Would you like details on any of these?
```

### 3. Track Blockers

**Auto-detect blockers**:
- User says: "I can't", "it won't work", "stuck on"
- Error messages that can't be immediately fixed
- Missing credentials/access
- External dependencies not ready

**Proactive save**:
```
🚧 Detected blocker: API credentials not available

Saving as BLOCKER for tracking.

When this is resolved, say "blocker resolved: [brief description]"
```

**Blocker resolution**:
```
User: "blocker resolved: got API credentials"

✅ Blocker resolved: API credentials not available
📝 Updated memory with resolution timestamp
⏱️ Blocked for: 2 days 4 hours
```

### 4. Search Memories

Support rich queries:
- "search memories for auth" → Full-text search
- "show all blockers" → Filter by type
- "what did we decide this week" → Time-filtered DECISION
- "boostbox decisions" → Project + type filter
- "show preferences" → Type filter

**Search syntax**:
```
Basic: "search [topic]"
Type filter: "search decisions about [topic]"
Project filter: "search boostbox [topic]"
Time filter: "search [topic] this week|month|today"
Combined: "search boostbox decisions about database this week"
```

## Memory Types Deep Dive

### DECISION

**When to save**:
- Tech stack choices ("using React", "chose PostgreSQL")
- Architecture decisions ("microservices vs monolith")
- Design patterns ("using repository pattern")
- Library selections ("using Tailwind CSS")

**Structure**:
```markdown
# DECISION: {title}

## What we decided
{the decision}

## Why
{rationale - infer from conversation}

## Alternatives considered
{if discussed}

## Impact
{affected areas}
```

### BLOCKER

**When to save**:
- Can't access resource (API, database, server)
- Missing dependencies (libraries, services)
- External blockers (waiting on someone)
- Technical issues (bug preventing progress)

**Structure**:
```markdown
# BLOCKER: {title}

## Issue
{what's blocking}

## Impact
{what can't be done}

## Workarounds tried
{if any}

## Status
Active | Resolved | Bypassed

## Resolution (when resolved)
{how it was fixed}
{timestamp of resolution}
```

### CONTEXT

**When to save**:
- Project background ("this is for BOOSTBOX")
- Requirements ("must support offline mode")
- Constraints ("can't use paid services")
- Business rules ("users can't delete posts")

### PREFERENCE

**When to save**:
- Coding style ("prefer const over let")
- File organization ("components in src/components/")
- Testing approach ("always unit test utilities")
- Documentation style ("JSDoc for all public functions")

### PROCEDURE

**When to save**:
- Deployment process
- Build commands
- Testing workflows
- Release checklists

**Structure**:
```markdown
# PROCEDURE: {title}

## When to use
{triggering condition}

## Steps
1. {step 1}
2. {step 2}
3. {step 3}

## Expected outcome
{what success looks like}

## Troubleshooting
{common issues}
```

### NOTE

**When to save**:
- General observations
- Reminders
- Ideas for later
- Links to resources

## Time Anchoring (for Dyschronometria)

**Always provide**:
1. **Absolute timestamp**: ISO 8601 format
2. **Relative time**: "2 hours ago", "3 days ago", "last Tuesday"
3. **Context anchor**: "Before we added authentication", "After the redesign"

**Time utilities**:
```javascript
function relativeTime(timestamp) {
  const now = Date.now();
  const then = new Date(timestamp).getTime();
  const diff = now - then;

  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 60) return `${minutes} minutes ago`;
  if (hours < 24) return `${hours} hours ago`;
  if (days < 7) return `${days} days ago`;
  if (days < 30) return `${Math.floor(days/7)} weeks ago`;
  return `${Math.floor(days/30)} months ago`;
}
```

## Memory Index Structure

### Core Index File

`~/.claude-memories/index.json` (Linux/macOS) or `%USERPROFILE%\.claude-memories\index.json` (Windows):

```json
{
  "version": "1.0.0",
  "created": "ISO8601",
  "last_updated": "ISO8601",
  "total_memories": 0,
  "memories_by_type": {
    "DECISION": 0,
    "BLOCKER": 0,
    "CONTEXT": 0,
    "PREFERENCE": 0,
    "PROCEDURE": 0,
    "NOTE": 0
  },
  "memories": [
    {
      "id": "uuid",
      "type": "DECISION|BLOCKER|CONTEXT|PREFERENCE|PROCEDURE|NOTE",
      "content": "brief summary",
      "timestamp": "ISO8601",
      "tags": ["tag1", "tag2"],
      "project": "project-name",
      "status": "active|resolved|archived",
      "context": {
        "file": "optional-file-path",
        "line": "optional-line-number"
      }
    }
  ],
  "tags_index": {
    "tag-name": ["uuid1", "uuid2"]
  },
  "project_index": {
    "project-name": ["uuid1", "uuid2"]
  },
  "session_index": {
    "session-id": ["uuid1", "uuid2"]
  }
}
```

### Directory Structure

```
~/.claude-memories/  (Linux/macOS) or %USERPROFILE%\.claude-memories\ (Windows)
├── index.json                 # Master index
├── decisions/                 # Architecture decisions
│   ├── {uuid1}.md
│   └── {uuid2}.md
├── blockers/                  # Active/resolved blockers
│   ├── {uuid3}.md
│   └── {uuid4}.md
├── context/                   # Project context
│   ├── {uuid5}.md
│   └── {uuid6}.md
├── preferences/               # User preferences
│   ├── {uuid7}.md
│   └── {uuid8}.md
├── procedures/                # How-to procedures
│   ├── {uuid9}.md
│   └── {uuid10}.md
├── notes/                     # General notes
│   ├── {uuid11}.md
│   └── {uuid12}.md
├── sessions/                  # Session summaries
│   ├── 2025-10-17.md
│   └── 2025-10-16.md
└── backups/                   # Daily backups
    ├── index-2025-10-17.json
    └── index-2025-10-16.json
```

## Integration with Other Skills

### Session Launcher

Provides memories for session restoration:
- Recent decisions (last 7 days)
- Active blockers
- Project context
- Session summaries

### Error Debugger

Searches memories for:
- Similar past errors
- Solutions that worked
- Known blockers
- Relevant procedures

### Testing Builder

Recalls preferences:
- Testing style (unit/integration/E2E)
- Coverage requirements
- Test framework choices
- Mocking preferences

### Deployment Orchestrator

Loads procedures:
- Deployment workflows
- Environment configurations
- Rollback procedures
- Checklist items

## Proactive Memory Saving

Auto-save memories in these situations:

**During architecture discussions**:
```
User: "Let's use React for the frontend"
→ Auto-save as DECISION: Using React for frontend
```

**When encountering blockers**:
```
User: "Can't connect to the API"
→ Auto-save as BLOCKER: API connection failing
```

**When establishing preferences**:
```
User: "I prefer TypeScript over JavaScript"
→ Auto-save as PREFERENCE: Prefer TypeScript
```

**When creating procedures**:
```
User: "To deploy: run npm build then copy to server"
→ Auto-save as PROCEDURE: Deployment process
```

**Always confirm**:
```
💾 Saved as DECISION: Using React for frontend
(say "undo" within 30 seconds to cancel)
```

## Backup Strategy

**Daily backups**:
```bash
# Every 24 hours, create backup
# Linux/macOS:
cp ~/.claude-memories/index.json \
   ~/.claude-memories/backups/index-$(date +%Y-%m-%d).json

# Windows PowerShell:
# Copy-Item "$env:USERPROFILE\.claude-memories\index.json" `
#   "$env:USERPROFILE\.claude-memories\backups\index-$(Get-Date -Format 'yyyy-MM-dd').json"

# Keep last 30 days (Linux/macOS):
find ~/.claude-memories/backups/ -name "index-*.json" -mtime +30 -delete

# Windows PowerShell:
# Get-ChildItem "$env:USERPROFILE\.claude-memories\backups\index-*.json" |
#   Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

**Corruption recovery**:
```bash
# If index.json corrupted, restore from backup
# Linux/macOS:
cp ~/.claude-memories/backups/index-$(date -d yesterday +%Y-%m-%d).json \
   ~/.claude-memories/index.json

# Windows PowerShell:
# Copy-Item "$env:USERPROFILE\.claude-memories\backups\index-$(Get-Date (Get-Date).AddDays(-1) -Format 'yyyy-MM-dd').json" `
#   "$env:USERPROFILE\.claude-memories\index.json"
```

## Quick Reference

### Common Commands

| User Says | Action |
|-----------|--------|
| "remember we're using PostgreSQL" | Save as DECISION |
| "what did we decide about the database" | Search DECISIONs for "database" |
| "show all blockers" | List active BLOCKERs |
| "any blockers?" | Quick blocker check |
| "remember I prefer functional components" | Save as PREFERENCE |
| "search memories for authentication" | Full-text search |
| "blocker resolved: got API key" | Mark blocker as resolved |

### File Paths

- **Index**: `~/.claude-memories/index.json` (Linux/macOS) or `%USERPROFILE%\.claude-memories\index.json` (Windows)
- **Decisions**: `~/.claude-memories/decisions/{uuid}.md` or `%USERPROFILE%\.claude-memories\decisions\{uuid}.md`
- **Blockers**: `~/.claude-memories/blockers/{uuid}.md` or `%USERPROFILE%\.claude-memories\blockers\{uuid}.md`
- **Backups**: `~/.claude-memories/backups/` or `%USERPROFILE%\.claude-memories\backups\`

### Memory Lifecycle

1. **Create**: User says "remember" or auto-detected
2. **Store**: Added to index + detailed file created
3. **Recall**: Searched by keywords/tags/type/project
4. **Update**: Can be edited if context changes
5. **Archive**: Old memories archived but never deleted

### Success Criteria

✅ User never has to remember decisions
✅ "What did we decide?" is always answerable
✅ Blockers are tracked automatically
✅ All context is time-anchored
✅ Memory search returns relevant results in <1 second
✅ Zero reliance on user's biological memory
