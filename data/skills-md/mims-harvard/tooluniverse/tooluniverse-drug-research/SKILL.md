---
name: tooluniverse-drug-research
description: Generates comprehensive drug research reports with compound disambiguation, evidence grading, and mandatory completeness sections. Covers identity, chemistry, pharmacology, targets, clinical trials, safety, pharmacogenomics, and ADMET properties. Use when users ask about drugs, medications, therapeutics, or need drug profiling, safety assessment, or clinical development research.
---

# Drug Research Strategy

Comprehensive drug investigation using 50+ ToolUniverse tools across chemical databases, clinical trials, adverse events, pharmacogenomics, and literature.

**KEY PRINCIPLES**:
1. **Report-first approach** - Create report file FIRST, then populate progressively
2. **Compound disambiguation FIRST** - Resolve identifiers before research
3. **Citation requirements** - Every fact must have inline source attribution
4. **Evidence grading** - Grade claims by evidence strength
5. **Mandatory completeness** - All sections must exist, even if "data unavailable"

---

## Critical Workflow Requirements

### 1. Report-First Approach (MANDATORY)

**DO NOT** show the search process or tool outputs to the user. Instead:

1. **Create the report file FIRST** - Before any data collection, create a markdown file:
   - File name: `[DRUG]_drug_report.md` (e.g., `metformin_drug_report.md`)
   - Initialize with all 11 section headers from the template
   - Add placeholder text: `[Researching...]` in each section

2. **Progressively update the report** - As you gather data:
   - Update each section with findings immediately after retrieving data
   - Replace `[Researching...]` with actual content
   - The user sees the report growing, not the search process

3. **Use ALL relevant tools** - For comprehensive coverage:
   - Query multiple databases for each data type
   - Cross-reference information across sources
   - Use fallback tools when primary tools return limited data

### 2. Citation Requirements (MANDATORY)

**Every piece of information MUST include its source.** Use inline citations:

```markdown
## 3. Mechanism & Targets

### 3.1 Primary Mechanism
Metformin activates AMP-activated protein kinase (AMPK), reducing hepatic glucose 
production and increasing insulin sensitivity in peripheral tissues.

*Source: PubChem via `PubChem_get_drug_label_info_by_CID` (CID: 4091)*

### 3.2 Primary Target(s)
| Target | UniProt | Activity | Potency | Source |
|--------|---------|----------|---------|--------|
| AMPK (PRKAA1) | Q13131 | Activator | EC50 ~10 µM | ChEMBL |
| Mitochondrial Complex I | - | Inhibitor | IC50 ~1 mM | Literature |

*Source: ChEMBL via `ChEMBL_get_target_by_chemblid` (CHEMBL1431)*
```

### Citation Format

For each data section, include at the end:

```markdown
---
**Data Sources for this section:**
- PubChem: `PubChem_get_compound_properties_by_CID` (CID: 4091)
- ChEMBL: `ChEMBL_get_bioactivity_by_chemblid` (CHEMBL1431)
- DGIdb: `DGIdb_get_drug_info` (metformin)
---
```

### 3. Progressive Writing Workflow

```
Step 1: Create report file with all section headers
        ↓
Step 2: Resolve compound identifiers → Update Section 1
        ↓
Step 3: Query PubChem/ADMET-AI → Update Section 2 (Chemistry)
        ↓
Step 4: Query ChEMBL/DGIdb → Update Section 3 (Mechanism & Targets)
        ↓
Step 5: Query ADMET-AI tools → Update Section 4 (ADMET)
        ↓
Step 6: Query ClinicalTrials.gov → Update Section 5 (Clinical Development)
        ↓
Step 7: Query FAERS/DailyMed → Update Section 6 (Safety)
        ↓
Step 8: Query PharmGKB → Update Section 7 (Pharmacogenomics)
        ↓
Step 9: Query DailyMed → Update Section 8 (Regulatory)
        ↓
Step 10: Query PubMed/literature → Update Section 9 (Literature)
        ↓
Step 11: Synthesize findings → Update Executive Summary & Section 10
        ↓
Step 12: Document all sources → Update Section 11 (Data Sources)
```

### 4. Report Detail Requirements

Each section must be **comprehensive and detailed**:

- **Tables**: Use tables for structured data (targets, trials, adverse events)
- **Lists**: Use bullet points for features, findings, key points
- **Paragraphs**: Include narrative summaries that synthesize findings
- **Numbers**: Include specific values, counts, percentages (not vague terms)
- **Context**: Explain what the data means, not just what it is

**BAD** (too brief):
```markdown
### Clinical Trials
Multiple trials completed. Approved for diabetes.
```

**GOOD** (detailed with sources):
```markdown
### 5.2 Clinical Trial Landscape

| Phase | Total | Completed | Recruiting | Status |
|-------|-------|-----------|------------|--------|
| Phase 4 | 89 | 72 | 12 | Post-marketing |
| Phase 3 | 156 | 134 | 15 | Pivotal |
| Phase 2 | 203 | 178 | 18 | Dose-finding |
| Phase 1 | 67 | 61 | 4 | Safety |

*Source: ClinicalTrials.gov via `search_clinical_trials` (intervention="metformin")*

**Total Registered Trials**: 515 (as of 2026-02-04)
**Primary Indications Under Investigation**: Type 2 diabetes (312), PCOS (87), Cancer (45), Obesity (38), NAFLD (33)

### Trial Outcomes Summary
- **Glycemic Control**: Mean HbA1c reduction of 1.0-1.5% in monotherapy [★★★: NCT00123456]
- **Cardiovascular**: UKPDS showed 39% reduction in MI risk [★★★: PMID:9742976]
- **Cancer Prevention**: Mixed results; ongoing investigation [★★☆: NCT02019979]

*Source: `extract_clinical_trial_outcomes` for NCT IDs listed*
```

---

## Initial Report Template (Create This First)

When starting research, **immediately create this file** before any tool calls:

**File**: `[DRUG]_drug_report.md`

```markdown
# Drug Research Report: [DRUG NAME]

**Generated**: [Date] | **Query**: [Original query] | **Status**: In Progress

---

## Executive Summary
[Researching...]

---

## 1. Compound Identity
### 1.1 Database Identifiers
[Researching...]
### 1.2 Structural Information
[Researching...]
### 1.3 Names & Synonyms
[Researching...]

---

## 2. Chemical Properties
### 2.1 Physicochemical Profile
[Researching...]
### 2.2 Drug-Likeness Assessment
[Researching...]
### 2.3 Solubility & Permeability
[Researching...]

---

## 3. Mechanism & Targets
### 3.1 Primary Mechanism of Action
[Researching...]
### 3.2 Primary Target(s)
[Researching...]
### 3.3 Target Selectivity & Off-Targets
[Researching...]
### 3.4 Bioactivity Profile (ChEMBL)
[Researching...]

---

## 4. ADMET Properties
### 4.1 Absorption
[Researching...]
### 4.2 Distribution
[Researching...]
### 4.3 Metabolism
[Researching...]
### 4.4 Excretion
[Researching...]
### 4.5 Toxicity Predictions
[Researching...]

---

## 5. Clinical Development
### 5.1 Development Status
[Researching...]
### 5.2 Clinical Trial Landscape
[Researching...]
### 5.3 Approved Indications
[Researching...]
### 5.4 Investigational Indications
[Researching...]
### 5.5 Key Efficacy Data
[Researching...]

---

## 6. Safety Profile
### 6.1 Clinical Adverse Events
[Researching...]
### 6.2 Post-Marketing Safety (FAERS)
[Researching...]
### 6.3 Black Box Warnings
[Researching...]
### 6.4 Contraindications
[Researching...]
### 6.5 Drug-Drug Interactions
[Researching...]

### 6.6 Drug-Target Interactions (Off-Target)
[Researching...]

---

## 7. Pharmacogenomics
### 7.1 Relevant Pharmacogenes
[Researching...]
### 7.2 Clinical Annotations
[Researching...]
### 7.3 Dosing Guidelines (CPIC/DPWG)
[Researching...]
### 7.4 Actionable Variants
[Researching...]

---

## 8. Regulatory & Labeling
### 8.1 Approval Status
[Researching...]
### 8.2 Label Highlights
[Researching...]
### 8.3 Patents & Exclusivity
[Researching...]

---

## 9. Literature & Research Landscape
### 9.1 Publication Metrics
[Researching...]
### 9.2 Research Themes
[Researching...]
### 9.3 Recent Key Publications
[Researching...]

---

## 10. Conclusions & Assessment
### 10.1 Drug Profile Scorecard
[Researching...]
### 10.2 Key Strengths
[Researching...]
### 10.3 Key Concerns/Limitations
[Researching...]
### 10.4 Research Gaps
[Researching...]

---

## 11. Data Sources & Methodology
[Will be populated as research progresses...]
```

