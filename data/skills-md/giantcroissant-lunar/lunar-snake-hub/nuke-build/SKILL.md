---
name: nuke-build
version: 0.1.0
kind: cli
description: Build and orchestrate tasks using Nuke build system. Use when task involves running Nuke build targets, orchestrating complex build workflows, or managing build pipelines.
inputs:
  target: [Clean, Restore, Compile]
  configuration: [Debug, Release]
  parameters: object
contracts:
  success: 'Target completes successfully with zero errors; build artifacts created'
  failure: 'Non-zero exit code or target execution errors'
---

# Nuke Build Skill (Entry Map)

> **Status:** Deprecated – Build orchestration now lives in the `unify-build` repository. Use that repository's build tooling instead of this skill when working on current projects.
> **Goal:** Guide agent to execute Nuke build targets and orchestrate build workflows.

## Quick Start (Pick One)

- **Run build targets** → `references/build-targets.md`
- **Setup Nuke in new project** → `references/setup-nuke.md`

## When to Use

- Execute Nuke build targets (Clean, Restore, Compile)
- Orchestrate complex build workflows
- Run cross-platform builds with unified interface
- Manage build pipelines and dependencies
- Integrate with CI/CD systems

**NOT for:** Simple .NET builds (use dotnet-build), testing (dotnet-test), or formatting (code-format)

## Inputs & Outputs

**Inputs:** `target` (Clean/Restore/Compile), `configuration` (Debug/Release), `parameters` (custom build parameters)

**Outputs:** Build artifacts, target execution logs, exit code (0=success)

**Guardrails:** Execute from ./build/nuke directory, verify targets exist, never commit build artifacts

## Navigation

**1. Run Build Targets** → [`references/build-targets.md`](references/build-targets.md)

- Execute Clean, Restore, Compile targets
- Pass custom parameters to build
- Run multiple targets in sequence

**2. Setup Nuke** → [`references/setup-nuke.md`](references/setup-nuke.md)

- Bootstrap Nuke in existing project
- Configure build targets and dependencies
- Set up CI/CD integration

## Common Patterns

### Run Default Target (Compile)

```bash
cd ./build/nuke
./build.sh
```

### Run Specific Target

```bash
cd ./build/nuke
./build.sh Clean
./build.sh Restore
./build.sh Compile
```

### Run with Configuration

```bash
cd ./build/nuke
./build.sh Compile --configuration Release
```

### Run Multiple Targets

```bash
cd ./build/nuke
./build.sh Clean Restore Compile
```

### Windows (PowerShell)

```powershell
cd ./build/nuke
./build.ps1 Compile
```

### Windows (Command Prompt)

```cmd
cd build\nuke
build.cmd Compile
```

### Cross-Platform Build

```bash
# Linux/macOS
./build/nuke/build.sh Compile --configuration Release

# Windows
.\build\nuke\build.ps1 Compile --configuration Release
```

## Troubleshooting

**Build fails:** Check error messages. See `references/build-targets.md` for detailed error handling.

**Script not executable:** Run `chmod +x build.sh` on Linux/macOS.

**Missing .NET SDK:** Install .NET SDK 8.0 or later. Build scripts will attempt to download if missing.

**Target not found:** Check available targets with `./build.sh --help` or see `references/build-targets.md`.

**Compilation errors:** Nuke build uses MSBuild under the hood. Check Build.cs for target implementation.

## Success Indicators

```
═══════════════════════════════
Target             Status      Duration
───────────────────────────────
Restore            ✓          00:00:02
Compile            ✓          00:00:05
───────────────────────────────
Build succeeded
═══════════════════════════════
```

Build artifacts in: `./build/nuke/build/bin/`

## Integration

**Complements dotnet-build:** Nuke orchestrates higher-level workflows; dotnet-build handles direct .NET compilation
**After build:** dotnet-test (tests), code-analyze (static analysis)
**Before build:** code-format (style fixes)

## Nuke vs. dotnet CLI

| Aspect             | Nuke Build                       | dotnet CLI                     |
| ------------------ | -------------------------------- | ------------------------------ |
| **Purpose**        | Build orchestration & pipelines  | Direct .NET compilation        |
| **Complexity**     | Complex multi-step workflows     | Simple build/test tasks        |
| **Cross-platform** | Unified scripts (sh/ps1/cmd)     | dotnet command (all platforms) |
| **Customization**  | C# code for build logic          | MSBuild properties             |
| **CI/CD**          | First-class support              | Requires scripting             |
| **Learning curve** | Moderate (requires C# knowledge) | Low (CLI commands)             |

**When to use Nuke:** Complex builds, CI/CD pipelines, multi-project orchestration
**When to use dotnet:** Simple builds, quick compilation, local development

## Related

- [`./build/nuke/build/Build.cs`](../../../build/nuke/build/Build.cs) - Build target definitions
- [`./build/nuke/build/_build.csproj`](../../../build/nuke/build/_build.csproj) - Build project
- [`.agent/skills/dotnet-build/`](../dotnet-build/) - Direct .NET build skill
- [Nuke documentation](https://nuke.build/) - Official Nuke docs

## Available Targets

Current project targets (see `Build.cs`):

- **Clean**: Removes build artifacts and output directories
- **Restore**: Restores NuGet dependencies
- **Compile**: Compiles the solution (default target)

Target dependencies:

- Compile → Restore
- Clean → (runs before Restore)
