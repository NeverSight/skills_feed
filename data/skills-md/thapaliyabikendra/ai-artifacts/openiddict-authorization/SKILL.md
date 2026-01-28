---
name: openiddict-authorization
description: "Master OAuth 2.0 authorization patterns with OpenIddict and ABP Framework including permission-based authorization, role-based access control, custom claims, and multi-tenant security. Use when implementing authentication/authorization for ABP applications."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [authentication, authorization, permissions, rbac, claims, oauth2, multi-tenant]
depends_on: []
complements: [security-patterns, abp-framework-patterns]
keywords: [Authorize, Permission, IAuthorizationService, CurrentUser, OpenIddict, JWT, Bearer]
---

# OpenIddict Authorization Patterns

OAuth 2.0 and authorization patterns for ABP Framework with OpenIddict.

## When to Use

- Implementing permission-based authorization
- Configuring role-based access control (RBAC)
- Adding custom claims to tokens
- Securing API endpoints
- Implementing multi-tenant authorization
- Configuring OAuth 2.0 flows

## ABP Permission System

### Define Permissions

```csharp
// Domain.Shared/Permissions/{ProjectName}Permissions.cs
public static class {ProjectName}Permissions
{
    public const string GroupName = "{ProjectName}";

    public static class {Feature1}
    {
        public const string Default = GroupName + ".{Feature1}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string Export = Default + ".Export";
    }

    public static class {Feature2}
    {
        public const string Default = GroupName + ".{Feature2}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string ViewAll = Default + ".ViewAll"; // Admin only
        public const string Cancel = Default + ".Cancel";
    }

    public static class {Feature3}
    {
        public const string Default = GroupName + ".{Feature3}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string Manage = Default + ".Manage";
    }
}
```

### Register Permission Definitions

```csharp
// Application.Contracts/Permissions/{ProjectName}PermissionDefinitionProvider.cs
public class {ProjectName}PermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var mainGroup = context.AddGroup(
            {ProjectName}Permissions.GroupName,
            L("Permission:{ProjectName}"));

        // Feature1
        var feature1Permission = mainGroup.AddPermission(
            {ProjectName}Permissions.{Feature1}.Default,
            L("Permission:{Feature1}"));

        feature1Permission.AddChild(
            {ProjectName}Permissions.{Feature1}.Create,
            L("Permission:{Feature1}.Create"));

        feature1Permission.AddChild(
            {ProjectName}Permissions.{Feature1}.Edit,
            L("Permission:{Feature1}.Edit"));

        feature1Permission.AddChild(
            {ProjectName}Permissions.{Feature1}.Delete,
            L("Permission:{Feature1}.Delete"));

        feature1Permission.AddChild(
            {ProjectName}Permissions.{Feature1}.Export,
            L("Permission:{Feature1}.Export"));

        // Feature2
        var feature2Permission = mainGroup.AddPermission(
            {ProjectName}Permissions.{Feature2}.Default,
            L("Permission:{Feature2}"));

        feature2Permission.AddChild(
            {ProjectName}Permissions.{Feature2}.Create,
            L("Permission:{Feature2}.Create"));

        feature2Permission.AddChild(
            {ProjectName}Permissions.{Feature2}.ViewAll,
            L("Permission:{Feature2}.ViewAll"));

        // Feature3 - restricted to admin
        var feature3Permission = mainGroup.AddPermission(
            {ProjectName}Permissions.{Feature3}.Default,
            L("Permission:{Feature3}"),
            multiTenancySide: MultiTenancySides.Host); // Host-only permission
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<{ProjectName}Resource>(name);
    }
}
```

## Using Authorization in AppServices

### Declarative Authorization

```csharp
[Authorize({ProjectName}Permissions.{Feature}.Default)]
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    [Authorize({ProjectName}Permissions.{Feature}.Create)]
    public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
    {
        // Only users with {Feature}.Create permission can execute
    }

    [Authorize({ProjectName}Permissions.{Feature}.Edit)]
    public async Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input)
    {
        // Only users with {Feature}.Edit permission can execute
    }

    [Authorize({ProjectName}Permissions.{Feature}.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        // Only users with {Feature}.Delete permission can execute
    }

    [AllowAnonymous]
    public async Task<{Entity}Dto> GetPublicInfoAsync(Guid id)
    {
        // Anyone can access
    }
}
```

### Imperative Authorization

