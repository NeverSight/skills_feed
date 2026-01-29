---
name: deep-research
description: >
  Exhaustive investigation with citations and structured findings. Use when thorough coverage
  is needed, all sources must be cited, or research will inform critical decisions. Triggers on:
  "use deep-research mode", "deep research", "exhaustive investigation", "thorough research",
  "cite all sources", "comprehensive analysis", "leave no stone unturned", "research everything".
  Read-only mode - investigates and documents but doesn't modify code.
---

# Deep-Research Mode

Exhaustive investigation with full citations and structured findings.

## Core Philosophy

> "Thorough beats fast. Citations beat claims. Structured beats stream-of-consciousness."

This mode is for when surface-level understanding isn't enough. You're building a complete, citable reference that others can verify.

## When to Use

- Research will inform critical decisions
- Findings need to be verifiable by others
- Coverage must be exhaustive (no gaps allowed)
- Multiple stakeholders need to review the research
- Building documentation that will outlive the session

## Output Structure

Every deep-research output must include:

### 1. Executive Summary

2-3 sentences covering:

- What was investigated
- Key finding (one sentence)
- Confidence level (High/Medium/Low)

### 2. Scope Definition

| Included              | Excluded                         |
| --------------------- | -------------------------------- |
| [What was researched] | [What was intentionally skipped] |

### 3. Findings

Each finding must have:

```markdown
#### Finding: [Title]

**Confidence:** High | Medium | Low

**Evidence:**

- [file.py#L42](file.py#L42) - [what this shows]
- [config.yaml#L15](config.yaml#L15) - [what this shows]

**Analysis:**
[Interpretation of the evidence]

**Implications:**
[What this means for the task at hand]
```

### 4. Coverage Report

| Area          | Files Checked | Confidence       |
| ------------- | ------------- | ---------------- |
| [Component A] | 12            | High             |
| [Component B] | 5             | Medium           |
| [Component C] | 0             | Not investigated |

### 5. Open Questions

- [ ] [Question that couldn't be answered with available information]
- [ ] [Area that needs human clarification]

## Research Techniques

### Breadth-First Scan

Before going deep, establish the landscape:

1. **File search** - Find all files matching patterns
2. **Grep for patterns** - Key terms, class names, function names
3. **Directory structure** - Understand organization
4. **Entry points** - Main files, index files, configs

### Depth-First Trace

For each important area:

1. **Start at entry point** - Where execution begins
2. **Follow all branches** - Don't skip conditionals
3. **Document dependencies** - What does this call/import?
4. **Note side effects** - File writes, API calls, state changes

### Cross-Reference

Connect findings across areas:

- Same pattern used differently in different places?
- Inconsistencies between documentation and code?
- Dead code paths?
- Hidden coupling between components?

## Citation Standards

### Always Cite

- Specific line numbers when referencing code
- File paths for configuration claims
- Test names when citing expected behavior
- Commit hashes for historical claims (if relevant)

### Citation Format

```markdown
[path/to/file.py#L42-L50](path/to/file.py#L42-L50) - Description
```

### Confidence Levels

| Level  | Meaning                               | Citation Requirement          |
| ------ | ------------------------------------- | ----------------------------- |
| High   | Verified in code, tests pass          | Direct code citation          |
| Medium | Inferred from patterns                | Multiple supporting citations |
| Low    | Speculation based on naming/structure | Clearly marked as inference   |

## Quality Checklist

Before completing research:

- [ ] All claims have citations
- [ ] Coverage report shows no critical gaps
- [ ] Confidence levels are assigned to each finding
- [ ] Open questions are explicitly listed
- [ ] Executive summary captures the essence
- [ ] Another agent could verify findings from citations

## Anti-Patterns

| ❌ Don't                     | ✅ Do                                                                   |
| ---------------------------- | ----------------------------------------------------------------------- |
| "The codebase uses React"    | "[package.json#L15](package.json#L15) lists react@18.2.0 as dependency" |
| "This probably handles auth" | "Auth handling uncertain - no direct evidence found (Low confidence)"   |
| "I looked at the files"      | "Examined 23 files in src/services/, found 4 relevant"                  |
| "Everything seems fine"      | "No issues found in [scope]. Coverage: [X] files, [Y] functions"        |

## Integration with Explore Agent

When spawned as a subagent from Explore:

1. Receive the investigation topic from parent
2. Perform exhaustive research using techniques above
3. Return structured findings in the output format
4. Parent agent incorporates summary, not full investigation trace
