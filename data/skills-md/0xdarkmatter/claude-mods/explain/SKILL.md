---
name: explain
description: "Deep explanation of complex code, files, or concepts. Routes to expert agents, uses structural search, generates mermaid diagrams. Triggers on: explain, deep dive, how does X work, architecture, data flow."
allowed-tools: "Read Glob Grep Bash Task"
compatibility: "Uses ast-grep, tokei, rg, fd if available. Falls back to standard tools."
depends-on: []
related-skills: ["structural-search", "code-stats"]
---

# Explain - Deep Code Explanation

Get a comprehensive explanation of code, files, directories, or architectural concepts. Automatically routes to the most relevant expert agent and uses modern CLI tools for analysis.

## Arguments

$ARGUMENTS

- `<target>` - File path, function name, class name, directory, or concept
- `--depth <shallow|normal|deep|trace>` - Level of detail (default: normal)
- `--focus <arch|flow|deps|api|perf>` - Specific focus area

## Architecture

```
/explain <target> [--depth] [--focus]
    |
    +-> Step 1: Detect & Classify Target
    |     +- File exists? -> Read it
    |     +- Function/class? -> ast-grep to find definition
    |     +- Directory? -> tokei for overview
    |     +- Concept? -> rg search codebase
    |
    +-> Step 2: Gather Context (parallel)
    |     +- structural-search skill -> find usages
    |     +- code-stats skill -> assess scope
    |     +- Find related: tests, types, docs
    |     +- Load: AGENTS.md, CLAUDE.md conventions
    |
    +-> Step 3: Route to Expert Agent
    |     +- .ts/.tsx -> typescript-expert or react-expert
    |     +- .py -> python-expert
    |     +- .vue -> vue-expert
    |     +- .sql/migrations -> postgres-expert
    |     +- agents/skills/commands -> claude-architect
    |     +- Default -> general-purpose
    |
    +-> Step 4: Generate Explanation
    |     +- Structured markdown with sections
    |     +- Mermaid diagrams (flowchart/sequence/class)
    |     +- Related code paths as file:line refs
    |     +- Design decisions and rationale
    |
    +-> Step 5: Integrate
          +- Offer to save to ARCHITECTURE.md (if significant)
          +- Link to /save if working on related task
```

## Execution Steps

### Step 1: Detect Target Type

```bash
# Check if target is a file
test -f "$TARGET" && echo "FILE" && exit

# Check if target is a directory
test -d "$TARGET" && echo "DIRECTORY" && exit

# Otherwise, search for it as a symbol
```

**For files:** Read directly with bat (syntax highlighted) or Read tool.

**For directories:** Get overview with tokei (if available):
```bash
command -v tokei >/dev/null 2>&1 && tokei "$TARGET" --compact || echo "tokei unavailable"
```

**For symbols (function/class):** Find definition with ast-grep:
```bash
# Try ast-grep first (structural)
command -v ast-grep >/dev/null 2>&1 && ast-grep -p "function $TARGET" -p "class $TARGET" -p "def $TARGET"

# Fallback to ripgrep
rg "(?:function|class|def|const|let|var)\s+$TARGET" --type-add 'code:*.{ts,tsx,js,jsx,py,vue}' -t code
```

### Step 2: Gather Context

Run these in parallel where possible:

**Find usages (structural-search skill):**
```bash
# With ast-grep
ast-grep -p "$TARGET($_)" --json 2>/dev/null | head -20

# Fallback
rg "$TARGET" --type-add 'code:*.{ts,tsx,js,jsx,py,vue}' -t code -l
```

**Find related files:**
```bash
# Tests
fd -e test.ts -e spec.ts -e test.py -e spec.py | xargs rg -l "$TARGET" 2>/dev/null

# Types/interfaces
fd -e d.ts -e types.ts | xargs rg -l "$TARGET" 2>/dev/null
```

**Load project conventions:**
- Read AGENTS.md if exists
- Read CLAUDE.md if exists
- Check for framework-specific patterns

### Step 3: Route to Expert Agent

Determine the best expert based on file extension and content:

| Pattern | Primary Agent | Condition |
|---------|---------------|-----------|
| `.ts` | typescript-expert | No JSX/React imports |
| `.tsx` | react-expert | JSX present |
| `.js`, `.jsx` | javascript-expert | - |
| `.py` | python-expert | - |
| `.vue` | vue-expert | - |
| `.sql`, `migrations/*` | postgres-expert | - |
| `agents/*.md`, `skills/*`, `commands/*` | claude-architect | Claude extensions |
| `*.test.*`, `*.spec.*` | (framework expert) | Route by file type |
| Other | general-purpose | Fallback |

