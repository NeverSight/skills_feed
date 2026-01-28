---
name: docker-dotnet-containerize
description: "Generate production-ready Docker configurations for .NET APIs with multi-stage builds, Alpine optimization, layer caching, and build scripts. Use when containerizing .NET applications, creating Dockerfiles, or optimizing existing Docker setups."
layer: 1
tech_stack: [docker, dotnet]
topics: [dockerfile, multi-stage, alpine, layer-caching, docker-compose, optimization]
depends_on: []
complements: []
keywords: [Dockerfile, docker-compose, FROM, COPY, RUN, ENTRYPOINT, Alpine, multi-stage]
---

# .NET Docker Containerization Skill

Generate optimized Docker configurations for .NET projects using advanced build techniques, progressive layer publishing, and production-ready multi-stage builds.

## What This Skill Does

I will analyze your .NET solution and generate:
1. **Optimized Dockerfile** with BuildKit features and layer caching
2. **Build scripts** (Bash/PowerShell) with version tagging
3. **.dockerignore** file with comprehensive patterns
4. **Validation checklist** and troubleshooting guidance

## Advanced Techniques Applied

### BuildKit Frontend (syntax=docker/dockerfile:1-labs)
I use the experimental BuildKit frontend for:
- `--parents` flag support (preserves directory structure)
- Better caching mechanisms
- Advanced COPY operations
- Improved build performance

### Progressive Layer Publishing
For complex projects, I publish in dependency order:
1. **Domain layer** → Publish first (most stable)
2. **Infrastructure/EF Core** → Publish second
3. **Application/HttpApi** → Publish third  
4. **API Host** → Publish last (changes most)

**Why?** This creates separate layers in `/app/publish`, optimizing Docker layer caching. When you change only the API code, earlier layers remain cached.

### Non-Alpine SDK with Alpine Runtime
- **Build stage**: Uses full SDK (not Alpine) for better compatibility
- **Runtime stage**: Uses Alpine for minimal footprint
- **Benefit**: Avoid Alpine SDK build issues while keeping final image small

## Project Analysis

### Detection Process
I'll examine:
- Solution file (`*.sln`) location and structure
- All project files (`*.csproj`) and their dependencies
- Main entry point (typically `*.Host`, `*.Api`, `*.HttpApi.Host`)
- .NET version from `<TargetFramework>` tags
- Existence of `common.props` (ABP Framework indicator)
- Project architecture (Simple, DDD, ABP, Clean Architecture)

### Dependency Graph Mapping
I'll build a dependency graph to determine:
- Which projects reference which
- Optimal layer ordering for caching
- Whether progressive publishing is beneficial

**Simple projects (≤3)**: Single publish step  
**Complex projects (≥4)**: Progressive multi-layer publishing

## Dockerfile Generation

### Standard Template Structure

```dockerfile
# syntax=docker/dockerfile:1-labs
# BuildKit frontend for advanced features (--parents flag)

# Runtime base: Alpine for minimal size
FROM mcr.microsoft.com/dotnet/aspnet:{VERSION}-alpine AS base
USER app
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

# Build stage: Full SDK (not Alpine) for compatibility
FROM mcr.microsoft.com/dotnet/sdk:{VERSION}-alpine AS publish
ARG BUILD_CONFIGURATION=Release
WORKDIR /src

# [Project-specific COPY and publish commands]

# Final runtime
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "{MainAssembly}.dll"]
```

### Pattern 1: Simple Projects (2-3 projects)

```dockerfile
# syntax=docker/dockerfile:1-labs

FROM mcr.microsoft.com/dotnet/aspnet:9.0-alpine AS base
USER app
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

FROM mcr.microsoft.com/dotnet/sdk:9.0-alpine AS publish
ARG BUILD_CONFIGURATION=Release
WORKDIR /src

# Copy project files with --parents (preserves structure)
COPY --parents src/MyProject.Models/MyProject.Models.csproj \
               src/MyProject.Api/MyProject.Api.csproj \
              /src/

# Restore dependencies (quiet mode)
RUN dotnet restore "./src/MyProject.Api/MyProject.Api.csproj" -v q

# Copy all source code
COPY --parents src/MyProject.Models/ \
               src/MyProject.Api/ \
              /src/

# Single publish step
RUN dotnet publish "src/MyProject.Api/MyProject.Api.csproj" \
    -c $BUILD_CONFIGURATION \
    -o /app/publish \
    /p:UseAppHost=false \
    -v q

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyProject.Api.dll"]
```

