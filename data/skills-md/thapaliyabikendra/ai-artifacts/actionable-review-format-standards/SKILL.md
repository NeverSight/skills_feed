---
name: actionable-review-format-standards
description: "Standardized output format for code reviews with severity labels, file:line references, and fix code snippets. Use when generating review reports that need consistent, actionable feedback structure."
layer: 1
tech_stack: [dotnet, csharp, typescript, react]
topics: [code-review, output-format, severity, feedback, pull-requests]
depends_on: []
complements: [code-review-excellence]
keywords: [CRITICAL, HIGH, MEDIUM, LOW, severity, file-path, line-number, fix, suggestion, blocking]
---

# Actionable Review Format Standards

Standardized output format for code reviews ensuring consistent, actionable, and prioritized feedback across all reviewer agents.

## When to Use This Skill

- Generating code review reports
- Formatting PR feedback
- Creating security audit reports
- Producing performance review outputs
- Any review output requiring severity classification

## Core Principles

1. **Every issue has a severity** - Never leave findings unclassified
2. **Every issue has a location** - Always include `file:line` references
3. **Every blocking issue has a fix** - Provide code snippets for Critical/High
4. **Summary before details** - Lead with counts and verdicts
5. **Categorize by concern** - Group Security, Performance, Patterns separately

---

## Severity Classification

### Severity Levels

| Level | Icon | Criteria | Action Required |
|-------|------|----------|-----------------|
| **CRITICAL** | 🔴 | Security vulnerabilities, data loss risk, system crashes | Must fix before merge |
| **HIGH** | 🟠 | Significant bugs, missing authorization, performance blockers | Should fix before merge |
| **MEDIUM** | 🟡 | Code quality issues, minor bugs, missing validation | Fix soon, not blocking |
| **LOW** | 🟢 | Style issues, minor improvements, suggestions | Nice to have |
| **INFO** | 💡 | Educational comments, alternative approaches | No action required |

### Severity Decision Tree

```
Is it a security vulnerability?
├── Yes → CRITICAL
└── No → Can it cause data loss or corruption?
         ├── Yes → CRITICAL
         └── No → Can it cause system crash/downtime?
                  ├── Yes → HIGH
                  └── No → Does it break functionality?
                           ├── Yes → HIGH
                           └── No → Does it affect performance significantly?
                                    ├── Yes → MEDIUM
                                    └── No → Is it a code quality issue?
                                             ├── Yes → MEDIUM/LOW
                                             └── No → LOW/INFO
```

### Severity Examples

```markdown
🔴 CRITICAL - Security
- SQL injection vulnerability
- Missing authorization on delete endpoint
- Hardcoded credentials in source code
- PII exposure in logs

🟠 HIGH - Must Fix
- Missing null checks causing NullReferenceException
- N+1 query in frequently called method
- Business logic error causing wrong calculations
- Missing input validation on public API

🟡 MEDIUM - Should Fix
- Blocking async call (.Result, .Wait())
- Missing error handling
- Inefficient LINQ query
- Duplicate code that should be extracted

🟢 LOW - Nice to Have
- Variable naming improvements
- Missing XML documentation
- Code formatting inconsistencies
- Minor refactoring opportunities

💡 INFO - Educational
- Alternative pattern suggestion
- Performance optimization tip
- Best practice recommendation
```

---

## Location Format

### Standard Format

```
{FilePath}:{LineNumber}
```

### Examples

```markdown
✅ Good:
- `src/Application/PatientAppService.cs:45`
- `src/Domain/Patient.cs:23-28` (range)
- `src/Application/Validators/CreatePatientDtoValidator.cs:12`

❌ Bad:
- `PatientAppService.cs` (missing path)
- `line 45` (missing file)
- `src/Application/` (missing file and line)
```

### Multi-Location Issues

When an issue spans multiple files:

```markdown
**[MEDIUM]** Duplicate validation logic
- `src/Application/PatientAppService.cs:45`
- `src/Application/DoctorAppService.cs:52`
- `src/Application/AppointmentAppService.cs:38`

**Suggestion**: Extract to shared `ValidationHelper` class.
```

---

## Issue Format

### Single Issue Template

