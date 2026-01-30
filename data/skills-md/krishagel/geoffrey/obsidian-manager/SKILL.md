---
name: obsidian-manager
description: Manage Obsidian vault for persistent knowledge storage, search, and retrieval
triggers:
  - "save to obsidian"
  - "search my notes"
  - "find in vault"
  - "check my readwise"
  - "search readwise"
  - "search snipd"
  - "check my highlights"
  - "create note"
  - "add to obsidian"
  - "what did I read about"
  - "what podcasts mentioned"
allowed-tools: Read, Write, Bash, Glob, Grep
version: 0.1.0
---

# Obsidian Manager Skill

Manage the user's Obsidian vault as a persistent second brain. Read existing knowledge, write new content, and search across years of highlights and notes.

## Vault Configuration

**Path:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal_Notes/`

**Write Mode:** Auto-create new files, confirm before updating existing files.

## Vault Structure

```
Personal_Notes/
├── Geoffrey/              # Geoffrey-generated content
│   ├── Mission Control.md # Central dashboard (Dataview queries)
│   ├── Scheduled Tasks.md # Scheduler dashboard
│   ├── Research/          # Research task outputs
│   │   ├── Daily AI Briefings/  # Daily automated research
│   │   ├── {Project}/     # Other research projects
│   │   └── attachments/   # Research images
│   ├── Reports/           # Generated reports and artifacts
│   │   ├── PSD/           # Peninsula School District reports
│   │   │   ├── Discipline/    # Discipline reports and infographics
│   │   │   ├── Enrollment/    # Enrollment reports
│   │   │   ├── Tech Support/  # Tech support dashboards
│   │   │   └── {topic}/       # Other PSD topics
│   │   ├── HRG/           # Hat Rack Group (consulting LLC) reports
│   │   │   └── {topic}/       # HRG topics
│   │   ├── Personal/      # Personal reports
│   │   │   └── {topic}/       # Personal topics
│   │   └── {org}/         # Other organizations as needed
│   ├── Daily-Logs/        # Session summaries (YYYY-MM-DD.md)
│   ├── Learnings/         # Extracted patterns (YYYY-MM-DD-topic.md)
│   └── Decisions/         # Major decisions with rationale (YYYY-MM-DD-topic.md)
├── Meetings/              # Meeting notes (YYYY-MM-DD format)
├── People/                # Contact profiles with metadata
├── Readwise/              # Synced highlights (368 articles, 34 books)
│   ├── Articles/
│   ├── Books/
│   ├── Podcasts/
│   └── Tweets/
├── Snipd/                 # Podcast highlights (58+ episodes)
│   └── Data/              # Podcast folders > episodes
└── Templates/             # Note templates
```

**CRITICAL:** See CLAUDE.md "Obsidian Organizational Rules" section for:
- Strict folder structure requirements
- File naming conventions
- Routing rules by content type
- Validation checklist before writing

Always validate folder placement before writing any files to Geoffrey folder.

## Scripts

All scripts use Python via `uv run` with inline dependencies.

### Search Scripts

#### search.py - General Vault Search
```bash
uv run scripts/search.py "query" [folder] [--limit N]
```

Search across the vault for keyword matches. Returns file paths and matching excerpts.

**Examples:**
```bash
# Search entire vault
uv run scripts/search.py "prompt engineering"

# Search specific folder
uv run scripts/search.py "leadership" People

# Limit results
uv run scripts/search.py "AI" Readwise/Articles --limit 10
```

#### search-readwise.py - Search Highlights
```bash
uv run scripts/search-readwise.py "query" [--author "name"] [--category articles|books|podcasts]
```

Search Readwise highlights by topic, author, or category.

**Examples:**
```bash
# Search by topic
uv run scripts/search-readwise.py "second brain"

# Search specific author
uv run scripts/search-readwise.py "AI" --author "Andrej Karpathy"

# Search books only
uv run scripts/search-readwise.py "habits" --category books
```

#### search-snipd.py - Search Podcast Transcripts
```bash
uv run scripts/search-snipd.py "query" [--show "podcast name"]
```

Search Snipd podcast transcripts and snips.

**Examples:**
```bash
# Search all podcasts
uv run scripts/search-snipd.py "machine learning"

# Search specific show
uv run scripts/search-snipd.py "leadership" --show "Huberman Lab"
```

### Creation Scripts

#### create-note.py - Create New Note
```bash
uv run scripts/create-note.py "title" "content" [--folder Geoffrey/Research] [--tags tag1,tag2] [--related "[[Note]]"]
```

Create a new note with proper frontmatter and optional backlinks.

**Examples:**
```bash
# Create research note
uv run scripts/create-note.py "AI Model Comparison" "Content here..." --folder Geoffrey/Research --tags research,ai

