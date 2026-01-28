---
name: dotnet-async-patterns
description: "Master .NET async/await patterns including Task-based Asynchronous Pattern (TAP), ValueTask optimization, ConfigureAwait usage, cancellation tokens, parallel processing, and avoiding deadlocks in ASP.NET Core applications for maximum performance and responsiveness."
layer: 1
tech_stack: [dotnet, csharp]
topics: [async-await, task, valuetask, cancellation, parallel, deadlock-prevention]
depends_on: []
complements: [error-handling-patterns, csharp-advanced-patterns]
keywords: [async, await, Task, ValueTask, CancellationToken, ConfigureAwait, WhenAll, Parallel]
---

# .NET Async/Await Patterns

Master asynchronous programming in .NET for building high-performance, scalable ASP.NET Core applications.

## When to Use This Skill

- Building ASP.NET Core APIs
- Working with async database operations (EF Core)
- Calling external APIs or web services
- Implementing background processing
- Handling concurrent requests efficiently
- Preventing thread pool starvation
- Optimizing application performance
- Avoiding deadlocks

## Core Concepts

### 1. Async/Await Fundamentals

**Basic Async Method:**
```csharp
// Async method signature
public async Task<Patient> GetPatientAsync(Guid id)
{
    var patient = await _dbContext.Patients.FindAsync(id);
    return patient;
}

// Async method without return value
public async Task SendEmailAsync(string to, string subject, string body)
{
    await _emailService.SendAsync(to, subject, body);
}

// Async method with value return
public async Task<int> GetPatientCountAsync()
{
    return await _dbContext.Patients.CountAsync();
}
```

**Calling Async Methods:**
```csharp
// Good: Always await async methods
public async Task<AppointmentDto> CreateAppointmentAsync(CreateAppointmentDto input)
{
    var patient = await _patientRepository.GetAsync(input.PatientId);
    var doctor = await _doctorRepository.GetAsync(input.DoctorId);

    // Validate and create appointment
    var appointment = new Appointment(/*...*/);
    await _appointmentRepository.InsertAsync(appointment);

    return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
}

// Bad: Blocking async code (causes deadlocks)
public AppointmentDto CreateAppointment(CreateAppointmentDto input)
{
    var patient = _patientRepository.GetAsync(input.PatientId).Result; // DON'T DO THIS
    var doctor = _doctorRepository.GetAsync(input.DoctorId).Wait(); // DON'T DO THIS
    // ...
}
```

### 2. ConfigureAwait

**Library Code (Use ConfigureAwait(false)):**
```csharp
// In class libraries or reusable components
public async Task<Patient> GetPatientByEmailAsync(string email)
{
    // ConfigureAwait(false) avoids capturing synchronization context
    // Better performance, especially in library code
    var patient = await _dbContext.Patients
        .FirstOrDefaultAsync(p => p.Email == email)
        .ConfigureAwait(false);

    return patient;
}
```

**ASP.NET Core (ConfigureAwait Not Needed):**
```csharp
// In ASP.NET Core controllers/app services
public async Task<ActionResult<PatientDto>> GetPatient(Guid id)
{
    // No need for ConfigureAwait in ASP.NET Core
    // ASP.NET Core doesn't have a synchronization context
    var patient = await _patientRepository.GetAsync(id);
    return Ok(patient);
}
```

**Rule of Thumb:**
- ASP.NET Core: ConfigureAwait not needed
- Library code: Use ConfigureAwait(false) for performance
- UI applications (WPF/WinForms): Don't use ConfigureAwait(false)

### 3. ValueTask for Performance

**When to Use ValueTask:**
```csharp
// Use ValueTask when result is often synchronous (cached/immediate)
public ValueTask<Patient> GetPatientAsync(Guid id)
{
    // Check cache first
    if (_cache.TryGetValue(id, out Patient cachedPatient))
    {
        return new ValueTask<Patient>(cachedPatient); // Synchronous return
    }

    // Cache miss, fetch from database
    return new ValueTask<Patient>(FetchPatientFromDatabaseAsync(id));
}

private async Task<Patient> FetchPatientFromDatabaseAsync(Guid id)
{
    return await _dbContext.Patients.FindAsync(id);
}

// Use Task for always-async operations
public async Task<Patient> CreatePatientAsync(CreatePatientDto input)
{
    // Always async, use Task
    var patient = new Patient(/*...*/);
    await _dbContext.Patients.AddAsync(patient);
    await _dbContext.SaveChangesAsync();
    return patient;
}
```

