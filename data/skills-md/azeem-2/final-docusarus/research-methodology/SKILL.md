---
name: research-methodology
description: Systematic approach to gathering book research including source evaluation, citation formatting, fact-checking, and research organization. Use when conducting research, evaluating sources, or managing citations.
version: 1.2.0
tags: [research, citations, fact-checking, sources, bibliography]
changelog:
  - 1.2.0 (2025-11-27): Flexible source targets (quality over quantity), removed rigid 10+ quota
  - 1.1.0 (2025-11-26): Optimized for rapid research (3-4 hrs/chapter), removed interviews, strengthened source authentication requirements
  - 1.0.0 (2025-11-26): Initial release
---

# Research Methodology Skill

This skill provides systematic procedures for gathering, evaluating, and organizing research for book writing.

## When to Use This Skill

- Beginning research on a new book topic
- Evaluating source credibility and relevance
- Organizing research notes and citations
- Fact-checking claims during writing or editing
- Managing bibliography and references
- Planning research timelines for rapid book generation (target: 1 week)
- Managing digital research assets

## Research Workflow

### Phase 1: Planning (10% of research time)

1. **Define Research Questions**
   - What are the core questions this book answers?
   - What subsidiary questions emerge from the core?
   - What knowledge gaps need filling?

2. **Set Source Targets**
   - **Quality over quantity**: Use as many sources as needed for conceptual reliability
   - Guideline: 5-15 sources per major section (adjust based on topic depth)
   - Niche topics may have fewer authoritative sources — that's acceptable
   - Balance: Prioritize Tier 1, supplement with Tier 2, avoid Tier 3
   - Aim for diverse perspectives (avoid echo chambers)

