---
name: abp-api-implementation
description: "Implement REST APIs in ABP Framework with AppServices, DTOs, pagination, filtering, and authorization. Use when building API endpoints for ABP applications."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [abp, rest-api, appservice, dto, pagination, filtering, authorization]
depends_on: [abp-framework-patterns]
complements: [api-design-principles, api-response-patterns, fluentvalidation-patterns]
keywords: [ABP, REST, API, AppService, DTO, PagedResultDto, Authorization, WhereIf]
---

# ABP API Implementation

Implement REST APIs in ABP Framework using AppServices, DTOs, pagination, filtering, and authorization. This skill focuses on **C# implementation** - for design principles, see `api-design-principles`.

## When to Use This Skill

- Implementing REST API endpoints in ABP AppServices
- Creating paginated and filtered list endpoints
- Setting up authorization on API endpoints
- Designing DTOs for API requests/responses
- Handling API errors and validation

## Audience

- **ABP Developers** - API implementation
- **Backend Developers** - .NET/C# patterns

> **For Design**: Use `api-design-principles` for API contract design decisions.

---

## Core Patterns

### 1. AppService with Full CRUD

```csharp
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace MyApp.Patients;

public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public PatientAppService(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;
    }

    // GET /api/app/patient/{id}
    [Authorize(MyAppPermissions.Patients.Default)]
    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // GET /api/app/patient?skipCount=0&maxResultCount=10&sorting=name&filter=john
    [Authorize(MyAppPermissions.Patients.Default)]
    public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input)
    {
        var query = await _patientRepository.GetQueryableAsync();

        // Apply filters using WhereIf pattern
        query = query
            .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
                p => p.Name.Contains(input.Filter!) ||
                     p.Email.Contains(input.Filter!))
            .WhereIf(input.Status.HasValue,
                p => p.Status == input.Status!.Value)
            .WhereIf(input.DoctorId.HasValue,
                p => p.DoctorId == input.DoctorId!.Value);

        // Get total count before pagination
        var totalCount = await AsyncExecuter.CountAsync(query);

        // Apply sorting and pagination
        query = query
            .OrderBy(input.Sorting.IsNullOrWhiteSpace() ? nameof(Patient.Name) : input.Sorting)
            .PageBy(input);

        var patients = await AsyncExecuter.ToListAsync(query);

        return new PagedResultDto<PatientDto>(
            totalCount,
            ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients)
        );
    }

    // POST /api/app/patient
    [Authorize(MyAppPermissions.Patients.Create)]
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = new Patient(
            GuidGenerator.Create(),
            input.Name,
            input.Email,
            input.DateOfBirth
        );

        await _patientRepository.InsertAsync(patient);

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // PUT /api/app/patient/{id}
    [Authorize(MyAppPermissions.Patients.Edit)]
    public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
    {
        var patient = await _patientRepository.GetAsync(id);

        patient.SetName(input.Name);
        patient.SetEmail(input.Email);
        patient.SetDateOfBirth(input.DateOfBirth);

        await _patientRepository.UpdateAsync(patient);

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // DELETE /api/app/patient/{id}
    [Authorize(MyAppPermissions.Patients.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        await _patientRepository.DeleteAsync(id);
    }
}
```

### 2. DTO Patterns

**Output DTO** (Response):
```csharp
using Volo.Abp.Application.Dtos;

namespace MyApp.Patients;

public class PatientDto : FullAuditedEntityDto<Guid>
{
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime DateOfBirth { get; set; }
    public PatientStatus Status { get; set; }
    public Guid? DoctorId { get; set; }

    // Computed property
    public int Age => DateTime.Today.Year - DateOfBirth.Year;
}
```

**Create DTO** (Input):
```csharp
namespace MyApp.Patients;

public class CreatePatientDto
{
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime DateOfBirth { get; set; }
    public Guid? DoctorId { get; set; }
}
```

**Update DTO** (Input):
```csharp
namespace MyApp.Patients;

public class UpdatePatientDto
{
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime DateOfBirth { get; set; }
    public PatientStatus Status { get; set; }
}
```

**List Input DTO** (Query Parameters):
```csharp
using Volo.Abp.Application.Dtos;

namespace MyApp.Patients;

public class GetPatientListInput : PagedAndSortedResultRequestDto
{
    // Search filter
    public string? Filter { get; set; }

    // Specific filters
    public PatientStatus? Status { get; set; }
    public Guid? DoctorId { get; set; }
    public DateTime? CreatedAfter { get; set; }
    public DateTime? CreatedBefore { get; set; }
}
```

