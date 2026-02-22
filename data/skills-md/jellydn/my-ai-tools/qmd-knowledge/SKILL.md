---
name: qmd-knowledge
description: Project-specific knowledge management system using qmd MCP server. Captures learnings, issue notes, and conventions in a searchable knowledge base.
license: MIT
compatibility: opencode, claude, amp, codex, gemini
hint: Use when recording or retrieving project knowledge, learnings, and issue notes
user-invocable: true
metadata:
  audience: all
  workflow: knowledge-management
---

## What I do

- Record and retrieve project learnings and insights
- Capture issue-specific notes and resolutions
- Build a growing, AI-searchable knowledge base
- Provide context about project architecture and decisions

## When to use me

Use this skill when you need to:

- **Record learnings**: Capture new insights, patterns, or best practices discovered during development
- **Track issues**: Add notes to ongoing or resolved issues
- **Query knowledge**: Search for previous decisions, learnings, or solutions
- **Maintain context**: Build institutional memory for the project

## How it works

This skill provides a unified knowledge management system. You install the skill once, and it manages knowledge across all your projects using qmd collections:

```
# The qmd-knowledge skill (installed to your AI tool's skills directory)
# Location varies by tool: ~/.config/opencode/skill/, ~/.claude/skills/, or ~/.config/amp/skills/
├── SKILL.md              # This file - the skill definition
├── scripts/              # Executable scripts
│   └── record.sh         # Record learnings/issues/notes
└── references/           # Example structure and READMEs

# Project knowledge storage (managed by the skill)
~/.ai-knowledges/
├── <project-name>/       # Collection for your project
│   ├── learnings/
│   └── issues/
└── another-project/      # Collection for another project
    ├── learnings/
    └── issues/
```

The `qmd` MCP server provides AI-powered search across all stored knowledge, allowing your AI assistant to autonomously query and update the knowledge base.

## Available scripts

### Recording knowledge

**Important**: Before recording knowledge, ensure qmd is installed and your project collection is set up. Run a preflight check:

```bash
# Verify qmd is installed
command -v qmd || echo "Install qmd: bun install -g https://github.com/tobi/qmd"

# Verify your project collection exists (replace my-project with your actual project name)
qmd collection list | grep my-project
```

```bash
# Record a learning (use the skill's script)
$SKILL_PATH/scripts/record.sh learning "qmd MCP integration"

# Add a note to an issue
$SKILL_PATH/scripts/record.sh issue 123 "Fixed by updating dependencies"

# Record a general note
$SKILL_PATH/scripts/record.sh note "Consider using agent skills for extensibility"
```

**After recording**: 
- The `record.sh` script automatically runs `qmd embed` to re-index the knowledge base
- This embedding step is **required** to make newly added content searchable for the next query
- If auto-embedding fails or you manually add/edit files, run `qmd embed` explicitly to update the index

### Querying knowledge

Use the qmd MCP server tools directly from Claude or OpenCode:

```bash
# Fast keyword search
qmd search "MCP servers" -c <project-name>

# Semantic search with AI embeddings
qmd vsearch "how to configure MCP"

# Hybrid search with reranking (best quality)
qmd query "MCP server configuration"

# Get specific document
qmd get "references/learnings/2024-01-26-qmd-integration.md"

# Search with minimum score filter
qmd search "API" --all --files --min-score 0.3 -c <project-name>
```

## Setup

**Preflight check**: Before starting, verify you have the required tools:

```bash
# Check for bun or node
command -v bun || command -v node || echo "Install bun or node.js first"

# Verify git is available (for project detection)
command -v git || echo "Install git for automatic project name detection"
```

1. **Install qmd**:
   ```bash
   bun install -g https://github.com/tobi/qmd
   ```

2. **Install the skill**:
   ```bash
   # The skill is installed to your AI tool's skills directory:
   # - OpenCode: ~/.config/opencode/skill/qmd-knowledge/
   # - Claude Code: ~/.claude/skills/qmd-knowledge/
   # - Amp: ~/.config/amp/skills/qmd-knowledge/
   ```

