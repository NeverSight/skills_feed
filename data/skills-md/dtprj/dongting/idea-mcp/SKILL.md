---
name: idea-mcp
description: |
  IntelliJ-IDEA MCP provides powerful IDE features including running tests, code analysis, refactoring, search, and project navigation. Use this when you need accurate Java code analysis (avoiding LSP false positives), running tests via IDEA configurations, refactoring symbols, or exploring codebase structure. Key commands: execute_run_configuration (run tests), get_file_problems (accurate errors/warnings), search_in_files_by_text (search code), list_directory_tree (view structure), get_file_text_by_path (read files), rename_refactoring (safe refactoring), execute_terminal_command (run shell commands).
---

# IntelliJ IDEA MCP Skill

**MCP is self-describing - this skill only documents known pitfalls and best practices not covered by MCP descriptions.**

## 🚨 Critical Pitfalls (MCP Doesn't Warn You)

### Connection Requirements
- **IDEA MUST be running** with MCP server connected
- Commands fail silently if IDEA is not running - no clear error message

### Path Confusion (Most Common Error)
- `projectPath`: **ABSOLUTE PATH** to project root (e.g., `/Users/name/project`)
  - ❌ `project` (wrong - relative)
  - ✅ `/Users/name/project` (correct - absolute)
- `filePath`/`pathInProject`/`directoryPath`: **RELATIVE** to project root

### Search Command Schema Bugs
**MCP claims parameters are optional but they're REQUIRED:**

- `search_in_files_by_text` & `search_in_files_by_regex`: **MUST** include `maxUsageCount`
  - Without this → schema error
  - Start with `maxUsageCount: 10`

- `find_files_by_name_keyword` & `find_files_by_glob`: **MUST** include `fileCountLimit`
  - Without this → schema error "data must have required property 'probablyHasMoreMatchingFiles'"
  - **Known bug**: Schema validation fails with certain patterns:
    - `find_files_by_name_keyword`: Start with `fileCountLimit: 1`
    - `find_files_by_glob`: Start with `fileCountLimit: 5-7`
    - Broader patterns (e.g., `**/*.java`) may support higher limits
    - If schema error, try smaller `fileCountLimit` or different patterns

### Rename Refactoring Limitations
**⚠️ MCP doesn't document what rename_refactoring CANNOT do:**
- ✅ Renames: Field/variable declarations and their references
- ❌ May have limitations with: Method parameters in signatures, certain symbol types (test before relying)
- **Always** use `search_in_files_by_text` first to understand scope
- **Always** verify with `get_file_problems` after renaming

### High-Risk Operations
**MCP doesn't emphasize danger levels:**
- `execute_terminal_command`: **HIGH RISK** - Can run ANY shell command with full system permissions (no sandboxing). Use with extreme caution; verify commands before execution.
- `rename_refactoring` & `replace_text_in_file`: Modifies code globally
- `create_new_file`: Creates files on disk immediately
- `reformat_file`: Modifies formatting without confirmation

## ✅ Essential Best Practices

1. **Path discipline**: Absolute for `projectPath`, relative for everything else
2. **Count parameters**: Always include `maxUsageCount` for search, `fileCountLimit` for file search
3. **File search**: Start conservative - `fileCountLimit: 1` for name keyword, `5-7` for glob
4. **Before refactoring**: Search first to understand scope
5. **After changes**: Use `get_file_problems` to verify no errors introduced
6. **Java accuracy**: Prefer IDEA's `get_file_problems` over LSP (avoids false positives)
7. **Text replacement**: Get exact text with `get_file_text_by_path` before replacing
8. **Test execution**: Use `execute_run_configuration` for proper TeamCity-formatted output
9. **Timeouts**: Build/test may need 120-300s, not default 30s

## 🔄 Common Workflows (Dongting Project)

*Note: Examples use project path `/Users/huangli/dt/dongting`. Adjust `projectPath` for other projects.*

### 1. Find a Java Class by Name
**Use case**: Locate `KvImpl.java` in the codebase.

```yaml
Tool: IntelliJ-IDEA_find_files_by_name_keyword
Parameters:
  projectPath: "/Users/huangli/dt/dongting"  # Absolute path
  nameKeyword: "KvImpl"
  fileCountLimit: 1  # Start with 1 due to schema bug
```

