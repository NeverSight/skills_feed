---
name: abp-contract-scaffolding
description: "Generate ABP Application.Contracts layer scaffolding (interfaces, DTOs, permissions) from technical design. Enables parallel development by abp-developer and qa-engineer. Use when: (1) backend-architect needs to generate contracts, (2) preparing for parallel implementation workflow, (3) creating API contracts before implementation."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [interface, dto, contracts, scaffolding, permissions]
depends_on: [abp-framework-patterns]
complements: [technical-design-patterns, api-design-principles]
keywords: [IAppService, Dto, CreateDto, UpdateDto, GetListInput, Permissions, Contracts]
---

# ABP Contract Scaffolding

Generate Application.Contracts layer code to enable parallel development workflows.

## Purpose

Contract scaffolding separates **interface design** from **implementation**, enabling:
- `abp-developer` to implement against defined interfaces
- `qa-engineer` to write tests against interfaces (before implementation exists)
- True parallel execution in `/add-feature` workflow

## When to Use

- Backend-architect creating technical design with contract generation
- Preparing for parallel implementation and testing
- Defining API contracts before implementation starts
- Interface-first development approach

## Project Structure

```
{Project}.Application.Contracts/
├── {Feature}/
│   ├── I{Entity}AppService.cs      # Service interface
│   ├── {Entity}Dto.cs              # Output DTO
│   ├── Create{Entity}Dto.cs        # Create input
│   ├── Update{Entity}Dto.cs        # Update input
│   └── Get{Entity}sInput.cs        # List filter/pagination
└── Permissions/
    └── {Entity}Permissions.cs      # Permission constants
```

## Templates

### 1. Service Interface

```csharp
using System;
using System.Threading.Tasks;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace {ProjectName}.{Feature};

/// <summary>
/// Application service interface for {Entity} management.
/// </summary>
public interface I{Entity}AppService : IApplicationService
{
    /// <summary>
    /// Gets a paginated list of {entities}.
    /// </summary>
    Task<PagedResultDto<{Entity}Dto>> GetListAsync(Get{Entity}sInput input);

    /// <summary>
    /// Gets a single {entity} by ID.
    /// </summary>
    Task<{Entity}Dto> GetAsync(Guid id);

    /// <summary>
    /// Creates a new {entity}.
    /// </summary>
    Task<{Entity}Dto> CreateAsync(Create{Entity}Dto input);

    /// <summary>
    /// Updates an existing {entity}.
    /// </summary>
    Task<{Entity}Dto> UpdateAsync(Guid id, Update{Entity}Dto input);

    /// <summary>
    /// Deletes a {entity} by ID.
    /// </summary>
    Task DeleteAsync(Guid id);
}
```

### 2. Output DTO

```csharp
using System;
using Volo.Abp.Application.Dtos;

namespace {ProjectName}.{Feature};

/// <summary>
/// DTO for {Entity} output.
/// Inherits audit fields from FullAuditedEntityDto.
/// </summary>
public class {Entity}Dto : FullAuditedEntityDto<Guid>
{
    /// <summary>
    /// {Property description}
    /// </summary>
    public {Type} {PropertyName} { get; set; }

    // Add properties matching entity definition
}
```

### 3. Create Input DTO

```csharp
using System;

namespace {ProjectName}.{Feature};

/// <summary>
/// DTO for creating a new {Entity}.
/// Validation is handled by FluentValidation in Application layer.
/// </summary>
public class Create{Entity}Dto
{
    /// <summary>
    /// {Property description}
    /// </summary>
    /// <remarks>Required. Max length: {N} characters.</remarks>
    public string {PropertyName} { get; set; } = string.Empty;

    // Add required properties for creation
}
```

### 4. Update Input DTO

```csharp
using System;

namespace {ProjectName}.{Feature};

/// <summary>
/// DTO for updating an existing {Entity}.
/// Validation is handled by FluentValidation in Application layer.
/// </summary>
public class Update{Entity}Dto
{
    /// <summary>
    /// {Property description}
    /// </summary>
    public string {PropertyName} { get; set; } = string.Empty;

    // Add updatable properties
}
```

### 5. List Filter Input DTO

```csharp
using Volo.Abp.Application.Dtos;

namespace {ProjectName}.{Feature};

/// <summary>
/// Input DTO for filtering and paginating {Entity} list.
/// </summary>
public class Get{Entity}sInput : PagedAndSortedResultRequestDto
{
    /// <summary>
    /// Optional text filter for searching by name or description.
    /// </summary>
    public string? Filter { get; set; }

    /// <summary>
    /// Optional filter by active status.
    /// </summary>
    public bool? IsActive { get; set; }

    // Add entity-specific filters
}
```

