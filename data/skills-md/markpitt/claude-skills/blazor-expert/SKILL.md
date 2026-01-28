---
name: blazor-expert
description: Comprehensive Blazor development expertise covering Blazor Server, WebAssembly, and Hybrid apps. Use when building Blazor components, implementing state management, handling routing, JavaScript interop, forms and validation, authentication, or optimizing Blazor applications. Includes best practices, architecture patterns, and troubleshooting guidance.
version: 2.0
---

# Blazor Expert - Orchestration Hub

Expert-level guidance for developing applications with Blazor, Microsoft's framework for building interactive web UIs using C# instead of JavaScript.

## Quick Reference: When to Load Which Resource

| Task | Load Resource | Key Topics |
|------|---------------|-----------|
| **Build components, handle lifecycle events** | [components-lifecycle.md](resources/components-lifecycle.md) | Component structure, lifecycle methods, parameters, cascading values, RenderFragment composition |
| **Manage component state, handle events** | [state-management-events.md](resources/state-management-events.md) | Local state, EventCallback, data binding, cascading state, service-based state |
| **Configure routes, navigate between pages** | [routing-navigation.md](resources/routing-navigation.md) | Route parameters, constraints, navigation, NavLink, query strings, layouts |
| **Build forms, validate user input** | [forms-validation.md](resources/forms-validation.md) | EditForm, input components, DataAnnotations validation, custom validators |
| **Setup authentication & authorization** | [authentication-authorization.md](resources/authentication-authorization.md) | Auth setup, AuthorizeView, Authorize attribute, policies, claims |
| **Optimize performance, use JavaScript interop** | [performance-advanced.md](resources/performance-advanced.md) | Rendering optimization, virtualization, JS interop, lazy loading, WASM best practices |

## Orchestration Protocol

### Phase 1: Task Analysis

Identify your primary objective:
- **UI Building** → Load components-lifecycle.md
- **State Handling** → Load state-management-events.md
- **Navigation** → Load routing-navigation.md
- **Data Input** → Load forms-validation.md
- **User Access** → Load authentication-authorization.md
- **Speed/Efficiency** → Load performance-advanced.md

### Phase 2: Resource Loading

Open the recommended resource file(s) and search for your specific need using Ctrl+F. Each resource is organized by topic with working code examples.

### Phase 3: Implementation & Validation

- Follow code patterns from the resource
- Adapt to your specific requirements
- Test in appropriate hosting model (Server/WASM/Hybrid)
- Review troubleshooting section if issues arise

## Blazor Hosting Models Overview

### Blazor Server
- **How**: Runs on server via SignalR
- **Best For**: Line-of-business apps, need full .NET runtime, small download size
- **Trade-offs**: High latency, requires connection, server resource intensive

### Blazor WebAssembly
- **How**: Runs in browser via WebAssembly
- **Best For**: PWAs, offline apps, no server dependency, client-heavy applications
- **Trade-offs**: Large initial download, limited .NET APIs, slower cold start

### Blazor Hybrid
- **How**: Runs in MAUI/WPF/WinForms with Blazor UI
- **Best For**: Cross-platform desktop/mobile apps
- **Trade-offs**: Platform-specific considerations, additional dependencies

**Decision**: Choose based on deployment environment, offline requirements, and server constraints.

## Common Implementation Workflows

### Scenario 1: Build a Data-Entry Component

1. Read [components-lifecycle.md](resources/components-lifecycle.md) - Component structure section
2. Read [state-management-events.md](resources/state-management-events.md) - EventCallback pattern
3. Read [forms-validation.md](resources/forms-validation.md) - EditForm component
4. Combine: Create component with parameters → capture user input → validate → notify parent

### Scenario 2: Implement User Authentication & Protected Pages

1. Read [authentication-authorization.md](resources/authentication-authorization.md) - Setup section
2. Read [routing-navigation.md](resources/routing-navigation.md) - Layouts section
3. Read [authentication-authorization.md](resources/authentication-authorization.md) - AuthorizeView section
4. Combine: Configure auth → create login page → protect routes → check auth in components