# Create with backlinks
uv run scripts/create-note.py "Meeting Notes" "Content..." --folder Meetings --related "[[John Smith]],[[Project Alpha]]"
```

#### open-in-obsidian.py - Open Note in Obsidian
```bash
uv run scripts/open-in-obsidian.py "path/to/note.md"
```

Opens the specified note in Obsidian using Actions URI.

## Content Routing

**CRITICAL:** When creating content, use these destinations. NEVER dump files directly into `Geoffrey/` - always use proper subfolders.

| Content Type | Folder | Naming Pattern |
|--------------|--------|----------------|
| Research results | `Geoffrey/Research/` | `YYYY-MM-DD-topic.md` |
| **Reports** | `Geoffrey/Reports/{org}/{topic}/` | Descriptive name with date |
| **Images/Infographics** | Same as parent report | `Descriptive Name YYYY-MM-DD.png` |
| Meeting notes | `Meetings/` | `Topic - YYYY-MM-DD.md` |
| Daily summaries | `Geoffrey/Daily-Logs/` | `YYYY-MM-DD.md` |
| Learnings | `Geoffrey/Learnings/` | `topic-slug.md` |
| Decisions | `Geoffrey/Decisions/` | `YYYY-MM-DD-decision.md` |
| Person updates | `People/` | Existing file name |

**Naming Rules:**
- All images/infographics MUST include date in filename
- Format: `Descriptive Name YYYY-MM-DD.png` or `Descriptive Name YYYY-MM-DD to YYYY-MM-DD.png` for date ranges
- Example: `Peninsula High School Discipline Report 2025-11-17 to 2025-11-20.png`

**Reports Folder Structure:**
Pattern: `Geoffrey/Reports/{organization}/{topic}/`

Organizations:
- **PSD** - Peninsula School District reports
  - `Geoffrey/Reports/PSD/Discipline/`
  - `Geoffrey/Reports/PSD/Enrollment/`
  - `Geoffrey/Reports/PSD/Attendance/`
  - `Geoffrey/Reports/PSD/{topic}/`

- **HRG** - Hat Rack Group (consulting LLC) reports
  - `Geoffrey/Reports/HRG/{topic}/`

- **Personal** - Personal reports
  - `Geoffrey/Reports/Personal/{topic}/`

- **{org}** - Other organizations as needed

## Frontmatter Standard

All Geoffrey-created notes should include:

```yaml
---
created: 2025-11-23
tags: [geoffrey, research]
source: geoffrey
related:
  - "[[Related Note 1]]"
  - "[[Related Note 2]]"
---
```

## When to Read from Vault

- **Before research tasks:** Check if user has relevant Readwise highlights or existing notes
- **When people mentioned:** Look up context in People folder
- **For meeting prep:** Find past meetings and related notes
- **For context:** Search Snipd transcripts for podcast discussions on topic

## When to Write to Vault

- **After research:** Save results to `Geoffrey/Research/`
- **Learned patterns:** Extract insights to `Geoffrey/Learnings/`
- **Major decisions:** Document with rationale in `Geoffrey/Decisions/`
- **Session summaries:** Optional daily logs to `Geoffrey/Daily-Logs/`

## Creating Backlinks

Always create backlinks to existing content:

1. **Search before creating:** Find related notes first
2. **Use wiki-links:** `[[Note Title]]` format
3. **Add to frontmatter:** List in `related:` field
4. **Reference sources:** Link to Readwise/Snipd sources when relevant

**Example:**
```markdown
Based on insights from [[Readwise/Articles/Building a Second Brain]],
and discussed in [[Snipd/Data/Huberman Lab/episode-123]],
the key pattern is...
```

## Readwise Content Format

Readwise notes have this structure:

```yaml
---
Author: "Author Name"
Full Title: "Article Title"
Category: #articles
Summary: "AI-generated summary"
---

## Highlights
- Highlight text with optional tags like [[topic]]
```

## Snipd Content Format

Snipd episodes have rich metadata:

```yaml
---
episode_show: "Podcast Name"
episode_publish_date: 2024-01-15
mentioned_books: ["Book 1", "Book 2"]
snips_count: 5
---

### Snip 1
**Timestamp:** 00:15:30
> Quote text here

**Transcript:** Full context...
```

## Actions URI Integration

Use Actions URI to interact with Obsidian app:

```bash
# Open a note
open "obsidian://actions-uri/note/open?vault=Personal_Notes&file=Geoffrey/Research/note.md"

# Create and open
open "obsidian://actions-uri/note/create?vault=Personal_Notes&file=path&content=..."
```

## Best Practices

1. **Search before creating:** Always check for existing content
2. **Link generously:** Create connections between notes
3. **Use consistent tags:** Match existing tag patterns
4. **Keep notes atomic:** One idea per note in Learnings
5. **Include sources:** Always cite Readwise/Snipd sources
6. **Respect existing structure:** Don't reorganize user's folders

## Output Format

When completing Obsidian operations:

```markdown
## Summary
What was done

## Files
- Created: `path/to/new.md`
- Updated: `path/to/existing.md` (if confirmed)

## Related Content Found
- [[Relevant Note 1]] - why it's relevant
- [[Relevant Note 2]] - why it's relevant

## Next Steps
- Recommendations if any
```