**If no results**: Try `find_files_by_glob` with pattern:
```yaml
Tool: IntelliJ-IDEA_find_files_by_glob
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  globPattern: "**/*KvImpl*.java"
  fileCountLimit: 5
```

### 2. Search for Text Across Codebase
**Use case**: Find all occurrences of "DtLog.getLogger".

```yaml
Tool: IntelliJ-IDEA_search_in_files_by_text
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  searchText: "DtLog.getLogger"
  maxUsageCount: 20  # REQUIRED parameter
  caseSensitive: true
```

**For regex patterns** (e.g., find all log declarations):
```yaml
Tool: IntelliJ-IDEA_search_in_files_by_regex
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  regexPattern: "private static final DtLog log = DtLogs\\.getLogger\\(.*\\)"
  maxUsageCount: 10
```

### 3. Run a Test via IDEA Run Configuration
**Use case**: Execute the "client:test" run configuration.

```yaml
Tool: IntelliJ-IDEA_execute_run_configuration
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  configurationName: "client:test"
  timeout: 120000  # 2 minutes for tests
```

**First, list available run configurations**:
```yaml
Tool: IntelliJ-IDEA_get_run_configurations
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
```

### 4. Check Compilation Errors in a File
**Use case**: Verify `server/src/main/java/com/github/dtprj/dongting/raft/server/RaftNode.java` has no errors.

```yaml
Tool: IntelliJ-IDEA_get_file_problems
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  filePath: "server/src/main/java/com/github/dtprj/dongting/raft/server/RaftNode.java"
  errorsOnly: true
```

**Note**: More accurate than LSP for this multi-module Maven project.

### 5. Safe Refactoring: Rename a Field
**Pre-verification**: Search for current usage:
```yaml
Tool: IntelliJ-IDEA_search_in_files_by_text
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  searchText: "currentTerm"
  maxUsageCount: 50
```

**Execute rename**:
```yaml
Tool: IntelliJ-IDEA_rename_refactoring
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  pathInProject: "server/src/main/java/com/github/dtprj/dongting/raft/server/RaftNode.java"
  symbolName: "currentTerm"
  newName: "currentElectionTerm"
```

**Post-verification**: Check for errors:
```yaml
Tool: IntelliJ-IDEA_get_file_problems
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  filePath: "server/src/main/java/com/github/dtprj/dongting/raft/server/RaftNode.java"
```

### 6. Explore Project Structure
**Use case**: View module layout.

```yaml
Tool: IntelliJ-IDEA_list_directory_tree
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
  directoryPath: "."  # Project root
  maxDepth: 3
```

**To see all open files** (helpful for context):
```yaml
Tool: IntelliJ-IDEA_get_all_open_file_paths
Parameters:
  projectPath: "/Users/huangli/dt/dongting"
```

## 🤔 When to Use: IDEA MCP vs LSP vs Bash Tools

### Decision Matrix

| Task | Recommended Tool | Why |
|------|-----------------|-----|
| **Java code analysis** (errors, warnings) | **IDEA MCP** (`get_file_problems`) | More accurate for multi-module Maven projects; avoids LSP false positives |
| **Running tests** | **IDEA MCP** (`execute_run_configuration`) | Proper test environment, TeamCity-formatted output, dependency resolution |
| **Refactoring** (rename, move) | **IDEA MCP** (`rename_refactoring`) | Semantic understanding, cross-file updates, safer than manual edits |
| **Search code** (text, regex) | **IDEA MCP** (`search_in_files_by_text`) | Fast, indexes entire project; better than `grep` for large codebases |
| **Find files** (by name, glob) | **IDEA MCP** (`find_files_by_*`) | Fast indexed search; use workarounds for schema bugs |
| **Read file content** | **LSP** (`read` tool) or **IDEA MCP** (`get_file_text_by_path`) | LSP for quick reads; IDEA for large files or binary detection |
| **Build/compile** | **Bash** (`mvn` commands) | Full control, reproducible; IDEA build may have caching issues |
| **Git operations** | **Bash** (`git` commands) | Standard, predictable; IDEA MCP lacks git tools |
| **Project exploration** | **IDEA MCP** (`list_directory_tree`) | Visual tree structure; better than `ls` for nested directories |
| **Terminal commands** | **IDEA MCP** (`execute_terminal_command`) or **Bash** | IDEA for integrated terminal; Bash for complex pipelines |

