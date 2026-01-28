---
name: debugging-patterns
description: "Debug .NET/ABP and React applications with systematic root cause analysis. Use when: (1) investigating bugs or errors, (2) analyzing stack traces, (3) diagnosing N+1 queries, (4) fixing async deadlocks, (5) resolving React state issues."
layer: 1
tech_stack: [dotnet, csharp, typescript, react]
topics: [root-cause-analysis, stack-traces, logging, profiling, breakpoints]
depends_on: []
complements: [error-handling-patterns]
keywords: [Debug, StackTrace, Logging, Profiler, Breakpoint, Exception, NullReference]
---

# Debugging Patterns

Systematic debugging patterns for ABP Framework and React applications.

## When to Use

- Investigating bugs or test failures
- Analyzing stack traces and error messages
- Diagnosing database query issues (N+1, tracking conflicts)
- Fixing async/await deadlocks
- Resolving React state management bugs

## Debugging Process

### 1. Capture Information
- Error message and full stack trace
- Reproduction steps (reliable vs intermittent)
- Environment (dev/staging/prod)
- Recent code changes

### 2. Isolate the Problem
- Identify failing component (backend/frontend)
- Narrow down to specific file/function
- Check logs and network requests

### 3. Form Hypothesis
- Match error pattern to known issues
- Check similar past issues
- Review recent commits

### 4. Verify and Fix
- Test hypothesis with minimal change
- Verify fix doesn't break other things
- Add test to prevent regression

## ABP Framework Issues

### Authorization Failure

**Error**: `Authorization failed for the request`

**Diagnosis Checklist**:
1. Is permission defined in `{Project}Permissions.cs`?
2. Is permission granted to role in `PermissionDefinitionProvider`?
3. Is `[Authorize]` attribute using correct permission constant?

```csharp
// Check permission definition
public static class ClinicPermissions
{
    public static class Patients
    {
        public const string Default = "Clinic.Patients";
        public const string Create = "Clinic.Patients.Create"; // Missing?
    }
}

// Check attribute matches
[Authorize(ClinicPermissions.Patients.Create)]  // Not .Default
public async Task<PatientDto> CreateAsync(...)
```

### Entity Not Found

**Error**: `Entity of type Patient with id X was not found`

**Diagnosis**:
```csharp
// Debug: Verify entity exists
var exists = await _repository.AnyAsync(x => x.Id == id);
_logger.LogDebug("Patient {Id} exists: {Exists}", id, exists);

// Fix: Use FirstOrDefaultAsync for graceful handling
var patient = await _repository.FirstOrDefaultAsync(x => x.Id == id);
if (patient == null)
{
    throw new UserFriendlyException("Patient not found");
}
```

### Async Deadlock

**Symptom**: Application hangs, no error message

**Cause**: Using `.Result` or `.Wait()` on async code

```csharp
// BAD: Causes deadlock in ASP.NET Core
var result = _service.GetAsync(id).Result;
var result2 = _service.GetAsync(id).Wait();

// GOOD: Proper async/await
var result = await _service.GetAsync(id);
```

## Entity Framework Core Issues

### N+1 Query Problem

**Symptom**: Slow API response, excessive database queries in logs

**Diagnosis**: Enable EF Core logging
```json
{
  "Logging": {
    "LogLevel": {
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

```csharp
// BAD: N+1 queries - executes 1 + N queries
var patients = await _repository.GetListAsync();
foreach (var patient in patients)
{
    var appointments = patient.Appointments; // Lazy load each time!
}

// GOOD: Eager loading with Include
var patients = await _repository
    .WithDetailsAsync(p => p.Appointments);

// BETTER: Project to DTO
var patients = await query
    .Select(p => new PatientDto
    {
        Id = p.Id,
        AppointmentCount = p.Appointments.Count
    })
    .ToListAsync();
```

### Tracking Conflict

**Error**: `The instance of entity type cannot be tracked`

**Cause**: Entity with same key already tracked

```csharp
// Fix: Use AsNoTracking for read-only queries
var patient = await _repository
    .AsNoTracking()
    .FirstOrDefaultAsync(p => p.Id == id);
```

## React/TypeScript Issues

### Stale Closure

**Symptom**: State shows old value in callback

```typescript
// BAD: Stale closure - always uses initial count
const [count, setCount] = useState(0);
useEffect(() => {
  const interval = setInterval(() => {
    setCount(count + 1); // Captures initial count = 0
  }, 1000);
  return () => clearInterval(interval);
}, []); // Empty deps = stale closure

// GOOD: Functional update
setCount(prev => prev + 1);
```

### React Query Cache Not Updating

**Symptom**: Data not refreshing after mutation

```typescript
// BAD: Cache not invalidated
const createMutation = useMutation(createPatient);

// GOOD: Invalidate on success
const queryClient = useQueryClient();
const createMutation = useMutation(createPatient, {
  onSuccess: () => {
    queryClient.invalidateQueries(['patients']);
  }
});
```

### TypeScript Any Leak

**Symptom**: Runtime type errors despite compilation success

```typescript
// Diagnosis: Search for any types
// grep ": any" or "as any"

// Fix: Add explicit types
interface ApiResponse<T> {
  data: T;
  success: boolean;
  error?: string;
}
```

## Debug Commands

```bash
# Backend: Run with verbose logging
dotnet run --project api/src/ClinicManagementSystem.HttpApi.Host 2>&1 | grep -i error

# Backend: Run specific failing test
dotnet test --filter "FullyQualifiedName~PatientAppService_Tests"

# EF Core: See generated SQL (in appsettings.Development.json)
# "Microsoft.EntityFrameworkCore.Database.Command": "Information"

# Frontend: Browser DevTools
# Console tab: JavaScript errors
# Network tab > XHR: API requests/responses
```

## Output Format

```markdown
## Bug Analysis: [Issue Title]

### Symptoms
- [What was observed]

### Root Cause
[Technical explanation of why this happened]

### Evidence
```
[Stack trace or log excerpt]
```

### Fix
```csharp
// Before
[problematic code]

// After
[fixed code]
```

### Verification
- [ ] Unit test passes
- [ ] Manual test passes
- [ ] No regression

### Prevention
[How to prevent this in the future]
```

## Integration Points

This skill is used by:
- **debugger**: Root cause analysis and diagnosis
- **abp-code-reviewer**: Identifying potential issues in backend PRs
- **abp-developer**: Fixing bugs during implementation
