---
name: pocketbase
description: Comprehensive PocketBase development and deployment skill providing setup guides, schema templates, security patterns, API examples, data management scripts, and real-time integration patterns for building backend services with PocketBase.
---

# PocketBase Skill - Comprehensive Reference

## Overview

This skill provides modular, searchable documentation for PocketBase development. Use the table of contents below to navigate to specific topics. The researcher-pocketbase agent can efficiently search and extract information from the reference files based on your query. PocketBase is an open source backend in 1 file. It provides a realtime database, authentication, file storage, an admin dashboard and is extendable to much more.

## Quick Navigation

### For Newcomers
→ Start with [Getting Started](references/core/getting_started.md) for initial setup and basic concepts
→ Review [Collections](references/core/collections.md) to understand data modeling
→ See [Authentication](references/core/authentication.md) for user management
→ Check [API Rules & Filters](references/core/api_rules_filters.md) for security

### For Implementation
→ Browse [Schema Templates](references/templates/schema_templates.md) for pre-built data models
→ Use [Records API](references/api/api_records.md) for CRUD operations
→ Implement [Real-time](references/api/api_realtime.md) for live updates
→ Follow [Files Handling](references/core/files_handling.md) for file uploads
→ Read [Working with Relations](references/core/working_with_relations.md) for data relationships

### For Production
→ See [Going to Production](references/core/going_to_production.md) for deployment
→ Review [Security Rules](references/security_rules.md) for access control
→ Check [API Reference](references/api_reference.md) for complete API documentation

### For Advanced Users
→ Explore [Go Extensions](references/go/go_overview.md) for custom functionality
→ Study [Event Hooks](references/go/go_event_hooks.md) for automation
→ Learn [Database Operations](references/go/go_database.md) for advanced queries
→ Plan data migrations with [Data Migration Workflows](references/core/data_migration.md)

---

## Table of Contents

### Core Concepts & Setup
| Topic | Description | When to Use |
|-------|-------------|-------------|
| [Getting Started](references/core/getting_started.md) | Initial setup, quick start, basic concepts | First time using PocketBase, initial configuration |
| [CLI Commands](references/core/cli_commands.md) | PocketBase CLI, serve, migrate, admin, superuser | Development workflow, server management, migrations |
| [Collections](references/core/collections.md) | Collection types, schema design, rules, indexes | Designing data models, creating collections |
| [Authentication](references/core/authentication.md) | User registration, login, OAuth2, JWT tokens | Building user accounts, login systems |
| [API Rules & Filters](references/core/api_rules_filters.md) | Security rules, filtering, sorting, query optimization | Controlling data access, writing efficient queries |
| [Files Handling](references/core/files_handling.md) | File uploads, thumbnails, CDN, security | Managing file uploads, image processing |
| [Working with Relations](references/core/working_with_relations.md) | One-to-many, many-to-many, data relationships | Building complex data models, linking collections |
| [Going to Production](references/core/going_to_production.md) | Deployment, security hardening, monitoring, backups | Moving from development to production |
| [Data Migration Workflows](references/core/data_migration.md) | Import/export strategies, scripts, and tooling | Planning and executing data migrations |

---

### API Reference
| Endpoint | Description | Reference File |
|----------|-------------|----------------|
| Records API | CRUD operations, pagination, filtering, batch operations | [api_records.md](references/api/api_records.md) |
| Realtime API | WebSocket subscriptions, live updates, event handling | [api_realtime.md](references/api/api_realtime.md) |
| Files API | File uploads, downloads, thumbnails, access control | [api_files.md](references/api/api_files.md) |
| Collections API | Manage collections, schemas, rules, indexes | [api_collections.md](references/api/api_collections.md) |
| Settings API | App configuration, CORS, SMTP, general settings | [api_settings.md](references/api/api_settings.md) |
| Logs API | Access logs, authentication logs, request logs | [api_logs.md](references/api/api_logs.md) |
| Crons API | Background jobs, scheduled tasks, automation | [api_crons.md](references/api/api_crons.md) |
| Backups API | Database backups, data export, disaster recovery | [api_backups.md](references/api/api_backups.md) |
| Health API | System health, metrics, performance monitoring | [api_health.md](references/api/api_health.md) |

---

### SDKs & Development Tools
| SDK | Description | Reference File |
|-----|-------------|----------------|
| JavaScript SDK | Frontend integration, React, Vue, vanilla JS | [js_sdk.md](references/sdk/js_sdk.md) |
| Go SDK | Server-side integration, custom apps | [go_sdk.md](references/sdk/go_sdk.md) |
| Dart SDK | Mobile app integration (Flutter, etc.) | [dart_sdk.md](references/sdk/dart_sdk.md) |

---

