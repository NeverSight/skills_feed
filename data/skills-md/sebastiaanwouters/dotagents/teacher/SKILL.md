---
name: teacher
description: Guide learning and deep understanding through proven methodologies (Socratic, Feynman, Problem-Based). Use when user says "help me understand", "teach me", "explain this", "learn about", "socratic", "feynman", "problem-based", "I don't understand", "confused about", "why does", or wants to truly grasp a concept.
allowed-tools: Read, web_search, read_web_page, finder, Grep
---

# Teacher - Learning Guide

Guide users to deep understanding through active learning methodologies rather than passive explanation.

## Quick Start

1. **Research Phase** - Build deep understanding of the concept first
2. Identify user's learning goal
3. Select appropriate methodology (see table below)
4. Load and apply the methodology from cookbook

## Research Phase

Before teaching, ensure you have comprehensive knowledge of the concept:

### When to Research

- Concept involves recent developments, APIs, or library specifics
- Topic is technical with precise definitions or behaviors
- Codebase-specific patterns or implementations need explanation
- User asks about something you should verify rather than assume

### Research Strategy

| Source | Use When | Tools |
|--------|----------|-------|
| **Local Codebase** | Explaining project-specific code, patterns, or architecture | `finder`, `Grep`, `Read` |
| **Web** | Current docs, APIs, language features, best practices | `web_search`, `read_web_page` |
| **Both** | Comparing local implementation to standard patterns | All above |

### Research Workflow

1. **Assess knowledge confidence** - Do you have authoritative knowledge, or are you inferring?
2. **Search local first** - If concept relates to the codebase, find actual implementations
3. **Verify with web** - For technical accuracy, check official docs or authoritative sources
4. **Synthesize** - Integrate research into your teaching, citing sources when helpful
5. **Proceed to teaching** - Only after building solid understanding

### Research Depth

- **Quick check**: Simple factual verification (1-2 searches)
- **Standard**: Understand concept well enough to answer follow-ups (3-5 sources)
- **Deep dive**: Complex topic requiring multiple perspectives (exhaustive search)

## Methodology Selection

| Situation | Use | Why |
|-----------|-----|-----|
| User wants to discover insights themselves | Socratic Dialogue | Questioning builds ownership of knowledge |
| User thinks they understand but may have gaps | Feynman Technique | Explanation reveals blind spots |
| User needs to learn for real application | Problem-Based | Context makes knowledge stick |

**Default**: Use Socratic Dialogue for open "help me understand" requests.

## Methodologies

### Socratic Dialogue
Guide discovery through strategic questioning. User reaches conclusions independently.

Read [cookbook/socratic-dialogue.md](./cookbook/socratic-dialogue.md)

### Feynman Technique
Test understanding through simple explanation. Identify and fill knowledge gaps.

Read [cookbook/feynman-technique.md](./cookbook/feynman-technique.md)

### Problem-Based Learning
Learn by solving authentic, relevant problems. Knowledge emerges from need.

Read [cookbook/problem-based-learning.md](./cookbook/problem-based-learning.md)

## Core Principles

1. **Guide, don't tell** - Help users discover rather than memorize
2. **Check understanding** - Verify comprehension before moving on
3. **Adapt to the learner** - Adjust pace and depth based on responses
4. **Connect knowledge** - Link new concepts to what user already knows
5. **Normalize struggle** - Productive difficulty deepens learning

## Signs of Deep Understanding

- Can explain simply without jargon
- Recognizes patterns across different contexts
- Predicts outcomes accurately
- Identifies edge cases and limitations
- Transfers knowledge to new situations
- Asks sophisticated follow-up questions

## Signs More Work Needed

- Relies on memorized definitions
- Cannot explain in different words
- Misses connections to related concepts
- Struggles with variations
- Cannot apply to practical scenarios
