---
name: code-modularization-evaluator
description: Evaluate and improve code modularization using the Balanced Coupling Model. Analyzes coupling strength, connascence types, and distance to identify refactoring opportunities and architectural improvements. Use when reviewing code architecture, refactoring modules, or designing new systems.
version: 1.0.0
---

# Code Modularization Evaluator

Evaluate code modularization using the Balanced Coupling Model from Vlad Khononov's "Balancing Coupling in Software Design." This skill helps identify problematic coupling patterns and provides actionable refactoring guidance.

## Core Principle

**Coupling is not inherently bad—misdesigned coupling is bad.** The goal is balanced coupling, not zero coupling. 

The fundamental formula:

```
MODULARITY = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY
```

A system achieves modularity when:
- High integration strength components are close together (same module/service)
- Low integration strength components can be far apart (different services)
- Low volatility components can tolerate coupling mismatches

## The Three Dimensions of Coupling

Always evaluate coupling across these three dimensions: 

### 1. Integration Strength (What knowledge is shared?)

From strongest (worst) to weakest (best):

| Level | Type | Description | Example |
|-------|------|-------------|---------|
| 1 | **Intrusive** | Using non-public interfaces | Direct database access to another service, reflection on private fields |
| 2 | **Functional** | Sharing business logic/rules | Same validation duplicated in two places, order-dependent operations |
| 3 | **Model** | Sharing domain models | Two services using identical entity definitions |
| 4 | **Contract** | Only explicit interfaces | Well-designed APIs, DTOs, protocols |

### 2. Distance (How far does knowledge travel?)

From closest to most distant:
1. Methods within same class
2. Classes within same file
3. Classes in same namespace/package
4. Modules in different namespaces
5. Separate services/microservices
6. Services owned by different teams
7. Different systems/organizations 

### 3. Volatility (How often will it change?)

Use Domain-Driven Design subdomain classification:
- **Core subdomains**: High volatility (competitive advantage, frequent changes)
- **Supporting subdomains**: Low volatility (necessary but not differentiating)
- **Generic subdomains**: Low volatility (solved problems, stable)

## Decision Framework

When evaluating code, apply this matrix:

| Integration Strength | Distance | Result |
|---------------------|----------|--------|
| **High** | **High** | ❌ COMPLEXITY (Distributed monolith) |
| **Low** | **Low** | ❌ COMPLEXITY (Unnecessary abstraction) |
| **High** | **Low** | ✅ MODULARITY (Related things together) |
| **Low** | **High** | ✅ MODULARITY (Independent components apart) |

**Exception**: If volatility is LOW, coupling mismatches are acceptable. 

## Connascence Analysis

Use connascence to identify specific coupling types. See `references/connascence-types.md` for detailed examples.

### Static Connascence (Compile-time, easier to fix)
Ordered weakest to strongest:
1. **Name (CoN)**: Components agree on names
2. **Type (CoT)**: Components agree on types
3. **Meaning (CoM)**: Components agree on value meanings (magic numbers)
4. **Position (CoP)**: Components agree on order of values
5. **Algorithm (CoA)**: Components share algorithm logic 

### Dynamic Connascence (Runtime, harder to detect)
Ordered weakest to strongest:
6. **Execution (CoE)**: Order of method calls matters
7. **Timing (CoTm)**: Timing of execution matters
8. **Value (CoV)**: Multiple values must change together
9. **Identity (CoI)**: Must reference same instance 

### Connascence Rules
1. Minimize overall connascence
2. Minimize connascence crossing module boundaries
3. Maximize connascence within module boundaries
4. Convert stronger connascence to weaker forms
5. As distance increases, connascence should weaken

## Evaluation Checklist

When analyzing code, check for:

### Red Flags (Immediate Action Required)
- [ ] Direct database access to another service's data (Intrusive coupling)
- [ ] Reflection to access private fields
- [ ] Business logic duplicated across services
- [ ] Microservices requiring synchronized deployments
- [ ] CBO (Coupling Between Objects) > 14 for a class
- [ ] Instability index 0.3-0.7 for frequently-changing modules
- [ ] Circular dependencies between modules