### Scenario 3: Build Interactive List with Search/Filter

1. Read [routing-navigation.md](resources/routing-navigation.md) - Query strings section
2. Read [state-management-events.md](resources/state-management-events.md) - Data binding section
3. Read [performance-advanced.md](resources/performance-advanced.md) - Virtualization section
4. Combine: Capture search input → update URL query → fetch filtered data → virtualize if large

### Scenario 4: Optimize Performance of Existing App

1. Read [performance-advanced.md](resources/performance-advanced.md) - All sections
2. Identify bottlenecks:
   - Unnecessary renders? → ShouldRender override, @key directive
   - Large lists? → Virtualization
   - JS latency? → Module isolation pattern
3. Apply targeted optimizations from resource

## Key Blazor Concepts

### Component Architecture
- **Components**: Self-contained UI units with optional logic
- **Parameters**: Inputs to components, enable reusability
- **Cascading Values**: Share state with descendants without explicit parameters
- **Events**: Child-to-parent communication via EventCallback
- **Layouts**: Parent wrapper for consistent page structure

### State Management
- **Local State**: Component-specific fields and properties
- **Cascading Values**: Share state to descendants
- **Services**: Application-wide state via dependency injection
- **Event Binding**: React to user interactions
- **Data Binding**: Two-way synchronization with UI

### Routing & Navigation
- **@page Directive**: Make component routable
- **Route Parameters**: Pass data via URL (`{id:int}`)
- **Navigation**: Programmatic navigation via NavigationManager
- **NavLink**: UI component that highlights active route
- **Layouts**: Wrap pages with common structure

### Forms & Validation
- **EditForm**: Form component with validation support
- **Input Components**: Typed controls (InputText, InputNumber, etc.)
- **Validators**: DataAnnotations attributes or custom logic
- **EventCallback**: Notify parent of form changes
- **Messages**: Display validation errors to user

### Authentication & Authorization
- **Claims & Roles**: Identify users and define access levels
- **Policies**: Fine-grained authorization rules
- **Authorize Attribute**: Protect pages from unauthorized access
- **AuthorizeView**: Conditional rendering based on permissions
- **AuthenticationStateProvider**: Get current user information

### Performance Optimization
- **ShouldRender()**: Prevent unnecessary re-renders
- **@key Directive**: Help diffing algorithm match list items
- **Virtualization**: Render only visible items in large lists
- **JS Interop**: Call JavaScript from C# and vice versa
- **AOT/Trimming**: Reduce WASM download size (production)

## Best Practices Highlights

### Component Design
✅ **Single Responsibility** - Each component has one clear purpose
✅ **Composition** - Use RenderFragments for flexible layouts
✅ **Parameter Clarity** - Use descriptive names, mark required with `[EditorRequired]`
✅ **Proper Disposal** - Implement `IDisposable` to clean up resources
✅ **Event-Based Communication** - Use `EventCallback` for child-to-parent updates

### State Management
✅ **EventCallback Over Action** - Proper async handling
✅ **Immutable Updates** - Create new objects/collections, don't mutate
✅ **Service-Based State** - Use scoped services for shared state
✅ **Unsubscribe from Events** - Prevent memory leaks in Dispose
✅ **InvokeAsync for Background Threads** - Thread-safe state updates

### Routing & Navigation
✅ **Route Constraints** - Use `:int`, `:guid`, etc. to validate formats
✅ **NavLink Component** - Automatic active state highlighting
✅ **forceLoad After Logout** - Clear client-side state
✅ **ReturnUrl Pattern** - Redirect back after login
✅ **Query Strings** - Preserve filters/pagination across navigation

### Forms & Validation
✅ **EditForm + DataAnnotationsValidator** - Built-in validation
✅ **ValidationMessage** - Show field-level errors
✅ **Custom Validators** - Extend for complex rules
✅ **Async Validation** - Check server availability before submit
✅ **Loading State** - Disable submit button while processing

