---
name: Agent Prompt Evolution
description: Track and optimize agent specialization during methodology development. Use when agent specialization emerges (generic agents show >5x performance gap), multi-experiment comparison needed, or methodology transferability analysis required. Captures agent set evolution (Aₙ tracking), meta-agent evolution (Mₙ tracking), specialization decisions (when/why to create specialized agents), and reusability assessment (universal vs domain-specific vs task-specific). Enables systematic cross-experiment learning and optimized M₀ evolution. 2-3 hours overhead per experiment.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Agent Prompt Evolution

**Systematically track how agents specialize during methodology development.**

> Specialized agents emerge from need, not prediction. Track their evolution to understand when specialization adds value.

---

## When to Use This Skill

Use this skill when:
- 🔄 **Agent specialization emerges**: Generic agents show >5x performance gap
- 📊 **Multi-experiment comparison**: Want to learn across experiments
- 🧩 **Methodology transferability**: Analyzing what's reusable vs domain-specific
- 📈 **M₀ optimization**: Want to evolve base Meta-Agent capabilities
- 🎯 **Specialization decisions**: Deciding when to create new agents
- 📚 **Agent library**: Building reusable agent catalog

**Don't use when**:
- ❌ Single experiment with no specialization
- ❌ Generic agents sufficient throughout
- ❌ No cross-experiment learning goals
- ❌ Tracking overhead not worth insights

---

## Quick Start (10 minutes per iteration)

### Track Agent Evolution in Each Iteration

**iteration-N.md template**:

```markdown
## Agent Set Evolution

### Current Agent Set (Aₙ)
1. **coder** (generic) - Write code, implement features
2. **doc-writer** (generic) - Documentation
3. **data-analyst** (generic) - Data analysis
4. **coverage-analyzer** (specialized, created iteration 3) - Analyze test coverage gaps

### Changes from Previous Iteration
- Added: coverage-analyzer (10x speedup for coverage analysis)
- Removed: None
- Modified: None

### Specialization Decision
**Why coverage-analyzer?**
- Generic data-analyst took 45 min for coverage analysis
- Identified 10x performance gap
- Coverage analysis is recurring task (every iteration)
- Domain knowledge: Go coverage tools, gap identification patterns
- **ROI**: 3 hours creation cost, saves 40 min/iteration × 3 remaining iterations = 2 hours saved

### Agent Reusability Assessment
- **coder**: Universal (100% transferable)
- **doc-writer**: Universal (100% transferable)
- **data-analyst**: Universal (100% transferable)
- **coverage-analyzer**: Domain-specific (testing methodology, 70% transferable to other languages)

### System State
- Aₙ ≠ Aₙ₋₁ (new agent added)
- System UNSTABLE (need iteration N+1 to confirm stability)
```

---

## Four Tracking Dimensions

### 1. Agent Set Evolution (Aₙ)

**Track changes iteration-to-iteration**:

```
A₀ = {coder, doc-writer, data-analyst}
A₁ = {coder, doc-writer, data-analyst} (unchanged)
A₂ = {coder, doc-writer, data-analyst} (unchanged)
A₃ = {coder, doc-writer, data-analyst, coverage-analyzer} (new specialist)
A₄ = {coder, doc-writer, data-analyst, coverage-analyzer, test-generator} (new specialist)
A₅ = {coder, doc-writer, data-analyst, coverage-analyzer, test-generator} (stable)
```

**Stability**: Aₙ == Aₙ₋₁ for convergence

### 2. Meta-Agent Evolution (Mₙ)

**Standard M₀ capabilities**:
1. **observe**: Pattern observation
2. **plan**: Iteration planning
3. **execute**: Agent orchestration
4. **reflect**: Value assessment
5. **evolve**: System evolution

**Track enhancements**:

```
M₀ = {observe, plan, execute, reflect, evolve}
M₁ = {observe, plan, execute, reflect, evolve, gap-identify} (new capability)
M₂ = {observe, plan, execute, reflect, evolve, gap-identify} (stable)
```

**Finding** (from 8 experiments): M₀ sufficient in all cases (no evolution needed)

### 3. Specialization Decision Tree

**When to create specialized agent**:

```
Decision tree:
1. Is generic agent sufficient? (performance within 2x)
   YES → No specialization
   NO → Continue

2. Is task recurring? (happens ≥3 times)
   NO → One-off, tolerate slowness
   YES → Continue

3. Is performance gap >5x?
   NO → Tolerate moderate slowness
   YES → Continue

4. Is creation cost <ROI?
   Creation cost < (Time saved per use × Remaining uses)
   NO → Not worth it
   YES → Create specialized agent
```

