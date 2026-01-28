---
name: dotnet-build
version: 0.2.0
kind: cli
description: Build .NET solution/projects using dotnet CLI. Use when task involves compiling, restoring dependencies, or building artifacts.
inputs:
  target: [solution, project, all]
  configuration: [Debug, Release]
  project_path: string
contracts:
  success: 'Build completes with zero errors; artifacts in bin/'
  failure: 'Non-zero exit code or compilation errors'
---

# .NET Build Skill (Entry Map)

> **Goal:** Guide agent to the exact build procedure needed.

## Quick Start (Pick One)

- **Build entire solution** → `references/build-solution.md`
- **Restore dependencies only** → `references/restore-deps.md`

## When to Use

- Compile .NET code (`.csproj`, `.sln` files)
- Restore NuGet packages and dependencies
- Build Debug/Release configurations
- Generate build artifacts (binaries, assemblies)

**NOT for:** tests (dotnet-test), formatting (code-format), or analysis (code-analyze)

## Inputs & Outputs

**Inputs:** `target` (solution/project/all), `configuration` (Debug/Release), `project_path` (default: ./dotnet/PigeonPea.sln)

**Outputs:** `artifact_path` (bin/ directory), `build_log`, exit code (0=success)

**Guardrails:** Operate in ./dotnet only, never commit bin/obj/, idempotent builds

## Navigation

**1. Build Entire Solution** → [`references/build-solution.md`](references/build-solution.md)

- First build after cloning, building before tests, creating release artifacts

**2. Restore Dependencies Only** → [`references/restore-deps.md`](references/restore-deps.md)

- Setup dev environment, fix missing packages, troubleshoot NuGet

## Common Patterns

### Quick Build (Debug)

```bash
cd ./dotnet
dotnet build PigeonPea.sln
```

### Quick Build (Release)

```bash
cd ./dotnet
dotnet build PigeonPea.sln --configuration Release
```

### Restore then Build

```bash
cd ./dotnet
dotnet restore PigeonPea.sln
dotnet build PigeonPea.sln --no-restore
```

### Clean and Rebuild

```bash
cd ./dotnet
dotnet clean PigeonPea.sln
dotnet build PigeonPea.sln
```

### Build Specific Project

```bash
cd ./dotnet
dotnet build console-app/PigeonPea.Console.csproj
```

### Verbose Build for Debugging

```bash
cd ./dotnet
dotnet build PigeonPea.sln --verbosity detailed
```

## Troubleshooting

**Build fails:** Check error messages. See `references/build-solution.md` for detailed error handling.

**Missing dependencies:** Run `dotnet restore`. See `references/restore-deps.md`.

**NU1301 (service index):** NuGet unreachable. Check `references/restore-deps.md`.

**Slow builds:** Use `--no-restore`, `-m` (parallel), or `/p:RunAnalyzers=false`. See `references/build-solution.md`.

**Stale artifacts:** Run `dotnet clean` then rebuild.

## Success Indicators

```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

Artifacts in: `./dotnet/{ProjectName}/bin/{Configuration}/net9.0/`

## Integration

**After build:** dotnet-test (tests), code-analyze (static analysis)
**Before build:** code-format (style fixes)

## Related

- [`./dotnet/README.md`](../../../dotnet/README.md) - Project structure
- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - Architecture
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
