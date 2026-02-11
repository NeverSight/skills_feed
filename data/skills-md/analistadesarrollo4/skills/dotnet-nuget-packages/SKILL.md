---
name: dotnet-nuget-packages
description: "NuGet dependency management and versioning policy for .NET projects. Use when: (1) Adding or updating packages in .csproj files, (2) Setting up new project dependencies, (3) Questions about package versions or stability policies, (4) Configuring core architecture packages (MediatR, FluentValidation, EF Core, Serilog, etc.), (5) Evaluating if a package should be included, or (6) Troubleshooting dependency conflicts."
---

# NuGet Dependency Management

## Package Installation Commands

**ALWAYS use .NET CLI commands** to add, update, or remove packages. Never manually edit .csproj files for package references.

### Adding Packages

```bash
# Add latest stable version (RECOMMENDED)
dotnet add package <PackageName>

# Add specific version
dotnet add package <PackageName> --version <Version>

# Add to specific project
dotnet add <path/to/project.csproj> package <PackageName>
```

### Updating Packages

```bash
# Update specific package to latest version
dotnet add package <PackageName>

# List outdated packages
dotnet list package --outdated
```

### Removing Packages

```bash
# Remove package
dotnet remove package <PackageName>

# Remove from specific project
dotnet remove <path/to/project.csproj> package <PackageName>
```

### Examples

```bash
# Install MediatR
dotnet add package MediatR

# Install specific EF Core version
dotnet add package Microsoft.EntityFrameworkCore.SqlServer --version 8.0.0

# Install to Infrastructure project
dotnet add Infrastructure/Infrastructure.csproj package Serilog.AspNetCore
```

## Version and Stability Policy

- **CRITICAL: Always use the latest stable MAJOR version** of any package.
- **NEVER use prerelease, beta, or release candidate versions** (e.g., `8.0.0-rc1`, `9.0.0-beta.5`) unless explicitly requested by the user for a specific package.
- Verify and install the most recent stable version before adding any dependency.
- Use `dotnet add package <PackageName>` without `--version` to get the latest stable version automatically.

## Required Core Packages by Layer

When setting up a new project, **use dotnet CLI to install** the following packages (when applicable) in their latest stable version.

### Application and Domain Layer

```bash
dotnet add package MediatR
dotnet add package FluentValidation.AspNetCore
dotnet add package Polly
dotnet add package Microsoft.Extensions.Http
```

- **MediatR**: For CQRS pattern implementation (Commands and Queries).
- **FluentValidation.AspNetCore**: For strict validation of input models (Commands/Queries).
- **Polly**: For implementing resilience and fault-tolerance strategies (Retries, Circuit Breakers, etc.).
- **Microsoft.Extensions.Http**: For efficient HTTP client creation and management (HttpClientFactory).

### Infrastructure Layer (Persistence and Messaging)

```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.EntityFrameworkCore.Tools
dotnet add package RabbitMQ.Client
dotnet add package Serilog.AspNetCore
dotnet add package Microsoft.Extensions.Logging
```

- **Microsoft.EntityFrameworkCore.SqlServer**: SQL Server database provider.
- **Microsoft.EntityFrameworkCore.Design**: Design-time components for EF Core.
- **Microsoft.EntityFrameworkCore.Tools**: Command-line tools for migrations.
- **RabbitMQ.Client**: For message broker integration.
- **Serilog.AspNetCore**: For structured logging implementation.
- **Microsoft.Extensions.Logging**: .NET standard logging.

### Presentation Layer (API)

```bash
dotnet add package Swashbuckle.AspNetCore
```

This meta-package includes:
- **Swashbuckle.AspNetCore.Swagger**
- **Swashbuckle.AspNetCore.SwaggerGen**
- **Swashbuckle.AspNetCore.SwaggerUI**

## Verification and Management

### Check Installed Packages

```bash
# List all packages in project
dotnet list package

# List all packages including transitive dependencies
dotnet list package --include-transitive

# Check for outdated packages
dotnet list package --outdated

# Check for vulnerable packages
dotnet list package --vulnerable
```

### Restore Packages

```bash
# Restore all packages for solution
dotnet restore

# Restore for specific project
dotnet restore <path/to/project.csproj>
```

## Restrictions and Best Practices

- **Prohibited Packages**: Avoid installing abstraction or utility packages that duplicate native .NET Core/C# functionality (e.g., obsolete wrappers, libraries already in `System.*`).
- **Service Configuration**: Configure and register third-party services or utilities using **Extension Methods** to keep `Program.cs` clean, as stipulated in the Infrastructure Organization guidelines.
- Avoid redundant wrapper packages that duplicate modern .NET functionality.
