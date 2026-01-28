---
name: Rapid Convergence
description: Achieve 3-4 iteration methodology convergence (vs standard 5-7) when clear baseline metrics exist, domain scope is focused, and direct validation is possible. Use when you have V_meta baseline ≥0.40, quantifiable success criteria, retrospective validation data, and generic agents are sufficient. Enables 40-60% time reduction (10-15 hours vs 20-30 hours) without sacrificing quality. Prediction model helps estimate iteration count during experiment planning. Validated in error recovery (3 iterations, 10 hours, V_instance=0.83, V_meta=0.85).
allowed-tools: Read, Grep, Glob
---

# Rapid Convergence

**Achieve methodology convergence in 3-4 iterations through structural optimization, not rushing.**

> Rapid convergence is not about moving fast - it's about recognizing when structural factors naturally enable faster progress without sacrificing quality.

---

## When to Use This Skill

Use this skill when:
- 🎯 **Planning new experiment**: Want to estimate iteration count and timeline
- 📊 **Clear baseline exists**: Can quantify current state with V_meta(s₀) ≥ 0.40
- 🔍 **Focused domain**: Can describe scope in <3 sentences without ambiguity
- ✅ **Direct validation**: Can validate with historical data or single context
- ⚡ **Time constraints**: Need methodology in 10-15 hours vs 20-30 hours
- 🧩 **Generic agents sufficient**: No complex specialization needed

**Don't use when**:
- ❌ Exploratory research (no established metrics)
- ❌ Multi-context validation required (cross-language, cross-domain testing)
- ❌ Complex specialization needed (>10x speedup from specialists)
- ❌ Incremental pattern discovery (patterns emerge gradually, not upfront)

---

## Quick Start (5 minutes)

### Rapid Convergence Self-Assessment

Answer these 5 questions:

1. **Baseline metrics exist**: Can you quantify current state objectively? (YES/NO)
2. **Domain is focused**: Can you describe scope in <3 sentences? (YES/NO)
3. **Validation is direct**: Can you validate without multi-context deployment? (YES/NO)
4. **Prior art exists**: Are there established practices to reference? (YES/NO)
5. **Success criteria clear**: Do you know what "done" looks like? (YES/NO)

**Scoring**:
- **4-5 YES**: ⚡ Rapid convergence (3-4 iterations) likely
- **2-3 YES**: 📊 Standard convergence (5-7 iterations) expected
- **0-1 YES**: 🔬 Exploratory (6-10 iterations), establish baseline first

---

## Five Rapid Convergence Criteria

### Criterion 1: Clear Baseline Metrics (CRITICAL)

**Indicator**: V_meta(s₀) ≥ 0.40

**What it means**:
- Domain has established metrics (error rate, test coverage, build time)
- Baseline can be measured objectively in iteration 0
- Success criteria can be quantified before starting

**Example (Bootstrap-003)**:
```
✅ Clear baseline:
- 1,336 errors quantified via MCP queries
- 5.78% error rate calculated
- Clear MTTD/MTTR targets
- Result: V_meta(s₀) = 0.48

Outcome: 3 iterations, 10 hours
```

**Counter-example (Bootstrap-002)**:
```
❌ No baseline:
- No existing test coverage data
- Had to establish metrics first
- Fuzzy success criteria initially
- Result: V_meta(s₀) = 0.04

Outcome: 6 iterations, 25.5 hours
```

**Impact**: High V_meta baseline means:
- Fewer iterations to reach 0.80 threshold (+0.40 vs +0.76)
- Clearer iteration objectives (gaps are obvious)
- Faster validation (metrics already exist)

See [reference/baseline-metrics.md](reference/baseline-metrics.md) for achieving V_meta ≥ 0.40.

### Criterion 2: Focused Domain Scope (IMPORTANT)

**Indicator**: Domain described in <3 sentences without ambiguity

