---
name: layered-reasoning
description: Use when reasoning across multiple abstraction levels (strategic/tactical/operational), designing systems with hierarchical layers, explaining concepts at different depths, maintaining consistency between high-level principles and concrete implementation, or when users mention 30,000-foot view, layered thinking, abstraction levels, top-down design, or need to move fluidly between strategy and execution.
---

# Layered Reasoning

## Purpose

Layered reasoning structures thinking across multiple levels of abstraction—from high-level principles (30,000 ft) to tactical approaches (3,000 ft) to concrete actions (300 ft). Good layered reasoning maintains consistency: lower layers implement upper layers, upper layers constrain lower layers, and each layer is independently useful.

Use this skill when:
- **Designing systems** with architectural layers (strategy → design → implementation)
- **Explaining complex topics** at multiple depths (executive summary → technical detail → code)
- **Strategic planning** connecting vision → objectives → tactics → tasks
- **Ensuring consistency** between principles and execution
- **Bridging communication** between stakeholders at different levels (CEO → manager → engineer)
- **Problem-solving** where high-level constraints must guide low-level decisions

Layered reasoning prevents inconsistency: strategic plans that can't be executed, implementations that violate principles, or explanations that confuse by jumping abstraction levels.

---

## Common Patterns

### Pattern 1: 30K → 3K → 300 ft Decomposition (Top-Down)

**When**: Starting from vision/principles, deriving concrete actions

**Structure**:
- **30,000 ft (Strategic)**: Why? Core principles, invariants, constraints (e.g., "Customer privacy is non-negotiable")
- **3,000 ft (Tactical)**: What? Approaches, architectures, policies (e.g., "Zero-trust security model, end-to-end encryption")
- **300 ft (Operational)**: How? Specific actions, procedures, code (e.g., "Implement AES-256 encryption for data at rest")

**Example**: Product strategy
- **30K**: "Become the most trusted platform" (principle)
- **3K**: "Achieve SOC 2 compliance, publish security reports, 24/7 support" (tactics)
- **300 ft**: "Implement MFA, conduct quarterly audits, hire 5 support engineers" (actions)

**Process**: (1) Define strategic layer invariants, (2) Derive tactical options that satisfy invariants, (3) Select tactics, (4) Design operational procedures implementing tactics, (5) Validate operational layer doesn't violate strategic constraints

### Pattern 2: Bottom-Up Aggregation

**When**: Starting from observations/data, building up to principles

**Structure**:
- **300 ft**: Specific observations, measurements, incidents (e.g., "User A clicked 5 times, User B abandoned")
- **3,000 ft**: Patterns, trends, categories (e.g., "40% abandon at checkout, slow load times correlate with abandonment")
- **30,000 ft**: Principles, theories, root causes (e.g., "Performance impacts conversion; every 100ms costs 1% conversion")

**Example**: Engineering postmortem
- **300 ft**: "Service crashed at 3:42 PM, memory usage spiked to 32GB, 500 errors returned"
- **3K**: "Memory leak in caching layer, triggered by specific API call pattern under load"
- **30K**: "Our caching strategy lacks eviction policy; need TTL-based expiration for all caches"

**Process**: (1) Collect operational data, (2) Identify patterns and group, (3) Formulate hypotheses at tactical layer, (4) Validate with more data, (5) Distill strategic principles

### Pattern 3: Layer Translation (Cross-Layer Communication)

**When**: Explaining same concept to different audiences (CEO, manager, engineer)

**Technique**: Translate preserving core meaning while adjusting abstraction

**Example**: Explaining tech debt
- **CEO (30K)**: "We built quickly early on. Now growth slows 20% annually unless we invest $2M to modernize."
- **Manager (3K)**: "Monolithic architecture prevents independent team velocity. Migrate to microservices over 6 months."
- **Engineer (300 ft)**: "Extract user service from monolith. Create API layer, implement service mesh, migrate traffic."

**Process**: (1) Identify audience's layer, (2) Extract core message, (3) Translate using concepts/metrics relevant to that layer, (4) Maintain causal links across layers

### Pattern 4: Constraint Propagation (Top-Down)

**When**: High-level constraints must guide low-level decisions

**Mechanism**: Strategic constraints flow down, narrowing options at each layer

**Example**: Healthcare app design
- **30K constraint**: "HIPAA compliance is non-negotiable" (strategic)
- **3K derivation**: "All PHI must be encrypted, audit logs required, access control mandatory" (tactical)
- **300 ft implementation**: "Use AWS KMS for encryption, CloudTrail for audits, IAM for access" (operational)

**Guardrail**: Lower layers cannot violate upper constraints (e.g., operational decision to skip encryption violates strategic constraint)

### Pattern 5: Emergent Property Recognition (Bottom-Up)

**When**: Lower-layer interactions create unexpected upper-layer behavior

**Example**: Team structure
- **300 ft**: "Each team owns microservice, deploys independently, uses Slack for coordination"
- **3K emergence**: "Conway's Law: architecture mirrors communication structure; slow cross-team features"
- **30K insight**: "Org structure determines system architecture; realign teams to product lines, not services"

