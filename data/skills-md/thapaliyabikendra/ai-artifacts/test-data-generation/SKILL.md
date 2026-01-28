---
name: test-data-generation
description: "Test data generation patterns using Bogus, test builders, and ABP seeders. Use when: (1) creating realistic test data, (2) implementing test data seeders, (3) building test fixtures, (4) generating fake data for development."
layer: 1
tech_stack: [csharp, dotnet, bogus, xunit]
topics: [test-data, bogus, builder-pattern, seeders, fixtures]
depends_on: []
complements: [xunit-testing-patterns, api-integration-testing]
keywords: [Bogus, Faker, TestDataBuilder, Seeder, Fixture, TestData]
---

# Test Data Generation

Generate realistic test data using Bogus, test builders, and ABP data seeders.

## When to Use

- Creating realistic fake data for tests
- Building complex object graphs for testing
- Seeding test databases
- Generating development data
- Creating deterministic test fixtures

## Bogus Faker Setup

### Installation

```xml
<PackageReference Include="Bogus" Version="35.*" />
```

### Basic Faker Configuration

```csharp
using Bogus;

public static class FakeDataGenerators
{
    // Set seed for reproducible tests
    public static int Seed { get; set; } = 12345;

    static FakeDataGenerators()
    {
        Randomizer.Seed = new Random(Seed);
    }

    public static Faker<Patient> PatientFaker => new Faker<Patient>()
        .RuleFor(p => p.Id, f => Guid.NewGuid())
        .RuleFor(p => p.FirstName, f => f.Name.FirstName())
        .RuleFor(p => p.LastName, f => f.Name.LastName())
        .RuleFor(p => p.Email, (f, p) => f.Internet.Email(p.FirstName, p.LastName))
        .RuleFor(p => p.Phone, f => f.Phone.PhoneNumber("###-###-####"))
        .RuleFor(p => p.DateOfBirth, f => f.Date.Past(80, DateTime.Today.AddYears(-18)))
        .RuleFor(p => p.Address, f => f.Address.FullAddress())
        .RuleFor(p => p.Status, f => f.PickRandom<PatientStatus>());

    public static Faker<Doctor> DoctorFaker => new Faker<Doctor>()
        .RuleFor(d => d.Id, f => Guid.NewGuid())
        .RuleFor(d => d.Name, f => $"Dr. {f.Name.FullName()}")
        .RuleFor(d => d.Specialization, f => f.PickRandom(
            "Cardiology", "Neurology", "Pediatrics", "Orthopedics"))
        .RuleFor(d => d.LicenseNumber, f => f.Random.AlphaNumeric(10).ToUpper())
        .RuleFor(d => d.YearsOfExperience, f => f.Random.Int(1, 40));

    public static Faker<Appointment> AppointmentFaker => new Faker<Appointment>()
        .RuleFor(a => a.Id, f => Guid.NewGuid())
        .RuleFor(a => a.DateTime, f => f.Date.Future(30))
        .RuleFor(a => a.Duration, f => TimeSpan.FromMinutes(f.PickRandom(15, 30, 45, 60)))
        .RuleFor(a => a.Notes, f => f.Lorem.Sentence())
        .RuleFor(a => a.Status, f => f.PickRandom<AppointmentStatus>());
}
```

### Advanced Bogus Patterns

```csharp
public static class AdvancedFakers
{
    // Faker with relationships
    public static Faker<Appointment> AppointmentWithRelationsFaker(
        Guid? patientId = null,
        Guid? doctorId = null)
    {
        return new Faker<Appointment>()
            .RuleFor(a => a.Id, f => Guid.NewGuid())
            .RuleFor(a => a.PatientId, f => patientId ?? Guid.NewGuid())
            .RuleFor(a => a.DoctorId, f => doctorId ?? Guid.NewGuid())
            .RuleFor(a => a.DateTime, f => f.Date.Future(30))
            .RuleFor(a => a.Status, AppointmentStatus.Scheduled);
    }

    // Faker with conditional rules
    public static Faker<Patient> PatientFakerWithScenario(PatientScenario scenario)
    {
        var faker = new Faker<Patient>()
            .RuleFor(p => p.Id, f => Guid.NewGuid())
            .RuleFor(p => p.Name, f => f.Name.FullName())
            .RuleFor(p => p.Email, f => f.Internet.Email());

        return scenario switch
        {
            PatientScenario.Adult => faker
                .RuleFor(p => p.DateOfBirth, f => f.Date.Past(50, DateTime.Today.AddYears(-18))),
            PatientScenario.Minor => faker
                .RuleFor(p => p.DateOfBirth, f => f.Date.Past(17, DateTime.Today.AddYears(-1))),
            PatientScenario.Elderly => faker
                .RuleFor(p => p.DateOfBirth, f => f.Date.Past(30, DateTime.Today.AddYears(-65))),
            _ => faker
        };
    }

    // Faker with locale
    public static Faker<Patient> BrazilianPatientFaker => new Faker<Patient>("pt_BR")
        .RuleFor(p => p.Name, f => f.Name.FullName())
        .RuleFor(p => p.Phone, f => f.Phone.PhoneNumber());

    // Generate unique values
    public static Faker<Patient> UniquePatientFaker => new Faker<Patient>()
        .RuleFor(p => p.Id, f => Guid.NewGuid())
        .RuleFor(p => p.Email, f => f.Internet.Email().ToLower())
        .RuleFor(p => p.SocialSecurityNumber, f => f.Random.Replace("###-##-####"));
}

public enum PatientScenario { Adult, Minor, Elderly }
```

