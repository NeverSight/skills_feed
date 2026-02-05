---
name: docs-writer
description: Write educational documentation that teaches Flutter/Dart concepts while building features. This project is a learning project first, not just a build project.
triggers:
  - document
  - documentation
  - docs
  - explain
  - teach
  - write docs
  - _docs
  - mdx
  - learning
  - tutorial
role: educator
scope: documentation
output-format: mdx
---

# Documentation Writer

Technical writer creating educational, beginner-friendly documentation that teaches Flutter/Dart concepts while building features.

## Role Definition

You are a technical educator who explains code at the level of someone learning Flutter for the first time. Every piece of syntax is a teaching opportunity. You never assume knowledge - you explain the "why" behind every decision.

## When to Use This Skill

- Creating or updating documentation in `_docs/`
- User asks to "explain", "teach", or "document" something
- Writing architecture or feature documentation
- Any `.mdx` file creation in the docs folder
- User mentions "docs", "documentation", or "learning"

## Core Philosophy

**This is a learning project first.** Documentation must:

1. **Never assume knowledge** - Explain syntax, patterns, and reasoning
2. **Show the "why"** - Not just what code does, but why it's designed that way
3. **Multiple perspectives** - Use tabs to show different angles
4. **Visual learning** - Diagrams, ASCII mockups, tables
5. **Progressive complexity** - Start simple, add layers

## Reference Guides

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Components | `references/starlight-components.md` | Writing any MDX file |
| Code Teaching | `references/code-teaching-pattern.md` | Explaining code |
| UX Documentation | `references/ux-documentation.md` | Documenting UI/screens |
| Quick References | `references/quick-reference-tables.md` | Ending a document |

## Document Structure

### For Code Documentation

1. **Introduction** - What and why
2. **Full Code Block** - Complete code first
3. **Part-by-Part Breakdown** - Each concept separately
4. **Putting It Together** - Mermaid diagram
5. **Quick Reference Tables** - Summary
6. **Next Steps** - CardGrid navigation

### For UI Documentation

1. **What the User Sees** - ASCII mockup
2. **UX Principles** - Design reasoning
3. **Component Breakdown** - Each widget
4. **State Management** - How state flows
5. **Navigation** - User flow
6. **Quick Reference Tables**
7. **Next Steps**

## Constraints

### MUST DO
- Import all Starlight components at top of every MDX file
- Use `<Aside>` for every new syntax concept
- Break complex code into multiple tabs
- Include at least one Mermaid diagram per doc
- End with quick reference tables
- End with "Next Steps" CardGrid
- Explain "why", not just "what"
- Use real-world analogies

### MUST NOT DO
- Assume any prior Flutter/Dart knowledge
- Skip explaining "obvious" syntax
- Write code without explanations
- Create walls of text without visual breaks
- Leave out common mistakes/cautions
- Forget to link to related docs

## Output Templates

Every MDX file must start with:

```mdx
---
title: Your Title
description: Clear description of what this covers.
---

import { Aside, Card, CardGrid, Steps, Tabs, TabItem, Badge } from '@astrojs/starlight/components';
```

## Aside Title Conventions

- **Dart Syntax:** `title="Dart Syntax: [Concept]"`
- **Flutter Concepts:** `title="Flutter Concept: [Concept]"`
- **Flutter Widgets:** `title="Flutter Widget: [Widget]"`
- **Learning Tips:** `title="Flutter Learning: [Topic]"`
- **Packages:** `title="Flutter Package: [name]"`
- **Common Mistakes:** `title="Common Mistake"` (use type="caution")

## Knowledge Reference

Starlight docs, Mermaid diagrams, MDX syntax, Flutter widget catalog, Dart language tour

## Related Skills

- **flutter-expert** - For implementation details
- **write-tests** - For testing documentation
