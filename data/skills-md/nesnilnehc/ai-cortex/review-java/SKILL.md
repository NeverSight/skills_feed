---
name: review-java
description: "Review Java code for language and runtime conventions: concurrency, exceptions, try-with-resources, API versioning, collections and Streams, NIO, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Java

## Purpose

Review code in **Java** for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on concurrency and thread safety, exceptions and try-with-resources, API and version compatibility, collections and Streams, NIO and proper closing, modules (JPMS) where relevant, and testability.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for Java projects.
- **Java-only review**: When the user wants only language/runtime conventions checked.
- **Pre-PR Java checklist**: Ensure concurrency, resource management, and API compatibility are correct.

**When to use**: When the code under review is Java and the task includes language/runtime quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Java language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-Java files for Java rules unless explicitly in scope.

### Review checklist (Java dimension only)

1. **Concurrency and thread safety**: Correct use of synchronized, volatile, locks, or concurrent APIs; visibility and happens-before; shared mutable state; executor usage and shutdown.
2. **Exceptions and resources**: try-with-resources for Closeable/AutoCloseable; exception handling and suppression; avoiding empty catch or overly broad catch.
3. **API and version compatibility**: Public API stability; backward compatibility; use of deprecated APIs and migration path; module boundaries (JPMS) if applicable.
4. **Collections and Streams**: Appropriate use of Stream API; side effects in streams; allocation and boxing; immutable collections where appropriate.
5. **NIO and closing**: Proper closing of streams, channels, and selectors; avoid resource leaks; use try-with-resources.
6. **Testability**: Dependency injection; static and singleton usage; overridable vs final; test doubles and mocking.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided Java code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-java**.

---

## Restrictions

- **Do not** perform security, architecture, or scope selection. Stay within Java language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-Java code for Java-specific rules unless explicitly in scope.

---

## Self-Check

- [ ] Was only the Java language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are concurrency, exceptions, resources, collections/Streams, NIO, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-java, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

---

## Examples

### Example 1: Resource and exception

- **Input**: Java method that opens an InputStream and does not use try-with-resources.
- **Expected**: Emit a finding for resource management; suggest try-with-resources. Category = language-java.

### Example 2: Concurrency

- **Input**: Shared mutable list accessed from multiple threads without synchronization or concurrent collection.
- **Expected**: Emit finding(s) for thread safety (e.g. use CopyOnWriteArrayList or synchronize); reference the field and usage. Category = language-java.

### Edge case: Mixed Java and SQL

- **Input**: File with JDBC or JPA and Java logic.
- **Expected**: Review only Java conventions (resources, exceptions, concurrency). Do not emit SQL-injection findings here; that is for review-security or review-sql.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-java`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/main/java/com/example/Loader.java:45`
- **Category**: language-java
- **Severity**: major
- **Title**: InputStream not closed in all paths
- **Description**: Leak possible if an exception is thrown before close.
- **Suggestion**: Use try-with-resources for the InputStream.
```
