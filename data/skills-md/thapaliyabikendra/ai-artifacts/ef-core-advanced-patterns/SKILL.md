---
name: ef-core-advanced-patterns
description: Master Entity Framework Core advanced patterns including change tracking optimization, lazy/eager/explicit loading strategies, query splitting, compiled queries, batch operations, optimistic concurrency, performance optimization, and PostgreSQL-specific features for .NET applications.
---

# Entity Framework Core Advanced Patterns

Master EF Core patterns for building high-performance, maintainable data access layers with PostgreSQL.

## When to Use This Skill

- Optimizing database query performance
- Eliminating N+1 query problems
- Managing change tracking efficiently
- Implementing bulk operations
- Handling concurrency conflicts
- Working with PostgreSQL-specific features
- Debugging slow EF Core queries
- Optimizing memory usage

## Core Concepts

### 1. Change Tracking Optimization

**No-Tracking Queries for Read-Only Operations:**
```csharp
// Bad: Unnecessary tracking overhead
public async Task<List<PatientDto>> GetPatientsAsync()
{
    var patients = await _dbContext.Patients.ToListAsync();
    return _mapper.Map<List<PatientDto>>(patients);
}

// Good: No tracking for read-only queries
public async Task<List<PatientDto>> GetPatientsAsync()
{
    var patients = await _dbContext.Patients
        .AsNoTracking()
        .ToListAsync();
    return _mapper.Map<List<PatientDto>>(patients);
}

// Best: Configure no-tracking at query level or globally
public class ClinicDbContext : AbpDbContext<ClinicDbContext>
{
    public ClinicDbContext(DbContextOptions<ClinicDbContext> options)
        : base(options)
    {
        // Global no-tracking (opt-in tracking when needed)
        ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }
}
```

**Identity Resolution:**
```csharp
// NoTrackingWithIdentityResolution: Tracks for query duration only
var patients = await _dbContext.Patients
    .AsNoTrackingWithIdentityResolution()
    .Include(p => p.Appointments)
        .ThenInclude(a => a.Doctor)
    .ToListAsync();
// Ensures same entity instances are used within this query
// But not tracked after query completes
```

**Change Tracker Management:**
```csharp
public async Task ProcessLargeBatchAsync()
{
    var patients = await _dbContext.Patients.ToListAsync();

    foreach (var patient in patients)
    {
        // Process patient
        patient.LastProcessedDate = DateTime.UtcNow;

        // Every 100 entities, save and clear tracker
        if (patients.IndexOf(patient) % 100 == 0)
        {
            await _dbContext.SaveChangesAsync();
            _dbContext.ChangeTracker.Clear(); // Free memory
        }
    }

    await _dbContext.SaveChangesAsync();
}
```

### 2. Loading Strategies

**Eager Loading with Include:**
```csharp
// Basic Include
var appointments = await _dbContext.Appointments
    .Include(a => a.Patient)
    .Include(a => a.Doctor)
    .ToListAsync();

// ThenInclude for nested navigation
var appointments = await _dbContext.Appointments
    .Include(a => a.Patient)
        .ThenInclude(p => p.MedicalRecords)
    .Include(a => a.Doctor)
        .ThenInclude(d => d.Specializations)
    .ToListAsync();

// Filtered Include (EF Core 5+)
var doctors = await _dbContext.Doctors
    .Include(d => d.Appointments.Where(a => a.Status == AppointmentStatus.Scheduled))
    .ToListAsync();

// Multiple navigation properties
var patients = await _dbContext.Patients
    .Include(p => p.Appointments)
    .Include(p => p.MedicalRecords)
    .Include(p => p.PrimaryDoctor)
    .ToListAsync();
```

