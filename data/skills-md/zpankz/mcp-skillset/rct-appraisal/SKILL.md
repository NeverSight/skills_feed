---
name: rct-appraisal
description: Systematically appraise randomized controlled trials using integrated 120-point checklist (CONSORT 2025, Cochrane RoB 2.0, GRADE, TIDieR, Benefits/Harms Assessment, COI Framework) with dual-validation methodology, automated evidence extraction, and comprehensive risk-benefit evaluation. Use when conducting peer review, evaluating RCT quality for systematic reviews, guideline development, assessing intervention benefits and harms, identifying biases, or evaluating conflicts of interest for editorial writing and critical appraisal.
---

# RCT Comprehensive Appraisal

## Overview

This skill enables systematic, reproducible appraisal of randomized controlled trial (RCT) papers through:

1. **Multi-framework integration** - CONSORT 2025, Cochrane RoB 2.0, GRADE, TIDieR, Benefits/Harms, COI assessment
2. **Comprehensive bias assessment** - Systematic evaluation across 5 risk of bias domains with ~30 signaling questions
3. **Benefits and harms evaluation** - Structured assessment of therapeutic benefits, adverse events, and risk-benefit balance
4. **Conflicts of interest analysis** - Systematic COI detection and impact evaluation
5. **Evidence certainty grading** - GRADE framework for rating confidence in effect estimates
6. **Dual-validation methodology** - Independent concurrent appraisals with concordance analysis
7. **Editorial writing support** - Generate evidence-based 1500-word editorial content on RCT quality

The skill transforms RCT critical appraisal from a subjective, variable process into a systematic, evidence-based workflow (~2-4 hours depending on scope).

## When to Use This Skill

Apply this skill when:
- Conducting peer review for journal submissions containing RCTs
- Evaluating RCT quality for inclusion in systematic reviews or meta-analyses
- Assessing evidence for clinical guideline development
- Writing editorials or commentaries requiring assessment of benefits, harms, biases, and COI
- Training on systematic RCT critical appraisal methodology
- Evaluating intervention safety profiles and risk-benefit balance
- Identifying methodological biases that may affect validity
- Assessing transparency and completeness of intervention reporting

## Workflow: RCT to Comprehensive Appraisal Report

Follow this sequential 6-step workflow for comprehensive appraisal:

### Step 1: Setup & Framework Selection

**Select Appraisal Scope:**

Choose based on appraisal purpose (see `references/frameworks_overview.md` for details):

- `comprehensive`: All 6 frameworks (~120 items, 3-4 hours) - Full quality assessment
- `reporting_quality`: CONSORT 2025 only (~25 items, 1-2 hours) - Reporting transparency
- `bias_assessment`: RoB 2.0 + GRADE (~35 items, 1-2 hours) - Risk of bias focus
- `benefits_harms`: Benefits/Harms + GRADE (~20 items, 1-2 hours) - Safety/efficacy evaluation
- `intervention_quality`: TIDieR + CONSORT (~37 items, 1-2 hours) - Intervention reporting
- `editorial_focus`: RoB 2.0 + Benefits/Harms + COI (~50 items, 2-3 hours) - Editorial writing support

**Verify Framework Resources:**

Confirm all framework guides are available in `references/`:
- consort_2025_checklist.md
- rob2_assessment_guide.md
- grade_rct_framework.md
- tidier_checklist.md
- benefits_harms_framework.md
- coi_assessment_guide.md
- integrated_workflow.md

**Prepare Appraisal Infrastructure:**

```bash
cd /Users/mikhail/.claude/skills/rct-appraisal/scripts/

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Verify calculator scripts
python grade_calculator.py --version
python effect_size_calculator.py --version
```

### Step 2: Initial Evidence Extraction

**Systematic PDF/Document Review:**

1. Extract study metadata:
   - Trial registration number (ClinicalTrials.gov, etc.)
   - CONSORT diagram availability
   - Primary and secondary outcomes
   - Sample size and power calculation
   - Funding sources and COI statements

2. Map evidence to framework sections:
   - **CONSORT**: Title, abstract, introduction, methods, results sections
   - **RoB 2.0**: Randomization process, deviations, missing data, outcome measurement, selective reporting
   - **GRADE**: Effect size, precision, consistency, directness evidence
   - **TIDieR**: Intervention description in methods section
   - **Benefits/Harms**: Adverse events reporting in results/discussion
   - **COI**: Author disclosures, funding statements, competing interests

**Create Structured Evidence Log:**

```json
{
  "study_metadata": {
    "title": "...",
    "registration": "NCT...",
    "population": "...",
    "intervention": "...",
    "comparator": "...",
    "outcomes": ["primary", "secondary"]
  },
  "evidence_map": {
    "consort_section": {...},
    "rob2_section": {...},
    "grade_section": {...},
    "tidier_section": {...},
    "benefits_harms_section": {...},
    "coi_section": {...}
  }
}
```

