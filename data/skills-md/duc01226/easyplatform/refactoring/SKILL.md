---
name: refactoring
description: Use when restructuring code without changing behavior - extract method, extract class, rename, move, inline, introduce parameter object. Triggers on keywords like "extract", "rename", "move method", "inline", "restructure", "decompose".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
infer: true
---

# Code Refactoring

Expert code restructuring agent for EasyPlatform. Focuses on structural changes that improve code quality without modifying behavior.

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files before starting. Do NOT skip.**

- **⚠️ MUST READ** `references/code-smells-catalog.md` — patterns, examples, BEM/SCSS standards
- **⚠️ MUST READ** `docs/claude/clean-code-rules.md` — clean code rules

## Workflow

### Phase 1: Analysis

1. **Identify Target**: Locate code to refactor
2. **Map Dependencies**: Find all usages with Grep
3. **Assess Impact**: List affected files and tests
4. **Verify Tests**: Ensure test coverage exists

### Phase 2: Plan

```markdown
## Refactoring Plan

**Target**: [file:line_number]
**Type**: [Extract Method | Move to Extension | etc.]
**Reason**: [Why this refactoring improves code]

### Changes
1. [ ] Create/modify [file]
2. [ ] Update usages in [files]
3. [ ] Run tests

### Risks
- [Potential issues]
```

### Phase 3: Execute

Apply the refactoring pattern from the catalog. Key platform patterns:

| Pattern            | When                       | Target                            |
| ------------------ | -------------------------- | --------------------------------- |
| Extract Expression | Complex inline logic       | Entity static expression          |
| Move to Extension  | Reusable repo queries      | `{Entity}RepositoryExtensions`    |
| Move to DTO        | Mapping in handler         | `PlatformEntityDto.MapToEntity()` |
| Move to Entity     | Business logic in handler  | Instance method or static expr    |
| Handler to Helper  | Reused cross-handler logic | Helper class with DI              |

### Phase 4: Verify

1. Run affected tests
2. Verify no behavior change
3. Check code compiles
4. Review for consistency

## Code Responsibility Check (CRITICAL)

**Before any refactoring, verify logic is in the LOWEST appropriate layer:**

```
Entity/Model (Lowest)  ->  Service  ->  Component/Handler (Highest)
```

| Wrong Location | Move To        | Example                               |
| -------------- | -------------- | ------------------------------------- |
| Component      | Entity/Model   | Dropdown options, display helpers     |
| Component      | Service        | Command building, data transformation |
| Handler        | Entity         | Business rules, static expressions    |
| Handler        | Repository Ext | Reusable query patterns               |

## Safety Checklist

- [ ] Searched all usages (static + dynamic)?
- [ ] Test coverage exists?
- [ ] Documented in todo list?
- [ ] Changes are incremental?
- [ ] No behavior change verified?

## Anti-Patterns

- **Big Bang Refactoring**: Make small, incremental changes
- **Refactoring Without Tests**: Ensure coverage first
- **Mixing Refactoring with Features**: Do one or the other
- **Breaking Public APIs**: Maintain backward compatibility
- **Logic in Wrong Layer**: Move to lowest appropriate layer


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
