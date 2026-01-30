---
name: parallel-agents
description: Coordinate parallel agent execution for complex multi-step tasks using background agents and delegation patterns.
---

# Parallel Agent Execution Skill

This skill enables efficient multi-agent coordination for complex tasks.

## When to Use

- Complex tasks requiring multiple exploration paths
- Research + implementation in parallel
- Large refactoring across multiple files
- Tasks benefiting from diverse approaches

## Available Agents

### Built-in Agents
| Agent | Purpose | Mode |
|-------|---------|------|
| `@agent` | Autonomous coding | Full access |
| `#ask` | Q&A, explanations | Read-only |
| `#edit` | Direct file editing | Write |
| `Plan` | Research & planning | Read-only |
| `Research` | KB lookup | Read-only |
| `Planner` | Implementation design | Read-only |

### GitHub Copilot Coding Agent
For async background work that creates PRs:
```
Use: mcp_github_github_assign_copilot_to_issue
Result: Creates branch (copilot/*) and opens PR
```

## Parallelism Patterns

### Pattern 1: Explore-Then-Implement
```
1. Fire Research agent for solutions
2. Fire Planner agent for design
3. Wait for both results
4. Implement using @agent
```

### Pattern 2: Multi-File Refactor
```
1. Use runSubagent for each file group
2. Coordinate changes via todo list
3. Apply changes sequentially
```

### Pattern 3: Research + Code
```
1. Parallel: KB search + web fetch + file read
2. Sequential: Plan → Implement → Test
```

## Best Practices

1. **Never parallelize terminal commands** - Run sequentially
2. **Parallelize read operations** - file reads, searches, fetches
3. **Use todo list** - Track multi-step progress
4. **Delegate exploration** - Use subagents for research
5. **Commit per turn** - When using background agents

## Task Delegation Table

| Task Type | Recommended Agent |
|-----------|-------------------|
| Algorithm research | Research subagent |
| Code generation | @agent |
| File exploration | runSubagent |
| Quick edits | #edit |
| Planning | Plan subagent |
| Async PR work | Copilot Coding Agent |
