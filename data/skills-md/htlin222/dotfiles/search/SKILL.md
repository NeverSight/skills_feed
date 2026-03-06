---
name: search
description: Expert web research with advanced search techniques. Use for deep research, information gathering, or fact verification.
---

# Search Research

Find and synthesize information effectively.

## When to use

- Deep research tasks
- Fact verification
- Competitive analysis
- Documentation lookup
- Trend analysis

## Search strategies

### Query formulation

```
# Exact phrase
"error handling best practices"

# Exclude terms
python tutorial -beginner

# Site-specific
site:github.com react hooks

# File type
filetype:pdf security audit

# Date range (use WebSearch date filtering)
react 18 features 2024
```

### Domain filtering

```python
# WebSearch with domain filtering
WebSearch(
    query="kubernetes best practices",
    allowed_domains=["kubernetes.io", "cloud.google.com", "docs.aws.amazon.com"],
)

# Exclude unreliable sources
WebSearch(
    query="health benefits of X",
    blocked_domains=["pinterest.com", "quora.com"],
)
```

## Research workflow

### 1. Scope definition

- What specific question needs answering?
- What type of sources are authoritative?
- What time period is relevant?

### 2. Initial search

```python
# Broad search first
queries = [
    "main topic overview",
    "main topic best practices",
    "main topic common problems",
]
```

### 3. Deep dive

```python
# Follow up on promising results
for result in initial_results:
    if is_authoritative(result):
        content = WebFetch(url=result.url, prompt="Extract key findings")
        facts.append(content)
```

### 4. Verification

- Cross-reference claims across sources
- Check publication dates
- Verify author credentials
- Look for primary sources

## Output format

```markdown
## Research Summary: [Topic]

### Key Findings

1. **Finding 1** - [Source](url)
   - Supporting detail
   - Supporting detail

2. **Finding 2** - [Source](url)
   - Supporting detail

### Consensus

- Points that multiple sources agree on

### Contradictions

- Areas where sources disagree

### Gaps

- Questions that couldn't be answered

### Sources

- [Title](url) - Credibility: High/Medium/Low
```

## Source evaluation

| Indicator | High Credibility               | Low Credibility         |
| --------- | ------------------------------ | ----------------------- |
| Domain    | .gov, .edu, major publications | Unknown, user-generated |
| Author    | Named expert, organization     | Anonymous, unclear      |
| Date      | Recent, regularly updated      | Outdated, no date       |
| Citations | Links to sources               | No references           |
| Bias      | Balanced, factual              | Promotional, extreme    |

## Examples

**Input:** "Research best auth solutions for SaaS"
**Action:** Search auth providers, compare features, check reviews, summarize

**Input:** "Verify this claim about performance"
**Action:** Find benchmarks, check methodology, cross-reference results
