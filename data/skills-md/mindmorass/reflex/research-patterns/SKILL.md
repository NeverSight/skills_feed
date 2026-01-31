---
name: research-patterns
description: Knowledge retrieval and research patterns using Qdrant for stored knowledge
---

# Research Patterns

Patterns for finding and synthesizing information, with Qdrant-first retrieval.

## Workflow

### 1. Check Stored Knowledge First

Before external research, query Qdrant:
```
Tool: qdrant-find
Query: "your search query"
```

If relevant results exist, use them and cite the source metadata.

### 2. External Research If Needed

If stored knowledge is insufficient or outdated:
- Search official documentation
- Use WebSearch for current information
- Cross-reference multiple sources

### 3. Store Valuable Findings

For information worth persisting, use `qdrant-store`:
```
Tool: qdrant-store
Information: "<content>"
Metadata:
  source: "<URL>"
  type: "documentation"
  harvested_at: "<ISO date>"
```

## Research Checklist

1. **Query Qdrant** - Always check stored knowledge first
2. **Assess freshness** - Check `harvested_at` metadata
3. **Define gaps** - What's missing or outdated?
4. **Search externally** - Find additional sources if needed
5. **Evaluate** - Assess source quality and relevance
6. **Synthesize** - Combine into coherent answer
7. **Cite** - Reference sources including Qdrant metadata
8. **Store** - Save valuable new findings to Qdrant

## Best Practices

- Note data freshness in responses
- Cross-reference multiple sources
- Distinguish cached vs fresh information
- Keep stored documents focused (one topic each)
