---
name: address-sanitizer
description: Use AddressSanitizer to detect memory safety bugs in C/C++ programs. Identifies use-after-free, buffer overflow, memory leaks, and other memory errors.
category: testing-handbook-skills
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Address Sanitizer Skill

**Trit**: -1 (MINUS)
**Category**: testing-handbook-skills
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Use AddressSanitizer to detect memory safety bugs in C/C++ programs. Identifies use-after-free, buffer overflow, memory leaks, and other memory errors.

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

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
address-sanitizer (○) + SDF.Ch5 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