Save as `evidence_extraction.json`.

### Step 3: Apply Framework Checklists

**CONSORT 2025 Assessment** (25 items):

Load `references/consort_2025_checklist.md` and evaluate:
- Title and abstract transparency
- Introduction and rationale clarity
- Methods completeness (eligibility, interventions, outcomes, sample size, randomization, blinding)
- Results reporting (participant flow, baseline characteristics, outcomes, harms)
- Discussion interpretation and generalizability
- Registration and protocol access

**Cochrane RoB 2.0 Assessment** (5 domains, ~30 signaling questions):

Load `references/rob2_assessment_guide.md` and assess:
1. **Randomization process**: Sequence generation, allocation concealment, baseline imbalances
2. **Deviations from intended interventions**: Implementation, adherence, appropriate analysis
3. **Missing outcome data**: Data availability, reasons for missingness, impact on results
4. **Measurement of the outcome**: Blinding of assessors, appropriateness of measurement method
5. **Selection of reported result**: Pre-specified outcomes, selective reporting

**GRADE Assessment** (5 downgrading + 3 upgrading criteria):

Load `references/grade_rct_framework.md` and evaluate:
- Starting level: HIGH (RCT evidence)
- Downgrade for: Risk of bias, inconsistency, indirectness, imprecision, publication bias
- Upgrade for: Large effect, dose-response gradient, residual confounding reducing effect
- Final certainty: High / Moderate / Low / Very Low

**TIDieR Assessment** (12 items):

Load `references/tidier_checklist.md` and check:
- Brief name, rationale, materials, procedures, provider, mode of delivery
- Location, dosage/intensity, tailoring, modifications, fidelity assessment

**Benefits/Harms Assessment** (15 items):

Load `references/benefits_harms_framework.md` and evaluate:
- Benefits: Efficacy, clinical significance, consistency, durability
- Harms: Adverse events completeness, severity assessment, causality, reporting quality
- Balance: Risk-benefit ratio, patient-important outcomes, subgroup considerations

**COI Assessment** (8 items):

Load `references/coi_assessment_guide.md` and assess:
- Funding source transparency, author financial disclosures, industry involvement
- Protocol independence, data access, statistical analysis control
- Interpretation bias indicators, competing interests impact

### Step 4: Conduct Dual-Validation Appraisal

**Manual Appraisal with Independent Reviewers:**

For each framework section:

1. **Appraiser #1 (Critical Reviewer)**:
   - Evidence threshold: HIGH
   - Stance: Skeptical, conservative
   - For each item: Assign rating (✓/⚠/✗/N/A) + confidence level (high/moderate/low/unable)
   - Document evidence source and location in paper

2. **Appraiser #2 (Methodologist)**:
   - Evidence threshold: MODERATE
   - Stance: Technical rigor emphasis
   - For each item: Assign rating independently without consulting Appraiser #1
   - Document evidence interpretation and rationale

**Structure Appraisal Results:**

```json
{
  "study_id": "...",
  "appraisal_date": "2025-10-24",
  "frameworks_applied": ["CONSORT", "RoB2", "GRADE", "TIDieR", "Benefits_Harms", "COI"],
  "sections": [
    {
      "framework": "CONSORT_2025",
      "items": [
        {
          "item_id": "1a",
          "criterion": "Identification as randomized trial in title",
          "appraiser_1_rating": "✓",
          "appraiser_1_confidence": "high",
          "appraiser_1_evidence": "Title states 'randomized controlled trial'",
          "appraiser_2_rating": "✓",
          "appraiser_2_confidence": "high",
          "appraiser_2_evidence": "Explicit mention in title",
          "consensus_rating": "✓",
          "concordance": "perfect"
        },
        ...
      ],
      "section_summary": {...}
    },
    ...
  ],
  "overall_quality": {...}
}
```

Save as `appraisal_results.json`.

### Step 5: Concordance Analysis & Resolution

**Calculate Agreement Metrics:**

```bash
python scripts/concordance_analyzer.py appraisal_results.json --output concordance_report.json
```

**Review Discordances:**

- **Perfect Agreement**: Both appraisers assign identical ratings → Accept without review
- **Minor Discordance**: Adjacent ratings (✓ vs ⚠) → Apply evidence-weighted resolution
- **Major Discordance**: Opposite ratings (✓ vs ✗) → Flag for manual meta-review with justification from both appraisers

**Resolution Strategy** (default: evidence-weighted):
- Compare evidence quality and specificity
- Prefer rating with explicit PDF citations
- Document resolution rationale for major discordances

