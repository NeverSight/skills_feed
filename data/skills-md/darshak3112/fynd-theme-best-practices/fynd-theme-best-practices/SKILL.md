---
name: fynd-theme-best-practices
description: Optimize, refactor, and explain Fynd Commerce theme codebases (FDK React templates). Use when asked to locate or explain features in `src/`, apply theme best practices, reason about theme sections/blocks, or clarify Storefront GraphQL queries like `productPrice`.
---

# Fynd Theme Best Practices

## Quick Start Decision Tree
Use this skill when the request involves:
1. **"Where is X feature?"** → Codebase navigation workflow
2. **"How do I implement Y?"** → Best practices + pattern workflow
3. **"This isn't working"** → Debugging workflow
4. **"What's wrong with this code?"** → Code review workflow
5. **"How do sections/blocks work?"** → Theme architecture workflow
6. **"GraphQL query issues"** → GraphQL workflow

**Prerequisites**:
- For React best practices: install the `vercel-react-best-practices` skill if not available
- For codebase questions: ensure you have access to the project's `src/` directory

## Core Workflows

### 1. Codebase Navigation Workflow
**Goal**: Locate specific features, components, or functionality

**Step 1**: Identify the feature domain
- **UI Components** → `src/components/`
- **Page Routes** → `src/pages/`
- **Feature Modules** (Cart, PLP, Auth, Checkout) → `src/page-layouts/`
- **Utilities/Hooks** → `src/helper/`
- **Constants/Mappings** → `src/constants/`
- **Styling** → `src/styles/`

**Step 2**: Use targeted search patterns
```bash
# Product listing/filters/facets
rg -n "filter|facet|sort|range" src/page-layouts/plp/

# Data fetching/GraphQL
rg -n "productPrice|graphql|fpi|useFPI" src/

# Sections/blocks
rg -n "SectionRenderer|settings|blocks" src/

# Authentication/user flows
rg -n "login|auth|user|token" src/page-layouts/

# Cart/checkout
rg -n "cart|checkout|payment|address" src/page-layouts/
```

**Step 3**: Read component READMEs
- Check `src/components/README.md` for component index
- Check `src/pages/README.md` for page index
- Most components have co-located README files with usage examples

**Reference**: `references/codebase_fdk_react_templates.md`

### 2. Debugging Workflow
**Goal**: Troubleshoot issues in FDK theme code

**Common Issue Patterns**:

**A. SSR/Hydration Errors**
- **Symptom**: "window is not defined", hydration mismatch
- **Check**: Is `isRunningOnClient()` used before accessing browser APIs?
- **Reference**: `references/common_gotchas.md` (SSR Safety section)

**B. Data Not Loading**
- **Check 1**: Is `useFPI()` properly imported and called?
- **Check 2**: Are GraphQL queries fetching all required fields?
- **Check 3**: Is data available in both SSR and client-side navigation?
- **Reference**: `references/debugging_guide.md` (Data Fetching section)

**C. Styling Issues**
- **Check 1**: Are LESS files properly imported?
- **Check 2**: Is CSS module scope conflicting?
- **Check 3**: Are Tailwind utilities (if used) configured correctly?
- **Reference**: `references/tailwind_integration.md`

**D. Section/Block Not Rendering**
- **Check 1**: Does the component export both `Component` and `settings`?
- **Check 2**: Is the settings schema valid?
- **Check 3**: Is the section registered in theme configuration?
- **Reference**: `references/themes_sections.md`

**E. Hook Issues**
- **Check 1**: Are hooks called at the top level (not conditional)?
- **Check 2**: Review custom hook usage in `references/global_components_and_hooks.md`
- **Common hooks**: `useFPI()`, `useGlobalStore()`, `useGlobalTranslation()`, `useMobile()`, `useViewport()`

**Reference**: `references/debugging_guide.md`

### 3. Code Review Workflow
**Goal**: Review and improve existing theme code

