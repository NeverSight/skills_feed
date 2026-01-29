---
name: xunit-testing-patterns
description: "Master xUnit testing patterns for ABP Framework applications including unit tests, integration tests, test data seeders, and mocking strategies. Use when: (1) writing xUnit tests for ABP services, (2) creating test data seeders, (3) implementing integration tests, (4) setting up test infrastructure."
layer: 3
tech_stack: [dotnet, csharp, xunit]
topics: [unit-testing, integration-testing, mocking, test-data, shouldly, nsubstitute, interface-first]
depends_on: [abp-framework-patterns]
complements: [e2e-testing-patterns]
keywords: [xUnit, Fact, Theory, Shouldly, NSubstitute, TestBase, DataSeeder, InlineData, Interface-First]
---

# xUnit Testing Patterns for ABP Framework

Comprehensive testing patterns for ABP Framework applications using xUnit, Shouldly, and NSubstitute.

## When to Use

- Writing unit tests for AppServices
- Creating integration tests for ABP modules
- Setting up test data seeders
- Mocking repositories and services
- Testing authorization and validation
- Writing domain service tests
- **Interface-first testing** (writing tests before implementation)

## Test Project Structure

```
{ProjectName}.TestBase/
├── {ProjectName}TestBase.cs           # Base class with common setup
├── {ProjectName}TestBaseModule.cs     # Test module configuration
└── {Feature}/
    ├── {Entity}TestData.cs            # Test constants
    └── {Entity}TestDataSeedContributor.cs  # Test data seeder

{ProjectName}.Application.Tests/
├── {ProjectName}ApplicationTestBase.cs  # Application test base
├── {ProjectName}ApplicationTestModule.cs
└── {Feature}/
    └── {Entity}AppService_Tests.cs    # AppService tests

{ProjectName}.Domain.Tests/
├── {ProjectName}DomainTestBase.cs     # Domain test base
├── {ProjectName}DomainTestModule.cs
└── {Feature}/
    └── {Entity}Manager_Tests.cs       # Domain service tests
```

## Interface-First Testing (NEW)

Write tests against interfaces **before implementation exists**. This enables parallel development in `/add-feature` workflow.

### Benefits

1. Tests can be written as soon as interface contracts exist
2. Enables true parallel execution of `abp-developer` and `qa-engineer`
3. Tests document expected behavior
4. Catches interface design issues early

### Example: Testing Against Interface

```csharp
// This test compiles and is ready to run once implementation exists
public class PatientAppService_Tests : ClinicApplicationTestBase
{
    private readonly IPatientAppService _patientAppService;

    public PatientAppService_Tests()
    {
        // Resolves implementation from DI container
        _patientAppService = GetRequiredService<IPatientAppService>();
    }

    [Fact]
    public async Task GetAsync_WithValidId_ReturnsPatient()
    {
        // Arrange - uses test data constants
        var patientId = PatientTestData.Patient1Id;

        // Act - calls interface method
        var result = await _patientAppService.GetAsync(patientId);

        // Assert - validates contract expectations
        result.ShouldNotBeNull();
        result.Id.ShouldBe(patientId);
        result.FirstName.ShouldBe(PatientTestData.Patient1FirstName);
    }
}
```

## Core Templates

### Test Data Constants

```csharp
// {ProjectName}.TestBase/{Feature}/{Entity}TestData.cs
namespace {ProjectName}.{Feature};

public static class PatientTestData
{
    // Use deterministic GUIDs for test reproducibility
    public static Guid Patient1Id { get; } = Guid.Parse("00000000-0000-0000-0001-000000000001");
    public static Guid Patient2Id { get; } = Guid.Parse("00000000-0000-0000-0001-000000000002");
    public static Guid NonExistentId { get; } = Guid.Parse("00000000-0000-0000-0001-999999999999");

    // Valid test data
    public const string Patient1FirstName = "John";
    public const string Patient1LastName = "Doe";
    public const string Patient1Email = "john.doe@example.com";

    public const string Patient2FirstName = "Jane";
    public const string Patient2LastName = "Smith";
    public const string Patient2Email = "jane.smith@example.com";

    // Valid data for create tests
    public const string ValidFirstName = "New";
    public const string ValidLastName = "Patient";
    public const string ValidEmail = "new.patient@example.com";

    // Invalid data for negative tests
    public const string EmptyString = "";
    public const string WhitespaceString = "   ";
    public static readonly string TooLongName = new('X', 256);
    public const string InvalidEmail = "not-an-email";
}
```

