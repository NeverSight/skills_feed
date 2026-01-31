---
name: update-context
description: "Capture conversation context AND git changes to create comprehensive markdown documentation. Analyzes both discussed reasoning and actual code changes (via git diff) for accurate, meaningful documentation of features, bugs, architecture, and refactors."
argument-hint: "[context-type] [optional-name]"
disable-model-invocation: false
allowed-tools: "Write, Read, Glob, Bash, Edit"
---

# Update Context Skill

Maintain persistent context documentation by capturing conversation insights and organizing them into markdown files.

## When to Use This Skill

Use this skill to document:
- **Features**: New feature implementations and requirements
- **Bugs**: Bug analysis, root causes, and fixes
- **Architecture**: Architectural decisions and design patterns
- **Refactors**: Refactoring efforts and outcomes
- **Performance**: Performance improvements and optimizations
- **Security**: Security considerations and implementations

## How Documentation Is Used

**Important**: Context documentation creates a **searchable knowledge base**, not automatic context loading.

- Documentation must be **explicitly referenced** in future sessions (e.g., "read the auth context doc")
- Primary value is for **human developers** to understand past decisions and implementations
- AI agents can read these docs **when asked**, but don't auto-load them at session start
- Best used as **Architectural Decision Records (ADRs)** with code evidence
- Searchable via grep/glob for finding relevant past context

## Usage

### Automatic Invocation
During technical conversations, I may proactively use this skill to capture important context, decisions, and implementation details.

### Manual Invocation
```bash
# Document a feature
/update-context feature my-feature-name

# Document a bug analysis
/update-context bug issue-123

# Document an architectural decision
/update-context architecture auth-system-redesign

# Document a refactor
/update-context refactor state-management

# Document a performance improvement
/update-context performance query-optimization

# Document a security implementation
/update-context security rate-limiting
```

## Documentation Structure

The skill creates a two-tier documentation system:

### 1. Index at Project Root (CLAUDE.md)

A lightweight index file at the project root provides quick scanning of all context:

```
CLAUDE.md   # Minimal index with brief summaries + links
```

**Purpose**: Quick overview without loading full documentation. Contains:
- Brief 1-2 sentence summaries
- Links to detailed documentation
- Organized by type (Features, Bugs, Architecture, etc.)
- Alphabetically sorted within each type

**What gets modified**: Only the 6 context type sections (Features, Bugs, Architecture, Refactors, Performance, Security). All other content in CLAUDE.md is preserved.

See [examples/CLAUDE.md.example](examples/CLAUDE.md.example) for a complete example.

### 2. Detailed Documentation (Agent-Specific Directories)

Full context documentation is organized in agent-specific directories. The skill automatically detects your AI coding agent and uses the appropriate directory:

- **Claude Code**: `.claude/context-docs/`
- **Cursor**: `.cursor/context-docs/`
- **Aider**: `.aider/context-docs/`
- **GitHub Copilot**: `.github/copilot/context-docs/`
- **Generic/Unknown**: `.ai-context/`

You can also specify a custom directory using the `--output` flag.

```
<context-dir>/
├── features/
│   └── [feature-name].md
├── bugs/
│   └── [bug-id].md
├── architecture/
│   └── [decision-name].md
├── refactors/
│   └── [description].md
├── performance/
│   └── [optimization-name].md
└── security/
    └── [security-feature].md
```

## What Gets Captured

Each documentation file includes insights from both conversation and code changes:

- **Overview**: Clear description of what this is about (from conversation + git analysis)
- **Problem/Goal**: What are we solving? (from conversation context)
- **Solution/Implementation**: How did we solve it? (from conversation + actual code changes in git diff)
- **Key Decisions**: Why did we choose this approach? (from conversation)
- **Code Changes**: Specific files modified and key changes made (from git diff analysis)
- **Tradeoffs**: Benefits and costs (from conversation + code complexity analysis)
- **Related Files**: Which files are affected? (from git diff + conversation)
- **Testing**: Verification approach (from conversation + test file changes)
- **Status**: Current state (In Progress, Complete, etc.)
- **Date**: When was this documented?

The skill intelligently combines:
- **Conversation insights**: "Why" decisions were made, architectural reasoning
- **Code changes**: "What" actually changed, implementation details from git diff

## Template Structure