**Explicit Loading:**
```csharp
// Load related entities on demand
var patient = await _dbContext.Patients
    .FirstOrDefaultAsync(p => p.Id == patientId);

// Explicitly load appointments
await _dbContext.Entry(patient)
    .Collection(p => p.Appointments)
    .LoadAsync();

// Explicitly load with filtering
await _dbContext.Entry(patient)
    .Collection(p => p.Appointments)
    .Query()
    .Where(a => a.AppointmentDate >= DateTime.Today)
    .LoadAsync();

// Load and count without loading all data
var appointmentCount = await _dbContext.Entry(patient)
    .Collection(p => p.Appointments)
    .Query()
    .CountAsync();
```

**Lazy Loading (Use Sparingly):**
```csharp
// Enable lazy loading (requires proxies)
public class ClinicDbContext : AbpDbContext<ClinicDbContext>
{
    public ClinicDbContext(DbContextOptions<ClinicDbContext> options)
        : base(options)
    {
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseLazyLoadingProxies();
    }
}

// Virtual navigation properties enable lazy loading
public class Patient
{
    public virtual ICollection<Appointment> Appointments { get; set; }
    // WARNING: Can cause N+1 queries if not careful
}
```

### 3. Query Splitting

**Avoid Cartesian Explosion:**
```csharp
// Bad: Single query with multiple includes causes cartesian explosion
var doctors = await _dbContext.Doctors
    .Include(d => d.Appointments)
    .Include(d => d.DoctorSchedules)
    .Include(d => d.Specializations)
    .ToListAsync();
// Results in: Doctors × Appointments × Schedules × Specializations rows

// Good: Split query to avoid cartesian product
var doctors = await _dbContext.Doctors
    .Include(d => d.Appointments)
    .Include(d => d.DoctorSchedules)
    .Include(d => d.Specializations)
    .AsSplitQuery()
    .ToListAsync();
// Executes 4 separate queries and combines results
```

**Global Split Query Configuration:**
```csharp
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    optionsBuilder
        .UseNpgsql(connectionString)
        .UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery);
}
```

### 4. Compiled Queries

**Pre-compile Frequently Used Queries:**
```csharp
public class PatientQueries
{
    // Compiled query for better performance
    private static readonly Func<ClinicDbContext, Guid, Task<Patient>> _getPatientByIdQuery =
        EF.CompileAsyncQuery((ClinicDbContext context, Guid id) =>
            context.Patients
                .Include(p => p.PrimaryDoctor)
                .FirstOrDefault(p => p.Id == id));

    private static readonly Func<ClinicDbContext, string, Task<Patient>> _getPatientByEmailQuery =
        EF.CompileAsyncQuery((ClinicDbContext context, string email) =>
            context.Patients
                .FirstOrDefault(p => p.Email == email));

    public static Task<Patient> GetByIdAsync(ClinicDbContext context, Guid id)
        => _getPatientByIdQuery(context, id);

    public static Task<Patient> GetByEmailAsync(ClinicDbContext context, string email)
        => _getPatientByEmailQuery(context, email);
}

// Usage
var patient = await PatientQueries.GetByIdAsync(_dbContext, patientId);
```

### 5. Batch Operations (EF Core 7+)

**ExecuteUpdate - Bulk Update Without Loading:**
```csharp
// Bad: Load all entities, update, save
var patients = await _dbContext.Patients
    .Where(p => p.IsActive == false)
    .ToListAsync();

foreach (var patient in patients)
{
    patient.Status = PatientStatus.Inactive;
}

await _dbContext.SaveChangesAsync();

// Good: Bulk update in single SQL statement
await _dbContext.Patients
    .Where(p => p.IsActive == false)
    .ExecuteUpdateAsync(setters => setters
        .SetProperty(p => p.Status, PatientStatus.Inactive)
        .SetProperty(p => p.LastModifiedDate, DateTime.UtcNow));

// Update with expression
await _dbContext.Appointments
    .Where(a => a.AppointmentDate < DateTime.Today && a.Status == AppointmentStatus.Scheduled)
    .ExecuteUpdateAsync(setters => setters
        .SetProperty(a => a.Status, AppointmentStatus.Expired)
        .SetProperty(a => a.Notes, a => a.Notes + " [Auto-expired]"));
```

