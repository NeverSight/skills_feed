---
name: second-brain
description: Personal intelligence system for capturing thoughts, managing knowledge, and surfacing insights. Use when user wants to capture an idea, task, or note during conversation; query their knowledge base; check their inbox; review digests; or update task status. Triggers include "remember this," "add a task," "what did I say about," "show my inbox," or "mark complete."
license: MIT
---

# Second Brain Skill

Conversational interface to the Second Brain personal knowledge management system. Capture thoughts naturally during Claude Code sessions, query your knowledge graph, and manage your inbox.

## Core Philosophy

**Capture at the point of thinking, not after.**

This skill enables seamless capture during work sessions without breaking flow:
- Capture thoughts as they emerge
- Query past decisions and notes
- Surface today's priorities
- Track what needs review

**The system remembers so you don't have to.**

---

## Core Capabilities

### 1. Capture

Capture thoughts, tasks, ideas, and references directly from conversation.

**Usage patterns:**
- "Remember that the API rate limit is 1000 req/min"
- "Add a task to review the PR from Sarah"
- "Note: decided to use Supabase for sync"
- "Capture this idea: what if we..."

**Classification:**
The system uses AI to classify captures into types:
- **task**: Actionable item with completion state
- **idea**: Non-actionable insight worth remembering
- **reference**: Information for later retrieval
- **meeting**: Time-bound event with notes
- **goal**: Outcome you're working toward
- **project**: Collection of related work
- **value**: Core principle that guides decisions
- **person**: Relationship context

**Confidence threshold:**
- High confidence (≥0.6): Auto-classified
- Low confidence (<0.6): Sent to needs_review

---

### 2. Query

Search and explore your knowledge graph.

**Usage patterns:**
- "What did I say about authentication?"
- "What projects support the 'shipping velocity' goal?"
- "Show me tasks related to the SecondBrain project"
- "Who did I meet with about the budget?"

**Query types:**
- **Semantic search**: Find by meaning, not just keywords
- **Graph traversal**: Follow relationships (supports, blocks, contains)
- **Filter by type**: "Show me all ideas from this week"
- **Filter by domain**: "What work tasks are due?"

---

### 3. Inbox

Review and triage pending captures.

**Usage patterns:**
- "Show my inbox"
- "What's waiting for review?"
- "How many pending captures?"

**Inbox states:**
- **pending**: Awaiting AI classification
- **needs_review**: Low confidence, needs human decision
- **processing**: Currently being classified

---

### 4. Digest

Get actionable summaries of what matters.

**Usage patterns:**
- "What should I focus on today?"
- "Show me today's digest"
- "What's overdue?"

**Digest includes:**
- Due tasks (today and overdue)
- High priority items
- Today's meetings
- Items needing review
- Recent insights

**Constraints:**
- Daily digest: <150 words
- Weekly review: <250 words

---

### 5. Actions

Update status and manage nodes.

**Usage patterns:**
- "Mark the PR review task done"
- "Complete task abc123"
- "Archive the old project"
- "Set priority to high for..."

**Supported actions:**
- Complete/reopen tasks
- Update priority (0-4)
- Change status (active, completed, archived)
- Add domain tag (work, personal, both)

---

## Workflow Integration

### During Work Sessions

When user mentions something capture-worthy during natural conversation:

1. **Recognize capture intent:**
   - Direct: "Remember this...", "Add a task..."
   - Implicit: "I should...", "Don't forget...", "Note to self..."

2. **Capture with context:**
   - Include relevant context from current conversation
   - Tag with source: "cli" (Claude Code session)
   - Add any mentioned relationships

3. **Confirm capture:**
   - Brief confirmation with ID
   - Mention if needs_review due to low confidence

### Quick Actions

For common actions, provide shortcuts:

```
/sb capture "thought or idea"     # Capture immediately
/sb inbox                         # Show pending items
/sb digest                        # Today's actionable summary
/sb query "search term"           # Search knowledge base
/sb done <id>                     # Mark task complete
```

---

## Meeting Transcript Processing

**Use case:** Paste meeting transcripts to automatically extract and capture structured content.

### Workflow

1. **User pastes transcript:**
   ```
   "Here's the transcript from today's standup:
   [transcript content]"
   ```

2. **System processes and extracts:**
   - Meeting summary → MEETING node
   - Action items → TASK nodes
   - Decisions made → REFERENCE nodes
   - People mentioned → PERSON links
   - Follow-up meetings → MEETING nodes
   - Key insights → IDEA nodes

3. **Confirmation and review:**
   ```
   Processed standup transcript:

   📅 Created: "Daily Standup - Jan 15" (meeting)

   ✅ Extracted 4 tasks:
   - "Review PR #1234" → assigned to you (high)
   - "Update API docs" → assigned to Sarah
   - "Schedule design review" → due Friday
   - "Fix login bug" → blocked by infrastructure

   📝 Captured 2 decisions:
   - "Using Postgres instead of MongoDB"
   - "Sprint ends Friday, demo at 2pm"

   👥 Linked 3 people:
   - Sarah (mentioned 5x)
   - Mike (mentioned 2x)
   - John (new person, created)

   💡 1 insight flagged:
   - "Team velocity improves when standups are <15 min"
   ```

### Extraction Patterns

**Action items (→ TASK):**
- "TODO: ...", "Action: ...", "Need to..."
- "Sarah will...", "I'll...", "We should..."
- "@mentions with action verbs"

