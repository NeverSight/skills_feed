---
name: sorcha-cli
description: |
  Builds and maintains the Sorcha CLI tool using System.CommandLine 2.0.2, Refit HTTP clients, and Spectre.Console.
  Use when: Creating CLI commands, adding options/arguments, implementing Refit service clients, writing CLI tests, or fixing command structure issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Sorcha CLI Skill

The Sorcha CLI (`sorcha`) is a .NET 10 global tool for managing the Sorcha distributed ledger platform. It uses **System.CommandLine 2.0.2** for command parsing, **Refit** for HTTP API clients, and **Spectre.Console** for rich terminal output.

## Project Location

```
src/Apps/Sorcha.Cli/
├── Commands/           # Command implementations
├── Infrastructure/     # Helpers (ConsoleHelper, ExitCodes, HttpClientFactory)
├── Models/             # Request/Response DTOs for APIs
├── Services/           # Refit interfaces and service contracts
└── Program.cs          # Entry point and command registration
```

## Quick Reference

### Creating a New Command

```csharp
// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Sorcha Contributors

using System.CommandLine;
using System.CommandLine.Parsing;
using System.Net;
using System.Text.Json;
using Refit;
using Sorcha.Cli.Infrastructure;
using Sorcha.Cli.Services;

namespace Sorcha.Cli.Commands;

public class MyCommand : Command
{
    private readonly Option<string> _idOption;
    private readonly Option<bool> _verboseOption;

    public MyCommand(
        HttpClientFactory clientFactory,
        IAuthenticationService authService,
        IConfigurationService configService)
        : base("mycommand", "Description of command")
    {
        // IMPORTANT: Option constructor takes (name, description) NOT (alias1, alias2)
        _idOption = new Option<string>("--id", "The resource ID")
        {
            Required = true
        };

        _verboseOption = new Option<bool>("--verbose", "Enable verbose output")
        {
            Required = false
        };

        // Add options to command
        Options.Add(_idOption);
        Options.Add(_verboseOption);

        // Set the action handler
        this.SetAction(async (ParseResult parseResult, CancellationToken ct) =>
        {
            var id = parseResult.GetValue(_idOption)!;
            var verbose = parseResult.GetValue(_verboseOption);

            // Implementation here
            return ExitCodes.Success;
        });
    }
}
```

### System.CommandLine 2.0.2 Key Points

| Pattern | Correct | Wrong |
|---------|---------|-------|
| Option constructor | `new Option<string>("--id", "Description")` | `new Option<string>("--id", "-i")` |
| Add short alias | `option.Aliases.Add("-i")` | Second constructor param |
| Option name property | Returns `"--id"` (with dashes) | Does NOT return `"id"` |
| Get option value | `parseResult.GetValue(_option)` | `parseResult.GetValueForOption()` |
| Set action | `this.SetAction(async (pr, ct) => {...})` | Override Execute |
| Test find option | `o.Name == "--id"` | `o.Aliases.Contains("--id")` |

**Testing Note:** The `Aliases` collection does NOT include the option name. Use `o.Name == "--id"` to find options in tests.

### Adding Short Aliases

```csharp
_idOption = new Option<string>("--id", "The resource ID") { Required = true };
_idOption.Aliases.Add("-i");  // Add short alias separately
Options.Add(_idOption);
```

### Parent Command with Subcommands

```csharp
public class ParentCommand : Command
{
    public ParentCommand(
        HttpClientFactory clientFactory,
        IAuthenticationService authService,
        IConfigurationService configService)
        : base("parent", "Parent command description")
    {
        Subcommands.Add(new ChildListCommand(clientFactory, authService, configService));
        Subcommands.Add(new ChildGetCommand(clientFactory, authService, configService));
        Subcommands.Add(new ChildCreateCommand(clientFactory, authService, configService));
    }
}
```

### Registering Commands in Program.cs

```csharp
// Program.cs
rootCommand.Subcommands.Add(new MyCommand(clientFactory, authService, configService));
```

## Refit Service Clients

### Interface Definition

```csharp
// Services/IMyServiceClient.cs
using Refit;

public interface IMyServiceClient
{
    [Get("/api/resources")]
    Task<List<Resource>> ListAsync([Header("Authorization")] string authorization);

    [Get("/api/resources/{id}")]
    Task<Resource> GetAsync(string id, [Header("Authorization")] string authorization);

    [Post("/api/resources")]
    Task<Resource> CreateAsync([Body] CreateRequest request, [Header("Authorization")] string authorization);

    [Put("/api/resources/{id}")]
    Task<Resource> UpdateAsync(string id, [Body] UpdateRequest request, [Header("Authorization")] string authorization);

    [Delete("/api/resources/{id}")]
    Task DeleteAsync(string id, [Header("Authorization")] string authorization);

    // Pagination with query parameters
    [Get("/api/resources")]
    Task<List<Resource>> ListAsync(
        [Query] int? page,
        [Query] int? pageSize,
        [Header("Authorization")] string authorization);

    // OData queries
    [Get("/odata/{resource}")]
    Task<HttpResponseMessage> QueryODataAsync(
        string resource,
        [Query("$filter")] string? filter,
        [Query("$orderby")] string? orderby,
        [Query("$top")] int? top,
        [Query("$skip")] int? skip,
        [Header("Authorization")] string authorization);
}
```

### Using Refit Client in Commands

```csharp
// Get client from factory
var client = await clientFactory.CreateMyServiceClientAsync(profileName);

// Get auth token
var token = await authService.GetAccessTokenAsync(profileName);
if (string.IsNullOrEmpty(token))
{
    ConsoleHelper.WriteError("You must be authenticated.");
    return ExitCodes.AuthenticationError;
}

// Call API with Bearer token
var result = await client.GetAsync(id, $"Bearer {token}");
```

