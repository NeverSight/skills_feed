---
name: blazor-blog-feature
description: Adds a complete blog feature to an existing Blazor WebAssembly Static Web App with Azure Functions backend and Azure File Share for markdown storage. Use when implementing blog functionality in .NET Blazor WASM projects with Azure infrastructure. Includes post listing, detail pages, markdown rendering, Azure Storage integration.
version: 2.0
---

# Blog Feature Skill for Blazor WASM + Azure Functions

This skill provides a complete, production-ready blog feature for Blazor WASM applications hosted on Azure Static Web Apps with serverless backend processing.

## Quick Reference: When to Load Which Resource

| Your Task | Load Resource | Key Concepts |
|-----------|---------------|--------------|
| Understand architecture, prerequisites, shared models | `resources/core-architecture.md` | 3-layer architecture, project structure, data models |
| Implement backend services, Azure Functions, file share integration | `resources/backend-services.md` | BlogStorageService, YAML parsing, DI setup |
| Build Blazor components, UI pages, styling | `resources/frontend-components.md` | Razor components, markdown rendering, responsive design |
| Configure Azure environment, local settings, deployment | `resources/azure-configuration.md` | Connection strings, file share setup, environment variables |
| Create sample content, test workflow, troubleshoot issues | `resources/sample-content-testing.md` | Sample markdown, testing checklist, common issues |

## Orchestration Protocol

### Phase 1: Setup & Understanding

**Before writing any code, establish context:**

1. Review your current Blazor WASM project structure
2. Confirm you have Azure Functions API project ready
3. Verify Azure Storage account and File Share access
4. Load `resources/core-architecture.md` to understand 3-layer design

**Quick assessment:**
- Do you have existing Blazor WASM + Functions project? → YES, proceed
- Do you need to understand what to build? → Load core-architecture.md first
- Are you setting up Azure resources? → Go to azure-configuration.md

### Phase 2: Implementation Selection

**Choose your implementation path:**

| Your Situation | Load This First | Then Load |
|---|---|---|
| Starting from scratch | core-architecture.md | backend-services.md |
| Backend complete, need UI | frontend-components.md | (skip backend-services.md) |
| Just need configuration help | azure-configuration.md | (reference other resources as needed) |
| Debugging or testing | sample-content-testing.md | (target troubleshooting section) |

### Phase 3: Execution & Validation

**Implementation sequence:**

1. **Create project structure** (core-architecture.md Step 1-2)
2. **Add NuGet packages** (backend-services.md)
3. **Implement BlogStorageService** (backend-services.md)
4. **Create Azure Functions** (backend-services.md)
5. **Build Blazor components** (frontend-components.md)
6. **Configure Azure environment** (azure-configuration.md)
7. **Test locally** (sample-content-testing.md testing workflow)
8. **Deploy to Azure** (azure-configuration.md deployment section)

**Validation checkpoints:**
- Backend: Functions respond correctly to test calls
- Frontend: Components load and display posts
- Integration: End-to-end blog viewing works
- Azure: Configuration deployed and accessible

## Common Workflow Scenarios

### Scenario 1: Fresh Implementation (First Time)
**Timeline: 2-3 hours**

1. Read `core-architecture.md` → understand what you're building
2. Follow `backend-services.md` → implement API layer
3. Follow `frontend-components.md` → build UI layer
4. Follow `azure-configuration.md` → configure Azure resources
5. Use `sample-content-testing.md` → validate with sample posts

### Scenario 2: Existing Backend, Need Frontend
**Timeline: 1 hour**

1. Skip to `frontend-components.md`
2. Reference `core-architecture.md` if component questions arise
3. Use sample posts from `sample-content-testing.md`
4. Deploy following `azure-configuration.md`

### Scenario 3: Update Existing Blog
**Timeline: 30 minutes**

1. Jump to relevant resource file
2. Reference back to `core-architecture.md` for context
3. Test changes with `sample-content-testing.md` checklist