```markdown
**[{SEVERITY}]** `{file:line}` - {Category}

{Brief description of the issue}

**Problem**:
```{language}
// Current code
{problematic code}
```

**Fix**:
```{language}
// Suggested fix
{corrected code}
```

**Why**: {Explanation of impact/risk}
```

### Compact Issue Format (for tables)

```markdown
| Severity | Location | Category | Issue | Fix |
|----------|----------|----------|-------|-----|
| 🔴 CRITICAL | `File.cs:42` | Security | Missing `[Authorize]` | Add `[Authorize(Permissions.Delete)]` |
| 🟠 HIGH | `File.cs:67` | Performance | N+1 query in loop | Use `.Include()` or batch query |
```

---

## Report Structure

### Full Review Report Template

```markdown
# Code Review: {PR Title}

**Date**: {YYYY-MM-DD}
**Reviewer**: {agent-name}
**Files Reviewed**: {count}
**Lines Changed**: +{added} / -{removed}

---

## Verdict

{✅ APPROVE | 💬 APPROVE WITH COMMENTS | 🔄 REQUEST CHANGES}

**Summary**: {1-2 sentence overview}

---

## Issue Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| 🔴 CRITICAL | {n} | Yes |
| 🟠 HIGH | {n} | Yes |
| 🟡 MEDIUM | {n} | No |
| 🟢 LOW | {n} | No |

---

## 🔴 Critical Issues

{If none: "No critical issues found."}

### [CRITICAL] `{file:line}` - {Title}

{Description}

**Problem**:
```{lang}
{code}
```

**Fix**:
```{lang}
{code}
```

---

## 🟠 High Issues

{Issues in same format}

---

## 🟡 Medium Issues

{Issues in same format or table format for brevity}

---

## 🟢 Low Issues / Suggestions

- **`{file:line}`** [nit]: {suggestion}
- **`{file:line}`** [style]: {suggestion}

---

## 🔒 Security Summary

| Check | Status | Notes |
|-------|--------|-------|
| Authorization | ✅ Pass / ❌ Fail | {details} |
| Input Validation | ✅ Pass / ❌ Fail | {details} |
| Data Exposure | ✅ Pass / ❌ Fail | {details} |
| Secrets | ✅ Pass / ❌ Fail | {details} |

---

## ⚡ Performance Summary

| Check | Status | Notes |
|-------|--------|-------|
| N+1 Queries | ✅ Pass / ❌ Fail | {details} |
| Async Patterns | ✅ Pass / ❌ Fail | {details} |
| Pagination | ✅ Pass / ❌ Fail | {details} |
| Query Optimization | ✅ Pass / ❌ Fail | {details} |

---

## ✅ What's Good

- {Positive observation 1}
- {Positive observation 2}
- {Positive observation 3}

---

## Action Items

**Must fix before merge**:
- [ ] {Critical/High issue 1}
- [ ] {Critical/High issue 2}

**Should fix soon**:
- [ ] {Medium issue 1}
- [ ] {Medium issue 2}

---

## Technical Debt Noted

- {Future improvement 1}
- {Future improvement 2}
```

---

## Category Labels

Use consistent category labels to classify issues:

| Category | Description | Examples |
|----------|-------------|----------|
| **Security** | Vulnerabilities, auth issues | Missing auth, SQL injection, XSS |
| **Performance** | Efficiency issues | N+1, blocking async, missing pagination |
| **DDD** | Domain design issues | Public setters, anemic entities |
| **ABP** | Framework pattern violations | Wrong base class, missing GuidGenerator |
| **Validation** | Input validation issues | Missing validators, weak rules |
| **Error Handling** | Exception handling issues | Silent catch, wrong exception type |
| **Async** | Async/await issues | Blocking calls, missing cancellation |
| **Testing** | Test quality issues | Missing tests, flaky tests |
| **Style** | Code style issues | Naming, formatting |
| **Documentation** | Doc issues | Missing comments, outdated docs |

---

## Feedback Language

### Use Constructive Language

```markdown
❌ Bad:
"This is wrong."
"You should know better."
"Why didn't you use X?"

✅ Good:
"Consider using X because..."
"This could cause Y. Here's a fix:"
"Have you considered X? It would improve Y."
```

