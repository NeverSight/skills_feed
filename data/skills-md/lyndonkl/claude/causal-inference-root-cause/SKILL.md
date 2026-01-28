---
name: causal-inference-root-cause
description: Use when investigating why something happened and need to distinguish correlation from causation, identify root causes vs symptoms, test competing hypotheses, control for confounding variables, or design experiments to validate causal claims. Invoke when debugging systems, analyzing failures, researching health outcomes, evaluating policy impacts, or when user mentions root cause, causal chain, confounding, spurious correlation, or asks "why did this really happen?"
---

# Causal Inference & Root Cause Analysis

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Causal Inference?](#what-is-causal-inference)
- [Workflow](#workflow)
  - [1. Define the Effect](#1--define-the-effect)
  - [2. Generate Hypotheses](#2--generate-hypotheses)
  - [3. Build Causal Model](#3--build-causal-model)
  - [4. Test Causality](#4--test-causality)
  - [5. Document & Validate](#5--document--validate)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Systematically investigate causal relationships to identify true root causes rather than mere correlations or symptoms. This skill helps distinguish genuine causation from spurious associations, test competing explanations, and design interventions that address underlying drivers.

## When to Use This Skill

- Investigating system failures or production incidents
- Debugging performance issues with multiple potential causes
- Analyzing why a metric changed (e.g., conversion rate drop)
- Researching health outcomes or treatment effects
- Evaluating policy or intervention impacts
- Distinguishing correlation from causation in data
- Identifying confounding variables in experiments
- Tracing symptom back to root cause
- Testing competing hypotheses about cause-effect relationships
- Designing experiments to validate causal claims
- Understanding why a project succeeded or failed
- Analyzing customer churn or retention drivers

**Trigger phrases:** "root cause", "why did this happen", "causal chain", "correlation vs causation", "confounding", "spurious correlation", "what really caused", "underlying driver"

## What is Causal Inference?

A systematic approach to determine whether X causes Y (not just correlates with Y):

- **Correlation**: X and Y move together (may be coincidental or due to third factor Z)
- **Causation**: Changing X directly causes change in Y (causal mechanism exists)

**Key Concepts:**

- **Root cause**: The fundamental issue that, if resolved, prevents the problem
- **Proximate cause**: Immediate trigger (may be symptom, not root)
- **Confounding variable**: Third factor that causes both X and Y, creating spurious correlation
- **Counterfactual**: "What would have happened without X?" - the key causal question
- **Causal mechanism**: The pathway or process through which X affects Y

**Quick Example:**

```markdown
# Effect: Website conversion rate dropped 30%

## Competing Hypotheses:
1. New checkout UI is confusing (proximate)
2. Payment processor latency increased (proximate)
3. We changed to a cheaper payment processor that's slower (root cause)

## Test:
- Rollback UI (no change) → UI not cause
- Check payment logs (confirm latency) → latency is cause
- Trace to processor change → processor change is root cause

## Counterfactual:
"If we hadn't switched processors, would conversion have dropped?"
→ No, conversion was fine with old processor

## Conclusion:
Root cause = processor switch
Mechanism = slow checkout → user abandonment
```

## Workflow

Copy this checklist and track your progress:

```
Root Cause Analysis Progress:
- [ ] Step 1: Define the effect
- [ ] Step 2: Generate hypotheses
- [ ] Step 3: Build causal model
- [ ] Step 4: Test causality
- [ ] Step 5: Document and validate
```

**Step 1: Define the effect**

Describe effect/outcome (what happened, be specific), quantify if possible (magnitude, frequency), establish timeline (when it started, is it ongoing?), determine baseline (what's normal, what changed?), and identify stakeholders (who's impacted, who needs answers?). Key questions: What exactly are we explaining? One-time event or recurring pattern? How do we measure objectively?

**Step 2: Generate hypotheses**

List proximate causes (immediate triggers/symptoms), identify potential root causes (underlying factors), consider confounders (third factors creating spurious associations), and challenge assumptions (what if initial theory wrong?). Techniques: 5 Whys (ask "why" repeatedly), Fishbone diagram (categorize causes), Timeline analysis (what changed before effect?), Differential diagnosis (what else explains symptoms?). For simple investigations → Use `resources/template.md`. For complex problems → Study `resources/methodology.md` for advanced techniques.

**Step 3: Build causal model**

Draw causal chains (A → B → C → Effect), identify necessary vs sufficient causes, map confounding relationships (what influences both cause and effect?), note temporal sequence (cause precedes effect - necessary for causation), and specify mechanisms (HOW X causes Y). Model elements: Direct cause (X → Y), Indirect (X → Z → Y), Confounding (Z → X and Z → Y), Mediating variable (X → M → Y), Moderating variable (X → Y depends on M).

**Step 4: Test causality**

Check temporal sequence (cause before effect?), assess strength of association (strong correlation?), look for dose-response (more cause → more effect?), test counterfactual (what if cause absent/removed?), search for mechanism (explain HOW), check consistency (holds across contexts?), and rule out confounders. Evidence hierarchy: RCT (gold standard) > natural experiment > longitudinal > case-control > cross-sectional > expert opinion. Use Bradford Hill Criteria (9 factors: strength, consistency, specificity, temporality, dose-response, plausibility, coherence, experiment, analogy).

**Step 5: Document and validate**

Create `causal-inference-root-cause.md` with: effect description/quantification, competing hypotheses, causal model (chains, confounders, mechanisms), evidence assessment, root cause(s) with confidence level, recommended tests/interventions, and limitations/alternatives. Validate using `resources/evaluators/rubric_causal_inference_root_cause.json`: verify distinguished proximate from root cause, controlled confounders, explained mechanism, assessed evidence systematically, noted uncertainty, recommended interventions, acknowledged alternatives. Minimum standard: Score ≥ 3.5.

## Common Patterns

**For incident investigation (engineering):**
- Effect: System outage, performance degradation
- Hypotheses: Recent deploy, traffic spike, dependency failure, resource exhaustion
- Model: Timeline + dependency graph + recent changes
- Test: Logs, metrics, rollback experiments
- Output: Postmortem with root cause and prevention plan

**For metric changes (product/business):**
- Effect: Conversion drop, revenue change, user engagement shift
- Hypotheses: Product changes, seasonality, market shifts, measurement issues
- Model: User journey + external factors + recent experiments
- Test: Cohort analysis, A/B test data, segmentation
- Output: Causal explanation with recommended actions

**For policy evaluation (research/public policy):**
- Effect: Health outcome, economic indicator, social metric
- Hypotheses: Policy intervention, confounding factors, secular trends
- Model: DAG with confounders + mechanisms
- Test: Difference-in-differences, regression discontinuity, propensity matching
- Output: Causal effect estimate with confidence intervals

**For debugging (software):**
- Effect: Bug, unexpected behavior, test failure
- Hypotheses: Recent changes, edge cases, race conditions, dependency issues
- Model: Code paths + data flows + timing
- Test: Reproduce, isolate, binary search, git bisect
- Output: Bug report with root cause and fix

## Guardrails

**Do:**
- Distinguish correlation from causation explicitly
- Generate multiple competing hypotheses (not just confirm first theory)
- Map out confounding variables and control for them
- Specify causal mechanisms (HOW X causes Y)
- Test counterfactuals ("what if X hadn't happened?")
- State confidence levels and uncertainty
- Acknowledge alternative explanations
- Recommend testable interventions based on root cause

**Don't:**
- Confuse proximate cause with root cause
- Cherry-pick evidence that confirms initial hypothesis
- Assume correlation implies causation
- Ignore confounding variables
- Skip mechanism explanation (just stating correlation)
- Overstate confidence without strong evidence
- Stop at first plausible explanation without testing alternatives
- Propose interventions without identifying root cause

**Common Pitfalls:**
- **Post hoc ergo propter hoc**: "After this, therefore because of this" (temporal sequence ≠ causation)
- **Spurious correlation**: Two things correlate due to third factor or coincidence
- **Confounding**: Third variable causes both X and Y
- **Reverse causation**: Y causes X, not X causes Y
- **Selection bias**: Sample is not representative
- **Regression to mean**: Extreme values naturally move toward average

## Quick Reference

- **Template**: `resources/template.md` - Structured framework for root cause analysis
- **Methodology**: `resources/methodology.md` - Advanced techniques (DAGs, confounding control, Bradford Hill criteria)
- **Quality rubric**: `resources/evaluators/rubric_causal_inference_root_cause.json`
- **Output file**: `causal-inference-root-cause.md`
- **Key distinction**: Correlation (X and Y move together) vs. Causation (X → Y mechanism)
- **Gold standard test**: Randomized controlled trial (eliminates confounding)
- **Essential criteria**: Temporal sequence (cause before effect), mechanism (how it works), counterfactual (what if cause absent)
