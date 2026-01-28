---
name: maker-framework
description: Orchestrate reliable multi-agent reasoning using MAKER (Maximal Agentic Knowledge Engine for Reasoning). Implements three-pillar architecture for transforming probabilistic LLM outputs into deterministic, verifiable results. Use when tasks require high reliability, parallel consensus voting, or systematic error detection. Triggers include reliability-critical tasks, multi-step reasoning chains, consensus-based verification, parallel agent execution, or explicit MAKER invocation.
---

# MAKER Framework Skill

Transform unreliable single-model inference into robust, verifiable reasoning through maximal decomposition, parallel consensus voting, and systematic error filtering.

## When to Use MAKER

**High-value triggers:**
- Tasks requiring >90% accuracy (medical, legal, financial)
- Multi-step reasoning where errors compound (p^n problem)
- Verification-critical outputs (code, calculations, facts)
- Ambiguous tasks benefiting from diverse perspectives

**Skip MAKER for:**
- Single-fact retrieval (no decomposition benefit)
- Creative tasks where diversity is desirable
- Time-critical responses (voting adds latency)

## Core Architecture

MAKER operates on three pillars applied sequentially:

```
Task → [Pillar 1: Decompose] → DAG of subtasks
     → [Pillar 2: Vote]      → Parallel execution + consensus
     → [Pillar 3: Filter]    → Red-flag invalid outputs
     → Validated Result
```

### Pillar 1: Maximal Agentic Decomposition (MAD)

Decompose complex tasks into atomic, independently-executable subtasks forming a DAG.

**Decomposition principles:**
- Each subtask has single, well-defined objective
- Subtasks receive explicit input/output schemas
- Dependencies form acyclic graph (no cycles)
- Maximize width (parallelism) over depth (sequential)

**Tool:** `maker_build_dag`

### Pillar 2: First-to-Ahead-by-k Voting

Execute each subtask with m parallel agents; accept when one result leads by k votes.

**Configuration by criticality:**
| Level    | m  | k | Confidence |
|----------|----|----|------------|
| low      | 3  | 1  | ~70%       |
| medium   | 5  | 2  | ~85%       |
| high     | 7  | 3  | ~95%       |
| critical | 11 | 5  | ~99%       |

**Tool:** `maker_vote`, `maker_get_config`

### Pillar 3: Red-Flagging System

Discard outputs exhibiting error indicators before voting.

**Red flag types:**
- Length exceeded (verbose = uncertain)
- Format violation (schema mismatch)
- Placeholder detected ([TODO], [N/A])
- Uncertainty markers ("possibly", "might be")

**Tool:** `maker_red_flag`

## Workflow

### Standard MAKER Pipeline

```
1. Decompose task → maker_build_dag
2. For each subtask in topological order:
   a. Generate prompts → maker_generate_prompt (×m)
   b. Execute agents (parallel LLM calls)
   c. Validate outputs → maker_red_flag (each)
   d. Vote on valid outputs → maker_vote
3. Compose results → maker_compose_results
```

### Example: Multi-Hop QA

Task: "What is the capital of the country where the inventor of the telephone was born?"

**Step 1: Decompose**
```json
{
  "subtasks": [
    {"id": "t1", "description": "Identify inventor of telephone", "dependencies": []},
    {"id": "t2", "description": "Determine birthplace of {t1}", "dependencies": ["t1"]},
    {"id": "t3", "description": "Identify capital of {t2}", "dependencies": ["t2"]}
  ]
}
```

**Step 2: Execute with voting (m=5, k=2 for medium criticality)**

t1 outputs: ["Alexander Graham Bell", "Alexander Graham Bell", "A.G. Bell", "Alexander Graham Bell", "Bell"]
→ Normalize → "alexander graham bell" wins with 4 votes

t2 (with input "Alexander Graham Bell"):
→ "Edinburgh, Scotland" wins after red-flagging one verbose response

t3 (with input "Scotland"):
→ "Edinburgh" wins unanimously

**Step 3: Compose**
Final answer: "Edinburgh"

## Integration with Reasoning Skills

### With hierarchical-reasoning

MAKER complements hierarchical-reasoning by adding reliability to each reasoning level:

```
Strategic level → MAKER(criticality=high) for key decisions
Tactical level  → MAKER(criticality=medium) for approach validation
Operational     → Direct execution for atomic operations
```

### With knowledge-graph

Use MAKER voting on entity extraction to achieve higher-quality knowledge graphs:

```
Document → [MAKER: Extract entities (m=5)] → Validated entities
        → [MAKER: Extract relations (m=5)] → Validated relations
        → knowledge-graph merge
```

## Tool Reference

### maker_build_dag
Construct DAG from subtask definitions. Validates acyclicity and computes execution order.

### maker_red_flag  
Apply red-flag validation to agent output. Returns is_valid boolean and flag details.

### maker_vote
Execute first-to-ahead-by-k voting. Returns consensus output with confidence score.

### maker_compute_reliability
Calculate theoretical system reliability for given (m, k, n) configuration.

### maker_get_config
Get recommended (m, k) configuration for criticality level.

### maker_compose_results
Combine validated subtask outputs into final result.

### maker_generate_prompt
Create optimized micro-agent prompt with constraints and schema.

## Configuration Guide

### Selecting m and k

**Cost-accuracy tradeoff:**
- Higher m → more reliable but costlier
- Higher k → stronger consensus but slower termination
- Early termination typically reduces cost by 30-50%

**Decision framework:**
1. Start with criticality-based defaults via `maker_get_config`
2. Use `maker_compute_reliability` to validate configuration
3. Adjust based on empirical accuracy and cost metrics

### Output Schema Design

Well-designed schemas enable format-based red-flagging:

```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "required": ["answer"]
}
```

### Equivalence Methods

- `exact`: String equality after trim (dates, numbers)
- `normalized`: Lowercase + whitespace normalization (text)
- `json`: Parse and re-serialize for canonical comparison (structured)

## Performance Characteristics

**Reliability improvement (assuming 85% agent accuracy):**
| Steps | Single Agent | MAKER (m=5, k=2) |
|-------|-------------|------------------|
| 1     | 85.0%       | 97.1%            |
| 3     | 61.4%       | 91.5%            |
| 5     | 44.4%       | 86.2%            |

**Cost multiplier:** ~4-6× single agent (with early termination)

**Latency:** ~2-4× single agent (parallelism offsets voting overhead)

## Error Handling

**Insufficient valid outputs (red-flagging too aggressive):**
1. Retry with additional agents
2. Relax red-flag thresholds
3. Refine subtask prompt

**No consensus (high disagreement):**
1. Further decompose the problematic subtask
2. Increase k threshold
3. Escalate to human review

**Cycle detected in DAG:**
1. Review dependency structure
2. Break circular dependencies into sequential steps