**Quality Control Checks:**
- Overall agreement rate ≥ 70%
- No more than 5% major discordance
- Evidence confidence ≥ moderate for ≥60% of items

### Step 6: Generate Reports and Calculate Metrics

**Calculate Effect Size Metrics:**

```bash
# Calculate NNT, NNH, ARR, RRR from RCT data
python scripts/effect_size_calculator.py \
  --intervention-events 42 --intervention-total 150 \
  --control-events 68 --control-total 150 \
  --output effect_sizes.json
```

**Calculate GRADE Certainty:**

```bash
# Apply GRADE downgrading/upgrading logic
python scripts/grade_calculator.py appraisal_results.json \
  --output grade_assessment.json
```

**Generate Comprehensive Report:**

```bash
python scripts/report_generator.py appraisal_results.json \
  --include-effect-sizes effect_sizes.json \
  --include-grade grade_assessment.json \
  --format markdown \
  --output rct_appraisal_report.md
```

**Report Contents:**
1. Executive summary with overall quality ratings
2. Study characteristics and PICO framework
3. CONSORT compliance table (25 items)
4. RoB 2.0 assessment with traffic light plots (5 domains)
5. GRADE evidence certainty summary
6. TIDieR intervention quality assessment
7. Benefits and harms comprehensive evaluation
8. COI analysis with impact assessment
9. Concordance analysis summary
10. Recommendations for decision-makers and authors
11. Evidence citations with confidence scores

**Generate Editorial Content** (for editorial writing assignments):

```bash
python scripts/editorial_generator.py appraisal_results.json \
  --focus benefits_harms_biases_coi \
  --word-count 1500 \
  --output editorial_content.md
```

## Methodological Decision Points

### Risk of Bias Domain-Specific Guidance

**Domain 1: Randomization Process**
- LOW risk: Adequate sequence generation + allocation concealment + no baseline imbalances
- SOME CONCERNS: Inadequate information on sequence generation or concealment
- HIGH risk: Non-random sequence or no allocation concealment + baseline imbalances

**Domain 2: Deviations from Intended Interventions**
- LOW risk: No deviations or deviations unlikely to impact outcome
- SOME CONCERNS: Deviations present but balanced or appropriate analysis used
- HIGH risk: Substantial deviations + inappropriate analysis

**Domain 3: Missing Outcome Data**
- LOW risk: Data nearly complete or missingness unlikely to bias results
- SOME CONCERNS: Missingness present but likely not affecting results
- HIGH risk: Substantial missingness + likely biased results

**Domain 4: Outcome Measurement**
- LOW risk: Blinded assessors + appropriate measurement method
- SOME CONCERNS: Unblinded but unlikely to influence outcome
- HIGH risk: Unblinded + measurement influenced by knowledge of intervention

**Domain 5: Selective Reporting**
- LOW risk: Pre-registered outcomes reported + no evidence of selective reporting
- SOME CONCERNS: No protocol access or minor outcome omissions
- HIGH risk: Not all pre-specified outcomes reported + selective reporting evident

### GRADE Certainty Downgrading Guidance

**Start at HIGH** (RCT evidence):

**Downgrade for:**
1. **Risk of bias (-1 or -2)**: Serious limitations in RoB 2.0 domains → -1; Very serious → -2
2. **Inconsistency (-1 or -2)**: Unexplained heterogeneity or conflicting results
3. **Indirectness (-1 or -2)**: Differences in PICO between question and evidence
4. **Imprecision (-1 or -2)**: Wide confidence intervals or small sample size
5. **Publication bias (-1)**: Evidence of selective outcome reporting or small study effects

**Upgrade for (rare for single RCT):**
1. **Large effect (+1 or +2)**: RR >2 or <0.5 with no plausible confounders
2. **Dose-response gradient (+1)**: Evidence of dose-response relationship
3. **Residual confounding (+1)**: Plausible confounders would reduce observed effect

**Final Certainty Levels:**
- **High**: Very confident true effect lies close to estimate
- **Moderate**: Moderately confident; true effect likely close but may differ substantially
- **Low**: Limited confidence; true effect may differ substantially
- **Very Low**: Very little confidence; true effect likely substantially different

### Benefits/Harms Balance Assessment

**Favorable Benefit-Risk Profile:**
- Large magnitude of benefit (NNT <10)
- Small/rare harms (NNH >100)
- Patient-important outcomes improved
- Benefits outweigh harms decisively

**Uncertain Benefit-Risk Profile:**
- Modest benefits (NNT 10-50)
- Moderate harms (NNH 20-100)
- Trade-offs require patient preferences
- Balance depends on context

**Unfavorable Benefit-Risk Profile:**
- Small benefits (NNT >50)
- Frequent/severe harms (NNH <20)
- Harms outweigh benefits
- Intervention not recommended

