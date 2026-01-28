---
name: codemap
description: Navigate codebases efficiently using structural indexes. Use when finding symbol definitions (classes, functions, methods), exploring file structure, or locating code by name. Reduces token consumption by 60-80% through targeted line-range reads instead of full file scans.
allowed-tools: Read, Bash, Glob, Grep
user-invocable: true
---

# CodeMap - Codebase Structural Index

Navigate codebases efficiently using pre-built structural indexes stored in `.codemap/` directories.

## When to Use This Skill

**USE CodeMap when:**
- Finding where a class, function, method, or type is defined
- Understanding a file's structure before reading it
- Searching for symbols by name
- Reducing token usage during codebase exploration

**READ full files when:**
- Understanding implementation details
- Making edits to code
- The symbol isn't in the index (new/untracked file)

## Quick Reference

```bash
# Find a symbol by name (case-insensitive)
codemap find "SymbolName"

# Filter by type
codemap find "handle" --type method
codemap find "User" --type class
codemap find "Config" --type interface

# Show file structure with all symbols
codemap show path/to/file.ts

# Check if index is up-to-date
codemap validate

# View index statistics
codemap stats
```

## Workflow: Finding Code

### Step 1: Find Symbol Location
```bash
codemap find "UserService"
```
Output:
```
src/services/user.ts:15-189 [class] UserService
  (config: Config)
```

### Step 2: Read Only Relevant Lines
Instead of reading the entire file, read just lines 15-189:
```
Read src/services/user.ts lines 15-189
```

### Step 3: Explore Nested Symbols
```bash
codemap show src/services/user.ts
```
Output:
```
File: src/services/user.ts (hash: a3f2b8c1)
Lines: 542
Language: typescript

Symbols:
- UserService [class] L15-189
  - constructor [method] L20-35
  - getUser [method] L37-98
    (userId: string) : Promise<User>
  - createUser [async_method] L100-145
    (data: CreateUserDto) : Promise<User>
```

## Symbol Types

| Type | Description |
|------|-------------|
| `class` | Class declaration |
| `function` | Function declaration |
| `method` | Class method |
| `async_function` | Async function |
| `async_method` | Async class method |
| `interface` | TypeScript interface |
| `type` | TypeScript type alias |
| `enum` | Enum declaration |

## Index Structure

The `.codemap/` directory mirrors the project structure:
```
.codemap/
├── .codemap.json              # Root manifest
├── _root.codemap.json         # Files in project root
├── src/
│   ├── .codemap.json          # Files in src/
│   └── services/
│       └── .codemap.json      # Files in src/services/
```

## Direct JSON Access

For programmatic access, read the JSON files directly:
```bash
cat .codemap/src/services/.codemap.json
```

## Validation

Before trusting cached line numbers (especially after context compaction):
```bash
codemap validate path/to/file.ts
```
- "up to date": Line ranges are valid
- "stale": File changed, re-read or run `codemap update`

## Setup (If Not Initialized)

If a project doesn't have a `.codemap/` directory:

### Prerequisites
- Python 3.10+ and pip must be installed
- Verify with: `python3 --version && pip --version`

### Installation
```bash
# Install codemap from GitHub (NOT from PyPI - there's a different package there)
pip install git+https://github.com/AZidan/codemap.git

# Initialize index
codemap init .
```

**IMPORTANT**: Do NOT use `pip install codemap` - that installs a different package from PyPI. Always use the GitHub URL above.

### Start Watch Mode (Recommended)
Start watch mode in the background to keep the index automatically updated:
```bash
codemap watch . &
```

This runs in the background and updates the index whenever files change. No need to manually run `codemap update`.

To stop watch mode later:
```bash
pkill -f "codemap watch"
```

## Best Practices

1. **Search before scanning**: Always try `codemap find` before grep/glob
2. **Use line ranges**: Read specific line ranges instead of full files
3. **Check freshness**: Use `codemap validate` before trusting cached line numbers
4. **Explore structure first**: Use `codemap show` to understand file layout before diving in

## Example Session

Task: "Fix the authentication bug in the login handler"

```bash
# 1. Find relevant symbols
codemap find "login"
# → src/auth/handlers.ts:45-92 [function] handleLogin

# 2. Check file structure
codemap show src/auth/handlers.ts
# Shows handleLogin and related functions with line ranges

# 3. Read only the relevant function (lines 45-92)
# ... make your fix ...

# 4. If you need related code, find it
codemap find "validateToken"
# → src/auth/utils.ts:12-38 [function] validateToken
```
