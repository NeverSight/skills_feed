---
name: morphological-analysis-triz
description: Use when need systematic innovation through comprehensive solution space exploration, resolving technical contradictions (speed vs precision, strength vs weight, cost vs quality), generating novel product configurations, exploring all feasible design alternatives before prototyping, finding inventive solutions to engineering problems, identifying patent opportunities through parameter combinations, or when user mentions morphological analysis, Zwicky box, TRIZ, inventive principles, technical contradictions, systematic innovation, or design space exploration.
---

# Morphological Analysis & TRIZ

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Systematically explore solution spaces through morphological analysis (parameter-option matrices) and resolve technical contradictions using TRIZ inventive principles to generate novel, non-obvious solutions.

## When to Use

**Systematic Exploration:**
- Explore all feasible configurations before committing
- Generate comprehensive set of design alternatives
- Create product line variations across parameters
- Document complete solution space

**Innovation & Invention:**
- Find novel, non-obvious solutions
- Generate patentable innovations
- Discover synergies between features
- Break out of conventional thinking

**Resolving Contradictions:**
- Improve one parameter without worsening another
- Solve "impossible" trade-offs (faster AND cheaper)
- Apply proven inventive principles
- Resolve conflicts between requirements

**Engineering & Design:**
- Design new products/systems from scratch
- Optimize existing designs systematically
- Configure complex systems with many parameters

## What Is It

Two complementary methods:

**Morphological Analysis:** Decompose problem into parameters, identify options for each, systematically combine to explore solution space.
```
Parameters: Power (3 options) × Size (4 options) × Material (3 options) = 36 configurations
```

**TRIZ:** Resolve contradictions using 40 inventive principles. Example: "Improve speed → worsens precision" solved by Principle #1 (Segmentation): fast rough pass + slow precision pass.

## Workflow

Copy this checklist:

```
Morphological Analysis & TRIZ Progress:
- [ ] Step 1: Define problem and objectives
- [ ] Step 2: Choose method (MA, TRIZ, or both)
- [ ] Step 3: Build morphological box (if MA)
- [ ] Step 4: Identify contradictions (if TRIZ)
- [ ] Step 5: Apply TRIZ principles
- [ ] Step 6: Evaluate and select solutions
```

**Step 1: Define problem and objectives**

Clarify problem statement, key objectives, constraints (cost, size, time, materials), and success criteria.

**Step 2: Choose method**

- **Morphological Analysis:** 3-7 clear parameters, each with 2-5 options, goal is comprehensive exploration
- **TRIZ:** Clear contradiction (improving A worsens B), need inventive breakthrough
- **Both:** Complex system with parameters AND contradictions

**Step 3: Build morphological box (if using MA)**