### COI Impact Assessment

**Low Impact:**
- Academic/government funding only
- No industry involvement in design/analysis
- All authors declare no competing interests

**Moderate Impact:**
- Industry funding but independent data access
- Some authors with industry ties but protocol pre-registered
- Competing interests disclosed transparently

**High Impact:**
- Industry sponsor controls data/analysis
- Multiple authors with significant financial conflicts
- No protocol registration or selective outcome reporting
- Interpretation appears biased toward sponsor interests

## Resources

### scripts/

Production-ready Python scripts for automated calculations and report generation:

- **grade_calculator.py** - Calculate GRADE certainty levels with downgrade/upgrade logic
- **effect_size_calculator.py** - Calculate NNT, NNH, ARR, RRR, OR→RR conversions
- **concordance_analyzer.py** - Compute agreement metrics between independent appraisers
- **report_generator.py** - Generate markdown and YAML comprehensive appraisal reports
- **editorial_generator.py** - Generate 1500-word editorial content focused on benefits/harms/biases/COI
- **requirements.txt** - Python dependencies

**Usage:** Scripts can be run standalone via CLI or integrated into automated pipelines.

### references/

Comprehensive framework documentation for systematic appraisal:

- **consort_2025_checklist.md** - Complete 25-item CONSORT reporting standards
- **rob2_assessment_guide.md** - Cochrane RoB 2.0 with 5 domains and signaling questions
- **grade_rct_framework.md** - GRADE certainty assessment for RCTs (downgrade/upgrade criteria)
- **tidier_checklist.md** - 12-item intervention description quality assessment
- **benefits_harms_framework.md** - Systematic benefits/harms evaluation guide
- **coi_assessment_guide.md** - Conflicts of interest detection and impact assessment
- **integrated_workflow.md** - How all 6 frameworks work together for comprehensive appraisal
- **frameworks_overview.md** - Framework selection guide, rating scales, key references
- **dual_validation_methodology.md** - Independent appraiser roles, concordance analysis, resolution strategies

**Usage:** Load relevant framework references when conducting specific appraisal steps or interpreting results.

## Best Practices

1. **Always start with framework selection** - Choose appropriate scope based on appraisal purpose
2. **Extract evidence systematically** - Map paper sections to framework criteria before rating
3. **Maintain appraiser independence** - Conduct Appraiser #1 and #2 evaluations without cross-reference
4. **Document evidence sources** - Cite specific paper sections, tables, or figures for each rating
5. **Review discordances carefully** - Major discordances often reveal important methodological issues
6. **Use calculators for objectivity** - Employ effect_size_calculator.py for NNT/NNH rather than manual calculation
7. **Apply GRADE systematically** - Start at HIGH, apply each downgrade criterion sequentially
8. **Assess benefits AND harms** - Never evaluate efficacy without adverse events assessment
9. **Evaluate COI impact** - Consider how funding/conflicts may influence results interpretation
10. **Generate comprehensive reports** - Include all 6 framework sections for complete appraisal

## Limitations

- **Single-study focus**: Designed for individual RCT appraisal, not meta-analysis or systematic review
- **Requires full-text access**: Cannot assess protocols, supplementary materials, or trial registries without access
- **No automated extraction**: PDF intelligence not implemented; requires manual evidence extraction
- **Language**: Optimized for English-language papers
- **Clinical context required**: Some framework items (indirectness, clinical significance) require domain expertise
- **COI verification limited**: Cannot access external databases (e.g., Open Payments) for verification
- **Subjectivity remains**: Despite systematic approach, some items (e.g., clinical significance) involve judgment
- **Time-intensive**: Comprehensive appraisal with dual validation requires 3-4 hours even with tools

## Key References

1. **CONSORT 2025**: Schulz KF, et al. CONSORT 2025 explanation and elaboration: updated guideline for reporting randomised trials. *BMJ* 2025.

2. **Cochrane RoB 2.0**: Sterne JAC, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ* 2019;366:l4898.

3. **GRADE**: Guyatt GH, et al. GRADE guidelines: 1. Introduction—GRADE evidence profiles and summary of findings tables. *J Clin Epidemiol* 2011;64(4):383-394.

4. **TIDieR**: Hoffmann TC, et al. Better reporting of interventions: template for intervention description and replication (TIDieR) checklist and guide. *BMJ* 2014;348:g1687.

5. **Benefits/Harms**: Golder S, et al. Reporting of adverse events in published and unpublished studies of health care interventions: a systematic review. *PLoS Med* 2016;13(9):e1002127.

6. **COI**: Lundh A, et al. Industry sponsorship and research outcome. *Cochrane Database Syst Rev* 2017;2(2):MR000033.
