---
name: nlm-cli-skill
description: "Expert guide for the NotebookLM CLI (`nlm`) - a command-line interface for Google NotebookLM. Use this skill when users want to interact with NotebookLM programmatically, including: creating/managing notebooks, adding sources (URLs, YouTube, text, Google Drive), generating content (podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, data tables), conducting research, chatting with sources, or automating NotebookLM workflows. Triggers on mentions of \"nlm\", \"notebooklm\", \"notebook lm\", \"podcast generation\", \"audio overview\", or any NotebookLM-related automation task."
---

# NotebookLM CLI Expert

This skill provides comprehensive guidance for using the `nlm` CLI to automate Google NotebookLM workflows.

## Quick Reference

```bash
nlm --help              # List all commands
nlm <command> --help    # Help for specific command
nlm --ai                # Full AI-optimized documentation
nlm --version           # Check installed version
```

## Critical Rules (Read First!)

1. **Always authenticate first**: Run `nlm login` before any operations
2. **Sessions expire in ~20 minutes**: Re-run `nlm login` if commands start failing
3. **`--confirm` is REQUIRED**: All generation and delete commands need `--confirm` or `-y`
4. **Research requires `--notebook-id`**: The flag is mandatory, not positional
5. **Capture IDs from output**: Create/start commands return IDs needed for subsequent operations
6. **Use aliases**: Simplify long UUIDs with `nlm alias set <name> <uuid>`
7. **⚠️ ALWAYS ASK USER BEFORE DELETE**: Before executing ANY delete command, ask the user for explicit confirmation. Deletions are **irreversible**. Show what will be deleted and warn about permanent data loss.
8. **Check aliases before creating**: Run `nlm alias list` before creating a new alias to avoid conflicts with existing names.
9. **DO NOT launch REPL**: Never use `nlm chat start` - it opens an interactive REPL that AI tools cannot control. Use `nlm notebook query` for one-shot Q&A instead.
10. **Choose output format wisely**: Default output (no flags) is compact and token-efficient—use it for status checks. Use `--quiet` to capture IDs for piping. Only use `--json` when you need to parse specific fields programmatically.

## Workflow Decision Tree

Use this to determine the right sequence of commands:

```
User wants to...
│
├─► Work with NotebookLM for the first time
│   └─► nlm login → nlm notebook create "Title"
│
├─► Add content to a notebook
│   ├─► From a URL/webpage → nlm source add <nb-id> --url "https://..."
│   ├─► From YouTube → nlm source add <nb-id> --url "https://youtube.com/..."
│   ├─► From pasted text → nlm source add <nb-id> --text "content" --title "Title"
│   ├─► From Google Drive → nlm source add <nb-id> --drive <doc-id> --type doc
│   └─► Discover new sources → nlm research start "query" --notebook-id <nb-id>
│
├─► Generate content from sources
│   ├─► Podcast/Audio → nlm audio create <nb-id> --confirm
│   ├─► Written summary → nlm report create <nb-id> --confirm
│   ├─► Study materials → nlm quiz/flashcards create <nb-id> --confirm
│   ├─► Visual content → nlm mindmap/slides/infographic create <nb-id> --confirm
│   ├─► Video → nlm video create <nb-id> --confirm
│   └─► Extract data → nlm data-table create <nb-id> "description" --confirm
│
├─► Ask questions about sources
│   └─► nlm notebook query <nb-id> "question"
│       (Use --conversation-id for follow-ups)
│       ⚠️ Do NOT use `nlm chat start` - it's a REPL for humans only
│
├─► Check generation status
│   └─► nlm studio status <nb-id>
│
└─► Manage/cleanup
    ├─► List notebooks → nlm notebook list
    ├─► List sources → nlm source list <nb-id>
    ├─► Delete source → nlm source delete <source-id> --confirm
    └─► Delete notebook → nlm notebook delete <nb-id> --confirm
```

## Command Categories

### 1. Authentication

```bash
nlm login                    # Launch Chrome, extract cookies (primary method)
nlm login --check            # Validate current session
nlm login --profile work     # Use named profile for multiple accounts
nlm auth status              # Check if authenticated
nlm auth list                # List all profiles
```

**Session lifetime**: ~20 minutes. Re-authenticate when commands fail with auth errors.

### 2. Notebook Management