**Invoke via Task tool:**
```
Task tool with subagent_type: "[detected]-expert"
Prompt includes:
  - File content
  - Related files found
  - Project conventions
  - Requested depth and focus
```

### Step 4: Generate Explanation

The expert agent produces a structured explanation:

```markdown
# Explanation: [target]

## Overview
[1-2 sentence summary of purpose and role in the system]

## Architecture

[Mermaid diagram - choose appropriate type]

### Flowchart (for control flow)
` ` `mermaid
flowchart TD
    A[Input] --> B{Validate}
    B -->|Valid| C[Process]
    B -->|Invalid| D[Error]
    C --> E[Output]
` ` `

### Sequence (for interactions)
` ` `mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Database
    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Result
    Server-->>Client: Response
` ` `

### Class (for structures)
` ` `mermaid
classDiagram
    class Component {
        +props: Props
        +state: State
        +render(): JSX
    }
` ` `

## How It Works

### Step 1: [Phase Name]
[Explanation with code references]

See: `src/module.ts:42`

### Step 2: [Phase Name]
[Explanation]

## Key Concepts

### [Concept 1]
[Explanation]

### [Concept 2]
[Explanation]

## Dependencies

| Import | Purpose |
|--------|---------|
| `package` | [why it's used] |

## Design Decisions

### Why [decision]?
[Rationale and tradeoffs considered]

## Related Code

| File | Relationship |
|------|--------------|
| `path/to/file.ts:123` | [how it relates] |

## See Also

- `/explain path/to/related` - [description]
- [External docs link] - [description]
```

## Depth Modes

| Mode | Output |
|------|--------|
| `--shallow` | Overview paragraph, key exports, no diagram |
| `--normal` | Full explanation with 1 diagram, main concepts (default) |
| `--deep` | Exhaustive: all internals, edge cases, history, multiple diagrams |
| `--trace` | Data flow tracing through entire system, sequence diagrams |

### Shallow Example
```bash
/explain src/auth/token.ts --shallow
```
Output: Single paragraph + exports list.

### Deep Example
```bash
/explain src/core/engine.ts --deep
```
Output: Full internals, algorithm analysis, performance notes, edge cases.

### Trace Example
```bash
/explain handleLogin --trace
```
Output: Traces data flow from entry to database to response.

## Focus Modes

| Mode | What It Analyzes |
|------|------------------|
| `--focus arch` | Module boundaries, layer separation, dependencies |
| `--focus flow` | Data flow, control flow, state changes |
| `--focus deps` | Imports, external dependencies, integrations |
| `--focus api` | Public interface, inputs/outputs, contracts |
| `--focus perf` | Complexity, bottlenecks, optimization opportunities |

## CLI Tool Integration

Commands use modern CLI tools with graceful fallbacks:

| Tool | Purpose | Fallback |
|------|---------|----------|
| `tokei` | Code statistics | Skip stats |
| `ast-grep` | Structural search | `rg` with patterns |
| `bat` | Syntax highlighting | Read tool |
| `rg` | Content search | Grep tool |
| `fd` | File finding | Glob tool |

**Check availability:**
```bash
command -v tokei >/dev/null 2>&1 || echo "tokei not installed - skipping stats"
```

## Usage Examples

```bash
# Explain a file
/explain src/auth/oauth.ts

# Explain a function (finds it automatically)
/explain validateToken

# Explain a directory
/explain src/services/

# Deep dive with architecture focus
/explain src/core/engine.ts --deep --focus arch

# Trace data flow
/explain handleUserLogin --trace

# Quick overview
/explain src/utils/helpers.ts --shallow

# Focus on dependencies
/explain package.json --focus deps
```

## Integration

| Skill/Command | Relationship |
|---------------|--------------|
| `/review` | Review after understanding |
| `/testgen` | Generate tests for explained code |
| `/save` | Save progress if working on related task |

## Persistence

After significant explanations, you may be offered:

```
Would you like to save this explanation?
  1. Append to ARCHITECTURE.md
  2. Append to AGENTS.md (if conventions-related)
  3. Don't save (output only)
```

This keeps valuable architectural knowledge in git-tracked documentation.

## Notes

- Explanations are based on code analysis, not documentation
- Complex systems may need multiple `/explain` calls
- Use `--deep` for unfamiliar codebases
- Mermaid diagrams render in GitHub, GitLab, VSCode, and most markdown viewers
- Expert agents provide framework-specific insights