**Decisions (→ REFERENCE):**
- "Decided: ...", "Agreed: ..."
- "We're going with...", "The plan is..."
- "Final decision: ..."

**Follow-ups (→ MEETING):**
- "Let's meet again...", "Schedule a follow-up..."
- "Next week we'll discuss..."
- Explicit dates/times mentioned

**People (→ PERSON links):**
- Names mentioned in context
- @mentions
- "talked to...", "asked..."

**Insights (→ IDEA):**
- Observations about patterns
- Hypotheses mentioned
- "I noticed...", "Interesting that..."

### Post-Processing

After extraction:
1. **Create meeting node** with summary
2. **Create task nodes** with assignments and due dates
3. **Link people** (create if new)
4. **Store decisions** as references
5. **Write to Obsidian** with wikilinks

### Configuration

```yaml
# ~/.config/secondbrain/daemons.yml
transcript_processing:
  auto_assign_unassigned: true  # Assign to self
  default_task_priority: 2
  flag_low_confidence: true     # Mark uncertain extractions
  link_to_meeting: true         # Connect all items to meeting node
```

---

## Graph Model

### Node Types

| Type | Description | Example |
|------|-------------|---------|
| value | Core principle | "Family comes first" |
| goal | Outcome to achieve | "Run a marathon by December" |
| project | Related work collection | "Kitchen renovation" |
| task | Actionable item | "Call dentist to schedule" |
| person | Relationship context | "Sarah - VP Engineering" |
| meeting | Time-bound event | "1:1 with Sarah - Jan 15" |
| idea | Non-actionable insight | "What if AI for onboarding?" |
| reference | Info for retrieval | "API rate limit: 1000/min" |

### Edge Types

| Relation | Meaning | Example |
|----------|---------|---------|
| supports | Provides evidence for | project → goal |
| blocks | Prevents progress on | task → task |
| contains | Hierarchical parent | project → task |
| derived_from | Extracted from | goal → value |
| assigned_to | Assigned to person | task → person |
| mentioned_in | Referenced in context | person → meeting |
| related_to | General relationship | idea → reference |
| child_of | Subtask/child | task → task |

---

## Implementation

### CLI Integration

This skill wraps the `sb` CLI commands:

```bash
sb capture "content"      # Capture a thought
sb inbox                  # List pending captures
sb process                # Classify pending captures
sb digest                 # Generate daily digest
sb list [type]            # List nodes
sb show <id>              # Show node details
sb status                 # System health check
```

### Database

- Local SQLite at `~/.local/share/secondbrain/secondbrain.db`
- Obsidian vault for markdown output
- Graph model: nodes + typed edges

### Configuration

```yaml
# ~/.config/secondbrain/config.yml
node_id: "home"
vault_path: "/path/to/vault"
classification:
  model: "claude-sonnet-4-20250514"
  confidence_threshold: 0.6
```

---

## Context Awareness

### Use Session Context

When capturing, leverage current conversation context:

- **File being discussed**: Link to related codebase notes
- **Error being debugged**: Capture as reference with solution
- **Decision being made**: Note with rationale
- **Meeting notes mentioned**: Parse for action items

### Domain Detection

Infer domain from context:
- In work project directory → domain: work
- Personal topics mentioned → domain: personal
- Both contexts mixed → domain: both

---

## Example Interactions

### Capture During Work

```
User: "The deadline for the API migration is March 15th"
Assistant: [Captures as task with due date]
Captured: API migration deadline - Due March 15th (ID: abc123)
```

### Query Knowledge

```
User: "What did we decide about authentication?"
Assistant: [Searches knowledge graph]
Found 3 related items:
- [reference] "Use JWT with refresh tokens" (Jan 5)
- [task] "Implement OAuth flow" (in_progress)
- [meeting] "Auth design review with Sarah" (Jan 3)
```

### Morning Digest

```
User: "What should I focus on today?"
Assistant: [Generates digest]

📋 Today's Focus (Wed, Jan 15):
- [OVERDUE] Review PR from Sarah (due Jan 14)
- [HIGH] Prepare API migration plan
- [DUE TODAY] Call dentist to reschedule

📅 Meetings:
- 10:00 1:1 with Mike

⚠️ Needs Review: 2 items in inbox
```

---

## Anti-Patterns

**Don't:**
- Capture every single thing mentioned (be selective)
- Force classification when context is unclear
- Interrupt flow for minor captures
- Create duplicate entries for same concept
- Over-classify simple notes

**Do:**
- Capture when user expresses intent or importance
- Ask for clarification if capture intent is ambiguous
- Batch confirmations when capturing multiple items
- Link to existing nodes when relationships are clear
- Respect user's domain boundaries

---

## Integration Points

**With beads issue tracker:**
- Cross-reference tasks with beads issues
- Import epic/task relationships

**With Obsidian vault:**
- Generated markdown syncs via Obsidian Sync
- Wikilinks enable navigation
- Daily notes include digest

**With SiliconDoppelgangerActual:**
- Deep queries via agent conversation
- Complex graph traversals
- Multi-step reasoning about priorities

---

## Success Metrics

**Skill succeeds when:**
- Captures happen naturally without flow interruption
- User finds past information quickly
- Daily digests surface actionable items
- Inbox stays manageable (<10 items needing review)
- Classification accuracy >85%

**User feels:**
- Confident nothing important is lost
- Informed about what matters today
- In control of their knowledge system