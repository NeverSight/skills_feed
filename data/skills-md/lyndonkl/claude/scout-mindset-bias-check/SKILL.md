---
name: scout-mindset-bias-check
description: Use to detect and remove cognitive biases from reasoning. Invoke when prediction feels emotional, stuck at 50/50, or when you want to validate forecasting process. Use when user mentions scout mindset, soldier mindset, bias check, reversal test, scope sensitivity, or cognitive distortions.
---

# Scout Mindset & Bias Check

## Table of Contents
- [What is Scout Mindset?](#what-is-scout-mindset)
- [When to Use This Skill](#when-to-use-this-skill)
- [Interactive Menu](#interactive-menu)
- [Quick Reference](#quick-reference)
- [Resource Files](#resource-files)

---

## What is Scout Mindset?

**Scout Mindset** (Julia Galef) is the motivation to see things as they are, not as you wish them to be. Contrast with **Soldier Mindset**, which defends a position regardless of evidence.

**Core Principle:** Your goal is to map the territory accurately, not win an argument.

**Why It Matters:**
- Forecasting requires intellectual honesty
- Biases systemically distort probabilities
- Emotional attachment clouds judgment
- Motivated reasoning leads to overconfidence

---

## When to Use This Skill

Use this skill when:
- **Prediction feels emotional** - You want a certain outcome
- **Stuck at 50/50** - Indecisive, can't commit to probability
- **Defending a position** - Arguing for your forecast, not questioning it
- **After inside view analysis** - Used specific details, need bias check
- **Disagreement with others** - Different people, different probabilities
- **Before finalizing** - Last sanity check

Do NOT skip this when stakes are high, you have strong priors, or forecast affects you personally.

---

## Interactive Menu

**What would you like to do?**

### Core Workflows

**1. [Run the Reversal Test](#1-run-the-reversal-test)** - Check if you'd accept opposite evidence
- Detect motivated reasoning
- Validate evidence standards
- Expose special pleading

**2. [Check Scope Sensitivity](#2-check-scope-sensitivity)** - Ensure probabilities scale with inputs
- Linear scaling test
- Reference point calibration
- Magnitude assessment

**3. [Test Status Quo Bias](#3-test-status-quo-bias)** - Challenge "no change" assumptions
- Entropy principle
- Change vs stability energy
- Default state inversion

**4. [Audit Confidence Intervals](#4-audit-confidence-intervals)** - Validate CI width
- Surprise test
- Historical calibration
- Overconfidence check

**5. [Run Full Bias Audit](#5-run-full-bias-audit)** - Comprehensive bias scan
- All major cognitive biases
- Systematic checklist
- Prioritized remediation

**6. [Learn the Framework](#6-learn-the-framework)** - Deep dive into methodology
- Read [Scout vs Soldier Mindset](resources/scout-vs-soldier.md)
- Read [Cognitive Bias Catalog](resources/cognitive-bias-catalog.md)
- Read [Debiasing Techniques](resources/debiasing-techniques.md)

**7. Exit** - Return to main forecasting workflow

---

## 1. Run the Reversal Test

**Check if you'd accept evidence pointing the opposite direction.**

```
Reversal Test Progress:
- [ ] Step 1: State your current conclusion
- [ ] Step 2: Identify supporting evidence
- [ ] Step 3: Reverse the evidence
- [ ] Step 4: Ask "Would I still accept it?"
- [ ] Step 5: Adjust for double standards
```

### Step 1: State your current conclusion

**What are you predicting?**
- Prediction: [Event]
- Probability: [X]%
- Direction: [High/Low confidence]

### Step 2: Identify supporting evidence

**List the evidence that supports your conclusion.**

**Example:** Candidate A will win (75%)
1. Polls show A ahead by 5%
2. A has more campaign funding
3. Expert pundits favor A
4. A has better debate ratings

### Step 3: Reverse the evidence

**Imagine the same evidence pointed the OTHER way.**

**Reversed:** What if polls showed B ahead, B had more funding, experts favored B, and B had better ratings?

### Step 4: Ask "Would I still accept it?"

**The Critical Question:**
> If this reversed evidence existed, would I accept it as valid and change my prediction?

**Three possible answers:**

**A) YES - I would accept reversed evidence**
✓ No bias detected, continue with current reasoning

**B) NO - I would dismiss reversed evidence**
⚠ **Warning:** Motivated reasoning - you're accepting evidence when it supports you, dismissing equivalent evidence when it doesn't (special pleading)

**C) UNSURE - I'd need to think about it**
⚠ **Warning:** Asymmetric evidence standards suggest rationalizing, not reasoning

### Step 5: Adjust for double standards

**If you answered B or C:**

**Ask:** Why do I dismiss this evidence in one direction but accept it in the other? Is there an objective reason, or am I motivated by preference?

**Common rationalizations:**
- "This source is biased" (only when it disagrees)
- "Sample size too small" (only for unfavorable polls)
- "Outlier data" (only for data you dislike)
- "Context matters" (invoked selectively)

**The Fix:**
- **Option 1:** Reject the evidence entirely (if you wouldn't trust it reversed, don't trust it now)
- **Option 2:** Accept it in both directions (trust evidence regardless of direction)
- **Option 3:** Weight it appropriately (maybe it's weak evidence both ways)

**Probability adjustment:** If you detected double standards, move probability 10-15% toward 50%

**Next:** Return to [menu](#interactive-menu)

---

## 2. Check Scope Sensitivity

**Ensure your probabilities scale appropriately with magnitude.**

```
Scope Sensitivity Progress:
- [ ] Step 1: Identify the variable scale
- [ ] Step 2: Test linear scaling
- [ ] Step 3: Check reference point calibration
- [ ] Step 4: Validate magnitude assessment
- [ ] Step 5: Adjust for scope insensitivity
```

### Step 1: Identify the variable scale

**What dimension has magnitude?**
- Number of people (100 vs 10,000 vs 1,000,000)
- Dollar amounts ($1K vs $100K vs $10M)
- Time duration (1 month vs 1 year vs 10 years)

### Step 2: Test linear scaling

**The Linearity Test:** Double the input, check if impact doubles.

**Example: Startup funding**
- If raised $1M: ___%
- If raised $10M: ___%
- If raised $100M: ___%

**Scope sensitivity check:** Did probabilities scale reasonably? If they barely changed → Scope insensitive

### Step 3: Check reference point calibration

**The Anchoring Test:** Did you start with a number (base rate, someone else's forecast, round number) and insufficiently adjust?

**The fix:**
- Generate probability from scratch without looking at others
- Then compare and reconcile differences
- Don't just "split the difference" - reason about why estimates differ

### Step 4: Validate magnitude assessment

**The "1 vs 10 vs 100" Test:** For your forecast, vary the scale by 10×.

**Example: Project timeline**
- 1 month: P(success) = ___%
- 10 months: P(success) = ___%
- 100 months: P(success) = ___%

**Expected:** Probability should change significantly. If all three estimates are within 10 percentage points → Scope insensitivity

### Step 5: Adjust for scope insensitivity

**The problem:** Your emotional system responds to the category, not the magnitude.

**The fix:**

**Method 1: Logarithmic scaling** - Use log scale for intuition

**Method 2: Reference class by scale** - Don't use "startups" as reference class. Use "Startups that raised $1M" (10% success) vs "Startups that raised $100M" (60% success)

**Method 3: Explicit calibration** - Use a formula: P(success) = base_rate + k × log(amount)

**Next:** Return to [menu](#interactive-menu)

---

## 3. Test Status Quo Bias

**Challenge the assumption that "no change" is the default.**

```
Status Quo Bias Progress:
- [ ] Step 1: Identify status quo prediction
- [ ] Step 2: Calculate energy to maintain status quo
- [ ] Step 3: Invert the default
- [ ] Step 4: Apply entropy principle
- [ ] Step 5: Adjust probabilities
```

### Step 1: Identify status quo prediction

**Are you predicting "no change"?** Examples: "This trend will continue," "Market share will stay the same," "Policy won't change"

Status quo predictions often get inflated probabilities because change feels risky.

### Step 2: Calculate energy to maintain status quo

**The Entropy Principle:** In the absence of active energy input, systems decay toward disorder.

**Question:** "What effort is required to keep things the same?"

**Examples:**
- **Market share:** To maintain requires matching competitor innovation → Energy required: High → Status quo is HARD
- **Policy:** To maintain requires no proposals for change → Energy required: Low → Status quo is easier

### Step 3: Invert the default

**Mental Exercise:**
- **Normal framing:** "Will X change?" (Default = no)
- **Inverted framing:** "Will X stay the same?" (Default = no)

**Bias check:** If P(change) + P(same) ≠ 100%, you have status quo bias.

### Step 4: Apply entropy principle

**Second Law of Thermodynamics (applied to forecasting):**

**Ask:**
1. Is this system open or closed?
2. Is energy being input to maintain/improve?
3. Is that energy sufficient?

### Step 5: Adjust probabilities

**If you detected status quo bias:**

**For "no change" predictions that require high energy:**
- Reduce P(status quo) by 10-20%
- Increase P(change) correspondingly

**For predictions where inertia truly helps:** No adjustment needed

**The heuristic:** If maintaining status quo requires active effort, decay is more likely than you think.

**Next:** Return to [menu](#interactive-menu)

---

## 4. Audit Confidence Intervals

**Validate that your CI width reflects true uncertainty.**

```
Confidence Interval Audit Progress:
- [ ] Step 1: State current CI
- [ ] Step 2: Run surprise test
- [ ] Step 3: Check historical calibration
- [ ] Step 4: Compare to reference class variance
- [ ] Step 5: Adjust CI width
```

### Step 1: State current CI

**Current confidence interval:**
- Point estimate: ___%
- Lower bound: ___%
- Upper bound: ___%
- Width: ___ percentage points
- Confidence level: ___ (usually 80% or 90%)

### Step 2: Run surprise test

**The Surprise Test:** "Would I be **genuinely shocked** if the true value fell outside my confidence interval?"

**Calibration:**
- 80% CI → Should be shocked 20% of the time
- 90% CI → Should be shocked 10% of the time

**Test:** Imagine the outcome lands just below your lower bound or just above your upper bound.

**Three possible answers:**
- **A) "Yes, I'd be very surprised"** - ✓ CI appropriately calibrated
- **B) "No, not that surprised"** - ⚠ CI too narrow (overconfident) → Widen interval
- **C) "I'd be amazed if it landed in the range"** - ⚠ CI too wide → Narrow interval

### Step 3: Check historical calibration

**Look at your past forecasts:**
1. Collect last 20-50 forecasts with CIs
2. Count how many actual outcomes fell outside your CIs
3. Compare to theoretical expectation

| CI Level | Expected Outside | Your Actual |
|----------|------------------|-------------|
| 80% | 20% | ___% |
| 90% | 10% | ___% |

**Diagnosis:** Actual > Expected → CIs too narrow (overconfident) - Most common

### Step 4: Compare to reference class variance

**If you have reference class data:**
1. Calculate standard deviation of reference class outcomes
2. Your CI should roughly match that variance

**Example:** Reference class SD = 12%, your 80% CI ≈ Point estimate ± 15%

If your CI is narrower than reference class variance, you're claiming to know more than average. Justify why, or widen CI.

### Step 5: Adjust CI width

**Adjustment rules:**
- **If overconfident:** Multiply current width by 1.5× to 2×
- **If underconfident:** Reduce width by 0.5× to 0.75×

**Next:** Return to [menu](#interactive-menu)

---

## 5. Run Full Bias Audit

**Comprehensive scan of major cognitive biases.**

```
Full Bias Audit Progress:
- [ ] Step 1: Confirmation bias check
- [ ] Step 2: Availability bias check
- [ ] Step 3: Anchoring bias check
- [ ] Step 4: Affect heuristic check
- [ ] Step 5: Overconfidence check
- [ ] Step 6: Attribution error check
- [ ] Step 7: Prioritize and remediate
```

See [Cognitive Bias Catalog](resources/cognitive-bias-catalog.md) for detailed descriptions.

**Quick audit questions:**

### 1. Confirmation Bias
- [ ] Did I seek out disconfirming evidence?
- [ ] Did I give equal weight to evidence against my position?
- [ ] Did I actively try to prove myself wrong?

**If NO to any → Confirmation bias detected**

### 2. Availability Bias
- [ ] Did I rely on recent/memorable examples?
- [ ] Did I use systematic data vs "what comes to mind"?
- [ ] Did I check if my examples are representative?

**If NO to any → Availability bias detected**

### 3. Anchoring Bias
- [ ] Did I generate my estimate independently first?
- [ ] Did I avoid being influenced by others' numbers?
- [ ] Did I adjust sufficiently from initial anchor?

**If NO to any → Anchoring bias detected**

### 4. Affect Heuristic
- [ ] Do I have an emotional preference for the outcome?
- [ ] Did I separate "what I want" from "what will happen"?
- [ ] Would I make the same forecast if incentives were reversed?

**If NO to any → Affect heuristic detected**

### 5. Overconfidence
- [ ] Did I run a premortem?
- [ ] Are my CIs wide enough (surprise test)?
- [ ] Did I identify ways I could be wrong?

**If NO to any → Overconfidence detected**

### 6. Fundamental Attribution Error
- [ ] Did I attribute success to skill vs luck appropriately?
- [ ] Did I consider situational factors, not just personal traits?
- [ ] Did I avoid "great man" narratives?

**If NO to any → Attribution error detected**

### Step 7: Prioritize and remediate

**For each detected bias:**
1. **Severity:** High / Medium / Low
2. **Direction:** Pushing probability up or down?
3. **Magnitude:** Estimated percentage point impact

**Remediation example:**

| Bias | Severity | Direction | Adjustment |
|------|----------|-----------|------------|
| Confirmation | High | Up | -15% |
| Availability | Medium | Up | -10% |
| Affect heuristic | High | Up | -20% |

**Net adjustment:** -45% → Move probability down by 45 points (e.g., 80% → 35%)

**Next:** Return to [menu](#interactive-menu)

---

## 6. Learn the Framework

**Deep dive into the methodology.**

### Resource Files

📄 **[Scout vs Soldier Mindset](resources/scout-vs-soldier.md)**
- Julia Galef's framework
- Motivated reasoning
- Intellectual honesty
- Identity and beliefs

📄 **[Cognitive Bias Catalog](resources/cognitive-bias-catalog.md)**
- 20+ major biases
- How they affect forecasting
- Detection methods
- Remediation strategies

📄 **[Debiasing Techniques](resources/debiasing-techniques.md)**
- Systematic debiasing process
- Pre-commitment strategies
- External accountability
- Algorithmic aids

**Next:** Return to [menu](#interactive-menu)

---

## Quick Reference

### The Scout Commandments

1. **Truth over comfort** - Accuracy beats wishful thinking
2. **Seek disconfirmation** - Try to prove yourself wrong
3. **Hold beliefs lightly** - Probabilistic, not binary
4. **Update incrementally** - Change mind with evidence
5. **Separate wanting from expecting** - Desire ≠ Forecast
6. **Check your work** - Run bias audits routinely
7. **Stay calibrated** - Track accuracy over time

> Scout mindset is the drive to see things as they are, not as you wish them to be.

---

## Resource Files

📁 **resources/**
- [scout-vs-soldier.md](resources/scout-vs-soldier.md) - Mindset framework
- [cognitive-bias-catalog.md](resources/cognitive-bias-catalog.md) - Comprehensive bias reference
- [debiasing-techniques.md](resources/debiasing-techniques.md) - Remediation strategies

---

**Ready to start? Choose a number from the [menu](#interactive-menu) above.**
