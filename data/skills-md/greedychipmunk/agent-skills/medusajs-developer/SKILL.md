---
name: medusajs-developer
description: Specialized agent for MedusaJS development including custom modules, API routes, data models, workflows, scheduled jobs, and third-party integrations. Provides expert guidance on commerce platform architecture and plugin development.
license: MIT
compatibility: Requires Node.js 18+, TypeScript, and MedusaJS v2
metadata:
  category: ecommerce
  framework: medusajs
  version: 2.x
  expertise: commerce-modules, api-development, plugin-creation
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Grep, Glob, WebFetch]
---

# MedusaJS Developer Agent Skill

An expert agent specializing in MedusaJS development, focusing on building scalable e-commerce solutions with custom modules, API integrations, and third-party plugins.

## Core Capabilities

### 1. Custom Module Development
- **Data Models**: Create and manage data models using MedusaJS DML
- **Module Services**: Implement service layers with automatic CRUD operations
- **Module Configuration**: Set up proper module structure and exports
- **Database Migrations**: Generate and manage database schema changes

### 2. API Route Development
- **Custom Endpoints**: Create REST API routes in `src/api/[route-name]/route.ts`
- **HTTP Methods**: Implement GET, POST, PUT, DELETE handlers
- **Request/Response Handling**: Manage MedusaRequest and MedusaResponse objects
- **Authentication**: Integrate with MedusaJS auth systems

### 3. Commerce Module Integration
- **18 Built-in Modules**: Work with API Key, Auth, Cart, Customer, Order, Payment, Product, Pricing, Promotion, Tax, and more
- **Module Links**: Create relationships between different modules
- **Custom Fields**: Extend existing modules with additional data fields
- **Module Composition**: Combine multiple modules for complex workflows

### 4. Workflow & Automation
- **Scheduled Jobs**: Create recurring tasks with cron expressions
- **Event Handling**: Implement subscribers for asynchronous operations
- **Business Logic**: Orchestrate complex commerce workflows
- **Background Processing**: Handle long-running operations efficiently

### 5. Third-Party Integrations
- **Payment Providers**: Integrate custom payment gateways
- **External APIs**: Connect with shipping, tax, and inventory services
- **Webhooks**: Handle incoming webhooks from external systems
- **Data Synchronization**: Sync data with external platforms

## Development Patterns

### Module Structure
```typescript
// src/modules/my-module/models/post.ts
import { model } from "@medusajs/framework/utils"

const Post = model.define("post", {
  id: model.id().primaryKey(),
  title: model.text(),
  content: model.text().nullable(),
  published: model.boolean().default(false)
})

export default Post
```

### API Route Example
```typescript
// src/api/posts/route.ts
import { MedusaRequest, MedusaResponse } from "@medusajs/framework/http"

export const GET = async (req: MedusaRequest, res: MedusaResponse) => {
  const postService = req.scope.resolve("postService")
  const posts = await postService.listPosts()
  
  res.json({ posts })
}

export const POST = async (req: MedusaRequest, res: MedusaResponse) => {
  const postService = req.scope.resolve("postService")
  const post = await postService.createPost(req.body)
  
  res.json({ post })
}
```

### Scheduled Job Example
```typescript
// src/jobs/sync-inventory.ts
import { MedusaContainer } from "@medusajs/framework/types"

export default async function syncInventoryJob(container: MedusaContainer) {
  const inventoryService = container.resolve("inventoryService")
  await inventoryService.syncWithExternalProvider()
}

export const config = {
  name: "sync-inventory",
  schedule: "0 */6 * * *" // Every 6 hours
}
```

## Best Practices

### 1. Project Setup
- Use MedusaJS CLI for project initialization
- Follow TypeScript best practices
- Implement proper error handling
- Set up comprehensive testing

### 2. Module Design
- Keep modules focused on single domains
- Use clear naming conventions
- Implement proper validation
- Document module interfaces

### 3. API Design
- Follow RESTful conventions
- Use proper HTTP status codes
- Implement pagination for list endpoints
- Validate input data thoroughly

### 4. Performance Optimization
- Use database indexes appropriately
- Implement caching strategies
- Optimize database queries
- Handle large datasets efficiently

### 5. Integration Patterns
- Use environment variables for configuration
- Implement retry mechanisms for external calls
- Handle rate limiting gracefully
- Log integration activities properly

## Common Tasks

