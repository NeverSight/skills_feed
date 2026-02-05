---
name: wikipedia-research
description: |
  Comprehensive Wikipedia research skill for extracting verifiable, citation-backed information in structured JSON format optimized for AI consumption and verification pipelines.
  MANDATORY TRIGGERS: Wikipedia research, Wikipedia citations, verify Wikipedia claims, extract Wikipedia references, fact-check with sources, research topic with citations, gather verifiable information, Wikipedia API, collect research data, build knowledge graph, entity extraction, research timeline
  Use when: (1) Researching topics that need source verification, (2) Extracting Wikipedia content WITH its underlying citations, (3) Building research datasets for AI verification, (4) Collecting structured bibliographic data, (5) Tracing claims to original sources, (6) Building knowledge graphs of entities and relationships, (7) Constructing timelines from biographical/historical data, (8) Cross-validating facts across multiple sources
---

# Wikipedia Research Skill

Extract verifiable research from Wikipedia with full citation provenance, entity relationships, timelines, and verification reports for AI consumption.

## Why Use This Skill?

| Without Skill | With Skill |
|---------------|------------|
| Unstructured prose | Structured JSON with schema |
| "Various sources" | 12+ citations with DOIs, PMIDs |
| Claims float freely | Every claim mapped to citations |
| No verification possible | DOI/PMID validation included |
| Unknown reliability | Admiralty Code quality rating |
| No relationships | Entity + relationship extraction |
| No timeline | Chronological event mapping |
| Dead links undetected | Archive fallback included |

## Complete Research Workflow

### Phase 1: Extract

```python
from scripts.citation_extractor import CitationExtractor

extractor = CitationExtractor()
research = extractor.extract_article("Subject_Name")
```

### Phase 2: Verify

```python
from scripts.source_verifier import SourceVerifier

verifier = SourceVerifier()

# Verify all citations (DOI, PMID, URL checks)
citation_results = verifier.verify_citations(research['citations'])

# Detect inconsistencies
inconsistencies = verifier.detect_inconsistencies(research)

# Extract Wikipedia uncertainty flags ({{citation needed}}, etc.)
flags = verifier.extract_uncertainty_flags(wikitext)

# Generate verification report
report = verifier.generate_verification_report(
    research, citation_results, inconsistencies, flags
)
```

### Phase 3: Enrich

```python
from scripts.entity_extractor import EntityExtractor

entity_extractor = EntityExtractor()

# Extract people, organizations, publications mentioned
entities = entity_extractor.extract_entities(research)

# Map relationships (collaborators, employers, etc.)
relationships = entity_extractor.extract_relationships(
    research, entities, "Subject Name"
)

# Build chronological timeline
timeline = entity_extractor.build_timeline(research)

# Generate knowledge graph
graph = entity_extractor.generate_knowledge_graph(
    "Subject Name", entities, relationships, timeline
)
```

### Phase 4: Output

```python
from scripts.research_collector import ResearchCollector

collector = ResearchCollector()
collector.save_research({
    **research,
    'verification': report,
    'knowledge_graph': graph
}, "output.json")
```

## Output Schema (Enhanced)

```json
{
  "article": {
    "title": "Subject Name",
    "url": "https://en.wikipedia.org/wiki/...",
    "revision_id": "1234567890",
    "extracted_at": "2026-02-03T10:30:00Z"
  },
  "sections": [{
    "heading": "Section Name",
    "content": "Text content...",
    "claims": [{
      "text": "Specific factual claim",
      "citation_ids": ["ref_1", "ref_2"],
      "confidence": 0.92
    }]
  }],
  "citations": [{
    "id": "ref_1",
    "type": "article-journal",
    "title": "Paper Title",
    "author": [{"family": "Smith", "given": "John"}],
    "DOI": "10.1234/example",
    "PMID": "12345678",
    "URL": "https://...",
    "issued": {"date-parts": [[2024, 1, 15]]}
  }],
  "verification": {
    "verification_summary": {
      "total_citations": 15,
      "verified_count": 12,
      "verification_score": 0.80,
      "dead_links": 2,
      "archived_recoveries": 1,
      "reliability_assessment": "high"
    },
    "citation_details": {
      "ref_1": {
        "status": "verified",
        "doi_valid": true,
        "pmid_valid": true,
        "url_accessible": true
      }
    },
    "inconsistencies": [],
    "uncertainty_flags": [{
      "section": "Early Life",
      "type": "citation_needed",
      "context": "..."
    }]
  },
  "knowledge_graph": {
    "nodes": [
      {"id": "Subject", "type": "subject"},
      {"id": "Harvard", "type": "organization"},
      {"id": "Collaborator Name", "type": "person"}
    ],
    "edges": [
      {"source": "Subject", "target": "Harvard", "type": "employment"},
      {"source": "Subject", "target": "Collaborator", "type": "collaborator"}
    ],
    "timeline": [
      {"date": "2010", "type": "education", "description": "PhD from..."},
      {"date": "2016", "type": "award", "description": "Received..."}
    ]
  },
  "provenance": {
    "source": "Wikipedia",
    "extraction_method": "MediaWiki API + wikitext parsing",
    "skill_version": "2.0",
    "verification_performed": true
  },
  "metadata": {
    "total_citations": 15,
    "verified_citations": 12,
    "total_claims": 24,
    "entities_extracted": 8,
    "timeline_events": 6,
    "source_quality": {
      "rating": "A",
      "score": 0.85
    }
  }
}
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `wikipedia_client.py` | Core API client with caching |
| `citation_extractor.py` | Extract & parse citations to CSL-JSON |
| `research_collector.py` | Multi-article research orchestration |
| `source_verifier.py` | **NEW:** Verify DOIs, PMIDs, detect dead links |
| `entity_extractor.py` | **NEW:** Extract entities, relationships, timelines |

## Verification Features

### Citation Validation

```python
verifier = SourceVerifier()
result = verifier.verify_citations(citations)