### 3. WhereIf Pattern for Filtering

```csharp
using System.Linq.Dynamic.Core;

public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    // WhereIf - only applies condition if value is not null/empty
    query = query
        // Text search
        .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
            p => p.Name.Contains(input.Filter!) ||
                 p.Email.Contains(input.Filter!) ||
                 p.PhoneNumber.Contains(input.Filter!))

        // Enum filter
        .WhereIf(input.Status.HasValue,
            p => p.Status == input.Status!.Value)

        // Foreign key filter
        .WhereIf(input.DoctorId.HasValue,
            p => p.DoctorId == input.DoctorId!.Value)

        // Date range filter
        .WhereIf(input.CreatedAfter.HasValue,
            p => p.CreationTime >= input.CreatedAfter!.Value)
        .WhereIf(input.CreatedBefore.HasValue,
            p => p.CreationTime <= input.CreatedBefore!.Value)

        // Boolean filter
        .WhereIf(input.IsActive.HasValue,
            p => p.IsActive == input.IsActive!.Value);

    var totalCount = await AsyncExecuter.CountAsync(query);

    // Dynamic sorting with System.Linq.Dynamic.Core
    var sorting = input.Sorting.IsNullOrWhiteSpace()
        ? $"{nameof(Patient.CreationTime)} DESC"
        : input.Sorting;

    query = query.OrderBy(sorting).PageBy(input);

    var patients = await AsyncExecuter.ToListAsync(query);

    return new PagedResultDto<PatientDto>(
        totalCount,
        ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients)
    );
}
```

### 4. Authorization Patterns

**Permission-Based Authorization**:
```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    // Read permission
    [Authorize(MyAppPermissions.Patients.Default)]
    public async Task<PatientDto> GetAsync(Guid id) { ... }

    // Create permission
    [Authorize(MyAppPermissions.Patients.Create)]
    public async Task<PatientDto> CreateAsync(CreatePatientDto input) { ... }

    // Edit permission
    [Authorize(MyAppPermissions.Patients.Edit)]
    public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input) { ... }

    // Delete permission (often more restricted)
    [Authorize(MyAppPermissions.Patients.Delete)]
    public async Task DeleteAsync(Guid id) { ... }
}
```

**Programmatic Authorization Check**:
```csharp
public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
{
    // Check permission programmatically
    await AuthorizationService.CheckAsync(MyAppPermissions.Patients.Edit);

    var patient = await _patientRepository.GetAsync(id);

    // Resource-based authorization
    if (patient.DoctorId != CurrentUser.Id)
    {
        await AuthorizationService.CheckAsync(MyAppPermissions.Patients.EditAny);
    }

    // ... update logic
}
```

**Permission Definitions**:
```csharp
public static class MyAppPermissions
{
    public const string GroupName = "MyApp";

    public static class Patients
    {
        public const string Default = GroupName + ".Patients";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string EditAny = Default + ".EditAny"; // Admin only
    }
}
```

### 5. Validation with FluentValidation

```csharp
using FluentValidation;

namespace MyApp.Patients;

public class CreatePatientDtoValidator : AbstractValidator<CreatePatientDto>
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public CreatePatientDtoValidator(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;

        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required.")
            .MaximumLength(100).WithMessage("Name cannot exceed 100 characters.");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required.")
            .EmailAddress().WithMessage("Invalid email format.")
            .MustAsync(BeUniqueEmail).WithMessage("Email already exists.");

        RuleFor(x => x.DateOfBirth)
            .NotEmpty().WithMessage("Date of birth is required.")
            .LessThan(DateTime.Today).WithMessage("Date of birth must be in the past.")
            .GreaterThan(DateTime.Today.AddYears(-150)).WithMessage("Invalid date of birth.");
    }

    private async Task<bool> BeUniqueEmail(string email, CancellationToken cancellationToken)
    {
        return !await _patientRepository.AnyAsync(p => p.Email == email);
    }
}
```

