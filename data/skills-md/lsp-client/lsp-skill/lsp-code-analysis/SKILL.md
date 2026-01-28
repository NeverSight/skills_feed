---
name: lsp-code-analysis
description: Semantic code analysis via LSP. Navigate code (definitions, references, implementations), search symbols, preview refactorings, and get file outlines. Use for exploring unfamiliar codebases or performing safe refactoring.
license: LICENSE
---

# LSP Code Analysis

## IMPORTANT: PREREQUISITE

To use this skill, you **MUST** follow these steps:

1.  **Check for updates**: Run the [update script](scripts/update.sh) to ensure you are using the latest version of the tool.
2.  **Verify project support**: Run `lsp server start <project_path>` to start the LSP server and confirm the project is supported.

**IF YOU DO NOT PERFORM THESE STEPS, YOU ARE NOT ALLOWED TO USE THIS SKILL.**

## Abstract

This document specifies the operational requirements and best practices for the `lsp-code-analysis` skill. It provides a semantic interface to codebase navigation, analysis and refactoring via the Language Server Protocol (LSP).

## Overview

You are provided with `lsp` CLI tool for semantic code navigation and analysis. It SHOULD be preferred over `read` or `grep` for most code understanding tasks.

Usages:

- **Semantic navigation**: Jump to definitions, find references, locate implementations - understands code structure, not just text patterns.
- **Language-aware**: Distinguishes between variables, functions, classes, types - eliminates false positives from text search.
- **Cross-file intelligence**: Trace dependencies, refactor safely across entire codebase - knows what imports what.
- **Type-aware**: Get precise type information, signatures, documentation - without reading implementation code.

### Tool Selection

**Guideline**: You SHOULD prioritize LSP commands for code navigation and analysis. Agents MAY use `read` or `grep` ONLY when semantic analysis is not applicable (e.g., searching for comments or literal strings).