**ValueTask Rules:**
- Don't await ValueTask multiple times
- Don't call .Result or .GetAwaiter().GetResult()
- Consider using for hot paths with frequent synchronous returns

### 4. Cancellation Tokens

**Controller with Cancellation:**
```csharp
[HttpGet]
public async Task<ActionResult<List<PatientDto>>> GetPatients(
    CancellationToken cancellationToken) // Automatically bound from request
{
    var patients = await _dbContext.Patients
        .AsNoTracking()
        .ToListAsync(cancellationToken); // Pass token to async operations

    return Ok(patients);
}
```

**Service with Cancellation:**
```csharp
public class AppointmentService : IAppointmentService
{
    public async Task<List<Appointment>> GetUpcomingAppointmentsAsync(
        Guid doctorId,
        CancellationToken cancellationToken = default)
    {
        // Check if cancellation requested
        cancellationToken.ThrowIfCancellationRequested();

        var appointments = await _dbContext.Appointments
            .Where(a => a.DoctorId == doctorId && a.AppointmentDate >= DateTime.Today)
            .ToListAsync(cancellationToken);

        // Long-running operation
        foreach (var appointment in appointments)
        {
            cancellationToken.ThrowIfCancellationRequested();
            await ProcessAppointmentAsync(appointment, cancellationToken);
        }

        return appointments;
    }
}
```

**Creating CancellationToken:**
```csharp
// Timeout after 30 seconds
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));

try
{
    var result = await _externalApiService.FetchDataAsync(cts.Token);
}
catch (OperationCanceledException)
{
    _logger.LogWarning("External API call timed out");
}

// Manual cancellation
var cts = new CancellationTokenSource();
var task = LongRunningOperationAsync(cts.Token);

// Cancel from another thread/operation
cts.Cancel();

// Linked cancellation tokens
var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
    httpContext.RequestAborted,
    timeoutToken);
```

### 5. Parallel Processing

**Task.WhenAll - Wait for Multiple Tasks:**
```csharp
// Sequential (slow)
public async Task<DashboardDto> GetDashboardAsync()
{
    var patientCount = await _dbContext.Patients.CountAsync();
    var appointmentCount = await _dbContext.Appointments.CountAsync();
    var doctorCount = await _dbContext.Doctors.CountAsync();

    return new DashboardDto
    {
        PatientCount = patientCount,
        AppointmentCount = appointmentCount,
        DoctorCount = doctorCount
    };
}

// Parallel (fast)
public async Task<DashboardDto> GetDashboardAsync()
{
    var patientCountTask = _dbContext.Patients.CountAsync();
    var appointmentCountTask = _dbContext.Appointments.CountAsync();
    var doctorCountTask = _dbContext.Doctors.CountAsync();

    await Task.WhenAll(patientCountTask, appointmentCountTask, doctorCountTask);

    return new DashboardDto
    {
        PatientCount = patientCountTask.Result,
        AppointmentCount = appointmentCountTask.Result,
        DoctorCount = doctorCountTask.Result
    };
}

// Or use awaited tuple
public async Task<DashboardDto> GetDashboardAsync()
{
    var (patientCount, appointmentCount, doctorCount) = await (
        _dbContext.Patients.CountAsync(),
        _dbContext.Appointments.CountAsync(),
        _dbContext.Doctors.CountAsync()
    );

    return new DashboardDto
    {
        PatientCount = patientCount,
        AppointmentCount = appointmentCount,
        DoctorCount = doctorCount
    };
}
```

**Task.WhenAny - First to Complete:**
```csharp
public async Task<Patient> GetPatientFromMultipleSourcesAsync(Guid id)
{
    var primaryTask = _primaryDbService.GetPatientAsync(id);
    var backupTask = _backupDbService.GetPatientAsync(id);
    var cacheTask = _cacheService.GetPatientAsync(id);

    var completedTask = await Task.WhenAny(primaryTask, backupTask, cacheTask);

    return await completedTask;
}

// With timeout
public async Task<Patient> GetPatientWithTimeoutAsync(Guid id, TimeSpan timeout)
{
    var patientTask = _dbContext.Patients.FindAsync(id).AsTask();
    var timeoutTask = Task.Delay(timeout);

    var completedTask = await Task.WhenAny(patientTask, timeoutTask);

    if (completedTask == timeoutTask)
    {
        throw new TimeoutException("Database query timed out");
    }

    return await patientTask;
}
```