3. **Configure MCP server** (see installation docs for Claude/OpenCode/Amp)

4. **Create a knowledge collection for your project**:
   ```bash
   # The skill's record.sh script will auto-detect the project name when executed.
   # For manual setup, use your desired project name consistently in the commands below.
   # Optional: export QMD_PROJECT=<project-name> to override auto-detection
   
   # Create storage directory for your project (replace <project-name> with your project)
   mkdir -p ~/.ai-knowledges/<project-name>/learnings
   mkdir -p ~/.ai-knowledges/<project-name>/issues
   
   # Add qmd collection
   qmd collection add ~/.ai-knowledges/<project-name> --name <project-name>
   qmd context add qmd://<project-name> "Knowledge base for <project-name> project: learnings, issue notes, and conventions"
   
   # Generate embeddings for AI-powered search
   qmd embed
   ```

## Knowledge structure

- `references/learnings/`: Time-stamped markdown files with project insights
  - Format: `YYYY-MM-DD-topic-slug.md`
  - Contains learnings, patterns, architectural decisions

- `references/issues/`: Issue-specific notes and resolutions
  - Format: `<issue-id>.md`
  - Append-only log of notes related to specific issues

## Integration with qmd MCP server

The qmd MCP server allows Claude to:

- **Search knowledge**: Use natural language queries to find relevant context
- **Auto-update index**: Automatically reindex after adding new knowledge
- **Filter by project**: Use `--collection` flag to scope searches to specific projects

## Example workflow

1. **During development**, you discover something useful:
   > "I learned that qmd MCP server allows Claude to use tools autonomously."

2. **Claude recognizes the skill and executes**:
   ```bash
   $SKILL_PATH/scripts/record.sh learning "qmd MCP autonomous tool use"
   ```

3. **Later, you ask**:
   > "What did I learn about MCP servers?"

4. **Claude queries the knowledge base** using qmd MCP tools:
   ```bash
   qmd query --collection <project-name> "MCP servers"
   ```



## Project detection

The skill automatically detects your project name using the following priority:

1. **QMD_PROJECT environment variable** (highest priority)
   ```bash
   export QMD_PROJECT=my-project-name
   ```

2. **Git remote URL** (most reliable - extracts repo name from origin URL)
   - Example: `https://github.com/user/my-project.git` → `my-project`
   - Works even if the local folder has a different name

3. **Git repository folder name** (fallback)
   - Uses the name of the git repository root directory
   - Works when you're anywhere inside a git repository
   - Note: May not match the actual repo name if the folder was renamed

4. **Current directory name** (last resort)
   - Uses the name of your current working directory
   - Used when not in a git repository

This means you can use the skill in any project without hardcoding project names. The knowledge base will be stored at `~/.ai-knowledges/<detected-project-name>/`.

**Important**: The script prioritizes the git remote URL to ensure consistent project naming even if local folders are renamed or in non-standard locations (e.g., dated folders like `2026-01-08-my-ai-tools.qmd-skill`).

## 📋 Best Practices

### 🎨 Session Wrap-up

At the end of a work session, consider prompting the user about key learnings:

> "What were the main discoveries or decisions from this session? Would you like me to record any learnings?"

### 🎨 Pattern Detection

Be attentive to phrases that indicate valuable knowledge capture opportunities:

- "I discovered that..."
- "I learned that..."
- "The solution was..."
- "The key insight is..."
- "Don't forget to..."
- "Make sure to..."

When you detect these patterns, suggest recording:
> "That sounds like a useful learning. Would you like me to record it?"

### 🎨 Auto-Index Updates

The record script automatically runs `qmd embed` after each write, ensuring the knowledge base is searchable immediately. This re-indexing step is **required** to make new content available for search queries.

**Important**: If you manually create or edit knowledge files (outside of the record script), you must run `qmd embed` manually to update the search index:

```bash
# Manual re-indexing after direct file edits
qmd embed
```

Without re-indexing, newly added or modified content will not appear in search results.