### Test Data Seeder

```csharp
// {ProjectName}.TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
using System;
using System.Threading.Tasks;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Domain.Repositories;

namespace {ProjectName}.{Feature};

public class PatientTestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<Patient, Guid> _repository;

    public PatientTestDataSeedContributor(IRepository<Patient, Guid> repository)
    {
        _repository = repository;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        // Idempotent seeding
        if (await _repository.GetCountAsync() > 0)
        {
            return;
        }

        // Patient 1 - Active
        await _repository.InsertAsync(
            new Patient(
                PatientTestData.Patient1Id,
                PatientTestData.Patient1FirstName,
                PatientTestData.Patient1LastName,
                PatientTestData.Patient1Email),
            autoSave: true);

        // Patient 2 - For deletion/update tests
        await _repository.InsertAsync(
            new Patient(
                PatientTestData.Patient2Id,
                PatientTestData.Patient2FirstName,
                PatientTestData.Patient2LastName,
                PatientTestData.Patient2Email),
            autoSave: true);
    }
}
```

### AppService Test Class

For full test class template with all CRUD operations, lifecycle tests, and mocking patterns:
**See [references/appservice-test-template.md](references/appservice-test-template.md)**

**Quick example:**

```csharp
[Trait("Category", "Integration")]
public class {Entity}AppService_Tests : {ProjectName}ApplicationTestBase
{
    private readonly I{Entity}AppService _{entity}AppService;

    public {Entity}AppService_Tests()
    {
        _{entity}AppService = GetRequiredService<I{Entity}AppService>();
    }

    [Fact]
    public async Task GetAsync_WithValidId_Returns{Entity}()
    {
        var result = await _{entity}AppService.GetAsync({Entity}TestData.{Entity}1Id);
        result.ShouldNotBeNull();
        result.Id.ShouldBe({Entity}TestData.{Entity}1Id);
    }

    [Fact]
    public async Task CreateAsync_WithValidInput_CreatesAndReturns{Entity}()
    {
        var input = new Create{Entity}Dto { Name = {Entity}TestData.ValidName };
        var result = await _{entity}AppService.CreateAsync(input);
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
    }
}
```

## Test Categories

### 1. Happy Path Tests
Test normal successful operations.

```csharp
[Fact]
public async Task Should_Create_Entity_Successfully()
{
    // Standard create with valid data
}
```

### 2. Validation Tests
Test input validation and constraints.

```csharp
[Theory]
[InlineData("")]
[InlineData(null)]
[InlineData("   ")]
public async Task Should_Reject_Invalid_Name(string? name)
{
    var input = new CreateDto { Name = name! };
    await Should.ThrowAsync<AbpValidationException>(
        () => _service.CreateAsync(input));
}
```

### 3. Authorization Tests
Test permission enforcement.

```csharp
[Fact]
public async Task Should_Require_Permission_To_Create()
{
    // Login as user without permission
    await WithUnitOfWorkAsync(async () =>
    {
        await Should.ThrowAsync<AbpAuthorizationException>(
            () => _service.CreateAsync(input));
    });
}
```

### 4. Edge Case Tests
Test boundary conditions and edge cases.

```csharp
[Fact]
public async Task Should_Handle_Empty_List()
{
    // Clear all data
    var result = await _service.GetListAsync(new GetListInput());
    result.TotalCount.ShouldBe(0);
    result.Items.ShouldBeEmpty();
}

[Fact]
public async Task Should_Handle_Max_Page_Size()
{
    var result = await _service.GetListAsync(
        new GetListInput { MaxResultCount = 1000 });
    result.Items.Count.ShouldBeLessThanOrEqualTo(100); // Capped
}
```

### 5. Lifecycle Tests (for Activate/Deactivate patterns)

See [references/appservice-test-template.md](references/appservice-test-template.md) for full lifecycle test examples.

