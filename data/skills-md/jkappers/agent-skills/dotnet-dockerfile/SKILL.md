---
name: dotnet-dockerfile
description: Create optimized, secure multi-stage Dockerfiles for .NET Core and ASP.NET Core applications. Use when (1) creating a new Dockerfile for a .NET project, (2) containerizing a .NET application, (3) optimizing an existing .NET Dockerfile, (4) setting up Docker for .NET 6/7/8+ apps, or (5) user mentions .NET and Docker/container together.
---

# .NET Dockerfile Generator

Generate production-ready multi-stage Dockerfiles for .NET applications.

## Workflow

1. Determine .NET version (8, 9, or 10) from project file or ask user
2. Identify project type: ASP.NET Core web app, API, worker service, or console app
3. Locate project file path (e.g., `src/MyApp/MyApp.csproj`)
4. Choose optimization: standard, chiseled (smaller), or native AOT (smallest/fastest startup)

> **Breaking Change in .NET 10**: Ubuntu is now the default Linux distribution for all .NET container images. Debian images are no longer provided. Tags like `10.0`, `10.0-noble`, and `10.0-noble-chiseled` all use Ubuntu 24.04 "Noble Numbat".

## Image Selection Guide

| Scenario | Runtime Image | Compressed Size |
|----------|--------------|-----------------|
| Standard ASP.NET | `aspnet:10.0` | ~92 MB |
| Smaller footprint | `aspnet:10.0-alpine` | ~52 MB |
| Production (recommended) | `aspnet:10.0-noble-chiseled` | ~53 MB |
| Azure Linux distroless | `aspnet:10.0-azurelinux3.0-distroless` | ~55 MB |
| Self-contained | `runtime-deps:10.0-noble-chiseled` | ~22 MB |
| Native AOT | `runtime-deps:10.0-noble-chiseled` | ~12 MB |

**Chiseled images**: Ubuntu-based, no shell, no package manager, non-root by default. Recommended for production.

**Azure Linux distroless**: Alternative to chiseled with Microsoft supply chain security. Similar benefits: no shell, non-root by default.

## Standard Pattern

```dockerfile
# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copy project files and restore (cache layer)
COPY *.csproj ./
RUN dotnet restore

# Copy source and publish
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Runtime
FROM mcr.microsoft.com/dotnet/aspnet:10.0-noble-chiseled AS production
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

## Multi-Project Solution Pattern

For solutions with multiple projects, copy all .csproj files first:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copy solution and project files (cache layer)
COPY *.sln ./
COPY src/MyApp/*.csproj ./src/MyApp/
COPY src/MyApp.Core/*.csproj ./src/MyApp.Core/
COPY tests/MyApp.Tests/*.csproj ./tests/MyApp.Tests/
RUN dotnet restore

# Copy everything and publish
COPY . .
RUN dotnet publish src/MyApp -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0-noble-chiseled AS production
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

## Self-Contained Deployment

Bundles .NET runtime with app, enables smallest runtime-deps images:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish \
    --self-contained true \
    -r linux-x64

FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble-chiseled AS production
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["./MyApp"]
```

## Native AOT (Fastest Startup)

Compiles to native code. Smallest image (~12 MB), fastest startup:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0-aot AS build
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble-chiseled AS production
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["./MyApp"]
```

**Dedicated AOT SDK images** include native compilation prerequisites:
- `mcr.microsoft.com/dotnet/sdk:10.0-aot` (Ubuntu, also tagged `10.0-noble-aot`)
- `mcr.microsoft.com/dotnet/sdk:10.0-alpine-aot`
- `mcr.microsoft.com/dotnet/sdk:10.0-azurelinux3.0-aot`

**Requires in .csproj:**
```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>
</PropertyGroup>
```

**Limitations**: No runtime reflection, not all libraries compatible.

## Dockerfile-less Container Publishing

.NET 10 supports publishing containers directly from the SDK—no Dockerfile required:

```bash
# Publish to local container runtime
dotnet publish --os linux --arch x64 /t:PublishContainer

# Publish directly to a registry (no Docker needed)
dotnet publish --os linux --arch x64 /t:PublishContainer \
    -p ContainerRegistry=ghcr.io \
    -p ContainerRepository=myorg/myapp

# Multi-architecture publishing
dotnet publish /t:PublishContainer \
    -p ContainerRuntimeIdentifiers="linux-x64;linux-arm64"
```

**Project file configuration:**
```xml
<PropertyGroup>
  <!-- Control image format: Docker or OCI -->
  <ContainerImageFormat>OCI</ContainerImageFormat>
  <!-- Customize base image -->
  <ContainerBaseImage>mcr.microsoft.com/dotnet/aspnet:10.0-noble-chiseled</ContainerBaseImage>
  <!-- Set image name and tag -->
  <ContainerRepository>myapp</ContainerRepository>
  <ContainerImageTag>1.0.0</ContainerImageTag>
</PropertyGroup>
```

## Development Stage

Add a development stage for local dev with hot reload:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS base
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore

FROM base AS development
COPY . .
ENTRYPOINT ["dotnet", "watch", "run"]

FROM base AS build
COPY . .
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0-noble-chiseled AS production
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

Build development: `docker build --target development -t myapp:dev .`

## Cache Optimization

Use BuildKit cache mount for NuGet packages:

```dockerfile
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore
```

## SHA Pinning for Production

Pin exact image digests for reproducibility and security:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0@sha256:abc123... AS build
```

To find the current digest, run:
```bash
docker pull mcr.microsoft.com/dotnet/sdk:10.0
docker inspect --format='{{index .RepoDigests 0}}' mcr.microsoft.com/dotnet/sdk:10.0
```

## Required .dockerignore

Always create `.dockerignore`:

```dockerignore
**/bin/
**/obj/
**/.vs/
**/.vscode/
**/node_modules/
**/*.user
**/*.userosscache
**/*.suo
*.md
.git
.gitignore
Dockerfile*
docker-compose*
```

## Verification Checklist

- SDK image for build stage, runtime/aspnet for production
- .NET 8+ uses port 8080 (not 80)
- Copy .csproj files before source for cache efficiency
- Use `USER app` for non-root execution (chiseled images have this user)
- Chiseled images have no shell—use exec form only, no `&&` chains in final stage
- Include .dockerignore to exclude build artifacts
- Match runtime identifier (`-r linux-x64`) for self-contained builds
- Consider SHA pinning for production reproducibility
