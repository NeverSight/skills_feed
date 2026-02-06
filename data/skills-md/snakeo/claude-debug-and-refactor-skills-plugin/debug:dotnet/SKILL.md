---
name: debug:dotnet
description: Debug ASP.NET Core and .NET applications with systematic diagnostic approaches. This skill covers troubleshooting dependency injection container errors, middleware pipeline issues, Entity Framework Core query problems, configuration binding failures, authentication/authorization issues, and startup failures. Includes Visual Studio and VS Code debugging, dotnet-trace, dotnet-dump, dotnet-counters tools, Serilog configuration, Application Insights integration, and four-phase debugging methodology.
---

# ASP.NET Core Debugging Guide

This guide provides a systematic approach to debugging ASP.NET Core applications, covering common error patterns, diagnostic tools, and resolution strategies.

## Common Error Patterns

### 1. Dependency Injection (DI) Container Errors

**Symptoms:**
- `InvalidOperationException: Unable to resolve service for type 'X'`
- `InvalidOperationException: A circular dependency was detected`
- `ObjectDisposedException: Cannot access a disposed object`

**Common Causes:**
```csharp
// Missing service registration
public class MyController
{
    public MyController(IMyService service) { } // Not registered in DI
}

// Circular dependency
public class ServiceA
{
    public ServiceA(ServiceB b) { }
}
public class ServiceB
{
    public ServiceB(ServiceA a) { } // Circular!
}

// Captive dependency (singleton holding scoped)
services.AddSingleton<ISingletonService, SingletonService>();
services.AddScoped<IScopedService, ScopedService>(); // Captured by singleton!
```

**Debugging Steps:**
1. Check `Program.cs` or `Startup.cs` for service registration
2. Verify service lifetime compatibility (Singleton > Scoped > Transient)
3. Use `IServiceProvider.GetRequiredService<T>()` for explicit resolution
4. Enable detailed DI errors in development:
```csharp
builder.Host.UseDefaultServiceProvider(options =>
{
    options.ValidateScopes = true;
    options.ValidateOnBuild = true;
});
```

**Resolution Patterns:**
```csharp
// Register missing service
builder.Services.AddScoped<IMyService, MyService>();

// Break circular dependency with Lazy<T> or factory
builder.Services.AddScoped<ServiceA>();
builder.Services.AddScoped<ServiceB>(sp =>
    new ServiceB(() => sp.GetRequiredService<ServiceA>()));

// Fix captive dependency - make both singleton or use factory
builder.Services.AddSingleton<IScopedService>(sp =>
    sp.CreateScope().ServiceProvider.GetRequiredService<ScopedService>());
```

### 2. Middleware Pipeline Issues

**Symptoms:**
- Requests returning unexpected status codes
- Authentication/authorization not working
- CORS errors
- Request body already read exceptions
- Response already started exceptions

**Common Causes:**
```csharp
// Wrong middleware order
app.UseAuthorization(); // Must come AFTER UseAuthentication!
app.UseAuthentication();

// Missing middleware
app.UseRouting();
// Missing UseAuthentication() and UseAuthorization()
app.MapControllers();

// Response already started
app.Use(async (context, next) =>
{
    await context.Response.WriteAsync("Hello"); // Response started
    await next(); // Next middleware tries to modify headers - ERROR
});
```

**Debugging Steps:**
1. Add diagnostic middleware to trace pipeline:
```csharp
app.Use(async (context, next) =>
{
    Console.WriteLine($"Request: {context.Request.Path}");
    await next();
    Console.WriteLine($"Response: {context.Response.StatusCode}");
});
```
2. Check middleware order matches recommended sequence
3. Enable developer exception page in development
4. Check for `Response.HasStarted` before modifying response

**Correct Middleware Order:**
```csharp
app.UseExceptionHandler("/error");
app.UseHsts();
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.UseSession();
app.MapControllers();
```

### 3. Entity Framework Core Query Problems

**Symptoms:**
- `InvalidOperationException: The instance of entity type 'X' cannot be tracked`
- N+1 query problems (excessive database queries)
- `DbUpdateConcurrencyException`
- Lazy loading returning null
- Query performance issues

**Common Causes:**
```csharp
// N+1 problem
var orders = context.Orders.ToList();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name); // Each access = new query
}

// Tracking conflict
var entity = context.Products.Find(1);
context.Products.Update(new Product { Id = 1 }); // Already tracked!

// Missing Include for related data
var order = context.Orders.First(); // Customer is null!
```

