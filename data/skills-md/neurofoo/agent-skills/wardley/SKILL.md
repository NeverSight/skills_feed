---
name: wardley
description: Wardley Mapping strategic analysis—map value chains against evolution to reveal build vs buy decisions and competitive dynamics. Use for technology strategy or investment decisions.
user-invocable: true
---

# Wardley Map

Create a strategic map showing components positioned by their evolution stage and visibility in the value chain.

## Instructions

Identify the user need, map the value chain of components required to meet it, and position each component on the evolution axis.

### Output Format

**Context**: [What situation we're mapping]
**User**: [Who the user is]
**User Need**: [What they're trying to accomplish]

---

## Value Chain Identification

**Working backward from user need:**

| Component | Depends On | Visibility |
|-----------|------------|------------|
| [User Need] | [what it requires] | High (User-facing) |
| [Component A] | [what it requires] | High/Med/Low |
| [Component B] | [what it requires] | High/Med/Low |
| [Infrastructure] | [base requirements] | Low (Hidden) |

---

## Evolution Assessment

| Component | Evolution Stage | Evidence |
|-----------|-----------------|----------|
| [Component A] | Genesis / Custom / Product / Commodity | [Why at this stage] |
| [Component B] | Genesis / Custom / Product / Commodity | [Why at this stage] |

**Evolution Indicators**:
- Genesis: Novel, poorly understood, no standard, high uncertainty
- Custom: Emerging practices, divergent approaches, experimentation
- Product: Feature differentiation, rental/purchase models, scalable
- Commodity: Standardized, utility pricing, essential but undifferentiated

---

## The Map

```
VISIBLE │
   TO   │  [User Need]
  USER  │       │
        │       ▼
        │  [Component A]
        │       │
        │       ▼
INVISIBLE│  [Component B]
        │
        └──────┬──────┬──────┬──────┬──────►
            GENESIS  CUSTOM PRODUCT COMMODITY
              I        II     III      IV
```

---

## Movement Analysis

**What's evolving rightward?**
| Component | Current Stage | Evolving Toward |
|-----------|---------------|-----------------|
| [component] | [stage] | [next stage] |

**Inertia Points**
- [Component with inertia] — [why we might resist]

---

## Strategic Analysis

### Build vs. Buy

| Component | Recommendation | Rationale |
|-----------|----------------|-----------|
| [Genesis/Custom] | **Build** | Differentiator |
| [Commodity] | **Buy** | Commodity, not differentiating |

### Competitive Dynamics

**Our differentiators** (left side of map):
- [Component we do differently]

**Commoditization threats**:
- [Component becoming commodity]

---

## Recommendations

**Short-term actions**:
1. [Action based on map insights]

**What to stop doing**:
- [Component to outsource/buy instead of build]

---

**Key Insight**:
> [Main strategic takeaway from the mapping exercise]

## Guidelines

- Always start with user need
- Everything evolves left to right (genesis → commodity)
- Build on the left (differentiation), buy on the right (commodity)
- Watch for inertia—past success creates resistance to change

$ARGUMENTS
