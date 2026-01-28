---
name: abp-infrastructure-patterns
description: "ABP Framework cross-cutting patterns including authorization, background jobs, distributed events, multi-tenancy, and module configuration. Use when: (1) defining permissions, (2) creating background jobs, (3) publishing/handling distributed events, (4) configuring modules."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [authorization, permissions, background-jobs, distributed-events, multi-tenancy, module]
depends_on: [csharp-advanced-patterns]
complements: [abp-entity-patterns, abp-service-patterns, openiddict-authorization]
keywords: [Authorize, Permission, BackgroundJob, DistributedEvent, IMultiTenant, AbpModule]
---

# ABP Infrastructure Patterns

Cross-cutting concerns and infrastructure patterns for ABP Framework.

## Authorization & Permissions

### Define Permissions

```csharp
// Domain.Shared/Permissions/ClinicPermissions.cs
public static class ClinicPermissions
{
    public const string GroupName = "Clinic";

    public static class Patients
    {
        public const string Default = GroupName + ".Patients";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
    }

    public static class Appointments
    {
        public const string Default = GroupName + ".Appointments";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string ViewAll = Default + ".ViewAll";  // Admins only
    }
}
```

### Register Permissions

```csharp
// Application.Contracts/Permissions/ClinicPermissionDefinitionProvider.cs
public class ClinicPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var clinicGroup = context.AddGroup(ClinicPermissions.GroupName);

        var patients = clinicGroup.AddPermission(
            ClinicPermissions.Patients.Default,
            L("Permission:Patients"));

        patients.AddChild(ClinicPermissions.Patients.Create, L("Permission:Patients.Create"));
        patients.AddChild(ClinicPermissions.Patients.Edit, L("Permission:Patients.Edit"));
        patients.AddChild(ClinicPermissions.Patients.Delete, L("Permission:Patients.Delete"));

        var appointments = clinicGroup.AddPermission(
            ClinicPermissions.Appointments.Default,
            L("Permission:Appointments"));

        appointments.AddChild(ClinicPermissions.Appointments.Create, L("Permission:Appointments.Create"));
        appointments.AddChild(ClinicPermissions.Appointments.ViewAll, L("Permission:Appointments.ViewAll"));
    }

    private static LocalizableString L(string name)
        => LocalizableString.Create<ClinicResource>(name);
}
```

### Use Permissions

```csharp
// Declarative
[Authorize(ClinicPermissions.Patients.Create)]
public async Task<PatientDto> CreateAsync(CreatePatientDto input) { }

// Imperative
public async Task<AppointmentDto> GetAsync(Guid id)
{
    var appointment = await _appointmentRepository.GetAsync(id);

    if (appointment.DoctorId != CurrentUser.Id)
    {
        await AuthorizationService.CheckAsync(ClinicPermissions.Appointments.ViewAll);
    }

    return _mapper.AppointmentToDto(appointment);
}

// Check without throwing
public async Task<bool> CanCreatePatientAsync()
    => await AuthorizationService.IsGrantedAsync(ClinicPermissions.Patients.Create);
```

## Background Jobs

### Define Job

```csharp
public class AppointmentReminderJob : AsyncBackgroundJob<AppointmentReminderArgs>, ITransientDependency
{
    private readonly IRepository<Appointment, Guid> _appointmentRepository;
    private readonly IEmailSender _emailSender;

    public AppointmentReminderJob(
        IRepository<Appointment, Guid> appointmentRepository,
        IEmailSender emailSender)
    {
        _appointmentRepository = appointmentRepository;
        _emailSender = emailSender;
    }

    public override async Task ExecuteAsync(AppointmentReminderArgs args)
    {
        var appointment = await _appointmentRepository.GetAsync(args.AppointmentId);

        await _emailSender.SendAsync(
            appointment.Patient.Email,
            "Appointment Reminder",
            $"You have an appointment on {appointment.AppointmentDate}");
    }
}

public class AppointmentReminderArgs
{
    public Guid AppointmentId { get; set; }
}
```

### Enqueue Job

```csharp
public async Task<AppointmentDto> CreateAsync(CreateAppointmentDto input)
{
    var appointment = await _appointmentManager.CreateAsync(/*...*/);

    // Schedule reminder 24 hours before
    var reminderTime = appointment.AppointmentDate.AddHours(-24);

    await _backgroundJobManager.EnqueueAsync(
        new AppointmentReminderArgs { AppointmentId = appointment.Id },
        delay: reminderTime - DateTime.Now);

    return _mapper.AppointmentToDto(appointment);
}
```

## Distributed Events

### Publish Event

```csharp
// From entity (recommended for domain events)
public class Patient : AggregateRoot<Guid>
{
    public void Activate()
    {
        IsActive = true;
        AddDistributedEvent(new PatientActivatedEto
        {
            Id = Id,
            Name = Name,
            Email = Email
        });
    }
}

// From application service
public async Task ActivateAsync(Guid id)
{
    var patient = await _patientRepository.GetAsync(id);
    patient.Activate();

    // Or manually publish:
    await _distributedEventBus.PublishAsync(new PatientActivatedEto
    {
        Id = patient.Id,
        Name = patient.Name,
        Email = patient.Email
    });
}
```