## Error Handling Pattern

```csharp
try
{
    var result = await client.GetAsync(id, $"Bearer {token}");
    // Success handling
}
catch (ApiException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    ConsoleHelper.WriteError($"Resource '{id}' not found.");
    return ExitCodes.NotFound;
}
catch (ApiException ex) when (ex.StatusCode == HttpStatusCode.Unauthorized)
{
    ConsoleHelper.WriteError("Authentication failed. Your access token may have expired.");
    ConsoleHelper.WriteInfo("Run 'sorcha auth login' to re-authenticate.");
    return ExitCodes.AuthenticationError;
}
catch (ApiException ex) when (ex.StatusCode == HttpStatusCode.Forbidden)
{
    ConsoleHelper.WriteError("You do not have permission to access this resource.");
    return ExitCodes.AuthorizationError;
}
catch (ApiException ex)
{
    ConsoleHelper.WriteError($"API Error: {ex.Message}");
    if (ex.Content != null)
    {
        ConsoleHelper.WriteError($"Details: {ex.Content}");
    }
    return ExitCodes.GeneralError;
}
catch (Exception ex)
{
    ConsoleHelper.WriteError($"Failed: {ex.Message}");
    return ExitCodes.GeneralError;
}
```

## Console Output Helpers

```csharp
// Success message (green)
ConsoleHelper.WriteSuccess("Operation completed successfully!");

// Error message (red)
ConsoleHelper.WriteError("Something went wrong.");

// Warning message (yellow)
ConsoleHelper.WriteWarning("This action cannot be undone.");

// Info message (cyan)
ConsoleHelper.WriteInfo("Use 'sorcha help' for more information.");
```

## Exit Codes

```csharp
public static class ExitCodes
{
    public const int Success = 0;
    public const int GeneralError = 1;
    public const int AuthenticationError = 2;
    public const int AuthorizationError = 3;
    public const int NotFound = 4;
    public const int ValidationError = 5;
}
```

## JSON Output Support

```csharp
// Check output format option
var outputFormat = parseResult.GetValue(BaseCommand.OutputOption) ?? "table";
if (outputFormat.Equals("json", StringComparison.OrdinalIgnoreCase))
{
    Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
    return ExitCodes.Success;
}

// Otherwise display as table
Console.WriteLine($"{"ID",-36} {"Name",-30} {"Status",-10}");
Console.WriteLine(new string('-', 80));
foreach (var item in results)
{
    Console.WriteLine($"{item.Id,-36} {item.Name,-30} {item.Status,-10}");
}
```

## See Also

- [commands](references/commands.md) - Complete command reference
- [testing](references/testing.md) - Unit test patterns and fixes
- [models](references/models.md) - DTO and model patterns

## Related Skills

- **dotnet** - .NET 10 / C# 13 patterns
- **xunit** - Unit testing with xUnit
- **fluent-assertions** - FluentAssertions patterns
- **moq** - Mocking with Moq

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| System.CommandLine | 2.0.2 | CLI framework |
| Refit | 9.0.2 | HTTP client |
| Refit.HttpClientFactory | 9.0.2 | DI integration |
| Spectre.Console | 0.54.0 | Rich console output |
| System.IdentityModel.Tokens.Jwt | 8.3.0 | JWT token handling |

## Tool Version Management

The Sorcha CLI can be installed as a .NET global tool or run from local build. When working on the CLI, check for version mismatches.

### Check for Global Tool Installation

```bash
# Check if sorcha is installed as a global tool
dotnet tool list --global | grep -i sorcha

# Find where the current 'sorcha' command is located
which sorcha  # Linux/macOS
where sorcha  # Windows
```

### Uninstall Global Tool (for local development)

If a global tool is installed, it may conflict with local development builds:

```bash
# Uninstall global tool to use local build
dotnet tool uninstall --global sorcha.cli
```

### Local Build Paths

After building with `dotnet build src/Apps/Sorcha.Cli`, the executable is at:

- **Release:** `src/Apps/Sorcha.Cli/bin/Release/net10.0/Sorcha.Cli.exe`
- **Debug:** `src/Apps/Sorcha.Cli/bin/Debug/net10.0/Sorcha.Cli.exe`

### Walkthrough Scripts

When writing walkthrough scripts that use the CLI, prefer finding the local build:

```powershell
# PowerShell pattern for finding CLI
$RepoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
$LocalCliPath = Join-Path $RepoRoot "src/Apps/Sorcha.Cli/bin/Release/net10.0/Sorcha.Cli.exe"
$DebugCliPath = Join-Path $RepoRoot "src/Apps/Sorcha.Cli/bin/Debug/net10.0/Sorcha.Cli.exe"

if (Test-Path $LocalCliPath) {
    $SorchaCliPath = $LocalCliPath
} elseif (Test-Path $DebugCliPath) {
    $SorchaCliPath = $DebugCliPath
} else {
    $SorchaCliPath = "sorcha"  # Fall back to global tool
}
```

### Version Mismatch Symptoms

If you see unexpected command options or missing features:
1. Check if global tool version differs from source code
2. Rebuild with `dotnet build src/Apps/Sorcha.Cli -c Release`
3. Verify using `sorcha --version` vs `./Sorcha.Cli.exe --version`

## Documentation Resources

> Fetch latest System.CommandLine documentation with Context7.

**Library ID:** `/dotnet/command-line-api`

**Recommended Queries:**
- "Option constructor aliases System.CommandLine 2.0"
- "SetAction handler pattern"
- "ParseResult GetValue"
