---
name: context-engineering-kit
description: Advanced context engineering techniques for AI agents. Token-efficient plugins improving output quality through structured reasoning, reflection loops, and multi-agent patterns.
original_source: https://github.com/NeoLabHQ/context-engineering-kit
author: NeoLabHQ
license: GPL-3.0
---

# Context Engineering Kit

A collection of advanced context engineering techniques and patterns designed to improve AI agent results while minimizing token consumption.

## When to Use This Skill

- Improving AI output quality systematically
- Reducing token usage in complex tasks
- Implementing structured reasoning patterns
- Multi-agent code review workflows
- Spec-driven development processes
- When standard prompting isn't enough

## Core Techniques

### 1. Reflexion Pattern
Feedback loops that improve output by 8-21% across tasks.

**How it works:**
```
1. Generate initial response
2. Self-evaluate against criteria
3. Identify improvement areas
4. Generate refined response
5. Repeat until quality threshold met
```

**Use when:**
- Writing complex code
- Creating documentation
- Solving multi-step problems

### 2. Spec-Driven Development
Based on GitHub Spec Kit and OpenSpec frameworks.

**Process:**
```markdown
# Specification Document

## Requirements
[Clear, testable requirements]

## Acceptance Criteria
[Specific success conditions]

## Constraints
[Limitations and boundaries]

## Examples
[Input/output pairs]
```

**Benefits:**
- Clearer requirements
- Testable outputs
- Reduced ambiguity

### 3. Subagent-Driven Development
Competitive generation with quality gates.

**Architecture:**
```
┌─────────────────────────┐
│   Orchestrator Agent    │
├─────────────────────────┤
│  ┌─────┐  ┌─────┐      │
│  │Gen 1│  │Gen 2│ ...  │
│  └─────┘  └─────┘      │
├─────────────────────────┤
│    Quality Gate Agent   │
└─────────────────────────┘
```

**Flow:**
1. Multiple agents generate solutions
2. Quality agent evaluates each
3. Best solution selected/merged
4. Iterative refinement

### 4. First Principles Framework (FPF)
Hypothesis-driven decision making.

**Structure:**
```
Observation → Hypothesis → Test → Conclusion
```

**Application:**
- Debugging complex issues
- Architecture decisions
- Technology selection

### 5. Kaizen (Continuous Improvement)
Systematic iterative enhancement.

**Cycle:**
```
Plan → Do → Check → Act → Repeat
```

## Plugin Categories

### Reasoning Enhancement
- **Reflexion**: Self-evaluation loops
- **Chain of Thought**: Step-by-step reasoning
- **Tree of Thoughts**: Branching exploration

### Code Quality
- **Multi-Agent Review**: Parallel code analysis
- **Security Audit**: Vulnerability detection
- **Performance Analysis**: Optimization suggestions

### Development Process
- **Spec-Driven**: Requirements-first approach
- **TDD Support**: Test-first workflows
- **Documentation**: Auto-generated docs

### Meta-Skills
- **Plugin Development**: Create new plugins
- **Workflow Composition**: Combine techniques
- **Performance Tuning**: Optimize patterns

## How to Use

### Basic: Reflexion Loop
```
Review my code with reflexion:

[paste code]

Requirements:
- Error handling
- Performance
- Readability
```

### Spec-Driven Task
```
Create a spec for: User authentication system

Then implement following the spec.
```

### Multi-Agent Review
```
Review this PR with multiple perspectives:
- Security focus
- Performance focus
- Maintainability focus

[paste code or PR link]
```

## Token Efficiency Tips

### 1. Structured Prompts
```markdown
## Context
[Brief, relevant context only]

## Task
[Clear, specific task]

## Output Format
[Expected structure]
```

### 2. Progressive Disclosure
- Start with essential info
- Add details only when needed
- Remove redundant context

### 3. Pattern Libraries
- Reuse proven patterns
- Reference by name
- Avoid repeated explanations

## Example: Complex Code Review

**Traditional approach** (~2000 tokens):
> Review this code for bugs, security issues, performance problems...

**Context-engineered approach** (~800 tokens):
```markdown
## Review: auth.py

### Focus Areas
1. Security (OWASP Top 10)
2. Error handling
3. SQL injection

### Output
- Issues: severity + line number
- Fixes: specific code suggestions

[code]
```

**Result:** Same quality, 60% fewer tokens.

## Best Practices

1. **Start Simple**: Add complexity only when needed
2. **Measure Impact**: Track quality improvements
3. **Iterate**: Refine patterns based on results
4. **Document**: Keep notes on what works
5. **Share**: Contribute successful patterns

## Integration

Works with:
- Claude Code
- Cursor
- VS Code + Continue
- Any LLM-based tool

## Creating Custom Patterns

```markdown
# Pattern: [Name]

## When to Use
[Trigger conditions]

## Process
[Step-by-step]

## Example
[Concrete example]

## Metrics
[How to measure success]
```
