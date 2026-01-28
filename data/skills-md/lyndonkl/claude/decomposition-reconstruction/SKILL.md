---
name: decomposition-reconstruction
description: Use when dealing with complex systems that need simplification, identifying bottlenecks or critical failure points, redesigning architecture or processes for better performance, breaking down problems that feel overwhelming, analyzing dependencies to understand ripple effects, user mentions "this is too complex", "where's the bottleneck", "how do we redesign this", "what are the key components", or when optimization requires understanding how parts interact.
---

# Decomposition & Reconstruction

## What Is It?

Decomposition-reconstruction is a two-phase analytical technique: first, break a complex system into atomic components and understand their relationships; second, either recombine components in better configurations or identify critical elements that drive system behavior.

**Quick example:**

**System:** Slow web application (3-second page load)

**Decomposition:**
- Frontend: 1.2s (JS bundle: 0.8s, CSS: 0.2s, HTML render: 0.2s)
- Network: 0.5s (API calls: 3 requests × 150ms each, parallel)
- Backend: 1.3s (Database query: 1.0s, business logic: 0.2s, serialization: 0.1s)

**Reconstruction (bottleneck identification):**
Critical path: Database query (1.0s) + JS bundle (0.8s) = 1.8s of the 3.0s total
Optimization target: Optimize DB query indexing and code-split JS bundle → Expected 1.5s page load

## Workflow

Copy this checklist and track your progress:

```
Decomposition & Reconstruction Progress:
- [ ] Step 1: Define the system and goal
- [ ] Step 2: Decompose into components and relationships
- [ ] Step 3: Analyze component properties and interactions
- [ ] Step 4: Reconstruct for insight or optimization
- [ ] Step 5: Validate and deliver recommendations
```

**Step 1: Define the system and goal**

