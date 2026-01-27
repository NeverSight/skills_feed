---
name: research
description: Structured web research with multi-source validation. Output reports with complete citation links. Focus on key results, verify information quality.
---

# Technical Research Skill

Structured research workflow for gathering, validating, and synthesizing information from multiple sources.

## Core Principles

1. **Tool-agnostic**: Use available search tools (WebSearch, WebFetch, or alternatives)
2. **Multi-source validation**: Cross-reference claims across sources
3. **Quality over quantity**: Focus on authoritative, recent sources
4. **Complete citations**: All claims need clickable sources
5. **Bias awareness**: Note vendor bias, sponsored content

## Available Tools

Research uses these capabilities (implementation varies by environment):

| Capability | Primary Tool | Fallback |
|------------|--------------|----------|
| Web Search | WebSearch | codex --enable web_search_request |
| Page Fetch | WebFetch | codex with URL |
| Link Validation | WebFetch (HEAD) | Manual verification |

**Tool Selection**:
- Use built-in WebSearch/WebFetch when available (faster, no external deps)
- Fall back to codex skill when built-in tools are unavailable
- Let user verify simple URLs by clicking (fastest)

## Research Depth Levels

### Quick Research (3-5 sources)
- **Use when**: Simple factual questions, quick comparisons
- **Output**: 1-2 paragraphs with key links

### Standard Research (8-12 sources)
- **Use when**: Technical comparisons, feature analysis
- **Output**: Structured report with sections

### Deep Research (15+ sources)
- **Use when**: Architecture decisions, comprehensive analysis
- **Output**: Full report with cross-references, trade-off analysis
- **Additional steps**: Multiple search iterations, source triangulation, expert opinion synthesis

## Research Workflow

### Phase 1: Scoping

#### 1. Clarify Research Goals

Confirm with user:
- What's the core question?
- What needs comparison?
- Which aspects matter? (architecture/performance/use cases/cost)
- Depth level: Quick / Standard / Deep

#### 2. Define Search Strategy

Plan before searching:
- Primary keywords + synonyms
- Year constraints (default: current year - 1 to current)
- Domain restrictions (official docs, academic, community)
- Negative keywords (exclude irrelevant results)

### Phase 2: Collection

#### 3. Multi-Angle Search

Execute parallel searches across different angles:

| Angle | Query Pattern | Example |
|-------|---------------|---------|
| Factual | "What is X", "X definition" | "What is OpenSearch" |
| Comparative | "X vs Y", "X alternatives" | "OpenSearch vs Elasticsearch differences" |
| Technical | "X architecture", "X implementation" | "OpenSearch architecture internals" |
| Practical | "X tutorial", "X best practices" | "OpenSearch best practices 2024" |
| Recent | "X 2024 2025", "X latest" | "OpenSearch new features 2024 2025" |

**Query Tips**:
- Add year constraints for recent info
- Include exact product name in query
- Focus each query on single topic

#### 4. Source Diversification

Ensure coverage across source types:
- [ ] Official documentation (at least 2 sources)
- [ ] Official blogs/announcements
- [ ] Independent technical analysis
- [ ] Community discussions (GitHub issues, Stack Overflow)
- [ ] Academic papers (if applicable)

### Phase 3: Validation

#### 5. Cross-Reference Verification

For each key claim:
- Find at least 2 independent sources confirming
- Note conflicting information
- Identify primary vs secondary sources

**Triangulation Method**:
1. Official source (docs, blog)
2. Independent analysis
3. Community validation (issues, discussions)

#### 6. Link Validation

Before finalizing report:
- Verify all URLs are accessible (use WebFetch or manual check)
- Replace 404 links with alternatives
- Ensure reference names match page content

**Validation Rules**:
- Let user verify simple URLs by clicking (faster)
- Use WebFetch for batch verification when needed
- Search for replacement URLs for broken links

### Phase 4: Synthesis

#### 7. Information Quality Assessment

Rate each source:

| Criteria | Weight | Scoring |
|----------|--------|---------|
| Authority | 30% | Official docs (5) > Official blog (4) > Tech publication (3) > Community (2) > Anonymous (1) |
| Recency | 25% | <6mo (5) > 6-12mo (4) > 1-2yr (3) > 2-3yr (2) > >3yr (1) |
| Specificity | 25% | Detailed with examples (5) > General overview (3) > Vague (1) |
| Independence | 20% | Unbiased (5) > Slight bias (3) > Vendor content (1) |

#### 8. Conflict Resolution

When sources disagree:
1. Prefer official documentation
2. Check publication dates (newer often wins for tech)
3. Note the disagreement in report
4. Provide both perspectives if unresolved

**Conflict Template**:
```markdown
> **Conflicting Information**
> - Source A claims: [X]
> - Source B claims: [Y]
> - Resolution: [Your analysis or "Both perspectives included"]
```

#### 9. Organize and Analyze

- Filter valuable information
- Structure by user's priority
- Add analysis and insights
- Unify citation format

### Phase 5: Delivery

#### 10. Final Review Checklist

- [ ] All claims have citations
- [ ] All links validated
- [ ] No fabricated data
- [ ] Balanced perspective (vendor bias noted)
- [ ] Matches user's depth requirement
- [ ] Version information included where relevant

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

## Source Priority

1. **Official documentation** - Most authoritative, prefer when available
2. **Official blogs/announcements** - For news, releases, roadmaps
3. **Third-party tech blogs** - Only if official docs lack detail; verify quality first
4. **Independent benchmarks** - For performance data (note: vendor benchmarks may be biased)

**Note**: Third-party blogs may have lower quality. Always verify content accuracy before using.

## Guidelines

- **Don't fabricate data**: No performance numbers without sources
- **Trim sections**: Only keep what users care about
- **Valid links**: Prefer official docs, reputable tech blogs
- **Declarative titles**: Don't use questions as headings
- **Reference name accuracy**: Ensure `[Reference Name]` matches actual page content
- **Version awareness**: Note software versions, flag deprecated features

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Search returns wrong product | Always include exact product name in query |
| 404 links in final report | Validate all links before finalizing |
| Reference name doesn't match content | Verify page content matches reference name |
| Using vendor benchmarks as neutral | Note the source bias in report |
| Overly broad search queries | Focus each query on single topic |
| Missing year constraints | Add current/recent years for tech info |
| Single source for key claims | Cross-reference with at least 2 sources |
| Outdated information | Check publication date, prefer recent sources |

## Example Research Task

User: Research differences between OpenSearch and Elasticsearch

Steps:
1. Clarify depth level with user (Quick/Standard/Deep)
2. Search OpenSearch unique features (include "OpenSearch" in query)
3. Search architecture differences
4. Search licensing and governance differences
5. Search performance comparisons (with sources, note vendor bias)
6. Cross-reference key claims across sources
7. Assess source quality (authority, recency, bias)
8. Organize into report, add links to all citations
9. Validate all links with WebFetch or user verification
10. Fix any 404 links with replacements