**Debugging Steps:**
1. Enable sensitive data logging:
```csharp
optionsBuilder
    .EnableSensitiveDataLogging()
    .EnableDetailedErrors()
    .LogTo(Console.WriteLine, LogLevel.Information);
```
2. Use SQL Server Profiler or EF Core logging to inspect queries
3. Check for `AsNoTracking()` usage on read-only queries
4. Verify `Include()` statements for related entities

**Resolution Patterns:**
```csharp
// Eager loading to prevent N+1
var orders = context.Orders
    .Include(o => o.Customer)
    .Include(o => o.OrderItems)
    .ToList();

// Use AsNoTracking for read-only queries
var products = context.Products
    .AsNoTracking()
    .Where(p => p.Price > 100)
    .ToList();

// Handle concurrency with retry
try
{
    await context.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    var entry = ex.Entries.Single();
    await entry.ReloadAsync();
    // Retry or merge changes
}

// Split queries for complex includes
var orders = context.Orders
    .Include(o => o.OrderItems)
    .AsSplitQuery()
    .ToList();
```

### 4. Configuration Binding Failures

**Symptoms:**
- Configuration values are null or default
- `InvalidOperationException` when binding to options
- Environment-specific settings not loading
- Secrets not being read

**Common Causes:**
```csharp
// Mismatched property names
public class MyOptions
{
    public string ConnectionString { get; set; } // But appsettings has "connectionString"
}

// Missing section
services.Configure<MyOptions>(config.GetSection("NonExistent"));

// Wrong environment file
// appsettings.Development.json not loading in Development
```

**Debugging Steps:**
1. Log all configuration sources:
```csharp
foreach (var source in builder.Configuration.Sources)
{
    Console.WriteLine(source.GetType().Name);
}
```
2. Dump effective configuration:
```csharp
Console.WriteLine(builder.Configuration.GetDebugView());
```
3. Verify `ASPNETCORE_ENVIRONMENT` is set correctly
4. Check file names match exactly (case-sensitive on Linux)

**Resolution Patterns:**
```csharp
// Validate options on startup
services.AddOptions<MyOptions>()
    .Bind(config.GetSection("MyOptions"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Use strongly-typed configuration
public class MyOptions
{
    public const string SectionName = "MySettings";

    [Required]
    public string ApiKey { get; set; } = string.Empty;

    [Range(1, 100)]
    public int MaxRetries { get; set; } = 3;
}

// Load with validation
builder.Services.AddOptions<MyOptions>()
    .BindConfiguration(MyOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

### 5. Authentication/Authorization Issues

**Symptoms:**
- 401 Unauthorized when credentials are correct
- 403 Forbidden with correct roles
- JWT token validation failures
- Cookie authentication not persisting
- Claims not available in controllers

**Common Causes:**
```csharp
// Missing authentication scheme
[Authorize] // No scheme specified, uses default
public class MyController { }

// Wrong claim type for roles
options.TokenValidationParameters = new TokenValidationParameters
{
    RoleClaimType = "role", // But token has "roles"
};

// Cookie not being sent (SameSite issues)
options.Cookie.SameSite = SameSiteMode.Strict; // Blocks cross-site
```

**Debugging Steps:**
1. Log authentication events:
```csharp
services.AddAuthentication()
    .AddJwtBearer(options =>
    {
        options.Events = new JwtBearerEvents
        {
            OnAuthenticationFailed = context =>
            {
                Console.WriteLine($"Auth failed: {context.Exception}");
                return Task.CompletedTask;
            },
            OnTokenValidated = context =>
            {
                Console.WriteLine($"Token validated for: {context.Principal?.Identity?.Name}");
                return Task.CompletedTask;
            }
        };
    });
```
2. Inspect JWT tokens at jwt.io
3. Check claims in controller: `User.Claims.Select(c => $"{c.Type}: {c.Value}")`
4. Verify HTTPS is configured correctly for secure cookies

**Resolution Patterns:**
```csharp
// Configure JWT properly
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = "your-issuer",
            ValidateAudience = true,
            ValidAudience = "your-audience",
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes("your-secret-key-at-least-32-chars")),
            RoleClaimType = ClaimTypes.Role,
            NameClaimType = ClaimTypes.Name
        };
    });

// Configure CORS for cookie auth
services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", builder =>
        builder.WithOrigins("https://frontend.com")
               .AllowCredentials()
               .AllowAnyHeader()
               .AllowAnyMethod());
});
```

### 6. Startup and Hosting Failures

**Symptoms:**
- 502.5 Process Failure on IIS/Azure
- Application fails to start with no clear error
- `HostAbortedException` during startup
- Port already in use errors

**Common Causes:**
```csharp
// Missing required service
var myService = app.Services.GetRequiredService<IMyService>(); // Throws on startup

