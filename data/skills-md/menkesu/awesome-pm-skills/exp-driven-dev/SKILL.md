---
name: exp-driven-dev
description: Builds features with A/B testing in mind using Ronny Kohavi's frameworks and Netflix/Airbnb experimentation culture. Use when implementing feature flags, choosing metrics, designing experiments, or building for fast iteration. Focuses on guardrail metrics, statistical significance, and experiment-driven development.
---

# Experimentation-Driven Development

## When This Skill Activates

Claude uses this skill when:
- Building new features that affect core metrics
- Implementing A/B testing infrastructure
- Making data-driven decisions
- Setting up feature flags for gradual rollouts
- Choosing which metrics to track

## Core Frameworks

### 1. Experiment Design (Source: Ronny Kohavi, Microsoft/Netflix)

**The HITS Framework:**

**H - Hypothesis:**
> "We believe that [change] will cause [metric] to [increase/decrease] because [reason]"

**I - Implementation:**
- Feature flag setup
- Treatment vs control
- Sample size calculation

**T - Test:**
- Run for statistical significance
- Monitor guardrail metrics
- Watch for unexpected effects

**S - Ship or Stop:**
- Ship if positive
- Stop if negative
- Iterate if inconclusive

**Example:**
```markdown
Hypothesis:
"We believe that adding social proof ('X people bought this') 
will increase conversion rate by 10% 
because it reduces purchase anxiety."

Implementation:
- Control: No social proof
- Treatment: Show "X people bought"
- Sample size: 10,000 users per variant
- Duration: 2 weeks

Test:
- Primary metric: Conversion rate
- Guardrails: Cart abandonment, return rate

Ship or Stop:
- If conversion +5% or more → Ship
- If conversion -2% or less → Stop
- If inconclusive → Iterate and retest
```

---

### 2. Metric Selection

**Primary Metric:**
- ONE metric you're trying to move
- Directly tied to business value
- Clear success threshold

**Guardrail Metrics:**
- Metrics that shouldn't degrade
- Prevent gaming the system
- Ensure quality maintained

**Example:**
```
Feature: Streamlined checkout

Primary Metric:
✅ Purchase completion rate (+10%)

Guardrail Metrics:
⚠️ Cart abandonment (don't increase)
⚠️ Return rate (don't increase)
⚠️ Support tickets (don't increase)
⚠️ Load time (stay <2s)
```

---

### 3. Statistical Significance

**The Math:**
```
Minimum sample size = (Effect size, Confidence, Power)

Typical settings:
- Confidence: 95% (p < 0.05)
- Power: 80% (detect 80% of real effects)
- Effect size: Minimum detectable change

Example:
- Baseline conversion: 10%
- Minimum detectable effect: +1% (to 11%)
- Required: ~15,000 users per variant
```

**Common Mistakes:**
- ❌ Stopping test early (peeking bias)
- ❌ Running too short (seasonal effects)
- ❌ Too many variants (dilutes sample)
- ❌ Changing test mid-flight

---

### 4. Feature Flag Architecture

**Implementation:**
```javascript
// Feature flag pattern
function checkoutFlow(user) {
  if (isFeatureEnabled(user, 'new-checkout')) {
    return newCheckoutExperience();
  } else {
    return oldCheckoutExperience();
  }
}

// Gradual rollout
function isFeatureEnabled(user, feature) {
  const rolloutPercent = getFeatureRollout(feature);
  const userBucket = hashUserId(user.id) % 100;
  return userBucket < rolloutPercent;
}

// Experiment assignment
function assignExperiment(user, experiment) {
  const variant = consistentHash(user.id, experiment);
  track('experiment_assigned', {
    userId: user.id,
    experiment: experiment,
    variant: variant
  });
  return variant;
}
```

---

## Decision Tree: Should We Experiment?

```
NEW FEATURE
│
├─ Affects core metrics? ──────YES──→ EXPERIMENT REQUIRED
│  NO ↓
│
├─ Risky change? ──────────────YES──→ EXPERIMENT RECOMMENDED
│  NO ↓
│
├─ Uncertain impact? ──────────YES──→ EXPERIMENT USEFUL
│  NO ↓
│
├─ Easy to A/B test? ─────────YES──→ WHY NOT EXPERIMENT?
│  NO ↓
│
└─ SHIP WITHOUT TEST ←────────────────┘
   (But still feature flag for rollback)
```

## Action Templates

### Template 1: Experiment Spec

```markdown
# Experiment: [Name]

## Hypothesis
**We believe:** [change]
**Will cause:** [metric] to [increase/decrease]
**Because:** [reasoning]

## Variants

### Control (50%)
[Current experience]

### Treatment (50%)
[New experience]

## Metrics

### Primary Metric
- **What:** [metric name]
- **Current:** [baseline]
- **Target:** [goal]
- **Success:** [threshold]

### Guardrail Metrics
- **Metric 1:** [name] - Don't decrease
- **Metric 2:** [name] - Don't increase
- **Metric 3:** [name] - Maintain

## Sample Size
- **Users needed:** [X per variant]
- **Duration:** [Y days]
- **Confidence:** 95%
- **Power:** 80%

## Implementation
```javascript
if (experiment('feature-name') === 'treatment') {
  // New experience
} else {
  // Old experience
}
```

## Success Criteria
- [ ] Primary metric improved by [X]%
- [ ] No guardrail degradation
- [ ] Statistical significance reached
- [ ] No unexpected negative effects

## Decision
- **If positive:** Ship to 100%
- **If negative:** Rollback, iterate
- **If inconclusive:** Extend or redesign
```

