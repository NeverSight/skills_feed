---
name: sdd-research
description: Pattern investigation and technical research before specification. Use when technical approach is unclear, exploring existing solutions, or analyzing codebase patterns.
---

# SDD Research Skill

Investigate codebase patterns and external solutions to inform specification and planning.

## When to Use

- Technical approach is unclear
- Need to understand existing patterns
- Evaluating solution options
- Before `/specify` or `/plan` commands
- When `sdd-explorer` findings need deeper analysis

## Research Protocol

### Phase 1: Codebase Analysis
1. **Existing patterns**: How similar problems are solved
2. **Reusable components**: What can be leveraged
3. **Conventions**: Naming, structure, architecture patterns
4. **Dependencies**: What libraries/frameworks are used

### Phase 2: External Solutions
1. **Best practices**: Industry standards for this problem
2. **Library options**: Available tools and their tradeoffs
3. **Architecture patterns**: Applicable design patterns
4. **Reference implementations**: Similar solutions elsewhere

### Phase 3: Synthesis
1. **Compare options**: Pros/cons matrix
2. **Recommend approach**: Based on findings
3. **Flag risks**: Technical concerns and unknowns
4. **Document assumptions**: What needs validation

## Research Output Format

```markdown
# Research: [Topic]

## Summary
[1-2 sentence overview of findings]

## Codebase Analysis

### Existing Patterns
| Pattern | Location | Relevance |
|---------|----------|-----------|
| [pattern] | [file/dir] | [how it applies] |

### Reusable Components
- [component]: [how to leverage]

### Conventions
- [convention type]: [standard used]

## External Solutions

### Option 1: [Name]
- **Pros**: [advantages]
- **Cons**: [disadvantages]
- **Effort**: [estimate]

### Option 2: [Name]
- **Pros**: [advantages]
- **Cons**: [disadvantages]
- **Effort**: [estimate]

## Comparison Matrix

| Criteria | Option 1 | Option 2 |
|----------|----------|----------|
| [criteria] | [score] | [score] |

## Recommendation
[Recommended approach with rationale]

## Risks & Unknowns
- [risk]: [mitigation]

## Next Steps
1. [action item]
```

## Reference Patterns

See `references/patterns.md` for common architectural patterns and when to use them.

## Integration

- Findings feed into `/specify` command
- Informs `sdd-planner` subagent decisions
- Can be invoked by `sdd-explorer` for deeper analysis
- Use the ask question tool when research reveals multiple valid approaches