// Database not available during startup
await context.Database.MigrateAsync(); // DB not ready

// Incorrect program entry
public static void Main(string[] args) { } // Missing async/await
```

**Debugging Steps:**
1. Enable stdout logging for IIS:
```xml
<!-- web.config -->
<aspNetCore processPath="dotnet" stdoutLogEnabled="true" stdoutLogFile=".\logs\stdout" />
```
2. Check Windows Event Viewer for .NET Runtime errors
3. Run application directly from command line:
```bash
dotnet MyApp.dll --urls "http://localhost:5000"
```
4. Use `ASPNETCORE_DETAILEDERRORS=true` environment variable

**Resolution Patterns:**
```csharp
// Graceful startup with error handling
try
{
    var builder = WebApplication.CreateBuilder(args);
    // Configure services
    var app = builder.Build();
    // Configure pipeline
    await app.RunAsync();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}

// Handle database not ready
services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 5,
            maxRetryDelay: TimeSpan.FromSeconds(30),
            errorNumbersToAdd: null);
    });
});
```

## Debugging Tools

### Visual Studio Debugger

**Essential Features:**
- **Breakpoints**: Conditional, hit count, filter by thread
- **Exception Settings**: Break on specific exceptions (Debug > Windows > Exception Settings)
- **Immediate Window**: Evaluate expressions during debugging
- **Diagnostic Tools**: CPU, memory, events timeline
- **Hot Reload**: Edit code during debugging (supported operations)

**Advanced Techniques:**
```csharp
// Conditional breakpoint expression
User.IsAuthenticated && Request.Path.StartsWithSegments("/api")

// Tracepoint (log without stopping)
// Right-click breakpoint > Actions > Log a message
"Request to {Request.Path} at {DateTime.Now}"

// DebuggerDisplay attribute for better visualization
[DebuggerDisplay("Order {Id}: {Customer.Name} - ${Total}")]
public class Order { }
```

### Visual Studio Code Debugging

**launch.json Configuration:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": ".NET Core Launch (web)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/bin/Debug/net8.0/MyApp.dll",
            "args": [],
            "cwd": "${workspaceFolder}",
            "stopAtEntry": false,
            "env": {
                "ASPNETCORE_ENVIRONMENT": "Development",
                "ASPNETCORE_URLS": "https://localhost:5001"
            }
        },
        {
            "name": ".NET Core Attach",
            "type": "coreclr",
            "request": "attach",
            "processId": "${command:pickProcess}"
        }
    ]
}
```

### dotnet-trace

**Performance tracing and diagnostics:**
```bash
# Install
dotnet tool install --global dotnet-trace

# Collect trace from running process
dotnet-trace collect --process-id <PID>

# Collect with specific providers
dotnet-trace collect -p <PID> --providers Microsoft-Extensions-Logging

# Collect CPU profile
dotnet-trace collect -p <PID> --profile cpu-sampling

# Convert to speedscope format for visualization
dotnet-trace convert trace.nettrace --format speedscope
```

### dotnet-dump

**Memory dump analysis:**
```bash
# Install
dotnet tool install --global dotnet-dump

# Collect dump from running process
dotnet-dump collect -p <PID>

# Analyze dump
dotnet-dump analyze dump.dmp

# Common SOS commands in analyze mode
> dumpheap -stat              # Heap statistics
> dumpheap -type MyClass      # Find specific type instances
> gcroot <address>            # Find GC roots for object
> threadpool                  # Thread pool info
> eestack                     # Managed stack traces
```

### dotnet-counters

**Real-time performance monitoring:**
```bash
# Install
dotnet tool install --global dotnet-counters

# Monitor default counters
dotnet-counters monitor -p <PID>

# Monitor specific counters
dotnet-counters monitor -p <PID> --counters \
    System.Runtime,\
    Microsoft.AspNetCore.Hosting,\
    Microsoft-AspNetCore-Server-Kestrel

# Export to CSV
dotnet-counters collect -p <PID> --format csv -o counters.csv
```

### ILogger and Logging Frameworks

**Built-in Logging Configuration:**
```csharp
// Program.cs
builder.Logging
    .ClearProviders()
    .AddConsole()
    .AddDebug()
    .SetMinimumLevel(LogLevel.Debug);

// Filter by category
builder.Logging.AddFilter("Microsoft.EntityFrameworkCore", LogLevel.Warning);
builder.Logging.AddFilter("MyApp", LogLevel.Debug);
```

