---
name: abp-service-patterns
description: "ABP Framework application layer patterns including AppServices, DTOs, Mapperly mapping, Unit of Work, and common patterns like Filter DTOs and ResponseModel. Use when: (1) creating AppServices, (2) mapping DTOs with Mapperly, (3) implementing list filtering, (4) wrapping API responses."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [appservice, dto, mapperly, unit-of-work, filter-dto, response-model]
depends_on: [csharp-advanced-patterns, dotnet-async-patterns]
complements: [abp-entity-patterns, fluentvalidation-patterns]
keywords: [AppService, ApplicationService, DTO, Mapperly, UnitOfWork, PagedResultDto, WhereIf]
---

# ABP Service Patterns

Application layer patterns for ABP Framework.

## Application Service Pattern

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly PatientManager _patientManager;  // Domain service
    private readonly ClinicApplicationMappers _mapper;

    public PatientAppService(
        IRepository<Patient, Guid> patientRepository,
        PatientManager patientManager,
        ClinicApplicationMappers mapper)
    {
        _patientRepository = patientRepository;
        _patientManager = patientManager;
        _mapper = mapper;
    }

    [Authorize(ClinicPermissions.Patients.Default)]
    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        return _mapper.PatientToDto(patient);
    }

    [Authorize(ClinicPermissions.Patients.Create)]
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = await _patientManager.CreateAsync(
            input.FirstName, input.LastName, input.Email, input.DateOfBirth);
        return _mapper.PatientToDto(patient);
    }

    [Authorize(ClinicPermissions.Patients.Edit)]
    public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
    {
        var patient = await _patientRepository.GetAsync(id);
        _mapper.UpdatePatientFromDto(input, patient);
        await _patientRepository.UpdateAsync(patient);
        return _mapper.PatientToDto(patient);
    }

    [Authorize(ClinicPermissions.Patients.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        await _patientRepository.DeleteAsync(id);
    }
}
```

## Object Mapping with Mapperly

ABP 10.x uses **Mapperly** (source generator) instead of AutoMapper.

```csharp
// Application/ClinicApplicationMappers.cs
[Mapper]
public partial class ClinicApplicationMappers
{
    // Entity to DTO
    public partial PatientDto PatientToDto(Patient patient);
    public partial List<PatientDto> PatientsToDtos(List<Patient> patients);

    // DTO to Entity (creation)
    public partial Patient CreateDtoToPatient(CreatePatientDto dto);

    // DTO to Entity (update) - ignores Id
    [MapperIgnoreTarget(nameof(Patient.Id))]
    public partial void UpdatePatientFromDto(UpdatePatientDto dto, Patient patient);

    // Complex mapping with navigation properties
    [MapProperty(nameof(Appointment.Patient.FirstName), nameof(AppointmentDto.PatientName))]
    [MapProperty(nameof(Appointment.Doctor.FullName), nameof(AppointmentDto.DoctorName))]
    public partial AppointmentDto AppointmentToDto(Appointment appointment);
}
```

**Register in Module:**
```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddSingleton<ClinicApplicationMappers>();
}
```

## Unit of Work

ABP automatically manages UoW for application service methods.

```csharp
public class AppointmentAppService : ApplicationService
{
    // This method is automatically wrapped in a UoW
    // All changes are committed together or rolled back on exception
    public async Task<AppointmentDto> CreateAsync(CreateAppointmentDto input)
    {
        var patient = await _patientRepository.GetAsync(input.PatientId);
        patient.LastAppointmentDate = input.AppointmentDate;

        var appointment = new Appointment(
            GuidGenerator.Create(),
            input.PatientId,
            input.DoctorId,
            input.AppointmentDate);

        await _appointmentRepository.InsertAsync(appointment);

        // Both changes committed together automatically
        return _mapper.AppointmentToDto(appointment);
    }
}
```

**Manual UoW Control:**
```csharp
[UnitOfWork(isTransactional: false)]  // Disable for read-only
public async Task GenerateLargeReportAsync() { }