| Task                | Traditional Tool | Recommended LSP Command                         |
| ------------------- | ---------------- | ----------------------------------------------- |
| **Find Definition** | `grep`, `read`   | [`definition`](#definition-navigate-to-source)  |
| **Find Usages**     | `grep -r`        | [`reference`](#reference-find-all-usages)       |
| **Understand File** | `read`           | [`outline`](#outline-file-structure)            |
| **View Docs/Types** | `read`           | [`doc`](#doc-get-documentation)                 |
| **Refactor**        | `sed`            | See [Refactoring Guide](references/refactor.md) |

## Commands

All commands support `-h` or `--help`.

### Locating Symbols

Most commands use a unified locating syntax via the `--scope` and `--find` options.

**Arguments**: `<file_path>`

**Options**:

- `--scope`: Narrow search to a symbol body or line range.
- `--find`: Text pattern to find within the scope.

**Scope Formats**:

- `<line>`: Single line number (e.g., `42`).
- `<start>,<end>`: Line range (e.g., `10,20`). Use `0` for end to mean till EOF (e.g., `10,0`).
- `<symbol_path>`: Symbol path with dots (e.g., `MyClass.my_method`).

**Find Pattern (`--find`)**:

The `--find` option narrows the target to a **text pattern within the selected scope**:

- The scope is determined by `--scope` (line/range/symbol). If no `--scope` is given, the entire file is the scope.
- Pattern matching is **whitespace-insensitive**: differences in spaces, tabs, and newlines are ignored.
- You MAY include the cursor marker `<|>` inside the pattern to specify the **exact position of interest** within the match (for example, on a variable name, keyword, or operator).
- If `--find` is omitted, the command uses the start of the scope (or a tool-specific default) as the navigation target.

**Cursor Marker (`<|>`)**:

The `<|>` marker indicates the exact position for symbol resolution. It represents the character immediately to its right. Use it within the find pattern to point to a specific element (e.g., `user.<|>name` to target the `name` property).

**Examples**:

- `lsp doc foo.py --find "self.<|>"` - Find `self.` in entire file, position at the character after the dot (typically for completion or member access)
- `lsp doc foo.py --scope 42 --find "return <|>result"` - Find `return result` on line 42, position at `r` of `result`
- `lsp doc foo.py --scope 10,20 --find "if <|>condition"` - Find `if condition` in lines 10-20, position at `c` of `condition`
- `lsp doc foo.py --scope MyClass.my_method --find "self.<|>"` - Find `self.` within `MyClass.my_method`, position after the dot
- `lsp doc foo.py --scope MyClass` - Target the `MyClass` symbol directly

**Guideline for Scope vs. Find**:

- Use `--scope <symbol_path>` (e.g., `--scope MyClass`, `--scope MyClass.my_method`) to target **classes, functions, or methods**. This is the most robust and preferred way to target symbol.
- Use `--find` (often combined with `--scope`) to target variables or specific positions. Use this when the target is not a uniquely named symbol or when you need to pinpoint a specific usage within a code block.

Agents MAY use `lsp locate <file_path> --scope <scope> --find <find>` to verify if the target exists in the file and view its context before running other commands.

```bash
# Verify location exists
lsp locate main.py --scope 42 --find "<|>process_data"
```

### Pagination

Use pagination for large result sets like `reference` or `search`.

- `--pagination-id <ID>`: (Required) Unique session ID for consistent paging.
- `--max-items <N>`: Page size.
- `--start-index <N>`: Offset (0-based).

**Example**:

```bash
# Page 1
lsp search "User" --max-items 20 --pagination-id "task_123"

# Page 2
lsp search "User" --max-items 20 --start-index 20 --pagination-id "task_123"
```

**Guideline**: Use pagination with a unique ID for common symbols to fetch results in manageable chunks. Increment `--start-index` using the same ID to browse.

### Outline: File Structure

Get hierarchical symbol structure without reading implementation.

```bash
# Get main symbols (classes, functions, methods)
lsp outline <file_path>

# Get all symbols including variables and parameters
lsp outline <file_path> --all
```

Agents SHOULD use `outline` before reading files to avoid unnecessary context consumption.

### Definition: Navigate to Source

Navigate to where symbols are defined.

```bash
# Jump to where User.get_id is defined
lsp definition models.py --scope User.get_id

# Find where an imported variable comes from
lsp definition main.py --scope 42 --find "<|>config"

# Find declaration (e.g., header files, interface declarations)
lsp definition models.py --scope 25 --mode declaration --find "<|>provider"

# Find the class definition of a variable's type
lsp definition models.py --scope 30 --find "<|>user" --mode type_definition
```

### Reference: Find All Usages

Find where symbols are used or implemented.

```bash
# Find all places where logger is referenced
lsp reference main.py --scope MyClass.run --find "<|>logger"

# Find all concrete implementations of an interface/abstract class
lsp reference api.py --scope "IDataProvider" --mode implementations

# Get more surrounding code context for each reference
lsp reference app.py --scope 10 --find "<|>my_var" --context-lines 5

# Limit results for large codebases
lsp reference utils.py --find "<|>helper" --max-items 50 --start-index 0
```

### Doc: Get Documentation

Get documentation and type information without navigating to source.

```bash
# Get docstring and type info for symbol at line 42
lsp doc main.py --scope 42

# Get API documentation for process_data function
lsp doc models.py --scope process_data
```

Agents SHOULD prefer `doc` over `read` when only documentation or type information is needed.

### Search: Global Symbol Search

Search for symbols across the workspace when location is unknown.

```bash
# Search by name (defaults to current directory)
lsp search "MyClassName"

# Search in specific project
lsp search "UserModel" --project /path/to/project

# Filter by symbol kind (can specify multiple times)
lsp search "init" --kinds function --kinds method

# Limit and paginate results for large codebases
lsp search "Config" --max-items 10
lsp search "User" --max-items 20 --start-index 0
```

Agents SHOULD use `--kinds` to filter results and reduce noise.

### Symbol: Get Complete Symbol Code

Get the full source code of the symbol containing a location.

```bash
# Get complete code of the function/class at line 15
lsp symbol main.py --scope 15

# Get full UserClass implementation
lsp symbol utils.py --scope UserClass

# Get complete method implementation
lsp symbol models.py --scope User.validate
```

Response includes: symbol name, kind (class/function/method), range, and **complete source code**.

Agents SHOULD use `symbol` to read targeted code blocks instead of using `read` on entire files.

### Refactoring Operations

Read [Refactoring Guide](references/refactor.md) for rename, extract, and other safe refactoring operations.

### Server: Manage Background Servers

The background manager starts automatically. Manual control is OPTIONAL.

```bash
# List running servers
lsp server list

# Start server for a project
lsp server start <path>

# Stop server for a project
lsp server stop <path>

# Shutdown the background manager
lsp server shutdown
```

## Best Practices

### General Workflows

#### Understanding Unfamiliar Code

The RECOMMENDED sequence for exploring new codebases:

```bash
# Step 1: Start with outline - Get file structure without reading implementation
lsp outline <file_path>

# Step 2: Inspect signatures - Use doc to understand API contracts
lsp doc <file_path> --scope <symbol_name>

# Step 3: Navigate dependencies - Follow definition chains
lsp definition <file_path> --scope <symbol_name>

# Step 4: Map usage - Find where code is called with reference
lsp reference <file_path> --scope <symbol_name>
```

#### Debugging Unknown Behavior

```bash
# Step 1: Locate symbol definition workspace-wide
lsp search "<symbol_name>"

# Step 2: Verify implementation details
lsp definition <file_path> --scope <symbol_name>

# Step 3: Trace all callers to understand invocation context
lsp reference <file_path> --scope <symbol_name>
```

### Finding Interface Implementations

```bash
# Step 1: Locate interface definition
lsp search "IUserService" --kinds interface

# Step 2: Find all implementations
lsp reference src/interfaces.py --scope IUserService --mode implementations
```

### Tracing Data Flow

```bash
# Step 1: Find where data is created
lsp search UserDTO --kinds class

# Step 2: Find where it's used
lsp reference models.py --scope UserDTO

# Step 3: Check transformations
lsp doc transform.py --scope map_to_dto
```

### Understanding Type Hierarchies

```bash
# Step 1: Get class outline
lsp outline models.py

# Step 2: Find subclasses (references to base)
lsp reference models.py --scope BaseModel

# Step 3: Check type definitions
lsp definition models.py --scope BaseModel --mode type_definition
```

### Performance Tips

```bash
# Use outline instead of reading entire files
lsp outline large_file.py  # Better than: read large_file.py

# Use symbol paths for nested structures (more precise than line numbers)
lsp definition models.py --scope User.Profile.validate

# Limit results in large codebases
lsp search "User" --max-items 20

# Use doc to understand APIs without navigating to source
lsp doc api.py --scope fetch_data  # Get docs/types without jumping to definition

# Verify locate strings if commands fail
lsp locate main.py --scope 42 --find "<|>my_var"
```

### Domain-Specific Guides

For specialized scenarios, see:

- **Monorepo**: [monorepo.md](references/monorepo.md)
- **Frontend**: [bp_frontend.md](references/bp_frontend.md)
- **Backend**: [bp_backend.md](references/bp_backend.md)