### Handle Event

```csharp
public class PatientActivatedEventHandler :
    IDistributedEventHandler<PatientActivatedEto>,
    ITransientDependency
{
    private readonly IEmailSender _emailSender;
    private readonly ILogger<PatientActivatedEventHandler> _logger;

    public PatientActivatedEventHandler(
        IEmailSender emailSender,
        ILogger<PatientActivatedEventHandler> logger)
    {
        _emailSender = emailSender;
        _logger = logger;
    }

    public async Task HandleEventAsync(PatientActivatedEto eventData)
    {
        _logger.LogInformation("Patient activated: {Name}", eventData.Name);

        await _emailSender.SendAsync(
            eventData.Email,
            "Welcome",
            "Your patient account has been activated");
    }
}
```

### Robust Event Handler (Idempotent + Multi-Tenant)

```csharp
public class EntitySyncEventHandler :
    IDistributedEventHandler<EntityUpdatedEto>,
    ITransientDependency
{
    private readonly IRepository<Entity, Guid> _repository;
    private readonly IDataFilter _dataFilter;
    private readonly ILogger<EntitySyncEventHandler> _logger;

    public async Task HandleEventAsync(EntityUpdatedEto eto)
    {
        // Disable tenant filter for cross-tenant sync
        using (_dataFilter.Disable<IMultiTenant>())
        {
            try
            {
                _logger.LogInformation("Processing entity sync: {Id}", eto.Id);

                // Idempotency check
                var existing = await _repository.FirstOrDefaultAsync(
                    x => x.ExternalId == eto.ExternalId);

                if (existing != null)
                {
                    ObjectMapper.Map(eto, existing);
                    await _repository.UpdateAsync(existing);
                }
                else
                {
                    var entity = ObjectMapper.Map<EntityUpdatedEto, Entity>(eto);
                    await _repository.InsertAsync(entity);
                }

                _logger.LogInformation("Entity sync completed: {Id}", eto.Id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Entity sync failed: {Id}", eto.Id);
                throw new UserFriendlyException($"Failed to sync entity: {ex.Message}");
            }
        }
    }
}
```

## Multi-Tenancy

### Cross-Tenant Operations

```csharp
public class CrossTenantService : ApplicationService
{
    private readonly IDataFilter _dataFilter;
    private readonly ICurrentTenant _currentTenant;

    public async Task<List<PatientDto>> GetAllTenantsPatients()
    {
        using (_dataFilter.Disable<IMultiTenant>())
        {
            return await _patientRepository.GetListAsync();
        }
    }

    public async Task OperateOnTenant(Guid tenantId)
    {
        using (_currentTenant.Change(tenantId))
        {
            await DoTenantSpecificOperation();
        }
    }
}
```

### Tenant-Specific Seeding

```csharp
public async Task SeedAsync(DataSeedContext context)
{
    if (context.TenantId.HasValue)
        await SeedTenantDataAsync(context.TenantId.Value);
    else
        await SeedHostDataAsync();
}
```

## Module Configuration

```csharp
[DependsOn(
    typeof(ClinicDomainModule),
    typeof(AbpIdentityDomainModule),
    typeof(AbpPermissionManagementDomainModule))]
public class ClinicApplicationModule : AbpModule
{
    public override void PreConfigureServices(ServiceConfigurationContext context)
    {
        PreConfigure<AbpIdentityOptions>(options =>
        {
            options.ExternalLoginProviders.Add<GoogleExternalLoginProvider>();
        });
    }

    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        Configure<AbpDistributedCacheOptions>(options =>
        {
            options.KeyPrefix = "Clinic:";
        });

        context.Services.AddTransient<IPatientAppService, PatientAppService>();
        context.Services.AddSingleton<ClinicApplicationMappers>();
    }

    public override void OnApplicationInitialization(ApplicationInitializationContext context)
    {
        var app = context.GetApplicationBuilder();
        var env = context.GetEnvironment();

        if (env.IsDevelopment())
            app.UseDeveloperExceptionPage();
    }
}
```

### Object Extension

```csharp
public static class ClinicModuleExtensionConfigurator
{
    public static void Configure()
    {
        ObjectExtensionManager.Instance.Modules()
            .ConfigureIdentity(identity =>
            {
                identity.ConfigureUser(user =>
                {
                    user.AddOrUpdateProperty<string>(
                        "Title",
                        property =>
                        {
                            property.Attributes.Add(new StringLengthAttribute(64));
                        });
                });
            });
    }
}
```

## Best Practices

1. **Permissions** - Define hierarchically (Parent.Child pattern)
2. **Background jobs** - Use for long-running or delayed tasks
3. **Distributed events** - Use for loose coupling between modules
4. **Idempotency** - Check for existing before insert in event handlers
5. **Multi-tenancy** - Use `IDataFilter.Disable<IMultiTenant>()` sparingly
6. **Module deps** - Declare all dependencies explicitly

## Related Skills

- `abp-entity-patterns` - Domain layer patterns
- `abp-service-patterns` - Application layer patterns
- `openiddict-authorization` - OAuth implementation
- `distributed-events-advanced` - Advanced event patterns
