---
name: cli-router
description: Routes tasks to locally installed CLI tools using semantic matching. Triggers on tasks requiring shell commands, file operations, code search, data processing, visualization, or external tool invocation. Uses cli-index for semantic routing.
---

# CLI Router

Routes tasks to the most appropriate CLI tool based on semantic intent matching.

## Trigger Conditions

Activate when task involves:
- Shell/terminal operations
- File search or navigation
- Code search (semantic or pattern)
- Data processing (CSV, JSON)
- Visualization generation
- External tool invocation

## CLI Categories

| Category | Tools | Triggers |
|:---------|:------|:---------|
| **ai_llm** | claude, gemini, codex, amp, aider | AI help, implement, explain |
| **semantic_search** | ck, ast-grep, osgrep | semantic search, find code, pattern |
| **knowledge_graph** | cypher-shell, turbovault | graph, neo4j, knowledge |
| **data_processing** | qsv, csvtk, nu, jq | csv, json, transform, data |
| **file_navigation** | yazi, broot, fd, rg | browse, find files, navigate |
| **code_quality** | bat, difftastic, delta | diff, syntax, format |
| **visualization** | d2, mermaid, mermaid-ascii | diagram, flowchart, visual |
| **mcp_tools** | mcp-skillset, lootbox, automcp | mcp, skills, tools |
| **productivity** | fabric, atuin, btop, zellij | patterns, history, monitor |
| **document** | docling, pdf-search, qmd | pdf, document, markdown |

## Routing Logic

```bash
# Use cli-index for semantic routing
cli-index route "{user_intent}"

# Example output:
# tool: ck
# category: semantic_search
# confidence: 0.85
# command_hint: ck --sem "async functions" src/
```

## Decision Tree

```
CLI Task Detected
    │
    ├── Code search?
    │   ├── Semantic? → ck --sem
    │   ├── Pattern/AST? → ast-grep
    │   └── Grep-like? → rg
    │
    ├── File operations?
    │   ├── Navigate? → yazi | broot
    │   ├── Find files? → fd
    │   └── Search content? → rg
    │
    ├── Data processing?
    │   ├── CSV? → qsv | csvtk
    │   ├── JSON? → jq | sj
    │   └── Structured? → nu
    │
    ├── Visualization?
    │   ├── Diagrams? → d2
    │   ├── Flowcharts? → mermaid
    │   └── ASCII? → mermaid-ascii
    │
    ├── AI assistance?
    │   ├── Claude preferred? → claude
    │   ├── Long context? → gemini
    │   └── OpenAI? → codex
    │
    └── Document processing?
        ├── PDF? → docling | pdf-search
        └── Markdown? → qmd
```

## Commands

```bash
# Search for matching tools
cli-index search "semantic code search"

# Route to best tool
cli-index route "find async functions in codebase"

# List tools by category
cli-index list semantic_search

# Get tool info
cli-index info ck

# Suggest tool chain
cli-index suggest "search code then visualize dependencies"

# Verify all tools available
cli-index verify
```

## Integration

- **cli-index**: Primary routing CLI
- **ck**: Semantic code search with embeddings
- **reasoning-index**: Command framework routing
- **mcp-skillset**: Skill discovery

## Quick Reference

```yaml
semantic_search: ck --sem "query" path/
pattern_search: ast-grep -p "pattern"
file_find: fd "pattern"
content_search: rg "pattern"
csv_process: qsv [cmd] file.csv
json_query: jq ".path" file.json
diagram: d2 input.d2 output.svg
ai_help: claude -p "query"
```
