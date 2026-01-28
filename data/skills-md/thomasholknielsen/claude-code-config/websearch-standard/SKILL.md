---
name: websearch-standard
description: "Standard multi-source verification search strategy for moderate complexity research. 2-iteration workflow with source ranking, consensus identification, and citation transparency. Use for feature comparisons, moderate complexity topics, fact-checking. Keywords: compare, differences, features, fact-check, verify, what are."
---

# Standard Web Research Strategy

## What This Skill Does

Provides balanced research methodology for moderate complexity questions requiring multi-source verification but not full decomposition. Implements 2-iteration workflow with source evaluation, consensus identification, and citation transparency.

## When to Use This Skill

Use this skill when the research question requires:
- **Feature comparisons**: "What are the differences between GraphQL and REST?"
- **Moderate complexity topics**: Well-documented subjects with established consensus
- **Fact-checking**: Verifying claims or information across sources
- **Recent news/updates**: "What's new in React 19?"
- **Technology overviews**: Understanding a framework, tool, or concept

**Triggers**: Keywords like "compare", "differences", "features", "what are", "fact-check", "verify", "overview"

## Instructions

### Iteration 1: Multi-Source Research

**Objective**: Formulate query variations, identify authoritative sources, evaluate quality.

#### Step 1: Query Formulation (2-3 Variations)

Generate 2-3 query variations with different angles:
- **Variation 1 - Direct**: "GraphQL vs REST API differences"
- **Variation 2 - Technical**: "GraphQL REST comparison performance"
- **Variation 3 - Best Practices**: "when to use GraphQL vs REST"

**Search Operators**:
- `site:domain.com` - Specific domains
- `filetype:pdf` - PDF documents
- `intitle:"keyword"` - Page titles
- `after:2024` - Recent content
- `"exact phrase"` - Exact matching

#### Step 2: Source Identification (5-8 Sources)

Execute queries and identify 5-8 sources with diverse perspectives:
- 2-3 Official documentation sources
- 2-3 Established tech publications
- 1-2 Community sources (Stack Overflow, forums)

#### Step 3: Source Evaluation

Rank each source on three dimensions (0-10 scale):

**Credibility** (0-10):
- **10**: Official docs, peer-reviewed
- **7-9**: Established publications (MDN, Smashing Magazine)
- **4-6**: Technical blogs, Stack Overflow
- **1-3**: Unverified sources

**Freshness** (0-10):
- **10**: Last 3 months
- **7-9**: Last 6-12 months
- **4-6**: Last 1-2 years
- **1-3**: Older than 2 years

**Relevance** (0-10):
- **10**: Directly addresses question with examples
- **7-9**: Addresses with partial detail
- **4-6**: Tangentially related
- **1-3**: Minimal value

**Overall Quality** = (Credibility × 0.5) + (Freshness × 0.2) + (Relevance × 0.3)

#### Step 4: Extract Key Findings

For each source, extract 2-3 key findings with inline citations:
```markdown
GraphQL uses a single endpoint [1] while REST uses multiple resource-specific endpoints [2].
GraphQL allows clients to specify exact data needs [1][3], reducing over-fetching compared to REST [2].
```

### Iteration 2: Verification & Synthesis

**Objective**: Cross-reference findings, identify consensus, generate recommendations.

#### Step 5: Cross-Reference (3+ Sources)

For each key finding:
- **Consensus**: 3+ sources agree → strong signal
- **Partial agreement**: 2 sources agree → moderate confidence
- **Outlier**: Single source → flag as unverified or context-specific

Example:
```markdown
**Consensus View** (5 sources): GraphQL reduces network overhead for complex data needs [1][2][3][4][5]
**Partial Agreement** (2 sources): GraphQL has steeper learning curve [2][6]
**Outlier** (1 source): REST always faster for simple queries [7] - context: depends on caching strategy
```

#### Step 6: Identify Contradictions

When sources conflict:
1. Check dates (newer may reflect updates)
2. Assess authority (official > community)
3. Look for context (scenario-dependent)
4. Present both views with citations

Example:
```markdown
**Contradiction Noted**: Source A [1] recommends GraphQL for microservices, while Source B [2] suggests REST
is simpler for microservice communication. Context: GraphQL better for client-facing APIs [1],
REST better for service-to-service internal communication [2].
```

#### Step 7: Generate Recommendations

Create actionable recommendations based on verified findings:

**Critical (High Confidence - 3+ Sources)**:
- [ ] {Recommendation with strong evidence} [1][2][3]

**Important (Moderate Confidence - 2 Sources)**:
- [ ] {Recommendation with partial evidence} [4][5]