Then progressively replace `[Researching...]` with actual findings as you query each tool.

---

## Compound Disambiguation (Phase 1)

**CRITICAL**: Establish compound identity before any research.

### Identifier Resolution Chain

```
1. PubChem_get_CID_by_compound_name(compound_name)
   └─ Extract: CID, canonical SMILES, formula
   
2. ChEMBL_search_compounds(query=drug_name)
   └─ Extract: ChEMBL ID, pref_name
   
3. DailyMed_search_spls(drug_name)
   └─ Extract: Set ID, NDC codes (if approved)
   
4. PharmGKB_search_drugs(query=drug_name)
   └─ Extract: PharmGKB ID (PA...)
```

### Handle Naming Ambiguity

| Issue | Example | Resolution |
|-------|---------|------------|
| Salt forms | metformin vs metformin HCl | Note all CIDs; use parent compound |
| Isomers | omeprazole vs esomeprazole | Verify SMILES; separate entries if distinct |
| Prodrugs | enalapril vs enalaprilat | Document both; note conversion |
| Brand confusion | Different products same name | Clarify with user |

---

## Tool Chains by Research Path

### PATH 1: Chemical Properties

**Objective**: Full physicochemical profile and drug-likeness

**Multi-Step Chain**:
```
1. PubChem_get_compound_properties_by_CID(cid)
   └─ Extract: MW, formula, XLogP, TPSA, HBD, HBA, rotatable bonds
   
2. ADMETAI_predict_physicochemical_properties(smiles=[smiles])
   └─ Extract: MW, logP, HBD, HBA, Lipinski, QED, stereo_centers, TPSA
   
3. ADMETAI_predict_solubility_lipophilicity_hydration(smiles=[smiles])
   └─ Extract: Solubility_AqSolDB, Lipophilicity_AstraZeneca
```

**Output for Report**:
```markdown
### 2.1 Physicochemical Profile

| Property | Value | Drug-Likeness | Source |
|----------|-------|---------------|--------|
| **Molecular Weight** | 129.16 g/mol | ✓ (< 500) | PubChem |
| **LogP** | -2.64 | ✓ (< 5) | ADMET-AI |
| **TPSA** | 91.5 Å² | ✓ (< 140) | PubChem |
| **H-Bond Donors** | 2 | ✓ (≤ 5) | PubChem |
| **H-Bond Acceptors** | 5 | ✓ (< 10) | PubChem |
| **Rotatable Bonds** | 2 | ✓ (< 10) | PubChem |

**Lipinski Rule of Five**: ✓ PASS (0 violations)
**QED Score**: 0.74 (Good drug-likeness)

*Sources: PubChem via `PubChem_get_compound_properties_by_CID`, ADMET-AI via `ADMETAI_predict_physicochemical_properties`*
```

### PATH 2: Targets & Bioactivity

**Objective**: Primary targets, mechanism, selectivity, drug-protein interactions

**Multi-Step Chain**:
```
1. ChEMBL_get_bioactivity_by_chemblid(chembl_id)
   └─ Extract: Target names, activity types, potency values [★★★]
   
2. ChEMBL_get_target_by_chemblid(chembl_id)
   └─ Extract: Target ChEMBL IDs, UniProt accessions [★★★]
   
3. DGIdb_get_drug_info(drugs=[drug_name])
   └─ Extract: Target genes, interaction types, sources [★★☆]
   
4. PubChem_get_bioactivity_summary_by_CID(cid)
   └─ Extract: Assay summary, active/inactive counts [★★☆]

5. STITCH_get_chemical_protein_interactions(identifiers=[smiles], species=9606)
   └─ Extract: Predicted/known protein targets, confidence scores [★★☆-★☆☆]

6. STITCH_get_interaction_partners(identifiers=[drug_name], species=9606)
   └─ Extract: Full interaction network [★☆☆ for predictions]
```

**Evidence Tier Guide for Targets**:
- ChEMBL binding assay (IC50 <100nM) = ★★★
- ChEMBL functional assay = ★★☆
- Predicted interaction (STITCH) = ★☆☆

