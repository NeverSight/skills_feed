---
name: prioritization-craft
description: Applies prioritization frameworks including RICE, ICE, Value vs Effort, and Kano model. Use when prioritizing features, managing backlog, making tradeoffs, or saying no gracefully. Based on Shreyas Doshi and Intercom frameworks.
---

# Prioritization Engine

## When This Skill Activates

Claude uses this skill when:
- Prioritizing feature requests
- Managing product backlog
- Making tradeoff decisions
- Saying no gracefully

## Core Frameworks

### 1. RICE Framework (Source: Intercom)

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach: How many users affected (per quarter)
Impact: How much impact (0.25, 0.5, 1, 2, 3)
Confidence: How confident (%, use 80% if unsure)
Effort: How much work (person-months)
```

**Example:**
```markdown
Feature: In-app notifications

Reach: 1000 users/quarter
Impact: 2 (high impact)
Confidence: 80%
Effort: 1 person-month

RICE = (1000 × 2 × 0.8) / 1 = 1600
```

### 2. Value vs Effort Matrix

```
High Value, Low Effort  → DO FIRST (quick wins)
High Value, High Effort → DO NEXT (strategic)
Low Value, Low Effort   → DO LATER (fill-ins)
Low Value, High Effort  → DON'T DO (money pit)
```

---

## Action Templates

### Template: RICE Scoring

```markdown
# Feature Prioritization

## Feature 1: [Name]
- Reach: [X users/quarter]
- Impact: [0.25/0.5/1/2/3]
- Confidence: [X]%
- Effort: [X person-months]
- **RICE Score:** [calculate]

## Feature 2: [Name]
- Reach: [X users/quarter]
- Impact: [0.25/0.5/1/2/3]
- Confidence: [X]%
- Effort: [X person-months]
- **RICE Score:** [calculate]

## Priority Order
1. [Feature with highest RICE]
2. [Feature with second RICE]
3. [Feature with third RICE]
```

---

## Quick Reference

### 📊 Prioritization Checklist

**Score Each Feature:**
- [ ] Reach (how many users)
- [ ] Impact (how much value)
- [ ] Confidence (how sure)
- [ ] Effort (how much work)

**Prioritize:**
- [ ] Calculate RICE scores
- [ ] Order by score
- [ ] Say no to low scorers

---

## Key Quotes

**Shreyas Doshi:**
> "Saying no is the most underrated PM skill."

**Intercom:**
> "Without prioritization, everything feels urgent and nothing gets done well."

