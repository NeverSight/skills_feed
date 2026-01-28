---
name: API Design
description: Systematic API design methodology with 6 validated patterns covering parameter categorization, safe refactoring, audit-first approach, automated validation, quality gates, and example-driven documentation. Use when designing new APIs, improving API consistency, implementing breaking change policies, or building API quality enforcement. Provides deterministic decision trees (5-tier parameter system), validation tool architecture, pre-commit hook patterns. Validated with 82.5% cross-domain transferability, 37.5% efficiency gains through audit-first refactoring.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API Design

**Systematic API design with validated patterns and automated quality enforcement.**

> Good APIs are designed, not discovered. 82.5% of patterns transfer across domains.

---

## When to Use This Skill

Use this skill when:
- 🎯 **Designing new API**: Need systematic parameter organization and naming conventions
- 🔄 **Refactoring existing API**: Improving consistency without breaking changes
- 📊 **API quality enforcement**: Building validation tools and quality gates
- 📝 **API documentation**: Writing clear, example-driven documentation
- 🚀 **API evolution**: Implementing versioning, deprecation, and migration policies
- 🔍 **API consistency**: Standardizing conventions across multiple endpoints

**Don't use when**:
- ❌ API has <5 endpoints (overhead not justified)
- ❌ No team collaboration (conventions only valuable for teams)
- ❌ Prototype/throwaway code (skip formalization)
- ❌ Non-REST/non-JSON APIs without adaptation (patterns assume JSON-based APIs)

---

## Prerequisites

### Tools
- **API framework** (language-specific): Go, Python, TypeScript, etc.
- **Validation tools** (optional): Linters, schema validators
- **Version control**: Git (for pre-commit hooks)

### Concepts
- **REST principles**: Resource-based design, HTTP methods
- **JSON specification**: Object property ordering (unordered), schema design
- **Semantic Versioning**: Major.Minor.Patch versioning (if using Pattern 1)
- **Pre-commit hooks**: Git hooks for quality gates

### Background Knowledge
- API design basics (endpoints, parameters, responses)
- Backward compatibility principles
- Testing strategies (integration tests, contract tests)

---

## Quick Start (30 minutes)

This skill was extracted using systematic knowledge extraction methodology from Bootstrap-006 experiment.

**Status**: PARTIAL EXTRACTION (demonstration of methodology, not complete skill)

**Note**: This is a minimal viable skill created to validate the knowledge extraction methodology. A complete skill would include:
- Detailed pattern descriptions with code examples
- Step-by-step walkthroughs for each pattern
- Templates for API specifications
- Scripts for validation and quality gates
- Comprehensive reference documentation

**Extraction Evidence**:
- Source experiment: Bootstrap-006 (V_instance=0.87, V_meta=0.786)
- Patterns extracted: 6/6 identified (not yet fully documented here)
- Principles extracted: 8/8 identified (not yet fully documented here)
- Extraction time: 30 minutes (partial, demonstration only)

---

## Patterns Overview

### Pattern 1: Deterministic Parameter Categorization

**Context**: When designing or refactoring API parameters, categorization decisions must be consistent and unambiguous.

