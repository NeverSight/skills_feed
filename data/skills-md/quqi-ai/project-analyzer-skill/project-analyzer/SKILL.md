---
name: project-analyzer
description: Analyzes Java project structure and generates comprehensive documentation including tech stack, architecture, modules, configuration, internal SDKs, and development guidelines. Use this skill when you need to understand a Java/Spring Boot codebase, onboard new developers, generate project documentation, or provide context for AI-assisted development. Triggers include "analyze project structure", "generate project documentation", "what is the project architecture", or when starting work on an unfamiliar codebase.
---

# Project Analyzer

Analyzes Java project structure and generates comprehensive documentation to help developers and AI agents understand the codebase.

## Core Principles

- **Read-only**: Only analyze code, never modify it
- **Evidence-based**: All conclusions must be based on observable code or configuration
- **No speculation**: If information isn't available in the codebase, state it explicitly
- **No side effects**: Do not execute builds, call networks, or run tests

## Analysis Workflow

### 1. Initial Discovery

Start by identifying the project type and structure:

1. **Check for multi-module structure**: Look for parent `pom.xml` with `<modules>` section
2. **Identify project root**: Find the main application entry point (`@SpringBootApplication`)
3. **Check build files**: Examine `pom.xml` or `build.gradle` for dependencies

### 2. Technology Stack Analysis

Analyze dependencies and configurations to identify:

**Frameworks:**
- Spring Boot version (check `pom.xml` for `spring-boot-starter-parent`)
- Spring Cloud components (Gateway, Feign, Config, etc.)
- Persistence frameworks (MyBatis, JPA, MyBatis-Plus)
- Web frameworks (Spring MVC, WebFlux)

**Middleware & Infrastructure:**
- Message queues (check for RabbitMQ, Kafka, RocketMQ dependencies)
- Caching (Redis, Caffeine, Ehcache)
- Service discovery (Nacos, Eureka, Consul)
- Databases (check `application.yml` for datasource configurations)

**Development Tools:**
- Lombok, MapStruct, Swagger/OpenAPI
- Testing frameworks (JUnit, Mockito, TestContainers)

**Search patterns:**
```bash
# Find Spring Boot version
grep -r "spring-boot-starter-parent" --include="pom.xml"

# Find middleware dependencies
grep -r "spring-boot-starter-data-redis\|rabbitmq\|kafka\|nacos" --include="pom.xml"

# Find database configurations
grep -r "url:\|driver-class-name:" --include="*.yml" --include="*.yaml" --include="*.properties"
```

### 3. Project Structure Analysis

Map out the module and package organization:

**For multi-module projects:**
1. Read parent `pom.xml` to list all modules
2. For each module, identify its purpose from naming and dependencies
3. Common module patterns:
   - `*-api`: API definitions, DTOs, interfaces
   - `*-service`: Business logic implementation
   - `*-web`: Web controllers, REST APIs
   - `*-dao` / `*-mapper`: Data access layer
   - `*-common`: Shared utilities, constants
   - `*-model` / `*-entity`: Domain models

**Package structure analysis:**
```bash
# Find main package structure
find . -type d -name "java" -o -name "com" -o -name "cn" | head -20

# Identify common layers
find . -name "controller" -o -name "service" -o -name "dao" -o -name "mapper" -o -name "config"
```

### 4. Key Components Discovery

Identify critical components in order of importance:

**Application Entry Points:**
- Classes annotated with `@SpringBootApplication`
- Main methods

**Configuration Classes:**
- Classes with `@Configuration`
- Files in `config/` packages
- `application.yml`, `application.properties`, `bootstrap.yml`

**Core Business Modules:**
- Service interfaces and implementations
- Domain models and entities
- Key controllers for main features

**Infrastructure Components:**
- Database mappers/repositories
- Message queue consumers/producers
- Scheduled tasks (`@Scheduled`)
- Filters, interceptors, aspect classes

**Search patterns:**
```bash
# Find application entry points
grep -r "@SpringBootApplication" --include="*.java"

# Find configuration classes
grep -r "@Configuration" --include="*.java"

# Find scheduled tasks
grep -r "@Scheduled" --include="*.java"

# Find MQ consumers
grep -r "@RabbitListener\|@KafkaListener" --include="*.java"
```