### Warning Signs (Investigate Further)
- [ ] Magic numbers/values shared between components (CoM)
- [ ] Position-dependent parameters in APIs (CoP)
- [ ] Algorithm logic duplicated in multiple places (CoA)
- [ ] Methods must be called in specific order (CoE)
- [ ] Long method chains: `a.b().c().d()` (Law of Demeter violation)
- [ ] Classes with "Manager", "Helper", "Utility" doing too much

### Healthy Patterns
- [x] Contract-based integration between services
- [x] DTOs that truly abstract internal models
- [x] High cohesion within modules
- [x] Single responsibility per class
- [x] Dependency injection for external dependencies

## Refactoring Strategies

### By Integration Strength Problem

**Intrusive → Contract Coupling**:
1. Identify all direct dependencies on implementation details
2. Define explicit interface/contract
3. Create adapter layer
4. Route all access through adapter

**Functional → Model Coupling**:
1. Extract shared business logic to dedicated module
2. Define clear ownership
3. Consume via explicit dependency

**Model → Contract Coupling**:
1. Create integration-specific DTOs
2. Map between internal models and DTOs at boundaries
3. Version contracts independently of models

### By Connascence Type

| From | To | Technique |
|------|-----|-----------|
| CoM (Meaning) | CoN (Name) | Replace magic values with named constants/enums |
| CoP (Position) | CoN (Name) | Use named parameters, builder pattern, or parameter objects |
| CoA (Algorithm) | CoN (Name) | Extract algorithm to single location, reference by name |
| CoT (Type) | CoN (Name) | Use duck typing or interfaces |
| CoE (Execution) | Explicit | Use state machines, builder pattern, or constructor injection |
| CoI (Identity) | Explicit | Use dependency injection with explicit wiring |

### By Distance Problem

**High Strength + High Distance** (Distributed Monolith):
- Option A: Reduce distance—merge services/modules
- Option B: Reduce strength—introduce contracts, async messaging

**Low Strength + Low Distance** (Over-abstraction):
- Remove unnecessary abstraction layers
- Inline overly generic code
- Combine closely-related classes

## Analysis Workflow

When asked to evaluate code modularization:

1. **Map the component structure**
   - Identify modules, services, classes
   - Draw dependency graph

2. **Assess Integration Strength**
   - For each dependency, classify: Intrusive/Functional/Model/Contract
   - Flag high-strength cross-boundary dependencies

3. **Measure Distance**
   - Note component locations (same file → different systems)
   - Identify team/ownership boundaries

4. **Evaluate Volatility**
   - Classify each component's subdomain type
   - Note historically frequently-changed areas

5. **Apply the formula**
   - Check: Does strength match distance appropriately?
   - Does volatility excuse any mismatches?

6. **Identify Connascence**
   - Scan for specific connascence types
   - Prioritize: high strength + low locality + high degree

7. **Recommend actions**
   - Prioritize by impact and effort
   - Provide specific refactoring techniques

## Output Format

Structure your evaluation as:
```markdown
## Modularization Assessment

### Summary
[Brief overview of coupling health]

### Component Map
[Describe module/service structure]

### Coupling Analysis
| Component Pair | Strength | Distance | Volatility | Balance |
|---------------|----------|----------|------------|---------|
| A → B         | Model    | High     | High       | ❌      |

### Connascence Issues
1. [Specific connascence type]: [Location] - [Impact]

### Recommendations
1. **Priority 1**: [Action] - [Rationale]
2. **Priority 2**: [Action] - [Rationale]

### Refactoring Plan
[Step-by-step approach for highest-priority item]
```

## References

- For detailed connascence examples: see `references/connascence-types.md`
- For coupling metrics: see `references/coupling-metrics.md`
- For refactoring patterns: see `references/refactoring-patterns.md`

## Limitations

- Cannot assess runtime behavior without execution context
- Volatility assessment requires domain knowledge
- Team/organizational distance requires project context
- Historical change frequency not available from static analysis alone