**Output for Report**:
```markdown
### 3.2 Primary Target(s)

| Target | UniProt | Type | Potency | Assays | Source |
|--------|---------|------|---------|--------|--------|
| PRKAA1 (AMPK α1) | Q13131 | Activator | EC50 ~10 µM | 12 | ChEMBL |
| PRKAA2 (AMPK α2) | P54646 | Activator | EC50 ~15 µM | 8 | ChEMBL |
| SLC22A1 (OCT1) | O15245 | Substrate | Km ~1.5 mM | 5 | DGIdb |

*Source: ChEMBL via `ChEMBL_get_target_by_chemblid` (CHEMBL1431)*

### 3.4 Bioactivity Profile

**Total ChEMBL Activities**: 847 datapoints across 234 assays
- **Potency Range**: IC50/EC50 from 1 µM to 10 mM
- **Primary Activity**: AMPK activation (kinase assays)
- **Secondary Activities**: Mitochondrial complex I inhibition

*Source: `ChEMBL_get_bioactivity_by_chemblid`*
```

### PATH 3: ADMET Properties

**Objective**: Full ADMET profile with predictions

**Multi-Step Chain**:
```
1. ADMETAI_predict_bioavailability(smiles=[smiles])
   └─ Extract: Bioavailability_Ma, HIA_Hou, PAMPA_NCATS, Caco2_Wang, Pgp_Broccatelli
   
2. ADMETAI_predict_BBB_penetrance(smiles=[smiles])
   └─ Extract: BBB_Martins (0-1 probability)
   
3. ADMETAI_predict_CYP_interactions(smiles=[smiles])
   └─ Extract: CYP1A2, CYP2C9, CYP2C19, CYP2D6, CYP3A4 (inhibitor/substrate)
   
4. ADMETAI_predict_clearance_distribution(smiles=[smiles])
   └─ Extract: Clearance, Half_Life_Obach, VDss_Lombardo, PPBR_AZ
   
5. ADMETAI_predict_toxicity(smiles=[smiles])
   └─ Extract: AMES, hERG, DILI, ClinTox, LD50_Zhu, Carcinogens
```

**Output for Report**:
```markdown
### 4.1 Absorption

| Endpoint | Prediction | Interpretation |
|----------|------------|----------------|
| **Oral Bioavailability** | 0.72 | Good (>50%) |
| **Human Intestinal Absorption** | 0.89 | High |
| **Caco-2 Permeability** | -5.2 (log cm/s) | Moderate |
| **PAMPA** | 0.34 | Low-moderate |
| **P-gp Substrate** | 0.23 | Unlikely substrate |

*Source: ADMET-AI via `ADMETAI_predict_bioavailability`*

### 4.5 Toxicity Predictions

| Endpoint | Prediction | Risk Level |
|----------|------------|------------|
| **AMES Mutagenicity** | 0.08 | Low risk |
| **hERG Inhibition** | 0.12 | Low risk |
| **Hepatotoxicity (DILI)** | 0.15 | Low risk |
| **Clinical Toxicity** | 0.21 | Low risk |
| **LD50** | 2.8 (log mol/kg) | Moderate |

*Source: ADMET-AI via `ADMETAI_predict_toxicity`*

**Summary**: Low predicted toxicity across all endpoints. Favorable safety profile.
```

### PATH 4: Clinical Trials

**Objective**: Complete clinical development picture

**Multi-Step Chain**:
```
1. search_clinical_trials(intervention=drug_name, pageSize=100)
   └─ Extract: Total count, NCT IDs, phases, statuses
   
2. get_clinical_trial_conditions_and_interventions(nct_ids=[top_ids])
   └─ Extract: Conditions, interventions, arm groups
   
3. extract_clinical_trial_outcomes(nct_ids=[completed_phase3])
   └─ Extract: Primary outcomes, efficacy measures, p-values
   
4. extract_clinical_trial_adverse_events(nct_ids=[completed_ids])
   └─ Extract: Serious AEs, common AEs by organ system
```

### PATH 5: Post-Marketing Safety & Drug Interactions

**Objective**: Real-world safety signals from FAERS + drug-drug interactions