```bash
nlm notebook list                      # List all notebooks
nlm notebook list --json               # JSON output for parsing
nlm notebook list --quiet              # IDs only (for scripting)
nlm notebook create "Title"            # Create notebook, returns ID
nlm notebook get <id>                  # Get notebook details
nlm notebook describe <id>             # AI-generated summary + suggested topics
nlm notebook query <id> "question"     # One-shot Q&A with sources
nlm notebook rename <id> "New Title"   # Rename notebook
nlm notebook delete <id> --confirm     # PERMANENT deletion
```

### 3. Source Management

```bash
# Adding sources
nlm source add <nb-id> --url "https://..."           # Web page
nlm source add <nb-id> --url "https://youtube.com/..." # YouTube video
nlm source add <nb-id> --text "content" --title "X"  # Pasted text
nlm source add <nb-id> --drive <doc-id>              # Drive doc (auto-detect type)
nlm source add <nb-id> --drive <doc-id> --type slides # Explicit type

# Listing and viewing
nlm source list <nb-id>                # Table of sources
nlm source list <nb-id> --drive        # Show Drive sources with freshness
nlm source list <nb-id> --drive -S     # Skip freshness checks (faster)
nlm source get <source-id>             # Source metadata
nlm source describe <source-id>        # AI summary + keywords
nlm source content <source-id>         # Raw text content
nlm source content <source-id> -o file.txt  # Export to file

# Drive sync (for stale sources)
nlm source stale <nb-id>               # List outdated Drive sources
nlm source sync <nb-id> --confirm      # Sync all stale sources
nlm source sync <nb-id> --source-ids <ids> --confirm  # Sync specific

# Deletion
nlm source delete <source-id> --confirm
```

**Drive types**: `doc`, `slides`, `sheets`, `pdf`

### 4. Research (Source Discovery)

Research finds NEW sources from the web or Google Drive:

```bash
# Start research (--notebook-id is REQUIRED)
nlm research start "query" --notebook-id <id>              # Fast web (~30s)
nlm research start "query" --notebook-id <id> --mode deep  # Deep web (~5min)
nlm research start "query" --notebook-id <id> --source drive  # Drive search

# Check progress
nlm research status <nb-id>                   # Poll until done (5min max)
nlm research status <nb-id> --max-wait 0      # Single check, no waiting
nlm research status <nb-id> --task-id <tid>   # Check specific task
nlm research status <nb-id> --full            # Full details

# Import discovered sources
nlm research import <nb-id> <task-id>            # Import all
nlm research import <nb-id> <task-id> --indices 0,2,5  # Import specific
```

**Modes**: `fast` (~30s, ~10 sources) | `deep` (~5min, ~40+ sources, web only)

### 5. Content Generation (Studio)

All generation commands share these flags:
- `--confirm` or `-y`: **REQUIRED** to execute
- `--source-ids <id1,id2>`: Limit to specific sources
- `--language <code>`: BCP-47 code (en, es, fr, de, ja)

```bash
# Audio (Podcast)
nlm audio create <id> --confirm
nlm audio create <id> --format deep_dive --length default --confirm
nlm audio create <id> --format brief --focus "key topic" --confirm
# Formats: deep_dive, brief, critique, debate
# Lengths: short, default, long

# Report
nlm report create <id> --confirm
nlm report create <id> --format "Study Guide" --confirm
nlm report create <id> --format "Create Your Own" --prompt "Custom..." --confirm
# Formats: "Briefing Doc", "Study Guide", "Blog Post", "Create Your Own"

# Quiz
nlm quiz create <id> --confirm
nlm quiz create <id> --count 5 --difficulty 3 --confirm
# Count: number of questions (default: 2)
# Difficulty: 1-5 (1=easy, 5=hard)

# Flashcards
nlm flashcards create <id> --confirm
nlm flashcards create <id> --difficulty hard --confirm
# Difficulty: easy, medium, hard

# Mind Map
nlm mindmap create <id> --confirm
nlm mindmap create <id> --title "Topic Overview" --confirm
nlm mindmap list <id>  # List existing mind maps

# Slides
nlm slides create <id> --confirm
nlm slides create <id> --format presenter --length short --confirm
# Formats: detailed, presenter | Lengths: short, default

# Infographic
nlm infographic create <id> --confirm
nlm infographic create <id> --orientation portrait --detail detailed --confirm
# Orientations: landscape, portrait, square
# Detail: concise, standard, detailed

# Video
nlm video create <id> --confirm
nlm video create <id> --format brief --style whiteboard --confirm
# Formats: explainer, brief
# Styles: auto_select, classic, whiteboard, kawaii, anime, watercolor, retro_print, heritage, paper_craft

# Data Table
nlm data-table create <id> "Extract all dates and events" --confirm
# DESCRIPTION is required as second argument
```

