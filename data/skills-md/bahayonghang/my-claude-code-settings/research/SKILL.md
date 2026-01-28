---
name: research
description: Use codex web search for technical research, output reports with complete citation links. Focus on key results users care about, minimize irrelevant content.
category: research
tags: [web-search, technical-research, citation, report]
---

# Technical Research Skill

Use codex web search for online research, output structured reports with citations.

## Core Principles

1. **Codex only retrieves**: Get raw sources and links, analyze and organize yourself
2. **Focus on key results**: Only keep what users care about, trim irrelevant info
3. **Links must be complete**: All citations need clickable sources
4. **Verify all links**: Validate URLs before finalizing report

## Research Workflow

### 1. Clarify Research Goals

Confirm with user:
- What's the core question?
- What needs comparison?
- Which aspects matter? (architecture/performance/use cases/cost)

### 2. Batch Retrieval

Use codex web search in multiple queries, each focused on one topic:

```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Return RAW search results with URLs. Search: <specific query>"
```

**Query Tips**:
- Add year constraints: `2024 2025`
- Request raw links: `Return RAW search results with URLs`
- Focus each query on single topic, avoid overly broad searches
- **IMPORTANT**: Always include the exact product name in query (e.g., "OpenSearch" not "Elasticsearch" if researching OpenSearch)

**Example Queries**:
```bash
# Architecture features
"Return RAW search results with URLs. Search: OpenSearch unique features architecture 2024 2025"

# Comparison
"Return RAW search results with URLs. Search: OpenSearch vs Elasticsearch key differences 2024 2025"

# Performance data
"Return RAW search results with URLs. Search: OpenSearch performance benchmark 2024 2025"

# History
"Return RAW search results with URLs. Search: OpenSearch history timeline fork Elasticsearch"
```

### 3. Extract Key Information

From codex results, extract:
- Key facts and data
- Technical details and principles
- Corresponding URLs

### 4. Analyze and Organize Yourself

**Don't let codex write the report**. Do it yourself:
- Filter valuable information
- Organize structure
- Add analysis and insights
- Unify citation format

### 5. Link Validation (Critical)

After drafting report, validate all links:

```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Use web search to verify if these URLs are valid. For each URL that returns 404, search for the correct replacement URL:
1. <url1>
2. <url2>
...
Report: which URLs are valid, which are 404, and provide correct replacement URLs for broken ones."
```

**Validation Rules**:
- Let user verify simple URLs by clicking (faster than codex)
- Use codex validation only when user requests or for batch verification
- If URL is 404, codex can search for replacement in same request
- Ensure reference name matches actual page content

## Output Format

### Citation Format (Clickable Links)

Inline citation:
```markdown
OpenSearch forked from Elasticsearch 7.10 in 2021 (source: [AWS OpenSearch Blog]).
```

Link definitions at end:
```markdown
[AWS OpenSearch Blog]: https://aws.amazon.com/blogs/opensource/...
```

### Report Structure

```markdown
# [Topic] Research Report

## 1. Overview
What it is, what problem it solves

## 2. Core Features/Architecture
Key technical points with citations

## 3. Comparison (if applicable)
Table comparison, each item with source

## 4. Recommendations
Conclusions based on research

## References
[Link Name 1]: URL1
[Link Name 2]: URL2
...
```

## Guidelines

- **Don't fabricate data**: No performance numbers without sources
- **Trim sections**: Only keep what users care about
- **Valid links**: Prefer official docs, reputable tech blogs
- **Declarative titles**: Don't use questions as headings
- **Reference name accuracy**: Ensure `[Reference Name]` matches actual page content

## Source Priority

1. **Official documentation** - Most authoritative, prefer when available
2. **Official blogs/announcements** - For news, releases, roadmaps
3. **Third-party tech blogs** - Only if official docs lack detail; verify quality first
4. **Independent benchmarks** - For performance data (note: vendor benchmarks may be biased)

**Note**: Third-party blogs may have lower quality. Always verify content accuracy before using.

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Codex searches wrong product | Always include exact product name in query |
| 404 links in final report | Validate all links before finalizing |
| Reference name doesn't match content | Verify page content matches reference name |
| Using vendor benchmarks as neutral | Note the source bias in report |
| Overly broad search queries | Focus each query on single topic |
| Missing year constraints | Add `2024 2025` for recent info |

## Example Research Task

User: Research differences between OpenSearch and Elasticsearch

Steps:
1. Search OpenSearch unique features (include "OpenSearch" in query)
2. Search architecture differences
3. Search licensing and governance differences
4. Search performance comparisons (with sources, note vendor bias)
5. Organize into report, add links to all citations
6. Validate all links with codex or user verification
7. Fix any 404 links with replacements
