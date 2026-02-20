---
name: external-context
description: Invoke parallel document-specialist agents for external web searches and documentation lookup
argument-hint: <search query or topic>
---

# External Context Skill

Invoke parallel document-specialist agents to search the web for external documentation, references, and context.

## Overview

External Context decomposes a query into parallel web search facets, each handled by an independent document-specialist agent:

1. **Decomposition** - Break query into 2-5 independent search facets
2. **Parallel Search** - Spawn document-specialist agents for each facet
3. **Synthesis** - Aggregate findings into structured context

## Usage

```
/oh-my-claudecode:external-context <topic or question>
```

### Examples

```
/oh-my-claudecode:external-context What are the best practices for JWT token rotation in Node.js?
/oh-my-claudecode:external-context Compare Prisma vs Drizzle ORM for PostgreSQL
/oh-my-claudecode:external-context Latest React Server Components patterns and conventions
```

## Protocol

### Facet Decomposition

Given a query, decompose into 2-5 independent search facets:

```markdown
## Search Decomposition

**Query:** <original query>

### Facet 1: <facet-name>
- **Search focus:** What to search for
- **Sources:** Official docs, GitHub, blogs, etc.

### Facet 2: <facet-name>
...
```

### Parallel Agent Invocation

Fire independent facets in parallel via Task tool:

```
Task(subagent_type="oh-my-claudecode:document-specialist", model="sonnet", prompt="Search for: <facet 1 description>. Use WebSearch and WebFetch to find official documentation and examples. Cite all sources with URLs.")

Task(subagent_type="oh-my-claudecode:document-specialist", model="sonnet", prompt="Search for: <facet 2 description>. Use WebSearch and WebFetch to find official documentation and examples. Cite all sources with URLs.")
```

### Synthesis

After all agents complete, synthesize findings:

```markdown
## External Context: <query>

### Key Findings
1. **<finding>** - Source: [title](url)
2. **<finding>** - Source: [title](url)

### Detailed Results

#### Facet 1: <name>
<aggregated findings with citations>

#### Facet 2: <name>
<aggregated findings with citations>

### Sources
- [Source 1](url)
- [Source 2](url)
```

## Configuration

- Maximum 5 parallel document-specialist agents
- Each agent uses WebSearch and WebFetch tools
- No magic keyword trigger - explicit invocation only