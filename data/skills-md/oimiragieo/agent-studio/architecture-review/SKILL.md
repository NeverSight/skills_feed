---
name: architecture-review
description: Architecture review and design validation. Evaluates system designs against best practices, identifies anti-patterns, and ensures architectural decisions align with non-functional requirements.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep]
best_practices:
  - Evaluate designs against SOLID principles
  - Check for anti-patterns and code smells
  - Verify non-functional requirements
  - Document architectural decisions
error_handling: graceful
streaming: supported
---

# Architecture Review Skill

<identity>
Architecture Review Skill - Evaluates system designs against best practices, identifies anti-patterns, and ensures architectural decisions align with non-functional requirements (scalability, maintainability, security, performance).
</identity>

<capabilities>
- Reviewing system architecture designs
- Identifying anti-patterns and architectural smells
- Validating against SOLID, DRY, YAGNI principles
- Assessing non-functional requirements
- Recommending architectural improvements
</capabilities>

<instructions>
<execution_process>

### Step 1: Gather Architecture Context

Understand the current architecture by:

1. **Read project structure**: Use Glob to map directory structure
2. **Identify key components**: Find entry points, services, data layers
3. **Review dependencies**: Check package.json, imports, module graph
4. **Understand data flow**: Trace requests through the system

### Step 2: Evaluate Design Principles

Check adherence to fundamental principles:

**SOLID Principles**:

- **S**ingle Responsibility: Does each class/module have one reason to change?
- **O**pen/Closed: Can behavior be extended without modification?
- **L**iskov Substitution: Are subtypes substitutable for base types?
- **I**nterface Segregation: Are interfaces focused and minimal?
- **D**ependency Inversion: Do high-level modules depend on abstractions?

**Other Principles**:

- **DRY**: Is logic duplicated unnecessarily?
- **YAGNI**: Are there unused or speculative features?
- **Separation of Concerns**: Are responsibilities properly divided?

### Step 3: Check for Anti-Patterns

Identify common anti-patterns:

- **God Class/Module**: Classes doing too much
- **Spaghetti Code**: Tangled, hard-to-follow logic
- **Circular Dependencies**: Modules that reference each other
- **Feature Envy**: Classes that use other classes' data excessively
- **Shotgun Surgery**: Changes that require touching many files
- **Leaky Abstractions**: Implementation details exposed to consumers

### Step 4: Assess Non-Functional Requirements

Evaluate against NFRs:

- **Scalability**: Can the system handle increased load?
- **Maintainability**: How easy is it to modify and extend?
- **Testability**: Can components be tested in isolation?
- **Security**: Are there potential vulnerabilities?
- **Performance**: Are there obvious bottlenecks?
- **Observability**: Can the system be monitored effectively?

### Step 5: Generate Review Report

Create a structured report with:

1. **Summary**: Overall assessment and key findings
2. **Strengths**: What the architecture does well
3. **Concerns**: Issues requiring attention (prioritized)
4. **Recommendations**: Specific improvements with rationale
5. **Trade-offs**: Acknowledge valid design trade-offs

</execution_process>

<best_practices>

1. **Be Constructive**: Focus on improvements, not criticism
2. **Prioritize Issues**: Not all problems are equally important
3. **Consider Context**: Understand constraints and trade-offs
4. **Suggest Alternatives**: Don't just identify problems
5. **Reference Patterns**: Cite established patterns when relevant

</best_practices>
</instructions>

<examples>
<usage_example>
**Example Review Request**:

```
Review the architecture of src/services/ for scalability and maintainability
```

**Example Response Structure**:

```markdown
## Architecture Review: src/services/

### Summary

The service layer follows a reasonable structure but has some coupling issues...

### Strengths

- Clear separation between API handlers and business logic
- Good use of dependency injection

### Concerns

1. **High Priority**: UserService has 15 methods (God Class)
2. **Medium Priority**: Circular dependency between OrderService and InventoryService
3. **Low Priority**: Some magic numbers in validation logic

### Recommendations

1. Split UserService into UserAuthService and UserProfileService
2. Introduce EventBus to decouple Order and Inventory
3. Extract validation constants to configuration
```

</usage_example>
</examples>

## Rules

- Always provide constructive feedback with actionable recommendations
- Prioritize issues by impact and effort to fix
- Consider existing constraints and trade-offs

## Related Workflow

This skill has a corresponding workflow for complex multi-agent scenarios:

- **Workflow**: `.claude/workflows/architecture-review-skill-workflow.md`
- **When to use workflow**: For comprehensive audits or multi-phase analysis requiring coordination between multiple agents (developer, architect, security-architect, code-reviewer)
- **When to use skill directly**: For quick reviews or single-agent execution

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
