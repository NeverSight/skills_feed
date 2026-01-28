---
name: triz
description: |
  TRIZ systematic innovation methodology with AI-enhanced prompts. Use when: (1) Technical contradiction - improve A but B worsens, (2) Physical contradiction - need opposite properties, (3) Cross-industry solutions via FOS/MOS, (4) Technology evolution prediction, (5) Complex engineering problems. Triggers: "TRIZ", "contradiction", "inventive", "trade-off", "improve without worsening", "ข้อขัดแย้งทางเทคนิค", "innovation breakthrough"
---

# TRIZ Skill

Systematic innovation via Theory of Inventive Problem Solving. AI-enhanced.

## Problem Routing

| Problem Type | Tool | Reference |
|-------------|------|-----------|
| "Improve A but B worsens" | Contradiction Matrix | [40-principles.md](references/40-principles.md) |
| "Need opposite properties" | Separation Principles | Below |
| "System not working" | Su-Field Analysis | [advanced.md](references/advanced.md) |
| "How will tech evolve?" | Evolution Trends | [advanced.md](references/advanced.md) |
| "What do others do?" | FOS (cross-industry) | [ai-prompts.md](references/ai-prompts.md) |
| "Very complex problem" | ARIZ Algorithm | [ai-prompts.md](references/ai-prompts.md) |

## 6-Step Process

```
1. DEFINE IFR    → "The [system] ITSELF [does X] WITHOUT [cost/harm]"
2. IDENTIFY      → What contradiction? (Technical or Physical)
3. MAP           → Which of 39 parameters? [39-parameters.md]
4. RETRIEVE      → Matrix suggests which principles?
5. GENERATE      → Apply each principle specifically
6. EVALUATE      → Feasibility? Implementation?
```

## Step 1: Ideal Final Result (IFR)

> **"The [object] ITSELF [performs function] WITHOUT [cost/harm/complexity]"**

Formula: `Ideality = Benefits / (Cost + Harm)`

Examples:
- "The pipe itself prevents leaks" (not: add sensors)
- "The code itself fixes bugs" (not: add more tests)

## Step 2: Identify Contradiction

**Technical:** Improving A worsens B
```
"If we [improve A], then [B gets worse]"
→ ถ้าเราทำให้รถเร็วขึ้น, ประสิทธิภาพน้ำมันแย่ลง
```

**Physical:** Same element needs opposite properties
```
"[Element] must be [Property] for X AND [Opposite] for Y"
→ API ต้อง complex (power users) AND simple (beginners)
```

## Step 3: Map to 39 Parameters

See [39-parameters.md](references/39-parameters.md). Common ones:

| # | Parameter | Software Equivalent |
|---|-----------|---------------------|
| 9 | Speed | Performance, latency |
| 27 | Reliability | Uptime, MTBF |
| 33 | Ease of operation | UX, usability |
| 36 | Complexity | Code complexity |
| 39 | Productivity | Throughput |

## Step 4: Top 10 Principles

| # | Principle | Modern Example |
|---|-----------|----------------|
| 1 | Segmentation | Microservices |
| 2 | Taking Out | Separation of concerns |
| 10 | Preliminary Action | Caching |
| 13 | The Other Way Round | Event-driven vs polling |
| 15 | Dynamics | Adaptive algorithms |
| 24 | Intermediary | Middleware, adapters |
| 25 | Self-Service | Self-healing systems |
| 35 | Parameter Changes | Transform data format |

Full list: [40-principles.md](references/40-principles.md)

## Step 5: Physical Contradiction → Separation

| Separation | Strategy | Example |
|------------|----------|---------|
| **In Time** | Different times | Landing gear: extend/retract |
| **In Space** | Different locations | Pencil: hard core, soft eraser |
| **In Condition** | Different conditions | Smart glass: transparent/opaque |
| **In Scale** | Different levels | Water: liquid macro, molecules nano |

## Creative Mode: FOS/MOS

**Function Oriented Search (FOS):** Find how OTHER industries solve same function.

```
1. ABSTRACT → "Remove ice" → "Separate materials"
2. SEARCH → Find 5+ industries with similar function
3. TRANSFER → Adapt mechanism to your problem
```

**Method Oriented Search (MOS):** Apply known method to NEW domains.

See [ai-prompts.md](references/ai-prompts.md) for detailed prompts.

## Output Format

```markdown
## Problem: [Restated]

## IFR: "The [system] itself [does X] without [cost/harm]"

## Contradiction:
- Type: Technical / Physical
- Improving: Parameter #__
- Worsening: Parameter #__

## Principles: [#, #, #]

## Solutions:
### Principle #X: [Name]
- Application: [How]
- Idea: [Concrete solution]
- Feasibility: High/Medium/Low

## Next Steps:
1. [Prototype which solution]
2. [Validation approach]
```

## References

| Type | File | Content |
|------|------|---------|
| Core | [40-principles.md](references/40-principles.md) | All 40 principles + examples |
| Core | [39-parameters.md](references/39-parameters.md) | All 39 parameters |
| Advanced | [advanced.md](references/advanced.md) | Su-Field, 76 Standards, ARIZ, Evolution |
| AI | [ai-prompts.md](references/ai-prompts.md) | Ready-to-use prompt templates |
| AI | [methodology.md](references/methodology.md) | TRIZ + LLM integration |
| Examples | [examples.md](references/examples.md) | Case studies (Samsung, SpaceX, Netflix) |

## Related Skills (Optional)

| When | Suggest |
|------|---------|
| Problem not yet defined clearly | `/problem-solving` - ช่วย clarify ก่อน |
| Need more creative options | `/generate-creative-ideas` - divergent thinking |
| Business strategy context | `/manage-business-strategy` - SWOT, Porter's |
| Designing new business model | `/design-business-model` - BMC, Lean Canvas |

**Note:** These skills are optional. TRIZ works standalone for contradiction problems.
