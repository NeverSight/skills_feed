---
name: audit-prep-assistant
description: Prepare your codebase for security review using Trail of Bits' checklist. Helps set review goals, runs static analysis tools, increases test coverage, removes dead code, ensures accessibility, and generates comprehensive documentation (flowcharts, user stories, inline comments). (project, gitignored)
category: building-secure-contracts
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Audit Prep Assistant Skill

**Trit**: -1 (MINUS)
**Category**: building-secure-contracts
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Prepare your codebase for security review using Trail of Bits' checklist. Helps set review goals, runs static analysis tools, increases test coverage, removes dead code, ensures accessibility, and generates comprehensive documentation (flowcharts, user stories, inline comments). (project, gitignored)

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

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
audit-prep-assistant (○) + SDF.Ch1 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
