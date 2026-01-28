---
name: abp-entity-patterns
description: "ABP Framework domain layer patterns including entities, aggregates, repositories, domain services, and data seeding. Use when: (1) creating entities with proper base classes, (2) implementing custom repositories, (3) writing domain services, (4) seeding data."
layer: 2
tech_stack: [dotnet, csharp, abp, efcore]
topics: [entity, aggregate, repository, domain-service, data-seeding, soft-delete]
depends_on: [csharp-advanced-patterns]
complements: [efcore-patterns, abp-service-patterns]
keywords: [Entity, AggregateRoot, Repository, DomainService, IRepository, FullAuditedAggregateRoot]
---

# ABP Entity Patterns

Domain layer patterns for ABP Framework following DDD principles.

## Architecture Layers

```
Domain.Shared    → Constants, enums, shared types
Domain           → Entities, repositories, domain services, domain events
Application.Contracts → DTOs, application service interfaces
Application      → Application services, mapper profiles
EntityFrameworkCore → DbContext, repository implementations
HttpApi          → Controllers
HttpApi.Host     → Startup, configuration
```

**Key principle**: Dependencies flow downward. Application depends on Domain, but Domain never depends on Application.

## Entity Base Classes

### Choosing the Right Base Class

| Base Class | Use When |
|------------|----------|
| `Entity<TKey>` | Simple entity, no auditing |
| `AuditedEntity<TKey>` | Need creation/modification tracking |
| `FullAuditedEntity<TKey>` | Need soft delete + full audit |
| `AggregateRoot<TKey>` | Root entity of an aggregate |
| `FullAuditedAggregateRoot<TKey>` | **Most common** - full features |

### Standard Entity Pattern

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public string Email { get; private set; }
    public DateTime DateOfBirth { get; private set; }
    public bool IsActive { get; private set; }

    // Required for EF Core
    protected Patient() { }

    // Constructor with validation
    public Patient(
        Guid id,
        string firstName,
        string lastName,
        string email,
        DateTime dateOfBirth)
        : base(id)
    {
        SetName(firstName, lastName);
        SetEmail(email);
        DateOfBirth = dateOfBirth;
        IsActive = true;
    }

    // Domain methods with validation
    public void SetName(string firstName, string lastName)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: 100);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: 100);
    }

    public void SetEmail(string email)
    {
        Email = Check.NotNullOrWhiteSpace(email, nameof(email), maxLength: 256);
    }

    public void Activate() => IsActive = true;
    public void Deactivate() => IsActive = false;
}
```

### Soft Delete

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, ISoftDelete
{
    public bool IsDeleted { get; set; }
    // ABP automatically filters out soft-deleted entities
}
```

### Multi-Tenancy

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; set; }
    // ABP automatically filters by current tenant
}
```

### Audit Fields

`FullAuditedAggregateRoot<Guid>` provides:
- `CreationTime`, `CreatorId`
- `LastModificationTime`, `LastModifierId`
- `IsDeleted`, `DeletionTime`, `DeleterId`

## Repository Pattern

### Generic Repository Usage

```csharp
public class PatientAppService : ApplicationService
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public PatientAppService(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;
    }

    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    public async Task<PagedResultDto<PatientDto>> GetListAsync(PagedAndSortedResultRequestDto input)
    {
        var totalCount = await _patientRepository.GetCountAsync();
        var queryable = await _patientRepository.GetQueryableAsync();

        var patients = await AsyncExecuter.ToListAsync(
            queryable
                .OrderBy(input.Sorting ?? nameof(Patient.FirstName))
                .PageBy(input.SkipCount, input.MaxResultCount));

        return new PagedResultDto<PatientDto>(
            totalCount,
            ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients));
    }
}
```

### Custom Repository

**Define interface in Domain layer:**
```csharp
public interface IPatientRepository : IRepository<Patient, Guid>
{
    Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId);
    Task<Patient?> FindByEmailAsync(string email);
}
```

**Implement in EntityFrameworkCore layer:**
```csharp
public class PatientRepository : EfCoreRepository<ClinicDbContext, Patient, Guid>, IPatientRepository
{
    public PatientRepository(IDbContextProvider<ClinicDbContext> dbContextProvider)
        : base(dbContextProvider)
    {
    }