### 6. Studio (Artifact Management)

Check and manage generated content:

```bash
nlm studio status <nb-id>                          # List all artifacts
nlm studio status <nb-id> --json                   # JSON output
nlm studio delete <nb-id> <artifact-id> --confirm  # Delete artifact
```

**Status values**: `completed` (✓), `in_progress` (●), `failed` (✗)

### 7. Interactive Chat (Human Users Only)

> ⚠️ **AI TOOLS: DO NOT USE `nlm chat start`** - It launches an interactive REPL that cannot be controlled programmatically. Use `nlm notebook query` for one-shot Q&A instead.

For human users at a terminal:

```bash
nlm chat start <nb-id>  # Launch interactive REPL
```

**REPL Commands**:
- `/sources` - List available sources
- `/clear` - Reset conversation context
- `/help` - Show commands
- `/exit` - Exit REPL

**Configure chat behavior** (works for both REPL and query):
```bash
nlm chat configure <id> --goal default
nlm chat configure <id> --goal learning_guide
nlm chat configure <id> --goal custom --prompt "Act as a tutor..."
nlm chat configure <id> --response-length longer  # longer, default, shorter
```

### 8. Aliases (UUID Shortcuts)

Simplify long UUIDs:

```bash
nlm alias set myproject abc123-def456...  # Create alias (auto-detects type)
nlm alias get myproject                    # Resolve to UUID
nlm alias list                             # List all aliases
nlm alias delete myproject                 # Remove alias

# Use aliases anywhere
nlm notebook get myproject
nlm source list myproject
nlm audio create myproject --confirm
```

### 9. Configuration

```bash
nlm config show              # Show current config
nlm config get <key>         # Get specific setting
nlm config set <key> <value> # Update setting
```

## Output Formats

Most list commands support multiple formats:

| Flag | Description |
|------|-------------|
| (none) | Rich table (human-readable) |
| `--json` | JSON output (for parsing) |
| `--quiet` | IDs only (for piping) |
| `--title` | "ID: Title" format |
| `--url` | "ID: URL" format (sources only) |
| `--full` | All columns/details |

## Common Patterns

### Pattern 1: Research → Podcast Pipeline

```bash
nlm notebook create "AI Research 2026"   # Capture ID
nlm alias set ai <notebook-id>
nlm research start "agentic AI trends" --notebook-id ai --mode deep
nlm research status ai --max-wait 300    # Wait up to 5 min
nlm research import ai <task-id>         # Import all sources
nlm audio create ai --format deep_dive --confirm
nlm studio status ai                     # Check generation progress
```

### Pattern 2: Quick Content Ingestion

```bash
nlm source add <id> --url "https://example1.com"
nlm source add <id> --url "https://example2.com"
nlm source add <id> --text "My notes..." --title "Notes"
nlm source list <id>
```

### Pattern 3: Study Materials Generation

```bash
nlm report create <id> --format "Study Guide" --confirm
nlm quiz create <id> --count 10 --difficulty 3 --confirm
nlm flashcards create <id> --difficulty medium --confirm
```

### Pattern 4: Drive Document Workflow

```bash
nlm source add <id> --drive 1KQH3eW0hMBp7WK... --type slides
# ... time passes, document is edited ...
nlm source stale <id>                    # Check freshness
nlm source sync <id> --confirm           # Sync if stale
```

## Error Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Cookies have expired" | Session timeout | `nlm login` |
| "authentication may have expired" | Session timeout | `nlm login` |
| "Notebook not found" | Invalid ID | `nlm notebook list` |
| "Source not found" | Invalid ID | `nlm source list <nb-id>` |
| "Rate limit exceeded" | Too many calls | Wait 30s, retry |
| "Research already in progress" | Pending research | Use `--force` or import first |
| Chrome doesn't launch | Port conflict | Close Chrome, retry |

## Rate Limiting

Wait between operations to avoid rate limits:
- Source operations: 2 seconds
- Content generation: 5 seconds
- Research operations: 2 seconds
- Query operations: 2 seconds

## Advanced Reference

For detailed information, see:
- **[references/command_reference.md](references/command_reference.md)**: Complete command signatures
- **[references/troubleshooting.md](references/troubleshooting.md)**: Detailed error handling
- **[references/workflows.md](references/workflows.md)**: End-to-end task sequences
