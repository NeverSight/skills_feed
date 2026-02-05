---
name: fp-rater
description: |
  Automatically rates functional programming adherence after editing or creating code files. Use when: (1) A code file has been edited or created, (2) The file contains programming logic (JavaScript/TypeScript, Python, etc.). Output a minimalist rating table showing FP score out of 10.
---

# Functional Programming Rating

After editing or creating a code file, output a minimalist rating of its adherence to functional programming principles.

## When to Rate

Rate files containing programming logic after:
- Creating new code files
- Editing existing code files

Do NOT rate:
- Configuration files (JSON, YAML, etc.)
- Markup files (HTML, CSS, Markdown, .md files)
- Data files
- Documentation files

## Rating Criteria

Evaluate the file against these 7 principles (score out of 10):

1. **PURITY** - Pure functions (same inputs → same outputs, no side effects)
2. **IMMUTABILITY** - No mutations (use spread operators, return new values)
3. **EXPLICIT DEPENDENCIES** - Dependencies as parameters, not globals
4. **EFFECTS AT EDGES** - I/O and side effects at boundaries, not mixed with logic
5. **ERRORS AS VALUES** - Result/Either types instead of exceptions for expected failures
6. **DECLARATIVE STYLE** - map/filter/reduce over imperative loops
7. **COMPOSITION** - Small, focused, composable functions

## Scoring Guidelines

- **9-10**: Exemplary FP - follows nearly all principles
- **7-8**: Strong FP - follows most principles with minor violations
- **5-6**: Mixed approach - some FP patterns, some imperative
- **3-4**: Mostly imperative - minimal FP adherence
- **1-2**: Non-functional - direct violations of most principles

## Output Format

After completing file edits, append this exact table format at the bottom of your response:

```
Allegiance to Functional Programming
┌─────────────────────────┬───────┐
│ File                    │ Score │
├─────────────────────────┼───────┤
│ filename.ext            │ X/10  │
└─────────────────────────┴───────┘
```

Replace `filename.ext` with the actual file name and X with the numeric score. Include ONLY this table - no explanations, no breakdown, no additional commentary.

## Example

After editing `userService.ts`, append:

```
Allegiance to Functional Programming
┌─────────────────────────┬───────┐
│ File                    │ Score │
├─────────────────────────┼───────┤
│ userService.ts          │ 7/10  │
└─────────────────────────┴───────┘
```
