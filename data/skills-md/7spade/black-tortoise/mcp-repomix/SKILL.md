---
name: mcp-repomix
description: Use the Repomix MCP server to package codebase into consolidated files for AI analysis, search file contents, and understand project structure; essential for comprehensive codebase analysis and context gathering.
---

# MCP Skill: Repomix

## Scope
Use the MCP server configured as `repomix` in `.vscode/mcp.json` to:
- Package entire codebase into consolidated files for AI analysis
- Search and grep through packed repository outputs
- Understand project structure and file organization
- Provide comprehensive context for large-scale refactoring

## Preconditions
- Ensure `.vscode/mcp.json` contains a server entry named `repomix`.
- The Repomix MCP server provides tools for codebase packaging and analysis.

## Operating Rules
- Use `pack_codebase` to create consolidated repository snapshots for analysis
- Use `grep_repomix_output` to search within packed outputs
- Use `attach_packed_output` to load existing Repomix output files
- Prefer Repomix for full codebase context gathering before major refactors
- Use XML or Markdown output styles for better LLM comprehension

## When To Use
- **Before major architectural changes**: Get full codebase snapshot
- **Cross-cutting refactors**: Changes affecting multiple capabilities/layers
- **Understanding legacy code**: Analyze entire module structure
- **Documentation generation**: Extract all files for comprehensive docs
- **Code review preparation**: Package changes with full context
- **Migration planning**: Understand all dependencies before migration
- **Pattern analysis**: Search for specific patterns across entire codebase

## Key Tools Available
1. **pack_codebase** - Package local directory into consolidated file
2. **pack_remote_repository** - Clone and package GitHub repository
3. **attach_packed_output** - Load existing packed output for analysis
4. **read_repomix_output** - Read specific lines from packed output
5. **grep_repomix_output** - Search patterns in packed output
6. **generate_skill** - Create Claude Agent Skill from codebase

## Output Formats
- **XML**: Structured with `<file>` tags (best for precise parsing)
- **Markdown**: Human-readable with code blocks (best for review)
- **JSON**: Machine-readable key-value pairs
- **Plain**: Simple text with separators

## Integration with Black-Tortoise Workflow
- Combine with `mcp-sequential-thinking` for complex refactoring plans
- Use before running `architecture:gate` for comprehensive boundary analysis
- Essential for understanding DDD layer dependencies
- Helps validate "no deep imports" rule across entire codebase

## Prompt Templates
- "Pack the codebase and analyze all DDD boundary violations"
- "Use Repomix to find all usages of [pattern] across the entire repository"
- "Package src/app/capabilities and identify cross-capability dependencies"
- "Create a full codebase snapshot before starting [major refactor]"
- "Search the packed repository for all event emission points"

## Best Practices
1. **Scope appropriately**: Pack only relevant directories to reduce tokens
2. **Use compression**: Enable Tree-sitter compression for large codebases
3. **Combine with grep**: Use grep_repomix_output for targeted searches
4. **Sequential workflow**: Pack → Analyze → Plan → Implement
5. **Version control**: Save packed outputs for before/after comparison

## Example Workflows

### Workflow 1: Cross-Capability Analysis
```
1. pack_codebase(directory: "src/app/capabilities", compress: true)
2. grep_repomix_output(pattern: "import.*from.*@app/", contextLines: 3)
3. Identify violations of "no deep imports" rule
4. Use sequential-thinking to plan refactoring
```

### Workflow 2: Event Flow Analysis
```
1. pack_codebase(directory: "src/app", includePatterns: "**/*.ts")
2. grep_repomix_output(pattern: "publishEvent|EventBus", contextLines: 5)
3. Map all event producers and consumers
4. Validate append-before-publish contract
```

### Workflow 3: Dependency Analysis
```
1. pack_codebase(directory: "src/app", style: "json")
2. grep_repomix_output(pattern: "from ['\"]@angular/fire", contextLines: 2)
3. Ensure all Firebase imports are in integration layer only
4. Document violations for remediation
```

## Safety & Performance
- Large repositories: Use `compress: true` to reduce token usage by ~70%
- Incremental analysis: Use `grep_repomix_output` instead of re-packing
- File limits: Use `includePatterns` and `ignorePatterns` to scope packing
- Context management: Attach packed outputs once, reuse for multiple queries

## Compliance with Black-Tortoise Rules
- **Occam's Razor**: Use Repomix only when full context is genuinely needed
- **Minimal changes**: Helps identify smallest change radius for refactors
- **DDD boundaries**: Essential for validating layer dependencies
- **Documentation**: Can generate comprehensive project structure docs