### Creating a New Module
1. Create module directory structure
2. Define data models with proper relationships
3. Implement service layer with business logic
4. Generate and run database migrations
5. Create API routes for module operations
6. Add comprehensive tests

### Setting Up Third-Party Integration
1. Install necessary dependencies
2. Configure environment variables
3. Create service for external API communication
4. Implement webhook handlers if needed
5. Add error handling and logging
6. Test integration thoroughly

### Implementing Custom Workflow
1. Identify business process steps
2. Create necessary data models
3. Implement workflow orchestration
4. Add event handlers for state changes
5. Create monitoring and alerting
6. Document workflow behavior

## Troubleshooting

### Common Issues
- **Migration Failures**: Check model definitions and database constraints
- **Service Resolution**: Verify module exports and dependency injection
- **API Errors**: Validate request/response formats and authentication
- **Performance Issues**: Analyze database queries and implement caching

### Debugging Strategies
- Use MedusaJS debugging tools
- Check application logs for errors
- Verify database schema matches models
- Test API endpoints with proper headers
- Monitor external service responses

## Code Templates

This skill includes production-ready code templates in the `templates/` directory based on official MedusaJS documentation and best practices.

### Available Templates

#### module-complete.ts
Complete custom module structure with:
- Multiple data models with various property types
- One-to-many and many-to-many relationships
- Main service with custom methods
- Additional services with dependency injection

**Use case:** Creating custom modules (Blog, Brand, Restaurant, etc.)

#### api-route-complete.ts
Complete REST API route with:
- GET, POST, PUT, DELETE handlers
- Zod validation schemas
- Authentication and validation middlewares
- Error handling and logging
- Query integration for related data

**Use case:** Exposing module functionality via API endpoints

#### workflow-complete.ts
Complete workflow with:
- Multiple steps with compensation functions
- Data transformation between steps
- Conditional execution
- Integration with Medusa modules

**Use case:** Complex business logic with rollback requirements

#### subscriber-complete.ts
Event subscriber patterns:
- Basic event handling
- Workflow execution in subscribers
- Multi-event subscribers
- Retry logic and error handling

**Use case:** Responding to Medusa events (order.placed, product.created, etc.)

#### module-link.ts
Module link patterns:
- Basic links between modules
- List links (one-to-many)
- Custom columns in link tables
- Creating, dismissing, and querying links

**Use case:** Creating relationships between different modules

#### scheduled-job.ts
Scheduled job patterns:
- Basic scheduled tasks
- Batch processing
- External API integration
- Common cron patterns

**Use case:** Recurring automated tasks (sync, cleanup, reports)

### Template Usage Example

```bash
# Copy template to your project
cp templates/module-complete.ts src/modules/brand/

# Customize for your needs
# - Rename identifiers
# - Add/remove properties
# - Implement business logic

# Generate and run migrations
./scripts/generate-migration.sh brand
./scripts/run-migrations.sh
```

### Common Template Combinations

**E-commerce Extension:**
1. module-complete.ts → Create custom module
2. module-link.ts → Link to Product module
3. api-route-complete.ts → Create API endpoints
4. workflow-complete.ts → Implement business logic
5. subscriber-complete.ts → Handle events

**Data Synchronization:**
1. workflow-complete.ts → Sync workflow
2. scheduled-job.ts → Run periodically
3. subscriber-complete.ts → Trigger on events

See `templates/README.md` for detailed documentation, best practices, and more examples.

## Helper Scripts

This skill includes a collection of helper scripts in the `scripts/` directory to streamline common MedusaJS development tasks.

### Database Management Scripts

#### db-setup.sh
Creates a database, runs migrations, and syncs links in one command.

```bash
./scripts/db-setup.sh [database-name]
```

**Example:**
```bash
./scripts/db-setup.sh medusa-store
```

#### generate-migration.sh
Generates migration files for specified modules.

```bash
./scripts/generate-migration.sh <module-name> [additional-modules...]
```

**Examples:**
```bash
./scripts/generate-migration.sh blog
./scripts/generate-migration.sh blog product-custom
```

#### run-migrations.sh
Runs all pending migrations with optional flags to skip links or data migrations.

```bash
./scripts/run-migrations.sh [--skip-links] [--skip-data]
```

**Examples:**
```bash
./scripts/run-migrations.sh
./scripts/run-migrations.sh --skip-links
```

#### rollback-migration.sh
Reverts the last migration for specified modules with safety confirmation.

```bash
./scripts/rollback-migration.sh <module-name> [additional-modules...]
```

### Development & Build Scripts

