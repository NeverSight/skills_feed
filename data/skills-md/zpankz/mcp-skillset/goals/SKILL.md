---
name: goals
description: Optimize prompts via process goals (controllable behavioral instructions) rather than outcome goals (sparse end-result demands). Grounded in sports psychology meta-analysis showing process goals (d=1.36) vastly outperform outcome goals (d=0.09). Use when designing prompts, optimizing LLM steering, implementing CoT/decomposition patterns, or building automatic prompt optimization pipelines. Instantiates surrogate loss paradigm for discrete prompt space.
---

# Process Goals in Prompt Optimization

## Core Principle

**Process goals** (controllable intermediate actions) provide **dense feedback signals**; **outcome goals** (end-result demands) provide **sparse, delayed feedback**. This asymmetry explains why behavioral prompting dominates direct output demands.

```
Mechanism: Dense intermediate supervision → stable gradients → reliable optimization
Failure mode: Sparse outcome signal → high variance → reward hacking / hallucination
```

## Goal Typology

| Type | Effect Size | Prompt Analog | Signal Density | Failure Mode |
|------|-------------|---------------|----------------|--------------|
| **Outcome** | d=0.09 | "Give the correct answer" | Sparse | Hallucination, reward hacking |
| **Performance** | d=0.44 | "Achieve high accuracy" | Proxy | Goodhart's Law misalignment |
| **Process** | d=1.36 | "Think step-by-step" | Dense | Over-specification (rare) |

## λ-Instantiations

### Chain-of-Thought (CoT)

```python
# Outcome (weak): "What is 247 × 38?"
# Process (strong):
prompt = """
Solve 247 × 38.
Think step-by-step:
1. Break into partial products
2. Show each multiplication
3. Sum the results
4. State final answer
"""
```

**Mechanism**: Mandates controllable decomposition → self-supervision at each step → error detection before propagation.

**Variants**: Zero-shot CoT ("Let's think step by step"), Auto-CoT (automated exemplar generation), Faithful CoT (enforced structure).

### Decomposition & Sub-Goals

```python
# Tree-of-Thoughts pattern
decompose = """
Generate 3 possible approaches to this problem.
For each approach:
  - State the sub-goals required
  - Identify potential failure points
  - Estimate confidence
Select the approach with highest expected success.
"""

# ReAct pattern
react = """
Thought: [Analyze current state]
Action: [Select tool/operation]
Observation: [Record result]
... repeat until solved ...
"""
```

**Mechanism**: Explicit sub-goal enumeration → local optimization per sub-problem → composition into global solution.

### Auxiliary Tasks

```python
# Direct (weak): "Write a function to sort this list"
# With auxiliary (strong):
aux_prompt = """
Before writing the function:
1. State the input/output types
2. Identify edge cases (empty, single element, duplicates)
3. Choose algorithm and justify complexity
4. Write the function
5. Trace execution on a small example
"""
```

**Mechanism**: Forces deeper processing via intermediate outputs → surfaces implicit assumptions → catches errors early.

### Structured Output Constraints

```python
# Unstructured (weak): "Analyze this data"
# Structured (strong):
structured = """
Analyze the data. Output as:

## Summary Statistics
[numerical summary]

## Key Findings
1. [finding with evidence]
2. [finding with evidence]

## Confidence Assessment
- High confidence: [claims]
- Uncertain: [claims requiring verification]
"""
```

**Mechanism**: Format constraints → consistent reasoning patterns → verifiable outputs.

## Automatic Optimization Paradigm

### Why Process Goals Emerge

```
Search space: discrete prompt tokens
Objective: maximize downstream performance
Challenge: non-differentiable, combinatorial

Solution: Search for PROCESS INSTRUCTIONS
  → Dense intermediate feedback enables gradient estimation
  → Behavioral prompts transfer across tasks
  → Compositional structure reduces search dimensionality
```

### Optimization Methods

| Method | Mechanism | Process Goal Discovery |
|--------|-----------|----------------------|
| **APE** | LLM generates candidates, scores on held-out | Discovers zero-shot CoT variants |
| **OPRO** | Meta-prompt + performance trajectory | Evolves process instructions iteratively |
| **TextGrad** | Gradient through text feedback | Optimizes behavioral descriptions |
| **DEEVO** | Multi-agent debate | Converges on robust process formulations |

### DSPy Integration

