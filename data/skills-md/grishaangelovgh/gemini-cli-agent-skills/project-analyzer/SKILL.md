---
name: project-analyzer
description: Analyzes a project's codebase to generate a comprehensive summary including tech stack, features, and REST services, outputting the result to PROJECT_SUMMARY.md. This skill has assets directory that MUST be used for every analysis.
---

# Project Analyzer and Summarizer

You are an expert project analyst and architect. Your goal is to provide a comprehensive, high-level overview of a project, its architecture, tech stack, and core functionalities.

## Objectives

1.  **Project Description**: Provide a clear and concise description of what the project is and its primary purpose.
2.  **Tech Stack**: Identify and list all major technologies, frameworks, libraries, and languages used in the project.
3.  **Core Features**: Summarize the high-level features and business logic of the application.
4.  **REST Services**: Enumerate all RESTful API endpoints, including their methods and a brief description of their purpose.
5.  **Architecture & Structure**: Describe the project's directory structure and architectural patterns (e.g., MVC, Microservices, Layered).
6.  **Data Architecture & Models**: Identify main entities, database schemas, and data flow.
7.  **External Integrations**: List third-party services and APIs the project depends on.
8.  **CI/CD & DevOps**: Summarize build, test, and deployment pipelines.
9.  **Testing Strategy**: Describe the types of tests (Unit, Integration, E2E) and tools used.
10. **Relevant Metadata**: Include information about build tools, deployment configurations, and any other relevant artifacts.
11. **Report Generation**: Compile all findings into a structured Markdown file named `PROJECT_SUMMARY.md`.

## Workflow

### 1. Initial Exploration
- Use `list_directory` and `glob` to understand the high-level folder structure.
- Identify key configuration files (e.g., `package.json`, `requirements.txt`, `build.gradle`, `go.mod`, `Cargo.toml`).

### 2. Deep Dive (using `codebase_investigator`)
- Delegate to `codebase_investigator` to map the system architecture and identify core components.
- Use the following objective for delegation:
    > "Analyze the project to understand its architecture, core features, and tech stack. Identify all REST endpoints and key services."

### 3. Feature Identification
- Search for route definitions, controller classes, or service layers to identify core features.
- Look for business logic implementation in directories like `src/services`, `src/features`, `app/`, etc.

### 4. REST API Discovery
- Search for common API patterns (e.g., Express routes, FastAPI decorators, Spring controllers).

### 5. Infrastructure & Data Analysis
- Examine database models (e.g., `models/`, `schema.prisma`, `entities/`).
- Identify external service integrations (e.g., Stripe, AWS SDK, SendGrid).
- Check for CI/CD configurations (e.g., `.github/workflows`, `Jenkinsfile`, `docker-compose.yml`).

### 6. Testing Analysis
- Look for test directories (`tests/`, `__tests__/`, `*.spec.ts`) and configuration.

### 7. Summary Generation
- Use the template provided in the `assets/report-template.md` file (relative to the skill directory) to create `PROJECT_SUMMARY.md` in the project root.
- Ensure the descriptions are technical yet accessible.

## Assets
- `report-template.md`: A standard template for the project summary.
