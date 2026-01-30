---
name: platonic-code-review
description: Review code implementation against specifications to ensure consistency and completeness. Use when validating that code correctly implements RFC specs, requirements documents, or design specifications. Generates reports by default without modifying code.
license: MIT
metadata:
  version: "1.0.0"
  author: "caesar0301"
  category: "validation"
---

# Platonic Code Review

Validate that code implementation is consistent with project specifications and requirements.

## When to Use This Skill

Use this skill when you need to:

- **Verify** code implementation matches RFC specifications
- **Validate** feature completeness against requirements
- **Check consistency** between specs and actual code
- **Identify gaps** where specs exist but implementation is missing
- **Find discrepancies** where code behavior differs from specs
- **Audit compliance** with documented design decisions

Keywords: spec compliance, implementation validation, requirement verification, consistency check, gap analysis

## What This Skill Does

This is NOT a general code quality reviewer. It specifically focuses on:

✅ **Spec-to-Code Consistency**: Does the code implement what the specs describe?  
✅ **Completeness**: Are all specified features implemented?  
✅ **Correctness**: Does the implementation match spec requirements?  
✅ **Gap Identification**: What's specified but not implemented?  
✅ **Discrepancy Detection**: Where does code differ from specs?

## Default Behavior

**By Default**: Generates review report **without modifying code**

- Creates detailed report of findings
- Highlights inconsistencies and gaps
- Provides actionable recommendations
- Does NOT make code changes automatically

**To Modify Code**: User must explicitly request code modifications

## Review Procedure

The standard review process follows these steps:

### Step 1: Understand Specifications

- Locate and read relevant specification documents
  - RFC documents (rfc-*.md)
  - Requirements documents
  - Design documents
  - API specifications
- Extract key requirements and expected behaviors
- Identify testable criteria

### Step 2: Generate Functionality Checklist

Create a comprehensive checklist from specs:
- List all specified features
- List all specified behaviors
- List all API endpoints/interfaces
- List all data structures
- List all business rules
- List all constraints and validations

### Step 3: Map Specs to Code

Identify code locations implementing each spec:
- Find relevant files and modules
- Map features to implementation
- Identify entry points and key functions
- Understand code structure

### Step 4: Review Implementation Against Specs

For each checklist item:
- **Status**: ✅ Implemented / ⚠️ Partial / ❌ Missing / 🔍 Unclear
- **Consistency**: Does implementation match spec?
- **Completeness**: Are all aspects implemented?
- **Correctness**: Does it work as specified?
- **Evidence**: Specific code references

### Step 5: Identify Discrepancies

Document inconsistencies:
- **Implementation differs** from spec
- **Missing features** specified but not implemented
- **Extra features** implemented but not specified
- **Incorrect behavior** doesn't match spec requirements
- **Incomplete implementation** partially done

### Step 6: Generate Review Report

Create structured report with:
- Executive summary
- Functionality checklist with status
- Detailed findings (consistent, inconsistent, missing)
- Code references for each finding
- Prioritized recommendations
- Suggested actions (ask user before implementing)

## Extended Review Capabilities

Beyond the basic procedure, this skill can:

### Validation Levels

**Level 1: Basic Compliance**
- Check if major features are implemented
- Verify core functionality exists

**Level 2: Detailed Verification**
- Validate all specified behaviors
- Check edge cases and error handling
- Verify data structures and interfaces

**Level 3: Comprehensive Audit**
- Deep dive into implementation details
- Compare algorithms and approaches
- Validate performance requirements
- Check all specified constraints

### Cross-Reference Analysis

- **Bi-directional Check**: 
  - Specs → Code (what's missing in code?)
  - Code → Specs (what's not documented?)
- **Dependency Validation**: 
  - Check if dependencies match specs
  - Verify integration points
- **Version Alignment**: 
  - Ensure code version matches spec version
  - Track changes across versions

### Test Coverage Integration

- Compare test cases with spec requirements
- Identify untested specified behaviors
- Suggest test scenarios based on specs
- Validate test coverage completeness

## Report Format

Reviews generate structured reports:

```markdown
# Spec-to-Code Review Report

## Summary
- Specifications Reviewed: X
- Code Modules Reviewed: Y
- Consistency Rate: Z%

## Checklist Summary
- ✅ Fully Implemented: A items
- ⚠️ Partially Implemented: B items
- ❌ Not Implemented: C items
- 🔍 Unclear/Needs Investigation: D items

## Critical Inconsistencies
[Items where code contradicts specs]

## Missing Implementations
[Specified features not found in code]

## Extra Implementations
[Code features not in specs]

## Recommendations
[Prioritized actions - ASK USER before modifying code]
```

## Usage Examples

### Example 1: Basic Spec Review

```
Use platonic-code-review to review the implementation of 
rfc-001-user-authentication.md in the src/auth/ directory.
Generate a report showing what's implemented and what's missing.
```

### Example 2: Comprehensive Module Review

```
Use platonic-code-review to conduct a comprehensive review 
of the entire API implementation against all RFCs in ./specs/.
Focus on API endpoints, data structures, and error handling.
```

### Example 3: Feature Completeness Check

```
Use platonic-code-review to verify that all features 
specified in rfc-005-payment-processing.md are fully 
implemented in src/payments/. Generate a detailed checklist.
```

### Example 4: Gap Analysis

```
Use platonic-code-review to perform a gap analysis between 
./specs/ and ./src/, identifying specifications without 
implementations and implementations without specifications.
```

## Important Notes

### Default: Report Only

⚠️ **This skill generates reports by default and does NOT modify code**

When inconsistencies are found:
1. Document the issue in the report
2. Provide specific code references
3. Explain the discrepancy
4. Recommend actions
5. **ASK USER** if they want code modifications

### When to Modify Code

Only modify code when user explicitly requests:
- "Fix the inconsistencies you found"
- "Update the code to match the specs"
- "Implement the missing features"

Otherwise, default to report generation only.

## Integration with Other Skills

Works well with:
- **platonic-code-specs**: Review code against RFCs managed by this skill
- **Documentation skills**: Generate docs from review findings
- **Testing skills**: Create tests for missing coverage

## Dependencies

- Read access to specification documents (RFCs, requirements, design docs)
- Read access to source code
- Understanding of project structure
- Write access only if user requests code modifications

## Best Practices

1. **Start with specs**: Always read and understand specs first
2. **Be thorough**: Check all specified requirements systematically
3. **Be specific**: Provide exact file names, line numbers, and code references
4. **Be objective**: Report facts, not opinions
5. **Prioritize findings**: Critical issues first, minor ones later
6. **Ask before modifying**: Never change code without user consent

See [references/REFERENCE.md](references/REFERENCE.md) for detailed review procedures and examples.