**Multi-Step Chain (FAERS)**:
```
1. FAERS_count_reactions_by_drug_event(medicinalproduct=drug_name)
   └─ Extract: Top 20 adverse reactions by MedDRA term [★★★ real-world]
   
2. FAERS_count_seriousness_by_drug_event(medicinalproduct=drug_name)
   └─ Extract: Serious vs non-serious ratio [★★★]
   
3. FAERS_count_outcomes_by_drug_event(medicinalproduct=drug_name)
   └─ Extract: Recovered, recovering, fatal, unresolved counts [★★★]
   
4. FAERS_count_death_related_by_drug(medicinalproduct=drug_name)
   └─ Extract: Fatal outcome count [★★★]
   
5. FAERS_count_patient_age_distribution(medicinalproduct=drug_name)
   └─ Extract: Reports by age group [★★★]
```

**Multi-Step Chain (Drug-Drug Interactions)**:
```
6. STITCH_get_chemical_protein_interactions(identifiers=[drug1, drug2], species=9606)
   └─ Extract: Shared targets (potential DDI mechanism) [★★☆]

7. DailyMed_search_spls(drug_name)
   └─ Extract: Drug interactions section from label [★★★ FDA-approved]

8. drugbank_get_targets_by_drug_name_or_drugbank_id(query=drug_name)
   └─ Extract: Targets, enzymes, transporters for DDI prediction [★★☆]
```

**DDI Mechanism Analysis**:
For each major interaction found, note:
- CYP enzyme involved (CYP3A4, CYP2D6, etc.)
- Interaction type (inhibitor/inducer/substrate)
- Clinical severity (contraindicated, major, moderate, minor)

**Output for Report**:
```markdown
### 6.2 Post-Marketing Safety (FAERS)

**Total FAERS Reports**: 45,234 (as of 2026-02-04)

#### Top Adverse Reactions
| Reaction (MedDRA PT) | Count | % of Reports |
|----------------------|-------|--------------|
| Diarrhoea | 8,234 | 18.2% |
| Nausea | 6,892 | 15.2% |
| Lactic acidosis | 3,456 | 7.6% |
| Vomiting | 2,987 | 6.6% |
| Abdominal pain | 2,543 | 5.6% |

*Source: FDA FAERS via `FAERS_count_reactions_by_drug_event`*

#### Outcome Distribution
| Outcome | Count | Percentage |
|---------|-------|------------|
| Recovered/Resolved | 18,234 | 40.3% |
| Not Recovered | 12,456 | 27.5% |
| Fatal | 2,134 | 4.7% |
| Unknown | 12,410 | 27.4% |

*Source: `FAERS_count_outcomes_by_drug_event`*

**Signal Assessment**: Lactic acidosis signal consistent with known labeling. GI events expected class effect.
```

### PATH 6: Pharmacogenomics

**Objective**: PGx associations and dosing guidelines

**Multi-Step Chain**:
```
1. PharmGKB_search_drugs(query=drug_name)
   └─ Extract: PharmGKB drug ID
   
2. PharmGKB_get_drug_details(drug_id)
   └─ Extract: Cross-references, related genes
   
3. PharmGKB_get_clinical_annotations(gene_id)  # For each related gene
   └─ Extract: Variant-drug associations, evidence levels
   
4. PharmGKB_get_dosing_guidelines(gene=gene_symbol)
   └─ Extract: CPIC/DPWG guideline recommendations
```

**Output for Report**:
```markdown
### 7.1 Relevant Pharmacogenes

| Gene | Role | Evidence Level | Source |
|------|------|----------------|--------|
| **SLC22A1** (OCT1) | Transporter (uptake) | 2A | PharmGKB |
| **SLC22A2** (OCT2) | Transporter (renal) | 2B | PharmGKB |
| **SLC47A1** (MATE1) | Transporter (efflux) | 3 | PharmGKB |

*Source: PharmGKB via `PharmGKB_get_drug_details`*

### 7.3 Dosing Guidelines

**CPIC Guideline**: No CPIC guideline currently available for metformin.

**Clinical Annotations**:
- rs628031 (SLC22A1): Reduced metformin response in *4/*4 carriers
- rs316019 (SLC22A2): May affect renal clearance

*Source: `PharmGKB_get_clinical_annotations`*
```

---

## Evidence Grading System

### Evidence Tiers