**ExecuteDelete - Bulk Delete Without Loading:**
```csharp
// Bad: Load and delete
var oldAppointments = await _dbContext.Appointments
    .Where(a => a.AppointmentDate < DateTime.Today.AddYears(-2))
    .ToListAsync();

_dbContext.Appointments.RemoveRange(oldAppointments);
await _dbContext.SaveChangesAsync();

// Good: Bulk delete in single SQL statement
await _dbContext.Appointments
    .Where(a => a.AppointmentDate < DateTime.Today.AddYears(-2))
    .ExecuteDeleteAsync();
```

### 6. Optimistic Concurrency

**Using Row Version:**
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    [Timestamp] // or [ConcurrencyCheck]
    public byte[] RowVersion { get; set; }

    public string Name { get; set; }
    public string Email { get; set; }
}

// Handle concurrency exception
try
{
    patient.Email = "newemail@example.com";
    await _dbContext.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    var entry = ex.Entries.Single();
    var databaseValues = await entry.GetDatabaseValuesAsync();

    if (databaseValues == null)
    {
        // Entity was deleted
        throw new EntityNotFoundException();
    }

    // Reload with current database values
    await entry.ReloadAsync();

    // Or merge values
    var databasePatient = (Patient)databaseValues.ToObject();
    // Apply custom merge logic
}
```

### 7. PostgreSQL-Specific Features

**Array Operations:**
```csharp
// Model with array
public class Patient
{
    public string[] Allergies { get; set; }
    public int[] ChronicConditionCodes { get; set; }
}

// Query arrays
var patientsWithPenicillinAllergy = await _dbContext.Patients
    .Where(p => p.Allergies.Contains("Penicillin"))
    .ToListAsync();

// Array overlap
var patientsWithAnyAllergy = await _dbContext.Patients
    .Where(p => p.Allergies.Any(a => new[] { "Penicillin", "Latex" }.Contains(a)))
    .ToListAsync();

// Configure in OnModelCreating
modelBuilder.Entity<Patient>()
    .Property(p => p.Allergies)
    .HasColumnType("text[]");
```

**JSON Columns (JSONB):**
```csharp
// Model with JSON
public class MedicalRecord
{
    public Guid Id { get; set; }
    public JsonDocument Metadata { get; set; } // System.Text.Json
    // Or use custom type
    public Dictionary<string, object> CustomData { get; set; }
}

// Configure JSONB column
modelBuilder.Entity<MedicalRecord>()
    .Property(m => m.Metadata)
    .HasColumnType("jsonb");

// Query JSON properties
var records = await _dbContext.MedicalRecords
    .Where(m => EF.Functions.JsonContains(
        m.Metadata,
        @"{""diagnosis"": ""hypertension""}"))
    .ToListAsync();
```

**Full-Text Search:**
```csharp
// Configure full-text search
modelBuilder.Entity<Patient>()
    .HasGeneratedTsVectorColumn(
        p => p.SearchVector,
        "english",
        p => new { p.Name, p.Email })
    .HasIndex(p => p.SearchVector)
    .HasMethod("GIN");

public class Patient
{
    public NpgsqlTsVector SearchVector { get; set; }
}

// Search
var patients = await _dbContext.Patients
    .Where(p => p.SearchVector.Matches(EF.Functions.ToTsQuery("english", "john & doe")))
    .ToListAsync();
```

**Range Types:**
```csharp
public class DoctorSchedule
{
    public NpgsqlRange<TimeOnly> WorkingHours { get; set; }
}

// Query ranges
var schedulesAtTime = await _dbContext.DoctorSchedules
    .Where(s => s.WorkingHours.Contains(TimeOnly.FromDateTime(DateTime.Now)))
    .ToListAsync();
```

### 8. Query Optimization Techniques

**Projection to DTOs:**
```csharp
// Bad: Load entire entity when only few fields needed
var patients = await _dbContext.Patients
    .Include(p => p.Appointments)
    .ToListAsync();

var result = patients.Select(p => new PatientListDto
{
    Id = p.Id,
    Name = p.Name
}).ToList();

