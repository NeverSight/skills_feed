---
name: efcore-patterns
description: "Master Entity Framework Core patterns for ABP Framework including entity configuration, DbContext, migrations, relationships, and performance optimization. Use when: (1) configuring entities with Fluent API, (2) creating migrations, (3) designing relationships, (4) implementing repository patterns."
layer: 2
tech_stack: [dotnet, csharp, efcore, postgresql]
topics: [dbcontext, migrations, relationships, fluent-api, entity-configuration, concurrency]
depends_on: [linq-optimization-patterns]
complements: [abp-framework-patterns]
keywords: [DbContext, Migration, DbSet, HasOne, HasMany, ToTable, ConfigureByConvention, Include]
---

# EF Core Patterns

Entity Framework Core patterns for ABP Framework code-first development with PostgreSQL.

## Entity Base Classes

| Base Class | Fields Included |
|------------|-----------------|
| `Entity<TKey>` | Id |
| `AuditedEntity<TKey>` | + CreationTime, CreatorId, LastModificationTime, LastModifierId |
| `FullAuditedEntity<TKey>` | + IsDeleted, DeleterId, DeletionTime |
| `AggregateRoot<TKey>` | Entity + Domain Events + Concurrency Token |
| `FullAuditedAggregateRoot<TKey>` | **Most common** - full features |

## Entity Configuration

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public string Email { get; private set; }

    private Patient() { } // For EF Core

    public Patient(Guid id, string firstName, string lastName, string email) : base(id)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: 100);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: 100);
        Email = Check.NotNullOrWhiteSpace(email, nameof(email), maxLength: 255);
    }
}
```

## Fluent API Configuration

```csharp
public class PatientConfiguration : IEntityTypeConfiguration<Patient>
{
    public void Configure(EntityTypeBuilder<Patient> builder)
    {
        builder.ToTable("Patients");
        builder.HasKey(x => x.Id);

        builder.Property(x => x.FirstName).IsRequired().HasMaxLength(100);
        builder.Property(x => x.LastName).IsRequired().HasMaxLength(100);
        builder.Property(x => x.Email).IsRequired().HasMaxLength(255);

        builder.HasIndex(x => x.Email).IsUnique();
        builder.HasQueryFilter(x => !x.IsDeleted); // ABP soft delete
    }
}
```

## Relationships

### One-to-Many (1:N)

```csharp
builder.Entity<Appointment>(b =>
{
    b.HasOne(x => x.Doctor)
        .WithMany(x => x.Appointments)
        .HasForeignKey(x => x.DoctorId)
        .OnDelete(DeleteBehavior.Restrict);
});
```

### Many-to-Many (N:N)

```csharp
// Explicit join entity (recommended for ABP)
public class DoctorSpecialization : Entity
{
    public Guid DoctorId { get; set; }
    public Guid SpecializationId { get; set; }
    public override object[] GetKeys() => new object[] { DoctorId, SpecializationId };
}

builder.Entity<DoctorSpecialization>(b =>
{
    b.HasKey(x => new { x.DoctorId, x.SpecializationId });
    b.HasOne(x => x.Doctor).WithMany(x => x.Specializations).HasForeignKey(x => x.DoctorId);
    b.HasOne(x => x.Specialization).WithMany(x => x.Doctors).HasForeignKey(x => x.SpecializationId);
});
```

### One-to-One (1:1)

```csharp
builder.Entity<PatientProfile>(b =>
{
    b.HasOne(x => x.Patient)
        .WithOne(x => x.Profile)
        .HasForeignKey<PatientProfile>(x => x.PatientId);
});
```

## Value Objects (Owned Types)

```csharp
builder.Entity<Patient>(b =>
{
    b.OwnsOne(x => x.Address, address =>
    {
        address.Property(a => a.Street).HasMaxLength(200);
        address.Property(a => a.City).HasMaxLength(100);
    });
});
```

## Migrations

```bash
# Add migration
cd api/src/ClinicManagementSystem.EntityFrameworkCore
dotnet ef migrations add AddPatientEntity --startup-project ../ClinicManagementSystem.DbMigrator