| Tier | Symbol | Description | Example |
|------|-------|-------------|---------|
| **T1** | ★★★ | Phase 3 RCT, meta-analysis, FDA approval | Pivotal trial, label indication |
| **T2** | ★★☆ | Phase 1/2 trial, large case series | Dose-finding study |
| **T3** | ★☆☆ | In vivo animal, in vitro cellular | Mouse PK study |
| **T4** | ☆☆☆ | Review mention, computational prediction | ADMET-AI prediction |

### Application in Report

```markdown
Metformin reduces hepatic glucose output via AMPK activation [★★★: FDA Label].
Phase 3 trials demonstrated HbA1c reduction of 1.0-1.5% [★★★: NCT00123456].
Preclinical studies suggest anti-cancer properties [★☆☆: PMID:23456789].
ADMET-AI predicts low hERG liability (0.12) [☆☆☆: computational].
```

### Per-Section Summary

Include evidence quality summary for each major section:

```markdown
### 5. Clinical Development
**Evidence Quality**: Strong (156 Phase 3 trials, 203 Phase 2, 67 Phase 1)
**Data Confidence**: High - mature clinical program with decades of data
```

---

## Section Completeness Checklist

Before finalizing any report, verify each section meets minimum requirements:

### Section 1 (Identity) - Minimum Requirements
- [ ] PubChem CID with link
- [ ] ChEMBL ID with link (or "Not in ChEMBL")
- [ ] Canonical SMILES
- [ ] Molecular formula and weight
- [ ] At least 3 brand names OR "Generic only"
- [ ] Salt forms identified (or "Parent compound only")

### Section 2 (Chemistry) - Minimum Requirements
- [ ] 6+ physicochemical properties in table format
- [ ] Lipinski rule assessment with pass/fail
- [ ] QED score with interpretation
- [ ] Solubility prediction with interpretation

### Section 3 (Mechanism) - Minimum Requirements
- [ ] Primary mechanism described in 2-3 sentences
- [ ] At least 1 primary target with UniProt ID
- [ ] Activity type and potency (IC50/EC50/Ki)
- [ ] Off-target activity addressed (or "Highly selective")

### Section 4 (ADMET) - Minimum Requirements
- [ ] All 5 subsections present (A, D, M, E, T)
- [ ] Absorption: bioavailability + at least 2 other endpoints
- [ ] Distribution: BBB + VDss or PPB
- [ ] Metabolism: CYP substrate/inhibitor status for 3+ CYPs
- [ ] Excretion: clearance OR half-life
- [ ] Toxicity: AMES + hERG + at least 1 other

### Section 5 (Clinical) - Minimum Requirements
- [ ] Development status clearly stated (Approved/Investigational/Preclinical)
- [ ] Trial counts by phase in table format
- [ ] Approved indications with year (or "Not approved")
- [ ] Key efficacy data with trial references (or "No outcome data")

### Section 6 (Safety) - Minimum Requirements
- [ ] Top 5 adverse events with frequencies
- [ ] FAERS data OR explicit "Insufficient FAERS data"
- [ ] Black box warnings (or "None")
- [ ] At least 3 drug interactions OR "No significant interactions"

### Section 7 (PGx) - Minimum Requirements
- [ ] Pharmacogenes listed (or "None identified in PharmGKB")
- [ ] CPIC/DPWG guideline status
- [ ] At least 1 clinical annotation OR "No annotations"

### Section 10 (Conclusions) - Minimum Requirements
- [ ] 5-point scorecard covering: efficacy, safety, PK, druggability, competition
- [ ] 3+ key strengths
- [ ] 3+ key concerns/limitations
- [ ] At least 2 research gaps identified

---

## Drug Profile Scorecard Template

Include in Section 10:

```markdown
### 10.1 Drug Profile Scorecard

| Criterion | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| **Efficacy Evidence** | 5 | Multiple Phase 3 trials, decades of use |
| **Safety Profile** | 4 | Well-tolerated; lactic acidosis rare but serious |
| **PK/ADMET** | 4 | Good bioavailability; renal elimination |
| **Target Validation** | 4 | AMPK mechanism well-established |
| **Competitive Position** | 3 | First-line but many alternatives |
| **Overall** | 4.0 | **Strong drug profile** |

**Interpretation**: 
- 5 = Excellent, 4 = Good, 3 = Moderate, 2 = Concerning, 1 = Poor
```

---

## Fallback Chains

