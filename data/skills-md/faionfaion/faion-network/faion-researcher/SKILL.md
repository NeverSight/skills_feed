---
name: faion-researcher
description: "Research: idea generation, market research, competitors, personas, pricing, validation."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrate all research and discovery activities for product/startup development. Coordinates 2 specialized sub-skills for comprehensive research coverage.

---

## Architecture

```
faion-researcher (orchestrator)
├── faion-market-researcher (22 methodologies)
│   ├── Market sizing (TAM/SAM/SOM)
│   ├── Competitor analysis
│   ├── Pricing research
│   ├── Trend analysis
│   ├── Niche evaluation
│   ├── Business model planning
│   └── Idea generation
└── faion-user-researcher (21 methodologies)
    ├── Persona building
    ├── User interviews
    ├── Pain point research
    ├── Jobs-to-be-done
    ├── Problem validation
    ├── Value proposition design
    └── Survey design
```

**Total:** 43 methodologies across 2 sub-skills

---

## Quick Decision Tree

| If you need... | Route to Sub-Skill |
|---------------|-------------------|
| **Market Intelligence** | |
| Market size (TAM/SAM/SOM) | faion-market-researcher |
| Competitors & gaps | faion-market-researcher |
| Pricing benchmarks | faion-market-researcher |
| Market trends | faion-market-researcher |
| Niche evaluation | faion-market-researcher |
| Business models | faion-market-researcher |
| Generate ideas | faion-market-researcher |
| **User Understanding** | |
| User profiles | faion-user-researcher |
| Pain points | faion-user-researcher |
| User motivations (JTBD) | faion-user-researcher |
| Value proposition | faion-user-researcher |
| Interview questions | faion-user-researcher |
| Problem validation | faion-user-researcher |
| Survey design | faion-user-researcher |
| **Full Research** | |
| Complete product research | Both (sequential) |

---

## Sub-Skills (2)

### faion-market-researcher

**Focus:** Market & business intelligence

| Capability | Methodologies |
|------------|---------------|
| Market Analysis | TAM/SAM/SOM, market sizing, trends |
| Competitive Intel | Competitor analysis, competitive intelligence |
| Business Planning | Models, niche eval, risk, distribution |
| Pricing | Research, benchmarking |
| Ideas | Generation, frameworks |

**Files:** 22 | **Location:** [faion-market-researcher/](../faion-market-researcher/)

### faion-user-researcher

**Focus:** User research & validation

| Capability | Methodologies |
|------------|---------------|
| Personas | Building, segmentation, AI-assisted |
| Interviews | Methods, analysis, at-scale |
| Pain Points | Research, validation |
| JTBD | Framework, motivations |
| Validation | Methods, problem-solution fit |
| Value Prop | Design, canvas |

**Files:** 21 | **Location:** [faion-user-researcher/](../faion-user-researcher/)

---

## Agents (2)

| Agent | Model | Purpose | Modes |
|-------|-------|---------|-------|
| faion-research-agent | opus | Research orchestrator | ideas, market, competitors, pains, personas, validate, niche, pricing, names |
| faion-domain-checker-agent | sonnet | Domain availability verification | - |

**Details:** [agent-invocation.md](agent-invocation.md)

---

## Research Modes (9)

| Mode | Output | Sub-Skill Used |
|------|--------|----------------|
| ideas | idea-candidates.md | market-researcher |
| market | market-research.md | market-researcher |
| competitors | competitive-analysis.md | market-researcher |
| pricing | pricing-research.md | market-researcher |
| niche | niche-evaluation.md | market-researcher |
| personas | user-personas.md | user-researcher |
| pains | pain-points.md | user-researcher |
| validate | problem-validation.md | user-researcher |
| names | name-candidates.md | market-researcher |

---

## Core Workflows

### 1. Idea Discovery
```
Context → Generate Ideas → Select → Pain Research → Niche Eval → Results
Sub-skills: market-researcher (ideas, niche) + user-researcher (pains)
```

### 2. Product Research
```
Parse Project → Read Docs → Select Modules → Sequential Execution → Summary
Sub-skills: market-researcher (market, competitors, pricing) + user-researcher (personas, validate)
```

### 3. Project Naming
```
Gather Concept → Generate Names → Select → Check Domains → Results
Sub-skill: market-researcher (naming)
```

**Details:** [workflows.md](workflows.md)

---

## Quick Reference

| Topic | File | Description |
|-------|------|-------------|
| **Navigation** | [CLAUDE.md](CLAUDE.md) | Entry point, when to use |
| **Agents** | [agent-invocation.md](agent-invocation.md) | Agent syntax, modes |
| **Workflows** | [workflows.md](workflows.md) | Research workflows |
| **Frameworks** | [frameworks.md](frameworks.md) | 7 Ps, JTBD, TAM/SAM/SOM |
| **Methodologies** | [methodologies-index.md](methodologies-index.md) | Full index |

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File | Sub-Skill |
|--------|-------------|-----------|
| Idea Discovery | idea-validation.md | market-researcher |
| Market Research | market-research.md | market-researcher |
| Competitors | competitive-analysis.md | market-researcher |
| Pricing | pricing-research.md | market-researcher |
| Niche | niche-evaluation.md | market-researcher |
| Personas | user-personas.md | user-researcher |
| Pain Points | pain-points.md | user-researcher |
| Validation | problem-validation.md | user-researcher |
| Summary | executive-summary.md | Both |

---

## Integration

### Entry Point
Invoked via `/faion-net` when intent is research-related:
```
if intent in ["idea", "research", "market", "competitors", "naming", "personas", "pricing"]:
    invoke("faion-researcher")
```

### Sub-Skill Invocation
```
# Market intelligence
invoke("faion-market-researcher", mode="market")

# User research
invoke("faion-user-researcher", mode="personas")

# Full research (sequential)
invoke("faion-market-researcher", mode="market")
invoke("faion-market-researcher", mode="competitors")
invoke("faion-user-researcher", mode="personas")
invoke("faion-user-researcher", mode="validate")
```

### Next Steps
After research complete, offer:
- "Create GTM Manifest?" → `faion-marketing-manager`
- "Create spec.md?" → `faion-sdd`
- "Start development?" → `faion-software-developer`

---

## Rules

1. **Sequential execution** - Run agents ONE BY ONE (not parallel)
2. **Sub-skill routing** - Market topics → market-researcher, User topics → user-researcher
3. **Source citations** - All research must include URLs
4. **Data quality** - If not found → "Data not available"

---

*faion-researcher v2.0*
*Orchestrator with 2 sub-skills*
*Total: 43 methodologies | Agents: 2 | Modes: 9*