**Review Checklist**:
1. **SSR Safety** - All browser API usage guarded
2. **GraphQL Efficiency** - Single query with minimal fields
3. **Component Size** - Functions under 150 lines, components focused
4. **Hooks Usage** - Proper dependency arrays, no violations
5. **Performance** - Memoization, code splitting, lazy loading
6. **Accessibility** - Semantic HTML, ARIA, keyboard navigation
7. **Error Handling** - Error boundaries, fallback UI
8. **Type Safety** - PropTypes or TypeScript
9. **Analytics** - No duplicate events, proper tracking
10. **Security** - Input sanitization, no hardcoded secrets

**References**:
- `references/themes_best_practices_full.md`
- `references/development_best_practices_checklist.md`
- `references/testing_best_practices_checklist.md`
- `references/performance_optimization_core_web_vitals.md`

### 4. Implementation Workflow
**Goal**: Build new features following FDK patterns

**Step 1**: Choose the right location
- **Reusable UI** → `src/components/` (with README)
- **Feature-specific UI** → `src/page-layouts/[feature]/Components/`
- **Route page** → `src/pages/`
- **Custom hook** → `src/helper/hooks/`
- **Utility function** → `src/helper/`
- **Constants** → `src/constants/`

**Step 2**: Follow FDK patterns
```javascript
// Platform access
import { useFPI } from "fdk-core/utils";
const fpi = useFPI();

// Global state
import { useGlobalStore } from "fdk-core/utils";
const userData = useGlobalStore(fpi.getters.getUserData);

// Translations
import { useGlobalTranslation } from "fdk-core/utils";
const t = useGlobalTranslation("translation");

// SSR safety
import { isRunningOnClient } from "fdk-core/utils";
if (isRunningOnClient()) {
  // Browser-only code
}
```

**Step 3**: Apply best practices
- Use functional components
- Implement proper error boundaries
- Add co-located LESS modules it is being used else use tailwind
- Use code splitting for large components

**References**:
- `references/common_patterns.md`
- `references/code_examples.md`
- `references/global_provider_resolvers.md`

### 5. Theme Sections Workflow
**Goal**: Work with theme sections and blocks

**Understanding the hierarchy**:
- **Theme** → collection of pages
- **Page** → collection of sections
- **Section** → configured component with settings
- **Block** → repeatable item within a section

**Section structure**:
```javascript
// Must export both Component and settings
export const Component = ({ props, blocks, globalConfig }) => {
  // Render logic
};

export const settings = {
  name: "section-name",
  label: "Section Label",
  props: [
    // Input schema for section settings
  ],
  blocks: [
    // Block definitions
  ]
};
```

**References**:
- `references/themes_sections.md`
- `references/key_concepts_pages_sections_blocks.md`
- `references/sections_code_splitting.md`

### 6. GraphQL Workflow
**Goal**: Work with Storefront GraphQL queries

**Best practices**:
- Fetch all needed data in a single query
- Request only required fields
- Use variables for dynamic values
- Handle loading and error states
- Cache appropriately

**Common queries**:
- `productPrice` - Product pricing data
- Application configuration
- User data
- Cart data

**References**:
- `references/graphql_product_price.md`
- `references/graphql_application_client_libraries.md`

### 7. Testing \u0026 Verification Workflow

**Local testing**:
1. Run development server
2. Test SSR (first load) and SPA (navigation)
3. Test on mobile and desktop viewports
4. Check browser console for errors
5. Verify analytics events

**References**:
- `references/local_testing_checklist.md`
- `references/testing_best_practices_checklist.md`

## Advanced Topics

### Multilingual Support
- Reference: `references/themes_multilingual.md`
- Use `useGlobalTranslation()` for all user-facing text
- Support RTL layouts with `useLocaleDirection()`

### Custom Templates
- Reference: `references/custom_templates.md`
- Create custom page templates for specific use cases

