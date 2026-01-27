---
name: codebase-exploration
description: Deep contextual grep for codebases. Expert at finding patterns, architectures, implementations, and answering "Where is X?", "Which file has Y?", and "Find code that does Z" questions. Use when exploring unfamiliar codebases, finding specific implementations, understanding code organization, discovering patterns across multiple files, or locating functionality in a project. Supports three thoroughness levels quick, medium, very thorough.
---

# Codebase Exploration

## Purpose

Specializes in systematic codebase exploration and discovery. Uses advanced search techniques, pattern recognition, and code analysis to quickly understand unfamiliar code, locate specific implementations, map architectural patterns, and answer location-based questions about code.

## When to Use

- Exploring an unfamiliar codebase for the first time
- Need to find where specific functionality is implemented
- Looking for examples of a pattern across the codebase
- Understanding how components interact
- Locating all usages of a particular API or pattern
- Mapping architectural organization
- Finding similar code across the project
- Questions like "Where is X?", "Which file has Y?", "Find code that does Z"

## Quick Start

**Invoke this skill when:**
- Exploring an unfamiliar codebase for the first time
- Need to find where specific functionality is implemented
- Looking for examples of a pattern across the codebase
- Understanding how components interact
- Questions like "Where is X?", "Which file has Y?", "Find code that does Z"

**Do NOT invoke when:**
- Debugging a known bug (use debugger-skill)
- Refactoring code (use refactoring-specialist-skill)
- Reviewing code quality (use code-reviewer-skill)
- Writing new code from scratch (use appropriate developer skill)

## Thoroughness Levels

**Quick** (Fast, broad strokes)
- File structure overview
- High-level pattern matching
- Directory organization
- Main entry points
- ~30 seconds

**Medium** (Balanced depth)
- Detailed file examination
- Cross-file pattern discovery
- Architectural mapping
- Common patterns analysis
- ~2-3 minutes

**Very Thorough** (Deep dive)
- Exhaustive code analysis
- Complex pattern matching
- Dependency tracing
- Edge case discovery
- ~5-10 minutes

## Decision Framework

### Search Strategy Selection

| Question Type | Search Strategy |
|--------------|----------------|
| "Where is user authentication?" | Search for auth keywords + login patterns |
| "How does data flow work?" | Find models, services, controllers pattern |
| "Which file handles X API?" | Search endpoints + route definitions |
| "Find all database queries" | Search ORM patterns, SQL keywords |
| "Locate error handling" | Find try-catch, error classes |

### Tool Selection

| Tool | Best For | Example |
|------|----------|---------|
| `grep/rg` | Text pattern matching | `rg "function handleAuth"` |
| `find/fd` | File name/path matching | `fd -e ts auth` |
| `ast-grep` | Code structure matching | `ast-grep --pattern "class $NAME"` |
| LSP tools | Symbol and reference finding | `lsp_find_references` |
| `git log` | Historical context | `git log --name-only` |

### Approach by Question Type

**"Where is X implemented?"**
1. Search for X by name: `rg "X|x"`
2. Search for related terms: `rg "related|terms"`
3. Check obvious locations: `ls src/X/`
4. Look in tests: `rg "X" tests/`

**"How does Y work?"**
1. Find Y's definition
2. Find Y's usage
3. Trace the flow
4. Understand dependencies

**"Which files use Z?"**
1. Search for imports of Z
2. Use LSP find-references
3. Search for Z's methods being called

## Core Capabilities

### Search Strategies

**Pattern-Based Search**
- Find by naming conventions
- Locate by code patterns
- Discover by architectural markers
- Identify by file organization

**Context-Aware Search**
- Understand code relationships
- Map dependencies
- Trace execution flows
- Find related components

**Multi-Angle Discovery**
- Search by functionality
- Search by structure
- Search by naming
- Search by patterns

## Exploration Workflow

### Step 1: Orient
- What are we looking for?
- Why do we need it?
- What level of detail is needed?
- Which thoroughness level is appropriate?

### Step 2: Map Structure
- Identify top-level organization
- Find key markers (entry points, config files)
- Note directory naming patterns

### Step 3: Execute Search
- Choose appropriate tools
- Use multiple search angles
- Document findings

### Step 4: Analyze & Synthesize
- Connect the dots
- Identify patterns
- Prioritize findings

## Best Practices

### Start Broad, Then Narrow
1. **First**: Get the lay of the land (`tree -L 2`, `ls -la src/`)
2. **Second**: Identify patterns (`fd -e ts`, `rg -c "class|function"`)
3. **Third**: Target specific areas

### Use Multiple Search Angles
- Search by name: `fd auth`
- Search by content: `rg "authentication"`
- Search by structure: `ast-grep --pattern "class $NAME"`
- Search by symbols: `lsp_workspace_symbols`

### Follow the Breadcrumbs
1. Check imports to find dependencies
2. Use LSP to find references
3. Look at file location for architectural clues
4. Check git history for context

### Document as You Go
```markdown
# Authentication Flow
1. Entry: src/middleware/auth.ts
2. Token validation: src/services/jwt.service.ts  
3. User lookup: src/repositories/user.repository.ts
4. Guards: src/guards/auth.guard.ts
```

## Anti-Patterns

- **Don't Search Without Context**: Understand what you're looking for first
- **Don't Ignore File Structure**: Always check directory organization
- **Don't Rely on Single Search Method**: Use multiple approaches
- **Don't Forget About Tests**: Search test files for real usage
- **Don't Skip Configuration Files**: Check config early

## Related Skills

- Use [[debugger-skill]] when exploration reveals bugs
- Use [[architect-reviewer-skill]] to evaluate discovered patterns
- Use [[refactoring-specialist-skill]] to improve found code
- Use [[technical-advisory-skill]] for complex architectural questions

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