    public async Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId)
    {
        var dbSet = await GetDbSetAsync();
        return await dbSet
            .Where(p => p.PrimaryDoctorId == doctorId && p.IsActive)
            .Include(p => p.Appointments)
            .ToListAsync();
    }

    public async Task<Patient?> FindByEmailAsync(string email)
    {
        var dbSet = await GetDbSetAsync();
        return await dbSet.FirstOrDefaultAsync(p => p.Email == email);
    }
}
```

## Domain Services

Use domain services when business logic involves multiple entities or external domain concepts.

```csharp
public class AppointmentManager : DomainService
{
    private readonly IRepository<Appointment, Guid> _appointmentRepository;
    private readonly IRepository<DoctorSchedule, Guid> _scheduleRepository;

    public AppointmentManager(
        IRepository<Appointment, Guid> appointmentRepository,
        IRepository<DoctorSchedule, Guid> scheduleRepository)
    {
        _appointmentRepository = appointmentRepository;
        _scheduleRepository = scheduleRepository;
    }

    public async Task<Appointment> CreateAsync(
        Guid patientId,
        Guid doctorId,
        DateTime appointmentDate,
        string description)
    {
        // Business rule: Check if doctor is available
        await CheckDoctorAvailabilityAsync(doctorId, appointmentDate);

        // Business rule: Check for conflicts
        await CheckAppointmentConflictsAsync(doctorId, appointmentDate);

        var appointment = new Appointment(
            GuidGenerator.Create(),
            patientId,
            doctorId,
            appointmentDate,
            description);

        return await _appointmentRepository.InsertAsync(appointment);
    }

    private async Task CheckDoctorAvailabilityAsync(Guid doctorId, DateTime appointmentDate)
    {
        var schedule = await _scheduleRepository.FirstOrDefaultAsync(
            s => s.DoctorId == doctorId && s.DayOfWeek == appointmentDate.DayOfWeek);

        if (schedule == null)
            throw new BusinessException("Doctor not available on this day");

        var timeOfDay = appointmentDate.TimeOfDay;
        if (timeOfDay < schedule.StartTime || timeOfDay > schedule.EndTime)
            throw new BusinessException("Doctor not available at this time");
    }

    private async Task CheckAppointmentConflictsAsync(Guid doctorId, DateTime appointmentDate)
    {
        var hasConflict = await _appointmentRepository.AnyAsync(a =>
            a.DoctorId == doctorId &&
            a.AppointmentDate == appointmentDate &&
            a.Status != AppointmentStatus.Cancelled);

        if (hasConflict)
            throw new BusinessException("Doctor already has an appointment at this time");
    }
}
```

## Data Seeding

### IDataSeedContributor Pattern

```csharp
public class ClinicDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<Doctor, Guid> _doctorRepository;
    private readonly IGuidGenerator _guidGenerator;

    public ClinicDataSeedContributor(
        IRepository<Doctor, Guid> doctorRepository,
        IGuidGenerator guidGenerator)
    {
        _doctorRepository = doctorRepository;
        _guidGenerator = guidGenerator;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        // Idempotent check
        if (await _doctorRepository.GetCountAsync() > 0)
            return;

        var doctors = new List<Doctor>
        {
            new Doctor(_guidGenerator.Create(), "Dr. Smith", "Cardiology", "smith@clinic.com"),
            new Doctor(_guidGenerator.Create(), "Dr. Jones", "Pediatrics", "jones@clinic.com"),
        };

        foreach (var doctor in doctors)
        {
            await _doctorRepository.InsertAsync(doctor);
        }
    }
}
```

### Test Data Seeding

```csharp
public class ClinicTestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    public static readonly Guid TestPatientId = Guid.Parse("2e701e62-0953-4dd3-910b-dc6cc93ccb0d");
    public static readonly Guid TestDoctorId = Guid.Parse("3a801f73-1064-5ee4-a21c-ed7dd4ddc1e");

    public async Task SeedAsync(DataSeedContext context)
    {
        await _patientRepository.InsertAsync(new Patient(
            TestPatientId, "Test", "Patient", "test@example.com", DateTime.Now.AddYears(-30)));

        await _doctorRepository.InsertAsync(new Doctor(
            TestDoctorId, "Test Doctor", "General", "doctor@example.com"));
    }
}
```

## Best Practices

1. **Encapsulate state** - Use private setters and domain methods
2. **Validate in constructor** - Ensure entity is always valid
3. **Use value objects** - For complex properties (Address, Money)
4. **Domain logic in entity** - Simple rules belong in the entity
5. **Domain service** - For cross-entity logic
6. **Custom repository** - Only when you need custom queries
7. **Idempotent seeding** - Always check before inserting

## Related Skills

- `abp-service-patterns` - Application layer patterns
- `abp-infrastructure-patterns` - Cross-cutting concerns
- `efcore-patterns` - Database configuration
