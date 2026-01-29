---
name: zero-skills
description: Comprehensive knowledge base for go-zero microservices framework. Use this skill when working with go-zero to understand correct patterns for REST APIs (Handler/Logic/Context architecture), RPC services (service discovery, load balancing), database operations (sqlx, MongoDB, caching), resilience patterns (circuit breaker, rate limiting), and troubleshooting common issues. Essential for generating production-ready go-zero code that follows framework conventions.
license: Apache-2.0
---

# go-zero Skills for AI Agents

Structured knowledge base optimized for AI agents to help developers work effectively with the [go-zero](https://github.com/zeromicro/go-zero) microservices framework.

## Overview

This skill provides AI agents with comprehensive go-zero knowledge to:
- Generate accurate code following go-zero conventions
- Understand the three-layer architecture (Handler → Logic → Model)
- Apply best practices for microservices development
- Troubleshoot common issues efficiently
- Build production-ready applications

## Quick Start

When helping with go-zero development:

1. **For new projects**: Start with [getting-started/quick-start.md](getting-started/quick-start.md)
2. **For specific patterns**: Reference the appropriate pattern guide
3. **For issues**: Check [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
4. **For best practices**: See [best-practices/overview.md](best-practices/overview.md)

## Core Patterns

### REST API Development
Reference: [references/rest-api-patterns.md](references/rest-api-patterns.md)

- Handler/Logic/Context three-layer architecture
- Request validation and error handling
- Middleware implementation (auth, logging, metrics)
- Response formatting with httpx
- Complete CRUD examples with ✅ correct and ❌ incorrect patterns

**When to use**: Creating or modifying REST API services, implementing HTTP endpoints

### RPC Services
Reference: [references/rpc-patterns.md](references/rpc-patterns.md)

- Protocol Buffers definitions and code generation
- Service discovery with etcd/consul
- Load balancing strategies
- Error handling and timeout configuration
- Client-server communication patterns

**When to use**: Building gRPC services, implementing service-to-service communication

### Database Operations
Reference: [references/database-patterns.md](references/database-patterns.md)

- SQL operations with sqlx (CRUD, transactions, batch operations)
- MongoDB integration patterns
- Redis caching strategies
- Connection pooling and performance optimization
- Model generation with goctl

**When to use**: Implementing data persistence, caching, or database queries

### Resilience Patterns
Reference: [references/resilience-patterns.md](references/resilience-patterns.md)

- Circuit breaker configuration
- Rate limiting and throttling
- Load shedding under high load
- Timeout and retry strategies
- Graceful degradation

**When to use**: Ensuring service reliability, handling failures, managing system load

## Integration with AI Tools

This skill works seamlessly with the go-zero AI ecosystem:

- **[ai-context](https://github.com/zeromicro/ai-context)**: Concise instructions for GitHub Copilot, Cursor, Windsurf
- **[mcp-zero](https://github.com/zeromicro/mcp-zero)**: Runtime tools for Claude Desktop/Code (goctl integration)

See [articles/ai-ecosystem-guide.md](articles/ai-ecosystem-guide.md) for complete integration guide.

## Project Structure

```
zero-skills/
├── SKILL.md                    # This file - skill entry point
├── getting-started/            # Quick start guides
│   └── quick-start.md
├── references/                 # Detailed pattern documentation
│   ├── rest-api-patterns.md
│   ├── rpc-patterns.md
│   ├── database-patterns.md
│   └── resilience-patterns.md
├── best-practices/             # Production recommendations
│   └── overview.md
├── troubleshooting/            # Common issues and solutions
│   └── common-issues.md
├── articles/                   # In-depth guides
│   └── ai-ecosystem-guide.md
└── examples/                   # Demo projects and scripts
    ├── verify-tutorial.sh
    └── demo-project/
```

## Common Workflows

### Creating a New REST API Service

1. Define API specification in `.api` file
2. Generate code with `goctl api go -api user.api -dir .`
3. Implement business logic in `logic` layer
4. Add validation and error handling
5. Test with httpx utilities

See complete workflow in [references/rest-api-patterns.md](references/rest-api-patterns.md)

### Implementing Database Operations

1. Design database schema
2. Generate model with `goctl model mysql datasource`
3. Inject model into ServiceContext
4. Use sqlx for queries in logic layer
5. Handle transactions and errors properly

See complete patterns in [references/database-patterns.md](references/database-patterns.md)

### Adding Middleware

1. Create middleware function in `internal/middleware/`
2. Register in route configuration
3. Implement authentication/authorization logic
4. Pass data through request context
5. Handle errors appropriately

See middleware patterns in [references/rest-api-patterns.md#middleware](references/rest-api-patterns.md)

## Key Principles

### ✅ Always Follow

- **Three-layer architecture**: Handler → Logic → Model separation
- **Error handling**: Use structured errors, not `fmt.Errorf` in APIs
- **Configuration**: Load config with `conf.MustLoad`
- **Context propagation**: Pass `ctx` through all layers
- **Type safety**: Define types in `.api` files, generate with goctl

### ❌ Never Do

- Put business logic in handlers
- Ignore errors or use bare `fmt.Errorf` for HTTP errors
- Hard-code configuration values
- Skip validation of user inputs
- Bypass the three-layer architecture

## Progressive Learning

**New to go-zero?**
1. Start with [getting-started/quick-start.md](getting-started/quick-start.md)
2. Build a simple REST API using [references/rest-api-patterns.md](references/rest-api-patterns.md)
3. Add database operations from [references/database-patterns.md](references/database-patterns.md)

**Building production services?**
1. Review [best-practices/overview.md](best-practices/overview.md)
2. Implement resilience patterns from [references/resilience-patterns.md](references/resilience-patterns.md)
3. Reference [troubleshooting/common-issues.md](troubleshooting/common-issues.md) for common pitfalls

**Extending capabilities?**
1. Check [articles/ai-ecosystem-guide.md](articles/ai-ecosystem-guide.md)
2. Use [examples/demo-project/](examples/demo-project/) to test configurations
3. Run [examples/verify-tutorial.sh](examples/verify-tutorial.sh) to validate setup

## Resources

- **Official documentation**: [go-zero.dev](https://go-zero.dev)
- **GitHub repository**: [zeromicro/go-zero](https://github.com/zeromicro/go-zero)
- **Community**: Join go-zero developer community (see main repo README)

## Version Compatibility

This skill targets go-zero 1.5+. Patterns are updated regularly to reflect framework evolution. Always check official documentation for the latest API changes.