**Enhancements (Context-Specific)**:
- [ ] {Recommendation with caveats} [6]

#### Step 8: Citation Reference Table

Create structured citation table:
```markdown
[1] **GraphQL Official Docs** - https://graphql.org/learn/
    Author/Org: GraphQL Foundation
    Date: 2025-01-15
    Excerpt: "GraphQL is a query language for APIs and a runtime..."

[2] **REST API Best Practices** - https://restfulapi.net/
    Author/Org: REST API Tutorial
    Date: 2024-11-20
    Excerpt: "REST uses HTTP methods to operate on resources..."
```

#### Step 9: Completeness Validation

Check completeness (target ≥ 85%):
- [ ] Research objective addressed?
- [ ] 5-8 sources consulted (3+ authoritative)?
- [ ] Key findings have 3+ source citations?
- [ ] Contradictions identified and explained?
- [ ] Recommendations provided?

**If <85% complete**: Note gaps in output, do NOT iterate further (max 2 iterations for standard mode)

### Output Template

```markdown
# Web Research Analysis (Standard Mode)

**Research Mode**: standard
**Objective**: {1-sentence: what was researched}

---

## Key Findings

{2-3 paragraph synthesis with inline citations [1][2][3]}

**Consensus Views**: {areas where 3+ sources agree}
**Contradictions**: {conflicting information with context}

---

## Methodology

**Queries Executed**: {count} query variations
- {query 1 with operators}
- {query 2 with operators}

**Sources Consulted**: {count} total ({count} authoritative, {count} recent)
**Iterations**: 2 (multi-source verification complete)

---

## Verified Sources

| # | Title | Author/Org | Date | Credibility | Freshness | Relevance | Overall |
|---|-------|------------|------|-------------|-----------|-----------|---------|
| [1] | {title} | {author} | {date} | {score} | {score} | {score} | {calc} |
| [2] | {title} | {author} | {date} | {score} | {score} | {score} | {calc} |

---

## Actionable Recommendations

### Critical (Do First) {count}
- [ ] {Specific recommendation with rationale} [1][2]

### Important (Do Next) {count}
- [ ] {Specific recommendation with rationale} [3][4]

### Enhancements (Nice to Have) {count}
- [ ] {Specific recommendation with rationale} [5]

---

## Citations

[1] **{Source Title}** - {URL} ({Author/Org}, {Date})
    Excerpt: "{relevant quote}"

[2] **{Source Title}** - {URL} ({Author/Org}, {Date})
    Excerpt: "{relevant quote}"

{...continue...}
```

## Examples

### Example 1: Feature Comparison

**Scenario**: "What are the main differences between GraphQL and REST APIs?"

**Process**:

**Iteration 1 - Multi-Source Research**:
```
Queries (3 variations):
- "GraphQL vs REST API differences"
- "GraphQL REST comparison 2025"
- "when to use GraphQL vs REST"

Sources Identified (8):
- GraphQL Official Docs (Cred: 10, Fresh: 10, Rel: 10) [1]
- MDN REST Guide (Cred: 10, Fresh: 9, Rel: 10) [2]
- Apollo GraphQL Blog (Cred: 9, Fresh: 10, Rel: 10) [3]
- Smashing Magazine Article (Cred: 8, Fresh: 8, Rel: 9) [4]
- Stack Overflow Discussion (Cred: 6, Fresh: 7, Rel: 8) [5]
- Dev.to Comparison (Cred: 7, Fresh: 10, Rel: 9) [6]
- API Design Patterns Book (Cred: 9, Fresh: 6, Rel: 9) [7]
- Hacker News Thread (Cred: 6, Fresh: 10, Rel: 7) [8]

Key Findings Extracted:
- GraphQL single endpoint vs REST multiple endpoints [1][2]
- GraphQL client-specified queries reduce over-fetching [1][3][4]
- REST simpler caching due to HTTP standards [2][7]
- GraphQL steeper learning curve [3][6][8]
```

**Iteration 2 - Verification & Synthesis**:
```
Cross-Reference:
- Consensus (7 sources): GraphQL reduces over/under-fetching [1][2][3][4][5][6][7]
- Consensus (5 sources): REST has better caching support [2][4][5][7][8]
- Partial Agreement (3 sources): GraphQL better for complex data needs [1][3][6]

Contradictions:
- Performance: GraphQL faster [3][6] vs REST faster [7][8]
  Context: Depends on use case - GraphQL for complex client needs, REST for simple CRUD

Recommendations Generated:
- Critical: Use GraphQL for complex client data requirements with nested relationships [1][3]
- Important: Use REST for simple CRUD operations with well-defined resources [2][7]
- Enhancement: Consider REST for public APIs needing extensive caching [2][7]

Completeness: 92% (8 sources, all findings verified, contradictions explained)
```