| Primary Tool | Fallback | Use When |
|--------------|----------|----------|
| `PubChem_get_CID_by_compound_name` | `ChEMBL_search_compounds` | Name not in PubChem |
| `ChEMBL_get_bioactivity_by_chemblid` | `PubChem_get_bioactivity_summary_by_CID` | No ChEMBL ID |
| `DailyMed_search_spls` | `PubChem_get_drug_label_info_by_CID` | DailyMed timeout |
| `PharmGKB_get_dosing_guidelines` | Document "No guideline" | No CPIC/DPWG |
| `FAERS_count_reactions_by_drug_event` | Document "FAERS unavailable" | API error |
| `ADMETAI_*` | Document "Predictions unavailable" | Invalid SMILES |

---

## Quick Reference: Tools by Use Case

| Use Case | Primary Tool | Fallback | Evidence Tier |
|----------|--------------|----------|---------------|
| Name → CID | `PubChem_get_CID_by_compound_name` | `ChEMBL_search_compounds` | ★★★ |
| SMILES → CID | `PubChem_get_CID_by_SMILES` | - | ★★★ |
| Properties | `PubChem_get_compound_properties_by_CID` | `ADMETAI_predict_physicochemical_properties` | ★★★ / ★★☆ |
| Drug-likeness | `ADMETAI_predict_physicochemical_properties` | Calculate from properties | ★★☆ |
| Targets | `ChEMBL_get_target_by_chemblid` | `DGIdb_get_drug_info` | ★★★ |
| Predicted targets | `STITCH_get_chemical_protein_interactions` | - | ★☆☆ |
| Bioactivity | `ChEMBL_get_bioactivity_by_chemblid` | `PubChem_get_bioactivity_summary_by_CID` | ★★★ |
| Absorption | `ADMETAI_predict_bioavailability` | - | ★★☆ (predicted) |
| BBB | `ADMETAI_predict_BBB_penetrance` | - | ★★☆ (predicted) |
| CYP | `ADMETAI_predict_CYP_interactions` | - | ★★☆ (predicted) |
| Toxicity | `ADMETAI_predict_toxicity` | - | ★★☆ (predicted) |
| Drug interactions | `DailyMed_search_spls` | `STITCH_*` tools | ★★★ / ★★☆ |
| Trials | `search_clinical_trials` | - | ★★★ |
| Trial outcomes | `extract_clinical_trial_outcomes` | - | ★★★ |
| FAERS | `FAERS_count_reactions_by_drug_event` | - | ★★★ |
| Label | `DailyMed_search_spls` | `PubChem_get_drug_label_info_by_CID` | ★★★ |
| PGx | `PharmGKB_search_drugs` | - | ★★☆-★★★ |
| CPIC | `PharmGKB_get_dosing_guidelines` | - | ★★★ |
| Literature | `PubMed_search_articles` | `EuropePMC_search_articles` | Varies |

---

## Common Use Cases

### Approved Drug Profile
User: "Tell me about metformin"
→ Full 11-section report emphasizing clinical data, FAERS, PGx

### Investigational Compound
User: "What do we know about compound X (ChEMBL123456)?"
→ Emphasize preclinical data, mechanism, early trials; safety sections may be sparse

### Safety Review
User: "What are the safety concerns with drug Y?"
→ Deep dive on FAERS, black box warnings, interactions, PGx; lighter on chemistry

### ADMET Assessment
User: "Evaluate this compound's drug-likeness [SMILES]"
→ Focus on Sections 2 and 4; other sections may be brief or N/A

### Clinical Development Landscape
User: "What trials are ongoing for drug Z?"
→ Heavy emphasis on Section 5; trial tables with status, phases, indications

---

## When NOT to Use This Skill

- **Target research** → Use target-intelligence-gatherer skill
- **Disease research** → Use disease-research skill
- **Literature-only** → Use literature-deep-research skill
- **Single property lookup** → Call tool directly
- **Structure similarity search** → Use `PubChem_search_compounds_by_similarity` directly

Use this skill for comprehensive, multi-dimensional drug profiling.

---

## Additional Resources

- **Tool reference**: [TOOLS_REFERENCE.md](TOOLS_REFERENCE.md) - Complete tool listing
- **Verification checklist**: [CHECKLIST.md](CHECKLIST.md) - Pre-delivery verification
- **Examples**: [EXAMPLES.md](EXAMPLES.md) - Detailed workflow examples