### Scenario 4: Troubleshooting Issues
**Timeline: As needed**

1. Go directly to `sample-content-testing.md`
2. Find problem in troubleshooting section
3. Reference other resources for context if needed

## Architecture Summary

**Frontend → Backend → Storage:**
- Blazor WASM pages call HTTP endpoints
- Azure Functions retrieve from File Share
- Markdown files with YAML frontmatter contain all content
- No database needed (files are the database)

**Key Components:**
- **BlogStorageService**: Abstracts File Share interactions
- **BlogFunctions**: HTTP endpoints for listing/retrieving posts
- **Index/Post Razor Components**: Client UI for browsing
- **CSS Styling**: Responsive design for all screen sizes

## Implementation Complexity

| Component | Complexity | Time |
|-----------|-----------|------|
| Backend Services | Medium | 45 min |
| Azure Functions | Easy | 30 min |
| Frontend Components | Medium | 60 min |
| Styling | Easy | 30 min |
| Configuration | Easy | 20 min |
| **Total** | **Easy-Medium** | **~3 hours** |

## Prerequisites Checklist

- ✅ Existing Blazor WASM SWA project
- ✅ Azure Functions API project
- ✅ Azure Storage account with File Share
- ✅ .NET 10 SDK (or later)
- ✅ Azure CLI (for deployment)
- ✅ Visual Studio Code or Visual Studio

## Resource Files Summary

### `resources/core-architecture.md` (285 lines)
Foundational knowledge about the blog system architecture, project structure, and shared data models needed across frontend and backend.

**Load when:** Getting started, understanding the design, creating shared models

### `resources/backend-services.md` (425 lines)
Complete implementation of Azure File Share service integration, BlogStorageService class, and Azure Functions for blog operations.

**Load when:** Building the API layer, implementing backend services

### `resources/frontend-components.md` (610 lines)
Blazor Razor components for blog listing and detail pages, CSS styling for responsive design, navigation integration.

**Load when:** Building the UI layer, styling components, creating Razor pages

### `resources/azure-configuration.md` (445 lines)
Azure environment setup, local development configuration, File Share structure, deployment guidelines, and security considerations.

**Load when:** Setting up Azure resources, configuring environments, deploying to production

### `resources/sample-content-testing.md` (395 lines)
Sample markdown formats, complete testing workflow checklist, troubleshooting guide for common issues, and enhancement ideas.

**Load when:** Creating test data, validating implementation, debugging problems

## Best Practices

1. **Start with core-architecture.md** - Don't skip understanding the design
2. **Implement sequentially** - Backend first, then frontend, then configuration
3. **Test locally** - Use Azure Storage Emulator before deploying
4. **Use sample content** - Test with provided markdown examples
5. **Follow naming conventions** - Consistent file naming prevents errors

## Quick Navigation by Goal

| I want to... | Resource | Section |
|---|---|---|
| Understand the system | core-architecture.md | Architecture Overview |
| Create the backend | backend-services.md | BlogStorageService |
| Build the UI | frontend-components.md | Blog Listing Page |
| Set up Azure | azure-configuration.md | Azure File Share Setup |
| Test everything | sample-content-testing.md | Testing Workflow |
| Fix a problem | sample-content-testing.md | Troubleshooting Guide |
| Deploy to production | azure-configuration.md | Deployment Checklist |

## Support & Next Steps

**After implementation:**
- Add pagination for better performance (recommended)
- Implement search functionality
- Consider caching for frequently-accessed posts
- Monitor Azure Function cold starts
- Optimize featured image sizes for performance

**Enhancement opportunities:**
- RSS feed generation
- Comment system integration
- Post categories and tagging
- Admin content management interface
- Email newsletter subscription

---

**Built with:** Blazor WASM, Azure Functions, Azure File Share, Markdown, YAML frontmatter

**Skill Type:** Feature Implementation (Blazor WASM + Azure)

**Difficulty:** Easy-Medium (3-4 hours total)
