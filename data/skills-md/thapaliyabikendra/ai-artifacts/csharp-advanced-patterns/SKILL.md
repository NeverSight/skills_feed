---
name: csharp-advanced-patterns
description: "Master advanced C# patterns including records, pattern matching, async/await, LINQ, and performance optimization for .NET 10. Use when: (1) implementing complex C# patterns, (2) optimizing performance, (3) refactoring legacy code, (4) writing modern idiomatic C#."
layer: 1
tech_stack: [dotnet, csharp]
topics: [records, pattern-matching, linq, generics, nullable, span, performance]
depends_on: []
complements: [dotnet-async-patterns]
keywords: [record, switch, pattern, Span, Memory, required, init, LINQ]
---

# C# Advanced Patterns

Advanced C# language patterns and .NET 10 features for elegant, performant code.

## When to Use

- Implementing complex business logic with pattern matching
- Optimizing async/await usage
- Writing performant code with Span<T>/Memory<T>
- Refactoring legacy code to modern C#
- Creating immutable DTOs with records

## Modern C# Features (.NET 10)

### Records for DTOs

```csharp
// Immutable DTO with required properties
public record CreatePatientDto
{
    public required string FirstName { get; init; }
    public required string LastName { get; init; }
    public required string Email { get; init; }
    public DateTime DateOfBirth { get; init; }
}

// Positional record with deconstruction
public record PatientDto(Guid Id, string FullName, string Email);

// Usage
var (id, name, email) = patient;
```

### Pattern Matching

```csharp
// Switch expression for status handling
public string GetStatusMessage(AppointmentStatus status) => status switch
{
    AppointmentStatus.Scheduled => "Your appointment is confirmed",
    AppointmentStatus.Completed => "Thank you for visiting",
    AppointmentStatus.Cancelled => "Your appointment was cancelled",
    AppointmentStatus.NoShow => "You missed your appointment",
    _ => throw new ArgumentOutOfRangeException(nameof(status))
};

// Property pattern matching
public decimal CalculateDiscount(Patient patient) => patient switch
{
    { Age: > 65 } => 0.20m,
    { IsVeteran: true } => 0.15m,
    { Visits: > 10 } => 0.10m,
    _ => 0m
};

// List patterns (.NET 7+)
public string DescribeList(int[] numbers) => numbers switch
{
    [] => "Empty",
    [var single] => $"Single: {single}",
    [var first, .., var last] => $"First: {first}, Last: {last}",
};
```

### Primary Constructors

```csharp
// Class with primary constructor
public class PatientService(
    IRepository<Patient, Guid> repository,
    ILogger<PatientService> logger)
{
    public async Task<Patient> GetAsync(Guid id)
    {
        logger.LogInformation("Getting patient {Id}", id);
        return await repository.GetAsync(id);
    }
}
```

### Collection Expressions

```csharp
// Modern collection initialization
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];
Span<int> span = [1, 2, 3];

// Spread operator
int[] combined = [..numbers, 6, 7, 8];
```

## Async/Await Patterns

### Proper Async with Cancellation

```csharp
public async Task<PatientDto> GetPatientAsync(
    Guid id,
    CancellationToken cancellationToken = default)
{
    var patient = await _repository
        .GetAsync(id, cancellationToken);

    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

### Parallel Processing with SemaphoreSlim

```csharp
public async Task ProcessPatientsAsync(
    IEnumerable<Guid> patientIds,
    CancellationToken ct)
{
    var semaphore = new SemaphoreSlim(10); // Max 10 concurrent
    var tasks = patientIds.Select(async id =>
    {
        await semaphore.WaitAsync(ct);
        try
        {
            await ProcessPatientAsync(id, ct);
        }
        finally
        {
            semaphore.Release();
        }
    });

    await Task.WhenAll(tasks);
}
```

### ValueTask for Hot Paths

```csharp
// Use ValueTask when result is often synchronous
public ValueTask<Patient?> GetCachedPatientAsync(Guid id)
{
    if (_cache.TryGetValue(id, out var patient))
        return ValueTask.FromResult<Patient?>(patient);

    return new ValueTask<Patient?>(LoadPatientAsync(id));
}
```

### Channel for Producer/Consumer

```csharp
public class PatientProcessor
{
    private readonly Channel<Patient> _channel =
        Channel.CreateBounded<Patient>(100);

    public async Task ProduceAsync(Patient patient, CancellationToken ct)
    {
        await _channel.Writer.WriteAsync(patient, ct);
    }