**Example** (Bootstrap-002):

```
Task: Test coverage gap analysis
Generic agent (data-analyst): 45 min
Potential specialist (coverage-analyzer): 4.5 min (10x faster)

Recurring: YES (every iteration, 3 remaining)
Performance gap: 10x (>5x threshold)
Creation cost: 3 hours
ROI: (45-4.5) min × 3 = 121.5 min = 2 hours saved
Decision: CREATE (positive ROI)
```

### 4. Reusability Assessment

**Three categories**:

**Universal** (90-100% transferable):
- Generic agents (coder, doc-writer, data-analyst)
- No domain knowledge required
- Applicable across all domains

**Domain-Specific** (60-80% transferable):
- Requires domain knowledge (testing, CI/CD, error handling)
- Patterns apply within domain
- Needs adaptation for other domains

**Task-Specific** (10-30% transferable):
- Highly specialized for particular task
- One-off creation
- Unlikely to reuse

**Examples**:

```
Agent: coverage-analyzer
Domain: Testing methodology
Transferability: 70%
- Go coverage tools (language-specific, 30% adaptation)
- Gap identification patterns (universal, 100%)
- Overall: 70% transferable to Python/Rust/TypeScript testing

Agent: test-generator
Domain: Testing methodology
Transferability: 40%
- Go test syntax (language-specific, 0% to other languages)
- Test pattern templates (moderately transferable, 60%)
- Overall: 40% transferable

Agent: log-analyzer
Domain: Observability
Transferability: 85%
- Log parsing (universal, 95%)
- Pattern recognition (universal, 100%)
- Structured logging concepts (universal, 100%)
- Go slog specifics (language-specific, 20%)
- Overall: 85% transferable
```

---

## Evolution Log Template

Create `agents/EVOLUTION-LOG.md`:

```markdown
# Agent Evolution Log

## Experiment Overview
- Domain: Testing Strategy
- Baseline agents: 3 (coder, doc-writer, data-analyst)
- Final agents: 5 (+coverage-analyzer, +test-generator)
- Specialization count: 2

---

## Iteration-by-Iteration Evolution

### Iteration 0
**Agent Set**: {coder, doc-writer, data-analyst}
**Changes**: None (baseline)
**Observations**: Generic agents sufficient for baseline establishment

### Iteration 3
**Agent Set**: {coder, doc-writer, data-analyst, coverage-analyzer}
**Changes**: +coverage-analyzer
**Reason**: 10x performance gap (45 min → 4.5 min)
**Creation Cost**: 3 hours
**ROI**: Positive (2 hours saved over 3 iterations)
**Reusability**: 70% (domain-specific, testing)

### Iteration 4
**Agent Set**: {coder, doc-writer, data-analyst, coverage-analyzer, test-generator}
**Changes**: +test-generator
**Reason**: 200x performance gap (manual test writing too slow)
**Creation Cost**: 4 hours
**ROI**: Massive (saved 10+ hours)
**Reusability**: 40% (task-specific, Go testing)

### Iteration 5
**Agent Set**: {coder, doc-writer, data-analyst, coverage-analyzer, test-generator}
**Changes**: None
**System**: STABLE (Aₙ == Aₙ₋₁)

---

## Specialization Analysis

### coverage-analyzer
**Purpose**: Analyze test coverage, identify gaps
**Performance**: 10x faster than generic data-analyst
**Domain**: Testing methodology
**Transferability**: 70%
**Lessons**: Coverage gap identification patterns are universal, tool integration is language-specific

### test-generator
**Purpose**: Generate test boilerplate from coverage gaps
**Performance**: 200x faster than manual
**Domain**: Testing methodology (Go-specific)
**Transferability**: 40%
**Lessons**: High speedup justified low transferability, patterns reusable but syntax is not

---

## Cross-Experiment Reuse

### From Previous Experiments
- **validation-builder** (from API design experiment) → Used for smoke test validation
- Reusability: Excellent (validation patterns are universal)
- Adaptation: Minimal (10 min to adapt from API to CI/CD context)

### To Future Experiments
- **coverage-analyzer** → Reusable for Python/Rust/TypeScript testing (70% transferable)
- **test-generator** → Less reusable (40% transferable, needs rewrite for other languages)

---

## Meta-Agent Evolution

### M₀ Capabilities
{observe, plan, execute, reflect, evolve}

### Changes
None (M₀ sufficient throughout)

### Observations
- M₀'s "evolve" capability successfully identified need for specialization
- No Meta-Agent evolution required
- Convergence: Mₙ == M₀ for all iterations

---

## Lessons Learned

### Specialization Decisions
- **10x performance gap** is good threshold (< 5x not worth it, >10x clear win)
- **Positive ROI required**: Creation cost must be justified by time savings
- **Recurring tasks only**: One-off tasks don't justify specialization

### Reusability Patterns
- **Generic agents always reusable**: coder, doc-writer, data-analyst (100%)
- **Domain agents moderately reusable**: coverage-analyzer (70%)
- **Task agents rarely reusable**: test-generator (40%)

### When NOT to Specialize
- Performance gap <5x (tolerable slowness)
- Task is one-off (no recurring benefit)
- Creation cost >ROI (not worth time investment)
- Generic agent will improve with practice (learning curve)
```