**Structured Logging with Serilog:**
```csharp
// Install: Serilog.AspNetCore
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .WriteTo.Console(outputTemplate:
        "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}")
    .WriteTo.File("logs/app-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 7)
    .WriteTo.Seq("http://localhost:5341") // Centralized logging
    .CreateLogger();

builder.Host.UseSerilog();
```

**Logging Best Practices:**
```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public async Task<Order> ProcessOrderAsync(int orderId)
    {
        // Use structured logging with meaningful context
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["OrderId"] = orderId,
            ["CorrelationId"] = Activity.Current?.Id
        }))
        {
            _logger.LogInformation("Processing order {OrderId}", orderId);

            try
            {
                var order = await GetOrderAsync(orderId);
                _logger.LogDebug("Order details: {@Order}", order);
                return order;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to process order {OrderId}", orderId);
                throw;
            }
        }
    }
}
```

### Application Insights

**Setup and Configuration:**
```csharp
// Install: Microsoft.ApplicationInsights.AspNetCore
builder.Services.AddApplicationInsightsTelemetry();

// Configure in appsettings.json
{
    "ApplicationInsights": {
        "ConnectionString": "InstrumentationKey=xxx;IngestionEndpoint=xxx"
    }
}
```

**Custom Telemetry:**
```csharp
public class PaymentService
{
    private readonly TelemetryClient _telemetry;

    public async Task ProcessPaymentAsync(Payment payment)
    {
        using var operation = _telemetry.StartOperation<RequestTelemetry>("ProcessPayment");

        _telemetry.TrackEvent("PaymentStarted", new Dictionary<string, string>
        {
            ["PaymentId"] = payment.Id.ToString(),
            ["Amount"] = payment.Amount.ToString("C")
        });

        try
        {
            // Process payment
            _telemetry.TrackMetric("PaymentAmount", (double)payment.Amount);
        }
        catch (Exception ex)
        {
            _telemetry.TrackException(ex);
            operation.Telemetry.Success = false;
            throw;
        }
    }
}
```

## The Four Phases of ASP.NET Core Debugging

### Phase 1: Reproduce and Isolate

**Goals:** Consistently reproduce the issue and narrow down the scope.

**Actions:**
1. Capture exact steps to reproduce
2. Note environment details (OS, .NET version, configuration)
3. Check if issue occurs in Development vs Production
4. Isolate to specific endpoint, service, or component

**Commands:**
```bash
# Check .NET version and environment
dotnet --info

# Verify configuration
dotnet run --environment Development

# Test specific endpoint
curl -v https://localhost:5001/api/health

# Check if issue is environment-specific
ASPNETCORE_ENVIRONMENT=Development dotnet run
ASPNETCORE_ENVIRONMENT=Production dotnet run
```

### Phase 2: Gather Evidence

**Goals:** Collect logs, traces, and diagnostic data.

**Actions:**
1. Enable verbose logging
2. Capture request/response details
3. Monitor performance counters
4. Collect memory dumps if needed

**Configuration for Maximum Diagnostics:**
```json
// appsettings.Development.json
{
    "Logging": {
        "LogLevel": {
            "Default": "Debug",
            "Microsoft.AspNetCore": "Debug",
            "Microsoft.EntityFrameworkCore": "Debug",
            "Microsoft.EntityFrameworkCore.Database.Command": "Information"
        }
    }
}
```

**Middleware for Request Logging:**
```csharp
app.Use(async (context, next) =>
{
    var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();

    logger.LogDebug("Request: {Method} {Path} {Query}",
        context.Request.Method,
        context.Request.Path,
        context.Request.QueryString);

    // Capture request body (careful with large bodies)
    context.Request.EnableBuffering();

    var stopwatch = Stopwatch.StartNew();
    await next();
    stopwatch.Stop();

    logger.LogDebug("Response: {StatusCode} in {ElapsedMs}ms",
        context.Response.StatusCode,
        stopwatch.ElapsedMilliseconds);
});
```

### Phase 3: Analyze and Hypothesize

**Goals:** Form theories based on evidence and test them.

**Common Analysis Patterns:**

**For DI Errors:**
```csharp
// List all registered services
foreach (var service in builder.Services)
{
    Console.WriteLine($"{service.ServiceType.Name} -> {service.ImplementationType?.Name} ({service.Lifetime})");
}
```

**For EF Core Issues:**
```csharp
// Log generated SQL
optionsBuilder.LogTo(
    message => Debug.WriteLine(message),
    new[] { DbLoggerCategory.Database.Command.Name },
    LogLevel.Information);
```

