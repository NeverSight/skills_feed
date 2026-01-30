---
name: knowledge-research
description: Research solutions, algorithms, and best practices from the SurrealDB GraphRAG knowledge base containing 600+ scientific papers, StackOverflow answers, and GitHub repositories.
---

# Knowledge Base Research Skill

This skill provides access to a curated knowledge base containing research on audio DSP, acoustics, AI/ML, and software development.

## When to Use

- Before implementing complex algorithms (reverb, FFT, convolution)
- When debugging unfamiliar errors
- For design patterns and best practices
- To find solutions from past conversations
- When researching scientific concepts

## Knowledge Base Access

```
URL: http://localhost:8000/sql
Auth: Basic cm9vdDpyb290 (root:root)
Headers: surreal-ns: research, surreal-db: knowledge
```

## Quick Queries

### Full-Text Search
```sql
SELECT title, content, source, url FROM knowledge 
WHERE title @@ 'keyword' OR content @@ 'keyword' LIMIT 10;
```

### Find Algorithms
```sql
SELECT name, description, success_rate, implementation_notes 
FROM algorithm WHERE name CONTAINS 'reverb';
```

### Search Past Solutions
```sql
SELECT user_text, assistant_text FROM chat_message 
WHERE assistant_text @@ 'solution keyword' LIMIT 5;
```

### Paper Research
```sql
SELECT cite_key, title, authors, abstract FROM paper 
WHERE abstract @@ 'acoustic simulation';
```

## Available Data Sources

| Source | Count | Content |
|--------|-------|---------|
| ArXiv | 500+ | Scientific papers |
| StackOverflow | 35+ | Q&A |
| DSP.SE | 15+ | Signal processing |
| Physics.SE | 50+ | Physics Q&A |
| GitHub | 20+ | Curated repos |

## Built-in Functions

- `fn::find_topic($keyword)` - Multi-table search
- `fn::get_algorithm_context($name)` - Algorithm + sources
- `fn::kb_stats()` - Database statistics