```markdown
# [Title]

**Type**: Feature | Bug | Architecture | Refactor | Performance | Security
**Date**: YYYY-MM-DD
**Status**: In Progress | Complete | Blocked | Review

## Overview
[Clear description from conversation + git analysis]

## Problem/Goal
[What are we solving?]

## Solution/Implementation
[How did we solve it? - from conversation]

## Code Changes
[If git analysis was performed, detailed breakdown of actual changes:]
- **Files Modified**: List of changed files with change summary
- **Key Changes**: Important code additions, modifications, or refactors
- **Patterns Used**: Design patterns or architectural approaches visible in code
- **Dependencies**: New packages or libraries added

## Key Decisions
- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Tradeoffs
- **Pros**: [Benefits]
- **Cons**: [Costs/Downsides]

## Related Files
- `path/to/file1.ts` - [Purpose and changes made]
- `path/to/file2.tsx` - [Purpose and changes made]

## Testing / Verification
- [ ] Unit tests
- [ ] E2E tests
- [ ] Manual testing
[Include test file changes if present in git diff]

## Notes
[Additional context, gotchas, future improvements]
```

See [template.md](template.md) for the full detailed template.

## Agent Detection & Configuration

The skill automatically detects your AI coding agent and creates documentation in the appropriate location:

### Auto-Detection Process

The skill checks for the following in order:

1. **Custom output flag**: `--output /path/to/docs` (highest priority)
2. **Environment variable**: `AI_CONTEXT_DIR` environment variable
3. **Agent-specific directories**:
   - `.claude/` exists → use `.claude/context-docs/`
   - `.cursor/` exists → use `.cursor/context-docs/`
   - `.aider/` exists → use `.aider/context-docs/`
   - `.github/copilot/` exists → use `.github/copilot/context-docs/`
4. **Generic fallback**: `.ai-context/` (works with any agent)

### Custom Output Directory

```bash
# Use a custom directory for documentation
/update-context feature my-feature --output ./docs/ai-context

# Use environment variable (set in your shell config)
export AI_CONTEXT_DIR=".ai-docs"
/update-context feature my-feature
```

### Multi-Agent Projects

If you work with multiple AI agents on the same project, the skill will create separate context directories for each agent. This allows each agent to maintain its own context while keeping documentation organized.

Alternatively, set `AI_CONTEXT_DIR` to use a shared directory across all agents:

```bash
export AI_CONTEXT_DIR=".ai-context"
```

## Implementation Steps

When this skill is invoked, I will:

1. **Parse arguments**: Extract context type ($0), optional name ($1), and optional flags (e.g., `--output`)
2. **Detect AI agent and determine output directory**:
   - Check for `--output` flag for custom directory
   - If not specified, auto-detect the AI agent:
     - Check for `.claude/` directory → use `.claude/context-docs/`
     - Check for `.cursor/` directory → use `.cursor/context-docs/`
     - Check for `.aider/` directory → use `.aider/context-docs/`
     - Check for `.github/copilot/` directory → use `.github/copilot/context-docs/`
     - Check environment variable `AI_CONTEXT_DIR` → use that value
     - Fallback to `.ai-context/` (generic, agent-agnostic)
   - Store the determined directory path for use in all subsequent steps
3. **Check git changes**: Run `git status` to see if there are any changes
4. **Ask user preference**: If changes exist, ask whether to analyze:
   - **Staged changes only** (`git diff --cached`) - cleaner, focused on what's ready to commit
   - **All changes** (`git diff HEAD`) - includes both staged and unstaged changes
   - **Skip git analysis** - use conversation context only
5. **Analyze git changes**: If user wants git analysis, run the appropriate git diff command and analyze:
   - Files modified
   - Nature of changes (added features, bug fixes, refactors)
   - Key code changes and patterns
6. **Ensure directory exists**: Create `<detected-context-dir>/[type]/` if needed (e.g., `.cursor/context-docs/features/`)
7. **Generate filename**: Use provided name or derive from conversation/git changes
8. **Check for existing file**: Read existing content if updating
9. **Capture context**: Extract relevant information from:
   - Conversation history
   - Git diff analysis (if available)
   - File changes and patterns
