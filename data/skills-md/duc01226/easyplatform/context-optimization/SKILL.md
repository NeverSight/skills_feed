---
name: context-optimization
description: Use when managing context window usage, compressing long sessions, or optimizing token usage. Triggers on keywords like "context", "memory", "tokens", "compress", "summarize session", "context limit", "optimize context".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, mcp__memory__*
infer: true
---

# Context Optimization & Management

Manage context window efficiently to maintain productivity in long sessions.

For persistent memory operations, see the `memory-management` skill.

---

## Four Strategies

### 1. Writing (Save Important Context)

Save critical findings to persistent memory via `memory-management` skill:
- Discovered architectural patterns
- Important business rules, cross-service dependencies
- Solution decisions

### 2. Selecting (Retrieve Relevant Context)

Load relevant memories at session start:
```javascript
mcp__memory__search_nodes({ query: 'relevant keywords' });
mcp__memory__open_nodes({ names: ['EntityName'] });
```

### 3. Compressing (Summarize Long Trajectories)

Create context anchors every 10 operations:
```markdown
=== CONTEXT ANCHOR [N] ===
Task: [Original task]
Completed: [Done items]
Remaining: [Todo items]
Findings: [Key discoveries]
Next: [Specific next step]
Confidence: [High/Medium/Low]
===========================
```

### 4. Isolating (Use Sub-Agents)

Delegate specialized tasks: broad exploration, independent research, parallel investigations.

---

## Token-Efficient Patterns

### File Reading
```javascript
// BAD: Reading entire files
Read({ file_path: 'large-file.cs' });

// GOOD: Read specific sections
Read({ file_path: 'large-file.cs', offset: 100, limit: 50 });

// GOOD: Use grep to find content first
Grep({ pattern: 'class SaveEmployeeCommand', path: 'src/' });
```

### Search Optimization
```javascript
// BAD: Multiple sequential searches
Grep({ pattern: 'CreateAsync' }); Grep({ pattern: 'UpdateAsync' });

// GOOD: Combined pattern
Grep({ pattern: 'CreateAsync|UpdateAsync|DeleteAsync', output_mode: 'files_with_matches' });
```

### Parallel Operations
```javascript
// GOOD: Parallel reads for independent files
[Read({ file_path: 'file1.cs' }), Read({ file_path: 'file2.cs' })];
```

---

## Anti-Patterns

| Anti-Pattern               | Better Approach                |
| -------------------------- | ------------------------------ |
| Reading entire large files | Use offset/limit or grep first |
| Sequential searches        | Combine with OR patterns       |
| Repeating same searches    | Cache results in memory        |
| No context anchors         | Write anchor every 10 ops      |
| Not using sub-agents       | Isolate exploration tasks      |
| Forgetting discoveries     | Save to memory entities        |

---

**Token Estimation:** 1 line ~ 10-15 tokens | 1 page ~ 500 tokens | Avg file ~ 1-3K tokens

**Thresholds:** 50K: consider compression | 100K: required | 150K: critical - save & summarize


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
