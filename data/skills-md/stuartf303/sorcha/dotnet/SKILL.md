---
name: dotnet
description: |
  Manages .NET 10 runtime, C# 13 syntax, and project configuration
  Use when: configuring projects, using modern C# features, setting up service defaults, working with DI patterns
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# .NET 10 / C# 13 Skill

This codebase uses .NET 10 (LTS) with C# 13, configured with strict nullable reference types, implicit usings, and XML documentation. All services follow the same project configuration patterns and share infrastructure through `Sorcha.ServiceDefaults`.

## Quick Start

### Project Configuration

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <NoWarn>$(NoWarn);CS1591</NoWarn>
  </PropertyGroup>
</Project>
```

### Service Setup Pattern

```csharp
var builder = WebApplication.CreateBuilder(args);

// Always call AddServiceDefaults first
builder.AddServiceDefaults();

// Add service-specific dependencies
builder.Services.AddScoped<IMyService, MyService>();

// Add JWT authentication (shared from ServiceDefaults)
builder.AddJwtAuthentication();

var app = builder.Build();
app.MapDefaultEndpoints();
app.UseAuthentication();
app.UseAuthorization();
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Primary constructors | Services with DI | `class MyService(IRepo repo)` |
| Collection expressions | Default values | `List<T> Items = []` |
| Required members | DTOs/contracts | `public required string Id { get; set; }` |
| Records | Value objects, DTOs | `public record PagedResult<T>(...)` |
| Raw string literals | Multi-line docs | `"""Markdown content"""` |

## Common Patterns

### Global Usings

```csharp
// GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading;
global using System.Threading.Tasks;
global using Sorcha.MyProject.Domain;  // Project-specific
```

### Test Project Setup

```xml
<ItemGroup>
  <Using Include="Xunit" />
  <Using Include="Moq" />
  <Using Include="FluentAssertions" />
</ItemGroup>
```

## See Also

- [patterns](references/patterns.md) - C# 13 features and code patterns
- [workflows](references/workflows.md) - Build, test, and deployment workflows

## Related Skills

- **aspire** - .NET Aspire orchestration and service defaults
- **minimal-apis** - Endpoint configuration with MapGet/MapPost
- **xunit** - Test project configuration and patterns
- **entity-framework** - EF Core integration with repositories

## Documentation Resources

> Fetch latest .NET documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "dotnet"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories when available
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/learn_microsoft_en-us_dotnet` _(high reputation, 42K+ snippets)_

**Recommended Queries:**
- "C# 13 new features primary constructors"
- "collection expressions syntax"
- "required members properties"
- "nullable reference types"