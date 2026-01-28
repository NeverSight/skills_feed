---
name: fake-survey-gen-foundation
description: Foundation knowledge about the Fake Survey Generator project architecture, Aspire orchestration, service topology, and build/test infrastructure. Use this skill as reference context when working on features for this project.
---

# Fake Survey Generator - Project Foundation

## Project Overview

**Fake Survey Generator** is a modern distributed application built with **.NET 10.0** and **Aspire orchestration**. It demonstrates a microservice architecture with a React frontend, multiple backend services, and enterprise infrastructure patterns (Dapr, SQL Server, Redis, Azure deployment).

## Architecture Overview

### Frontend
- **Framework**: React 19 + Vite + TypeScript
- **Location**: `src/client/frontend/`
- **Authentication**: Auth0
- **Styling**: Tailwind CSS 4.1
- **Build**: `npm run build` (TypeScript checking + Vite bundling)
- **Dev Server**: Runs on port 3000 (managed by Aspire)

### Backend Services
- **Api Service** (FakeSurveyGenerator.Api)
  - Main REST API for survey operations (create, retrieve, list surveys)
  - User management endpoints
  - Admin endpoints (health checks, version info, secret retrieval)
  - Connected to: SQL Server database, Redis cache
  - Health checks: `/health/live` and `/health/ready`
  - Dapr sidecar enabled for distributed capabilities

- **Worker Service** (FakeSurveyGenerator.Worker)
  - Background job processing service
  - Connected to: SQL Server database, Redis cache
  - Runs alongside API service

### Supporting Services
- **SQL Server** (sql-server)
  - Persistent data volume
  - Database: "database"
  - Both API and Worker depend on it

- **Redis Cache** (cache)
  - Cache layer for performance
  - RedisInsight UI enabled (port 6379)
  - Both API and Worker depend on it

- **Dapr Sidecar** (on Api service)
  - Components path: `../../../dapr/components`
  - Local file-based secret store for development
  - Configurable for Azure Key Vault in production

## Aspire Orchestration

### Resource Dependencies (from AppHost.cs)
```
sql-server (base)
  ↓
cache (base)
  ↓
api (depends on sql-server + cache)
  ↓
worker (depends on sql-server + cache)
  ↓
ui (depends on api)
```

All resources use WaitFor() to ensure dependency chain completion before starting.

### Running Aspire
```bash
aspire run
```

This starts all resources in order and makes them available via:
- Aspire Dashboard: http://localhost:19888
- SQL Server: localhost:1433
- Redis: localhost:6379
- API: http://localhost:17623 (internal), exposed via proxy
- UI: https://localhost:3000
- RedisInsight: http://localhost:8001

## Project Structure

### Backend Solution
- **FakeSurveyGenerator.Api** - Main REST API service
- **FakeSurveyGenerator.Worker** - Background worker service
- **FakeSurveyGenerator.Application** - Business logic & application services
- **FakeSurveyGenerator.ServiceDefaults** - Aspire service configuration defaults
- **FakeSurveyGenerator.Proxy** - Proxy service for UI/API communication
- **FakeSurveyGenerator.AppHost** - Aspire orchestration & resource definitions

### Test Projects
- **FakeSurveyGenerator.Application.Tests** - Unit tests for business logic (TUnit)
  - Uses: AutoFixture, NSubstitute (mocking), InMemory EF Core
  
- **FakeSurveyGenerator.Api.Tests.Integration** - Integration tests (TUnit)
  - Uses: Testcontainers (real SQL Server & Redis), Respawn (DB cleanup), AutoFixture
  
- **FakeSurveyGenerator.Acceptance.Tests** - E2E tests (TUnit + Playwright)
  - Uses: Aspire Hosting Testing library, Playwright for .NET, TUnit.Playwright
  
- **TestTests** - Utility test project

All tests use **TrxReport** for result reporting and **CodeCoverage** analysis.

## Build System

### .NET Backend
- **Target Framework**: net10.0
- **Package Management**: Centralized in `Directory.Packages.props`
- **Version Management**: Nerdbank.GitVersioning
- **Key Dependencies**:
  - Aspire 13.1.0 (hosting, testing)
  - EF Core 10.0
  - AutoMapper
  - MediatR
  - FluentValidation

### Frontend (Node.js)
- **Build Tool**: Vite
- **Scripts**:
  - `npm run dev` - Dev server with hot reload
  - `npm run build` - Production build (TypeScript check + Vite bundle)
  - `npm run lint` - Biome formatter
- **Key Dependencies**: React 19, Auth0 SDK, FontAwesome, Tailwind CSS 4.1

## Build Commands

### Backend (from repository root)
```bash
# Build all backend projects
dotnet build

# Run all tests with coverage
dotnet test

# Run specific test project
dotnet test src/server/FakeSurveyGenerator.Application.Tests/
dotnet test src/server/FakeSurveyGenerator.Api.Tests.Integration/
```

### Frontend (from src/client/frontend/)
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Lint/format
npm run lint
```

## Dapr Integration

### Development Setup
- **Secret Store**: Local file-based (`dapr/components/local-file.yml`)
- **Configuration**: `dapr/components/secrets.json`
- **Sidecar**: Auto-managed by Aspire on API service

### Production Setup
- **Secret Store**: Azure Key Vault
- **Configuration**: Via bicep deployments in `infra/` folder

## Key Patterns & Conventions

### API Endpoints
- **User Registration**: `POST /api/users/register` (Auth0 token required)
- **Survey Creation**: `POST /api/surveys` (creates survey for current user)
- **Survey Retrieval**: `GET /api/surveys/{id}` (retrieve specific survey)
- **Survey List**: `GET /api/surveys` (list all surveys for current user)
- **Health Checks**: `GET /health/live`, `GET /health/ready`

### Database & ORM
- **ORM**: Entity Framework Core 10.0 (code-first)
- **Migrations**: Managed via EF Core tooling
- **Strategy**: Application layer abstracts data access via repositories

### Testing Patterns
- **Unit Tests**: Async/await patterns, arrange-act-assert structure
- **Integration Tests**: Real database/cache via Testcontainers, Respawn for cleanup
- **Acceptance Tests**: Aspire orchestration + Playwright for UI interaction

## Common Development Tasks

### Adding a New API Endpoint
1. Create DTO/Command in Application layer
2. Create handler in Application layer
3. Register in Application DI setup
4. Create controller action in Api project
5. Add unit tests in Application.Tests
6. Add integration tests in Api.Tests.Integration

### Modifying Frontend Component
1. Update React component in `src/client/frontend/src/`
2. Run `npm run build` to validate TypeScript
3. Add UI assertions to E2E skill validation

### Adding Feature End-to-End
1. Implement backend logic (Application + Api layers)
2. Update frontend (React component)
3. Create unit tests
4. Create integration tests
5. Create acceptance test (Playwright)
6. Validate with `aspire run` + UI inspection
