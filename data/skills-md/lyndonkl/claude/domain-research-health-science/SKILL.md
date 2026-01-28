---
name: domain-research-health-science
description: Use when formulating clinical research questions (PICOT framework), evaluating health evidence quality (study design hierarchy, bias assessment, GRADE), prioritizing patient-important outcomes, conducting systematic reviews or meta-analyses, creating evidence summaries for guidelines, assessing regulatory evidence, or when user mentions clinical trials, evidence-based medicine, health research methodology, systematic reviews, research protocols, or study quality assessment.
---
# Domain Research: Health Science

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill helps structure clinical and health science research using evidence-based medicine frameworks. It guides you through formulating precise research questions (PICOT), evaluating study quality (hierarchy of evidence, bias assessment, GRADE), prioritizing outcomes (patient-important vs surrogate), and synthesizing evidence for clinical decision-making.

## When to Use

Use this skill when:

- **Formulating research questions**: Structuring clinical questions using P ICO T (Population, Intervention, Comparator, Outcome, Timeframe)
- **Evaluating evidence quality**: Assessing study design strength, risk of bias, certainty of evidence (GRADE framework)
- **Prioritizing outcomes**: Distinguishing patient-important outcomes from surrogate endpoints, creating outcome hierarchies
- **Systematic reviews**: Planning or conducting systematic reviews, meta-analyses, or evidence syntheses
- **Clinical guidelines**: Creating evidence summaries for practice guidelines or decision support
- **Trial design**: Designing RCTs, pragmatic trials, or observational studies with rigorous methodology
- **Regulatory submissions**: Preparing evidence dossiers for drug/device approval or reimbursement decisions
- **Critical appraisal**: Evaluating published research for clinical applicability and methodological quality

Trigger phrases: "clinical trial design", "systematic review", "PICOT question", "evidence quality", "bias assessment", "GRADE", "outcome measures", "research protocol", "evidence synthesis", "study appraisal"

## What Is It?

Domain Research: Health Science applies structured frameworks from evidence-based medicine to ensure clinical research is well-formulated, methodologically sound, and clinically meaningful.

**Quick example:**

**Vague question**: "Does this drug work for heart disease?"

**PICOT-structured question**:
- **P** (Population): Adults >65 with heart failure and reduced ejection fraction
- **I** (Intervention): SGLT2 inhibitor (dapagliflozin 10mg daily)
- **C** (Comparator): Standard care (ACE inhibitor + beta-blocker)
- **O** (Outcome): All-cause mortality (primary); hospitalizations, quality of life (secondary)
- **T** (Timeframe): 12-month follow-up

**Result**: Precise, answerable research question that guides study design, literature search, and outcome selection.

## Workflow

Copy this checklist and track your progress:

```
Health Research Progress:
- [ ] Step 1: Formulate research question (PICOT)
- [ ] Step 2: Assess evidence hierarchy and study design
- [ ] Step 3: Evaluate study quality and bias
- [ ] Step 4: Prioritize and define outcomes
- [ ] Step 5: Synthesize evidence and grade certainty
- [ ] Step 6: Create decision-ready summary
```

**Step 1: Formulate research question (PICOT)**