### Tailwind Integration  
- Reference: `references/tailwind_integration.md`
- Configure Tailwind for FDK themes
- Use utility classes alongside LESS

### Performance Optimization
- Reference: `references/performance_optimization_core_web_vitals.md`
- Optimize Core Web Vitals (LCP, FID, CLS)
- Image optimization with `transformImage`
- Code splitting and lazy loading

### Authentication Patterns
- Reference: `references/auth_guard.md`
- Protect routes and components
- Handle guest vs. authenticated users

### Data Management
- Reference: `references/data_management_fdk_store.md`
- FPI store patterns
- Custom values and configuration

### FDK CLI Usage
- References:
  - `references/fdk_overview_cli.md`
  - `references/fdk_cli_getting_started_versioning.md`
- Initialize, develop, and deploy themes

## Output Guidelines

When answering requests:
1. **Be specific**: Provide exact file paths and line numbers where relevant
2. **Explain why**: Don't just point to a location, explain the architectural reason
3. **Show patterns**: Reference existing code patterns in the codebase
4. **Provide examples**: Use code snippets from references or create minimal examples
5. **Ask when uncertain**: If context is missing (route name, feature flag, etc.), ask for it
6. **Think incrementally**: Suggest small, safe changes that align with existing patterns

## Complete Reference Index

### Core Concepts
- `references/intro_themes.md` - Introduction to Fynd themes
- `references/anatomy_of_theme.md` - Theme structure
- `references/key_concepts_pages_sections_blocks.md` - Architecture fundamentals
- `references/themes_get_started.md` - Getting started guide

### Best Practices
- `references/themes_best_practices.md` - Concise best practices
- `references/themes_best_practices_full.md` - Comprehensive best practices
- `references/development_best_practices_checklist.md` - Development checklist
- `references/testing_best_practices_checklist.md` - Testing checklist
- `references/performance_optimization_core_web_vitals.md` - Performance guide

### Development
- `references/themes_development.md` - Development workflow
- `references/boilerplate_overview.md` - Boilerplate structure
- `references/theme_sync.md` - Theme synchronization
- `references/local_testing_checklist.md` - Local testing guide

### Sections & Blocks
- `references/themes_sections.md` - Section architecture
- `references/sections_code_splitting.md` - Code splitting for sections

### Data & State
- `references/data_management_fdk_store.md` - FPI store patterns
- `references/global_provider_resolvers.md` - Global providers
- `references/server_fetch.md` - Server-side data fetching
- `references/fpi_mutations.md` - FPI mutation patterns

### GraphQL
- `references/graphql_application_client_libraries.md` - GraphQL overview
- `references/graphql_product_price.md` - Product price query

### Components & Hooks
- `references/global_components_and_hooks.md` - Global utilities
- `references/color_palette_mapping.md` - Color system
- `references/auth_guard.md` - Authentication patterns

### Styling
- `references/tailwind_integration.md` - Tailwind setup and usage

### Internationalization
- `references/themes_multilingual.md` - Multilingual support

### Customization
- `references/custom_templates.md` - Custom page templates

### CLI & Tooling
- `references/fdk_overview_cli.md` - FDK CLI overview
- `references/fdk_cli_getting_started_versioning.md` - CLI getting started

### Codebase
- `references/codebase_fdk_react_templates.md` - Codebase structure and patterns
- `references/actual_utilities.md` - Complete utility functions reference from actual codebase
- `references/fdk_core_components.md` - FDKLink, serverFetch, and core FDK components
- `references/core_components.md` - All 11 core UI components (fy-image, fy-button, modal, etc.)

### Troubleshooting (Enhanced)
- `references/debugging_guide.md` - Debugging common issues
- `references/common_gotchas.md` - Common pitfalls and solutions
- `references/common_patterns.md` - Reusable code patterns
- `references/code_examples.md` - Practical code examples