### 5. Configuration Analysis

Document all configuration sources:

**Spring configuration files:**
- `application.yml` / `application.properties` (default profile)
- `application-{profile}.yml` (environment-specific)
- `bootstrap.yml` (for Spring Cloud Config)

**External configuration:**
- Check for Nacos configuration references
- Environment variables (look for `${ENV_VAR}` patterns)
- System properties

**Configuration hierarchy:**
1. List all configuration files found
2. Identify active profiles from config or startup parameters
3. Document key configurations: datasource, Redis, MQ, Nacos, ports

### 6. Internal SDK & Dependencies

Identify internal/custom libraries:

**Search for internal artifacts:**
```bash
# Find internal dependencies (usually from company groupId)
grep -r "<groupId>com\.company\|<groupId>cn\.company" --include="pom.xml"

# Find local JAR references
grep -r "systemPath\|scope>system" --include="pom.xml"

# Check lib directories
find . -type d -name "lib" -o -name "libs"
```

**Document for each internal SDK:**
- Artifact name and version
- Purpose (infer from naming and usage in code)
- Key classes/interfaces it provides
- Where it's used in the project

**Search for usage:**
```bash
# Find imports from internal packages
grep -r "import com\.company" --include="*.java" | cut -d: -f2 | sort | uniq
```

### 7. Development Guidelines Extraction

Extract rules and patterns from the codebase:

**Architectural patterns:**
- Observe consistent patterns (e.g., "All services implement interfaces")
- Layer separation rules (e.g., "Controllers only call services, never DAOs")
- Naming conventions

**Common utilities:**
- Response wrapper classes
- Exception handling patterns
- Validation patterns

**Infer restrictions:**
- If all external API calls go through a specific client class → "All external calls must use XxxClient"
- If all database operations use MyBatis → "Direct JDBC is not used"
- If all AI calls use a specific interface → "All AI calls must go through AiClient"

**Local development requirements:**
- Check `README.md` or `docs/` for setup instructions
- Identify required services from configuration (Redis, Nacos, MySQL, etc.)
- Look for Docker Compose files

**Search patterns:**
```bash
# Find README files
find . -name "README*" -o -name "readme*"

# Find Docker Compose
find . -name "docker-compose*.yml"

# Find documentation
find . -type d -name "doc" -o -name "docs"
```

## Output Format

Generate a Markdown document with the following structure:

```markdown
# {Project Name} - Project Structure Documentation

> Generated on {date} | Analysis Type: Static Code Analysis

## 📋 Project Overview

- **Project Name**: {name}
- **Type**: {Single Module / Multi-Module}
- **Primary Language**: Java {version}
- **Build Tool**: Maven / Gradle
- **Main Framework**: Spring Boot {version}

## 🛠️ Technology Stack

### Core Frameworks
- Spring Boot {version}
- Spring Cloud {components if present}
- {Other frameworks}

### Middleware & Infrastructure
- **Service Discovery**: {Nacos / Eureka / None}
- **Configuration Center**: {Nacos / Config Server / None}
- **Cache**: {Redis / Caffeine / None}
- **Message Queue**: {RabbitMQ / Kafka / None}
- **Database**: {MySQL / PostgreSQL / etc.}

### Development Tools
- {Lombok, MapStruct, Swagger, etc.}

## 🏗️ Project Architecture

### Module Structure
{For multi-module projects, list modules}

```
project-root/
├── module-api/          - {Purpose}
├── module-service/      - {Purpose}
├── module-web/          - {Purpose}
└── module-common/       - {Purpose}
```

### Package Structure
{Describe package organization}

```
com.company.project/
├── controller/          - REST API endpoints
├── service/             - Business logic
│   ├── impl/
│   └── {domain}/
├── dao/mapper/          - Data access
├── model/entity/        - Domain models
├── config/              - Configuration classes
└── util/                - Utility classes
```

### Layered Architecture

```
┌─────────────────────────────────┐
│   Controller Layer              │  ← HTTP requests
├─────────────────────────────────┤
│   Service Layer                 │  ← Business logic
├─────────────────────────────────┤
│   DAO/Mapper Layer              │  ← Data access
├─────────────────────────────────┤
│   Infrastructure Layer          │  ← Redis, MQ, External APIs
└─────────────────────────────────┘
```

## 🔑 Key Components

### Application Entry Point
- `{path/to/Application.java}` - Main application class

### Core Business Modules
- **{Feature 1}**: {path} - {Description}
- **{Feature 2}**: {path} - {Description}

### Configuration Files
- `{path/to/application.yml}` - Main configuration
- `{path/to/application-dev.yml}` - Dev environment
- `{path/to/application-prod.yml}` - Production environment

### Infrastructure Components
- **Database Mappers**: `{path}` - {Count} mapper interfaces
- **Scheduled Tasks**: `{path}` - {Description}
- **Message Consumers**: `{path}` - {Description}

## 📦 Internal SDKs & Dependencies

### Internal Dependencies
1. **{artifact-name}** (`{groupId}:{artifactId}:{version}`)
   - **Purpose**: {Inferred purpose}
   - **Key Classes**: {List main classes/interfaces}
   - **Used In**: {Where it's imported}

2. **{another-sdk}**
   - ...

### External Key Dependencies
- {List critical 3rd party libraries}

## ⚙️ Configuration & Environment

### Configuration Sources
1. **Spring Configuration**: `application.yml`, `application-{profile}.yml`
2. **Nacos Configuration**: {If applicable}
   - Namespace: {value}
   - Group: {value}
   - DataId: {value}
3. **Environment Variables**: {List if found}

### Key Configurations
- **Server Port**: {port}
- **Database**: {connection details location}
- **Redis**: {configuration location}
- **Nacos**: {server address}

## 📐 Development Guidelines

### Architectural Rules
{Rules observed from code patterns}

- **Layer Separation**: Controllers must not directly access DAO layer
- **Service Interfaces**: All services implement interfaces in {package}
- **{Other patterns}**

### Conventions
- **Naming**: {Observed naming patterns}
- **Response Format**: All APIs return `Result<T>` wrapper (see `{path}`)
- **Exception Handling**: Unified exception handler at `{path}`

### Recommended Extension Points
- **Add New Feature**: Create service in `{package}`, controller in `{package}`
- **Add New Entity**: Place in `{package}`, create mapper in `{package}`
- **Add Configuration**: Add to `{config class}` or `application.yml`

### Prohibited Practices
{Inferred from codebase patterns}

- Do not bypass {XxxClient} for {external service} calls
- Do not use direct JDBC; use {MyBatis/JPA}
- Do not put business logic in Controller layer

### Local Development Requirements

**Required Services:**
- {Service 1} (e.g., MySQL 5.7+)
- {Service 2} (e.g., Redis 6.0+)
- {Service 3} (e.g., Nacos 2.0+)

**Setup Steps:**
{If found in README or docs}

**Startup Order:**
1. {Step 1}
2. {Step 2}

## 📚 Additional Resources

- **Documentation**: `{path to docs folder}`
- **API Documentation**: {Swagger URL if configured}
- **README**: `{path to README}`

---

*Note: This documentation was generated through static code analysis. For runtime behavior or deployment specifics, consult the team or deployment documentation.*
```

## Tips for Effective Analysis

1. **Start broad, then deep**: Begin with project structure, then drill into specific areas
2. **Use parallel searches**: Run multiple grep/find commands together when possible
3. **Verify with multiple sources**: Cross-reference pom.xml with actual code usage
4. **Be explicit about gaps**: If you can't find something, say "Not found in codebase" rather than guessing
5. **Focus on patterns**: Look for repeated patterns to infer architectural rules
6. **Respect scope**: Analyze only what's in the project; don't make assumptions about external systems

## When to Use This Skill

Trigger this skill when:
- User asks to "analyze project structure" or "generate project documentation"
- Starting work on an unfamiliar codebase
- Onboarding new team members or AI agents
- User asks "what is the architecture" or "how is this project organized"
- User needs context about internal SDKs or development guidelines
- User asks about tech stack, dependencies, or configuration

## What NOT to Do

- ❌ Do not run builds (`mvn clean install`, `gradle build`)
- ❌ Do not execute tests
- ❌ Do not make network calls or query external services
- ❌ Do not modify any code or configuration files
- ❌ Do not speculate about things not visible in code
- ❌ Do not assume technologies based on company conventions; only state what's observable