**Process**: (1) Observe operational behavior, (2) Identify emerging patterns at tactical layer, (3) Recognize strategic implications, (4) Adjust strategy if needed

### Pattern 6: Consistency Checking Across Layers

**When**: Validating that all layers align (no contradictions)

**Check types**:
- **Upward consistency**: Do operations implement tactics? Do tactics achieve strategy?
- **Downward consistency**: Can strategy be executed with these tactics? Can tactics be implemented operationally?
- **Lateral consistency**: Do parallel tactical choices contradict? Do operational procedures conflict?

**Example inconsistency**: Strategy says "Move fast," tactics say "Extensive approval process," operations say "3-week release cycle" → Contradiction

**Fix**: Align layers. Either (1) change strategy ("Move carefully"), (2) change tactics ("Lightweight approvals"), or (3) change operations ("Daily releases")

---

## Workflow

Use this structured approach when applying layered reasoning:

```
□ Step 1: Identify relevant layers and abstraction levels
□ Step 2: Define strategic layer (principles, invariants, constraints)
□ Step 3: Derive tactical layer (approaches that satisfy strategy)
□ Step 4: Design operational layer (concrete actions implementing tactics)
□ Step 5: Validate consistency across all layers
□ Step 6: Translate between layers for different audiences
□ Step 7: Iterate based on feedback from any layer
□ Step 8: Document reasoning at each layer
```

