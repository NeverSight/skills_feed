---
name: basecamp
description: Interact with Basecamp projects via CLI. Manage card tables, todos, messages, documents, schedules, campfires, people, check-ins, uploads, and more. Use when the user mentions Basecamp, cards, todos, messages, or project management.
---

# Basecamp CLI

Command-line interface for Basecamp. All output is JSON.

## Prerequisites

```bash
basecamp version   # Verify installation
basecamp projects  # Verify authentication (run `basecamp auth` if needed)
```

## Project Context

Create `.basecamp.yml` in a directory to set default project:

```yaml
project_id: 12345678
```

Then omit project_id from commands when in that directory.

## Commands Reference

### Projects & Boards

```bash
basecamp projects                          # List all projects
basecamp boards [project_id]               # List card tables
basecamp columns [project_id] <board_id>   # List columns in board
```

### Cards

```bash
basecamp cards [project_id] <board_id>                    # List cards
basecamp cards [project_id] <board_id> --column "Name"    # Filter by column
basecamp card [project_id] <card_id>                      # View card
basecamp card [project_id] <card_id> --comments           # With comments
basecamp card-create [project_id] <board_id> --column <col_id> --title "Title"
basecamp card-update [project_id] <card_id> --title "New" --content "Text"
basecamp move [project_id] <board_id> <card_id> --to "Column Name"
```

### Card Steps (Checklists)

```bash
basecamp step-create [project_id] <card_id> --title "Step"
basecamp step-create [project_id] <card_id> --title "Step" --due 2026-02-01 --assignees "123,456"
basecamp step-update [project_id] <step_id> --title "Updated"
basecamp step-complete [project_id] <step_id>
basecamp step-uncomplete [project_id] <step_id>
basecamp step-reposition [project_id] <card_id> <step_id> --position 0
```

### Todos

```bash
basecamp todolists [project_id]                           # List todo lists
basecamp todos [project_id] <todolist_id>                 # List todos
basecamp todos [project_id] <todolist_id> --completed     # Completed todos
basecamp todo [project_id] <todo_id>                      # View todo
basecamp todo-create [project_id] <list_id> --content "Task" --due 2026-02-01
basecamp todo-complete [project_id] <todo_id>
basecamp todo-uncomplete [project_id] <todo_id>
basecamp todo-reposition [project_id] <todo_id> --position 1
```

### Todo Groups

```bash
basecamp todolist-groups [project_id] <todolist_id>       # List groups
basecamp todolist-group [project_id] <group_id>           # View group
basecamp todolist-group-create [project_id] <list_id> --name "Sprint 1" --color green
```

### Messages

```bash
basecamp messages [project_id]                            # List messages
basecamp message [project_id] <message_id>                # View message
basecamp message [project_id] <message_id> --comments     # With comments
basecamp message-create [project_id] --subject "Subject" --content "Body"
```

### Comments

```bash
basecamp comment-add [project_id] <recording_id> --content "Comment"
```

### Documents

```bash
basecamp docs [project_id]                                # List documents
basecamp doc [project_id] <doc_id>                        # View document
basecamp doc [project_id] <doc_id> --comments             # With comments
basecamp doc-create [project_id] --title "Title" --content "Content"
```

### Schedule

```bash
basecamp schedule [project_id]                            # List entries
basecamp event [project_id] <entry_id>                    # View event
basecamp event [project_id] <entry_id> --comments         # With comments
basecamp event-create [project_id] --summary "Meeting" --starts-at "2026-02-01T10:00:00Z" --ends-at "2026-02-01T11:00:00Z"
basecamp event-create [project_id] --summary "Holiday" --starts-at "2026-02-01" --ends-at "2026-02-01" --all-day
```

### Campfire

```bash
basecamp campfire [project_id]                            # List messages
basecamp campfire-post [project_id] --content "Hello!"
```

### Search

```bash
basecamp search "query"                                   # Search all projects
basecamp search "query" --type Todo                       # Filter by type
basecamp search "query" --project <project_id>            # Filter by project
```

Types: Todo, Message, Document, Kanban::Card, Schedule::Entry, Comment

### People

```bash
basecamp people                                           # List all people
basecamp person <person_id>                               # View person
basecamp people-pingable                                  # Pingable people
basecamp people-project [project_id]                      # Project members
basecamp my-profile                                       # Your profile
basecamp project-access [project_id] --grant "123,456" --revoke "789"
```

### Automatic Check-ins

```bash
basecamp questionnaire [project_id]                       # Questionnaire info
basecamp questions [project_id]                           # List questions
basecamp question [project_id] <question_id>              # View question
basecamp question [project_id] <question_id> --comments   # With comments
basecamp question-answers [project_id] <question_id>      # List answers
basecamp question-answer [project_id] <answer_id>         # View answer
```

### Uploads

```bash
basecamp upload /path/to/file.pdf                         # Upload file (returns sgid)
basecamp uploads [project_id] <vault_id>                  # List uploads in vault
basecamp upload-view [project_id] <upload_id>             # View upload
basecamp upload-view [project_id] <upload_id> --comments  # With comments
```

### Recordings Management

```bash
basecamp archive [project_id] <recording_id>              # Archive recording
basecamp unarchive [project_id] <recording_id>            # Unarchive
basecamp trash [project_id] <recording_id>                # Trash recording
```

### Message Types

```bash
basecamp message-types [project_id]                       # List types
basecamp message-type [project_id] <type_id>              # View type
basecamp message-type-create [project_id] --name "Announcement" --icon "📢"
basecamp message-type-update [project_id] <type_id> --name "Update" --icon "✅"
basecamp message-type-delete [project_id] <type_id>
```

### Activity Events

```bash
basecamp events                                           # All events
basecamp events-project [project_id]                      # Project events
basecamp events-recording [project_id] <recording_id>     # Recording events
```

## Error Handling

Errors return JSON to stderr:

```json
{"error": "not authenticated, run 'basecamp auth' first"}
```

## Tips

- All commands output JSON - pipe to `jq` for filtering
- Use `--comments` flag to include comments on supported commands
- Recording IDs work across types (todos, cards, messages, etc.)
- Get vault_id from `basecamp docs` output for upload commands