### Go Extension Framework
| Topic | Description | Reference File |
|-------|-------------|----------------|
| Go Overview | Project structure, basic concepts, getting started | [go_overview.md](references/go/go_overview.md) |
| Event Hooks | Before/After hooks, custom logic, automation | [go_event_hooks.md](references/go/go_event_hooks.md) |
| Routing | Custom API endpoints, middleware, handlers | [go_routing.md](references/go/go_routing.md) |
| Database | Query builder, transactions, advanced queries | [go_database.md](references/go/go_database.md) |
| Records | Record CRUD, validation, custom fields | [go_records.md](references/go/go_records.md) |
| Collections | Dynamic schemas, collection management | [go_collections.md](references/go/go_collections.md) |
| Migrations | Schema changes, version control, deployment | [go_migrations.md](references/go/go_migrations.md) |
| Jobs & Scheduling | Background tasks, cron jobs, queues | [go_jobs_scheduling.md](references/go/go_jobs_scheduling.md) |
| Sending Emails | SMTP configuration, templated emails | [go_sending_emails.md](references/go/go_sending_emails.md) |
| Rendering Templates | HTML templates, email templates, PDFs | [go_rendering_templates.md](references/go/go_rendering_templates.md) |
| Console Commands | CLI commands, migrations, maintenance | [go_console_commands.md](references/go/go_console_commands.md) |
| Realtime | Custom realtime logic, event handling | [go_realtime.md](references/go/go_realtime.md) |
| File System | File storage, CDN, external storage providers | [go_filesystem.md](references/go/go_filesystem.md) |
| Logging | Structured logging, monitoring, debugging | [go_logging.md](references/go/go_logging.md) |
| Testing | Unit tests, integration tests, test helpers | [go_testing.md](references/go/go_testing.md) |
| Miscellaneous | Advanced features, utilities, tips | [go_miscellaneous.md](references/go/go_miscellaneous.md) |
| Record Proxy | Dynamic record behavior, computed fields | [go_record_proxy.md](references/go/go_record_proxy.md) |

---

### Reference Materials
| File | Description | Contents |
|------|-------------|----------|
| [Security Rules](references/security_rules.md) | Comprehensive security patterns | Owner-based access, role-based access, API rules |
| [Schema Templates](references/templates/schema_templates.md) | Pre-built data models | Blog, E-commerce, Social Network, Forums, Task Management |
| [API Reference](references/api_reference.md) | Complete API documentation | All endpoints, parameters, examples |

---

### Development Resources
| Resource | Description | Location |
|----------|-------------|----------|
| Scripts | Executable utilities for development | `scripts/` directory |
| Assets | Templates and configuration files | `assets/` directory |
| Docker Config | Production-ready Docker setup | `assets/docker-compose.yml` |
| Caddy Config | Automatic HTTPS configuration | `assets/Caddyfile` |
| Frontend Template | HTML/JS integration example | `assets/frontend-template.html` |
| Collection Schema | Blank collection template | `assets/collection-schema-template.json` |

---

## How to Use This Skill

### For the Researcher-Pocketbase Agent

This skill is designed for efficient information retrieval. When researching PocketBase topics:

1. **Start with Core Concepts** - Review `references/core/` for foundational knowledge
2. **Find API Details** - Use `references/api/` for specific API endpoints
3. **Look up Go Extensions** - Check `references/go/` for custom functionality
4. **Find Examples** - Reference `references/templates/` and `references/security_rules.md`

### Topic Categories

**Setup & Configuration**
- Getting Started → Initial setup and basic concepts
- CLI Commands → Development workflow, server management
- Going to Production → Deployment and production configuration
- Collections → Data model design

**Data Management**
- Collections → Creating and managing collections
- Working with Relations → Linking data across collections
- Files Handling → File uploads and storage

**Security & Access Control**
- Authentication → User management
- API Rules & Filters → Access control and queries
- Security Rules → Comprehensive security patterns

**API Integration**
- Records API → CRUD operations
- Realtime API → Live updates
- Files API → File management
- Other API endpoints → Settings, logs, backups, health

**Frontend Development**
- JavaScript SDK → Web integration
- Schema Templates → Pre-built data models
- Frontend Template → Integration example

**Backend Development**
- Go SDK → Server-side integration
- Go Extensions → Custom functionality
- Console Commands → CLI tools

### Common Query Patterns

**"How do I..."**
- How do I create a blog? → Schema Templates
- How do I set up authentication? → Authentication
- How do I upload files? → Files Handling
- How do I add real-time updates? → Realtime API

**"How to configure..."**
- How to configure production? → Going to Production
- How to set up security rules? → API Rules & Filters, Security Rules
- How to create custom endpoints? → Go Routing
- How to schedule jobs? → Jobs & Scheduling

**"What's the best way to..."**
- What's the best way to structure my data? → Collections, Working with Relations
- What's the best way to secure my API? → API Rules & Filters, Security Rules
- What's the best way to optimize queries? → API Rules & Filters
- What's the best way to handle files? → Files Handling

**"Error:..."**
- CORS errors → Authentication, Going to Production
- Permission errors → API Rules & Filters, Security Rules
- File upload errors → Files Handling
- Slow queries → API Rules & Filters (indexing)