### 6. Permission Constants

```csharp
namespace {ProjectName}.Permissions;

/// <summary>
/// Permission constants for {Entity} management.
/// These are registered in {ProjectName}PermissionDefinitionProvider.
/// </summary>
public static class {Entity}Permissions
{
    /// <summary>
    /// Permission group name.
    /// </summary>
    public const string GroupName = "{ProjectName}.{Entities}";

    /// <summary>
    /// Default permission (view/list).
    /// </summary>
    public const string Default = GroupName;

    /// <summary>
    /// Permission to create new {entities}.
    /// </summary>
    public const string Create = GroupName + ".Create";

    /// <summary>
    /// Permission to edit existing {entities}.
    /// </summary>
    public const string Edit = GroupName + ".Edit";

    /// <summary>
    /// Permission to delete {entities}.
    /// </summary>
    public const string Delete = GroupName + ".Delete";
}
```

## Common Patterns

### Activation/Deactivation Pattern

When entity supports activation lifecycle:

```csharp
// In interface
Task<{Entity}Dto> ActivateAsync(Guid id);
Task<{Entity}Dto> DeactivateAsync(Guid id);

// In permissions
public const string Activate = GroupName + ".Activate";
public const string Deactivate = GroupName + ".Deactivate";

// In filter DTO
public bool? IsActive { get; set; }
```

### Hierarchical Entity Pattern

When entity has parent-child relationships:

```csharp
// In output DTO
public Guid? ParentId { get; set; }
public string? ParentName { get; set; }
public List<{Entity}Dto> Children { get; set; } = new();

// In interface
Task<List<{Entity}Dto>> GetChildrenAsync(Guid parentId);
Task MoveAsync(Guid id, Guid? newParentId);

// In filter DTO
public Guid? ParentId { get; set; }
public bool IncludeChildren { get; set; }
```

### Lookup/Reference Pattern

For dropdown lists and references:

```csharp
// Lightweight DTO for dropdowns
public class {Entity}LookupDto
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
}

// In interface
Task<List<{Entity}LookupDto>> GetLookupAsync();
```

### Bulk Operations Pattern

When bulk operations are needed:

```csharp
// In interface
Task<int> DeleteManyAsync(List<Guid> ids);
Task<List<{Entity}Dto>> CreateManyAsync(List<Create{Entity}Dto> inputs);

// In permissions
public const string DeleteMany = GroupName + ".DeleteMany";
```

## Generation Checklist

When generating contracts, verify:

- [ ] Interface extends `IApplicationService`
- [ ] All DTOs in correct namespace `{ProjectName}.{Feature}`
- [ ] Output DTO extends `FullAuditedEntityDto<Guid>` (or appropriate base)
- [ ] Filter DTO extends `PagedAndSortedResultRequestDto`
- [ ] Permission constants follow `{Project}.{Resource}.{Action}` pattern
- [ ] XML documentation comments included
- [ ] Properties match technical design specification
- [ ] Required vs optional properties marked correctly
- [ ] Collection properties initialized (`= new()` or `= []`)

## Integration with /add-feature

This skill is used by `backend-architect` agent in Phase 1 of `/add-feature`:

```
Phase 1: backend-architect generates:
├── docs/features/{feature}/technical-design.md
├── Application.Contracts/{Feature}/I{Entity}AppService.cs
├── Application.Contracts/{Feature}/{Entity}Dto.cs
├── Application.Contracts/{Feature}/Create{Entity}Dto.cs
├── Application.Contracts/{Feature}/Update{Entity}Dto.cs
├── Application.Contracts/{Feature}/Get{Entity}sInput.cs
└── Application.Contracts/Permissions/{Entity}Permissions.cs

Phase 2 (parallel):
├── abp-developer: Implements against interface
└── qa-engineer: Writes tests against interface
```

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `I{Entity}AppService` | `IBookAppService` |
| Output DTO | `{Entity}Dto` | `BookDto` |
| Create DTO | `Create{Entity}Dto` | `CreateBookDto` |
| Update DTO | `Update{Entity}Dto` | `UpdateBookDto` |
| Filter DTO | `Get{Entity}sInput` | `GetBooksInput` |
| Lookup DTO | `{Entity}LookupDto` | `BookLookupDto` |
| Permissions | `{Entity}Permissions` | `BookPermissions` |

## Related Skills

- `abp-framework-patterns` - Full ABP patterns including implementation
- `technical-design-patterns` - Technical design document templates
- `api-design-principles` - REST API design best practices
