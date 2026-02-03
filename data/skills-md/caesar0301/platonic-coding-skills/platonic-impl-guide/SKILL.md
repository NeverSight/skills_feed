---
name: platonic-impl-guide
description: Create and manage implementation guides that translate RFC specifications into concrete, project-specific implementation designs. Implementation guides are language-aware, framework-aware, and MUST NOT contradict RFC specs. Use when planning implementation of RFC specifications, creating detailed technical designs, or documenting implementation architecture.
license: MIT
metadata:
  version: "1.0.0"
  author: "Xiaming Chen"
  category: "implementation"
---

# Platonic Implementation Guide

Create concrete, project-specific implementation designs from RFC specifications.

## When to Use This Skill

Use this skill when you need to:

- **Translate** RFC specifications into implementation-ready designs
- **Create** detailed technical architecture for a feature
- **Document** language-specific and framework-specific implementation decisions
- **Plan** module structure, dependencies, and data flow
- **Bridge** the gap between abstract specs and concrete code

Keywords: implementation guide, technical design, architecture, RFC implementation, module design

## What This Skill Does

This skill creates **Implementation Guides** that:

✅ **Supersede RFC Specs**: Provide concrete details while NEVER contradicting specs  
✅ **Language-Aware**: Include language-specific idioms, patterns, and best practices  
✅ **Framework-Aware**: Leverage framework capabilities and conventions  
✅ **Project-Specific**: Align with existing codebase architecture and patterns  
✅ **Actionable**: Provide clear module structure, types, and interfaces

## Core Principles

### 1. Spec Compliance (Non-Negotiable)

Implementation guides **MUST NOT** contradict RFC specifications:

- All invariants from specs must be preserved
- All required behaviors must be implemented
- All constraints must be respected
- If a spec is unclear, document the interpretation

### 2. Concrete Over Abstract

Unlike RFCs which define "what", implementation guides define "how":

- Specific module/crate/package structure
- Concrete type definitions with fields
- Actual function signatures
- Real dependency relationships
- Specific storage formats and schemas

### 3. Language and Framework Awareness

Implementation guides are technology-specific:

- Use idiomatic patterns for the target language
- Leverage framework conventions and capabilities
- Follow project-established coding standards
- Reference actual libraries and dependencies

### 4. Traceability

Every implementation decision should trace back to specs:

- Reference source RFCs explicitly
- Document which spec requirements each component satisfies
- Explain deviations or interpretations

## Implementation Guide Structure

An implementation guide follows this structure:

```markdown
# [Feature] Implementation Architecture

> Implementation guide for [feature] in [project].
> 
> **Crate/Module**: `module-name`
> **Source**: Derived from RFC-NNNN (Title)
> **Related RFCs**: RFC-XXXX, RFC-YYYY

---

## 1. Overview
[High-level summary of what this implements and why]

## 2. Architectural Position
[Where this fits in the overall system]
- Data flow diagram
- Dependency graph
- Crate/module responsibilities

## 3. Module Structure
[Concrete directory and file layout]

## 4. Core Types
[Actual type definitions with fields and documentation]

## 5. Key Interfaces/Traits
[API surface with function signatures]

## 6. Implementation Details
[Specific algorithms, storage formats, protocols]

## 7. Error Handling
[Error types and handling strategies]

## 8. Configuration
[Configuration options and defaults]

## 9. Testing Strategy
[How to test this implementation]

## 10. Migration/Compatibility
[If applicable, how to migrate from existing systems]
```

## Available Operations

| Operation | Reference File | Purpose |
|-----------|----------------|---------|
| **Create Guide** | `create-guide.md` | Create new implementation guide from RFC |
| **Validate Guide** | `validate-guide.md` | Check guide against RFC for contradictions |
| **Update Guide** | `update-guide.md` | Update guide when RFC changes |

See [references/REFERENCE.md](references/REFERENCE.md) for detailed operation guides.

## Templates

Templates are provided in `assets/`:

- `impl-guide-template.md` - Full implementation guide template

## Usage Examples

### Example 1: Create Implementation Guide

```
Use platonic-impl-guide to create an implementation guide for 
RFC-0042 (Message Queue Protocol) targeting the acme-queue crate.
The implementation should use Rust with async/await patterns.
```

### Example 2: Validate Existing Guide

```
Use platonic-impl-guide to validate that references/queue_impl.md
does not contradict RFC-0042 specifications.
```

### Example 3: Update Guide After RFC Change

```
Use platonic-impl-guide to update the implementation guide
after RFC-0042 was revised to add new message priority levels.
```

## Best Practices

1. **Read the RFC first**: Understand the specification completely before designing implementation
2. **Check existing patterns**: Look at how similar features are implemented in the project
3. **Document decisions**: Explain why specific implementation choices were made
4. **Keep it current**: Update guides when RFCs or implementations change
5. **Be specific**: Vague guides are not useful; include actual types and signatures
6. **Test coverage**: Include testing strategy in the guide

## Relationship to Other Artifacts

```
RFC Specification (abstract, what)
        ↓
Implementation Guide (concrete, how)  ← This skill
        ↓
Actual Code (executable)
        ↓
Tests (verification)
```

## Dependencies

- Read access to RFC specifications
- Understanding of target language and framework
- Knowledge of project architecture and conventions
- Write access to references/ or designated impl-guide directory