Ask user to describe the system (what are we analyzing), current problem or goal (what needs improvement, understanding, or redesign), boundaries (what's in scope vs out of scope), and success criteria (what would "better" look like). Clear boundaries prevent endless decomposition. See [Scoping Questions](#scoping-questions) for clarification prompts.

**Step 2: Decompose into components and relationships**

Break system into atomic parts that can't be meaningfully subdivided further. Identify relationships (dependencies, data flow, control flow, temporal ordering). Choose decomposition strategy based on system type. See [Decomposition Strategies](#decomposition-strategies) and [resources/template.md](resources/template.md) for structured process.

**Step 3: Analyze component properties and interactions**

For each component, identify key properties (cost, time, complexity, reliability, etc.). Map interactions (which components depend on which). Identify critical paths, bottlenecks, or vulnerable points. For complex analysis → See [resources/methodology.md](resources/methodology.md) for dependency mapping and critical path techniques.

**Step 4: Reconstruct for insight or optimization**

Based on goal, either: (a) Identify critical components (bottleneck, single point of failure, highest cost driver), (b) Redesign configuration (reorder, parallelize, eliminate, combine components), or (c) Simplify (remove unnecessary components). See [Reconstruction Patterns](#reconstruction-patterns) for common approaches.

**Step 5: Validate and deliver recommendations**

Self-assess using [resources/evaluators/rubric_decomposition_reconstruction.json](resources/evaluators/rubric_decomposition_reconstruction.json) (minimum score ≥ 3.5). Present decomposition-reconstruction.md with clear component breakdown, analysis findings (bottlenecks, dependencies), and actionable recommendations with expected impact.

## Scoping Questions

**To define the system:**
- What is the system we're analyzing? (Be specific: "checkout flow" not "website")
- Where does it start and end? (Boundaries)
- What's in scope vs out of scope? (Prevents endless decomposition)

**To clarify the goal:**
- What problem are we solving? (Slow performance, high cost, complexity, unreliability)
- What would success look like? (Specific target: "reduce latency to <500ms", "cut costs by 30%")
- Are we optimizing, understanding, or redesigning?

**To understand constraints:**
- What can't we change? (Legacy systems, budget limits, regulatory requirements)
- What's the time horizon? (Quick wins vs long-term redesign)
- Who are the stakeholders? (Engineering, business, customers)

## Decomposition Strategies

Choose based on system type:

### Functional Decomposition
**When:** Business processes, software features, workflows
**Approach:** Break down by function or task
**Example:** E-commerce checkout → Browse products | Add to cart | Enter shipping | Payment | Confirmation

### Structural Decomposition
**When:** Architecture, organizations, physical systems
**Approach:** Break down by component or module
**Example:** Web app → Frontend (React) | API (Node.js) | Database (PostgreSQL) | Cache (Redis)

### Data Flow Decomposition
**When:** Pipelines, ETL processes, information systems
**Approach:** Break down by data transformations
**Example:** Analytics pipeline → Ingest raw events | Clean & validate | Aggregate metrics | Store in warehouse | Visualize in dashboard

### Temporal Decomposition
**When:** Processes with sequential stages, timelines, user journeys
**Approach:** Break down by time or sequence
**Example:** Customer onboarding → Day 1: Signup | Day 2-7: Tutorial | Day 8-30: First value moment | Day 31+: Retention

### Cost/Resource Decomposition
**When:** Budget analysis, resource allocation, optimization
**Approach:** Break down by cost center or resource type
**Example:** AWS bill → Compute ($5K) | Storage ($2K) | Data transfer ($1K) | Other ($500)

**Depth guideline:** Stop decomposing when further breakdown doesn't reveal useful insights or actionable opportunities.

## Component Relationship Types

After decomposition, map relationships:

**1. Dependency (A requires B):**
- API service depends on database
- Frontend depends on API
- Critical for: Identifying cascading failures, understanding change impact

**2. Data flow (A sends data to B):**
- User input → Validation → Database → API response
- Critical for: Tracing information, finding transformation bottlenecks

**3. Control flow (A triggers B):**
- Button click triggers form submission
- Payment success triggers order fulfillment
- Critical for: Understanding execution paths, identifying race conditions

**4. Temporal ordering (A before B in time):**
- Authentication before authorization
- Compile before deploy
- Critical for: Sequencing, finding parallelization opportunities

**5. Resource sharing (A and B compete for C):**
- Multiple services share database connection pool
- Teams share budget
- Critical for: Identifying contention, resource constraints

## Reconstruction Patterns

### Pattern 1: Bottleneck Identification
**Goal:** Find what limits system throughput or speed
**Approach:** Measure component properties (time, cost, capacity), identify critical path or highest value
**Example:** DB query takes 80% of request time → Optimize DB query first

### Pattern 2: Simplification
**Goal:** Reduce complexity by removing unnecessary parts
**Approach:** Question necessity of each component, eliminate redundant or low-value parts
**Example:** Workflow has 5 approval steps, 3 are redundant → Remove 3 steps

### Pattern 3: Reordering
**Goal:** Improve efficiency by changing sequence
**Approach:** Identify dependencies, move independent tasks earlier or parallel
**Example:** Run tests parallel to build instead of sequential → Reduce CI time

### Pattern 4: Parallelization
**Goal:** Increase throughput by doing work concurrently
**Approach:** Find independent components, execute simultaneously
**Example:** Fetch user data and product data in parallel instead of serial → Cut latency in half

### Pattern 5: Substitution
**Goal:** Replace weak component with better alternative
**Approach:** Identify underperforming component, find replacement
**Example:** Replace synchronous API call with async message queue → Improve reliability

### Pattern 6: Consolidation
**Goal:** Reduce overhead by combining similar components
**Approach:** Find redundant or overlapping components, merge them
**Example:** Consolidate 3 microservices doing similar work into 1 → Reduce operational overhead

### Pattern 7: Modularization
**Goal:** Improve maintainability by separating concerns
**Approach:** Identify tightly coupled components, separate with clear interfaces
**Example:** Extract auth logic from monolith into separate service → Enable independent scaling

## When NOT to Use This Skill

**Skip decomposition-reconstruction if:**
- System is already simple (3-5 obvious components, no complex interactions)
- Problem is not about system structure (purely execution issue, not design issue)
- You need creativity/ideation (not analysis) - use brainstorming instead
- System is poorly understood (need discovery/research first, not decomposition)
- Changes are impossible (no point analyzing if you can't act on findings)

**Use instead:**
- Simple system → Direct analysis or observation
- Execution problem → Project management, process improvement
- Need ideas → Brainstorming, design thinking
- Unknown system → Discovery interviews, research
- Unchangeable → Workaround planning, constraint optimization

## Common Patterns by Domain

**Software Architecture:**
- Decompose: Modules, services, layers, data stores
- Reconstruct for: Microservices migration, performance optimization, reducing coupling

**Business Processes:**
- Decompose: Steps, decision points, handoffs, approvals
- Reconstruct for: Cycle time reduction, automation opportunities, removing waste

**Problem Solving:**
- Decompose: Sub-problems, dependencies, unknowns, constraints
- Reconstruct for: Task sequencing, identifying blockers, finding parallelizable work

**Cost Optimization:**
- Decompose: Cost centers, line items, resource usage
- Reconstruct for: Identifying biggest cost drivers, finding quick wins

**User Experience:**
- Decompose: User journey stages, interactions, pain points
- Reconstruct for: Simplifying flows, removing friction, improving conversion

**System Reliability:**
- Decompose: Components, failure modes, dependencies
- Reconstruct for: Identifying single points of failure, improving resilience

## Quick Reference

**Process:**
1. Define system and goal → Set boundaries
2. Decompose → Break into components and relationships
3. Analyze → Measure properties, map interactions
4. Reconstruct → Optimize, simplify, or redesign
5. Validate → Check against rubric, deliver recommendations

**Decomposition strategies:**
- Functional (by task), Structural (by component), Data flow, Temporal, Cost/Resource

**Reconstruction patterns:**
- Bottleneck ID, Simplification, Reordering, Parallelization, Substitution, Consolidation, Modularization

**Resources:**
- [resources/template.md](resources/template.md) - Structured decomposition process with templates
- [resources/methodology.md](resources/methodology.md) - Advanced techniques (dependency graphs, critical path analysis, hierarchical decomposition)
- [resources/evaluators/rubric_decomposition_reconstruction.json](resources/evaluators/rubric_decomposition_reconstruction.json) - Quality checklist

**Deliverable:** `decomposition-reconstruction.md` with component breakdown, analysis, and recommendations