3. **Establish Timeline**
   - Research sprint: 3-4 hours per chapter section (rapid generation mode)
   - Full book research: 5-7 days maximum
   - Source evaluation: real-time (as you discover sources)
   - Synthesis: continuous (don't wait until end)

### Phase 2: Discovery (40% of research time)

1. **Initial Exploration**
   - **START ONLY WITH AUTHORITATIVE SOURCES**: Academic databases (Google Scholar, JSTOR, PubMed), official documentation, peer-reviewed journals
   - **NEVER use Wikipedia or user-editable platforms** as research sources (content can be edited by anyone, unreliable)
   - Identify key terms, concepts, seminal works from authenticated sources
   - Map the intellectual landscape using Tier 1 sources

2. **Deep Dive**
   - Follow citations backward (what influenced this?)
   - Follow citations forward (who built on this?)
   - Use academic databases: Google Scholar, JSTOR, PubMed, IEEE Xplore
   - Access official documentation and technical standards

3. **Authority Identification**
   - Who are the recognized authorities in this field?
   - What institutions lead this research area?
   - Which papers/books are most cited by other Tier 1 sources?

### Phase 3: Evaluation (20% of research time)

Apply source evaluation criteria (see below) to all discovered sources.

### Phase 4: Synthesis (30% of research time)

1. **Pattern Recognition**
   - What themes emerge across sources?
   - Where do sources agree/disagree?
   - What narratives compete?

2. **Knowledge Integration**
   - Connect findings to research questions
   - Identify supporting evidence for key claims
   - Document gaps and uncertainties

## Source Evaluation Criteria

### Tier 1: Highly Authoritative (Prioritize)

- **Academic Journals**: Peer-reviewed papers in reputable journals
- **Academic Books**: Published by university presses or major academic publishers
- **Official Documentation**: Government reports, technical standards, official statistics
- **Expert Sources**: Published works by recognized domain experts

**Verification Checklist**:
- [ ] Author has relevant PhD or equivalent expertise
- [ ] Published by recognized institution/press
- [ ] Peer-reviewed or editorially reviewed
- [ ] Cited by other Tier 1 sources
- [ ] Methodology clearly documented

### Tier 2: Reliable (Use with verification)

- **Reputable News**: Major newspapers, established news organizations
- **Trade Publications**: Industry-specific magazines and journals
- **Professional Blogs**: Recognized experts in their field
- **Technical Documentation**: Official software/product documentation

**Verification Checklist**:
- [ ] Cross-referenced with at least one Tier 1 source
- [ ] Author expertise verified through credentials or body of work
- [ ] No obvious bias or conflicts of interest
- [ ] Recent publication (within 5 years for technical topics)

### Tier 3: Supplementary (Avoid)

- **General Blogs**: Personal opinion pieces (only if from recognized experts)
- **Social Media**: Trends and public opinion data (only for cultural context)
- **Opinion Pieces**: Clearly labeled as commentary (only from credentialed authors)

**Usage Guidelines**:
- Never cite as primary source
- Never use as factual reference
- Always trace to primary Tier 1 source before including in manuscript

### Sources to Avoid

- **Wikipedia and user-editable platforms** (anyone can edit, no authentication, unreliable)
- **Content farms** (sites generating low-quality content for SEO)
- **Outdated information** (>5 years unless historical context)
- **Sources with clear undisclosed bias**
- **Anonymous or unverifiable authors**
- **Predatory journals** (check DOAJ, Beall's List)
- **Press releases** without independent verification
- **User forums and Q&A sites** (Reddit, Quora, Stack Overflow for facts)
- **Crowdsourced content** without editorial oversight

## Citation Format Standards

### APA 7th Edition
- In-text: (Author, Year) or Author (Year)
- Single author: (Smith, 2020)
- Two authors: (Smith & Jones, 2020)
- Three or more: (Smith et al., 2020)
- Direct quote: (Smith, 2020, p. 42)

### MLA 9th Edition
- In-text: (Author Page) or Author (Page)
- Single author: (Smith 42)
- Two authors: (Smith and Jones 42)
- Three or more: (Smith et al. 42)

### Chicago 17th Edition
- In-text: Superscript numbers with corresponding footnotes/endnotes

## Fact-Checking Procedures

### Verification Workflow

1. **Identify Claims Requiring Verification**
   - Mark all factual statements in manuscript
   - Prioritize: statistics, dates, quotes, technical facts
   - Tag with confidence level: [VERIFY-HIGH], [VERIFY-MEDIUM], [VERIFY-LOW]

2. **Cross-Reference**
   - Check claim against minimum 2 independent sources
   - For critical claims: require 3+ sources
   - Document which sources confirm/contradict

3. **Document Confidence**
   - High: 3+ Tier 1 sources agree, recent data
   - Medium: 2 Tier 1 or 3+ Tier 2 sources agree
   - Low: Single source or conflicting sources
   - Flag: Unverifiable or conflicting

### Verification Standards

| Confidence | Criteria | Action |
|------------|----------|--------|
| **High** | 3+ Tier 1 sources agree, recent (<2 years), methodology clear | Use without qualification |
| **Medium** | 2 Tier 1 or 3+ Tier 2 sources agree, <5 years old | Use with standard citation |
| **Low** | Single source or conflicting sources, methodology unclear | Present with explicit uncertainty |
| **Unverified** | No reliable sources found or significant conflict | Flag for additional research or remove |

## Research Organization

### Directory Structure

```
research/
├── [topic-1]/
│   ├── primary-sources.md
│   ├── synthesis.md
│   ├── bibliography.md
│   ├── fact-checks.md
│   └── assets/
├── [topic-2]/
│   └── ...
├── cross-references.md
└── research-log.md
```

## Quality Assurance Checklist

### Before Moving to Writing Phase

**Source Quality**:
- [ ] Sufficient sources for conceptual reliability (5-15 per section, topic-dependent)
- [ ] Tier 1 sources prioritized (majority when available)
- [ ] No sources from "avoid" category (NO Wikipedia, user-editable platforms)
- [ ] All sources authenticated and verified
- [ ] Diverse perspectives represented (avoid echo chamber)
- [ ] Source gaps documented if topic has limited authoritative coverage

**Citation Completeness**:
- [ ] Citations formatted correctly and consistently
- [ ] Access dates recorded for all web sources
- [ ] DOIs included for all academic papers (where available)
- [ ] Page numbers noted for all direct quotes

**Time Efficiency**:
- [ ] Research time target met (3-4 hours per chapter section)
- [ ] No time wasted on Wikipedia or unverified sources
- [ ] Citation metadata captured immediately (no backtracking)

## Common Pitfalls to Avoid

1. **Over-reliance on Secondary Sources**: Always trace to primary source
2. **Confirmation Bias**: Actively seek sources that challenge assumptions
3. **Using Wikipedia**: Start ONLY with academic databases, peer-reviewed journals
4. **Outdated Information**: Check publication dates for technical topics
5. **Missing Citations**: Record source immediately
6. **Incomplete Metadata**: Capture all citation elements on first pass
7. **Assuming AI Accuracy**: Verify all AI-provided facts with primary sources

## Time Budget Quick Reference

```
Chapter section (3,000-5,000 words): 3-4 hours
Major chapter (10,000-15,000 words): 8-12 hours
Full book research varies by depth:
  - Light research (established topics): 30-40 hours (5-7 days)
  - Standard research (mixed sources): 50-70 hours (1-2 weeks)
  - Deep research (novel/technical): 80-120 hours (2-4 weeks)

Efficiency keys:
- Academic databases only (no Wikipedia browsing)
- Parallel research (multiple topics simultaneously)
- Immediate citation capture (no backtracking)
```

### Timeline Realism

> **⚠️ Note:** Research timelines depend heavily on:
> - Topic familiarity (established vs. cutting-edge)
> - Source availability (abundant vs. niche)
> - Depth required (overview vs. comprehensive)

**Adjust expectations based on actual source landscape, not arbitrary deadlines.**

---

**Skill Version**: 1.2.0
**Last Updated**: 2025-11-27
**Maintained By**: Universal Pedagogical Engine Team
