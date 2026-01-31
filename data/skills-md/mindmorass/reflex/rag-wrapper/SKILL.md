---
name: rag-wrapper
description: Patterns for wrapping any agent with RAG context from Qdrant. Use to add persistent memory to imported or external agents.
---

# RAG Wrapper Patterns

Patterns for augmenting any agent with Qdrant context retrieval.

## Quick Start

To wrap an agent with RAG:

```
Use rag-proxy agent:
  Target: {agent-to-wrap}
  Task: {the task}
```

## Manual Wrapping Pattern

If you need custom control, follow this pattern:

### Step 1: Query Relevant Context

```
Tool: qdrant-find
Query: {key terms from task}
```

### Step 2: Format Context Block

```markdown
## Retrieved Context

### Source: {metadata.source}
Harvested: {metadata.harvested_at}
Type: {metadata.type}

{document content}

---
```

### Step 3: Prepend to Task

```markdown
{context blocks}

## Task

{original task}

---
Note: Above context is from stored knowledge. Verify if needed.
```

### Step 4: Delegate

```
Tool: Task
Agent: {target-agent}
Prompt: {enriched prompt}
```

## Enriched Prompt Template

```markdown
# Context from Stored Knowledge

The following relevant information was retrieved from project memory:

{{#each contexts}}
## From Qdrant
**Source:** {{metadata.source}}
**Harvested:** {{metadata.harvested_at}}

{{content}}

---
{{/each}}

# Your Task

{{original_task}}

---

**Note:** The context above comes from previously harvested research.
Use it if relevant, but verify currency for time-sensitive information.
The `harvested_at` dates indicate when the content was stored.
```

## Selective Wrapping

Not all tasks need RAG. Skip for:

| Task Type | Wrap? | Reason |
|-----------|-------|--------|
| Fresh research | No | Need current, not cached data |
| Simple edits | No | Context not needed |
| RAG-aware agents | No | Already query Qdrant |
| Implementation | Yes | Benefit from patterns, decisions |
| Debugging | Yes | Previous solutions may help |
| Architecture | Yes | Decisions and constraints matter |

## Agent-Collection Affinity

Map agent types to useful query topics:

| Agent Type | Query Topics |
|------------|--------------|
| frontend-developer | react, design system, components |
| backend-architect | api, architecture, decisions |
| security-auditor | security, authentication, vulnerabilities |
| devops | infrastructure, terraform, deployment |
| tester | testing, coverage, quality |

## Storing Results

After the target agent completes:

```
Tool: qdrant-store
Information: "<valuable findings>"
Metadata:
  source: "agent-output"
  type: "generated"
  harvested_at: "<ISO date>"
  tags: "<relevant,keywords>"
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Empty query results | Proceed without context |
| Qdrant unavailable | Fall back to unwrapped delegation |
| Target agent fails | Report error, don't retry with less context |