### Template 2: Feature Flag Implementation

```typescript
// features.ts
export const FEATURES = {
  'new-checkout': {
    rollout: 10,  // 10% of users
    enabled: true,
    description: 'New streamlined checkout flow'
  },
  'ai-recommendations': {
    rollout: 0,  // Not live yet
    enabled: false,
    description: 'AI-powered product recommendations'
  }
};

// feature-flags.ts
export function isEnabled(userId: string, feature: string): boolean {
  const config = FEATURES[feature];
  if (!config || !config.enabled) return false;
  
  const bucket = consistentHash(userId) % 100;
  return bucket < config.rollout;
}

// usage in code
if (isEnabled(user.id, 'new-checkout')) {
  return <NewCheckout />;
} else {
  return <OldCheckout />;
}
```

### Template 3: Experiment Dashboard

```markdown
# Experiment Dashboard

## Active Experiments

### Experiment 1: [Name]
- **Status:** Running
- **Started:** [date]
- **Progress:** [X]% sample size reached
- **Primary metric:** [current result]
- **Guardrails:** ✅ All healthy

### Experiment 2: [Name]
- **Status:** Complete
- **Result:** Treatment won (+15% conversion)
- **Decision:** Ship to 100%
- **Shipped:** [date]

## Key Metrics

### Experiment Velocity
- **Experiments launched:** [X per month]
- **Win rate:** [Y]%
- **Average duration:** [Z] days

### Impact
- **Revenue impact:** +$[X]
- **Conversion improvement:** +[Y]%
- **User satisfaction:** +[Z] NPS

## Learnings
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]
```

## Quick Reference

### 🧪 Experiment Checklist

**Before Starting:**
- [ ] Hypothesis written (believe → cause → because)
- [ ] Primary metric defined
- [ ] Guardrails identified
- [ ] Sample size calculated
- [ ] Feature flag implemented
- [ ] Tracking instrumented

**During Experiment:**
- [ ] Don't peek early (wait for significance)
- [ ] Monitor guardrails daily
- [ ] Watch for unexpected effects
- [ ] Log any external factors (holidays, outages)

**After Experiment:**
- [ ] Statistical significance reached
- [ ] Guardrails not degraded
- [ ] Decision made (ship/stop/iterate)
- [ ] Learning documented

---

## Real-World Examples

### Example 1: Netflix Experimentation

**Volume:** 250+ experiments running at once
**Approach:** Everything is an experiment
**Culture:** "Strong opinions, weakly held - let data decide"

**Example Test:**
- Hypothesis: Bigger thumbnails increase engagement
- Result: No improvement, actually hurt browse time
- Decision: Rollback
- Learning: Saved $$ by not shipping

---

### Example 2: Airbnb's Experiments

**Test:** New search ranking algorithm
**Primary:** Bookings per search
**Guardrails:** 
- Search quality (ratings of bookings)
- Host earnings (don't concentrate bookings)
- Guest satisfaction

**Result:** +3% bookings, all guardrails healthy → Ship

---

### Example 3: Stripe's Feature Flags

**Approach:** Every feature behind flag
**Benefits:**
- Instant rollback (flip flag)
- Gradual rollout (1% → 5% → 25% → 100%)
- Test in production safely

**Example:**
```javascript
if (experiments.isEnabled('instant-payouts')) {
  return <InstantPayouts />;
}
```

---

## Common Pitfalls

### ❌ Mistake 1: Peeking Too Early
**Problem:** Stopping test before statistical significance
**Fix:** Calculate sample size upfront, wait for it

### ❌ Mistake 2: No Guardrails
**Problem:** Gaming the metric (increase clicks but hurt quality)
**Fix:** Always define guardrails

### ❌ Mistake 3: Too Many Variants
**Problem:** Not enough users per variant
**Fix:** Limit to 2-3 variants max

### ❌ Mistake 4: Ignoring External Factors
**Problem:** Holiday spike looks like treatment effect
**Fix:** Note external events, extend duration

---

## Related Skills

- **metrics-frameworks** - For choosing right metrics
- **growth-embedded** - For growth experiments
- **ship-decisions** - For when to ship vs test more
- **strategic-build** - For deciding what to test

---

## Key Quotes

**Ronny Kohavi:**
> "The best way to predict the future is to run an experiment."

**Netflix Culture:**
> "Strong opinions, weakly held. Let data be the tie-breaker."

**Airbnb:**
> "We trust our intuition to generate hypotheses, and we trust data to make decisions."

---

## Further Learning

- **references/experiment-design-guide.md** - Complete methodology
- **references/statistical-significance.md** - Sample size calculations
- **references/feature-flags-implementation.md** - Code examples
- **references/guardrail-metrics.md** - Choosing guardrails

