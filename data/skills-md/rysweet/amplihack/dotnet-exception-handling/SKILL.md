---
name: dotnet-exception-handling
description: Comprehensive .NET exception handling quality improvement workflow. Auto-detects .NET projects, investigates 10 common exception handling mistakes, generates prioritized findings, and orchestrates fixes following best practices.
version: 1.0.0
tags: [dotnet, quality, exception-handling, investigation, refactoring, security]
token_budget: 5000
maturity: experimental
source_urls:
  - https://abp.io/community/articles/top-10-exception-handling-mistakes-in-net-jhm8wzvg
  - https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions
  - https://learn.microsoft.com/en-us/aspnet/core/web-api/handle-errors
---

# .NET Exception Handling Quality Improvement

## Purpose

Systematic investigation and remediation of .NET exception handling anti-patterns. Detects, documents, and fixes the 10 most common exception handling mistakes in .NET applications.

**Use when**: Preparing for production, code quality audits, security reviews, or onboarding to a .NET codebase.

## Usage

```bash
# Investigation only (default)
/dotnet-exception-handling <path-to-dotnet-project>

# Filter by severity
/dotnet-exception-handling <project-path> --priority critical

# Auto-implement all fixes
/dotnet-exception-handling <project-path> --fix-all
```

**Arguments**:

- `project-path`: Directory containing .csproj or .sln (default: current directory)
- `--priority`: `critical` | `high` | `medium` | `low` | `all` (default: `all`)
- `--fix-all`: Implement fixes automatically (default: investigate only)

## The 10 Common Mistakes

1. **Catching Exception Too Broadly** - Base `Exception` instead of specific types
2. **Swallowing Exceptions Silently** - Empty catch blocks hiding errors
3. **Using `throw ex;`** - Resets stack traces (use `throw;`)
4. **Wrapping Everything in Try/Catch** - Defensive coding clutter
5. **Exceptions for Control Flow** - Performance overhead for expected conditions
6. **Forgetting to Await Async** - Unhandled exceptions on background threads
7. **Ignoring Background Task Exceptions** - Fire-and-forget losing errors
8. **Generic Exception Types** - Vague `new Exception()` instead of specific types
9. **Losing Inner Exceptions** - Breaking exception chains
10. **Missing Global Handler** - No centralized error handling (stack traces exposed)

**Detailed descriptions, detection patterns, and fix templates** → see `reference.md`

## Execution Workflow

### Phase 1: Investigation (6 Steps)

**Step 1: Project Detection**

- Scan for .csproj, .sln files
- Identify project types (ASP.NET Core, worker services, libraries)
- Count C# files for scope estimation

**Step 2: Parallel Analysis**

- Deploy 5 specialized agents:
  - Background Worker Specialist
  - API Layer Specialist
  - Service Layer Specialist
  - Data Layer Specialist
  - Infrastructure Specialist

**Step 3: Violation Detection**

- Use `rg -P` (ripgrep PCRE mode) for pattern matching:

  ```bash
  # Mistake #1: Broad catches
  rg -P 'catch\s*\(Exception\b' --glob '*.cs'

  # Mistake #2: Empty catches
  rg -P 'catch[^{]*\{\s*(//[^\n]*)?\s*\}' --glob '*.cs'

  # Mistake #3: throw ex
  rg 'throw\s+ex;' --glob '*.cs'
  ```

- See `reference.md` for complete pattern list

**Step 4: Severity Classification**

- **CRITICAL**: Security (stack trace exposure, missing global handler)
- **HIGH**: Reliability (swallowed exceptions, broad catches)
- **MEDIUM**: Code quality (excessive try/catch)
- **LOW**: Style issues

**Step 5: Findings Report**

- Generate markdown with file:line references
- Code snippets + recommended fixes
- Priority-based roadmap

**Step 6: Knowledge Capture**

- Store in `.claude/runtime/logs/EXCEPTION_INVESTIGATION_YYYY-MM-DD.md`
- Update project memory

### Phase 2: Development (If --fix-all)

**Step 7: Orchestrate Default Workflow**

- Create GitHub issue with findings
- Set up worktree for fixes
- Implement GlobalExceptionHandler, Result<T>, etc.
- Write comprehensive tests (TDD)
- Three-agent review (reviewer, security, philosophy)