**What it means**:
- Single cross-cutting concern
- Clear boundaries (what's in vs out of scope)
- Well-established practices (prior art)

**Examples**:
```
✅ Focused (Bootstrap-003):
"Reduce error rate through detection, diagnosis, recovery, prevention"

❌ Broad (Bootstrap-002):
"Develop test strategy" (requires scoping: what tests? which patterns? how much coverage?)
```

**Impact**: Focused scope means:
- Less exploration needed
- Clearer convergence criteria
- Lower risk of scope creep

### Criterion 3: Direct Validation (IMPORTANT)

**Indicator**: Can validate without multi-context deployment

**What it means**:
- Retrospective validation possible (use historical data)
- Single-context validation sufficient
- Proxy metrics strongly correlate with value

**Examples**:
```
✅ Direct (Bootstrap-003):
Retrospective validation via 1,336 historical errors
No deployment needed
Confidence: 0.79

❌ Indirect (Bootstrap-002):
Multi-context validation required (3 project archetypes)
Deploy and test in each context
Adds 2-3 iterations
```

**Impact**: Direct validation means:
- Faster iteration cycles
- Less complexity
- Easier V_meta calculation

See [../retrospective-validation](../retrospective-validation/SKILL.md) for retrospective validation technique.

### Criterion 4: Generic Agent Sufficiency (MODERATE)

**Indicator**: Generic agents (data-analyst, doc-writer, coder) sufficient

**What it means**:
- No specialized domain knowledge required
- Tasks are analysis + documentation + simple automation
- Pattern extraction is straightforward

**Examples**:
```
✅ Generic sufficient (Bootstrap-003):
Generic agents analyzed errors, documented taxonomy, created scripts
No specialization overhead
3 iterations

⚠️ Specialization needed (Bootstrap-002):
coverage-analyzer (10x speedup)
test-generator (200x speedup)
6 iterations (specialization added 1-2 iterations)
```

**Impact**: No specialization means:
- No iteration delay for agent design
- Simpler coordination
- Faster execution

### Criterion 5: Early High-Impact Automation (MODERATE)

**Indicator**: Top 3 automation opportunities identified by iteration 1

**What it means**:
- Pareto principle applies (20% patterns → 80% impact)
- High-frequency, high-impact patterns obvious
- Automation feasibility clear (no R&D risk)

**Examples**:
```
✅ Early identification (Bootstrap-003):
3 tools preventing 23.7% of errors identified in iteration 0-1
Clear automation path
Rapid V_instance improvement

⚠️ Gradual discovery (Bootstrap-002):
8 test patterns emerged gradually over 6 iterations
Pattern library built incrementally
```

**Impact**: Early automation means:
- Faster V_instance improvement
- Clearer path to convergence
- Less trial-and-error

---

## Convergence Speed Prediction Model

### Formula

```
Predicted Iterations = Base(4) + Σ penalties

Penalties:
- V_meta(s₀) < 0.40: +2 iterations
- Domain scope fuzzy: +1 iteration
- Multi-context validation: +2 iterations
- Specialization needed: +1 iteration
- Automation unclear: +1 iteration
```

### Worked Examples

**Bootstrap-003 (Error Recovery)**:
```
Base: 4
V_meta(s₀) = 0.48 ≥ 0.40: +0 ✓
Domain scope clear: +0 ✓
Retrospective validation: +0 ✓
Generic agents sufficient: +0 ✓
Automation identified early: +0 ✓
---
Predicted: 4 iterations
Actual: 3 iterations ✅
```

**Bootstrap-002 (Test Strategy)**:
```
Base: 4
V_meta(s₀) = 0.04 < 0.40: +2 ✗
Domain scope broad: +1 ✗
Multi-context validation: +2 ✗
Specialization needed: +1 ✗
Automation unclear: +0 ✓
---
Predicted: 10 iterations
Actual: 6 iterations ✅ (model conservative)
```

**Interpretation**: Model predicts upper bound. Actual often faster due to efficient execution.

See [examples/prediction-examples.md](examples/prediction-examples.md) for more cases.

---

## Rapid Convergence Strategy

If criteria indicate 3-4 iteration potential, optimize:

### Pre-Iteration 0: Planning (1-2 hours)

**1. Establish Baseline Metrics**
- Identify existing data sources
- Define quantifiable success criteria
- Ensure automatic measurement

**Example**: `meta-cc query-tools --status error` → 1,336 errors immediately

**2. Scope Domain Tightly**
- Write 1-sentence definition
- List explicit in/out boundaries
- Identify prior art

**Example**: "Error detection, diagnosis, recovery, prevention for meta-cc"

**3. Plan Validation Approach**
- Prefer retrospective (historical data)
- Minimize multi-context overhead
- Identify proxy metrics

**Example**: Retrospective validation with 1,336 historical errors

### Iteration 0: Comprehensive Baseline (3-5 hours)

**Target: V_meta(s₀) ≥ 0.40**

**Tasks**:
1. Quantify current state thoroughly
2. Create initial taxonomy (≥70% coverage)
3. Document existing practices
4. Identify top 3 automations

**Example (Bootstrap-003)**:
- Analyzed all 1,336 errors
- Created 10-category taxonomy (79.1% coverage)
- Documented 5 workflows, 5 patterns, 8 guidelines
- Identified 3 tools preventing 23.7% errors
- Result: V_meta(s₀) = 0.48 ✅

**Time**: Spend 3-5 hours here (saves 6-10 hours overall)

### Iteration 1: High-Impact Automation (3-4 hours)

**Tasks**:
1. Implement top 3 tools
2. Expand taxonomy (≥90% coverage)
3. Validate with data (if possible)
4. Target: ΔV_instance = +0.20-0.30

**Example (Bootstrap-003)**:
- Built 3 tools (515 LOC, ~150-180 lines each)
- Expanded taxonomy: 10 → 12 categories (92.3%)
- Result: V_instance = 0.55 (+0.27) ✅

### Iteration 2: Validate and Converge (3-4 hours)

**Tasks**:
1. Test automation (real/historical data)
2. Complete taxonomy (≥95% coverage)
3. Check convergence:
   - V_instance ≥ 0.80?
   - V_meta ≥ 0.80?
   - System stable?

**Example (Bootstrap-003)**:
- Validated 23.7% error prevention
- Taxonomy: 95.4% coverage
- Result: V_instance = 0.83, V_meta = 0.85 ✅ CONVERGED

**Total time**: 10-13 hours (3 iterations)

---

## Anti-Patterns

### 1. Premature Convergence

**Symptom**: Declare convergence at iteration 2 with V ≈ 0.75

**Problem**: Rushed without meeting 0.80 threshold

**Solution**: Rapid convergence = 3-4 iterations (not 2). Respect quality threshold.

### 2. Scope Creep

**Symptom**: Adding categories/patterns in iterations 3-4

**Problem**: Poorly scoped domain

**Solution**: Tight scoping in README. If scope grows, re-plan or accept slower convergence.

### 3. Over-Engineering Automation

**Symptom**: Spending 8+ hours on complex tools

**Problem**: Complexity delays convergence

**Solution**: Keep tools simple (1-2 hours, 150-200 lines). Complex tools are iteration 3-4 work.

### 4. Unnecessary Multi-Context Validation

**Symptom**: Testing 3+ contexts despite obvious generalizability

**Problem**: Validation overhead delays convergence

**Solution**: Use judgment. Error recovery is universal. Test strategy may need multi-context.

---

## Comparison Table

| Aspect | Standard | Rapid |
|--------|----------|-------|
| **Iterations** | 5-7 | 3-4 |
| **Duration** | 20-30h | 10-15h |
| **V_meta(s₀)** | 0.00-0.30 | 0.40-0.60 |
| **Domain** | Broad/exploratory | Focused |
| **Validation** | Multi-context often | Direct/retrospective |
| **Specialization** | Likely (1-3 agents) | Often unnecessary |
| **Discovery** | Incremental | Most patterns early |
| **Risk** | Scope creep | Premature convergence |

**Key**: Rapid convergence is about **recognizing structural factors**, not rushing.

---

## Success Criteria

Rapid convergence pattern successfully applied when:

1. **Accurate prediction**: Actual iterations within ±1 of predicted
2. **Quality maintained**: V_instance ≥ 0.80, V_meta ≥ 0.80
3. **Time efficiency**: Duration ≤50% of standard convergence
4. **Artifact completeness**: Deliverables production-ready
5. **Reusability validated**: ≥80% transferability achieved

**Bootstrap-003 Validation**:
- ✅ Predicted: 3-4, Actual: 3
- ✅ Quality: V_instance=0.83, V_meta=0.85
- ✅ Efficiency: 10h (39% of Bootstrap-002's 25.5h)
- ✅ Artifacts: 13 categories, 8 workflows, 3 tools
- ✅ Reusability: 85-90%

---

## Related Skills

**Parent framework**:
- [methodology-bootstrapping](../methodology-bootstrapping/SKILL.md) - Core OCA cycle

**Complementary acceleration**:
- [retrospective-validation](../retrospective-validation/SKILL.md) - Fast validation
- [baseline-quality-assessment](../baseline-quality-assessment/SKILL.md) - Strong iteration 0

**Supporting**:
- [agent-prompt-evolution](../agent-prompt-evolution/SKILL.md) - Agent stability

---

## References

**Core guide**:
- [Rapid Convergence Criteria](reference/criteria.md) - Detailed criteria explanation
- [Prediction Model](reference/prediction-model.md) - Formula and examples
- [Strategy Guide](reference/strategy.md) - Iteration-by-iteration tactics

**Examples**:
- [Bootstrap-003 Case Study](examples/error-recovery-3-iterations.md) - Rapid convergence
- [Bootstrap-002 Comparison](examples/test-strategy-6-iterations.md) - Standard convergence

---

**Status**: ✅ Validated | Bootstrap-003 | 40-60% time reduction | No quality sacrifice