---

## Cross-Experiment Analysis

After 3+ experiments, create `agents/CROSS-EXPERIMENT-ANALYSIS.md`:

```markdown
# Cross-Experiment Agent Analysis

## Agent Reuse Matrix

| Agent | Exp1 | Exp2 | Exp3 | Reuse Rate | Transferability |
|-------|------|------|------|------------|-----------------|
| coder | ✓ | ✓ | ✓ | 100% | Universal |
| doc-writer | ✓ | ✓ | ✓ | 100% | Universal |
| data-analyst | ✓ | ✓ | ✓ | 100% | Universal |
| coverage-analyzer | ✓ | - | ✓ | 67% | Domain (testing) |
| test-generator | ✓ | - | - | 33% | Task-specific |
| validation-builder | - | ✓ | ✓ | 67% | Domain (validation) |
| log-analyzer | - | - | ✓ | 33% | Domain (observability) |

## Specialization Patterns

### Universal Agents (100% reuse)
- Generic capabilities (coder, doc-writer, data-analyst)
- No domain knowledge
- Always included in A₀

### Domain Agents (50-80% reuse)
- Require domain knowledge (testing, CI/CD, observability)
- Reusable within domain
- Examples: coverage-analyzer, validation-builder, log-analyzer

### Task Agents (10-40% reuse)
- Highly specialized
- One-off or rare reuse
- Examples: test-generator (Go-specific)

## M₀ Sufficiency

**Finding**: M₀ = {observe, plan, execute, reflect, evolve} sufficient in ALL experiments

**Implications**:
- No Meta-Agent evolution needed
- Base capabilities handle all domains
- Specialization occurs at Agent layer, not Meta-Agent layer

## Specialization Threshold

**Data** (from 3 experiments):
- Average performance gap for specialization: 15x (range: 5x-200x)
- Average creation cost: 3.5 hours (range: 2-5 hours)
- Average ROI: Positive in 8/9 cases (89% success rate)

**Recommendation**: Use 5x performance gap as threshold

---

**Updated**: After each new experiment
```

---

## Success Criteria

Agent evolution tracking succeeded when:

1. **Complete tracking**: All agent changes documented each iteration
2. **Specialization justified**: Each specialized agent has clear ROI
3. **Reusability assessed**: Each agent categorized (universal/domain/task)
4. **Cross-experiment learning**: Patterns identified across 2+ experiments
5. **M₀ stability documented**: Meta-Agent evolution (or lack thereof) tracked

---

## Related Skills

**Parent framework**:
- [methodology-bootstrapping](../methodology-bootstrapping/SKILL.md) - Core OCA cycle

**Complementary**:
- [rapid-convergence](../rapid-convergence/SKILL.md) - Agent stability criterion

---

## References

**Core guide**:
- [Evolution Tracking](reference/tracking.md) - Detailed tracking process
- [Specialization Decisions](reference/specialization.md) - Decision tree
- [Reusability Framework](reference/reusability.md) - Assessment rubric

**Examples**:
- [Bootstrap-002 Evolution](examples/testing-strategy-agent-evolution.md) - 2 specialists
- [Bootstrap-007 No Evolution](examples/ci-cd-no-specialization.md) - Generic sufficient

---

**Status**: ✅ Formalized | 2-3 hours overhead | Enables systematic learning
