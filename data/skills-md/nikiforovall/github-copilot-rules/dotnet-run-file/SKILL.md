---
name: dotnet-run-file
description: Run script-like CSharp programs using dotnet run file.cs. Use this skill when users want to execute CSharp code directly, write one-liner scripts via stdin, or learn about run file directives.
---

# .NET Run Files

Run C# code directly without creating project files using .NET 10's `dotnet run file.cs` feature.

## When to Use This Skill

Use this skill when the user wants to:
- Execute C# code quickly without creating a project
- Write one-liner scripts via stdin (ideal for Claude Code)
- Learn about run file directives (`#:package`, `#:sdk`, `#:property`)
- Create executable shell scripts in C#
- Convert a run file to a full project

## Guide

For detailed examples and directives reference, load `references/guide.md`.

## Quick Reference

### Basic Execution

```bash
# Run a .cs file
dotnet run app.cs

# Run from stdin
echo 'Console.WriteLine("Hello");' | dotnet run -

# Multi-line via heredoc
dotnet run - << 'EOF'
var now = DateTime.Now;
Console.WriteLine($"Time: {now}");
EOF
```

### Directives

```csharp
#:package Humanizer@*            // NuGet package (version required, wildcards ok)
#:sdk Microsoft.NET.Sdk.Web       // SDK selection
#:property LangVersion preview    // MSBuild property
#:project ../src/MyLib            // Project reference
```

### Convert to Project

```bash
dotnet project convert app.cs
```

## Core Operations

### 1. Run a C# File

**Steps**:
1. Create a `.cs` file with your code (top-level statements supported)
2. Add directives at the top if needed (packages, SDK, properties)
3. Execute: `dotnet run filename.cs`

**Example**:
```csharp
// hello.cs
Console.WriteLine("Hello from .NET!");
```
```bash
dotnet run hello.cs
```

### 2. Execute via Stdin

**Purpose**: Run C# code without creating files - ideal for quick scripts and AI-assisted workflows.

**Patterns**:
```bash
# Simple one-liner
echo 'Console.WriteLine(Math.PI);' | dotnet run -

# With package
dotnet run - << 'EOF'
#:package Humanizer@*
using Humanizer;
Console.WriteLine(TimeSpan.FromMinutes(90).Humanize());
EOF

# Heredoc for multi-line
dotnet run - << 'EOF'
using System.Text.Json;

var obj = new { Name = "Test", Value = 42 };
Console.WriteLine(JsonSerializer.Serialize(obj));
EOF
```

## Interactive Flow

When user asks to run C# code without specifics:

1. Ask what they want to accomplish
2. Determine if stdin one-liner or file-based is better
3. For simple tasks → use stdin pattern
4. For complex tasks → create a `.cs` file
5. Add necessary directives based on requirements
6. Execute and show results

## Claude Code Integration Tips

**For AI-assisted workflows**:
- Prefer stdin for quick calculations, data transformations, API calls
- Use heredoc syntax for multi-line code
- Output JSON for easy parsing: `dotnet run script.cs | jq .`