**Step 8: Validation**

- All tests pass
- Security: Zero stack traces
- Performance: <5ms p99 overhead

## Quick Start Examples

### Example 1: Investigation Only

```bash
/dotnet-exception-handling ./src/MyApi
```

**Output**: Investigation report with 23 violations (1 CRITICAL, 8 HIGH, 12 MEDIUM, 2 LOW)

### Example 2: Fix Critical Only

```bash
/dotnet-exception-handling ./src/MyApi --priority critical --fix-all
```

**Output**: GitHub issue + PR implementing GlobalExceptionHandler + 15 tests

### Example 3: Complete Fix

```bash
/dotnet-exception-handling ./src/MyApi --fix-all
```

**Output**: 23 violations fixed, 67 tests, PR ready (CI passing)

## Core Architecture Patterns

### GlobalExceptionHandler (IExceptionHandler)

Centralized exception-to-HTTP mapping for ASP.NET Core:

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (statusCode, title) = exception switch
        {
            ArgumentException => (400, "Invalid request"),
            NotFoundException => (404, "Not found"),
            ConflictException => (409, "Conflict"),
            _ => (500, "Internal server error")
        };

        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = statusCode >= 500
                ? "An error occurred"
                : exception.Message
        }, cancellationToken);

        return true;
    }
}

// Registration in Program.cs
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

**Benefits**: Zero stack traces, consistent responses, no try/catch in controllers

### Result<T> Pattern

Railway-oriented programming for validation (no exceptions for expected conditions):

```csharp
public Result<Order> ValidateOrder(CreateOrderDto dto)
{
    if (dto.Items.Count == 0)
        return Result<Order>.Failure("Order must have items");

    return Result<Order>.Success(new Order(dto));
}

// Controller usage
var result = await _service.ValidateOrder(dto);
return result.Match(
    onSuccess: order => Ok(order),
    onFailure: error => BadRequest(error)
);
```

**Benefits**: 100x faster than exceptions, explicit error handling, better composition

**Complete implementations** → see `examples.md`

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Detailed descriptions of all 10 exception handling mistakes
- Complete detection patterns for ripgrep/grep
- Fix templates for each mistake type
- Security considerations (OWASP compliance, stack trace prevention)
- Severity classification reference
- Integration patterns (Azure SDK, EF Core, Service Bus)

**examples.md** - Read when you need:

- Before/after code examples for each mistake
- Complete working implementations (GlobalExceptionHandler, Result<T>, DbContextExtensions)
- Real-world scenarios (order processing, payment systems)
- Unit and integration testing patterns
- Copy-paste ready code

**patterns.md** - Read when you need:

- Architecture decision trees (global handler vs try/catch, Result<T> vs exceptions)
- Background worker exception handling patterns
- Azure SDK exception translation patterns
- EF Core concurrency and transaction patterns
- Performance benchmarks (Result<T> vs exceptions)
- Anti-patterns to avoid

## Workflow Integration

This skill orchestrates two canonical workflows:

1. **Investigation Workflow** (Phase 1): Scope → Explore → Analyze → Classify → Report → Capture
2. **Default Workflow** (Phase 2, if --fix-all): Requirements → Architecture → TDD → Implementation → Review → CI/CD

## References

- **Article**: [Top 10 Exception Handling Mistakes in .NET](https://abp.io/community/articles/top-10-exception-handling-mistakes-in-net-jhm8wzvg)
- **Microsoft**: [Best Practices for Exceptions](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions)
- **ASP.NET Core**: [Handle Errors in Web APIs](https://learn.microsoft.com/en-us/aspnet/core/web-api/handle-errors)
- **Investigation Workflow**: `~/.amplihack/.claude/workflow/INVESTIGATION_WORKFLOW.md`
- **Default Workflow**: `~/.amplihack/.claude/workflow/DEFAULT_WORKFLOW.md`

## Version History

- v1.0.0 (2026-02-10): Initial implementation based on CyberGym investigation (52 violations fixed, 87 tests)

## Known Limitations

- Requires .NET 6+ for IExceptionHandler
- Result<T> pattern targets C# 7.0+ (struct readonly, expression-bodied members)
- Patterns specific to ASP.NET Core (may not apply to class libraries)