```python
import dspy

class ProcessOptimizedModule(dspy.Module):
    """Process goals as learnable signatures."""

    def __init__(self):
        # Process-oriented signatures
        self.decompose = dspy.ChainOfThought("problem -> subgoals, approach")
        self.execute = dspy.ReAct("subgoals, context -> intermediate_results")
        self.synthesize = dspy.Predict("intermediate_results -> final_answer")

    def forward(self, problem):
        # Explicit process steps
        plan = self.decompose(problem=problem)
        results = self.execute(subgoals=plan.subgoals, context=plan.approach)
        return self.synthesize(intermediate_results=results)

# Optimizer learns to refine process instructions
optimizer = dspy.MIPROv2(metric=task_metric, num_threads=4)
optimized = optimizer.compile(ProcessOptimizedModule(), trainset=examples)
```

## Implementation Patterns

### Pattern 1: Process Scaffolding

```python
def scaffold_prompt(task: str, domain: str) -> str:
    """Wrap any task in process scaffolding."""
    return f"""
Task: {task}

Before responding:
1. Identify the key requirements
2. Consider potential approaches
3. Select approach and justify
4. Execute step-by-step
5. Verify output meets requirements

Domain context: {domain}
"""
```

### Pattern 2: Progressive Disclosure

```python
def progressive_process(complexity: int) -> str:
    """Scale process detail to task complexity."""

    if complexity < 2:  # Trivial
        return ""  # No scaffolding needed

    elif complexity < 4:  # Simple
        return "Think through this step by step."

    elif complexity < 8:  # Moderate
        return """
Break this into steps:
1. Understand the problem
2. Plan your approach
3. Execute and verify
"""

    else:  # Complex
        return """
Use systematic analysis:

## Problem Decomposition
- Core requirements:
- Constraints:
- Success criteria:

## Approach Selection
- Option A: [describe] - Pros/Cons
- Option B: [describe] - Pros/Cons
- Selected: [justify]

## Execution Trace
[step-by-step with intermediate validation]

## Verification
- Requirements met: [checklist]
- Confidence: [with justification]
"""
```

### Pattern 3: Self-Critique Integration

```python
critique_process = """
After your initial response:

CRITIQUE:
- What assumptions did I make?
- Where might I be wrong?
- What would a skeptic object to?

REVISION:
- Address each critique
- Strengthen weak points
- Explicitly note remaining uncertainty
"""
```

## Empirical Calibration

| Benchmark | Outcome Prompt | Process Prompt | Δ Relative |
|-----------|---------------|----------------|------------|
| GSM8K | 45% | 68% | +51% |
| Big-Bench Hard | 38% | 57% | +50% |
| MMLU (hard) | 52% | 61% | +17% |
| Coding (HumanEval) | 64% | 78% | +22% |

**Efficiency**: Process prompting often reduces total tokens via early error detection and structured reasoning.

## Risk Mitigation

| Risk | Mechanism | Mitigation |
|------|-----------|------------|
| Over-specification | Rigid process constrains valid alternatives | Use minimal scaffolding for simple tasks |
| Process drift | Steps followed without achieving goal | Include explicit goal-checking at each step |
| Verbosity | Excessive intermediate output | Compress after verification, emit summary |
| False confidence | Structured output mimics rigor | Require explicit uncertainty quantification |

## Integration with Holonic Architecture

```python
# Process goals as λ-transforms in skill composition
process_transform = {
    "ρ.parse": "Decompose input into components",
    "ρ.branch": "Generate alternative approaches",
    "ρ.reduce": "Select optimal path with justification",
    "ρ.ground": "Execute with intermediate verification",
    "ρ.emit": "Synthesize with confidence bounds"
}

# Validation: process goal adherence
def validate_process(response: str, expected_steps: List[str]) -> bool:
    """Verify process scaffolding was followed."""
    return all(
        step_marker in response
        for step_marker in expected_steps
    )
```

## Quick Reference

```
ALWAYS: Behavioral instructions > outcome demands
SCALE: Process detail ∝ task complexity
VERIFY: Include self-check at each process step
OPTIMIZE: Use APE/OPRO to discover domain-specific process formulations

CoT: "Think step by step" → d=1.36 equivalent
Decomposition: Sub-goals + local optimization
Auxiliary: Intermediate outputs force deep processing
Structure: Format constraints enable verification
```
