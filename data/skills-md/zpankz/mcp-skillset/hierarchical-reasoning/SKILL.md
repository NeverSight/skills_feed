---
name: hierarchical-reasoning
description: Implements sophisticated multi-level reasoning for complex problems requiring strategic planning, tactical approach design, and operational execution. Use for problems needing deep analysis, multi-step reasoning, systematic decomposition from first principles to implementation, convergence-aware iterative refinement, or uncertainty quantification across abstraction levels.
---

# Hierarchical Reasoning

Execute sophisticated reasoning through a three-level cognitive architecture that mirrors human multi-timescale processing: strategic (abstract planning), tactical (approach design), and operational (detailed execution).

## Core Principle

**Separate concerns by abstraction level while maintaining bidirectional information flow:**
- Strategic level formulates problems and sets goals (slow, abstract)
- Tactical level designs approaches and selects methods (medium, structured)  
- Operational level performs detailed computations (fast, concrete)

Each level informs the others through iterative refinement until convergence.

## When to Use

Apply hierarchical reasoning for:

1. **Complex multi-step problems** requiring systematic decomposition
2. **Strategic questions** needing both big-picture framing and detailed analysis
3. **Design challenges** bridging abstract requirements to concrete implementation
4. **Reasoning under uncertainty** where confidence tracking matters
5. **Deep analysis** requiring multiple passes of refinement
6. **First principles thinking** building from fundamentals to emergent systems

Do NOT use for:
- Simple factual lookups
- Single-step calculations
- Purely creative tasks without logical structure
- Real-time processing requirements

## Usage Pattern

### 1. Problem Structuring

Frame the problem with clarity:
```
Problem: [Clear statement of what needs to be reasoned about]
Context: [Relevant background, constraints, domain knowledge]
Success Criteria: [How to evaluate reasoning quality]
```

### 2. Execute Hierarchical Reasoning

Use the reasoning script:
```bash
python scripts/hierarchical_reasoner.py "<problem>" --context '<json_context>'
```

Or invoke programmatically:
```python
from hierarchical_reasoner import HierarchicalReasoner

reasoner = HierarchicalReasoner(
    max_strategic_cycles=3,
    max_tactical_cycles=5, 
    max_operational_cycles=7,
    convergence_threshold=0.95,
    uncertainty_threshold=0.1
)

result = reasoner.reason(problem, context)
```

### 3. Interpret Results

Examine multi-level outputs:
- **Strategic state**: Problem formulation, goals, high-level insights
- **Tactical state**: Approaches, methods, reasoning strategies
- **Operational state**: Detailed analysis, computations, evidence
- **Convergence metrics**: State stability and confidence at each level
- **Final synthesis**: Integrated conclusion across all levels

### 4. Iterate Based on Convergence

If not converged (convergence_score < threshold):
- Review which level has low convergence
- Add relevant context or constraints
- Increase cycle count for that level
- Re-run with refined inputs

## Reasoning Flow

```
┌─────────────────────────────────────────────┐
│ STRATEGIC LEVEL (Abstract Planning)         │
│ • Problem formulation                       │
│ • Goal identification                       │
│ • Success criteria                          │
└────────────┬────────────────────────────────┘
             │ guides ↓    ↑ informs
┌────────────▼────────────────────────────────┐
│ TACTICAL LEVEL (Approach Design)            │
│ • Method selection                          │
│ • Decomposition strategy                    │
│ • Reasoning structure                       │
└────────────┬────────────────────────────────┘
             │ guides ↓    ↑ informs
┌────────────▼────────────────────────────────┐
│ OPERATIONAL LEVEL (Detailed Execution)      │
│ • Concrete computations                     │
│ • Evidence gathering                        │
│ • Detailed analysis                         │
└─────────────────────────────────────────────┘
```

## Convergence Detection

Reasoning converges when:
1. State content stabilizes across iterations (high similarity)
2. Confidence increases above threshold (typically 0.90-0.95)
3. Uncertainty decreases below threshold (typically 0.10-0.15)

**Convergence Score Formula:**
```
score = 0.7 × similarity(current, previous) + 0.3 × confidence
```

**Multi-level convergence:**
```
converged = all levels > threshold OR weighted_average > threshold
weighted_avg = 0.5×strategic + 0.3×tactical + 0.2×operational
```

## Configuration Parameters

**Cycle Counts** (iterations per level):
- `max_strategic_cycles`: 2-5 (typically 3)
- `max_tactical_cycles`: 3-7 (typically 5)
- `max_operational_cycles`: 5-10 (typically 7)

Higher values allow more refinement but increase computation.

**Thresholds**:
- `convergence_threshold`: 0.90-0.98 (default 0.95)
- `uncertainty_threshold`: 0.05-0.20 (default 0.10)

Higher convergence thresholds require more stable reasoning.

## Example: Complex Problem Analysis

**Problem:** "Design a sustainable urban transportation system"

**Strategic Output:**
```
- Goal: Minimize environmental impact while maximizing accessibility
- Constraints: Budget, existing infrastructure, citizen adoption
- Success metrics: Emissions reduction, ridership, cost-effectiveness
```

**Tactical Output:**
```
- Approach: Multi-modal integration (public transit + micro-mobility)
- Method: Network optimization with accessibility mapping
- Validation: Simulation before implementation
```

**Operational Output:**
```
- Route optimization calculations
- Demand forecasting analysis
- Cost-benefit quantification
- Environmental impact assessment
```

**Synthesis:** Integrated design bridging strategic goals through tactical approaches to operational specifications, with confidence metrics for each component.

## Advanced Features

### Uncertainty Quantification

Each state tracks:
- **Confidence**: Self-assessed certainty (0.0 to 1.0)
- **Uncertainty**: Recognized unknowns and ambiguities
- **Convergence**: State stability over iterations

Use these for:
- Identifying areas needing more analysis
- Selective trust in conclusions
- Metacognitive awareness of reasoning quality

### Reasoning Trace

Enable full diagnostic trace:
```bash
python scripts/hierarchical_reasoner.py "<problem>" --trace
```

Outputs:
- State evolution at each cycle
- Convergence progression
- Confidence/uncertainty dynamics
- Dependency tracking

Useful for:
- Debugging reasoning failures
- Understanding convergence patterns
- Analyzing computational efficiency

## Architecture Details

For deep technical understanding of:
- Theoretical foundations
- Cognitive architecture alignment
- Implementation patterns
- Scaling properties
- Future enhancements

See: [references/architecture.md](references/architecture.md)

## Integration with Other Tools

Hierarchical reasoning complements:
- **Web search**: Operational level can gather facts
- **Code execution**: Operational level performs calculations
- **Knowledge graphs**: Strategic level structures problem space
- **Document analysis**: Tactical level designs analysis approach

Combine reasoning levels with appropriate tools at each abstraction.

## Troubleshooting

**Low convergence scores:**
- Increase cycle count for non-converging level
- Refine problem statement clarity
- Add relevant context to reduce uncertainty
- Check if problem requires more/fewer abstraction levels

**High computational cost:**
- Decrease cycle counts
- Increase convergence threshold (accept earlier stopping)
- Use adaptive early stopping
- Parallelize level updates (future enhancement)

**Inconsistent multi-level outputs:**
- Review information flow (are levels properly informing each other?)
- Check if strategic goals are well-defined
- Verify tactical approaches align with strategy
- Ensure operational details serve tactical plan
