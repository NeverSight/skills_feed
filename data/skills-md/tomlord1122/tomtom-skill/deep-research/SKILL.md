---
name: deep-research
description: Deep research expert for comprehensive technical investigations. Use when conducting technology evaluations, comparing solutions, analyzing papers, or exploring technical trends.
---

# Deep Research Expert

Expert assistant for comprehensive technical research, multi-source information synthesis, technology evaluation, and trend analysis.

## How It Works

1. Defines research scope and key questions
2. Gathers information from multiple sources (docs, web, Context7)
3. Analyzes and synthesizes findings
4. Produces structured research reports
5. Provides actionable recommendations

## Research Methodology

### Phase 1: Problem Definition
- Clarify research scope
- Identify key questions
- Establish evaluation criteria

### Phase 2: Information Gathering
- Official documentation (WebFetch)
- Technical blogs and discussions (WebSearch)
- GitHub project analysis
- Context7 documentation queries
- Academic papers if relevant

### Phase 3: Analysis Framework

**Technology Maturity Assessment:**
| Level | Description |
|-------|-------------|
| Emerging | < 1 year, experimental |
| Growing | 1-3 years, production-ready |
| Mature | 3+ years, widespread adoption |
| Declining | Decreasing activity |

**Community Health Metrics:**
- GitHub stars and growth rate
- Issue response time
- Release frequency
- Contributor diversity

**Performance Considerations:**
- Benchmark data availability
- Real-world case studies
- Scaling characteristics

### Phase 4: Synthesis
- Compare options against criteria
- Identify trade-offs
- Form recommendations

## Research Output Format

```markdown
# [Research Topic] Deep Research Report

## Executive Summary
[2-3 sentences summarizing key findings and recommendations]

## Background & Problem Statement
[Why this research is needed]

## Research Questions
1. [Question 1]
2. [Question 2]

## Findings

### Option A: [Name]
**Overview:** [Brief description]

**Strengths:**
- Point 1
- Point 2

**Weaknesses:**
- Point 1
- Point 2

**Best For:** [Use cases]

### Option B: [Name]
[Same structure]

## Comparative Analysis

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Maturity  | Mature   | Growing  | Emerging |
| Learning Curve | Medium | Low | High |
| Performance | High | Medium | High |
| Community | Active | Very Active | Small |

## Risk Assessment
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Recommendations
1. **Primary recommendation**: [Option] because [reasons]
2. **Alternative**: [Option] if [conditions]

## Implementation Roadmap
1. Step 1
2. Step 2
3. Step 3

## References
- [Source 1](url)
- [Source 2](url)
```

## Research Tips

### Effective Web Searches
- Use specific technical terms
- Include version numbers when relevant
- Search for "[technology] vs [alternative]"
- Look for "[technology] production experience"

### Evaluating Sources
- Prefer official documentation
- Check article/post dates
- Look for hands-on experience reports
- Verify claims with multiple sources

### Context7 Usage
- Resolve library ID first: `mcp__context7__resolve-library-id`
- Query with specific questions: `mcp__context7__query-docs`

## Present Results to User

When delivering research:
- Start with executive summary
- Provide clear recommendations
- Include comparative tables
- List sources for verification
- Acknowledge limitations

## Troubleshooting

**"Conflicting information found"**
- Note the discrepancy in report
- Check source dates (newer may be more accurate)
- Look for official clarification
- Present both perspectives if unresolved

**"Insufficient information"**
- Expand search terms
- Try different source types
- Acknowledge gaps in report
- Suggest ways to gather more data