## Test Builder Pattern

### Fluent Builder

```csharp
public class PatientBuilder
{
    private readonly Patient _patient;
    private readonly Faker _faker = new();

    public PatientBuilder()
    {
        _patient = new Patient
        {
            Id = Guid.NewGuid(),
            Name = _faker.Name.FullName(),
            Email = _faker.Internet.Email(),
            DateOfBirth = _faker.Date.Past(50, DateTime.Today.AddYears(-18)),
            Status = PatientStatus.Active
        };
    }

    public PatientBuilder WithId(Guid id)
    {
        _patient.Id = id;
        return this;
    }

    public PatientBuilder WithName(string name)
    {
        _patient.Name = name;
        return this;
    }

    public PatientBuilder WithEmail(string email)
    {
        _patient.Email = email;
        return this;
    }

    public PatientBuilder WithDateOfBirth(DateTime dob)
    {
        _patient.DateOfBirth = dob;
        return this;
    }

    public PatientBuilder AsMinor()
    {
        _patient.DateOfBirth = DateTime.Today.AddYears(-10);
        return this;
    }

    public PatientBuilder AsInactive()
    {
        _patient.Status = PatientStatus.Inactive;
        return this;
    }

    public PatientBuilder WithAppointments(int count)
    {
        _patient.Appointments = FakeDataGenerators.AppointmentFaker
            .Generate(count)
            .Select(a => { a.PatientId = _patient.Id; return a; })
            .ToList();
        return this;
    }

    public Patient Build() => _patient;

    // Implicit conversion for cleaner tests
    public static implicit operator Patient(PatientBuilder builder) => builder.Build();
}

// Usage
var patient = new PatientBuilder()
    .WithName("John Doe")
    .WithEmail("john@example.com")
    .AsMinor()
    .WithAppointments(3)
    .Build();
```

### DTO Builder

```csharp
public class CreatePatientDtoBuilder
{
    private readonly CreatePatientDto _dto;
    private readonly Faker _faker = new();

    public CreatePatientDtoBuilder()
    {
        _dto = new CreatePatientDto
        {
            Name = _faker.Name.FullName(),
            Email = _faker.Internet.Email(),
            Phone = _faker.Phone.PhoneNumber(),
            DateOfBirth = _faker.Date.Past(50, DateTime.Today.AddYears(-18))
        };
    }

    public CreatePatientDtoBuilder WithName(string name)
    {
        _dto.Name = name;
        return this;
    }

    public CreatePatientDtoBuilder WithEmail(string email)
    {
        _dto.Email = email;
        return this;
    }

    public CreatePatientDtoBuilder WithInvalidEmail()
    {
        _dto.Email = "not-an-email";
        return this;
    }

    public CreatePatientDtoBuilder WithEmptyName()
    {
        _dto.Name = "";
        return this;
    }

    public CreatePatientDto Build() => _dto;
}

// Usage in tests
[Fact]
public async Task Create_InvalidEmail_ReturnsValidationError()
{
    var input = new CreatePatientDtoBuilder()
        .WithInvalidEmail()
        .Build();

    var result = await _service.CreateAsync(input);
    // Assert...
}
```

## ABP Data Seeders

### Test Data Seeder