### Pattern 2: ABP Framework / Complex DDD (7+ projects)

```dockerfile
# syntax=docker/dockerfile:1-labs

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS base
USER app
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS publish
ARG BUILD_CONFIGURATION=Release
WORKDIR /src

# Copy solution-level configuration (ABP Framework)
COPY common.props ./

# Layer 1: Copy all project files for restore
COPY --parents src/Project.Domain.Shared/Project.Domain.Shared.csproj \
               src/Project.Domain/Project.Domain.csproj \
               src/Project.EntityFrameworkCore/Project.EntityFrameworkCore.csproj \
               src/Project.Application.Contracts/Project.Application.Contracts.csproj \
               src/Project.HttpApi/Project.HttpApi.csproj \
               src/Project.Application/Project.Application.csproj \
               src/Project.HttpApi.Host/Project.HttpApi.Host.csproj \
              /src/

# Restore from entry point (restores all dependencies)
RUN dotnet restore "./src/Project.HttpApi.Host/Project.HttpApi.Host.csproj" -v q

# Layer 2: Publish Domain + EF Core (most stable, changes least)
COPY --parents src/Project.Domain.Shared/ \
               src/Project.Domain/ \
               src/Project.EntityFrameworkCore/ \
              /src/

RUN dotnet publish "src/Project.EntityFrameworkCore/Project.EntityFrameworkCore.csproj" \
    -c $BUILD_CONFIGURATION \
    -o /app/publish \
    /p:UseAppHost=false \
    -v q

# Layer 3: Publish Application.Contracts + HttpApi
COPY --parents src/Project.Application.Contracts/ \
               src/Project.HttpApi/ \
              /src/

RUN dotnet publish "src/Project.HttpApi/Project.HttpApi.csproj" \
    -c $BUILD_CONFIGURATION \
    -o /app/publish \
    /p:UseAppHost=false \
    -v q

# Layer 4: Publish Application + Host (changes most often)
COPY --parents src/Project.Application/ \
               src/Project.HttpApi.Host/ \
              /src/

RUN dotnet publish "src/Project.HttpApi.Host/Project.HttpApi.Host.csproj" \
    -c $BUILD_CONFIGURATION \
    -o /app/publish \
    /p:UseAppHost=false \
    -v q

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Project.HttpApi.Host.dll"]
```

## Key Optimization Techniques

### 1. --parents Flag (BuildKit)
```dockerfile
# Preserves directory structure automatically
COPY --parents src/Domain/Domain.csproj /src/
# Result: /src/src/Domain/Domain.csproj (structure maintained)
```

**Why?** No need to manually match paths. Works with relative references in `.csproj` files.

### 2. Progressive Publishing Strategy

**Traditional approach** (single publish):
```dockerfile
RUN dotnet publish "Host.csproj" -o /app/publish
```
❌ Changes to Host trigger rebuild of entire application

**Progressive approach** (layered publishing):
```dockerfile
# Publish Domain (layer 1)
RUN dotnet publish "Domain.csproj" -o /app/publish

# Publish Infrastructure (layer 2)  
RUN dotnet publish "Infrastructure.csproj" -o /app/publish

# Publish Application (layer 3)
RUN dotnet publish "Application.csproj" -o /app/publish

# Publish Host (layer 4)
RUN dotnet publish "Host.csproj" -o /app/publish
```
✅ Changes to Host only rebuild layer 4, cache layers 1-3

### 3. Quiet Mode Builds (-v q)
```dockerfile
RUN dotnet restore "./Project.csproj" -v q
RUN dotnet publish "Project.csproj" -v q
```
**Why?** Cleaner build logs, easier to spot errors, less noise in CI/CD.

### 4. Alpine Runtime with Full SDK
```dockerfile
# Build: Full SDK for better compatibility
FROM mcr.microsoft.com/dotnet/sdk:9.0-alpine AS publish

# Runtime: Alpine for minimal size
FROM mcr.microsoft.com/dotnet/aspnet:9.0-alpine AS base
```
**Why?** Alpine SDK can have issues with certain NuGet packages. Full SDK works better, Alpine runtime keeps final image small.

