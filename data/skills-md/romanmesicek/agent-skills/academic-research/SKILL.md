---
name: academic-research
description: |
  Systematic academic literature search with source prioritization and APA 7th edition citations.
  Use when the user needs to research a topic with scholarly sources, verify claims with academic
  backing, find peer-reviewed evidence, compile research findings, or generate properly cited reports.
  Triggers: "research [topic]", "what does the research say about...", "find studies on...",
  "verify this claim...", "literature review", "academic sources for...", "peer-reviewed evidence",
  "scholarly articles about...", "evidence-based", "cite sources for...". This skill provides
  basic APA citation capabilities; for advanced citation work (complex source types, edge cases,
  batch formatting), consider the `apa-style-citation` skill which offers enhanced citation expertise.
---

# Academic Research Skill

Systematic literature search with source prioritization and APA 7th edition citations.

## Research Workflow

### 1. Search Strategy (Execute in Order)

**Phase 1 - Academic databases (Priority 1-2):**
- `site:scholar.google.com [topic]`
- `site:pubmed.ncbi.nlm.nih.gov [topic]`
- `site:semanticscholar.org [topic]`
- `site:arxiv.org [topic]`

**Phase 2 - Institutional (Priority 3-4):**
- `site:edu [topic] research`
- `site:gov [topic]`
- `site:who.int OR site:un.org [topic]`

**Phase 3 - General (only if needed):**
- Verify author credentials before citing
- Cross-reference with academic sources

### 2. Classify & Tag Sources

Classify each source by priority (1=highest, 6=lowest). See [references/source_hierarchy.md](references/source_hierarchy.md) for domain patterns.

Apply uncertainty markers to findings:
- `[UNVERIFIED]` - single source only
- `[CONFLICTING]` - sources disagree
- `[INDUSTRY SOURCE]` - potential commercial bias
- `[PREPRINT]` - not peer-reviewed
- `[OUTDATED]` - >5 years old in fast-moving field
- `[SECONDARY]` - primary source not accessed

### 3. Generate Report

```markdown
# Research Report: [Topic]

**Query:** [question]
**Date:** [YYYY-MM-DD]

## Executive Summary
[2-3 paragraph synthesis]

## Methodology
- Search queries used
- Databases searched
- Inclusion/exclusion criteria

## Findings
### [Theme 1]
[Content with inline citations (Author, Year)]

## Source Quality Assessment
| Source | Type | Priority | Notes |
|--------|------|----------|-------|

## Uncertainties and Limitations
- [conflicts, gaps, biases]

## References
[APA 7th edition, alphabetized]
```

## APA Citation Basics

**Inline:** (Smith, 2023) or (Smith et al., 2023) for 3+ authors

**Common reference formats:**
- **Journal:** Author, A. (Year). Title of article. *Journal Name, Vol*(Issue), pp–pp. https://doi.org/xxx
- **Website:** Author. (Year, Month Day). Title. Site Name. https://url
- **Report:** Organization. (Year). *Title of report*. https://url

For complete APA 7th edition rules, edge cases, and additional source types, see [references/apa_citation.md](references/apa_citation.md).

> **Note:** For advanced citation work (complex source types, legal/media citations, batch formatting), the `apa-style-citation` skill provides enhanced expertise.

## Quality Checklist

Before finalizing:
- [ ] All claims have citations
- [ ] Source hierarchy followed (prioritize peer-reviewed)
- [ ] Conflicts noted with `[CONFLICTING]` marker
- [ ] Uncertainties section populated
- [ ] References complete in APA format

## Core Rules

1. **Never fabricate sources** - if no evidence exists, say so
2. **Acknowledge limitations** - be transparent about gaps
3. **Maintain objectivity** - present conflicting evidence fairly
4. **Prioritize recency** - prefer recent sources unless historical context needed
5. **Weight by priority** - higher priority sources trump lower when conflicting

## Scripts

Generate search queries: `python scripts/research_agent.py generate-queries "topic"`
Classify a URL: `python scripts/research_agent.py classify-url "https://..."`