# Each citation gets:
# - status: 'verified', 'accessible', 'dead_link', 'archived'
# - doi_valid: True/False (checked against doi.org)
# - pmid_valid: True/False (checked against PubMed)
# - archive_url: Wayback Machine fallback if dead
```

### Uncertainty Detection

Automatically flags Wikipedia uncertainty templates:
- `{{citation needed}}` - Unsourced claim
- `{{disputed}}` - Contested information
- `{{original research}}` - May lack sources
- `{{outdated}}` - Information may be stale
- `{{who}}` / `{{when}}` - Vague attribution

### Inconsistency Detection

Cross-checks claims within the research:
- Date conflicts (PhD year differs between sections)
- Name variations
- Contradictory facts

## Entity & Relationship Extraction

### Entity Types

| Type | Examples |
|------|----------|
| `person` | Collaborators, mentors, colleagues |
| `organization` | Universities, companies, institutes |
| `publication_venue` | Journals, conferences |
| `concept` | Research fields, methods |

### Relationship Types

| Type | Meaning |
|------|---------|
| `collaborator` | Research collaboration |
| `employment` | Work affiliation |
| `education` | Degree/training |
| `publication` | Published in venue |
| `award_from` | Received award from |

## Timeline Construction

Automatically extracts chronological events:

```json
{
  "timeline": [
    {"date": "2005", "type": "education", "description": "BSc from University of Manchester"},
    {"date": "2010", "type": "education", "description": "PhD from Humboldt University"},
    {"date": "2011", "type": "publication", "description": "Published protein structure paper"},
    {"date": "2016", "type": "award", "description": "Received Overton Prize"}
  ]
}
```

## Quality Metrics

### Source Quality (Admiralty Code)

| Rating | Score | Meaning |
|--------|-------|---------|
| A | 0.80+ | Completely reliable - most citations verified |
| B | 0.60-0.79 | Usually reliable |
| C | 0.40-0.59 | Fairly reliable |
| D | 0.20-0.39 | Not usually reliable |
| E | <0.20 | Unreliable |

### Confidence Scoring

**Method:** Additive heuristic based on citation metadata presence.

Each claim's confidence is the average score of its supporting citations, calculated as:

```
Base score:                 0.50
+ DOI present:             +0.20  (indicates peer-reviewed)
+ PMID present:            +0.15  (indexed in PubMed)
+ ISBN present:            +0.10  (published book)
+ URL present:             +0.05  (verifiable link)
+ Author info present:     +0.10  (attributable)
+ Publication venue named: +0.05  (traceable)
─────────────────────────────────
Maximum possible:           1.00
```

**Typical scores:**

| Citation Type | Score |
|---------------|-------|
| Journal article (DOI + PMID + author) | 0.95-1.0 |
| Journal article (DOI + author) | 0.85 |
| Book (ISBN + author) | 0.75 |
| Webpage (URL + author) | 0.65 |
| Bare URL only | 0.55 |
| Citation not found | 0.30 |

**Limitations of this approach:**

- Does NOT verify that the source actually supports the claim
- Does NOT perform semantic analysis of source content
- Assumes DOI ≈ peer-reviewed (not always true for preprints)
- No weighting by journal reputation or citation count

**For higher-confidence verification:** Use `source_verifier.py` to validate DOIs/PMIDs exist, then manually verify claim-source alignment for critical facts.

## Best Practices

1. **Always verify** - Run source_verifier on all research
2. **Check uncertainty flags** - Wikipedia often marks weak areas
3. **Build timelines** - Chronology reveals inconsistencies
4. **Extract relationships** - Context matters for understanding
5. **Save revision_id** - Wikipedia changes; enable reproducibility
6. **Use DOIs** - Most reliable citation identifiers
7. **Check archives** - Dead links often have Wayback copies

## Reference Documentation

- `references/output_schema.md` - Complete JSON schema
- `references/api_reference.md` - Wikipedia API details
- `references/citation_templates.md` - Parsing guide