```csharp
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    public async Task<{Entity}Dto> GetAsync(Guid id)
    {
        var entity = await _repository.GetAsync(id);

        // Check if user can view this entity
        if (entity.OwnerId != CurrentUser.Id &&
            entity.AssignedUserId != CurrentUser.Id)
        {
            // User is neither the owner nor assigned - check admin permission
            await AuthorizationService.CheckAsync(
                {ProjectName}Permissions.{Feature}.ViewAll);
        }

        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    public async Task<bool> CanCancelAsync(Guid id)
    {
        var entity = await _repository.GetAsync(id);

        // Check various conditions
        if (entity.Status == {Entity}Status.Completed)
            return false;

        // Owner can always cancel
        if (entity.OwnerId == CurrentUser.Id)
            return true;

        // Check cancel permission
        return await AuthorizationService.IsGrantedAsync(
            {ProjectName}Permissions.{Feature}.Cancel);
    }
}
```

### Policy-Based Authorization

```csharp
// Define policy
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddAuthorization(options =>
    {
        options.AddPolicy("AdminOnly", policy =>
            policy.RequireRole("admin"));

        options.AddPolicy("DoctorOrAdmin", policy =>
            policy.RequireRole("admin", "doctor"));

        options.AddPolicy("CanManagePatients", policy =>
            policy.RequireAssertion(context =>
                context.User.HasClaim("Permission", ClinicPermissions.Patients.Default) ||
                context.User.IsInRole("admin")));
    });
}

// Use in AppService
[Authorize(Policy = "DoctorOrAdmin")]
public async Task<DoctorScheduleDto> GetScheduleAsync(Guid doctorId)
{
    // ...
}
```

## Role-Based Access Control

### Seed Default Roles

```csharp
public class ClinicDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IIdentityRoleRepository _roleRepository;
    private readonly IdentityRoleManager _roleManager;
    private readonly IPermissionManager _permissionManager;

    public async Task SeedAsync(DataSeedContext context)
    {
        await CreateRoleIfNotExistsAsync("Admin");
        await CreateRoleIfNotExistsAsync("Doctor");
        await CreateRoleIfNotExistsAsync("Receptionist");

        await AssignPermissionsToRolesAsync();
    }

    private async Task CreateRoleIfNotExistsAsync(string roleName)
    {
        var role = await _roleRepository.FindByNormalizedNameAsync(roleName.ToUpperInvariant());
        if (role == null)
        {
            role = new IdentityRole(GuidGenerator.Create(), roleName);
            await _roleManager.CreateAsync(role);
        }
    }

    private async Task AssignPermissionsToRolesAsync()
    {
        // Admin gets all permissions
        var allPermissions = new[]
        {
            ClinicPermissions.Patients.Default,
            ClinicPermissions.Patients.Create,
            ClinicPermissions.Patients.Edit,
            ClinicPermissions.Patients.Delete,
            ClinicPermissions.Appointments.Default,
            ClinicPermissions.Appointments.ViewAll,
            ClinicPermissions.Doctors.Default,
            ClinicPermissions.Doctors.ManageSchedule
        };

        foreach (var permission in allPermissions)
        {
            await _permissionManager.SetForRoleAsync("Admin", permission, true);
        }

        // Doctor permissions
        await _permissionManager.SetForRoleAsync("Doctor", ClinicPermissions.Appointments.Default, true);
        await _permissionManager.SetForRoleAsync("Doctor", ClinicPermissions.Patients.Default, true);

        // Receptionist permissions
        await _permissionManager.SetForRoleAsync("Receptionist", ClinicPermissions.Patients.Create, true);
        await _permissionManager.SetForRoleAsync("Receptionist", ClinicPermissions.Appointments.Create, true);
    }
}
```

## Custom Claims

### Add Custom Claims to Token

```csharp
// AuthServer/ClaimsPrincipalContributor.cs
public class ClinicClaimsPrincipalContributor : IAbpClaimsPrincipalContributor, ITransientDependency
{
    private readonly IRepository<Doctor, Guid> _doctorRepository;

    public ClinicClaimsPrincipalContributor(IRepository<Doctor, Guid> doctorRepository)
    {
        _doctorRepository = doctorRepository;
    }

    public async Task ContributeAsync(AbpClaimsPrincipalContributorContext context)
    {
        var identity = context.ClaimsPrincipal.Identities.FirstOrDefault();
        if (identity == null) return;

        var userId = identity.FindUserId();
        if (!userId.HasValue) return;

        // Add custom claims
        var doctor = await _doctorRepository.FirstOrDefaultAsync(d => d.UserId == userId);
        if (doctor != null)
        {
            identity.AddClaim(new Claim("doctor_id", doctor.Id.ToString()));
            identity.AddClaim(new Claim("specialization", doctor.Specialization));
        }
    }
}

// Register in module
public override void ConfigureServices(ServiceConfigurationContext context)
{
    Configure<AbpClaimsServiceOptions>(options =>
    {
        options.RequestedClaims.Add("doctor_id");
        options.RequestedClaims.Add("specialization");
    });
}
```

### Access Custom Claims