**"Need to implement..."**
- Need user roles? → Authentication, Security Rules
- Need file uploads? → Files Handling
- Need real-time chat? → Realtime API
- Need custom logic? → Go Extensions

---

## Quick Reference Index

### Common Tasks
- [Set up PocketBase](references/core/getting_started.md#quick-setup)
- [Master the CLI](references/core/cli_commands.md#overview)
- [Create collection](references/core/collections.md#creating-collections)
- [Add authentication](references/core/authentication.md#registration)
- [Write security rules](references/core/api_rules_filters.md#common-rule-patterns)
- [Upload files](references/core/files_handling.md#uploading-files)
- [Create relations](references/core/working_with_relations.md#creating-relations)
- [Query data](references/api/api_records.md#read-records)
- [Set up real-time](references/api/api_realtime.md#subscriptions)
- [Deploy to production](references/core/going_to_production.md#deployment-options)

### Code Examples
- [React integration](references/core/getting_started.md#react-integration)
- [Vue.js integration](references/core/getting_started.md#vuejs-example)
- [Create record](references/api/api_records.md#create-record)
- [Filter queries](references/api/api_records.md#filtering)
- [File upload](references/core/files_handling.md#single-file-upload)
- [Custom endpoint](references/go/go_overview.md#custom-api-endpoints)
- [Event hook](references/go/go_overview.md#event-hooks)

### Best Practices
- [Schema design](references/core/collections.md#best-practices)
- [Security rules](references/security_rules.md#best-practices)
- [Query optimization](references/api/api_records.md#performance-tips)
- [Production deployment](references/core/going_to_production.md#best-practices-checklist)

---

## File Locations

### Core Documentation
```
/references/core/
├── getting_started.md          # Initial setup and concepts
├── cli_commands.md             # CLI commands and server management
├── collections.md              # Data modeling and collections
├── authentication.md           # User management
├── api_rules_filters.md        # Security and querying
├── files_handling.md           # File uploads and storage
├── working_with_relations.md   # Data relationships
└── going_to_production.md      # Deployment guide
```

### API Reference
```
/references/api/
├── api_records.md              # CRUD operations
├── api_realtime.md             # WebSocket subscriptions
├── api_files.md                # File management
├── api_collections.md          # Collection operations
├── api_settings.md             # App configuration
├── api_logs.md                 # Logging
├── api_crons.md                # Background jobs
├── api_backups.md              # Backups
└── api_health.md               # Health checks
```

### Go Extensions
```
/references/go/
├── go_overview.md              # Getting started
├── go_event_hooks.md           # Event system
├── go_routing.md               # Custom routes
├── go_database.md              # Database operations
├── go_records.md               # Record management
├── go_collections.md           # Collection management
├── go_migrations.md            # Schema changes
├── go_jobs_scheduling.md       # Background tasks
├── go_sending_emails.md        # Email integration
├── go_rendering_templates.md   # Templates
├── go_console_commands.md      # CLI tools
├── go_realtime.md              # Custom realtime
├── go_filesystem.md            # File storage
├── go_logging.md               # Logging
├── go_testing.md               # Testing
├── go_miscellaneous.md         # Advanced topics
└── go_record_proxy.md          # Dynamic behavior
```

### SDKs
```
/references/sdk/
├── js_sdk.md                   # JavaScript
├── go_sdk.md                   # Go
└── dart_sdk.md                 # Dart
```

### Templates & Security
```
/references/
├── security_rules.md           # Security patterns
├── templates/
│   └── schema_templates.md     # Pre-built schemas
└── api_reference.md            # Complete API docs
```

---

## Information Architecture

This skill follows a modular architecture designed for progressive disclosure:

1. **Quick Access** - SKILL.md provides immediate overview and navigation
2. **Focused Topics** - Each reference file covers one specific area
3. **Cross-References** - Files link to related topics
4. **Examples First** - Practical code examples in each file
5. **Searchable** - Clear titles and descriptions for quick lookup

### When to Use Each Section

**references/core/**
- New users starting with PocketBase
- Understanding fundamental concepts
- Basic implementation tasks

**references/api/**
- Implementing specific API features
- Looking up endpoint details
- API integration examples

**references/go/**
- Building custom PocketBase extensions
- Advanced functionality
- Custom business logic

**references/sdk/**
- Frontend or mobile integration
- SDK-specific features
- Language-specific examples

**references/security_rules.md**
- Complex access control scenarios
- Security best practices
- Multi-tenant applications

**references/templates/**
- Rapid prototyping
- Common application patterns
- Pre-built data models

---

## Notes for Researchers

This skill contains over 30 reference files covering all aspects of PocketBase development. The researcher-pocketbase agent should:

1. Match queries to appropriate topic areas
2. Extract specific information from relevant files
3. Provide comprehensive answers using multiple references
4. Suggest related topics for further reading
5. Identify best practices and common pitfalls

Each reference file is self-contained with examples, explanations, and best practices. Use the table of contents above to quickly navigate to the most relevant information for any PocketBase-related question.
