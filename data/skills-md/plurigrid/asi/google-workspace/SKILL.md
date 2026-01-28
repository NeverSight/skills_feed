---
name: google-workspace
description: Google Workspace MCP integration for Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, and Chat. Use when the user wants to read/send emails, manage files, create/edit documents, schedule events, or interact with any Google Workspace service.
version: 1.0.0
---


# Google Workspace Skill

Comprehensive MCP integration for all Google Workspace services.

## Denotation

> **Google Workspace tasks map to functional invariants, resulting in consistent email, file, calendar, and task states under Narya condensation and GF(3) conservation.**

The skill reaches a **fixed point** when all pending operations complete with no H¹ obstructions (gluing failures), and thread/folder trit sums are conserved modulo 3.

## Formal Contract

```
Effect: Google Workspace → State × Trit
Invariant: ∀ closed workflow: Σ(trit) ≡ 0 (mod 3)
Denotation: ⟦GW⟧ = lim_{n→∞} Condense(Op_n(...Op_1(S_0)))
```

## Required Parameter

**All tools require `user_google_email`** - the user's Google email address.

## Services Overview

### 📧 Gmail (MINUS -1: Validator)

| Tool | Description |
|------|-------------|
| `search_gmail_messages` | Search with Gmail query syntax |
| `get_gmail_message_content` | Get full message content |
| `get_gmail_messages_content_batch` | Batch get (max 25) |
| `get_gmail_thread_content` | Get full conversation thread |
| `send_gmail_message` | Send email (supports replies) |
| `draft_gmail_message` | Create draft (supports replies) |
| `modify_gmail_message_labels` | Add/remove labels (archive, delete) |
| `batch_modify_gmail_message_labels` | Bulk label operations |
| `list_gmail_labels` | List all labels with IDs |
| `manage_gmail_label` | Create/update/delete labels |

**Query syntax examples:**
- `from:user@example.com` - From specific sender
- `is:unread` - Unread messages
- `has:attachment` - Has attachments
- `after:2024/01/01` - Date filters

### 📁 Drive (ERGODIC 0: Coordinator)

| Tool | Description |
|------|-------------|
| `search_drive_files` | Search files by query |
| `list_drive_items` | List folder contents |
| `get_drive_file_content` | Get file content (text extraction) |
| `get_drive_file_download_url` | Get download URL |
| `create_drive_file` | Create new file |
| `update_drive_file` | Update metadata |
| `share_drive_file` | Share with users/groups/anyone |
| `batch_share_drive_file` | Bulk sharing |
| `get_drive_file_permissions` | Check permissions |
| `get_drive_shareable_link` | Get shareable link |
| `remove_drive_permission` | Revoke access |
| `transfer_drive_ownership` | Transfer file ownership |

### 📅 Calendar (PLUS +1: Executor)

| Tool | Description |
|------|-------------|
| `list_calendars` | List user's calendars |
| `get_events` | Get events (by ID or time range) |
| `create_event` | Create new event |
| `modify_event` | Update existing event |
| `delete_event` | Delete event |

**Event creation options:**
- `add_google_meet: true` - Add Meet link
- `attendees: ["email1", "email2"]` - Invite attendees
- `reminders: [{"method": "popup", "minutes": 15}]` - Custom reminders
- `transparency: "transparent"` - Show as available

### 📄 Docs (MINUS -1)

| Tool | Description |
|------|-------------|
| `search_docs` | Search Google Docs |
| `list_docs_in_folder` | List docs in folder |
| `create_doc` | Create new document |
| `get_doc_content` | Get document content |
| `modify_doc_text` | Insert/replace/format text |
| `find_and_replace_doc` | Find and replace |
| `insert_doc_image` | Insert image |
| `insert_doc_elements` | Insert table/list/page break |
| `create_table_with_data` | Create populated table |
| `inspect_doc_structure` | Get document structure |
| `debug_table_structure` | Debug table layout |
| `update_doc_headers_footers` | Update headers/footers |
| `batch_update_doc` | Multiple operations |
| `export_doc_to_pdf` | Export to PDF |