1. Identify 3-7 independent parameters (changing one doesn't force another)
2. List 2-5 distinct options per parameter
3. Create parameter × option matrix

See [resources/template.md](resources/template.md) for structure.

**Step 4: Identify contradictions (if using TRIZ)**

State clearly:
- **Improving parameter:** What to increase?
- **Worsening parameter:** What degrades?
- Look up in TRIZ contradiction matrix

See [resources/template.md](resources/template.md) for 39 TRIZ parameters and contradiction matrix.

**Step 5: Apply TRIZ principles**

1. Review 3-4 principles recommended by matrix
2. Brainstorm applications of each principle
3. Generate solution concepts
4. Combine principles for stronger solutions

See [resources/template.md](resources/template.md) for all 40 principles.

For advanced techniques, see [resources/methodology.md](resources/methodology.md).

**Step 6: Evaluate and select**

**Morphological:** Identify promising combinations, eliminate infeasible, score on objectives, select top 3-5

**TRIZ:** Assess contradiction resolution, check side effects, estimate difficulty, select most promising

Use [resources/evaluators/rubric_morphological_analysis_triz.json](resources/evaluators/rubric_morphological_analysis_triz.json) for quality criteria.

## Common Patterns

### Typical Parameters (Examples)

**Physical Products:** Materials, power source, form factor, control interface, manufacturing method
**Software:** Architecture, data storage, UI, deployment, authentication
**Services:** Delivery channel, pricing model, timing, customization, support level
**Processes:** Automation level, batch size, quality control, scheduling, location

### Common Contradictions

| Improving ↑ | Worsens ↓ | Example TRIZ Principles |
|-------------|-----------|------------------------|
| Speed | Precision | Segmentation, Periodic action |
| Strength | Weight | Anti-weight, Composite materials |
| Reliability | Complexity | Segmentation, Beforehand cushioning |
| Functionality | Ease of use | Segmentation, Universality |
| Capacity | Size | Nesting, Another dimension |

**Full principles list:** See [resources/template.md](resources/template.md) for all 40.

### When to Combine MA + TRIZ

1. Build morphological box → Find promising configurations
2. Identify contradictions in top configurations
3. Apply TRIZ to resolve contradictions
4. Re-evaluate configurations with contradictions resolved

## Guardrails

**Morphological Analysis:**
- **Limit parameters:** 3-7 parameters (too few = incomplete, too many = explosion)
- **Ensure independence:** Changing one parameter shouldn't force changes in another
- **Manageable options:** 2-5 per parameter (practical range)
- **Don't enumerate all:** Focus on promising clusters

**TRIZ:**
- **Verify real contradiction:** Improving A truly worsens B (not just budget limit)
- **Adapt principles:** Use as metaphors, not literal prescriptions
- **Check new contradictions:** Solution may introduce new trade-offs
- **Combine principles:** Often need 2-3 together

**General:**
- Document rationale for parameters/options selected
- Iterate if first pass reveals missing dimensions
- Prototype top concepts - don't just analyze

## Quick Reference

**Resources:**
- `resources/template.md` - Morphological structure, TRIZ contradiction matrix, 40 principles
- `resources/methodology.md` - Advanced TRIZ (trends of evolution, substance-field, ARIZ algorithm)
- `resources/evaluators/rubric_morphological_analysis_triz.json` - Quality criteria

**Output:** `morphological-analysis-triz.md` with problem definition, morphological matrix (if used), contradictions, TRIZ principles applied, solution concepts, evaluation, selected solutions

**Success Criteria:**
- Parameters independent and essential (3-7 with 2-5 options each)
- Contradictions clearly stated (improving/worsening parameters)
- Multiple principles applied per contradiction
- Solutions are novel, feasible, address objectives
- Top 3-5 selected with rationale
- Score ≥ 3.5 on rubric

**Quick Decisions:**
- **Simple configuration?** → Morphological only
- **Clear contradiction?** → TRIZ only
- **Complex with trade-offs?** → Both methods
- **Unsure?** → Start TRIZ to identify contradictions, then build morphological box

**Common Mistakes:**
1. Too many parameters (>7 = explosion)
2. Dependent parameters (choosing A forces B)
3. Vague contradiction ("better vs cheaper" - be specific)
4. Literal TRIZ (principles are metaphors)
5. No evaluation (generate but don't filter)

**Examples:**

**Morphological (Portable Speaker):**
```
Power: Battery | Solar | Hybrid
Size: Pocket | Handheld | Tabletop
Audio: Mono | Stereo | Surround
Material: Plastic | Metal | Fabric
Control: Button | Touch | Voice | App
Result: 3×3×3×4×4 = 432 configs → Evaluate top 10
```

**TRIZ (Electric Vehicle Range):**
```
Contradiction: Increase range → worsens cost (battery expensive)
Principles: #6 (Universality - battery is structure), #35 (Parameter change - new chemistry)
Solution: Structural battery pack + high energy density cells
```

**Combined:**
```
Build morphological box for EV architecture → Top config has range/cost contradiction → Apply TRIZ Universality principle → Structural battery resolves both range and cost
```

---

**For detailed principle explanations, contradiction matrix, advanced techniques (substance-field analysis, ARIZ, trends of evolution), and software/service adaptation, see [resources/template.md](resources/template.md) and [resources/methodology.md](resources/methodology.md).**