**Step 1: Identify relevant layers and abstraction levels** ([details](#1-identify-relevant-layers-and-abstraction-levels))
Determine how many layers needed (typically 3-5). Map layers to domains: business (vision/strategy/execution), technical (architecture/design/code), organizational (mission/goals/tasks).

**Step 2: Define strategic layer** ([details](#2-define-strategic-layer))
Establish high-level principles, invariants, and constraints that must hold. These are non-negotiable and guide all lower layers.

**Step 3: Derive tactical layer** ([details](#3-derive-tactical-layer))
Generate approaches/policies/architectures that satisfy strategic constraints. Multiple tactical options may exist; choose based on tradeoffs.

**Step 4: Design operational layer** ([details](#4-design-operational-layer))
Create specific procedures, implementations, or actions that realize tactical choices. This is where execution happens.

**Step 5: Validate consistency across all layers** ([details](#5-validate-consistency-across-all-layers))
Check upward (do ops implement tactics?), downward (can strategy be executed?), and lateral (do parallel choices conflict?) consistency.

**Step 6: Translate between layers for different audiences** ([details](#6-translate-between-layers-for-different-audiences))
Communicate at appropriate abstraction level for each stakeholder. CEO needs strategic view, engineers need operational detail.

**Step 7: Iterate based on feedback from any layer** ([details](#7-iterate-based-on-feedback-from-any-layer))
If operational constraints make tactics infeasible, adjust tactics or strategy. If strategic shift occurs, propagate changes downward.

**Step 8: Document reasoning at each layer** ([details](#8-document-reasoning-at-each-layer))
Write explicit rationale at each layer explaining how it relates to layers above/below. Makes assumptions visible and aids future iteration.

---

## Critical Guardrails

### 1. Maintain Consistency Across Layers

**Danger**: Strategic goals contradict operational reality, or implementation violates principles

**Guardrail**: Regularly check upward, downward, and lateral consistency. Propagate changes bidirectionally (strategy changes → update tactics/ops; operational constraints → update tactics/strategy).

**Red flag**: "Our strategy is X but we actually do Y" signals layer mismatch

### 2. Don't Skip Layers When Communicating

**Danger**: Jumping from 30K to 300 ft confuses audiences, loses context

**Guardrail**: Move through layers sequentially. If explaining to executive, start 30K → 3K (stop there unless asked). If explaining to engineer, provide 30K context first, then dive to 300 ft.

**Test**: Can listener answer "why does this matter?" (links to upper layer) and "how do we do this?" (links to lower layer)

### 3. Each Layer Should Be Independently Useful

**Danger**: Layers that only make sense when combined, not standalone

**Guardrail**: Strategic layer should guide decisions even without seeing operations. Tactical layer should be understandable without code. Operational layer should be executable without re-deriving strategy.

**Principle**: Good layers can be consumed independently by different audiences

### 4. Limit Layers to 3-5 Levels

**Danger**: Too many layers create overhead; too few lose nuance

**Guardrail**: For most domains, 3 layers sufficient (strategy/tactics/operations or architecture/design/code). Complex domains may need 4-5 but rarely more.

**Rule of thumb**: Can you name each layer clearly? If not, you have too many.

### 5. Upper Layers Constrain, Lower Layers Implement

**Danger**: Treating layers as independent rather than hierarchical

**Guardrail**: Strategic layer sets constraints ("must be HIPAA compliant"). Tactical layer chooses approaches within constraints ("encryption + audit logs"). Operational layer implements ("AES-256 + CloudTrail"). Cannot violate upward.

**Anti-pattern**: Operational decision ("skip encryption for speed") violating strategic constraint ("HIPAA compliance")

### 6. Propagate Changes Bidirectionally

**Danger**: Strategic shift without updating tactics/ops, or operational constraint discovered but strategy unchanged

**Guardrail**: **Top-down**: Strategy changes → re-evaluate tactics → adjust operations. **Bottom-up**: Operational constraint → re-evaluate tactics → potentially adjust strategy.

**Example**: Strategy shift to "privacy-first" → Update tactics (end-to-end encryption) → Update ops (implement encryption). Or: Operational constraint (performance) → Tactical adjustment (different approach) → Strategic clarification ("privacy-first within performance constraints")

### 7. Make Assumptions Explicit at Each Layer

**Danger**: Implicit assumptions lead to inconsistency when assumptions violated

**Guardrail**: Document assumptions at each layer. Strategic: "Assuming competitive market." Tactical: "Assuming cloud infrastructure." Operational: "Assuming Python 3.9+."

**Benefit**: When assumptions change, know which layers need updating

### 8. Recognize Emergent Properties

**Danger**: Focusing only on designed properties, missing unintended consequences

**Guardrail**: Regularly observe bottom layer, look for emerging patterns at middle layer, consider strategic implications. Emergent properties can invalidate strategic assumptions.

**Example**: Microservices (operational) → Coordination overhead (tactical emergence) → Slower feature delivery (strategic failure if goal was speed)

---

## Quick Reference

### Layer Mapping by Domain

| Domain | Layer 1 (30K ft) | Layer 2 (3K ft) | Layer 3 (300 ft) |
|--------|------------------|-----------------|------------------|
| **Business** | Vision, mission | Strategy, objectives | Tactics, tasks |
| **Product** | Market positioning | Feature roadmap | User stories |
| **Technical** | Architecture principles | System design | Code implementation |
| **Organizational** | Culture, values | Policies, processes | Daily procedures |

### Consistency Check Questions

| Check Type | Question |
|------------|----------|
| **Upward** | Do these operations implement the tactics? Do tactics achieve strategy? |
| **Downward** | Can this strategy be executed with available tactics? Can tactics be implemented operationally? |
| **Lateral** | Do parallel tactical choices contradict each other? Do operational procedures conflict? |

### Translation Hints by Audience

| Audience | Layer | Focus | Metrics |
|----------|-------|-------|---------|
| **CEO / Board** | 30K ft | Why, outcomes, risk | Revenue, market share, strategic risk |
| **VP / Director** | 3K ft | What, approach, resources | Team velocity, roadmap, budget |
| **Manager / Lead** | 300-3K ft | How, execution, timeline | Sprint velocity, milestones, quality |
| **Engineer** | 300 ft | Implementation, details | Code quality, test coverage, performance |

---

## Resources

### Navigation to Resources

- [**Templates**](resources/template.md): Layered reasoning document template, consistency check template, cross-layer communication template
- [**Methodology**](resources/methodology.md): Layer design principles, consistency validation techniques, emergence detection, bidirectional propagation
- [**Rubric**](resources/evaluators/rubric_layered_reasoning.json): Evaluation criteria for layered reasoning quality (10 criteria)

### Related Skills

- **abstraction-concrete-examples**: For moving between abstract and concrete (related but less structured than layers)
- **decomposition-reconstruction**: For breaking down complex systems (complements layered approach)
- **communication-storytelling**: For translating between audiences at different layers
- **adr-architecture**: For documenting architectural decisions across layers
- **alignment-values-north-star**: For strategic layer definition (values → strategy)

---

## Examples in Context

### Example 1: SaaS Product Strategy

**30K (Strategic)**: "Become the easiest CRM for small businesses" (positioning)

**3K (Tactical)**: "Simple UI, 5-minute setup, mobile-first, $20/user pricing, self-serve onboarding"

**300 ft (Operational)**: "React app, OAuth for auth, Stripe for billing, onboarding flow: signup → import contacts → send first email"

**Consistency check**: Does $20 pricing support "easiest" (yes, low barrier)? Does 5-minute setup work with current implementation (measure in practice)? Does mobile-first align with React architecture (yes)?

### Example 2: Technical Architecture

**30K**: "Highly available system with <1% downtime, supports 10× traffic growth"

**3K**: "Multi-region deployment, auto-scaling, circuit breakers, blue-green deployments"

**300 ft**: "AWS multi-AZ, ECS Fargate with target tracking, Istio circuit breakers, CodeDeploy blue-green"

**Emergence**: Observed: cross-region latency 200ms → Tactical adjustment: regional data replication → Strategic clarification: "High availability within regions, eventual consistency across regions"

### Example 3: Organizational Change

**30K**: "Build customer-centric culture where customer feedback drives decisions"

**3K**: "Monthly customer advisory board, NPS surveys after each interaction, customer support KPIs in exec dashboards"

**300 ft**: "Schedule CAB meetings first Monday monthly, automated NPS via Delighted after ticket close, Looker dashboard with CS CSAT by rep"

**Consistency**: Does monthly CAB support "customer-centric" (or too infrequent)? Do support KPIs incentivize right behavior (check for gaming)? Does automation reduce personal touch (potential conflict)?