## Test Traits for Organization

```csharp
// Categorize tests for selective execution
[Trait("Category", "Unit")]
[Trait("Feature", "Patients")]
public class PatientAppService_UnitTests { }

[Trait("Category", "Integration")]
[Trait("Feature", "Patients")]
public class PatientAppService_IntegrationTests { }

// Run by category:
// dotnet test --filter "Category=Unit"
// dotnet test --filter "Feature=Patients"
```

## Mocking with NSubstitute

```csharp
using NSubstitute;

// Create mock
var repository = Substitute.For<IRepository<{Entity}, Guid>>();

// Setup return value
repository.GetAsync(entityId).Returns(entity);

// Verify call
await repository.Received(1).GetAsync(entityId);
```

For full mocking examples, see [references/appservice-test-template.md](references/appservice-test-template.md).

## Shouldly Assertion Patterns

```csharp
// Null checks
result.ShouldNotBeNull();
result.ShouldBeNull();

// Equality
result.Id.ShouldBe(expectedId);
result.Name.ShouldNotBe(oldName);

// Collections
result.Items.ShouldNotBeEmpty();
result.Items.ShouldContain(x => x.Name == "Test");
result.Items.Count.ShouldBe(5);
result.Items.ShouldAllBe(x => x.IsActive);

// Numeric comparisons
result.TotalCount.ShouldBeGreaterThan(0);
result.TotalCount.ShouldBeLessThanOrEqualTo(100);
result.TotalCount.ShouldBeInRange(1, 100);

// String assertions
result.Name.ShouldStartWith("Test");
result.Email.ShouldContain("@");
result.Name.ShouldNotBeNullOrWhiteSpace();

// Boolean assertions
result.IsActive.ShouldBeTrue();
result.IsDeleted.ShouldBeFalse();

// Exception assertions
await Should.ThrowAsync<EntityNotFoundException>(
    async () => await _service.GetAsync(invalidId));

var ex = await Should.ThrowAsync<BusinessException>(
    async () => await _service.CreateAsync(input));
ex.Code.ShouldBe("DuplicateEmail");
```

## Parallel Test Safety

When tests run in parallel, ensure data isolation:

```csharp
// Use unique IDs per test class
public static class PatientTestData
{
    // Include feature identifier in GUIDs to avoid collisions
    private const string FeaturePrefix = "00000000-0000-0001";

    public static Guid Patient1Id { get; } = Guid.Parse($"{FeaturePrefix}-0001-000000000001");
    public static Guid Patient2Id { get; } = Guid.Parse($"{FeaturePrefix}-0001-000000000002");
}
```

## Test Checklist

For each AppService, verify:

- [ ] GetAsync - valid ID returns entity
- [ ] GetAsync - non-existent ID throws EntityNotFoundException
- [ ] GetListAsync - returns paginated results
- [ ] GetListAsync - respects filters
- [ ] GetListAsync - respects pagination
- [ ] CreateAsync - valid input creates entity
- [ ] CreateAsync - empty required field throws validation
- [ ] CreateAsync - exceeds max length throws validation
- [ ] UpdateAsync - valid input updates entity
- [ ] UpdateAsync - non-existent ID throws EntityNotFoundException
- [ ] DeleteAsync - valid ID deletes entity
- [ ] DeleteAsync - non-existent ID throws EntityNotFoundException
- [ ] (If applicable) ActivateAsync - activates inactive entity
- [ ] (If applicable) DeactivateAsync - deactivates active entity

## Shared Knowledge

For foundational patterns, see the shared knowledge base:

| Topic | File | Description |
|-------|------|-------------|
| Folder structure | [knowledge/conventions/folder-structure.md](../../knowledge/conventions/folder-structure.md) | Test project layout |
| Naming conventions | [knowledge/conventions/naming.md](../../knowledge/conventions/naming.md) | Test class naming |
| CRUD example | [knowledge/examples/crud-entity.md](../../knowledge/examples/crud-entity.md) | Test target example |

## References

- [references/integration-test-patterns.md](references/integration-test-patterns.md) - Advanced integration testing
- [references/test-fixtures.md](references/test-fixtures.md) - Shared test fixtures
