---
name: sc-explain
description: Provide clear explanations of code, concepts, or system behavior. Use when user asks to explain code, understand behavior, or learn concepts.
---

# Code and Concept Explanation

Deliver clear, comprehensive explanations of code functionality, concepts, or system behavior.

## When to use

- User asks to explain code or function
- System behavior understanding needed
- Concept or pattern explanation requested
- Learning or educational context
- Code walkthrough or tutorial needed

## Instructions

### Usage

```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|diagram|examples]
```

### Arguments

- `target` - Code file, function, concept, or system to explain
- `--level` - Explanation complexity (basic, intermediate, advanced)
- `--format` - Output format (text, diagram, examples)
- `--context` - Additional context for explanation

### Execution

1. Analyze target code or concept thoroughly
2. Identify key components and relationships
3. Structure explanation based on complexity level
4. Provide relevant examples and use cases
5. Present clear, accessible explanation with proper formatting

### Claude Code Integration

- Uses Read for comprehensive code analysis
- Leverages Grep for pattern identification
- Applies Bash for runtime behavior analysis
- Maintains clear, educational communication style