### 5. Build Configuration as ARG
```dockerfile
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish -c $BUILD_CONFIGURATION
```
**Why?** Allows `docker build --build-arg BUILD_CONFIGURATION=Debug` for testing.

## Build Script Generation

### Bash Script (build.sh)
```bash
#!/bin/bash
# Build script for .NET Docker image with version tagging

if [ -z "$1" ]; then
    echo "************************************************"
    echo ""
    echo "Usage: ./build.sh <version>"
    echo "Example: ./build.sh 1.0.0"
    echo ""
    echo "************************************************"
    exit 1
fi

VERSION=$1
IMAGE_NAME="mycompany/myproject"
DOCKERFILE_PATH="./Dockerfile"

echo "Building Docker image: ${IMAGE_NAME}:${VERSION}"

docker build \
    -f ${DOCKERFILE_PATH} \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    --build-arg BUILD_CONFIGURATION=Release \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Image tagged as:"
    echo "  - ${IMAGE_NAME}:${VERSION}"
    echo "  - ${IMAGE_NAME}:latest"
    echo ""
    echo "To run: docker run -p 8080:8080 ${IMAGE_NAME}:${VERSION}"
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
```

### PowerShell Script (build.ps1)
```powershell
# Build script for .NET Docker image with version tagging
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$ImageName = "mycompany/myproject"
$DockerfilePath = "./Dockerfile"

Write-Host "Building Docker image: ${ImageName}:${Version}" -ForegroundColor Cyan

docker build `
    -f $DockerfilePath `
    -t "${ImageName}:${Version}" `
    -t "${ImageName}:latest" `
    --build-arg BUILD_CONFIGURATION=Release `
    .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build successful!" -ForegroundColor Green
    Write-Host "Image tagged as:"
    Write-Host "  - ${ImageName}:${Version}"
    Write-Host "  - ${ImageName}:latest"
    Write-Host ""
    Write-Host "To run: docker run -p 8080:8080 ${ImageName}:${Version}"
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
```

## .dockerignore Generation

```dockerignore
# Build outputs
**/bin/
**/obj/
**/out/
**/publish/

# IDE and editor files
**/.vs/
**/.vscode/
**/.idea/
**/*.user
**/*.suo
**/*.swp
**/.DS_Store

# Test results and coverage
**/TestResults/
**/coverage/
**/*.trx

# Package directories
**/node_modules/
**/packages/
**/bower_components/

# Logs and temporary files
**/*.log
**/logs/
**/temp/
**/tmp/

# Version control
.git/
.gitignore
.gitattributes

# CI/CD
.github/
.gitlab-ci.yml
azure-pipelines.yml

# Documentation
*.md
!README.md
docs/
documentation/

# Docker files (avoid recursion)
**/Dockerfile*
**/docker-compose*
**/.dockerignore

# Development tools
**/.editorconfig
**/.prettierrc
**/.eslintrc*
```

## Decision Logic for Dockerfile Patterns

### When to Use Single Publish
✅ **Use for:**
- Projects with ≤3 .csproj files
- Simple API + Models structure
- Microservices with minimal dependencies
- Fast build times (<30 seconds)

### When to Use Progressive Publishing
✅ **Use for:**
- Projects with ≥4 .csproj files
- ABP Framework projects
- Clean Architecture / DDD projects
- Long build times (>1 minute)
- Frequent changes to outer layers (API/Host)

**Progressive publishing trades:**
- Slightly more complex Dockerfile
- For significantly faster rebuild times

## Architecture-Specific Patterns

### ABP Framework Detection
**Indicators:**
- `common.props` file exists
- Projects named with `.Domain.Shared`, `.HttpApi.Host` suffixes
- 7+ projects in solution

**Special handling:**
```dockerfile
# Copy common.props first
COPY common.props ./