### Differentiate Blocking vs Non-Blocking

```markdown
🚫 [blocking]: Must fix before merge
💭 [suggestion]: Consider for improvement
📝 [nit]: Minor style preference, not blocking
📚 [learning]: Educational note, no action needed
```

---

## Quick Reference

### Minimum Requirements

Every review output MUST include:

1. **Verdict** - Approve/Request Changes
2. **Issue count by severity**
3. **All Critical/High issues with fixes**
4. **File:line references for all issues**
5. **At least one positive observation**

### Severity Quick Guide

| If you find... | Severity |
|----------------|----------|
| Security vulnerability | 🔴 CRITICAL |
| Missing authorization | 🔴 CRITICAL |
| Data corruption risk | 🔴 CRITICAL |
| Null reference exception | 🟠 HIGH |
| N+1 query pattern | 🟠 HIGH |
| Blocking async | 🟡 MEDIUM |
| Missing validation | 🟡 MEDIUM |
| Naming issues | 🟢 LOW |
| Missing docs | 🟢 LOW |

---

## Example Output

```markdown
# Code Review: Add Patient CRUD API

**Date**: 2025-12-13
**Reviewer**: abp-code-reviewer
**Files Reviewed**: 5
**Lines Changed**: +245 / -12

---

## Verdict

🔄 REQUEST CHANGES

**Summary**: Good implementation of Patient CRUD with proper ABP patterns. Found 1 critical security issue (missing authorization) and 2 performance concerns that need attention.

---

## Issue Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| 🔴 CRITICAL | 1 | Yes |
| 🟠 HIGH | 2 | Yes |
| 🟡 MEDIUM | 1 | No |
| 🟢 LOW | 2 | No |

---

## 🔴 Critical Issues

### [CRITICAL] `src/Application/PatientAppService.cs:67` - Security

**Missing authorization on DeleteAsync**

**Problem**:
```csharp
public async Task DeleteAsync(Guid id)
{
    await _repository.DeleteAsync(id);
}
```

**Fix**:
```csharp
[Authorize(ClinicManagementSystemPermissions.Patients.Delete)]
public async Task DeleteAsync(Guid id)
{
    await _repository.DeleteAsync(id);
}
```

**Why**: Any authenticated user can delete patients without permission check.

---

## 🟠 High Issues

### [HIGH] `src/Application/PatientAppService.cs:34` - Performance

**N+1 query pattern in GetListAsync**

**Problem**:
```csharp
foreach (var patient in patients)
{
    patient.Appointments = await _appointmentRepository.GetListAsync(a => a.PatientId == patient.Id);
}
```

**Fix**:
```csharp
var patientIds = patients.Select(p => p.Id).ToList();
var appointments = await _appointmentRepository.GetListAsync(a => patientIds.Contains(a.PatientId));
var grouped = appointments.GroupBy(a => a.PatientId).ToDictionary(g => g.Key, g => g.ToList());
foreach (var patient in patients)
{
    patient.Appointments = grouped.GetValueOrDefault(patient.Id, new List<Appointment>());
}
```

---

## 🔒 Security Summary

| Check | Status | Notes |
|-------|--------|-------|
| Authorization | ❌ Fail | DeleteAsync missing `[Authorize]` |
| Input Validation | ✅ Pass | FluentValidation in place |
| Data Exposure | ✅ Pass | DTOs properly scoped |
| Secrets | ✅ Pass | No hardcoded values |

---

## ⚡ Performance Summary

| Check | Status | Notes |
|-------|--------|-------|
| N+1 Queries | ❌ Fail | Loop in GetListAsync |
| Async Patterns | ✅ Pass | Proper async/await |
| Pagination | ✅ Pass | Using PageBy |
| Query Optimization | ✅ Pass | WhereIf pattern used |

---

## ✅ What's Good

- Excellent entity encapsulation with private setters
- Proper use of `GuidGenerator.Create()`
- Clean FluentValidation implementation
- Good separation of concerns

---

## Action Items

**Must fix before merge**:
- [ ] Add `[Authorize]` to DeleteAsync
- [ ] Fix N+1 query in GetListAsync

**Should fix soon**:
- [ ] Add XML documentation to public methods
```
