---
name: memory
description: Persistent knowledge storage using basic-memory CLI. Use to save notes, search memories semantically, and build context for topics across sessions.
---

# Memory - Persistent Knowledge Storage

Store and retrieve knowledge across sessions using semantic search.

## Prerequisites

Install basic-memory:
```bash
pip install basic-memory
```

## CLI Reference

### Write a Note
```bash
# Basic note
basic-memory tool write-note --title "Note Title" --content "Note content in markdown"

# With tags
basic-memory tool write-note --title "React Patterns" --content "# Content here" --tags "react,patterns,frontend"

# To specific folder
basic-memory tool write-note --title "Meeting Notes" --content "# Notes" --folder "meetings"

# With specific project
basic-memory tool write-note --title "Project Notes" --content "# Notes" --project myproject
```

### Read a Note
```bash
# By identifier/permalink
basic-memory tool read-note "note-title"

# From specific project
basic-memory tool read-note "note-title" --project myproject
```

### Search Memories
```bash
# Semantic search (query is positional)
basic-memory tool search-notes "your search query"

# Limit results
basic-memory tool search-notes "react hooks" --page-size 10

# Search by permalink
basic-memory tool search-notes "pattern" --permalink

# Search by title
basic-memory tool search-notes "meeting" --title

# Filter by date
basic-memory tool search-notes "feature" --after_date "7d"

# With specific project
basic-memory tool search-notes "authentication" --project myproject
```

### Build Context for a Topic
```bash
# Get related notes for a URL/topic (URL is positional)
basic-memory tool build-context "memory://topic/authentication"

# With depth and timeframe
basic-memory tool build-context "memory://note/my-note" --depth 2 --timeframe 30d

# With specific project
basic-memory tool build-context "memory://topic/api" --project myproject
```

### List Recent Activity
```bash
# Default (depth 1, 7 days)
basic-memory tool recent-activity

# With depth
basic-memory tool recent-activity --depth 3

# With timeframe
basic-memory tool recent-activity --timeframe 30d

# Combined
basic-memory tool recent-activity --depth 3 --timeframe 14d
```

### Continue Conversation
```bash
# Get prompt to continue previous work
basic-memory tool continue-conversation "previous topic or context"
```

### Sync Database
```bash
basic-memory sync
```

### Check Status
```bash
basic-memory status
```

## Note Format

Notes are stored as markdown with YAML frontmatter:

```markdown
---
title: My Note
tags: [tag1, tag2]
created: 2024-01-15
---

# My Note

Content here in markdown format.

## Sections

More content...
```

## Workflow Patterns

### Save Learning
When you discover something useful:
```bash
basic-memory tool write-note \
  --title "TypeScript Utility Types" \
  --content "# Utility Types\n\n- Partial<T> - Makes all properties optional\n- Required<T> - Makes all properties required\n- Pick<T, K> - Picks specific properties" \
  --tags "typescript,types,reference"
```

### Save Decision
When making an architectural decision:
```bash
basic-memory tool write-note \
  --title "Auth Strategy Decision" \
  --content "# Decision: Use JWT for API auth\n\n## Context\n...\n\n## Decision\n...\n\n## Consequences\n..." \
  --tags "architecture,auth,decision" \
  --folder "decisions"
```

### Retrieve Context
Before starting related work:
```bash
# Search for relevant notes
basic-memory tool search-notes "authentication jwt tokens"

# Or build comprehensive context
basic-memory tool build-context "memory://topic/api-authentication"
```

### Review Recent Work
```bash
basic-memory tool recent-activity --depth 5 --timeframe 7d
```

## Use Cases

### Personal Wiki
- Store code snippets and patterns
- Document project decisions
- Keep reference material

### Learning Log
- Record things you learn
- Tag by topic for later retrieval
- Build knowledge over time

### Project Context
- Save project-specific knowledge
- Retrieve relevant context at session start
- Share knowledge across sessions

## Best Practices

1. **Use meaningful titles** - They become permalinks
2. **Add tags** - Improves search and organization
3. **Use markdown** - Full markdown support in content
4. **Organize with folders** - Group related notes
5. **Search before writing** - Check if knowledge already exists
6. **Keep notes focused** - One topic per note
7. **Update, don't duplicate** - Revise existing notes

## Integration Pattern

### Session Start
```bash
# Get context for today's work
basic-memory tool build-context "memory://topic/feature-youre-building"
```

### During Work
```bash
# Save discoveries
basic-memory tool write-note --title "Discovery Title" --content "What I learned"
```

### Session End
```bash
# Sync to ensure persistence
basic-memory sync
```