#### dev-server.sh
Starts the Medusa application in development mode with hot reloading.

```bash
./scripts/dev-server.sh [--host HOST] [--port PORT]
```

**Examples:**
```bash
./scripts/dev-server.sh
./scripts/dev-server.sh --host 0.0.0.0 --port 9001
```

#### build-production.sh
Creates a production-ready build of the Medusa application or admin only.

```bash
./scripts/build-production.sh [--admin-only]
```

**Examples:**
```bash
./scripts/build-production.sh
./scripts/build-production.sh --admin-only
```

#### start-production.sh
Starts the built Medusa application in production mode.

```bash
./scripts/start-production.sh
```

#### predeploy.sh
Runs migrations and syncs links before deployment (for CI/CD pipelines).

```bash
./scripts/predeploy.sh
```

### Testing Scripts

#### setup-testing.sh
Installs and configures Jest and Medusa testing tools, creates test directories and configuration files.

```bash
./scripts/setup-testing.sh
```

#### run-tests.sh
Runs integration and unit tests with options for different test types.

```bash
./scripts/run-tests.sh [http|modules|unit|all]
```

**Examples:**
```bash
./scripts/run-tests.sh all
./scripts/run-tests.sh http
./scripts/run-tests.sh modules
./scripts/run-tests.sh unit
```

### Scaffolding Scripts

#### create-module.sh
Creates the basic structure for a new custom module with service and model directories.

```bash
./scripts/create-module.sh <module-name>
```

**Example:**
```bash
./scripts/create-module.sh blog
```

**Generated Structure:**
```
src/modules/<module-name>/
├── index.ts
├── service.ts
├── models/
└── __tests__/
```

#### create-api-route.sh
Creates a new API route with basic CRUD operations (GET, POST, PUT, DELETE).

```bash
./scripts/create-api-route.sh <route-name>
```

**Example:**
```bash
./scripts/create-api-route.sh posts
```

**Generated Endpoints:**
- `GET /api/<route-name>` - List all items
- `POST /api/<route-name>` - Create new item
- `GET /api/<route-name>/:id` - Get single item
- `PUT /api/<route-name>/:id` - Update item
- `DELETE /api/<route-name>/:id` - Delete item

#### create-scheduled-job.sh
Creates a new scheduled job with cron configuration template.

```bash
./scripts/create-scheduled-job.sh <job-name>
```

**Example:**
```bash
./scripts/create-scheduled-job.sh sync-inventory
```

**Common Cron Patterns:**
- `"0 0 * * *"` - Daily at midnight
- `"0 */6 * * *"` - Every 6 hours
- `"*/15 * * * *"` - Every 15 minutes
- `"0 9 * * 1"` - Every Monday at 9 AM

### Plugin Development Scripts

#### plugin-develop.sh
Starts a development server for a plugin with auto-reload (run from plugin directory).

```bash
./scripts/plugin-develop.sh
```

#### plugin-build.sh
Builds a plugin for publishing to NPM (run from plugin directory).

```bash
./scripts/plugin-build.sh
```

## Common Workflows

### Creating a New Feature Module

```bash
# 1. Create the module structure
./scripts/create-module.sh my-feature

# 2. Add data models in src/modules/my-feature/models/

# 3. Update service.ts with your models

# 4. Generate migrations
./scripts/generate-migration.sh my-feature

# 5. Run migrations
./scripts/run-migrations.sh

# 6. Create API routes
./scripts/create-api-route.sh my-feature

# 7. Write tests
# Add tests in src/modules/my-feature/__tests__/

# 8. Run tests
./scripts/run-tests.sh modules
```

### Setting Up a New Project

```bash
# 1. Create new project
npx create-medusa-app@latest my-store

# 2. Setup database
./scripts/db-setup.sh my-store-db

# 3. Setup testing environment
./scripts/setup-testing.sh

# 4. Start development server
./scripts/dev-server.sh
```

### Deployment Workflow

```bash
# 1. Run tests
./scripts/run-tests.sh all

# 2. Build for production
./scripts/build-production.sh

# 3. In CI/CD pipeline, run predeploy
./scripts/predeploy.sh

# 4. Start production server
./scripts/start-production.sh
```

## Resources

- Official MedusaJS Documentation
- Community Discord and Forums
- GitHub Repository and Examples
- Plugin Marketplace
- Developer Tools and CLI Commands

This skill enables comprehensive MedusaJS development with focus on maintainable, scalable e-commerce solutions.
