---
name: websearch-quick
description: "Fast, targeted single-pass search strategy for simple factual lookups. 1-iteration workflow with authoritative source verification and minimal citations. Use for version lookups, documentation finding, simple definitions, existence checks. Keywords: what version, find docs, link to, what is, does X support."
---

# Quick Web Research Strategy

## What This Skill Does

Provides fast, targeted search methodology for simple questions requiring direct factual answers from authoritative sources. Implements single-pass workflow with precise query formulation and minimal citation overhead.

## When to Use This Skill

Use this skill when the research question requires:
- **Version lookups**: "What version of React Router was released in 2025?"
- **Documentation finding**: "Find docs for Terraform AWS provider"
- **Simple definitions**: "What is GraphQL?"
- **Existence checks**: "Does Next.js support Server Components?"
- **URL/link requests**: "Link to Python asyncio documentation"

**Triggers**: Keywords like "what version", "find docs", "link to", "what is", "does X support", "URL for"

## Instructions

### Single-Pass Workflow

**Objective**: Execute 1-2 targeted queries, identify 1-2 authoritative sources, extract concise answer.

#### Step 1: Targeted Query Formulation (1-2 Queries)

Generate 1-2 highly specific queries using advanced operators:

**Query Strategy**:
- **Official Source Priority**: Use `site:` operator for authoritative domains
- **File Type Targeting**: Use `filetype:` for specific document types
- **Exact Phrase Matching**: Use `"exact phrase"` for precision
- **Recent Content**: Use `after:YYYY` for latest information

**Examples**:
```
Version Lookup:
- site:npmjs.com "react-router" "version"
- site:github.com "react-router" "releases" after:2025

Documentation Finding:
- site:terraform.io "aws provider" "documentation"
- site:docs.python.org "asyncio"

Simple Definition:
- site:graphql.org "what is GraphQL"
- "GraphQL definition" site:official-docs

Existence Check:
- site:nextjs.org "Server Components" "support"
- "Next.js Server Components" site:vercel.com
```

#### Step 2: Authoritative Source Identification (1-2 Sources)

**Target Authoritative Sources**:
- **Official documentation**: Framework/library official sites
- **Package registries**: npm, PyPI, Maven Central
- **Official GitHub repos**: Releases, changelog
- **Peer-reviewed sources**: Academic papers (rare for quick lookups)

**Credibility Hierarchy**:
1. **Official docs** (highest authority)
2. **Official GitHub/package registry**
3. **Established tech publications** (MDN, Smashing Magazine)
4. **Community sources** (Stack Overflow) - only if official unavailable

#### Step 3: Extract Concise Answer

Extract direct answer with minimal context:

**Answer Format**:
```markdown
{Concise 1-3 sentence answer with inline citation [1]}

Optional: {1 sentence additional context if needed} [2]
```

**Examples**:
```markdown
Version Lookup:
React Router v7.2.0 was released on March 15, 2025 [1]. The release introduced new data loading APIs and improved TypeScript support [1].

Documentation Finding:
The Terraform AWS Provider documentation is available at https://registry.terraform.io/providers/hashicorp/aws/latest/docs [1].

Simple Definition:
GraphQL is a query language for APIs that allows clients to request exactly the data they need [1].

Existence Check:
Yes, Next.js 14+ supports Server Components as a stable feature [1]. Server Components are enabled by default in the App Router [1].
```

#### Step 4: Minimal Citation

Provide 1-2 citations with essential information only:

**Citation Format**:
```markdown
[1] **{Source Title}**
    - URL: {URL}
    - Author/Org: {organization}
    - Date: {YYYY-MM-DD}
    - Excerpt: "{1-sentence quote}"
```

**Example**:
```markdown
[1] **React Router v7 Release Notes**
    - URL: https://github.com/remix-run/react-router/releases/tag/v7.2.0
    - Author/Org: Remix Team
    - Date: 2025-03-15
    - Excerpt: "React Router v7.2.0 introduces new data loading APIs..."
```

#### Step 5: Verify Factual Accuracy

Quick verification checklist:
- [ ] Answer directly addresses the question?
- [ ] Source is authoritative (official or highly credible)?
- [ ] Information is recent (if time-sensitive)?
- [ ] Citation includes URL for user verification?

**No iteration** - single pass only for quick mode.

### Output Template

```markdown
# Web Research Analysis (Quick Mode)

**Research Mode**: quick
**Objective**: {1-sentence: what was researched}

---

## Answer

{Concise 1-3 sentence answer with inline citations [1][2]}

---

## Source Citations

[1] **{Source Title}**
    - URL: {URL}
    - Author/Org: {author/org}
    - Date: {date}
    - Excerpt: "{quote}"

[2] **{Source Title}** (if applicable)
    - URL: {URL}
    - Author/Org: {author/org}
    - Date: {date}
    - Excerpt: "{quote}"
```

## Examples

### Example 1: Version Lookup

**Scenario**: "What version of React Router was released in 2025?"

**Process**:
```
Query (1):
site:github.com "react-router" "releases" "2025"

Source Identified (1):
React Router GitHub Releases [1]

Answer Extracted:
React Router v7.2.0 was released on March 15, 2025 [1].

Citation:
[1] React Router v7.2.0 Release
    - URL: https://github.com/remix-run/react-router/releases/tag/v7.2.0
    - Author/Org: Remix Team
    - Date: 2025-03-15
    - Excerpt: "v7.2.0 Release Notes..."

Verification: ✅ Authoritative (official repo), ✅ Recent, ✅ Directly answers question
```