### 📊 Sheets (ERGODIC 0)

| Tool | Description |
|------|-------------|
| `list_spreadsheets` | List spreadsheets |
| `create_spreadsheet` | Create new spreadsheet |
| `get_spreadsheet_info` | Get spreadsheet metadata |
| `create_sheet` | Add new sheet |
| `read_sheet_values` | Read cell range |
| `modify_sheet_values` | Write/update/clear cells |

**Range syntax:** `Sheet1!A1:D10` or `A1:Z1000`

### 📽️ Slides (PLUS +1)

| Tool | Description |
|------|-------------|
| `create_presentation` | Create new presentation |
| `get_presentation` | Get presentation details |
| `get_page` | Get slide details |
| `get_page_thumbnail` | Get slide thumbnail |
| `batch_update_presentation` | Apply updates |

### 📋 Forms

| Tool | Description |
|------|-------------|
| `create_form` | Create new form |
| `get_form` | Get form details |
| `list_form_responses` | List responses |
| `get_form_response` | Get specific response |
| `set_publish_settings` | Update publish settings |

### ✅ Tasks

| Tool | Description |
|------|-------------|
| `list_task_lists` | List all task lists |
| `get_task_list` | Get task list details |
| `create_task_list` | Create new list |
| `update_task_list` | Rename list |
| `delete_task_list` | Delete list |
| `list_tasks` | List tasks in list |
| `get_task` | Get task details |
| `create_task` | Create task |
| `update_task` | Update task |
| `delete_task` | Delete task |
| `move_task` | Move task (position/list) |
| `clear_completed_tasks` | Clear completed |

### 💬 Chat

| Tool | Description |
|------|-------------|
| `list_spaces` | List Chat spaces |
| `get_messages` | Get messages from space |
| `search_messages` | Search messages |
| `send_message` | Send message to space |

### 🔍 Custom Search

| Tool | Description |
|------|-------------|
| `search_custom` | Programmable Search Engine |
| `search_custom_siterestrict` | Site-restricted search |
| `get_search_engine_info` | Get search engine config |

### 💬 Comments (All Doc Types)

| Tool | Description |
|------|-------------|
| `read_document_comments` | Read doc comments |
| `create_document_comment` | Add doc comment |
| `reply_to_document_comment` | Reply to comment |
| `resolve_document_comment` | Resolve comment |
| `read_spreadsheet_comments` | Read sheet comments |
| `create_spreadsheet_comment` | Add sheet comment |
| `read_presentation_comments` | Read slide comments |
| `create_presentation_comment` | Add slide comment |

## GF(3) Triadic Workflow

```
MINUS (-1): Validation/Reading
├── search_gmail_messages
├── get_doc_content
├── read_sheet_values
└── list_drive_items

ERGODIC (0): Coordination/Metadata
├── get_spreadsheet_info
├── list_calendars
├── inspect_doc_structure
└── get_drive_file_permissions

PLUS (+1): Execution/Writing
├── send_gmail_message
├── create_event
├── modify_sheet_values
└── create_drive_file
```

## Common Workflows

### Email Management
```python
# Search → Read → Reply
messages = search_gmail_messages(query="from:boss is:unread")
content = get_gmail_message_content(message_id=messages[0].id)
send_gmail_message(
    to="boss@company.com",
    subject="Re: " + content.subject,
    body="Response...",
    thread_id=content.thread_id,
    in_reply_to=content.message_id
)
```

### Document Creation
```python
# Create → Inspect → Add Table
doc = create_doc(title="Report")
structure = inspect_doc_structure(document_id=doc.id)
create_table_with_data(
    document_id=doc.id,
    index=structure.total_length,
    table_data=[["Header1", "Header2"], ["Data1", "Data2"]]
)
```