### Key Principles
1. **IDEA MCP when**: Need IDE intelligence (refactoring, accurate errors, test execution)
2. **LSP when**: Quick file reads, symbol navigation (if IDEA not available)
3. **Bash when**: Builds, Git, system operations, or when IDEA MCP has schema bugs

**Remember**: IDEA must be running for MCP tools to work. If IDEA is unavailable, fall back to LSP/Bash.

## ⏱️ Performance Considerations & Timeouts

### Recommended Timeouts by Operation

| Operation | Recommended Timeout | Notes |
|-----------|-------------------|-------|
| **File search** (`find_files_by_*`) | 30000 (30s) | Usually fast; limit results with `fileCountLimit` |
| **Text search** (`search_in_files_by_*`) | 60000 (60s) | Can be slower for large codebases; use `maxUsageCount` |
| **Read file** (`get_file_text_by_path`) | 10000 (10s) | Fast for text files; binary files may fail |
| **Get file problems** (`get_file_problems`) | 15000 (15s) | Quick analysis |
| **Run configuration** (`execute_run_configuration`) | 300000 (5min) | Tests/builds can take minutes; adjust based on test size |
| **Build project** (`IntelliJ-IDEA_build_project`) | 300000 (5min) | Full rebuild may be slow |
| **Refactoring** (`rename_refactoring`) | 60000 (60s) | Usually fast for single symbols |
| **Directory listing** (`list_directory_tree`) | 20000 (20s) | Depends on project size |

### Performance Tips
1. **Limit search results**: Use `maxUsageCount` and `fileCountLimit` to avoid excessive data transfer
2. **Cache project state**: IDEA MCP maintains project index; repeated searches are faster
3. **Avoid redundant calls**: Use `get_all_open_file_paths` to see what's already loaded
4. **Batch operations**: Combine searches with careful planning (but MCP is stateless)
5. **Fallback for large operations**: For full project builds, use Bash `mvn` commands instead

### Memory & Resource Considerations
- IDEA MCP runs within IDEA's JVM; large operations may affect IDE performance
- Searching huge files (>10MB) may cause timeouts; use LSP `read` with offset/limit instead
- Concurrent MCP requests may queue; avoid parallel operations on same project

## 🔧 Quick Troubleshooting

### Common Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Structured content does not match the tool's output schema: data must have required property 'probablyHasMoreMatchingFiles'` | Missing `fileCountLimit` or `maxUsageCount` parameter | Add required parameter: `fileCountLimit: 1` (for file search) or `maxUsageCount: 10` (for text search) |
| `MCP error -32602: Structured content does not match the tool's output schema` | MCP server bug with certain parameter values | Reduce `fileCountLimit` (try 1, 5, 7); use simpler glob patterns |
| `Command failed: Connection refused` | IDEA not running or MCP server not connected | Verify IDEA is running with MCP plugin active; wait for connection |
| `Command timed out after X milliseconds` | Operation taking longer than default timeout | Increase `timeout` parameter (e.g., 120000 for tests, 30000 for builds) |
| `File not found` or `Path does not exist` | Incorrect path (absolute vs relative confusion) | Use absolute path for `projectPath`, relative path for `filePath` |
| `No occurrences found` | Search text not found or path incorrect | Verify search text exists; check `projectPath` and file paths |
| `Could not get document` or `File is binary` | Trying to read binary/ non-text file | Use `get_file_text_by_path` only for text files; check file type |
| `Project directory not found` | `projectPath` incorrect or IDEA project not loaded | Verify project is fully loaded in IDEA; use absolute path |

### "Structured content does not match" (schema error)
- Add missing `maxUsageCount` or `fileCountLimit` parameter
- For file search errors: Try smaller `fileCountLimit` values

### Commands fail/timeout
1. Verify IDEA is running with MCP server connected
2. Check MCP plugin is active in IDEA settings
3. Wait for connection (may take seconds)
4. Verify project is fully loaded in IDEA

### Search returns no results
1. Verify `projectPath` is absolute and correct
2. Verify file paths are relative to project root
3. Use `list_directory_tree` to verify structure exists

### File operation fails
- For `create_new_file`: Use `overwrite: true` if file exists
- For `replace_text_in_file`: Get exact text with `get_file_text_by_path` first
- Check file is not locked by another process