// Good: Project directly to DTO
var patients = await _dbContext.Patients
    .Select(p => new PatientListDto
    {
        Id = p.Id,
        Name = p.Name,
        AppointmentCount = p.Appointments.Count
    })
    .ToListAsync();
```

**Avoid Multiple Roundtrips:**
```csharp
// Bad: N+1 query problem
var appointments = await _dbContext.Appointments.ToListAsync();
foreach (var appointment in appointments)
{
    var patient = await _dbContext.Patients.FindAsync(appointment.PatientId);
    // Process...
}

// Good: Single query with Include
var appointments = await _dbContext.Appointments
    .Include(a => a.Patient)
    .ToListAsync();
```

**Use FromSqlRaw for Complex Queries:**
```csharp
// When LINQ translation is inefficient
var statistics = await _dbContext.Appointments
    .FromSqlRaw(@"
        SELECT
            a.*,
            COUNT(*) OVER (PARTITION BY a.doctor_id) as doctor_appointment_count
        FROM appointments a
        WHERE a.appointment_date >= @startDate",
        new NpgsqlParameter("@startDate", startDate))
    .ToListAsync();
```

**Query Filters for Soft Delete:**
```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Global query filter
    modelBuilder.Entity<Patient>()
        .HasQueryFilter(p => !p.IsDeleted);

    // Automatically applied to all queries
}

// Ignore filter when needed
var allPatients = await _dbContext.Patients
    .IgnoreQueryFilters()
    .ToListAsync();
```

### 9. Performance Monitoring

**Log Generated SQL:**
```csharp
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    optionsBuilder
        .UseNpgsql(connectionString)
        .LogTo(Console.WriteLine, LogLevel.Information)
        .EnableSensitiveDataLogging() // Development only
        .EnableDetailedErrors();
}
```

**Use ToQueryString for Debugging:**
```csharp
var query = _dbContext.Patients
    .Where(p => p.IsActive)
    .Include(p => p.Appointments);

var sql = query.ToQueryString();
Logger.LogInformation("Generated SQL: {Sql}", sql);
```

## Best Practices

1. **Use AsNoTracking** for read-only queries
2. **Project to DTOs** when you don't need full entities
3. **Split Queries** for multiple includes to avoid cartesian explosion
4. **Compiled Queries** for frequently executed queries
5. **Batch Operations** (ExecuteUpdate/Delete) for bulk operations
6. **Explicit Loading** when you conditionally need related data
7. **Avoid Lazy Loading** in production (causes N+1 queries)
8. **Use Query Filters** for cross-cutting concerns (soft delete, multi-tenancy)
9. **Monitor Generated SQL** to identify inefficient queries
10. **Use PostgreSQL Features** (arrays, JSONB, FTS) when appropriate

## Common Pitfalls

- **N+1 Queries**: Always use Include or explicit loading
- **Cartesian Explosion**: Use AsSplitQuery for multiple includes
- **Tracking Overhead**: Use AsNoTracking for read-only operations
- **Loading Too Much Data**: Project to DTOs instead of loading full entities
- **Lazy Loading in Loops**: Causes severe performance issues
- **Not Using Compiled Queries**: For hot paths
- **Ignoring Query Filters**: Can expose soft-deleted data

## Performance Checklist

- [ ] Read-only queries use `AsNoTracking()`
- [ ] DTOs used instead of entities for lists
- [ ] Multiple includes use `AsSplitQuery()`
- [ ] No N+1 queries (verified with SQL logging)
- [ ] Compiled queries for hot paths
- [ ] Bulk operations use ExecuteUpdate/Delete
- [ ] Appropriate indexes on database
- [ ] Query filters configured for soft delete
- [ ] Change tracker cleared in batch operations
- [ ] PostgreSQL-specific features utilized

## Resources

- **EF Core Documentation**: https://docs.microsoft.com/en-us/ef/core/
- **Performance Best Practices**: https://docs.microsoft.com/en-us/ef/core/performance/
- **Npgsql EF Core Provider**: https://www.npgsql.org/efcore/
