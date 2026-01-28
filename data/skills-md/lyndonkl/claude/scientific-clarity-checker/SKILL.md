---
name: scientific-clarity-checker
description: Use when reviewing any scientific document for logical clarity, argument soundness, and scientific rigor. Invoke when user mentions check clarity, review logic, scientific soundness, hypothesis-data alignment, claims vs evidence, or needs a cross-cutting scientific logic review independent of document type.
---

# Scientific Clarity Checker

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Analysis Frameworks](#analysis-frameworks)
- [Common Issues](#common-issues)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill provides systematic review of scientific clarity and logical rigor across any document type. It focuses on hypothesis-data alignment, argument validity, quantitative precision, and appropriate hedging. Use this as a cross-cutting check that complements document-specific skills.

## When to Use

Use this skill when:

- **Logic check needed**: Review scientific argumentation independent of format
- **Claims vs. evidence**: Verify conclusions follow from presented data
- **Terminology audit**: Check consistency and precision of scientific language
- **Pre-submission check**: Final clarity review before sending any document
- **Collaborative review**: Providing scientific critique to colleagues
- **Self-editing**: Checking your own work for blind spots

Trigger phrases: "check scientific clarity", "review the logic", "do claims match data", "scientific rigor check", "hypothesis-data alignment", "is this sound"

**Works with all document types:**
- Manuscripts
- Grants
- Letters
- Presentations
- Abstracts
- Any scientific writing

## Core Principles

**1. Claims must match evidence**: Every conclusion needs explicit support

**2. Precision over vagueness**: Quantify wherever possible

**3. Hedging matches certainty**: Strong claims need strong evidence

**4. Logic must flow**: Arguments should be traceable step by step

**5. Terminology must be consistent**: Same concept = same word

**6. Mechanistic clarity**: The "how" should be explained, not just "what"

## Workflow

Copy this checklist and track your progress:

```
Clarity Check Progress:
- [ ] Step 1: Identify core claims and hypotheses
- [ ] Step 2: Structural logic review (argument flow)
- [ ] Step 3: Claims-evidence audit
- [ ] Step 4: Quantitative precision check
- [ ] Step 5: Terminology consistency audit
- [ ] Step 6: Hedging calibration
- [ ] Step 7: Mechanistic clarity check
```

**Step 1: Identify Core Claims**

List all major claims, conclusions, and hypotheses in the document. These are what the author wants readers to believe after reading. Every claim needs to be evaluated. See [resources/methodology.md](resources/methodology.md#claim-identification) for claim extraction.

**Step 2: Structural Logic Review**

Map the argument structure: What premises lead to what conclusions? Are all logical steps explicit? Are there gaps in the reasoning chain? See [resources/methodology.md](resources/methodology.md#argument-mapping) for logic mapping.

**Step 3: Claims-Evidence Audit**

For each claim: What evidence supports it? Is the evidence presented in this document or only cited? Does the evidence actually support the claim? Flag overclaiming. See [resources/template.md](resources/template.md#claims-evidence-matrix) for audit format.

**Step 4: Quantitative Precision Check**

Look for vague quantifiers ("some", "many", "significant increase"). Check for missing statistics, n values, confidence intervals. Flag qualitative descriptions that should be quantitative. See [resources/template.md](resources/template.md#precision-checklist) for checklist.

**Step 5: Terminology Consistency Audit**

Check that terms are used consistently throughout. Verify abbreviations are defined before use. Ensure technical terms are appropriate for audience. See [resources/methodology.md](resources/methodology.md#terminology-audit) for audit process.

**Step 6: Hedging Calibration**

Match hedge strength to evidence strength. "Demonstrates" needs strong evidence; "suggests" allows weaker evidence. Flag overclaiming (strong words, weak evidence) and underclaiming (weak words, strong evidence). See [resources/methodology.md](resources/methodology.md#hedging-guide) for calibration.

**Step 7: Mechanistic Clarity Check**

Where explanations of "how" are needed, are they provided? Are mechanisms speculative or evidence-based? Is the level of mechanistic detail appropriate? Validate using [resources/evaluators/rubric_clarity.json](resources/evaluators/rubric_clarity.json). **Minimum standard**: Average score ≥ 3.5.

## Analysis Frameworks

### Claim-Evidence Chain

For each major claim, trace the chain:

```
CLAIM: [What the author asserts]
    ↓
EVIDENCE TYPE: [Data/Citation/Logic/Authority]
    ↓
EVIDENCE: [What supports this claim]
    ↓
EVALUATION: [Strong/Moderate/Weak/Missing]
    ↓
ISSUES: [If any - overclaiming, logical gap, etc.]
```

### Logic Flow Assessment

Map argument structure:

```
PREMISE 1: [Starting assumption or fact]
    +
PREMISE 2: [Additional assumption or fact]
    ↓
INFERENCE: [Logical step taken]
    ↓
CONCLUSION: [What follows from inference]
    ↓
VALIDITY CHECK: [Does conclusion follow from premises?]
```

Common logical issues:
- **Gap**: Missing premise needed for conclusion
- **Leap**: Conclusion doesn't follow from premises
- **Assumption**: Unstated premise that may not hold
- **Circularity**: Conclusion assumed in premise

### Quantitative Precision Matrix

| Type | Vague (Fix) | Precise (Good) |
|------|-------------|----------------|
| Magnitude | "Large increase" | "3.5-fold increase" |
| Frequency | "Often occurs" | "Occurs in 75% of cases" |
| Comparison | "Higher than control" | "2.1x higher (p<0.01)" |
| Sample | "Multiple experiments" | "n=6 biological replicates" |
| Time | "Extended period" | "14-day treatment" |
| Concentration | "High concentration" | "10 µM" |

### Hedging Calibration Scale

| Evidence Level | Appropriate Hedge Words |
|----------------|------------------------|
| Direct, replicated, mechanistic | demonstrates, establishes, proves |
| Strong indirect or correlational | shows, indicates, reveals |
| Moderate, single study | suggests, supports, is consistent with |
| Limited or preliminary | may, might, could, appears to |
| Speculation beyond data | conceivably, potentially, we speculate |

## Common Issues

### Overclaiming

**Pattern:** Strong conclusion words with weak evidence

**Examples:**
- ❌ "This proves X" (based on correlation)
- ❌ "We have demonstrated Y" (single experiment, no mechanism)
- ❌ "This establishes Z" (preliminary data only)

**Fix:** Match hedge strength to evidence or add qualifying statements

### Logical Gaps

**Pattern:** Conclusion requires unstated premise

**Examples:**
- "Protein X is elevated in disease Y; therefore, X causes Y" (missing: causation ≠ correlation)
- "Our model predicts Z; therefore, Z is true" (missing: model validation)

**Fix:** Make implicit premises explicit or acknowledge limitations

### Vague Quantification

**Pattern:** Qualitative language where numbers exist

**Examples:**
- "Expression was significantly increased" (what p-value? what fold-change?)
- "Most patients improved" (what percentage?)
- "The treatment worked well" (by what metric?)

**Fix:** Replace with specific numbers

### Terminology Drift

**Pattern:** Same concept, different words (or vice versa)

**Examples:**
- Alternating "subjects", "participants", "patients" for same group
- Using "expression" and "levels" interchangeably
- Abbreviation used before definition

**Fix:** Standardize terminology; create consistency table

### Missing Mechanism

**Pattern:** "What" without "how"

**Examples:**
- "Treatment X reduces disease Y" (how does it work?)
- "Mutation Z causes phenotype W" (through what pathway?)

**Fix:** Add mechanistic explanation or acknowledge it's unknown

## Guardrails

**Critical requirements:**

1. **Don't invent evidence**: Point out what's missing, don't fabricate support
2. **Preserve author intent**: Flag issues, don't rewrite meaning
3. **Audience-appropriate**: Technical detail depends on target readers
4. **Document-appropriate**: Standards differ for abstracts vs. full papers
5. **Constructive feedback**: Identify problems with suggestions for improvement

**What this skill does NOT do:**
- ❌ Check factual accuracy of citations (can't verify papers)
- ❌ Assess experimental design quality (would need methods expertise)
- ❌ Verify statistical analysis (specialized skill)
- ❌ Judge scientific importance (subjective)

**Focus areas:**
- ✅ Internal logic and consistency
- ✅ Claims vs. evidence alignment
- ✅ Clarity and precision of language
- ✅ Appropriate hedging
- ✅ Terminology consistency
- ✅ Argument structure

## Quick Reference

**Key resources:**
- **[resources/methodology.md](resources/methodology.md)**: Claim identification, argument mapping, terminology audit, hedging guide
- **[resources/template.md](resources/template.md)**: Claims-evidence matrix, precision checklist
- **[resources/evaluators/rubric_clarity.json](resources/evaluators/rubric_clarity.json)**: Quality scoring

**Quick checks:**
- [ ] Can I identify every major claim?
- [ ] Does each claim have explicit evidence?
- [ ] Are there logical gaps in the argument?
- [ ] Are numbers used instead of vague quantifiers?
- [ ] Is terminology consistent throughout?
- [ ] Does hedge strength match evidence strength?
- [ ] Are mechanisms explained where needed?

**Red flags to look for:**
- "This proves/demonstrates/establishes" + weak evidence
- "Significant" without p-values
- Conclusions that don't follow from premises
- Same concept with multiple names
- "How" questions left unanswered

**Time estimates:**
- Quick scan (major issues): 10-15 minutes
- Standard review (full checklist): 30-45 minutes
- Deep analysis (comprehensive audit): 1-2 hours

**Inputs required:**
- Scientific document (any type)
- Context (audience, purpose)
- Specific concerns (if any)

**Outputs produced:**
- Annotated document with issues flagged
- Summary of clarity issues by category
- Recommendations for improvement