### Authentication & Authorization
✅ **Server Validation** - Never trust client-side checks alone
✅ **Policies Over Roles** - More flexible authorization rules
✅ **Claims for Details** - Store user attributes in claims
✅ **Cascading AuthenticationState** - Available in all components
✅ **Error Boundaries** - Graceful error handling

### Performance
✅ **@key on Lists** - Optimize item matching
✅ **ShouldRender Override** - Prevent unnecessary renders
✅ **Virtualization for Large Lists** - Only render visible items
✅ **JS Module Isolation** - Load and cache JS modules efficiently
✅ **AOT for WASM** - Production deployments

## Common Troubleshooting

### Component Not Re-rendering
- **Cause**: Mutation instead of reassignment
- **Fix**: Create new object/collection: `items = items.Append(item).ToList()`
- **Or**: Call `StateHasChanged()` manually

### Parameter Not Updating
- **Cause**: Parent not re-rendering or same object reference
- **Fix**: Parent must re-render, ensure new reference for objects
- **Debug**: Check OnParametersSet is firing

### JS Interop Errors
- **Cause**: Called before script loaded or wrong function name
- **Fix**: Use `firstRender` check, verify JS file path
- **Pattern**: Use module isolation: `await JS.InvokeAsync("import", "./script.js")`

### Authentication State Not Available
- **Cause**: Cascading parameter not provided or timing issue
- **Fix**: Ensure AuthenticationStateProvider configured
- **Pattern**: Always null-check and use `await AuthStateTask!` in code block

### Large List Performance Issues
- **Cause**: Rendering all items in DOM
- **Fix**: Use Virtualize component for 1000+ items
- **Alternative**: Paginate with buttons/infinite scroll

### Blazor Server Connection Issues
- **Cause**: SignalR connection dropped or configuration issue
- **Fix**: Implement reconnection UI, increase timeout
- **Config**: Adjust `CircuitOptions.DisconnectedCircuitRetentionPeriod`

## Resource Files Summary

### components-lifecycle.md
Complete guide to component structure, lifecycle methods, parameters, cascading values, and composition patterns. Essential for understanding Blazor component fundamentals.

### state-management-events.md
Comprehensive coverage of local and service-based state, event handling with EventCallback, data binding patterns, and component communication. Core for interactive UI building.

### routing-navigation.md
Complete routing reference including route parameters, constraints, programmatic navigation, query strings, and layout management. Essential for multi-page apps.

### forms-validation.md
Full forms API with EditForm component, input controls, DataAnnotations validation, custom validators, and form patterns. Required for data entry scenarios.

### authentication-authorization.md
Complete auth setup for Server and WASM, AuthorizeView, policies, claims-based access control, and login/logout patterns. Necessary for secured applications.

### performance-advanced.md
Performance optimization techniques including ShouldRender, virtualization, JavaScript interop patterns, lazy loading, and WASM best practices. Vital for production apps.

---

## Implementation Approach

When implementing Blazor features:

1. **Identify Your Task** - Match against the decision table above
2. **Load Relevant Resource** - Read the appropriate .md file
3. **Find Code Example** - Search resource for similar implementation
4. **Adapt to Your Context** - Modify for your specific requirements
5. **Test Thoroughly** - Verify in your hosting model
6. **Reference Troubleshooting** - Consult resource if issues arise

## Next Steps

- **New to Blazor?** Start with [components-lifecycle.md](resources/components-lifecycle.md)
- **Building Data App?** Move through: components → state → forms → validation
- **Scaling Existing App?** Focus on [performance-advanced.md](resources/performance-advanced.md)
- **Adding Security?** Follow [authentication-authorization.md](resources/authentication-authorization.md)

---

**Version**: 2.0 - Modular Orchestration Pattern  
**Last Updated**: December 4, 2025  
**Status**: Production Ready ✅
