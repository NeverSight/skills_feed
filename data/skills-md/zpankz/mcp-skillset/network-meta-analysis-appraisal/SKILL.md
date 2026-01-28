---
name: network-meta-analysis-appraisal
description: Systematically appraise network meta-analysis papers using integrated 200-point checklist (PRISMA-NMA, NICE DSU TSD 7, ISPOR-AMCP-NPC, CINeMA) with triple-validation methodology, automated PDF extraction, semantic evidence matching, and concordance analysis. Use when evaluating NMA quality for peer review, guideline development, HTA, or reimbursement decisions.
---

# Network Meta-Analysis Comprehensive Appraisal

## Overview

This skill enables systematic, reproducible appraisal of network meta-analysis (NMA) papers through:

1. **Automated PDF intelligence** - Extract text, tables, and statistical content from NMA PDFs
2. **Semantic evidence matching** - Map 200+ checklist criteria to PDF content using AI similarity
3. **Triple-validation methodology** - Two independent concurrent appraisals + meta-review consensus
4. **Comprehensive frameworks** - PRISMA-NMA, NICE DSU TSD 7, ISPOR-AMCP-NPC, CINeMA integration
5. **Professional reports** - Generate markdown checklists and structured YAML outputs

The skill transforms a complex, time-intensive manual process (~6-8 hours) into a systematic, partially-automated workflow (~2-3 hours).

## When to Use This Skill

Apply this skill when:
- Conducting peer review for journal submissions containing NMA
- Evaluating evidence for clinical guideline development
- Assessing NMA for health technology assessment (HTA)
- Reviewing NMA for reimbursement/formulary decisions
- Training on systematic NMA critical appraisal methodology
- Comparing Bayesian vs Frequentist NMA approaches

## Workflow: PDF to Appraisal Report

Follow this sequential 5-step workflow for comprehensive appraisal:

### Step 1: Setup & Prerequisites

**Install Required Libraries:**
```bash
cd scripts/
pip install -r requirements.txt

# Download semantic model (first time only)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**Verify Checklist Availability:**
Confirm all 8 checklist sections are in `references/checklist_sections/`:
- SECTION I - STUDY RELEVANCE and APPLICABILITY.md
- SECTION II - REPORTING TRANSPARENCY and COMPLETENESS - PRISMA-NMA.md
- SECTION III - METHODOLOGICAL RIGOR - NICE DSU TSD 7.md
- SECTION IV - CREDIBILITY ASSESSMENT - ISPOR-AMCP-NPC.md
- SECTION V - CERTAINTY OF EVIDENCE - CINeMA Framework.md
- SECTION VI - SYNTHESIS and OVERALL JUDGMENT.md
- SECTION VII - APPRAISER INFORMATION.md
- SECTION VIII - APPENDICES.md

**Select Framework Scope:**
Choose based on appraisal purpose (see `references/frameworks_overview.md` for details):
- `comprehensive`: All 4 frameworks (~200 items, 4-6 hours)
- `reporting`: PRISMA-NMA only (~90 items, 2-3 hours)
- `methodology`: NICE + CINeMA (~30 items, 2-3 hours)
- `decision`: Relevance + ISPOR + CINeMA (~30 items, 2-3 hours)

### Step 2: Extract PDF Content

Run `pdf_intelligence.py` to extract structured content from the NMA paper:

```bash
python scripts/pdf_intelligence.py path/to/nma_paper.pdf --output pdf_extraction.json
```

**What This Does:**
- Extracts text with section detection (abstract, methods, results, discussion)
- Parses tables using multiple libraries (Camelot, pdfplumber)
- Extracts metadata (title, page count, etc.)
- Calculates extraction quality scores

**Outputs:**
- `pdf_extraction.json` - Structured PDF content for evidence matching

**Quality Check:**
- Verify `extraction_quality` scores ≥ 0.6 for text_coverage and sections_detected
- Low scores indicate poor PDF quality - may require manual supplementation

### Step 3: Match Evidence to Checklist Criteria

**Prepare Checklist Criteria JSON:**
Extract checklist items from markdown sections into machine-readable format:

```python
import json
from pathlib import Path

# Example: Extract criteria from Section II
criteria = []
section_file = Path("references/checklist_sections/SECTION II - REPORTING TRANSPARENCY and COMPLETENESS - PRISMA-NMA.md")
# Parse markdown table rows to extract item IDs and criteria text
# Format: [{"id": "4.1", "text": "Does the title identify the study as a systematic review and network meta-analysis?"},...]