# Apply migration
dotnet run --project ../ClinicManagementSystem.DbMigrator
```

## PostgreSQL-Specific Patterns

### Data Types

```csharp
builder.Entity<AuditRecord>(b =>
{
    b.Property(x => x.Tags).HasColumnType("text[]");       // Array
    b.Property(x => x.Metadata).HasColumnType("jsonb");    // JSON
    b.Property(x => x.Id).HasDefaultValueSql("gen_random_uuid()"); // UUID
});
```

### Index Types

```csharp
builder.Entity<Patient>(b =>
{
    b.HasIndex(x => x.Email).IsUnique();                    // B-tree (default)
    b.HasIndex(x => x.Tags).HasMethod("GIN");               // GIN for arrays/jsonb
    b.HasIndex(x => x.SearchVector).HasMethod("GIN");       // Full-text search
    b.HasIndex(x => x.CreationTime).HasMethod("BRIN");      // Large tables
    b.HasIndex(x => x.Email).HasFilter("\"IsDeleted\" = false"); // Partial
});
```

### Full-Text Search

```csharp
builder.Entity<Patient>(b =>
{
    b.Property(x => x.SearchVector)
        .HasColumnType("tsvector")
        .HasComputedColumnSql(
            "to_tsvector('english', coalesce(\"FirstName\", '') || ' ' || coalesce(\"LastName\", ''))",
            stored: true);

    b.HasIndex(x => x.SearchVector).HasMethod("GIN");
});

// Query
var patients = await dbSet
    .Where(p => p.SearchVector.Matches(EF.Functions.ToTsQuery("english", searchTerm)))
    .ToListAsync();
```

## Performance Patterns

### Batch Operations (EF Core 7+)

```csharp
// Batch update
await _context.Patients
    .Where(p => p.Status == PatientStatus.Inactive)
    .ExecuteUpdateAsync(s => s.SetProperty(p => p.IsArchived, true));

// Batch delete
await _context.AuditLogs
    .Where(l => l.CreationTime < DateTime.UtcNow.AddMonths(-6))
    .ExecuteDeleteAsync();
```

### Split Queries

```csharp
var doctors = await _context.Doctors
    .Include(d => d.Appointments)
    .Include(d => d.Specializations)
    .AsSplitQuery() // Avoid Cartesian explosion
    .ToListAsync();
```

### Compiled Queries

```csharp
private static readonly Func<ClinicDbContext, Guid, Task<Patient?>> GetPatientById =
    EF.CompileAsyncQuery((ClinicDbContext context, Guid id) =>
        context.Patients.FirstOrDefault(p => p.Id == id));
```

## Global Query Filters

```csharp
// ABP automatically applies:
// - ISoftDelete: WHERE IsDeleted = false
// - IMultiTenant: WHERE TenantId = @currentTenantId

// Disable temporarily
using (_dataFilter.Disable<ISoftDelete>())
{
    var allPatients = await _patientRepository.GetListAsync();
}
```

## Concurrency Handling

```csharp
// ABP provides automatic concurrency via AggregateRoot
try
{
    await _patientRepository.UpdateAsync(patient);
}
catch (AbpDbConcurrencyException)
{
    throw new UserFriendlyException("Record modified by another user. Please refresh.");
}
```

## Quality Checklist

- [ ] Entities inherit appropriate ABP base class
- [ ] Private setters with public domain methods
- [ ] Private parameterless constructor for EF Core
- [ ] Fluent API configuration in separate class
- [ ] Indexes defined for query patterns
- [ ] Relationships have explicit delete behavior
- [ ] PostgreSQL-specific types where appropriate (jsonb, arrays)
- [ ] GIN indexes for jsonb and full-text columns

## Detailed References

For comprehensive patterns, see:
- [references/postgresql-advanced.md](references/postgresql-advanced.md)
- [references/migration-strategies.md](references/migration-strategies.md)