**For Authentication Issues:**
```csharp
// Dump all claims
app.Use(async (context, next) =>
{
    if (context.User.Identity?.IsAuthenticated == true)
    {
        foreach (var claim in context.User.Claims)
        {
            Console.WriteLine($"Claim: {claim.Type} = {claim.Value}");
        }
    }
    await next();
});
```

### Phase 4: Fix and Verify

**Goals:** Implement fix with confidence and prevent regression.

**Best Practices:**
1. Write a failing test that reproduces the bug
2. Implement the minimal fix
3. Verify the test passes
4. Check for side effects
5. Add logging/monitoring for the fixed code path

**Example Test-Driven Fix:**
```csharp
[Fact]
public async Task ProcessOrder_WhenCustomerNotFound_ThrowsNotFoundException()
{
    // Arrange - This test should fail before fix
    var mockRepo = new Mock<ICustomerRepository>();
    mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<int>()))
        .ReturnsAsync((Customer)null);

    var service = new OrderService(mockRepo.Object);

    // Act & Assert
    await Assert.ThrowsAsync<CustomerNotFoundException>(
        () => service.ProcessOrderAsync(1, customerId: 999));
}
```

## Quick Reference Commands

### Build and Run

```bash
# Build project
dotnet build

# Build in Release mode
dotnet build -c Release

# Run with hot reload
dotnet watch run

# Run specific project
dotnet run --project src/MyApp/MyApp.csproj

# Run with specific environment
ASPNETCORE_ENVIRONMENT=Development dotnet run

# Publish for deployment
dotnet publish -c Release -o ./publish
```

### Entity Framework Core

```bash
# List migrations
dotnet ef migrations list

# Add new migration
dotnet ef migrations add AddUserTable

# Update database
dotnet ef database update

# Generate SQL script
dotnet ef migrations script --idempotent

# Remove last migration
dotnet ef migrations remove

# Drop database
dotnet ef database drop --force

# Scaffold from existing database
dotnet ef dbcontext scaffold "Server=.;Database=MyDb;Trusted_Connection=True" Microsoft.EntityFrameworkCore.SqlServer
```

### Testing

```bash
# Run all tests
dotnet test

# Run with verbosity
dotnet test -v detailed

# Run specific test
dotnet test --filter "FullyQualifiedName~OrderServiceTests"

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Generate coverage report
reportgenerator -reports:coverage.cobertura.xml -targetdir:coveragereport
```

### Diagnostics

```bash
# List running .NET processes
dotnet-trace ps

# Collect trace
dotnet-trace collect -p <PID> --duration 00:00:30

# Monitor counters
dotnet-counters monitor -p <PID>

# Collect memory dump
dotnet-dump collect -p <PID>

# Analyze dump
dotnet-dump analyze core_dump.dmp

# GC dump
dotnet-gcdump collect -p <PID>
```

### Package Management

```bash
# Add package
dotnet add package Serilog.AspNetCore

# Remove package
dotnet remove package OldPackage

# List packages
dotnet list package

# List outdated packages
dotnet list package --outdated

# Restore packages
dotnet restore

# Clear NuGet cache
dotnet nuget locals all --clear
```

### Secrets Management

```bash
# Initialize user secrets
dotnet user-secrets init

# Set a secret
dotnet user-secrets set "ConnectionStrings:Default" "Server=..."

# List secrets
dotnet user-secrets list

# Remove a secret
dotnet user-secrets remove "ConnectionStrings:Default"

# Clear all secrets
dotnet user-secrets clear
```

## Troubleshooting Checklist

### Before Debugging
- [ ] Reproduce the issue consistently
- [ ] Check if issue occurs in Development mode
- [ ] Verify .NET SDK/runtime version matches
- [ ] Confirm database is accessible
- [ ] Check environment variables are set

### During Debugging
- [ ] Enable detailed error pages (`app.UseDeveloperExceptionPage()`)
- [ ] Set logging to Debug level
- [ ] Check for null reference exceptions
- [ ] Verify DI service registrations
- [ ] Inspect middleware pipeline order
- [ ] Check EF Core generated SQL
- [ ] Verify authentication claims

### After Fixing
- [ ] Write test to prevent regression
- [ ] Update logging for the fixed code path
- [ ] Document the issue and solution
- [ ] Check for similar issues elsewhere
- [ ] Consider adding health checks

## Resources

- [ASP.NET Core Documentation](https://learn.microsoft.com/en-us/aspnet/core/)
- [Entity Framework Core Documentation](https://learn.microsoft.com/en-us/ef/core/)
- [.NET Diagnostics Documentation](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/)
- [Serilog Documentation](https://serilog.net/)
- [Application Insights Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