**Output**: Quick Mode Context File with concise answer and 1 citation

### Example 2: Documentation Finding

**Scenario**: "Find docs for Python asyncio"

**Process**:
```
Query (1):
site:docs.python.org "asyncio"

Source Identified (1):
Python Official Documentation [1]

Answer Extracted:
The Python asyncio documentation is available at https://docs.python.org/3/library/asyncio.html [1].

Citation:
[1] Python asyncio Documentation
    - URL: https://docs.python.org/3/library/asyncio.html
    - Author/Org: Python Software Foundation
    - Date: 2025-01-10 (last updated)
    - Excerpt: "asyncio is a library to write concurrent code using async/await syntax."

Verification: ✅ Official docs, ✅ Recent, ✅ Direct link
```

**Output**: Quick Mode summary with documentation URL

### Example 3: Simple Definition

**Scenario**: "What is GraphQL?"

**Process**:
```
Queries (2):
- site:graphql.org "what is GraphQL"
- "GraphQL definition"

Sources Identified (1 primary):
GraphQL Official Site [1]

Answer Extracted:
GraphQL is a query language for APIs and a runtime for fulfilling queries with existing data [1].
It was developed by Facebook and provides a complete description of the data in your API [1].

Citations:
[1] GraphQL Introduction
    - URL: https://graphql.org/
    - Author/Org: GraphQL Foundation
    - Date: 2024-12-01 (last updated)
    - Excerpt: "GraphQL is a query language for APIs and a runtime for fulfilling those queries..."

Verification: ✅ Official source, ✅ Clear definition
```

**Output**: Quick Mode summary with definition and official citation

### Example 4: Existence Check

**Scenario**: "Does Next.js support Server Components?"

**Process**:
```
Query (1):
site:nextjs.org "Server Components" "support"

Source Identified (1):
Next.js Official Documentation [1]

Answer Extracted:
Yes, Next.js 14+ supports Server Components as a stable feature [1]. Server Components are
enabled by default in the App Router and allow rendering components on the server [1].

Citation:
[1] Next.js Server Components Documentation
    - URL: https://nextjs.org/docs/app/building-your-application/rendering/server-components
    - Author/Org: Vercel
    - Date: 2025-01-20
    - Excerpt: "Server Components are a new feature that allow you to render components on the server..."

Verification: ✅ Official docs, ✅ Recent, ✅ Confirms existence and provides context
```

**Output**: Quick Mode summary confirming Server Components support

## Best Practices

- **Official Sources First**: Always try `site:official-domain.com` before broader searches
- **Be Specific**: Use exact version numbers, product names, specific terminology
- **Avoid Over-Research**: 1-2 sources sufficient for factual lookups - don't overthink
- **Verify Recency**: For technology topics, check publication/update date
- **Direct Answers Only**: No analysis, no comparison, no deep dive - just the answer
- **Single Iteration**: Never iterate in quick mode - if answer unclear, escalate to standard mode

## Common Patterns

### Pattern 1: Version Lookup
```
Query: site:{official-repo} "{package}" "version" "release" after:YYYY
Source: GitHub releases, npm registry, official changelog
Answer: "{Package} v{X.Y.Z} released on {date} [1]"
```

### Pattern 2: Documentation URL
```
Query: site:{official-docs-domain} "{topic}"
Source: Official documentation site
Answer: "Documentation available at {URL} [1]"
```

### Pattern 3: Yes/No Existence Check
```
Query: site:{official-site} "{feature}" "support"
Source: Official feature documentation
Answer: "Yes/No, {product} supports {feature} [1]. {1-sentence context} [1]"
```

## Troubleshooting

**Issue 1: Multiple Conflicting Versions**
- Check official source first (GitHub releases, official site)
- Verify date (latest is correct for "current version" questions)
- If user asks about specific date, note date in answer

**Issue 2: No Official Documentation Found**
- Try package registry (npm, PyPI)
- Check official GitHub repo
- If still not found, note "No official documentation found; community resources available at {URL}"

**Issue 3: Question More Complex Than Expected**
- Don't force quick mode for complex questions
- Note in output: "Question requires deeper analysis; recommend /research:standard or /research:deep"
- Provide best-effort answer with caveat

## Integration Points

- **WebSearch Tool**: Execute 1-2 targeted queries only
- **Official Sources**: Prioritize `site:` operator for authoritative domains
- **Context Files**: Persist minimal findings to `.agent/Session-{name}/context/research-web-analyst.md`
- **No MCP Servers**: Quick mode avoids external dependencies for speed

## Key Terminology

- **Targeted Query**: Highly specific search using advanced operators
- **Authoritative Source**: Official documentation, package registry, official repo
- **Single-Pass**: One iteration only, no refinement
- **Concise Answer**: 1-3 sentences directly addressing question
- **Minimal Citation**: 1-2 sources with essential metadata only

## Additional Resources

- Google Search Operators: https://ahrefs.com/blog/google-advanced-search-operators/
- Official Documentation Sites: Language/framework official domains
- Package Registries: npm (https://npmjs.com), PyPI (https://pypi.org), Maven (https://mvnrepository.com)
