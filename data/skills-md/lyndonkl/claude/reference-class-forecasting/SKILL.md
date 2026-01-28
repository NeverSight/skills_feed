---
name: reference-class-forecasting
description: Use when starting a forecast to establish a statistical baseline (base rate) before analyzing specifics. Invoke when need to anchor predictions in historical reality, avoid "this time is different" bias, or establish outside view before inside view analysis. Use when user mentions base rates, reference classes, outside view, or starting a new prediction.
---

# Reference Class Forecasting

## Table of Contents
- [What is Reference Class Forecasting?](#what-is-reference-class-forecasting)
- [When to Use This Skill](#when-to-use-this-skill)
- [Interactive Menu](#interactive-menu)
- [Quick Reference](#quick-reference)
- [Resource Files](#resource-files)

---

## What is Reference Class Forecasting?

Reference class forecasting is the practice of anchoring predictions in **historical reality** by identifying a class of similar past events and using their statistical frequency as a starting point. This is the "Outside View" - looking at what usually happens to things like this, before getting distracted by the specific details of "this case."

**Core Principle:** Assume this event is **average** until you have specific evidence proving otherwise.

**Why It Matters:**
- Defeats "inside view" bias (thinking your case is unique)
- Prevents base rate neglect (ignoring statistical baselines)
- Provides objective anchor before subjective analysis
- Forces humility and statistical thinking

---

## When to Use This Skill

Use this skill when:
- **Starting any forecast** - Establish base rate FIRST
- **Someone says "this time is different"** - Test if it really is
- **Making predictions about success/failure** - Find historical frequencies
- **Evaluating startup/project outcomes** - Anchor in class statistics
- **Challenged by confident predictions** - Ground in reality
- **Before detailed analysis** - Get outside view baseline

Do NOT use when:
- Event has literally never happened (novel situation)
- Working with deterministic physical laws
- Pure chaos with no patterns

---

## Interactive Menu

**What would you like to do?**

### Core Workflows

**1. [Find My Base Rate](#1-find-my-base-rate)** - Identify reference class and get statistical baseline
- Guided process to select correct reference class
- Search strategies for finding historical frequencies
- Validation that you have the right anchor

**2. [Test "This Time Is Different"](#2-test-this-time-is-different)** - Challenge uniqueness claims
- Reversal test for uniqueness bias
- Similarity matching framework
- Burden of proof calculator

**3. [Calculate Funnel Base Rates](#3-calculate-funnel-base-rates)** - Multi-stage probability chains
- When no single base rate exists
- Sequential probability modeling
- Product rule for compound events

**4. [Validate My Reference Class](#4-validate-my-reference-class)** - Ensure you chose the right comparison set
- Too broad vs too narrow test
- Homogeneity check
- Sample size evaluation

**5. [Learn the Framework](#5-learn-the-framework)** - Deep dive into methodology
- Read [Outside View Principles](resources/outside-view-principles.md)
- Read [Reference Class Selection Guide](resources/reference-class-selection.md)
- Read [Common Pitfalls](resources/common-pitfalls.md)

**6. Exit** - Return to main forecasting workflow

---

## 1. Find My Base Rate

**Let's establish your statistical baseline.**

### Step 1: What are you forecasting?
Tell me the specific event or outcome you're predicting.

**Example prompts:**
- "Will this startup succeed?"
- "Will this bill pass Congress?"
- "Will this project launch on time?"

---

### Step 2: Identify the Reference Class

I'll help you identify what bucket this belongs to.

**Framework:**
- **Too broad:** "All companies" → meaningless
- **Just right:** "Seed-stage B2B SaaS startups in fintech"
- **Too narrow:** "Companies founded by people named Steve in 2024" → no data

**Key Questions:**
1. What type of entity is this? (company, bill, project, person, etc.)
2. What stage/size/category?
3. What industry/domain?
4. What time period is relevant?

I'll work with you to refine this until we have a specific, searchable class.

---

### Step 3: Search for Historical Data

I'll help you find the base rate using:
- **Web search** for published statistics
- **Academic studies** on success rates
- **Government/industry reports**
- **Proxy metrics** if direct data unavailable

**Search Strategy:**
```
"historical success rate of [reference class]"
"[reference class] failure statistics"
"[reference class] survival rate"
"what percentage of [reference class]"
```

---

### Step 4: Set Your Anchor

Once we find the base rate, that becomes your **starting probability**.

**The Rule:**
> You are NOT allowed to move from this base rate until you have specific,
> evidence-based reasons in your "inside view" analysis.

**Default anchors if no data found:**
- Novel innovation: 10-20% (most innovations fail)
- Established industry: 50% (uncertain)
- Regulated/proven process: 70-80% (systems work)

**Next:** Return to [menu](#interactive-menu) or proceed to inside view analysis.

---

## 2. Test "This Time Is Different"

**Challenge uniqueness bias.**

When someone (including yourself) believes "this case is special," we need to stress-test that belief.

### The Uniqueness Audit

**Question 1: Similarity Matching**
- What are 5 historical cases that are most similar to this one?
- For each, what was the outcome?
- How is your case materially different from these?

**Question 2: The Reversal Test**
- If someone claimed a different case was "unique" for the same reasons you're claiming, would you accept it?
- Are you applying special pleading?

**Question 3: Burden of Proof**
The base rate says [X]%. You claim it should be [Y]%.

Calculate the gap: `|Y - X|`

**Required evidence strength:**
- Gap < 10%: Minimal evidence needed
- Gap 10-30%: Moderate evidence needed (2-3 specific factors)
- Gap > 30%: Extraordinary evidence needed (multiple independent strong signals)

### Output

I'll tell you:
1. Whether "this time is different" is justified
2. How much you can reasonably adjust from the base rate
3. What evidence would be needed to justify larger moves

**Next:** Return to [menu](#interactive-menu)

---

## 3. Calculate Funnel Base Rates

**For multi-stage processes without a single base rate.**

### When to Use
- No direct statistic exists (e.g., "success rate of X")
- Event requires multiple sequential steps
- Each stage has independent probabilities

### The Funnel Method

**Example: "Will Bill X become law?"**

No direct data on "Bill X success rate," but we can model the funnel:

1. **Stage 1:** Bills introduced → Bills that reach committee
   - P(committee | introduced) = ?

2. **Stage 2:** Bills in committee → Bills that reach floor vote
   - P(floor | committee) = ?

3. **Stage 3:** Bills voted on → Bills that pass
   - P(pass | floor vote) = ?

**Final Base Rate:**
```
P(law) = P(committee) × P(floor) × P(pass)
```

### Process

I'll help you:
1. **Decompose** the event into sequential stages
2. **Search** for statistics on each stage
3. **Multiply** probabilities using the product rule
4. **Validate** the model (are stages truly independent?)

### Common Funnels
- Startup success: Seed → Series A → Profitability → Exit
- Drug approval: Discovery → Trials → FDA → Market
- Project delivery: Planning → Development → Testing → Launch

**Next:** Return to [menu](#interactive-menu)

---

## 4. Validate My Reference Class

**Ensure you chose the right comparison set.**

### The Three Tests

**Test 1: Homogeneity**
- Are the members of this class actually similar enough?
- Is there high variance in outcomes?
- Should you subdivide further?

**Example:** "Tech startups" is too broad (consumer vs B2B vs hardware are very different). Subdivide.

---

**Test 2: Sample Size**
- Do you have enough historical cases?
- Minimum: 20-30 cases for meaningful statistics
- If N < 20: Widen the class or acknowledge high uncertainty

---

**Test 3: Relevance**
- Have conditions changed since the historical data?
- Are there structural differences (regulation, technology, market)?
- Time decay: Data from >10 years ago may be stale

### Validation Checklist

I'll walk you through:
- [ ] Class has 20+ historical examples
- [ ] Members are reasonably homogeneous
- [ ] Data is from relevant time period
- [ ] No major structural changes since data collection
- [ ] Class is specific enough to be meaningful
- [ ] Class is broad enough to have data

**Output:** Confidence level in your reference class (High/Medium/Low)

**Next:** Return to [menu](#interactive-menu)

---

## 5. Learn the Framework

**Deep dive into the methodology.**

### Resource Files

📄 **[Outside View Principles](resources/outside-view-principles.md)**
- Statistical thinking vs narrative thinking
- Why the outside view beats experts
- Kahneman's planning fallacy research
- When outside view fails

📄 **[Reference Class Selection Guide](resources/reference-class-selection.md)**
- Systematic method for choosing comparison sets
- Balancing specificity vs data availability
- Similarity metrics and matching
- Edge cases and judgment calls

📄 **[Common Pitfalls](resources/common-pitfalls.md)**
- Base rate neglect examples
- "This time is different" bias
- Overfitting to small samples
- Ignoring regression to the mean
- Availability bias in class selection

**Next:** Return to [menu](#interactive-menu)

---

## Quick Reference

### The Outside View Commandments

1. **Base Rate First:** Establish statistical baseline BEFORE analyzing specifics
2. **Assume Average:** Treat case as typical until proven otherwise
3. **Burden of Proof:** Large deviations from base rate require strong evidence
4. **Class Precision:** Reference class should be specific but data-rich
5. **No Narratives:** Resist compelling stories; trust frequencies

### One-Sentence Summary

> Find what usually happens to things like this, start there, and only move with evidence.

### Integration with Other Skills

- **Before:** Use `estimation-fermi` if you need to calculate base rate from components
- **After:** Use `bayesian-reasoning-calibration` to update from base rate with new evidence
- **Companion:** Use `scout-mindset-bias-check` to validate you're not cherry-picking the reference class

---

## Resource Files

📁 **resources/**
- [outside-view-principles.md](resources/outside-view-principles.md) - Theory and research
- [reference-class-selection.md](resources/reference-class-selection.md) - Systematic selection method
- [common-pitfalls.md](resources/common-pitfalls.md) - What to avoid

---

**Ready to start? Choose a number from the [menu](#interactive-menu) above.**
