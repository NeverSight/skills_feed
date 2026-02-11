---
name: review-dotnet
description: "Review .NET (C#/F#) code for language and runtime conventions: async/await, nullable, API versioning, IDisposable, LINQ, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review .NET

## Purpose

Review code in the **.NET** ecosystem (C#, F#) for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on async/await and ConfigureAwait, nullable reference types and NRE avoidance, API and versioning, resources and IDisposable, collections and LINQ, and testability.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for .NET projects.
- **.NET-only review**: When the user wants only language/runtime conventions checked (e.g. after adding a new C# file).
- **Pre-PR .NET checklist**: Ensure async, nullable, and resource patterns are correct.

**When to use**: When the code under review is .NET (C#/F#) and the task includes language/runtime quality. Scope (diff vs paths) is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: .NET language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection (diff vs codebase), security review, or architecture review; do not review non-.NET files unless asked to ignore language.

### Review checklist (.NET dimension only)

1. **async/await and ConfigureAwait**: Correct use of async; ConfigureAwait(false) where appropriate (library code); cancellation token propagation; avoid async void except event handlers.
2. **Nullable reference types and NRE**: Nullable annotations; null checks and null-forgiving where justified; avoid unnecessary null-forgiving.
3. **API and versioning**: Public API surface stability; breaking changes; versioning or deprecation strategy for libraries.
4. **Resources and IDisposable**: Proper use of IDisposable, using statements, and IAsyncDisposable; no leaking handles or streams.
5. **Collections and LINQ**: Appropriate use of LINQ; allocation and enumeration; avoid multiple enumeration; span/memory where relevant.
6. **Testability**: Dependency injection and testability; static usage; sealed/overridable where it affects testing.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided .NET code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-dotnet**.

---

## Restrictions

- **Do not** perform security, architecture, or scope selection. Stay within .NET language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-.NET code for .NET-specific rules unless the user explicitly includes it (e.g. embedded scripts).

---

## Self-Check

- [ ] Was only the .NET language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are async, nullable, IDisposable, LINQ, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-dotnet, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

---

## Examples

### Example 1: Async method

- **Input**: C# method that is async and calls other async methods without passing CancellationToken.
- **Expected**: Emit a finding (e.g. minor/suggestion) for CancellationToken propagation; reference the method and parameter list. Category = language-dotnet.

### Example 2: Nullable and disposal

- **Input**: C# class that holds an IDisposable and does not implement IDisposable or use using.
- **Expected**: Emit finding(s) for resource disposal and possibly nullable if the field can be null. Category = language-dotnet.

### Edge case: Mixed C# and SQL

- **Input**: File with C# and embedded SQL strings.
- **Expected**: Review only the C# parts for .NET conventions (e.g. async, nullable, disposal). Do not emit SQL-injection findings; that is for review-security or review-sql.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-dotnet`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/Services/DataLoader.cs:22`
- **Category**: language-dotnet
- **Severity**: minor
- **Title**: Async method does not accept or forward CancellationToken
- **Description**: Long-running or cancellable operations should support cancellation.
- **Suggestion**: Add CancellationToken parameter and pass it to underlying async calls.
```