**Parallel.ForEachAsync - Process Collection in Parallel:**
```csharp
// .NET 6+
public async Task ProcessPatientsAsync(List<Guid> patientIds)
{
    await Parallel.ForEachAsync(
        patientIds,
        new ParallelOptions { MaxDegreeOfParallelism = 10 },
        async (patientId, cancellationToken) =>
        {
            var patient = await _patientRepository.GetAsync(patientId);
            await ProcessPatientAsync(patient, cancellationToken);
        });
}

// For older versions, use SemaphoreSlim
public async Task ProcessPatientsAsync(List<Guid> patientIds)
{
    using var semaphore = new SemaphoreSlim(10); // Max 10 concurrent

    var tasks = patientIds.Select(async patientId =>
    {
        await semaphore.WaitAsync();
        try
        {
            var patient = await _patientRepository.GetAsync(patientId);
            await ProcessPatientAsync(patient);
        }
        finally
        {
            semaphore.Release();
        }
    });

    await Task.WhenAll(tasks);
}
```

### 6. Async Streams (IAsyncEnumerable)

**Producer:**
```csharp
public async IAsyncEnumerable<Patient> GetPatientsStreamAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    var patients = _dbContext.Patients.AsAsyncEnumerable();

    await foreach (var patient in patients.WithCancellation(cancellationToken))
    {
        // Process or filter
        if (patient.IsActive)
        {
            yield return patient;
        }
    }
}
```

**Consumer:**
```csharp
public async Task ProcessAllPatientsAsync()
{
    await foreach (var patient in _patientService.GetPatientsStreamAsync())
    {
        await ProcessPatientAsync(patient);
        // Memory efficient: processes one at a time
    }
}

// LINQ with async streams
var activePatientsCount = await _patientService
    .GetPatientsStreamAsync()
    .Where(p => p.IsActive)
    .CountAsync();
```

**SignalR Streaming:**
```csharp
// Hub method returning IAsyncEnumerable
public async IAsyncEnumerable<AppointmentDto> StreamAppointments(
    Guid doctorId,
    [EnumeratorCancellation] CancellationToken cancellationToken)
{
    while (!cancellationToken.IsCancellationRequested)
    {
        var appointments = await _appointmentService.GetUpcomingAsync(doctorId);

        foreach (var appointment in appointments)
        {
            yield return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
        }

        await Task.Delay(TimeSpan.FromSeconds(30), cancellationToken);
    }
}
```

### 7. Exception Handling in Async

**Try-Catch in Async Methods:**
```csharp
public async Task<Patient> GetPatientAsync(Guid id)
{
    try
    {
        var patient = await _dbContext.Patients.FindAsync(id);

        if (patient == null)
        {
            throw new EntityNotFoundException($"Patient {id} not found");
        }

        return patient;
    }
    catch (DbUpdateException ex)
    {
        _logger.LogError(ex, "Database error while fetching patient {PatientId}", id);
        throw new ApplicationException("Failed to retrieve patient", ex);
    }
}
```

**AggregateException with Task.WhenAll:**
```csharp
public async Task ProcessMultiplePatientsAsync(List<Guid> patientIds)
{
    var tasks = patientIds.Select(id => ProcessPatientAsync(id)).ToList();

    try
    {
        await Task.WhenAll(tasks);
    }
    catch (Exception)
    {
        // Only first exception is thrown
        // To get all exceptions:
        var exceptions = tasks
            .Where(t => t.IsFaulted)
            .Select(t => t.Exception.InnerException)
            .ToList();

        foreach (var ex in exceptions)
        {
            _logger.LogError(ex, "Failed to process patient");
        }

        throw new AggregateException("Multiple patients failed to process", exceptions);
    }
}
```

### 8. Deadlock Prevention

