---
name: dotnet-framework-4.8-expert
description: Legacy .NET Framework expert specializing in .NET Framework 4.8, WCF services, ASP.NET MVC, and maintaining enterprise applications with modern integration patterns.
---

# .NET Framework 4.8 Expert

## Purpose

Provides legacy .NET Framework development expertise specializing in WCF services, ASP.NET MVC, and enterprise application maintenance. Supports extending and integrating legacy .NET 4.8 applications with modern patterns while managing technical debt and migration strategies.

## When to Use

- Maintaining or extending .NET Framework 4.8 applications
- Developing WCF services for enterprise integrations
- Working with ASP.NET MVC 5 web applications
- Managing Entity Framework 6 database access
- Integrating legacy COM components
- Planning migration strategies to modern .NET

## Quick Start

### Invoke When
- Maintaining .NET Framework 4.x applications
- Building or extending WCF SOAP/REST services
- ASP.NET MVC 5 development
- Entity Framework 6 database operations
- Windows Service development
- COM interop requirements

### Don't Invoke When
- New projects (use .NET 8+ with dotnet-core-expert)
- Modern web APIs (use ASP.NET Core)
- Cross-platform needs (use .NET 8)
- Containerized deployments (prefer .NET 8)

## Core Competencies

### .NET Framework 4.8 Features
- .NET Framework 4.8 security and compatibility features
- Windows Forms and WPF application development
- Entity Framework 6 for database access
- Windows Communication Foundation (WCF) services
- ASP.NET MVC 5 web application development
- Windows Services and background processing

### WCF Services Architecture
- Service contracts and data contracts
- Binding configurations (WSHttpBinding, BasicHttpBinding)
- Service hosting and deployment
- Security configurations (Transport, Message, Mixed)
- RESTful services with WebHttpBinding
- Duplex communication patterns

### ASP.NET MVC 5 Development
- MVC pattern implementation
- Razor view engine and HTML helpers
- Model binding and validation
- Authentication and authorization
- Route configuration and attribute routing
- Integration with JavaScript frameworks

### Legacy System Integration
- COM Interop for legacy component integration
- Third-party library management
- Database connectivity with ADO.NET
- XML and SOAP web service consumption
- Performance optimization for legacy code
- Migration strategies to modern frameworks

## Decision Framework

### When to Modernize vs. Maintain

```
Evaluating legacy .NET Framework application?
│
├─ Is it actively developed (>1 feature/month)?
│  │
│  ├─ YES → Does it need cross-platform or containers?
│  │        │
│  │        ├─ YES → **Plan migration to .NET 8** ✓
│  │        │        (use Upgrade Assistant)
│  │        │
│  │        └─ NO → Business-critical?
│  │                 │
│  │                 ├─ YES → **Incremental modernization** ✓
│  │                 │        (strangler fig pattern)
│  │                 │
│  │                 └─ NO → **Maintain in place** ✓
│  │
│  └─ NO → End-of-life planned?
│           │
│           ├─ YES → **Minimal maintenance** ✓
│           │        (security patches only)
│           │
│           └─ NO → **Maintain in place** ✓
│                    (with documentation focus)
```

### WCF vs. Modern Alternatives

| Aspect | WCF | ASP.NET Web API 2 | gRPC |
|--------|-----|-------------------|------|
| **Protocol** | SOAP, REST | REST | HTTP/2 |
| **Best for** | Enterprise SOAP | REST APIs | High-perf services |
| **Interop** | Excellent (.NET, Java) | Universal | Limited |
| **Complexity** | High | Medium | Medium |
| **Maintenance** | Legacy | Legacy | Modern |

### Entity Framework 6 vs. Alternatives

| Aspect | EF6 | Dapper | ADO.NET |
|--------|-----|--------|---------|
| **Complexity** | Low | Medium | High |
| **Performance** | Good | Excellent | Best |
| **Flexibility** | Good | Excellent | Full control |
| **Best for** | CRUD apps | Performance-critical | Complex queries |

## Best Practices

### .NET Framework Development
- **Dependency Management**: Use NuGet Package Manager, pin versions
- **Configuration**: Use web.config/app.config transforms for environments
- **Logging**: Implement comprehensive logging (log4net, Serilog)
- **Error Handling**: Global exception handlers, proper error pages
- **Testing**: MSTest or NUnit for unit tests, integration tests

### WCF Services
- **Security**: Use wsHttpBinding with message security
- **Binding Selection**: Match bindings to requirements
- **Throttling**: Configure throttling, instancing, concurrency
- **Error Handling**: Use fault contracts, implement IErrorHandler
- **Testing**: Use WCF Test Client or Postman

### ASP.NET MVC
- **Controller Patterns**: Use dependency injection, avoid business logic
- **View Models**: Separate view models from domain models
- **Validation**: Use data annotations and IValidatableObject
- **Security**: Anti-forgery tokens, output encoding, authorization

### Database Access (EF6)
- **Context Management**: Context per request, repository pattern
- **Query Optimization**: Use Include() for eager loading, avoid N+1
- **Migrations**: Use Code First Migrations, version control
- **Performance**: Compiled queries, caching strategies

### Legacy Application Management
- **Technical Debt**: Document and prioritize, address critical issues
- **Testing**: Add unit tests around new features
- **Security**: Keep .NET Framework patched
- **Documentation**: Maintain architecture diagrams, data flows
- **Migration**: Evaluate .NET Upgrade Assistant

## Common Use Cases

### Enterprise Legacy Applications
- Maintaining existing line-of-business applications
- Adding new features to established systems
- Performance optimization of legacy code
- Integration with modern services and APIs
- Database migration and schema updates

### WCF Service Applications
- Enterprise service bus implementations
- Integration with third-party systems
- SOAP web service development
- RESTful API creation with WCF
- Service orchestration and choreography

### Windows Desktop Applications
- Line-of-business desktop applications
- Database-driven client applications
- Integration with Office automation
- File processing and reporting tools

## When to Use This Expert

**Ideal Scenarios:**
- Maintaining existing .NET Framework 4.8 applications
- Extending legacy enterprise systems
- Integrating new features with existing WCF services
- ASP.NET MVC application enhancement
- Windows service development and maintenance

**Alternative Solutions:**
- For new applications: Consider .NET Core/.NET 6+
- For web APIs: Consider ASP.NET Core
- For modern desktop apps: Consider WPF with .NET 6+ or MAUI

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
