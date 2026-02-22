---
name: optimize-md
description: Optimizes markdown documents for token efficiency, clarity, and LLM consumption. Use when (1) a markdown file needs streamlining for use as LLM context, (2) reducing token count in documentation without losing meaning, (3) converting verbose docs into concise reference material, (4) improving structure and scannability of markdown files, or (5) preparing best-practices or knowledge docs for agent consumption.
argument-hint: "<file path to markdown file>"
---

# Document Optimizer

Read, optimize, and rewrite markdown documents for token efficiency, structural clarity, and LLM parseability. The target file is provided as a file path argument.

## Workflow

1. **Read** the file at `$ARGUMENTS`. If no path is provided, ask for one
2. **Analyze** the document for optimization opportunities using the principles below
3. **Rewrite** the file in place with all optimizations applied
4. **Verify** the rewritten document preserves all factual content and meaning from the original
5. **Report** using this format:

> Original: [N] lines → Optimized: [N] lines ([N]% reduction)
> Changes: [comma-separated list of key changes]

## Optimization Principles

### Token Economics

Evaluate each sentence for token value. Remove content that restates common knowledge, repeats itself, or adds no actionable value.

Remove decorative language. No "please note", "it's worth mentioning", "remember that", "importantly".

Eliminate filler transitions. "Additionally", "furthermore", "in other words", "as mentioned above".

Remove hedging. "Consider", "try to", "when possible", "generally speaking", "it depends".

### Structural Optimization

| Technique | Apply When |
|-----------|------------|
| Convert prose to tables | Comparing options, listing attributes, or mapping inputs to outputs |
| Convert prose to lists | Content contains discrete, parallel, independent items |
| Keep prose | Explaining relationships, conditional logic, or rationale |
| Merge sections | Multiple sections cover the same concept |
| Remove sections | Content restates framework docs or common knowledge |

Flatten unnecessary nesting. Collapse single-item subsections into their parent.

Place critical information first within each section. Most important content at the top.

End sections decisively. No trailing "etc.", "and so on", or "and more".

### Sentence Compression

Remove filler words and passive voice:
- Before: "It is recommended that you should make sure to always validate user input"
- After: "Validate user input at API boundaries"

Combine related statements:
- Before: "Use TypeScript for all new files. Make sure to add type annotations. Enable strict mode in tsconfig."
- After: "Use TypeScript strict mode with explicit type annotations for all new files"

Remove redundant qualifiers:
- Before: "This is a very important and critical step that must always be done"
- After: "Required step"

### Content Filtering

#### Remove Entirely

- Welcome messages, introductions, background history
- Motivational statements ("This will help you write better code!")
- Content the model already knows (framework basics, language syntax)
- Hypothetical future scenarios ("If we ever migrate to...")
- Time-sensitive references without dates
- Redundant examples that demonstrate the same concept

#### Preserve

- Domain-specific knowledge the model lacks
- Concrete examples demonstrating non-obvious patterns
- Decision criteria and trade-off analysis
- Exact commands, configs, and code snippets
- Constraints and prohibited actions

### Formatting Cleanup

Use language-labeled code blocks. Never use unlabeled fences.

Use consistent heading hierarchy. No skipped levels (h2 -> h4).

Remove excessive emphasis. Bold only for hard constraints where violation causes failure. Limit to 10% of content.

Use one blank line between sections. Remove consecutive blank lines.

Standardize list markers within each list (all `-` or all `*`, not mixed).

### Terminology Consistency

Identify synonyms used for the same concept. Choose the most precise term and use it throughout.

- Before: alternating "endpoint", "route", "URL", "path" for the same concept
- After: consistently "endpoint" throughout

## Constraints

- **Preserve all factual content and meaning.** Compression must not alter semantics
- **Preserve code blocks verbatim** unless they contain obvious errors
- **Preserve document title** (h1 heading). Rephrase for concision only if verbose
- **Do not add new content.** Optimization removes and restructures; it does not invent
- **Do not add commentary or annotations** to the output file
- Write the optimized document directly to the source file

## Scope Boundaries

Do not use for:
- Non-markdown files
- Documents requiring content creation or expansion
- Files already optimized by a previous run
- Code files or config files with markdown comments
