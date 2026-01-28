---
name: research-claim-map
description: Use when verifying claims before decisions, fact-checking statements against sources, conducting due diligence on vendor/competitor assertions, evaluating conflicting evidence, triangulating source credibility, assessing research validity for literature reviews, investigating misinformation, rating evidence strength (primary vs secondary), identifying knowledge gaps, or when user mentions "fact-check", "verify this", "is this true", "evaluate sources", "conflicting evidence", or "due diligence".
---

# Research Claim Map

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It](#what-is-it)
4. [Workflow](#workflow)
5. [Evidence Quality Framework](#evidence-quality-framework)
6. [Source Credibility Assessment](#source-credibility-assessment)
7. [Common Patterns](#common-patterns)
8. [Guardrails](#guardrails)
9. [Quick Reference](#quick-reference)

## Purpose

Research Claim Map helps you systematically evaluate claims by triangulating sources, assessing evidence quality, identifying limitations, and reaching evidence-based conclusions. It prevents confirmation bias, overconfidence, and reliance on unreliable sources.

## When to Use

**Invoke this skill when you need to:**
- Verify factual claims before making decisions or recommendations
- Evaluate conflicting evidence from multiple sources
- Assess vendor claims, product benchmarks, or competitive intelligence
- Conduct due diligence on business assertions (revenue, customers, capabilities)
- Fact-check news stories, social media claims, or viral statements
- Review academic literature for research validity
- Investigate potential misinformation or misleading statistics
- Rate evidence strength for policy decisions or strategic planning
- Triangulate eyewitness accounts or historical records
- Identify knowledge gaps and areas requiring further investigation

**User phrases that trigger this skill:**
- "Is this claim true?"
- "Can you verify this?"
- "Fact-check this statement"
- "I found conflicting information about..."
- "How reliable is this source?"
- "What's the evidence for..."
- "Due diligence on..."
- "Evaluate these competing claims"

## What Is It

A Research Claim Map is a structured analysis that breaks down a claim into:
1. **Claim statement** (specific, testable assertion)
2. **Evidence for** (sources supporting the claim, rated by quality)
3. **Evidence against** (sources contradicting the claim, rated by quality)
4. **Source credibility** (expertise, bias, track record for each source)
5. **Limitations** (gaps, uncertainties, assumptions)
6. **Conclusion** (confidence level, decision recommendation)

**Quick example:**
- **Claim**: "Competitor X has 10,000 paying customers"
- **Evidence for**: Press release (secondary), case study count (tertiary)
- **Evidence against**: Industry analyst estimate of 3,000 (secondary)
- **Credibility**: Press release (biased source), analyst (independent but uncertain methodology)
- **Limitations**: No primary source verification, customer definition unclear
- **Conclusion**: Low confidence (40%) - likely inflated, need primary verification

## Workflow

Copy this checklist and track your progress:

```
Research Claim Map Progress:
- [ ] Step 1: Define the claim precisely
- [ ] Step 2: Gather and categorize evidence
- [ ] Step 3: Rate evidence quality and source credibility
- [ ] Step 4: Identify limitations and gaps
- [ ] Step 5: Draw evidence-based conclusion
```

**Step 1: Define the claim precisely**

Restate the claim as a specific, testable assertion. Avoid vague language - use numbers, dates, and clear terms. See [Common Patterns](#common-patterns) for claim reformulation examples.

**Step 2: Gather and categorize evidence**

Collect sources supporting and contradicting the claim. Organize into "Evidence For" and "Evidence Against". For straightforward verification → Use [resources/template.md](resources/template.md). For complex multi-source investigations → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Rate evidence quality and source credibility**

Apply [Evidence Quality Framework](#evidence-quality-framework) to rate each source (primary/secondary/tertiary). Apply [Source Credibility Assessment](#source-credibility-assessment) to evaluate expertise, bias, and track record.

**Step 4: Identify limitations and gaps**

Document what's unknown, what assumptions were made, and where evidence is weak or missing. See [resources/methodology.md](resources/methodology.md) for gap analysis techniques.

**Step 5: Draw evidence-based conclusion**

Synthesize findings into confidence level (0-100%) and actionable recommendation (believe/skeptical/reject claim). Self-check using `resources/evaluators/rubric_research_claim_map.json` before delivering. Minimum standard: Average score ≥ 3.5.

## Evidence Quality Framework

**Rating scale:**

**Primary Evidence (Strongest):**
- Direct observation or measurement
- Original data or records
- First-hand accounts from participants
- Raw datasets, transaction logs
- Example: Sales database showing 10,000 customer IDs

**Secondary Evidence (Medium):**
- Analysis or interpretation of primary sources
- Expert synthesis of multiple primary sources
- Peer-reviewed research papers
- Verified news reporting with primary source citations
- Example: Industry analyst report analyzing public filings

**Tertiary Evidence (Weakest):**
- Summaries of secondary sources
- Textbooks, encyclopedias, Wikipedia
- Press releases, marketing materials
- Anecdotal reports without verification
- Example: Company blog post claiming customer count

**Non-Evidence (Unreliable):**
- Unverified social media posts
- Anonymous claims
- "Experts say" without attribution
- Circular references (A cites B, B cites A)
- Example: Viral tweet with no source

## Source Credibility Assessment

**Evaluate each source on:**

**Expertise (Does source have relevant knowledge?):**
- High: Domain expert with credentials, track record
- Medium: Knowledgeable but not specialist
- Low: No demonstrated expertise

**Independence (Is source biased or conflicted?):**
- High: Independent, no financial/personal stake
- Medium: Some potential bias, disclosed
- Low: Direct financial interest, undisclosed conflicts

**Track Record (Has source been accurate before?):**
- High: Consistent accuracy, corrections when wrong
- Medium: Mixed record or unknown history
- Low: History of errors, retractions, unreliability

**Methodology (How did source obtain information?):**
- High: Transparent, replicable, rigorous
- Medium: Some methodology disclosed
- Low: Opaque, unverifiable, cherry-picked

## Common Patterns

**Pattern 1: Vendor Claim Verification**
- **Claim type**: Product performance, customer count, ROI
- **Approach**: Seek independent verification (analysts, customers), test claims yourself
- **Red flags**: Only vendor sources, vague metrics, "up to X%" ranges

**Pattern 2: Academic Literature Review**
- **Claim type**: Research findings, causal claims
- **Approach**: Check for replication studies, meta-analyses, competing explanations
- **Red flags**: Single study, small sample, conflicts of interest, p-hacking

**Pattern 3: News Fact-Checking**
- **Claim type**: Events, statistics, quotes
- **Approach**: Trace to primary source, check multiple outlets, verify context
- **Red flags**: Anonymous sources, circular reporting, sensational framing

**Pattern 4: Statistical Claims**
- **Claim type**: Percentages, trends, correlations
- **Approach**: Check methodology, sample size, base rates, confidence intervals
- **Red flags**: Cherry-picked timeframes, denominator unclear, correlation ≠ causation

## Guardrails

**Avoid common biases:**
- **Confirmation bias**: Actively seek evidence against your hypothesis
- **Authority bias**: Don't accept claims just because source is prestigious
- **Recency bias**: Older evidence can be more reliable than latest claims
- **Availability bias**: Vivid anecdotes ≠ representative data

**Quality standards:**
- Rate confidence numerically (0-100%), not vague terms ("probably", "likely")
- Document all assumptions explicitly
- Distinguish "no evidence found" from "evidence of absence"
- Update conclusions as new evidence emerges
- Flag when evidence quality is insufficient for confident conclusion

**Ethical considerations:**
- Respect source privacy and attribution
- Avoid cherry-picking evidence to support desired conclusion
- Acknowledge limitations and uncertainties
- Correct errors promptly when found

## Quick Reference

**Resources:**
- **Quick verification**: [resources/template.md](resources/template.md)
- **Complex investigations**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: `resources/evaluators/rubric_research_claim_map.json`

**Evidence hierarchy**: Primary > Secondary > Tertiary

**Credibility factors**: Expertise + Independence + Track Record + Methodology

**Confidence calibration**:
- 90-100%: Near certain, multiple primary sources, high credibility
- 70-89%: Confident, strong secondary sources, some limitations
- 50-69%: Uncertain, conflicting evidence or weak sources
- 30-49%: Skeptical, more evidence against than for
- 0-29%: Likely false, strong evidence against
