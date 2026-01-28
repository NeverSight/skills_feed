---
name: research
description: Use when you need to research, analyze, and plan technical solutions that are scalable, secure, and maintainable.
license: MIT
---

# Research

Always honor **YAGNI**, **KISS**, **DRY**. Be honest, brutal, straight to the point, concise.

## Workflow

### Phase 1: Scope Definition

- Identify key terms, concepts, recency requirements
- Establish evaluation criteria and research depth boundaries

### Phase 2: Information Gathering

1. **Search Strategy** (max **5 tool calls**, respect user limit):
   - Prefer `gemini -m gemini-2.5-flash -p "..."` bash command (timeout: 10min), save output using `Report:` path
   - Fallback to `WebSearch` tool if gemini unavailable
   - Run searches in parallel; use precise queries with "best practices", "2024", "latest"
   - Prioritize official docs, GitHub repos, authoritative sources

2. **Deep Analysis**: Use `docs-seeker` skill for GitHub repos. Focus on official docs, API refs, changelogs.

3. **Cross-Reference**: Verify across multiple sources, check dates, note conflicts.

### Phase 3: Analysis & Synthesis

- Identify common patterns, pros/cons, maturity, security implications
- Assess compatibility, integration requirements, performance

### Phase 4: Report Generation

Save reports using `Report:` path from `## Naming` section. If unavailable, ask main agent.

```markdown
# Research Report: [Topic]

## Executive Summary
## Research Methodology (sources, date range, search terms)
## Key Findings
### Technology Overview
### Current State & Trends
### Best Practices
### Security Considerations
### Performance Insights
## Comparative Analysis
## Implementation Recommendations
### Quick Start Guide
### Code Examples
### Common Pitfalls
## Resources & References
```

## Quality Standards

- **Accuracy**: Verified across multiple sources
- **Currency**: Prioritize last 12 months
- **Actionability**: Practical, implementable recommendations
- **Attribution**: Always cite sources with links

## Output Requirements

1. Save using `Report:` path with descriptive filename
2. Include timestamp, section navigation, syntax-highlighted code blocks
3. Conclude with specific, actionable next steps

**IMPORTANT:** Sacrifice grammar for concision. List unresolved questions at end.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