    public async Task ConsumeAsync(CancellationToken ct)
    {
        await foreach (var patient in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessAsync(patient);
        }
    }
}
```

## Result Pattern

```csharp
public readonly record struct Result<T>
{
    public T? Value { get; }
    public string? Error { get; }
    public bool IsSuccess => Error is null;

    private Result(T value) => Value = value;
    private Result(string error) => Error = error;

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);

    public TResult Match<TResult>(
        Func<T, TResult> onSuccess,
        Func<string, TResult> onFailure)
        => IsSuccess ? onSuccess(Value!) : onFailure(Error!);
}

// Usage
public Result<Patient> CreatePatient(CreatePatientDto dto)
{
    if (string.IsNullOrEmpty(dto.Email))
        return Result<Patient>.Failure("Email is required");

    var patient = new Patient(dto.FirstName, dto.LastName, dto.Email);
    return Result<Patient>.Success(patient);
}
```

## Extension Methods

```csharp
public static class PatientExtensions
{
    public static string GetFullName(this Patient patient)
        => $"{patient.FirstName} {patient.LastName}";

    public static bool IsEligibleForDiscount(this Patient patient)
        => patient.Age > 65 || patient.Visits > 10;

    // IQueryable extension for reusable filters
    public static IQueryable<Patient> ActiveOnly(this IQueryable<Patient> query)
        => query.Where(p => p.IsActive);

    public static IQueryable<Patient> ByEmail(
        this IQueryable<Patient> query,
        string email)
        => query.Where(p => p.Email == email);
}
```

## Performance Patterns

### Span<T> for Zero-Allocation

```csharp
public static int CountOccurrences(ReadOnlySpan<char> text, char target)
{
    int count = 0;
    foreach (var c in text)
    {
        if (c == target) count++;
    }
    return count;
}

// String slicing without allocation
ReadOnlySpan<char> firstName = fullName.AsSpan(0, spaceIndex);
```

### ArrayPool for Temporary Buffers

```csharp
public async Task ProcessLargeDataAsync(Stream stream)
{
    var buffer = ArrayPool<byte>.Shared.Rent(4096);
    try
    {
        int bytesRead;
        while ((bytesRead = await stream.ReadAsync(buffer)) > 0)
        {
            ProcessChunk(buffer.AsSpan(0, bytesRead));
        }
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### StringBuilder for String Building

```csharp
// Bad: String concatenation in loops
string result = "";
foreach (var item in items)
    result += item; // Creates new string each iteration

// Good: Use StringBuilder
var sb = new StringBuilder();
foreach (var item in items)
    sb.Append(item);
return sb.ToString();
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `.Result` / `.Wait()` | Deadlock risk | Use `await` |
| `catch (Exception)` | Catches everything | Catch specific types |
| String concat in loops | O(n²) allocations | Use StringBuilder |
| `async void` | Unobserved exceptions | Use `async Task` |
| Premature optimization | Complexity | Profile first |

```csharp
// Bad: Blocking on async
var result = GetPatientAsync(id).Result; // Deadlock risk!

// Good: Proper async
var result = await GetPatientAsync(id);

// Bad: async void (fire and forget)
async void ProcessPatient(Guid id) { ... }

// Good: async Task
async Task ProcessPatientAsync(Guid id) { ... }

// Bad: Catching base Exception
try { } catch (Exception ex) { }

// Good: Catch specific exceptions
try { }
catch (InvalidOperationException ex) { _logger.LogWarning(ex, "..."); }
catch (ArgumentException ex) { _logger.LogError(ex, "..."); }
```

## LINQ Best Practices

```csharp
// Avoid multiple enumeration
var patients = await _repository.GetListAsync(); // Materialize once
var count = patients.Count;
var first = patients.FirstOrDefault();

// Use AsNoTracking for read-only queries
var patients = await _context.Patients
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();

// Prefer Any() over Count() > 0
if (await _repository.AnyAsync(p => p.Email == email)) { ... }

// Project early to reduce data transfer
var dtos = await _context.Patients
    .Where(p => p.IsActive)
    .Select(p => new PatientDto(p.Id, p.FullName, p.Email))
    .ToListAsync();
```

## Quality Checklist

- [ ] Use records for DTOs (immutability)
- [ ] Use switch expressions over switch statements
- [ ] Pass CancellationToken through async chain
- [ ] Use ValueTask for hot paths with sync results
- [ ] Avoid blocking calls (.Result, .Wait())
- [ ] Use Span<T> for performance-critical parsing
- [ ] Catch specific exception types
- [ ] Use nullable reference types

## Integration Points

This skill is used by:
- **abp-developer**: Modern C# patterns in implementation
- **abp-code-reviewer**: Pattern validation during reviews
- **debugger**: Performance analysis and fixes
