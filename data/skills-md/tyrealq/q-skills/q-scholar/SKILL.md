---
name: q-scholar
description: Comprehensive academic writing skill for drafting journal-ready manuscripts. Orchestrates specialized sub-skills for descriptive analysis (q-descriptive-analysis), methods sections (q-methods), and results sections (q-results). Use when the user needs end-to-end support for academic manuscript preparation, from initial data exploration through publication-ready prose. Follows APA 7th edition formatting standards.
---

# Q-Scholar: Academic Manuscript Writing Suite

Q-Scholar is an overarching academic writing skill that orchestrates specialized sub-skills to support the complete manuscript preparation workflow. It produces journal-ready prose following APA 7th edition standards.

## Sub-Skills

### q-descriptive-analysis
Comprehensive exploratory analysis of tabular datasets. Generates grouped statistics, frequency distributions, entity extraction, temporal dynamics, and publication-ready summary reports.

Use for: Initial data exploration, descriptive statistics generation, understanding dataset structure before formal analysis.

### q-methods
Methods section drafting in clear, narrative style. Produces flowing paragraphs organized by workflow stages with appropriate appendix cross-references for technical details.

Use for: Writing data collection, preprocessing, analysis procedures, and validation descriptions.

### q-results
Results section drafting following APA 7th edition guidelines. Produces narrative prose organized by research questions with properly formatted tables.

Use for: Presenting findings, formatting statistical results, creating APA-compliant tables.

## Workflow Integration

### Phase 1: Data Exploration
Invoke q-descriptive-analysis to:
- Generate comprehensive descriptive statistics
- Identify patterns and distributions
- Create CSV tables and markdown summaries
- Understand grouping variables and key metrics

### Phase 2: Methods Documentation
Invoke q-methods to:
- Document data collection procedures
- Describe analytical approaches conceptually
- Reference technical details to appendices
- Include validation procedures

### Phase 3: Results Presentation
Invoke q-results to:
- Organize findings by research questions
- Write narrative prose integrating statistics
- Format tables per APA 7th edition
- Prepare appendices for detailed content

## Core Writing Principles

Across all sub-skills, Q-Scholar maintains consistent standards:

1. Narrative prose over bullet points
2. No em-dashes; use hyphens for compound modifiers only
3. No unnecessary bold or italic emphasis
4. APA 7th statistical notation (italicized symbols)
5. Numbers: spell out below 10 unless measurements/statistics
6. Tables: APA format with number, title, notes
7. Appendices for technical details and comprehensive codebooks
8. Placeholders for missing information (coauthor contributions, pending metrics)

## Usage Patterns

### Full Manuscript Support
```
User: Help me write the methods and results for my topic modeling study
Assistant: [Invokes q-methods for methods section, then q-results for results section]
```

### Targeted Section Drafting
```
User: Draft a results section for this analysis
Assistant: [Invokes q-results specifically]
```

### Data Exploration First
```
User: I have a new dataset and need to understand it before writing
Assistant: [Invokes q-descriptive-analysis for exploration, then proceeds to methods/results]
```

## Quality Standards

All output should meet these criteria:
- Ready for submission to peer-reviewed journals
- Consistent formatting throughout
- Complete information (or explicit placeholders)
- Appropriate use of appendices
- Logical organization and flow
- Objective reporting without premature interpretation

## Directory Structure

```
q-scholar/
├── SKILL.md                              # This file (orchestration)
├── references/                           # Shared style guides
│   ├── apa_style_guide.md                # Numbers, statistics, notation
│   └── table_formatting.md               # APA 7th table examples
├── q-descriptive-analysis/
│   └── SKILL.md                          # Data exploration skill
├── q-methods/
│   ├── SKILL.md                          # Methods drafting skill
│   └── references/
│       ├── methods_template.md
│       └── appendix_template.md
└── q-results/
    ├── SKILL.md                          # Results drafting skill
    └── references/
        └── results_template.md
```

## Cross-References

Shared references (apply to all sub-skills):
- references/apa_style_guide.md: numbers, statistics, notation
- references/table_formatting.md: APA 7th table examples

Sub-skill specific references:
- q-descriptive-analysis/SKILL.md: workflow templates, code patterns
- q-methods/references/: methods_template.md, appendix_template.md
- q-results/references/: results_template.md