```csharp
public class TestDataSeeder : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly IRepository<Doctor, Guid> _doctorRepository;
    private readonly IGuidGenerator _guidGenerator;

    public TestDataSeeder(
        IRepository<Patient, Guid> patientRepository,
        IRepository<Doctor, Guid> doctorRepository,
        IGuidGenerator guidGenerator)
    {
        _patientRepository = patientRepository;
        _doctorRepository = doctorRepository;
        _guidGenerator = guidGenerator;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        if (await _patientRepository.GetCountAsync() > 0)
            return;

        // Seed deterministic test data
        var patients = CreateTestPatients();
        await _patientRepository.InsertManyAsync(patients);

        var doctors = CreateTestDoctors();
        await _doctorRepository.InsertManyAsync(doctors);
    }

    private List<Patient> CreateTestPatients()
    {
        return new List<Patient>
        {
            new Patient(TestDataIds.Patient1, "John Doe", "john@test.com",
                new DateTime(1990, 5, 15)),
            new Patient(TestDataIds.Patient2, "Jane Smith", "jane@test.com",
                new DateTime(1985, 8, 22)),
            new Patient(TestDataIds.InactivePatient, "Inactive User", "inactive@test.com",
                new DateTime(1970, 1, 1)) { Status = PatientStatus.Inactive },
            new Patient(TestDataIds.DeletablePatient, "To Be Deleted", "delete@test.com",
                new DateTime(1995, 3, 10))
        };
    }

    private List<Doctor> CreateTestDoctors()
    {
        return new List<Doctor>
        {
            new Doctor(TestDataIds.Doctor1, "Dr. House", "Diagnostics", "LIC001"),
            new Doctor(TestDataIds.Doctor2, "Dr. Wilson", "Oncology", "LIC002")
        };
    }
}

// Centralized test IDs
public static class TestDataIds
{
    public static readonly Guid Patient1 = Guid.Parse("3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d");
    public static readonly Guid Patient2 = Guid.Parse("4b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e");
    public static readonly Guid InactivePatient = Guid.Parse("5c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f");
    public static readonly Guid DeletablePatient = Guid.Parse("6d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a");
    public static readonly Guid Doctor1 = Guid.Parse("7e5f6a7b-8c9d-0e1f-2a3b-4c5d6e7f8a9b");
    public static readonly Guid Doctor2 = Guid.Parse("8f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c");
}
```

### Bulk Data Seeder for Performance Tests

```csharp
public class BulkTestDataSeeder : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public async Task SeedAsync(DataSeedContext context)
    {
        if (!context.Properties.ContainsKey("BulkSeed"))
            return;

        var count = (int)context.Properties["BulkSeed"];

        var patients = FakeDataGenerators.PatientFaker.Generate(count);

        // Batch insert for performance
        const int batchSize = 1000;
        for (int i = 0; i < patients.Count; i += batchSize)
        {
            var batch = patients.Skip(i).Take(batchSize).ToList();
            await _patientRepository.InsertManyAsync(batch);
        }
    }
}

// Usage in test
[Fact]
public async Task GetList_LargeDataset_PerformsWell()
{
    await SeedDataAsync(new DataSeedContext()
        .WithProperty("BulkSeed", 10000));

    var stopwatch = Stopwatch.StartNew();
    var result = await _service.GetListAsync(new GetPatientListDto());
    stopwatch.Stop();

    stopwatch.ElapsedMilliseconds.ShouldBeLessThan(500);
}
```

## Test Fixtures

### Shared Fixture for Integration Tests

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    public IServiceProvider Services { get; private set; }
    public ClinicDbContext DbContext { get; private set; }

    public async Task InitializeAsync()
    {
        var services = new ServiceCollection();
        services.AddDbContext<ClinicDbContext>(options =>
            options.UseInMemoryDatabase($"TestDb_{Guid.NewGuid()}"));

        Services = services.BuildServiceProvider();
        DbContext = Services.GetRequiredService<ClinicDbContext>();

        await SeedTestDataAsync();
    }

    public async Task DisposeAsync()
    {
        await DbContext.DisposeAsync();
    }

    private async Task SeedTestDataAsync()
    {
        var patients = FakeDataGenerators.PatientFaker.Generate(10);
        DbContext.Patients.AddRange(patients);
        await DbContext.SaveChangesAsync();
    }
}

// Usage
public class PatientTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public PatientTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task Test_WithSharedData()
    {
        var patients = await _fixture.DbContext.Patients.ToListAsync();
        patients.ShouldNotBeEmpty();
    }
}
```

## Quick Reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| Bogus Faker | Random realistic data | `PatientFaker.Generate(10)` |
| Builder | Fluent test object creation | `new PatientBuilder().WithName("John").Build()` |
| Data Seeder | Database test data | `IDataSeedContributor` |
| Fixture | Shared test context | `IClassFixture<T>` |

### Bogus Cheat Sheet

| Method | Purpose |
|--------|---------|
| `f.Name.FullName()` | Random full name |
| `f.Internet.Email()` | Random email |
| `f.Phone.PhoneNumber("###-###-####")` | Formatted phone |
| `f.Date.Past(years)` | Past date |
| `f.Date.Future(days)` | Future date |
| `f.Lorem.Sentence()` | Random sentence |
| `f.Random.Int(min, max)` | Random integer |
| `f.PickRandom<Enum>()` | Random enum value |
| `f.Random.AlphaNumeric(length)` | Random string |

## Related Skills

- `xunit-testing-patterns` - Test structure and assertions
- `api-integration-testing` - API test patterns
- `efcore-patterns` - Database testing