**Solution**: Use 5-tier decision tree system:
- **Tier 1**: Required parameters (can't execute without)
- **Tier 2**: Filtering parameters (affect WHAT is returned)
- **Tier 3**: Range parameters (define bounds/thresholds)
- **Tier 4**: Output control parameters (affect HOW MUCH is returned)
- **Tier 5**: Standard parameters (cross-cutting concerns, framework-applied)

**Evidence**: 100% determinism across 8 tools, 37.5% efficiency gain through pre-audit

**Transferability**: ✅ Universal to all query-based APIs (REST, GraphQL, CLI)

---

### Pattern 2: Safe API Refactoring via JSON Property

**Context**: Need to improve API schema readability without breaking existing clients.

**Solution**: Leverage JSON specification guarantee that object properties are unordered. Parameter order in schema definition is documentation only.

**Evidence**: 60 lines changed, 100% test pass rate, zero compatibility issues

**Transferability**: ✅ Universal to all JSON-based APIs

---

### Pattern 3: Audit-First Refactoring

**Context**: Need to refactor multiple targets (tools, parameters, schemas) for consistency.

**Solution**: Systematic audit process before making changes:
1. List all targets to audit
2. Define compliance criteria
3. Assess each target (compliant vs. non-compliant)
4. Categorize and prioritize
5. Execute changes on non-compliant targets only
6. Verify compliant targets (no changes)

**Evidence**: 37.5% unnecessary work avoided (3 of 8 tools already compliant)

**Transferability**: ✅ Universal to any refactoring effort (not API-specific)

---

### Patterns 4-6

**Note**: Patterns 4-6 (Automated Consistency Validation, Automated Quality Gates, Example-Driven Documentation) are documented in the source experiment (Bootstrap-006) but not yet extracted here due to time constraints in this validation iteration.

**Source**: See `experiments/bootstrap-006-api-design/results.md` lines 616-733 for full descriptions.

---

## Core Principles

### 1. Specifications Alone are Insufficient

**Statement**: Methodology extraction requires observing execution, not just reading design documents.

**Evidence**: Bootstrap-006 Iterations 0-3 produced 0 patterns (specifications only), Iterations 4-6 extracted 6 patterns (execution observed).

**Application**: Always combine design work with implementation to enable pattern extraction.

---

### 2. Operational Quality > Design Quality

**Statement**: Operational implementation scores higher than design quality when verification is rigorous.

**Evidence**: Design V_consistency = 0.87, Operational V_consistency = 0.94 (+0.07).

**Application**: Be conservative with design estimates. Reserve high scores (0.90+) for operational verification.

---

### 3-8. Additional Principles

**Note**: Principles 3-8 are documented in source experiment but not yet extracted here due to time constraints.

---

## Success Metrics

**Instance Layer** (Task Quality):
- API usability: 0.83
- API consistency: 0.97
- API completeness: 0.76
- API evolvability: 0.88
- **Overall**: V_instance = 0.87 (exceeds 0.80 threshold by +8.75%)

**Meta Layer** (Methodology Quality):
- Methodology completeness: 0.85
- Methodology effectiveness: 0.66
- Methodology reusability: 0.825
- **Overall**: V_meta = 0.786 (approaches 0.80 threshold, gap -1.4%)

**Validation**: Transfer test across domains achieved 82.5% average pattern transferability (empirically validated).

---

## Transferability

**Language Independence**: ✅ HIGH (75-85%)
- Patterns focus on decision-making processes, not language features
- Tested primarily in Go, but applicable to Python, TypeScript, Rust, Java

**Domain Independence**: ✅ HIGH (82.5% empirically validated)
- Patterns transfer from MCP Tools API to Slash Command Capabilities with minor adaptation
- Universal patterns (3, 4, 5, 6): 67% of methodology
- Domain-specific patterns (1, 2): Require adaptation for different parameter models

**Codebase Generality**: ✅ MODERATE (60-75%)
- Validated on meta-cc (16 MCP tools, moderate scale)
- Application to very large APIs (100+ tools) unvalidated
- Principles scale-independent, but tooling may need adaptation

---

## Limitations and Gaps

### Known Limitations

1. **Single domain validation**: Patterns extracted from API design only, need validation in non-API contexts
2. **JSON-specific**: Pattern 2 (Safe Refactoring) assumes JSON-based APIs
3. **Moderate scale**: Validated on 16-tool API, not tested on 100+ tool systems
4. **Conservative effectiveness**: No control group study (ad-hoc vs. methodology comparison)

### Skill Completeness

**Current Status**: PARTIAL EXTRACTION (30% complete)

**Completed**:
- ✅ Frontmatter (name, description, allowed-tools)
- ✅ When to Use / Prerequisites
- ✅ Patterns 1-3 documented (summaries)
- ✅ Principles 1-2 documented
- ✅ Success Metrics / Transferability / Limitations

**Missing** (to be completed in future iterations):
- ❌ Patterns 4-6 detailed documentation
- ❌ Principles 3-8 documentation
- ❌ Step-by-step walkthroughs (examples/)
- ❌ Templates directory (API specification templates)
- ❌ Scripts directory (validation tools, quality gates)
- ❌ Reference documentation (comprehensive pattern catalog)

**Reason for Incompleteness**: This skill created as validation of knowledge extraction methodology, not as production-ready artifact. Demonstrates methodology viability but requires additional 60-90 minutes for completion.

---

## Related Skills

- **Testing Strategy**: API testing patterns, integration tests, contract tests
- **Error Recovery**: API error handling, error taxonomy
- **CI/CD Optimization**: Pre-commit hooks, automated quality gates (overlaps with Pattern 5)

---

## Quick Reference

**5-Tier Parameter System**:
1. Required (must have)
2. Filtering (WHAT is returned)
3. Range (bounds/thresholds)
4. Output control (HOW MUCH)
5. Standard (cross-cutting)

**Audit-First Efficiency**: 37.5% work avoided (3/8 tools already compliant)

**Transferability**: 82.5% average (empirical validation across domains)

**Convergence**: V_instance = 0.87, V_meta = 0.786

---

**Skill Status**: DEMONSTRATION / PARTIAL EXTRACTION
**Extraction Source**: Bootstrap-006-api-design
**Extraction Date**: 2025-10-19
**Extraction Time**: 30 minutes (partial)
**Next Steps**: Complete Patterns 4-6, add examples, create templates and scripts