10. **Structure content**: Use template format for consistency, integrating both conversation and code change insights
11. **Write/update file**: Save to appropriate location
12. **Update CLAUDE.md index** (PRESERVE ALL OTHER CONTENT):
   - Determine project root (parent of .git directory or current directory)
   - Check if CLAUDE.md exists at project root
   - If CLAUDE.md doesn't exist, create it using the template from `claude-md-template.md`
   - If CLAUDE.md exists, read and parse it:
     - Identify the 6 context type sections: `## Features`, `## Bugs`, `## Architecture`, `## Refactors`, `## Performance`, `## Security`
     - Extract ONLY list entries (lines starting with `- **`) from these sections
     - **PRESERVE ALL other content** (headers, explanatory text, custom sections, user notes)
     - Store content boundaries (what comes before, between, and after each section)
   - Extract brief summary from the generated context file:
     - Read the Overview section (first 1-2 sentences, max ~100 words)
     - This will be used as the indented description under the entry
   - Calculate relative path from project root to the context file:
     - Example for Claude Code: `.claude/context-docs/features/shopping-cart.md`
     - Example for Cursor: `.cursor/context-docs/features/shopping-cart.md`
     - Use forward slashes (/) even on Windows for cross-platform compatibility
   - Create/update entry:
     - Format: `- **[Title]** (YYYY-MM-DD) - [Details](relative/path/to/file.md)`
     - Next line (indented with 2 spaces): Brief summary from Overview section
     - Title: From context file header (remove markdown # symbols)
     - Date: From context file date field
   - Find or create the appropriate type section:
     - If section doesn't exist, create it in standard order: Features, Bugs, Architecture, Refactors, Performance, Security
     - Preserve all surrounding content
   - Update context entries:
     - Check if an entry with the same title already exists in that section
     - If yes, replace it (update scenario - don't duplicate)
     - If no, add as new entry
     - Sort all entries alphabetically by title within the section
   - Reconstruct CLAUDE.md:
     - Preserve all content before the first context section
     - Write each context type section with updated entries
     - Preserve all content between sections
     - Preserve all content after the last context section
   - Write updated CLAUDE.md back to project root
   - **CRITICAL**: Only context list entries are modified, everything else stays intact
13. **Confirm**: Report back with paths to both the detailed context file and CLAUDE.md (mention which agent directory was used)

## Git Changes Analysis

When invoked, the skill will:

1. **Check for changes**: Run `git status` to see if there are uncommitted changes
2. **Prompt for preference**: If changes exist, ask you to choose:
   - **Staged changes only**: Analyzes `git diff --cached` - Best for documenting specific commits or focused changes
   - **All changes**: Analyzes `git diff HEAD` - Best for comprehensive session documentation
   - **Skip git analysis**: Uses conversation context only - Best when working without git or discussing future plans

3. **Analyze the diff**: Extract and understand:
   - Files modified and their purposes
   - Functions/components added or changed
   - Patterns and architectural decisions visible in code
   - Test coverage changes
   - Configuration changes

This dual-context approach ensures documentation is both accurate (based on actual code) and meaningful (based on discussed reasoning).

## Arguments

- **$0** (required): Context type
  - Values: `feature`, `bug`, `architecture`, `refactor`, `performance`, `security`
- **$1** (optional): Name/identifier for the documentation file
  - If not provided, I'll derive a name from the conversation context
  - Examples: `shopping-cart`, `issue-123`, `auth-redesign`
- **--output** (optional): Custom output directory path
  - Example: `--output ./docs/context` or `--output .custom/ai-docs`
  - Overrides auto-detection

If no arguments are provided, I'll ask you what type of context to document.

## Examples

### Example 1: Document a Feature with Git Changes
```
/update-context feature data-grid-qis
```
I will:
1. Detect AI agent (e.g., finds `.cursor/` directory → will use `.cursor/context-docs/`)
2. Check git status (finds uncommitted changes)
3. Ask: "Would you like me to analyze: (1) Staged changes only, (2) All changes, or (3) Skip git analysis?"
4. User selects "Staged changes only"
5. Run `git diff --cached` and analyze the actual code changes
6. Combine conversation context + git analysis
7. Create: `.cursor/context-docs/features/data-grid-qis.md` with detailed implementation info

### Example 2: Document a Bug Fix
```
/update-context bug connection-modal-crash
```
With git changes, the documentation will include:
- Conversation: Root cause analysis and reasoning
- Git diff: Exact lines changed, files affected, fix implementation
- Result: Complete picture of the bug and its solution

### Example 3: Document Architecture Decision
```
/update-context architecture websocket-communication
```
Auto-detects agent directory and creates documentation (e.g., `.aider/context-docs/architecture/websocket-communication.md` for Aider).
Includes discussion of alternatives + actual implementation patterns from code changes.

### Example 4: Update Existing Documentation
If the file already exists, I'll read it first and merge/update the content with new information from the conversation and any new git changes.

### Example 5: Document Without Git (Planning Phase)
```
/update-context feature new-auth-system
```
If no git changes exist yet, or user selects "Skip git analysis", documentation will be based purely on conversation context - perfect for planning and design discussions.

### Example 6: Custom Output Directory
```
/update-context refactor code-cleanup --output ./team-docs/ai-context
```
Creates: `./team-docs/ai-context/refactors/code-cleanup.md`
Useful for shared team documentation or custom project structures.

### Example 7: Multi-Agent Project
In a project using both Claude and Cursor:
- Claude: Creates docs in `.claude/context-docs/`
- Cursor: Creates docs in `.cursor/context-docs/`

Each agent maintains its own context history. To share context across agents, set:
```bash
export AI_CONTEXT_DIR=".shared-context"
```

### Example 8: CLAUDE.md Index Integration

After running:
```bash
/update-context feature shopping-cart
```

Two files are created/updated:

1. **Detailed documentation**: `.claude/context-docs/features/shopping-cart.md`
   - Full 14-section documentation
   - Complete code changes, decisions, testing details

2. **Index entry in CLAUDE.md** (at project root):
   ```markdown
   ## Features

   - **Shopping Cart** (2026-01-15) - [Details](.claude/context-docs/features/shopping-cart.md)
     Real-time shopping cart with WebSocket synchronization across multiple devices
   ```

When you run the skill again to update existing context:
```bash
/update-context feature shopping-cart
```

Both files are updated:
- Detailed doc: Merged with new information
- CLAUDE.md: Entry updated with new date and summary (not duplicated)

**Benefit**: AI agents can quickly scan CLAUDE.md to find relevant context, then read detailed docs only when needed. Users can also add custom content to CLAUDE.md (notes, explanations, etc.) and it will be completely preserved - only the context list entries are modified.

## Tips

- **Use descriptive names**: Choose clear, searchable names for your documentation
- **Document as you go**: Invoke this skill during or right after implementation discussions
- **Stage your changes first**: For cleanest documentation, stage (`git add`) the files you want to document before running the skill
- **Use staged-only for commits**: When preparing a commit, use "staged changes only" to document exactly what's being committed
- **Use all changes for sessions**: When documenting a full work session with multiple changes, use "all changes"
- **Reference explicitly**: In future sessions, say "read .claude/context-docs/features/X.md" to load context
- **Searchable history**: Use grep/glob to find relevant docs (e.g., "grep 'authentication' context-docs/")
- **Team onboarding**: Primary value is for human developers to understand past decisions
- **Update when needed**: Re-run the skill with the same name to append new findings
- **Commit to git**: Include your context directory (e.g., `.claude/context-docs/` or `.ai-context/`) in your repository for team visibility
- **Works with or without git**: The skill adapts - use it for planning (no git) or post-implementation (with git)
- **Share across agents**: Set `AI_CONTEXT_DIR` environment variable to use a shared context directory for multiple AI agents
- **Custom locations**: Use `--output` flag to specify exactly where documentation should be saved
- **Multi-agent workflows**: Each agent can maintain its own context, or share a common directory - your choice!
- **Quick context discovery**: Check CLAUDE.md first to find relevant documentation without loading everything
- **Minimal index**: CLAUDE.md stays lightweight - only brief summaries, not full details
- **AI agent scanning**: AI agents can read CLAUDE.md to understand project history at a glance
- **Link to details**: Always use the links in CLAUDE.md to read full detailed documentation
- **Preserve your notes**: Feel free to add custom content to CLAUDE.md - only the context list entries are modified by the skill

## Integration with Development Workflow

This skill complements your existing workflow by combining conversation insights with actual code changes:

**Planning Phase** (no git changes):
- During architecture discussions → Record decisions and alternatives
- Before implementing → Document the planned approach

**Implementation Phase** (with git changes):
- While implementing → Stage changes and document incrementally
- After implementing a feature → Document with actual code analysis
- After fixing a bug → Capture root cause + exact fix from git diff
- After refactoring → Document the changes with before/after code comparison
- After performance improvements → Note the results with actual code changes

**Review Phase**:
- Before committing → Document staged changes for commit context
- After completing work session → Document all changes made

The documentation becomes a living record of your project's evolution, grounded in both reasoning (conversation) and reality (code changes).