### Calendar Scheduling
```python
# Check availability → Create event with Meet
events = get_events(
    time_min="2024-12-26T09:00:00Z",
    time_max="2024-12-26T17:00:00Z"
)
create_event(
    summary="Team Sync",
    start_time="2024-12-26T14:00:00Z",
    end_time="2024-12-26T15:00:00Z",
    attendees=["team@company.com"],
    add_google_meet=True
)
```

### File Sharing
```python
# Share with expiration
share_drive_file(
    file_id="abc123",
    share_with="contractor@example.com",
    role="writer",
    expiration_time="2025-01-15T00:00:00Z"
)
```

## Authentication

If tools fail with auth errors, use:
```
start_google_auth(service_name="gmail|drive|calendar|docs|sheets|slides|forms|tasks|chat")
```

## Tips

1. **Batch operations** - Use batch tools for multiple items
2. **Table creation** - Always call `inspect_doc_structure` first to get safe index
3. **Email threading** - Include `thread_id`, `in_reply_to`, `references` for proper replies
4. **Drive shared drives** - Use `drive_id` parameter for shared drive operations
5. **Calendar attachments** - Use Drive file URLs or IDs for event attachments

## Related Skills (Backlinks)

| Skill | Trit | Integration |
|-------|------|-------------|
| [finder-color-walk](file:///Users/alice/agent-o-rama/agent-o-rama/skills/finder-color-walk/SKILL.md) | 0 | Drive files ↔ local Finder GF(3) coloring via `drive_color_walk.py` |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | SplitMix64 deterministic colors for file organization |
| [triad-interleave](file:///Users/alice/.agents/skills/triad-interleave/SKILL.md) | +1 | Schedule Drive operations in GF(3)-balanced triplets |
| [bisimulation-game](file:///Users/alice/.agents/skills/bisimulation-game/SKILL.md) | -1 | Verify Drive state equivalence across agents |

## Triadic Integration Pattern

```
google-workspace (ERGODIC 0) ─── Coordinator
        │
        ├── finder-color-walk (0) ─── File coloring bridge
        │       └── drive_color_walk.py
        │
        ├── gay-mcp (+1) ─── Color generation
        │       └── SplitMix64 seeds → GF(3) trits
        │
        └── bisimulation-game (-1) ─── State verification
                └── Attacker/Defender/Arbiter protocol

GF(3) Check: 0 + 0 + 1 + (-1) = 0 ✓
```

## Invariant Set

| Invariant | Definition | Verification |
|-----------|------------|--------------|
| `NoDuplication` | Each item (message, event, file) resides in exactly one triadic queue | Queue intersection = ∅ |
| `RouteInvariance` | `route(item) = agent_of(trit(item))` always | For all items, routing is deterministic |
| `ThreadConservation` | Thread trit sum ≡ 0 (mod 3) at cycle close | `verify_h1_obstruction()` returns no violations |
| `ClosedWorkflowBalance` | Any complete workflow has Σ trits = 0 | GF(3) conservation check |

## Narya Compatibility

| Field | Definition | Example |
|-------|------------|---------|
| `before` | Raw input from Google APIs | `{"messages": [...], "files": [...]}` |
| `after` | Transformed interactions with GF(3) trits | `[{id, trit, verb, thread_id}]` |
| `delta` | Change in triadic queue state | `{added: 3, removed: 1, trit_sum_delta: +1}` |
| `birth` | Initial unprocessed state | Empty queues, no interactions |
| `impact` | 1 if equivalence class changed, 0 otherwise | Used for ANIMA detection |

## Condensation Policy

**Trigger**: When 10 consecutive operations yield no change in equivalence classes.

```python
def should_condense(history: List[State], threshold: int = 10) -> bool:
    if len(history) < threshold:
        return False
    recent = history[-threshold:]
    return all(equiv(s) == equiv(recent[0]) for s in recent)
```

**Action**: Collapse queue state into condensed fingerprint, archive processed items.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
google-workspace (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch7: Propagators
- Ch6: Layering
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch1: Flexibility through Abstraction

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.