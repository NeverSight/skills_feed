---
name: design-business-model
description: Business model design and validation using Business Model Canvas, Lean Canvas, and Value Proposition Canvas. Use when designing new business models, validating startup ideas, achieving product-market fit, or innovating existing business models.
---

# Business Model Frameworks

Design, visualize, and validate business models.

## Quick Start

1. **Choose framework** - Based on your situation
2. **Fill canvas** - Use structured approach below
3. **Validate** - Test assumptions with customers
4. **Iterate** - Refine based on learning

## Framework Selection

| Situation | Use This |
|-----------|----------|
| **Existing business** - understand or optimize current model | Business Model Canvas |
| **Startup/New idea** - validate quickly, test assumptions | Lean Canvas |
| **Product-market fit** - ensure value matches customer needs | Value Proposition Canvas |
| **Innovation** - transform existing business | Business Model Canvas + Blue Ocean |

## The Three Canvases

### 1. Business Model Canvas (BMC)

For established businesses or comprehensive business design.

[Full details: references/business-model-canvas.md](references/business-model-canvas.md)

```
┌─────────────┬────────────┬────────────┬────────────┬─────────────┐
│             │            │            │            │             │
│    Key      │    Key     │   Value    │  Customer  │   Customer  │
│  Partners   │ Activities │Proposition │Relationships│  Segments   │
│             │            │            │            │             │
│             ├────────────┤            ├────────────┤             │
│             │            │            │            │             │
│             │    Key     │            │  Channels  │             │
│             │ Resources  │            │            │             │
│             │            │            │            │             │
├─────────────┴────────────┴────────────┴────────────┴─────────────┤
│                          │                                        │
│       Cost Structure     │              Revenue Streams           │
│                          │                                        │
└──────────────────────────┴────────────────────────────────────────┘
```

### 2. Lean Canvas

For startups and new ventures - focus on problem/solution fit.

[Full details: references/lean-canvas.md](references/lean-canvas.md)

```
┌─────────────┬────────────┬────────────┬────────────┬─────────────┐
│             │            │            │            │             │
│   Problem   │  Solution  │  Unique    │   Unfair   │  Customer   │
│   (Top 3)   │  (Top 3)   │   Value    │  Advantage │  Segments   │
│             │            │Proposition │            │             │
│             ├────────────┤            ├────────────┤             │
│             │            │            │            │             │
│             │    Key     │            │  Channels  │             │
│             │  Metrics   │            │            │             │
│             │            │            │            │             │
├─────────────┴────────────┴────────────┴────────────┴─────────────┤
│                          │                                        │
│       Cost Structure     │              Revenue Streams           │
│                          │                                        │
└──────────────────────────┴────────────────────────────────────────┘
```

### 3. Value Proposition Canvas (VPC)

Zoom into Customer Segments + Value Proposition from BMC.

[Full details: references/value-proposition-canvas.md](references/value-proposition-canvas.md)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   VALUE MAP                         CUSTOMER PROFILE            │
│   ┌─────────────┐                   ┌─────────────┐            │
│   │   Products  │                   │    Gains    │            │
│   │  & Services │                   │             │            │
│   ├─────────────┤     FIT?          ├─────────────┤            │
│   │    Gain     │ ◄──────────────►  │    Jobs     │            │
│   │  Creators   │                   │  (To Be Done)│            │
│   ├─────────────┤                   ├─────────────┤            │
│   │    Pain     │                   │    Pains    │            │
│   │  Relievers  │                   │             │            │
│   └─────────────┘                   └─────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Canvas Comparison

| Aspect | Business Model Canvas | Lean Canvas | Value Proposition Canvas |
|--------|----------------------|-------------|-------------------------|
| **Creator** | Osterwalder & Pigneur | Ash Maurya | Osterwalder |
| **Focus** | Comprehensive business model | Problem-solution validation | Product-market fit |
| **Best for** | Established business | Startups, new ideas | Deep customer understanding |
| **Unique blocks** | Partners, Relationships | Problem, Unfair Advantage | Gains, Pains, Jobs |
| **Time to fill** | 1-2 hours | 20-30 minutes | 30-60 minutes |

## Workflow Recommendation

### For New Business Idea

```
1. Lean Canvas (20 min)
   ↓
2. Value Proposition Canvas (for top segment)
   ↓
3. Customer interviews (validate)
   ↓
4. Iterate Lean Canvas
   ↓
5. Business Model Canvas (when scaling)
```

### For Existing Business Innovation

```
1. Business Model Canvas (current state)
   ↓
2. Value Proposition Canvas (problem areas)
   ↓
3. Lean Canvas (for new initiatives)
   ↓
4. Business Model Canvas (future state)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with solution | Start with customer problems |
| One customer segment | Be specific, narrow first |
| Vague value proposition | Use customer's words |
| Untested assumptions | Validate with real customers |
| Static canvas | Update regularly |
| Working alone | Collaborate, get diverse input |

## Output Template

When presenting canvas analysis:

```markdown
## Business Model: [Name]

### Canvas Type: [BMC/Lean/VPC]

### Key Insights
1. [Most important finding]
2. [Second insight]
3. [Third insight]

### Riskiest Assumptions
1. [Assumption that could kill the business]
2. [Second risky assumption]

### Next Steps to Validate
- [ ] [Experiment 1]
- [ ] [Experiment 2]
- [ ] [Customer interview focus]
```

## Related Skills (Optional)

| When | Suggest |
|------|---------|
| Need strategic analysis (SWOT, Porter's) | `/manage-business-strategy` |
| Stuck, need structured thinking | `/problem-solving` - Polya, 5 Whys |
| Innovation breakthrough needed | `/triz` - contradiction solving |
| Need creative ideas for value prop | `/generate-creative-ideas` - divergent thinking |

**Note:** These skills are optional. Design-business-model works standalone for canvas design.