**Output**: Standard Mode Context File with key findings, 8 source citations, consensus views, contradiction analysis, recommendations

### Example 2: Technology Update Research

**Scenario**: "What's new in React 19?"

**Process**:

**Iteration 1**:
```
Queries:
- "React 19 new features"
- site:react.dev "React 19" "what's new"
- "React 19 changes" after:2024

Sources (6):
- React Official Blog [1]
- React GitHub Changelog [2]
- Vercel Blog [3]
- React Newsletter [4]
- Dev Community Posts [5][6]

Findings:
- New React Compiler (automatic optimization) [1][2]
- Improved Server Components [1][3]
- Actions API for form handling [1][4]
- use() Hook for async data [1][2]
```

**Iteration 2**:
```
Cross-Reference:
- Consensus (4 sources): React Compiler auto-optimizes components [1][2][3][4]
- Consensus (3 sources): Actions simplify form state management [1][4][6]

Completeness: 88%
```

**Output**: Standard Mode summary with React 19 features, 6 citations, migration considerations

## Best Practices

- **Balance Breadth and Depth**: Aim for 5-8 sources, not 20+ (diminishing returns)
- **Prioritize Quality Over Quantity**: 3 authoritative sources beat 10 low-quality ones
- **Verify Before Recommending**: Every recommendation needs 2-3 source citations minimum
- **Note Recency**: For technology topics, flag sources >1 year old
- **Consensus Matters**: Findings supported by 3+ sources are high-confidence
- **Context Contradictions**: Don't hide conflicts - explain why sources disagree
- **Stay Focused**: Stick to 2 iterations max - if incomplete, note gaps

## Common Patterns

### Pattern 1: Technology Comparison (A vs B)
```
Iteration 1:
- Query: "{A} vs {B}", "{A} {B} comparison", "when to use {A} vs {B}"
- Sources: Official docs for both, tech publications, community discussions
- Extract: Key differences, use cases, trade-offs

Iteration 2:
- Cross-reference: Consensus on strengths/weaknesses
- Synthesize: Decision matrix (when to use A vs B)
```

### Pattern 2: Fact-Checking
```
Iteration 1:
- Query: Claim keywords, source verification queries
- Sources: Primary sources, authoritative refs, fact-checking sites
- Extract: Evidence for/against claim

Iteration 2:
- Verify: Check dates, authority, context
- Synthesize: True/False/Nuanced with citations
```

### Pattern 3: Technology Overview
```
Iteration 1:
- Query: "{Technology} overview", "{Technology} use cases", "{Technology} best practices"
- Sources: Official docs, getting started guides, tutorials
- Extract: What it is, when to use, how it works

Iteration 2:
- Verify: Consensus on core concepts
- Synthesize: Quick reference guide with citations
```

## Troubleshooting

**Issue 1: Conflicting Information Across Sources**
- Check publication dates (recent vs outdated)
- Assess source authority (official vs opinion)
- Look for context (scenario-specific recommendations)
- Present both views with citations and context

**Issue 2: Insufficient Authoritative Sources**
- Broaden search to related domains
- Include slightly older but highly credible sources
- Note in output: "Limited recent authoritative sources; recommendations based on 2023-2024 data"

**Issue 3: Completeness Below 85%**
- Note specific gaps in output
- Do NOT iterate beyond 2 iterations (standard mode limit)
- Recommend user consider deep mode for comprehensive analysis

## Integration Points

- **WebSearch Tool**: Execute all queries through WebSearch
- **Context7 MCP**: Supplement with official framework docs when applicable
- **Source Table**: Track sources in structured format for quality tracking
- **Context Files**: Persist findings to `.agent/Session-{name}/context/research-web-analyst.md`

## Key Terminology

- **Query Variation**: Different phrasing/angle of same search
- **Source Quality Score**: Composite metric (credibility + freshness + relevance)
- **Consensus View**: Finding supported by 3+ sources
- **Contradiction**: Conflicting claims requiring contextual explanation
- **Completeness**: Percentage of research objectives met (target ≥85%)
- **Iteration**: Research cycle (max 2 for standard mode)

## Additional Resources

- Advanced Search Operators: https://ahrefs.com/blog/google-advanced-search-operators/
- Source Evaluation: https://guides.library.cornell.edu/evaluate
- Citation Formats: https://apastyle.apa.org/
