---
name: prior-art-search
description: Systematic 7-step methodology for comprehensive patent prior art searches and patentability assessments using BigQuery and CPC classification
tools: Bash, Read, Write
model: sonnet
---

# Prior Art Search Skill

Systematic 7-step methodology for comprehensive patent prior art searches and patentability assessments.

## When to Use

Invoke this skill when users ask to:
- Conduct prior art search for an invention
- Assess patentability of an idea
- Perform freedom-to-operate analysis
- Find blocking patents
- Research patent landscapes
- Prepare for patent filing

## What This Skill Does

Implements a professional 7-step prior art search methodology combining:
- Keyword searches across 76M+ patents (BigQuery)
- CPC classification searches
- USPTO API searches
- Timeline analysis
- Patentability assessment
- IDS (Information Disclosure Statement) preparation

## The 7-Step Methodology

### Step 1: Invention Definition (2-3 min)

**Goal**: Extract key features and define innovation scope

**Process**:
1. Interview user about invention
2. Extract core technical elements
3. Identify novel features
4. List all components/steps
5. Define search scope

**Output**: Structured invention summary with key features

**Questions to Ask**:
- What problem does this solve?
- What are the key components/steps?
- What makes this different from existing solutions?
- What is the core innovation?

---

### Step 2: Keyword Strategy (2-3 min)

**Goal**: Develop comprehensive search keyword list

**Process**:
1. Primary keywords from invention
2. Synonyms and variations
3. Technical terminology
4. Industry-specific terms
5. Boolean search strings

**Output**: Keyword search strategy document

**Example**:
```
Primary: blockchain authentication
Synonyms: distributed ledger verification, cryptographic authentication
Technical: public key infrastructure, digital signature
Related: decentralized identity, trustless verification
Searches:
- "blockchain AND (authentication OR verification)"
- "(distributed ledger) AND (identity OR credential)"
- "cryptographic AND (login OR access control)"
```

---

### Step 3: Broad Keyword Search (3-5 min)

**Goal**: Cast wide net to find relevant patents

**Process**:
1. Run keyword searches on BigQuery
2. Review top 20-30 results per query
3. Identify most relevant patents
4. Refine keyword strategy based on results
5. Document relevant patents found

**Code**:
```python
from python.bigquery_search import BigQueryPatentSearch
searcher = BigQueryPatentSearch()

results = searcher.search_patents(
    query="blockchain authentication",
    limit=30,
    country="US",
    start_year=2015  # Look back 5-10 years
)
```

**Output**: List of 10-20 potentially relevant patents

---

### Step 4: CPC Code Identification (2-3 min)

**Goal**: Find relevant classification codes

**Process**:
1. Extract CPC codes from relevant patents found in Step 3
2. Analyze CPC code descriptions
3. Identify primary classification areas
4. Select 3-5 most relevant CPC codes
5. Note CPC hierarchies

**Common CPC Categories**:
- **G06F**: Computing/data processing
- **H04L**: Digital communication/networks
- **G06Q**: Business methods
- **H04W**: Wireless communication
- **G06N**: AI/neural networks
- **G06T**: Image processing

**Output**: List of relevant CPC codes with descriptions

---

### Step 5: Deep CPC Search (5-10 min)

**Goal**: Comprehensive search within classifications

**Process**:
1. Search each CPC code identified
2. Review 50-100 patents per CPC code
3. Read abstracts and claims of top matches
4. Document closest prior art
5. Note key differences from invention

**Code**:
```python
results = searcher.search_by_cpc(
    cpc_code="G06F21/",  # Security arrangements
    limit=100,
    country="US"
)
```

**Output**: Comprehensive list of potentially blocking patents

---

### Step 6: Timeline Analysis (2-3 min)

**Goal**: Understand technology evolution

**Process**:
1. Filter results by date ranges
2. Identify filing trends over time
3. Find recent developments (last 2 years)
4. Check priority dates
5. Note technology progression

**Code**:
```python
# Search by year ranges
recent = searcher.search_patents(query, start_year=2022, end_year=2024)
older = searcher.search_patents(query, start_year=2015, end_year=2021)
```

**Output**: Timeline showing technology development

---

