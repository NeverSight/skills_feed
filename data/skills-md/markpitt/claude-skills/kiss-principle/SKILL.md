---
name: kiss-principle
description: Apply the K.I.S.S principle (Keep It Simple, Stupid) to reduce complexity, improve maintainability, and solve problems elegantly. Use when designing systems, writing code, planning solutions, creating documentation, architecting features, or making decisions where simplicity drives quality and efficiency.
version: 1.0
---

# K.I.S.S Principle Orchestration Skill

This skill helps you apply the K.I.S.S principle—"Keep It Simple, Stupid"—to systematically reduce unnecessary complexity while maintaining functionality and effectiveness. Simplicity is not about removing necessary features; it's about eliminating unnecessary complications.

## Quick Reference: When to Load Which Resource

| Your Situation | Load Resource | Why |
|---|---|---|
| Need to understand KISS fundamentals and why simplicity matters | `resources/kiss-fundamentals.md` | Learn core concepts, history, and empirical benefits |
| Reviewing code, design, or system for unnecessary complexity | `resources/complexity-analysis.md` | Identify complexity sources, anti-patterns, red flags |
| Want proven strategies to simplify solutions | `resources/simplification-strategies.md` | Learn 10+ actionable techniques with software/UX examples |
| Building or designing something new with KISS in mind | `resources/kiss-driven-design.md` | Apply KISS during design, architecture, feature planning |
| Comparing simple vs complex approaches | `resources/decision-frameworks.md` | Use frameworks to evaluate tradeoffs, make smart choices |
| Seeing worked examples of effective simplification | `resources/case-studies.md` | Real cases: code refactoring, API design, UX improvements |

## Core Principle

**Simplicity is the ultimate sophistication.** — Leonardo da Vinci

The K.I.S.S principle states that most systems work better when kept simple rather than made complex. Unnecessary complexity:
- Increases bugs and maintenance burden
- Makes systems harder to understand and modify
- Reduces performance and reliability
- Wastes development time and resources
- Creates cognitive overload for users and developers

**The Goal:** Solve problems with the minimum necessary complexity while preserving correctness and user value.

## Orchestration Protocol

### Phase 1: Assess Your Situation

Quickly identify what you're simplifying and why:

**Context Type:**
- **Code Review/Refactoring**: Existing code has unnecessary complexity → Load complexity-analysis.md
- **Feature Design**: Planning new functionality → Load kiss-driven-design.md
- **Architecture/System Design**: Building infrastructure or large systems → Load simplification-strategies.md
- **Problem-Solving**: Finding solution to technical challenge → Load decision-frameworks.md
- **UX/Documentation**: Improving clarity and usability → Load simplification-strategies.md
- **Learning**: Understanding KISS principles → Load kiss-fundamentals.md

**Complexity Level:**
- **Light**: Minor improvements, small scope → Use simplification-strategies.md directly
- **Medium**: Significant redesign needed, moderate scope → Use complexity-analysis.md + decision-frameworks.md
- **Heavy**: Major architectural changes, system-wide complexity → Use all resources systematically

**Action:** Load appropriate resource file(s) based on situation.

### Phase 2: Analyze and Plan

Based on context, follow these steps:

| Step | What to Do | Resource |
|---|---|---|
| **1. Identify complexity** | What makes this complex? What's unnecessary? | complexity-analysis.md |
| **2. Understand tradeoffs** | What are we gaining/losing with each approach? | decision-frameworks.md |
| **3. Select strategies** | Which simplification techniques apply here? | simplification-strategies.md |
| **4. Design simply** | How would we design this with KISS in mind? | kiss-driven-design.md |
| **5. Verify value** | Does the simple solution meet requirements? | decision-frameworks.md |
| **6. Reference examples** | How have others solved this simply? | case-studies.md |

### Phase 3: Execution & Validation

**Before Simplifying:**
- Preserve core functionality and requirements
- Document why current complexity exists
- Identify what stakeholders actually need vs. want
- Create rollback plan if needed

**During Simplification:**
1. Remove one layer of complexity at a time
2. Verify functionality after each change
3. Measure improvement (LOC, cyclomatic complexity, performance)
4. Document decisions and rationale

**After Simplification:**
- Test thoroughly (more bugs often hide in complexity)
- Gather feedback from team and users
- Monitor performance and stability
- Document simpler approach for future reference

## Complexity Assessment Framework

Quickly evaluate if something is too complex:

**Red Flags - This is Too Complex:**
- ❌ You can't explain it in 2-3 sentences
- ❌ It requires extensive documentation to understand
- ❌ New team members struggle to modify it for weeks
- ❌ It has many interdependencies and side effects
- ❌ Performance problems correlate with feature addition
- ❌ Bugs consistently appear in this component
- ❌ It has deeply nested conditionals (>3 levels)
- ❌ Multiple abstractions on top of each other
- ❌ Over-engineered for current and foreseeable needs

**Green Flags - This is Appropriately Simple:**
- ✅ You can explain it clearly in 1-2 minutes
- ✅ New developers understand it quickly
- ✅ It does one thing well (single responsibility)
- ✅ Dependencies are explicit and minimal
- ✅ It's stable with few bugs
- ✅ Code is readable and self-documenting
- ✅ It serves current needs without speculation

