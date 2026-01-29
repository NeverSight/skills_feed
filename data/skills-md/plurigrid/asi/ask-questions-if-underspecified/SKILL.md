---
name: ask-questions-if-underspecified
description: Clarify requirements before implementing. Use when serious doubts araise.
category: ask-questions-if-underspecified
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Ask Questions If Underspecified Skill

**Trit**: -1 (MINUS)
**Category**: ask-questions-if-underspecified
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Clarify requirements before implementing. Use when serious doubts araise.

## When to Use

This is a Trail of Bits security skill. Refer to the original repository for detailed usage guidelines and examples.

See: https://github.com/trailofbits/skills

## Related Skills

- audit-context-building
- codeql
- semgrep
- variant-analysis


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
ask-questions-if-underspecified (−) + SDF.Ch4 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