Path("checklist_criteria.json").write_text(json.dumps(criteria, indent=2))
```

**Run Semantic Evidence Matching:**
```bash
python scripts/semantic_search.py pdf_extraction.json checklist_criteria.json --output evidence_matches.json
```

**What This Does:**
- Encodes each checklist criterion as semantic vector
- Searches PDF sections for matching paragraphs
- Calculates similarity scores (0.0-1.0)
- Assigns confidence levels (high/moderate/low/unable)

**Outputs:**
- `evidence_matches.json` - Evidence mapped to each criterion with confidence scores

### Step 4: Conduct Triple-Validation Appraisal

**Manual Appraisal with Evidence Support:**

For each checklist section:

1. Load evidence matches for that section's criteria
2. Review PDF content highlighted by semantic search
3. Apply triple-validation methodology (see `references/triple_validation_methodology.md`):

   **Appraiser #1 (Critical Reviewer)**:
   - Evidence threshold: 0.75 (high)
   - Stance: Skeptical, conservative
   - For each item: Assign rating (✓/⚠/✗/N/A) based on evidence quality

   **Appraiser #2 (Methodologist)**:
   - Evidence threshold: 0.70 (moderate)
   - Stance: Technical rigor emphasis
   - For each item: Assign rating independently

4. **Meta-Review Concordance Analysis:**
   - Compare ratings between appraisers
   - Calculate agreement levels (perfect/minor/major discordance)
   - Apply resolution strategy (evidence-weighted by default)
   - Flag major discordances for manual review

**Structure Appraisal Results:**
```json
{
  "pdf_metadata": {...},
  "appraisal": {
    "sections": [
      {
        "id": "section_ii",
        "name": "REPORTING TRANSPARENCY & COMPLETENESS",
        "items": [
          {
            "id": "4.1",
            "criterion": "Title identification...",
            "rating": "✓",
            "confidence": "high",
            "evidence": "The title explicitly states...",
            "source": "methods section",
            "appraiser_1_rating": "✓",
            "appraiser_2_rating": "✓",
            "concordance": "perfect"
          },
          ...
        ]
      },
      ...
    ]
  }
}
```

Save as `appraisal_results.json`.

### Step 5: Generate Reports

**Create Markdown and YAML Reports:**
```bash
python scripts/report_generator.py appraisal_results.json --format both --output-dir ./reports
```

**Outputs:**
- `reports/nma_appraisal_report.md` - Human-readable checklist with ratings, evidence, concordance
- `reports/nma_appraisal_report.yaml` - Machine-readable structured data

**Report Contents:**
- Executive summary with overall quality ratings
- Detailed checklist tables (all 8 sections)
- Concordance analysis summary
- Recommendations for decision-makers and authors
- Evidence citations and confidence scores

**Quality Validation:**
- Review major discordance items flagged in concordance analysis
- Verify evidence confidence ≥ moderate for ≥50% of items
- Check overall agreement rate ≥ 65%
- Manually review any critical items with low confidence

## Methodological Decision Points

### Bayesian vs Frequentist Detection

The skill automatically detects statistical approach by scanning for keywords:

**Bayesian Indicators**: MCMC, posterior, prior, credible interval, WinBUGS, JAGS, Stan, burn-in, convergence diagnostic
**Frequentist Indicators**: confidence interval, p-value, I², τ², netmeta, prediction interval

Apply appropriate checklist items based on detected approach:
- Item 18.3 (Bayesian specifications) - only if Bayesian detected
- Items on heterogeneity metrics (I², τ²) - primarily Frequentist
- Convergence diagnostics - only Bayesian

### Handling Missing Evidence

When semantic search returns low confidence (<0.45):

1. Manually search PDF for the criterion
2. Check supplementary materials (if accessible)
3. If truly absent, rate as ⚠ or ✗ depending on item criticality
4. Document "No evidence found in main text" in evidence field

### Resolution Strategy Selection

Choose concordance resolution strategy based on appraisal purpose:

- **Evidence-weighted** (default): Most objective, prefers stronger evidence
- **Conservative**: For high-stakes decisions (regulatory submissions)
- **Optimistic**: For formative assessments or educational purposes

See `references/triple_validation_methodology.md` for detailed guidance.

## Resources

### scripts/

Production-ready Python scripts for automated tasks:

- **pdf_intelligence.py** - Multi-library PDF extraction (PyMuPDF, pdfplumber, Camelot)
- **semantic_search.py** - AI-powered evidence-to-criterion matching
- **report_generator.py** - Markdown + YAML report generation
- **requirements.txt** - Python dependencies

**Usage:** Scripts can be run standalone via CLI or orchestrated programmatically.

### references/

Comprehensive documentation for appraisal methodology:

- **checklist_sections/** - All 8 integrated checklist sections (PRISMA/NICE/ISPOR/CINeMA)
- **frameworks_overview.md** - Framework selection guide, rating scales, key references
- **triple_validation_methodology.md** - Appraiser roles, concordance analysis, resolution strategies

**Usage:** Load relevant references when conducting specific appraisal steps or interpreting results.

## Best Practices

1. **Always run pdf_intelligence.py first** - Extraction quality affects all downstream steps
2. **Review low-confidence matches manually** - Semantic search is not perfect
3. **Document resolution rationale** - For major discordances, explain meta-review decision
4. **Maintain appraiser independence** - Conduct Appraiser #1 and #2 evaluations without cross-reference
5. **Validate critical items** - Manually verify evidence for high-impact methodological criteria
6. **Use appropriate framework scope** - Comprehensive for peer review, targeted for specific assessments

## Limitations

- **PDF quality dependent**: Poor scans or complex layouts reduce extraction accuracy
- **Semantic matching not perfect**: May miss evidence phrased in unexpected ways
- **No external validation**: Cannot verify PROSPERO registration or check author COI databases
- **Language**: Optimized for English-language papers
- **Human oversight required**: Final appraisal should be reviewed by domain expert