**Common Deadlock Scenario (DON'T DO THIS):**
```csharp
// WEB API CONTROLLER - CAUSES DEADLOCK
public IActionResult GetPatient(Guid id)
{
    // NEVER block on async code in ASP.NET
    var patient = _patientService.GetPatientAsync(id).Result; // DEADLOCK!
    return Ok(patient);
}

// LIBRARY METHOD
public async Task<Patient> GetPatientAsync(Guid id)
{
    var patient = await _dbContext.Patients.FindAsync(id);
    // Tries to resume on captured synchronization context
    // But controller thread is blocked waiting for this to complete
    return patient;
}
```

**Solution: Async All the Way:**
```csharp
// GOOD: Async all the way
public async Task<IActionResult> GetPatientAsync(Guid id)
{
    var patient = await _patientService.GetPatientAsync(id);
    return Ok(patient);
}
```

**Solution: ConfigureAwait(false) in Library:**
```csharp
public async Task<Patient> GetPatientAsync(Guid id)
{
    var patient = await _dbContext.Patients
        .FindAsync(id)
        .ConfigureAwait(false); // Don't capture context

    return patient;
}
```

### 9. Background Work in ASP.NET Core

**IHostedService for Background Tasks:**
```csharp
public class AppointmentReminderService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<AppointmentReminderService> _logger;

    public AppointmentReminderService(
        IServiceScopeFactory scopeFactory,
        ILogger<AppointmentReminderService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Appointment Reminder Service started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await SendRemindersAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending appointment reminders");
            }

            // Wait 1 hour before next check
            await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
        }
    }

    private async Task SendRemindersAsync(CancellationToken cancellationToken)
    {
        // Create scope for scoped services
        using var scope = _scopeFactory.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<ClinicDbContext>();
        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();

        var tomorrow = DateTime.Today.AddDays(1);
        var appointments = await dbContext.Appointments
            .Where(a => a.AppointmentDate >= tomorrow &&
                       a.AppointmentDate < tomorrow.AddDays(1))
            .Include(a => a.Patient)
            .ToListAsync(cancellationToken);

        foreach (var appointment in appointments)
        {
            await emailService.SendReminderAsync(appointment, cancellationToken);
        }
    }
}

// Register in Program.cs
builder.Services.AddHostedService<AppointmentReminderService>();
```

## Best Practices

1. **Async All the Way**: Don't mix sync and async code
2. **Avoid .Result/.Wait()**: Causes deadlocks, use await
3. **Use CancellationToken**: For long-running operations
4. **ValueTask for Hot Paths**: When frequently synchronous
5. **ConfigureAwait(false)**: In library code for performance
6. **Task.WhenAll**: For parallel independent operations
7. **Async Streams**: For memory-efficient streaming
8. **SemaphoreSlim**: For limiting concurrency
9. **Proper Exception Handling**: Try-catch in async methods
10. **Background Services**: Use IHostedService for background work

## Common Pitfalls

- **Blocking async code** with .Result or .Wait()
- **Async void methods** (except event handlers)
- **Not passing CancellationToken** to async operations
- **Fire-and-forget** async methods (always await or use Task.Run)
- **Capturing variables in loops** with async lambdas
- **Not handling exceptions** in Task.WhenAll
- **Using Task.Run** unnecessarily (async I/O doesn't need Task.Run)

## Performance Tips

1. Avoid unnecessary Task.Run (async I/O is already async)
2. Use ValueTask for frequently synchronous paths
3. Pool objects with ObjectPool instead of recreating
4. Use ConfigureAwait(false) in libraries
5. Limit concurrency with SemaphoreSlim
6. Use IAsyncEnumerable for large datasets
7. Avoid Task.Result in hot paths
8. Prefer async methods over synchronous wrappers

## Async Method Checklist

- [ ] Method signature includes `async` keyword
- [ ] Return type is `Task`, `Task<T>`, or `ValueTask<T>`
- [ ] All async operations are awaited
- [ ] CancellationToken parameter included
- [ ] No .Result or .Wait() calls
- [ ] Exceptions properly handled
- [ ] ConfigureAwait(false) in library code
- [ ] No async void (except event handlers)

## Resources

- **Async/Await Best Practices**: Stephen Cleary's blog
- **Task-based Asynchronous Pattern**: Microsoft Docs
- **ConfigureAwait FAQ**: https://devblogs.microsoft.com/dotnet/configureawait-faq/
