---
name: decision-frameworks
description: Structures difficult decisions using Annie Duke's probabilistic thinking and Ben Horowitz's hard decisions frameworks. Use when facing tough choices, applying expected value thinking, or reducing decision paralysis with regret minimization and pre-mortems.
---

# Decision Architecture

## When This Skill Activates

Claude uses this skill when:
- Facing difficult product decisions
- Choosing between multiple options
- Reducing decision paralysis
- Evaluating tradeoffs

## Core Frameworks

### 1. Expected Value Thinking (Source: Annie Duke)

**The Formula:**
```
Expected Value = (Probability of Success × Value if Successful) 
                - (Probability of Failure × Cost if Fails)
```

**Example:**
```markdown
Decision: Build feature A or B?

Feature A:
- 70% chance of +$100K revenue = $70K
- 30% chance of -$20K cost = -$6K
- Expected value: +$64K

Feature B:
- 30% chance of +$500K revenue = $150K
- 70% chance of -$50K cost = -$35K
- Expected value: +$115K

Choose B (higher EV despite lower probability)
```

### 2. Regret Minimization (Source: Jeff Bezos)

**The Question:**
> "When I'm 80 years old, will I regret not trying this?"

**Framework:**
- Imagine yourself in the future
- Work backwards
- Minimize long-term regret

---

## Action Templates

### Template: Decision Matrix

```markdown
# Decision: [Choice A vs Choice B]

## Expected Value

### Option A
- Success probability: [X]%
- Success value: [$Y]
- Failure probability: [Z]%
- Failure cost: [$W]
- **Expected value:** [$EV]

### Option B
- Success probability: [X]%
- Success value: [$Y]
- Failure probability: [Z]%
- Failure cost: [$W]
- **Expected value:** [$EV]

## Regret Minimization
- If I choose A, will I regret not trying B?
- If I choose B, will I regret not trying A?

## Reversibility
- Can we reverse this? [Yes/No]
- Cost to reverse: [Low/Medium/High]

## Decision: [Option] because [reasoning]
```

---

## Quick Reference

### 🎲 Decision Checklist

**Analysis:**
- [ ] Expected value calculated
- [ ] Regret minimization applied
- [ ] Reversibility assessed
- [ ] Pre-mortem completed

**Decision:**
- [ ] Choice made
- [ ] Reasoning documented
- [ ] Success criteria defined

---

## Key Quotes

**Annie Duke:**
> "Life is poker, not chess. We're making decisions with incomplete information."

**Jeff Bezos:**
> "Most decisions should probably be made with somewhere around 70% of the information you wish you had."