```csharp
public class AppointmentAppService : ApplicationService
{
    public async Task<List<AppointmentDto>> GetMyAppointmentsAsync()
    {
        // Get doctor_id from claims
        var doctorIdClaim = CurrentUser.FindClaim("doctor_id");
        if (doctorIdClaim == null)
        {
            throw new BusinessException("User is not a doctor");
        }

        var doctorId = Guid.Parse(doctorIdClaim.Value);
        return await _appointmentRepository
            .GetListAsync(a => a.DoctorId == doctorId);
    }
}
```

## Multi-Tenant Authorization

### Tenant-Aware Permissions

```csharp
public class TenantPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var group = context.AddGroup("TenantSettings");

        // Tenant-side permission (available in tenants)
        group.AddPermission(
            "TenantSettings.Manage",
            multiTenancySide: MultiTenancySides.Tenant);

        // Host-side permission (only host/admin)
        group.AddPermission(
            "TenantSettings.ManageAll",
            multiTenancySide: MultiTenancySides.Host);
    }
}
```

### Cross-Tenant Data Access

```csharp
public class CrossTenantReportService : ApplicationService
{
    private readonly IDataFilter _dataFilter;
    private readonly ICurrentTenant _currentTenant;

    [Authorize("Reports.CrossTenant")]
    public async Task<ReportDto> GenerateCrossTenantReportAsync()
    {
        // Verify host-level access
        if (_currentTenant.Id.HasValue)
        {
            throw new BusinessException("Cross-tenant reports only available from host");
        }

        using (_dataFilter.Disable<IMultiTenant>())
        {
            // Access data across all tenants
            var allPatients = await _patientRepository.GetCountAsync();
            // ...
        }
    }
}
```

## OpenIddict Configuration

### AuthServer Setup

```csharp
// AuthServer/AuthServerModule.cs
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    PreConfigure<OpenIddictBuilder>(builder =>
    {
        builder.AddValidation(options =>
        {
            options.AddAudiences("ClinicManagementSystem");
            options.UseLocalServer();
            options.UseAspNetCore();
        });
    });
}

public override void ConfigureServices(ServiceConfigurationContext context)
{
    Configure<AbpOpenIddictOptions>(options =>
    {
        options.AddDevelopmentEncryptionAndSigningCertificate = true;
    });

    // Configure OpenIddict scopes
    Configure<OpenIddictServerOptions>(options =>
    {
        options.Scopes.Add("offline_access");
        options.Scopes.Add("profile");
        options.Scopes.Add("email");
        options.Scopes.Add("clinic_api");
    });
}
```

### API Host JWT Configuration

```csharp
// HttpApi.Host configuration
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();

    context.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer(options =>
        {
            options.Authority = configuration["AuthServer:Authority"];
            options.RequireHttpsMetadata = Convert.ToBoolean(
                configuration["AuthServer:RequireHttpsMetadata"]);
            options.Audience = "ClinicManagementSystem";

            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ClockSkew = TimeSpan.Zero
            };
        });
}
```

## Security Best Practices

### Input Validation in Authorization

```csharp
public async Task<PatientDto> GetAsync(Guid id)
{
    // Validate input
    if (id == Guid.Empty)
    {
        throw new AbpValidationException("Invalid patient ID");
    }

    var patient = await _patientRepository.FindAsync(id);
    if (patient == null)
    {
        throw new EntityNotFoundException(typeof(Patient), id);
    }

    // Authorization check
    await AuthorizationService.CheckAsync(ClinicPermissions.Patients.Default);

    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

### Audit Logging

```csharp
[Audited] // Enable audit logging for this service
public class PatientAppService : ApplicationService
{
    [DisableAuditing] // Disable for specific methods
    public async Task<List<PatientDto>> GetListAsync()
    {
        // ...
    }
}
```

## Quality Checklist

- [ ] Permissions defined for all features
- [ ] Permission hierarchy established (parent/child)
- [ ] Roles seeded with appropriate permissions
- [ ] All mutation endpoints have `[Authorize]`
- [ ] Custom claims added for domain-specific data
- [ ] Multi-tenancy permissions configured correctly
- [ ] Audit logging enabled for sensitive operations
- [ ] Token validation configured properly

## Shared Knowledge

For foundational patterns, see the shared knowledge base:

| Topic | File | Description |
|-------|------|-------------|
| Permission naming | [knowledge/conventions/permissions.md](../../knowledge/conventions/permissions.md) | Permission format and hierarchy |
| Naming conventions | [knowledge/conventions/naming.md](../../knowledge/conventions/naming.md) | Permission constant naming |

## Integration Points

This skill is used by:
- **abp-developer**: Authorization implementation
- **security-engineer**: Security audit and review
- **/review:permissions**: Permission coverage analysis
- **backend-architect**: Security architecture design
