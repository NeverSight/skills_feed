---
name: azure-swa
description: Comprehensive expertise for Azure Static Web Apps including architecture, configuration, API integration with Azure Functions, authentication, routing, deployment, and CI/CD. Use when building, configuring, deploying, or troubleshooting Azure Static Web Apps projects with frameworks like React, Angular, Vue, Blazor, or vanilla JavaScript.
version: 2.0
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Azure Static Web Apps (SWA) Orchestration Skill

Master Azure Static Web Apps—Microsoft's managed platform for full-stack web applications. This skill provides focused guidance organized by concern area. Select the resource that matches your current task.

## Quick Reference: When to Load Which Resource

| Task / Scenario | Load Resource |
|-----------------|---------------|
| Understanding SWA concepts, architecture, frameworks | `resources/core-concepts.md` |
| Routing, authentication rules, headers, fallback routes | `resources/configuration-routing.md` |
| Building APIs, calling from frontend, error handling | `resources/api-integration.md` |
| Login flow, roles, protecting routes, token management | `resources/authentication.md` |
| GitHub Actions, deployment, environment variables | `resources/deployment-cicd.md` |
| Custom domains, SSL, monitoring, troubleshooting | `resources/operations-monitoring.md` |

## Orchestration Protocol

### Phase 1: Task Analysis

Classify your task to identify the right resource:

**Task Type Classification:**
- **Architectural**: Understanding SWA concepts, choosing frameworks, design patterns → Load `core-concepts.md`
- **Configuration**: Setting up routing, security, headers, fallback behavior → Load `configuration-routing.md`
- **API Development**: Building functions, calling APIs, error handling → Load `api-integration.md`
- **Authentication**: Login flows, role-based access, user info → Load `authentication.md`
- **Deployment**: Setting up pipelines, environments, CI/CD configuration → Load `deployment-cicd.md`
- **Operations**: Monitoring, troubleshooting, custom domains, SSL → Load `operations-monitoring.md`

**Complexity Indicators:**
- Single concern vs. multi-component setup
- Development vs. production requirements
- Pre-existing vs. new project

### Phase 2: Resource Selection

Load only the resource(s) needed:

- **Single Resource**: When task clearly maps to one area
- **Sequential Resources**: When setup requires multiple steps (e.g., deployment → monitoring)
- **Cross-Resource**: When building complete solution (e.g., API → authentication → deployment)

### Phase 3: Execution & Validation

**During Execution:**
- Follow examples for your framework/language
- Apply patterns from the selected resource
- Test locally with SWA CLI when appropriate

**Before Deployment:**
- Verify configuration is complete
- Check staticwebapp.config.json
- Test authentication and API locally
- Review deployment logs

## Common Development Scenarios

### Scenario 1: Building a React App with API

1. Load `core-concepts.md` → Understand SWA architecture for React
2. Load `configuration-routing.md` → Set up SPA routing fallback
3. Load `api-integration.md` → Build Azure Functions API
4. Load `authentication.md` → Add login if needed
5. Load `deployment-cicd.md` → Configure GitHub Actions

### Scenario 2: Deploying Existing Angular App

1. Load `core-concepts.md` → Verify Angular is supported framework
2. Load `configuration-routing.md` → Set up navigation fallback for Angular routing
3. Load `deployment-cicd.md` → Configure build output location (`dist/<app-name>`)
4. Load `operations-monitoring.md` → Set up monitoring after deployment

### Scenario 3: Troubleshooting 404 Errors

1. Load `configuration-routing.md` → Check navigation fallback and route exclusions
2. Load `deployment-cicd.md` → Verify app_location and output_location
3. Load `operations-monitoring.md` → Enable debugging and review logs

### Scenario 4: Adding Role-Based Access Control

1. Load `authentication.md` → Configure auth providers
2. Load `configuration-routing.md` → Define routes with role restrictions
3. Load `api-integration.md` → Protect API endpoints with role checks

## Decision Tree: Which Resource?

```
START: What are you doing?
├─ Understanding/designing? → core-concepts.md
├─ Configuring routing/security? → configuration-routing.md
├─ Building/testing API? → api-integration.md
├─ Implementing login/auth? → authentication.md
├─ Setting up deployment? → deployment-cicd.md
└─ Running in production? → operations-monitoring.md
```

---

**Version:** 2.0 (Refactored - Modular Orchestration Pattern)
**Last Updated:** December 2024
**Maintained by:** Claude Skills Repository

## Resource Files Summary

The main SKILL.md is now an orchestration hub. Content is organized into 6 focused resource files:

- **core-concepts.md** - Architecture, frameworks, key concepts
- **configuration-routing.md** - staticwebapp.config.json, routing rules, headers
- **api-integration.md** - Azure Functions, calling APIs, error handling
- **authentication.md** - Auth providers, login flows, role-based access
- **deployment-cicd.md** - GitHub Actions, environments, CLI deployment
- **operations-monitoring.md** - Custom domains, SSL, monitoring, troubleshooting

All content preserved and significantly enhanced with better organization and accessibility.
