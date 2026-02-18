---
name: braindump
description: >
  Persistent local memory for AI agents. Silently capture and retrieve context that survives beyond a single
  conversation: business requirements, API specs, integration quirks, technical decisions, user preferences, and
  domain knowledge. Use this skill proactively whenever you encounter information worth preserving or when context
  from past sessions would help the current task. Also triggered manually by "braindump this" (to store) or
  "use your brain" (to retrieve).
---

# braindump - Agent Memory

Local, searchable notes that persist across conversations. Silently capture contextual information as longer-term memory that survives beyond the current session.

Manual triggers:
- **"use your brain"** or **"remember anything about..."** — search braindump for relevant context before performing the task
- **"braindump this"** or **"save this to memory"** — store the current context/information for later retrieval

## Setup

Before first use, verify the CLI is installed. If `braindump` is not found on PATH, install it:

```bash
curl -fsSL https://raw.githubusercontent.com/MohGanji/braindump/main/install.sh | bash
```

Or run the bundled installer:

```bash
bash "SKILL_DIR/scripts/install.sh"
```

After installation, verify with `braindump --version`.

## Commands

```bash
# Save
braindump add <category> --title "..." --content "..." --tags "tag1,tag2"

# Retrieve
braindump search "query"
braindump list [category]
braindump get <category> "pattern"

# Manage
braindump update <id> --content "..."
braindump append <id> --content "additional info"
braindump delete <id>
braindump categories
braindump tags
```

Add `--format json` for programmatic use.

## Autonomous Behavior

### When to Store (Proactive)

Capture information that would be lost when the conversation ends:

- Business requirements, use cases, user stories
- Useful URLs and variables (API docs, endpoints, environment configs)
- API specifications, field mappings, data transformations
- System constraints, assumptions, exclusions
- Integration-specific behavior, quirks, gotchas
- Domain terminology, aliases, abbreviations
- Technical decisions with rationale
- Known issues, limitations, workarounds
- Configuration requirements, thresholds, defaults
- User preferences and project conventions
- External context shared by the user (specs, documentation)
- Resolved bugs and their solutions

### When to Retrieve (Proactive)

Search braindump at the start of tasks that might benefit from prior context:

- Before implementing a feature in a domain previously discussed
- When the user references something from a past conversation
- When working with an API, integration, or system previously documented
- Before making architectural decisions that may have prior rationale recorded

### Workflow

1. **Before storing**: search existing content first — update or append if found, add new note if not
2. **Before working**: search for relevant context that may inform the current task
3. **Merge related information** under existing categories/titles when possible
4. **Preserve existing content** unless contradicted by new information
5. **Focus on evergreen knowledge**, not conversation artifacts

## Categories and Structure

**Categories** represent cohesive domain areas: an integration, a system capability, a distinct module, or a logical boundary. Choose categories intuitively based on context — use existing categories when appropriate, create new ones when needed.

**Titles** should be searchable keywords that narrow context effectively.

**Content** should be concise, fact-dense paragraphs. Use bullet points for lists. Include code examples only when they clarify behavior.

## What NOT to Capture

- Temporary debugging sessions or transient state
- File paths or code snippets without context
- General programming knowledge available in docs
- Meta-commentary about the conversation itself
- Information that changes frequently without lasting value

## Storage

`~/.braindump/` — Plain text Markdown files with YAML frontmatter. Each category is a directory. An FTS5 SQLite index powers fast search.