## KISS vs Over-Engineering

| Aspect | KISS | Over-Engineering |
|---|---|---|
| **Scope** | Solves current problem | Anticipates future needs |
| **Code** | ~100-200 LOC | ~500+ LOC |
| **Time to Ship** | 1-2 weeks | 4-8+ weeks |
| **Maintenance** | Easy to modify | Complex to change |
| **Performance** | Good enough | Highly optimized |
| **Bugs** | Few, obvious | Many, hidden |
| **Approach** | Add complexity when needed | Remove complexity as possible |

## Key Principles to Remember

1. **Necessity Test**: Does every component, line, and feature serve a current user need?
2. **Clarity First**: Clear code beats clever code
3. **Single Responsibility**: Each function/module does one thing well
4. **Minimal Dependencies**: Fewer connections = fewer failure points
5. **Explicit Better Than Implicit**: Code should be obvious, not magical
6. **Measure Before Optimizing**: Don't optimize prematurely
7. **Refactor Incrementally**: Simplify gradually, test continuously

## Common Complexity Anti-Patterns

See `resources/complexity-analysis.md` for detailed analysis of:
- Over-abstraction (too many layers)
- Premature optimization (optimizing before profiling)
- Gold plating (adding nice-to-haves)
- Speculative generalization (over-generalizing)
- Feature creep (scope expansion)
- Accidental complexity vs essential complexity
- Technical debt accumulation

## Simplification Strategies

See `resources/simplification-strategies.md` for 10+ proven techniques:
- Constraint-based design
- Default assumptions
- Removing features
- Consolidating logic
- Flattening architecture
- Eliminating abstractions
- Standardizing approaches
- And more...

## Resource Files Summary

### `resources/kiss-fundamentals.md`
Foundation and philosophy:
- KISS principle definition and history
- Why simplicity matters (empirical evidence)
- Simplicity vs complexity tradeoffs
- Principles of effective simplification
- Common misconceptions

### `resources/complexity-analysis.md`
Identifying and understanding complexity:
- Complexity sources and types
- Measuring complexity (cyclomatic, LOC, coupling)
- Identifying unnecessary complexity
- Recognizing over-engineering
- Red flags and anti-patterns

### `resources/simplification-strategies.md`
Actionable techniques for simplifying:
- 10+ proven simplification strategies
- When to apply each strategy
- Code examples in multiple languages
- UX simplification approaches
- Architecture simplification patterns

### `resources/kiss-driven-design.md`
Applying KISS from the start:
- Designing for simplicity
- Requirements gathering with KISS in mind
- Architecture patterns that promote simplicity
- Feature design principles
- Documentation and communication

### `resources/decision-frameworks.md`
Making trade-off decisions:
- Simple vs Complex evaluation framework
- When complexity is justified
- Cost-benefit analysis for features
- Decision trees for architectural choices
- Measuring ROI of simplification

### `resources/case-studies.md`
Real-world examples of successful simplification:
- Code refactoring case studies
- API design simplifications
- Architecture improvements
- UX improvements through simplification
- Decision-making examples

## How This Skill Works

1. **Assess your situation**: What are you simplifying and why?
2. **Analyze complexity**: Identify unnecessary complication
3. **Select approach**: Choose relevant strategies and frameworks
4. **Plan simplification**: Design the simpler solution
5. **Execute carefully**: Make changes incrementally, test continuously
6. **Validate**: Confirm the simple solution meets all needs
7. **Learn**: Reference cases and patterns for future decisions

## Quick Start: 5-Minute Simplification Check

1. Can you explain this in 2 sentences? (If no → too complex)
2. What would the simplest possible version look like?
3. What complexity is essential? What's optional?
4. Could you remove one component without breaking functionality?
5. What would new developers struggle with?

## Templates & Checklists

- **Complexity Assessment Checklist** in `resources/complexity-analysis.md`
- **Simplification Planning Template** in `resources/simplification-strategies.md`
- **Decision Framework Template** in `resources/decision-frameworks.md`
- **Design Checklist** in `resources/kiss-driven-design.md`

## Common Scenarios

**Scenario 1: Code Review**
→ Load `complexity-analysis.md` → identify issues → Load `simplification-strategies.md` → suggest improvements

**Scenario 2: Feature Design**
→ Load `kiss-fundamentals.md` → Load `kiss-driven-design.md` → plan with simplicity in mind

**Scenario 3: Architecture Redesign**
→ Load `complexity-analysis.md` → assess current state → Load `decision-frameworks.md` → evaluate tradeoffs → Load `simplification-strategies.md` → plan improvements

**Scenario 4: Learning from Examples**
→ Load `case-studies.md` → study approaches → Load `decision-frameworks.md` → understand tradeoffs

## Next Steps

1. Identify what you're working on (code, design, system, decision)
2. Load appropriate resource from table above
3. Assess complexity and identify problem areas
4. Select simplification strategies or design approaches
5. Plan and execute changes incrementally
6. Validate that simple version meets all requirements
7. Document decisions for team learning

---

**Remember**: The goal is solving the problem correctly with minimum necessary complexity. Simplicity requires discipline—resist the urge to over-engineer, and refactor ruthlessly to remove unnecessary complication.

*"Everything should be as simple as it is, but not simpler." — Albert Einstein*