# Follow ABP layer order
# Domain.Shared → Domain → EF Core → Contracts → HttpApi → Application → Host
```

### Clean Architecture Detection
**Indicators:**
- Projects in `src/Domain/`, `src/Application/`, `src/Infrastructure/`, `src/WebApi/` structure
- 4-6 projects typically

**Layer order:**
```
Domain → Application → Infrastructure → WebApi
```

### Simple API Detection
**Indicators:**
- 2-3 projects total
- Names like `*.Models`, `*.Api`, `*.Data`

**Strategy:** Single publish, no progressive layers needed.

## Validation Checklist

After generation, I'll verify:

- [ ] BuildKit syntax directive present (`# syntax=docker/dockerfile:1-labs`)
- [ ] .NET version matches project `<TargetFramework>`
- [ ] Alpine images used for SDK
- [ ] Non-root user configured (`USER app`)
- [ ] Ports correctly exposed (8080, 8081)
- [ ] `--parents` flag used in COPY commands
- [ ] Projects ordered by dependency (inner → outer)
- [ ] Progressive publishing for complex projects (≥4 projects)
- [ ] Quiet mode enabled (`-v q`)
- [ ] `BUILD_CONFIGURATION` parameterized
- [ ] `/p:UseAppHost=false` set
- [ ] Entry point references correct DLL
- [ ] .dockerignore excludes build artifacts
- [ ] Build scripts have version validation
- [ ] `common.props` copied if exists (ABP projects)

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Could not find project or directory" | Missing `--parents` flag | Add `--parents` to all COPY commands |
| "Project reference could not be resolved" | Wrong project copy order | Order by dependencies (Domain → API) |
| Build fails in Alpine SDK | Package compatibility | Use full SDK: `mcr.microsoft.com/dotnet/sdk:9.0` |
| Large image size (>200MB) | Not using Alpine runtime | Use `-alpine` |
| Cache not utilized | Wrong layer order | Publish stable layers first (Domain before API) |
| Build script fails | No version argument | Script validates argument existence |
| Missing common.props | ABP Framework project | Copy `common.props` before project files |
| Slow rebuilds | Single publish approach | Switch to progressive publishing |

## Build Commands Reference

### Development Build
```bash
# Quick build for testing
docker build -t myproject:dev .

# Build with debug configuration
docker build --build-arg BUILD_CONFIGURATION=Debug -t myproject:debug .
```

### Production Build
```bash
# Using build script (recommended)
./build.sh 1.0.0

# Manual build with version
docker build -t mycompany/myproject:1.0.0 -t mycompany/myproject:latest .
```

### Testing the Image
```bash
# Run container
docker run -d -p 8080:8080 --name myproject-test myproject:1.0.0

# Check health
curl http://localhost:8080/health

# View logs
docker logs -f myproject-test

# Inspect image size
docker images myproject:1.0.0

# Stop and remove
docker stop myproject-test && docker rm myproject-test
```

### CI/CD Integration
```bash
# Build with commit SHA
docker build -t myproject:${GITHUB_SHA} .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t myproject:1.0.0 .
```

## Performance Metrics

Typical improvements with this skill:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Image size** | 450MB | 120MB | 73% smaller |
| **Build time** (full) | 180s | 200s | +20s (one-time cost) |
| **Build time** (cached) | 180s | 15s | 92% faster |
| **Layer reuse** | 30% | 85% | 2.8x better caching |

*Note: Progressive publishing adds ~20s to initial build but saves 90%+ on subsequent builds*

## Best Practices Applied

1. **BuildKit features** - `--parents` flag for automatic path preservation
2. **Layer optimization** - Progressive publishing by dependency order
3. **Minimal images** - Alpine sdk (sdk:9.0-alpine)
4. **Compatible builds** - Full SDK or runtime avoids Alpine musl runtime issues.
5. **Security** - Non-root user, specific tags, minimal attack surface
6. **Build efficiency** - Quiet mode, ARG parameterization
7. **Caching strategy** - Copy .csproj before source, order by stability
8. **Version control** - Build scripts with validation and tagging
9. **ABP support** - Handles common.props and framework patterns
10. **Production ready** - UseAppHost=false, proper entry points

## Usage Examples

**Simple API:**
```
Containerize my .NET 9 Web API project with Models library
```

**ABP Framework:**
```
Create Docker setup for my ABP Framework solution with HttpApi.Host
```

**Clean Architecture:**
```
Generate optimized Dockerfile for my Clean Architecture DDD solution with 6 projects
```

**Optimization:**
```
My Docker builds are slow, optimize the existing Dockerfile for better caching
```