Use PICOT framework to structure answerable clinical question. Define Population (demographics, condition, setting), Intervention (treatment, exposure, diagnostic test), Comparator (alternative treatment, placebo, standard care), Outcome (patient-important endpoints), and Timeframe (follow-up duration). See [resources/template.md](resources/template.md#picot-framework) for structured templates.

**Step 2: Assess evidence hierarchy and study design**

Determine appropriate study design based on research question type (therapy: RCT; diagnosis: cross-sectional; prognosis: cohort; harm: case-control or cohort). Understand hierarchy of evidence (systematic reviews > RCTs > cohort > case-control > case series). See [resources/methodology.md](resources/methodology.md#evidence-hierarchy) for design selection guidance.

**Step 3: Evaluate study quality and bias**

Apply risk of bias assessment tools (Cochrane RoB 2 for RCTs, ROBINS-I for observational studies, QUADAS-2 for diagnostic accuracy). Evaluate randomization, blinding, allocation concealment, incomplete outcome data, selective reporting. See [resources/methodology.md](resources/methodology.md#bias-assessment) for detailed criteria.

**Step 4: Prioritize and define outcomes**

Distinguish patient-important outcomes (mortality, symptoms, quality of life, function) from surrogate endpoints (biomarkers, lab values). Create outcome hierarchy: critical (decision-driving), important (informs decision), not important. Define measurement instruments and minimal clinically important differences (MCID). See [resources/template.md](resources/template.md#outcome-hierarchy) for prioritization framework.

**Step 5: Synthesize evidence and grade certainty**

Apply GRADE (Grading of Recommendations Assessment, Development and Evaluation) to rate certainty of evidence (high, moderate, low, very low). Consider study limitations, inconsistency, indirectness, imprecision, publication bias. Upgrade for large effects, dose-response, or confounders reducing effect. See [resources/methodology.md](resources/methodology.md#grade-framework) for rating guidance.

**Step 6: Create decision-ready summary**

Produce evidence profile or summary of findings table linking outcomes to certainty ratings and effect estimates. Include clinical interpretation, applicability assessment, and evidence gaps. Validate using [resources/evaluators/rubric_domain_research_health_science.json](resources/evaluators/rubric_domain_research_health_science.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Therapy/Intervention Question**
- **PICOT**: Adults with condition → new treatment vs standard care → patient-important outcomes → follow-up period
- **Study design**: RCT preferred (highest quality for causation); systematic review of RCTs for synthesis
- **Key outcomes**: Mortality, morbidity, quality of life, adverse events
- **Bias assessment**: Cochrane RoB 2 (randomization, blinding, attrition, selective reporting)
- **Example**: SGLT2 inhibitors for heart failure → reduced mortality (GRADE: high certainty)

**Pattern 2: Diagnostic Test Accuracy**
- **PICOT**: Patients with suspected condition → new test vs reference standard → sensitivity/specificity → cross-sectional
- **Study design**: Cross-sectional study with consecutive enrollment; avoid case-control (inflates accuracy)
- **Key outcomes**: Sensitivity, specificity, positive/negative predictive values, likelihood ratios
- **Bias assessment**: QUADAS-2 (patient selection, index test, reference standard, flow and timing)
- **Example**: High-sensitivity troponin for MI → sensitivity 95%, specificity 92% (GRADE: moderate certainty)

**Pattern 3: Prognosis/Risk Prediction**
- **PICOT**: Population with condition/exposure → risk factors → outcomes (death, disease progression) → long-term follow-up
- **Study design**: Prospective cohort (follow from exposure to outcome); avoid retrospective (recall bias)
- **Key outcomes**: Incidence, hazard ratios, absolute risk, risk prediction model performance (C-statistic, calibration)
- **Bias assessment**: ROBINS-I or PROBAST (for prediction models)
- **Example**: Framingham Risk Score for CVD → C-statistic 0.76 (moderate discrimination)

**Pattern 4: Harm/Safety Assessment**
- **PICOT**: Population exposed to intervention → adverse events → timeframe for rare/delayed harms
- **Study design**: RCT for common harms; observational (cohort, case-control) for rare harms (larger sample, longer follow-up)
- **Key outcomes**: Serious adverse events, discontinuations, organ-specific toxicity, long-term safety
- **Bias assessment**: Different for rare vs common harms; consider confounding by indication in observational studies
- **Example**: NSAID cardiovascular risk → observational studies show increased MI risk (GRADE: low certainty due to confounding)

**Pattern 5: Systematic Review/Meta-Analysis**
- **PICOT**: Defined in protocol; guides search strategy, inclusion criteria, outcome extraction
- **Study design**: Comprehensive search, explicit eligibility criteria, duplicate screening/extraction, bias assessment, quantitative synthesis (if appropriate)
- **Key outcomes**: Pooled effect estimates (RR, OR, MD, SMD), heterogeneity (I²), certainty rating (GRADE)
- **Bias assessment**: Individual study RoB + review-level assessment (AMSTAR 2 for review quality)
- **Example**: Statins for primary prevention → RR 0.75 for MI (95% CI 0.70-0.80, I²=12%, GRADE: high certainty)

## Guardrails

**Critical requirements:**

1. **Use PICOT for all clinical questions**: Vague questions lead to unfocused research. Always specify Population, Intervention, Comparator, Outcome, Timeframe explicitly. Avoid "does X work?" without defining for whom, compared to what, and measuring which outcomes.

2. **Match study design to question type**: RCTs answer therapy questions (causal inference). Cohort studies answer prognosis. Cross-sectional studies answer diagnosis. Case-control studies answer rare harm or etiology. Don't claim causation from observational data or use case series for treatment effects.

3. **Prioritize patient-important outcomes over surrogates**: Surrogate endpoints (biomarkers, lab values) don't always correlate with patient outcomes. Focus on mortality, morbidity, symptoms, function, quality of life. Only use surrogates if validated relationship to patient outcomes exists.

4. **Assess bias systematically, not informally**: Use validated tools (Cochrane RoB 2, ROBINS-I, QUADAS-2) not subjective judgment. Bias assessment affects certainty of evidence and clinical recommendations. Common biases: selection bias, performance bias (lack of blinding), detection bias, attrition bias, reporting bias.

5. **Apply GRADE to rate certainty of evidence**: Don't conflate study design with certainty. RCTs start as high certainty but can be downgraded (serious limitations, inconsistency, indirectness, imprecision, publication bias). Observational studies start as low but can be upgraded (large effect, dose-response, residual confounding reducing effect).

6. **Distinguish statistical significance from clinical importance**: p < 0.05 doesn't mean clinically meaningful. Consider minimal clinically important difference (MCID), absolute risk reduction, number needed to treat (NNT). Small p-value with tiny effect size is statistically significant but clinically irrelevant.

7. **Assess external validity and applicability**: Evidence from selected trial populations may not apply to your patient. Consider PICO match (are your patients similar?), setting differences (tertiary center vs community), intervention feasibility, patient values and preferences.

8. **State limitations and certainty explicitly**: All evidence has limitations. Specify what's uncertain, where evidence gaps exist, and how this affects confidence in recommendations. Avoid overconfident claims not supported by evidence quality.

**Common pitfalls:**

- ❌ **Treating all RCTs as high quality**: RCTs can have serious bias (inadequate randomization, unblinded, high attrition). Always assess bias.
- ❌ **Ignoring heterogeneity in meta-analysis**: High I² (>50%) suggests important differences across studies. Explore sources (population, intervention, outcome definition) before pooling.
- ❌ **Confusing association with causation**: Observational studies show association, not causation. Residual confounding is always possible.
- ❌ **Using composite outcomes uncritically**: Composite endpoints (e.g., "death or MI or hospitalization") obscure which component drives effect. Report components separately.
- ❌ **Accepting industry-funded evidence uncritically**: Pharmaceutical/device company-sponsored trials may have bias (outcome selection, selective reporting). Assess for conflicts of interest.
- ❌ **Over-interpreting subgroup analyses**: Most subgroup effects are chance findings. Only credible if pre-specified, statistically tested for interaction, and biologically plausible.

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: PICOT framework, outcome hierarchy template, evidence table, GRADE summary template
- **[resources/methodology.md](resources/methodology.md)**: Evidence hierarchy, bias assessment tools, GRADE detailed guidance, study design selection, systematic review methods
- **[resources/evaluators/rubric_domain_research_health_science.json](resources/evaluators/rubric_domain_research_health_science.json)**: Quality criteria for research questions, evidence synthesis, and clinical interpretation

**PICOT Template:**
- **P** (Population): [Who? Age, sex, condition, severity, setting]
- **I** (Intervention): [What? Drug, procedure, test, exposure - dose, duration, route]
- **C** (Comparator): [Compared to what? Placebo, standard care, alternative treatment]
- **O** (Outcome): [What matters? Mortality, symptoms, QoL, harms - measurement instrument, timepoint]
- **T** (Timeframe): [How long? Follow-up duration, time to outcome]

**Evidence Hierarchy (Therapy Questions):**
1. Systematic reviews/meta-analyses of RCTs
2. Individual RCTs (large, well-designed)
3. Cohort studies (prospective)
4. Case-control studies
5. Case series, case reports
6. Expert opinion, pathophysiologic rationale

**GRADE Certainty Ratings:**
- **High** (⊕⊕⊕⊕): Very confident true effect is close to estimated effect
- **Moderate** (⊕⊕⊕○): Moderately confident, true effect likely close but could be substantially different
- **Low** (⊕⊕○○): Limited confidence, true effect may be substantially different
- **Very Low** (⊕○○○): Very little confidence, true effect likely substantially different

**Typical workflow time:**

- PICOT formulation: 10-15 minutes
- Single study critical appraisal: 20-30 minutes
- Systematic review protocol: 2-4 hours
- Evidence synthesis with GRADE: 1-2 hours
- Full systematic review: 40-100 hours (depending on scope)

**When to escalate:**

- Complex statistical meta-analysis (network meta-analysis, IPD meta-analysis)
- Advanced causal inference methods (instrumental variables, propensity scores)
- Health technology assessment (cost-effectiveness, budget impact)
- Guideline development panels (requires multi-stakeholder consensus)
→ Consult biostatistician, health economist, or guideline methodologist

**Inputs required:**

- **Research question** (clinical scenario or decision problem)
- **Evidence sources** (studies to appraise, databases for systematic review)
- **Outcome preferences** (which outcomes matter most to patients/clinicians)
- **Context** (setting, patient population, decision urgency)

**Outputs produced:**

- `domain-research-health-science.md`: Structured research question, evidence appraisal, outcome hierarchy, certainty assessment, clinical interpretation