public async Task ProcessBatchAsync(List<Guid> ids)
{
    foreach (var id in ids)
    {
        using (var uow = _unitOfWorkManager.Begin(requiresNew: true))
        {
            await ProcessItemAsync(id);
            await uow.CompleteAsync();
        }
    }
}
```

## Filter DTO Pattern

Separate query filters from pagination for clean, self-documenting APIs.

**Filter DTO:**
```csharp
public class PatientFilter
{
    public Guid? DoctorId { get; set; }
    public string? Name { get; set; }
    public string? Email { get; set; }
    public bool? IsActive { get; set; }
    public DateTime? CreatedAfter { get; set; }
    public DateTime? CreatedBefore { get; set; }
}
```

**AppService with WhereIf:**
```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(
    PagedAndSortedResultRequestDto input,
    PatientFilter filter)
{
    // Trim string inputs
    filter.Name = filter.Name?.Trim();
    filter.Email = filter.Email?.Trim();

    // Default sorting
    if (input.Sorting.IsNullOrWhiteSpace())
        input.Sorting = nameof(PatientDto.FirstName);

    var queryable = await _patientRepository.GetQueryableAsync();

    var query = queryable
        .WhereIf(filter.DoctorId.HasValue, x => x.DoctorId == filter.DoctorId)
        .WhereIf(!filter.Name.IsNullOrWhiteSpace(),
            x => x.FirstName.Contains(filter.Name) || x.LastName.Contains(filter.Name))
        .WhereIf(!filter.Email.IsNullOrWhiteSpace(),
            x => x.Email.ToLower().Contains(filter.Email.ToLower()))
        .WhereIf(filter.IsActive.HasValue, x => x.IsActive == filter.IsActive)
        .WhereIf(filter.CreatedAfter.HasValue, x => x.CreationTime >= filter.CreatedAfter)
        .WhereIf(filter.CreatedBefore.HasValue, x => x.CreationTime <= filter.CreatedBefore);

    var totalCount = await AsyncExecuter.CountAsync(query);

    var patients = await AsyncExecuter.ToListAsync(
        query.OrderBy(input.Sorting).PageBy(input.SkipCount, input.MaxResultCount));

    return new PagedResultDto<PatientDto>(totalCount, _mapper.PatientsToDtos(patients));
}
```

## ResponseModel Wrapper

```csharp
public class ResponseModel<T>
{
    public bool IsSuccess { get; set; }
    public T Data { get; set; }
    public string Message { get; set; }

    public static ResponseModel<T> Success(T data, string message = null)
        => new() { IsSuccess = true, Data = data, Message = message };

    public static ResponseModel<T> Failure(string message)
        => new() { IsSuccess = false, Message = message };
}

// Usage
public async Task<ResponseModel<PatientDto>> GetAsync(Guid id)
{
    var patient = await _patientRepository.FirstOrDefaultAsync(x => x.Id == id);
    if (patient == null)
        return ResponseModel<PatientDto>.Failure("Patient not found");

    return ResponseModel<PatientDto>.Success(_mapper.PatientToDto(patient));
}
```

## CommonDependencies Pattern

Reduce constructor bloat by grouping cross-cutting dependencies.

```csharp
public class CommonDependencies<T>
{
    public IDistributedEventBus DistributedEventBus { get; set; }
    public IDataFilter DataFilter { get; set; }
    public ILogger<T> Logger { get; set; }
    public IGuidGenerator GuidGenerator { get; set; }
}

// Register
context.Services.AddTransient(typeof(CommonDependencies<>));

// Usage
public class PatientAppService : ApplicationService
{
    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly CommonDependencies<PatientAppService> _common;