### Step 7: Patentability Report (5-10 min)

**Goal**: Professional assessment and recommendations

**Process**:
1. Analyze top 10 closest prior art
2. Assess novelty (35 USC 102)
3. Assess non-obviousness (35 USC 103)
4. Rank prior art by relevance
5. Provide claim strategy recommendations
6. Generate IDS list

**Output**: Comprehensive patentability report

---

## Report Format

```markdown
# PRIOR ART SEARCH REPORT

## Executive Summary
- Invention: [Brief description]
- Search Date: [Date]
- Searcher: Claude Patent Creator
- Databases: BigQuery (76M+ patents), USPTO API
- Time Period: [Year range]

## Patentability Assessment

### Novelty (35 USC 102)
[Assessment of whether invention is novel]

Score: [High/Medium/Low]

Analysis:
- No exact matches found
- Closest prior art: US10123456
- Key differences: [List]

### Non-Obviousness (35 USC 103)
[Assessment of whether invention is non-obvious]

Score: [High/Medium/Low]

Analysis:
- Combinations considered: [List]
- Motivation to combine: [Analysis]
- Unexpected results: [If any]

## Top 10 Most Relevant Prior Art

### 1. US10123456B2 - [Title] (95% Relevance)
**Assignee**: Example Corp
**Filed**: 2018-03-15
**Granted**: 2019-09-30
**CPC**: G06F21/31, H04L29/06

**Summary**: [Brief abstract]

**Similarities**:
- Uses blockchain for authentication
- Employs public key cryptography
- Distributed verification

**Differences**:
- Does not use [novel feature 1]
- Lacks [novel feature 2]
- Different approach to [aspect]

**Relevance**: High - core technology overlap

---

[Continue for top 10 patents...]

## Search Methodology

### Keywords Used
- Primary: blockchain, authentication, distributed ledger
- Synonyms: cryptographic verification, decentralized identity
- Technical: public key infrastructure, digital signature

### CPC Codes Searched
- G06F21/31 (Authentication)
- H04L29/06 (Security arrangements)
- G06Q20/40 (Payment authentication)

### Databases
- Google BigQuery: 247 results reviewed
- USPTO API: 89 results reviewed
- Total patents analyzed: 336
- Relevant patents identified: 47
- Top prior art selected: 10

## Claim Strategy Recommendations

### Recommended Approach
1. **Focus on novel aspects**: [Specific features]
2. **Claim breadth**: Start broad, add dependent claims
3. **Avoid prior art**: Distinguish from US10123456 by [...]

### Suggested Independent Claim Language
```
A system for [invention], comprising:
   [novel element 1];
   [novel element 2];
   wherein [novel relationship/function]
```

### Dependent Claim Opportunities
- Specific implementations of [feature]
- Combinations with [technology]
- Variations in [parameter/configuration]

## IDS (Information Disclosure Statement) List

Patents to be disclosed to USPTO:

1. US10123456B2 - [Title]
2. US10234567A1 - [Title]
3. US10345678B1 - [Title]
4. US10456789A1 - [Title]
5. US10567890B2 - [Title]
6. EP3123456A1 - [Title]
7. WO2019/123456 - [Title]
8. US2020/0123456A1 - [Title]
9. US10678901B2 - [Title]
10. US10789012A1 - [Title]

## Conclusion

**Patentability**: [High/Medium/Low]

**Rationale**:
[Summary of why invention is or is not patentable]

**Recommended Next Steps**:
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]
```

## Integration Points

This skill integrates with:
- **BigQuery Patent Search** skill (Step 3, 5, 6)
- **MPEP Search** skill (For legal guidance)
- **Patent Claims Analyzer** (For claim drafting)

## Required Data Access

- Google Cloud BigQuery (76M+ patents)
- USPTO API (optional, for additional coverage)
- Internet access for patent retrieval

## Estimated Time

- **Quick Search** (Steps 1-3): 10-15 minutes
- **Thorough Search** (Steps 1-6): 25-35 minutes
- **Complete Report** (All 7 steps): 40-60 minutes

## Tools Available

- **Bash**: To run Python searches
- **Write**: To save report and findings
- **Read**: To load invention descriptions
- **Grep**: To search through results