### 6. Custom Endpoints

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    // Custom action: POST /api/app/patient/{id}/activate
    [HttpPost("{id}/activate")]
    [Authorize(MyAppPermissions.Patients.Edit)]
    public async Task<PatientDto> ActivateAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        patient.Activate();
        await _patientRepository.UpdateAsync(patient);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // Custom query: GET /api/app/patient/by-email?email=john@example.com
    [HttpGet("by-email")]
    [Authorize(MyAppPermissions.Patients.Default)]
    public async Task<PatientDto?> GetByEmailAsync(string email)
    {
        var patient = await _patientRepository.FirstOrDefaultAsync(p => p.Email == email);
        return patient == null ? null : ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    // Custom query with lookup data: GET /api/app/patient/lookup
    [HttpGet("lookup")]
    [Authorize(MyAppPermissions.Patients.Default)]
    public async Task<List<PatientLookupDto>> GetLookupAsync()
    {
        var patients = await _patientRepository.GetListAsync();
        return patients.Select(p => new PatientLookupDto
        {
            Id = p.Id,
            DisplayName = $"{p.Name} ({p.Email})"
        }).ToList();
    }
}
```

### 7. Interface Definition (Application.Contracts)

```csharp
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace MyApp.Patients;

public interface IPatientAppService : IApplicationService
{
    Task<PatientDto> GetAsync(Guid id);

    Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input);

    Task<PatientDto> CreateAsync(CreatePatientDto input);

    Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input);

    Task DeleteAsync(Guid id);

    // Custom methods
    Task<PatientDto> ActivateAsync(Guid id);

    Task<PatientDto?> GetByEmailAsync(string email);

    Task<List<PatientLookupDto>> GetLookupAsync();
}
```

---

## Mapperly Configuration

```csharp
using Riok.Mapperly.Abstractions;

namespace MyApp;

[Mapper]
public static partial class ApplicationMappers
{
    // Entity to DTO
    public static partial PatientDto ToDto(this Patient patient);
    public static partial List<PatientDto> ToDtoList(this List<Patient> patients);

    // DTO to Entity (for creation)
    public static partial Patient ToEntity(this CreatePatientDto dto);

    // Update Entity from DTO
    public static partial void UpdateFrom(this Patient patient, UpdatePatientDto dto);
}
```

Usage in AppService:
```csharp
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    var patient = input.ToEntity();
    patient.Id = GuidGenerator.Create();

    await _patientRepository.InsertAsync(patient);

    return patient.ToDto();
}

public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
{
    var patient = await _patientRepository.GetAsync(id);
    patient.UpdateFrom(input);
    await _patientRepository.UpdateAsync(patient);
    return patient.ToDto();
}
```

---

## Error Handling

**Business Exception**:
```csharp
using Volo.Abp;

public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    // Check business rule
    if (await _patientRepository.AnyAsync(p => p.Email == input.Email))
    {
        throw new BusinessException(MyAppDomainErrorCodes.PatientEmailAlreadyExists)
            .WithData("email", input.Email);
    }

    // ... create logic
}
```

**Error Codes**:
```csharp
public static class MyAppDomainErrorCodes
{
    public const string PatientEmailAlreadyExists = "MyApp:Patient:001";
    public const string PatientNotActive = "MyApp:Patient:002";
    public const string PatientCannotBeDeleted = "MyApp:Patient:003";
}
```

**Localization**:
```json
{
  "MyApp:Patient:001": "A patient with email '{email}' already exists.",
  "MyApp:Patient:002": "Patient is not active.",
  "MyApp:Patient:003": "Patient cannot be deleted because they have active appointments."
}
```

---

## API Routes

ABP auto-generates routes based on AppService naming:

| Method | AppService Method | Generated Route |
|--------|-------------------|-----------------|
| `GetAsync(Guid id)` | GET | `/api/app/patient/{id}` |
| `GetListAsync(input)` | GET | `/api/app/patient` |
| `CreateAsync(input)` | POST | `/api/app/patient` |
| `UpdateAsync(id, input)` | PUT | `/api/app/patient/{id}` |
| `DeleteAsync(id)` | DELETE | `/api/app/patient/{id}` |

**Custom Route Override**:
```csharp
[RemoteService(Name = "PatientApi")]
[Route("api/v1/patients")] // Custom route
public class PatientAppService : ApplicationService, IPatientAppService
{
    [HttpGet("{id:guid}")]
    public async Task<PatientDto> GetAsync(Guid id) { ... }
}
```

---

## Integration with Other Skills

| Need | Skill |
|------|-------|
| **API design decisions** | `api-design-principles` |
| **Response wrappers** | `api-response-patterns` |
| **Input validation** | `fluentvalidation-patterns` |
| **Entity design** | `abp-entity-patterns` |
| **Query optimization** | `linq-optimization-patterns` |
| **Authorization** | `openiddict-authorization` |