    public PatientAppService(
        IRepository<Patient, Guid> patientRepository,
        CommonDependencies<PatientAppService> common)
    {
        _patientRepository = patientRepository;
        _common = common;
    }

    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        _common.Logger.LogInformation("Creating patient: {Name}", input.FirstName);
        var patient = new Patient(_common.GuidGenerator.Create(), /*...*/);
        await _patientRepository.InsertAsync(patient);
        await _common.DistributedEventBus.PublishAsync(new PatientCreatedEto { Id = patient.Id });
        return _mapper.PatientToDto(patient);
    }
}
```

## Structured Logging

```csharp
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    _logger.LogInformation(
        "[{Service}] {Method} - Started - Input: {@Input}",
        nameof(PatientAppService), nameof(CreateAsync), input);

    try
    {
        var patient = await _patientManager.CreateAsync(/*...*/);

        _logger.LogInformation(
            "[{Service}] {Method} - Completed - PatientId: {PatientId}",
            nameof(PatientAppService), nameof(CreateAsync), patient.Id);

        return _mapper.PatientToDto(patient);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex,
            "[{Service}] {Method} - Failed - Error: {Message}",
            nameof(PatientAppService), nameof(CreateAsync), ex.Message);
        throw;
    }
}
```

## Input Sanitization

```csharp
public static class InputSanitization
{
    public static string TrimAndLower(this string value) => value?.Trim()?.ToLowerInvariant();
    public static string TrimAndUpper(this string value) => value?.Trim()?.ToUpperInvariant();
}

// Usage
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    input.Email = input.Email.TrimAndLower();
    input.FirstName = input.FirstName?.Trim();
    // ...
}
```

## Mapping Validation Patterns

### Common Bug: Copy-Paste Property Mapping

Manual mappings (especially in `select new` clauses) are prone to copy-paste errors:

```csharp
// ❌ BUG: Wrong property copied - IsPutawayCompleted mapped from wrong source!
select new LicensePlateDto()
{
    IsInboundQCChecklistCompleted = lc.IsInboundQCChecklistCompleted,
    IsPutawayCompleted = lc.IsInboundQCChecklistCompleted,  // BUG! Should be lc.IsPutawayCompleted
    IsHold = lc.IsHold
}

// ✅ CORRECT: Use Mapperly to prevent copy-paste errors
[Mapper]
public partial class LicensePlateMapper
{
    public partial LicensePlateDto ToDto(LicensePlate entity);
}

// Or if manual mapping is required, double-check similar-named properties
select new LicensePlateDto()
{
    IsInboundQCChecklistCompleted = lc.IsInboundQCChecklistCompleted,
    IsPutawayCompleted = lc.IsPutawayCompleted,  // ✅ Correct property
    IsHold = lc.IsHold
}
```

### Manual Mapping Checklist

When manual mapping is unavoidable (e.g., complex projections), verify:

- [ ] Each DTO property maps to the **correct** entity property
- [ ] Similar-named properties double-checked (e.g., `IsXxxCompleted` vs `IsYyyCompleted`)
- [ ] Null checks on optional navigation properties
- [ ] No copy-paste from adjacent lines without modification

### High-Risk Property Patterns

Be extra careful with these patterns that look similar:

| DTO Property | Wrong Source | Correct Source |
|--------------|--------------|----------------|
| `IsPutawayCompleted` | `entity.IsInboundCompleted` | `entity.IsPutawayCompleted` |
| `UpdatedAt` | `entity.CreatedAt` | `entity.LastModificationTime` |
| `CustomerName` | `entity.ShipperName` | `entity.CustomerName` |
| `TargetDate` | `entity.SourceDate` | `entity.TargetDate` |

## Best Practices

1. **Thin AppServices** - Orchestrate, don't implement business logic
2. **Delegate to Domain** - Use domain services for complex rules
3. **Use Mapperly** - Source-generated mapping for performance (prevents copy-paste bugs)
4. **WhereIf pattern** - Clean optional filtering
5. **Structured logging** - Consistent format for tracing
6. **Input sanitization** - Trim and normalize inputs
7. **Authorization** - Always check permissions
8. **Verify manual mappings** - Double-check similar-named property assignments

## Related Skills

- `abp-entity-patterns` - Domain layer patterns
- `abp-infrastructure-patterns` - Cross-cutting concerns
- `fluentvalidation-patterns` - Input validation
