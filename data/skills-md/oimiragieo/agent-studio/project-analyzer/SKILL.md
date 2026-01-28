---
name: project-analyzer
description: Automated brownfield codebase analysis. Detects project type, frameworks, dependencies, architecture patterns, and generates comprehensive project profile. Essential for Conductor integration and onboarding existing projects.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep, Bash]
best_practices:
  - Detect project root from package managers and manifest files
  - Identify frameworks from dependencies and directory structure
  - Generate comprehensive file statistics and language breakdown
  - Map component relationships and architecture patterns
  - Validate output against project-analysis.schema.json
  - Execute in < 30 seconds for typical projects (< 10k files)
error_handling: graceful
streaming: supported
executable: .claude/tools/project-analyzer/analyzer.mjs
test_suite: .claude/tools/project-analyzer/tests/analyzer.test.mjs
output_schema: .claude/schemas/project-analysis.schema.json
---

<identity>
Project Analyzer - Automated brownfield codebase analysis for rapid project onboarding and understanding.
</identity>

<capabilities>
- Detecting project type (frontend, backend, fullstack, library, cli, mobile, monorepo)
- Identifying frameworks and libraries from manifests and structure
- Generating file statistics and language breakdown
- Mapping component relationships and module structure
- Detecting architecture patterns (MVC, layered, microservices, etc.)
- Analyzing dependency health and outdated packages
- Identifying code quality indicators (linting, testing, type safety)
- Detecting technical debt and anti-patterns
- Generating prioritized improvement recommendations
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Project Root

Locate project root by finding manifest files:

1. **Search for package manager files**:
   - `package.json` (Node.js/JavaScript/TypeScript)
   - `requirements.txt`, `pyproject.toml`, `setup.py` (Python)
   - `go.mod` (Go)
   - `Cargo.toml` (Rust)
   - `pom.xml`, `build.gradle` (Java/Maven/Gradle)
   - `composer.json` (PHP)

2. **Identify project root**:
   - Directory containing primary package manager file
   - Handle monorepos (multiple package.json files)
   - Detect workspace configuration

3. **Validate project root**:
   - Check for `.git` directory
   - Verify source code directories exist
   - Ensure manifest files are parsable

### Step 2: Detect Project Type

Classify project based on manifest files and directory structure:

1. **Frontend Projects**:
   - Indicators: React, Vue, Angular, Svelte dependencies
   - Directory: `src/components/`, `public/`, `assets/`
   - Frameworks: Next.js, Nuxt.js, Gatsby, Vite

2. **Backend Projects**:
   - Indicators: Express, FastAPI, Django, Flask, Gin dependencies
   - Directory: `routes/`, `controllers/`, `models/`, `api/`
   - Frameworks: Next.js API routes, FastAPI, Express

3. **Fullstack Projects**:
   - Indicators: Both frontend and backend frameworks
   - Directory: Combined frontend + backend structure
   - Frameworks: Next.js, Remix, SvelteKit, Nuxt.js

4. **Library/Package Projects**:
   - Indicators: No application-specific directories
   - Files: `index.ts`, `lib/`, `dist/`, `build/`
   - Manifests: `library` field in package.json

5. **CLI Projects**:
   - Indicators: `bin` field in package.json
   - Files: CLI entry points, command parsers
   - Dependencies: Commander, Yargs, Inquirer

6. **Mobile Projects**:
   - Indicators: React Native, Flutter, Ionic dependencies
   - Files: `android/`, `ios/`, `mobile/`
   - Frameworks: React Native, Expo, Flutter

7. **Monorepo Projects**:
   - Indicators: `workspaces` in package.json, `pnpm-workspace.yaml`
   - Structure: Multiple packages in subdirectories
   - Tools: Turborepo, Nx, Lerna

8. **Microservices Projects**:
   - Indicators: Multiple service directories
   - Files: `docker-compose.yml`, service configs
   - Structure: Service-based organization

### Step 3: Framework Detection

Identify frameworks from manifest files and imports:

1. **Read package.json dependencies** (Node.js):
   - Parse `dependencies` and `devDependencies`
   - Detect framework versions
   - Categorize by type (framework, ui-library, testing, etc.)

2. **Read requirements.txt** (Python):
   - Parse Python dependencies
   - Detect FastAPI, Django, Flask
   - Identify version constraints

3. **Analyze imports** (optional deep scan):
   - Scan source files for import statements
   - Detect used vs declared dependencies
   - Identify framework-specific patterns

4. **Framework Categories**:
   - **Framework**: React, Next.js, FastAPI, Express
   - **UI Library**: Material-UI, Ant Design, Chakra UI
   - **State Management**: Redux, Zustand, Pinia
   - **Testing**: Jest, Vitest, Cypress, Playwright
   - **Build Tool**: Vite, Webpack, Rollup, esbuild
   - **Database**: Prisma, TypeORM, SQLAlchemy
   - **ORM**: Prisma, Sequelize, Mongoose
   - **API**: tRPC, GraphQL, REST
   - **Auth**: NextAuth, Auth0, Clerk
   - **Logging**: Winston, Pino, Bunyan
   - **Monitoring**: Sentry, Datadog, New Relic

5. **Confidence Scoring**:
   - **1.0**: Framework listed in dependencies
   - **0.8**: Framework detected from imports
   - **0.6**: Framework inferred from structure

### Step 4: File Statistics

Generate quantitative project statistics:

1. **Count files by type**:
   - Use glob patterns for common extensions
   - Exclude: `node_modules/`, `.git/`, `dist/`, `build/`
   - Group by language/file type

2. **Count lines of code**:
   - Read source files and count lines
   - Exclude empty lines and comments (optional)
   - Calculate total LOC per language

3. **Identify largest files**:
   - Track file sizes (line count)
   - Report top 10 largest files
   - Flag files > 1000 lines (violates micro-service principle)

4. **Calculate averages**:
   - Average file size (lines)
   - Average directory depth
   - Files per directory

5. **Language Detection**:
   - Map extensions to languages:
     - `.ts`, `.tsx` → TypeScript
     - `.js`, `.jsx` → JavaScript
     - `.py` → Python
     - `.go` → Go
     - `.rs` → Rust
     - `.java` → Java
     - `.md` → Markdown
     - `.json` → JSON
     - `.yaml`, `.yml` → YAML

### Step 5: Structure Analysis

Analyze project structure and architecture:

1. **Identify root directories**:
   - Classify directories by purpose:
     - **source**: `src/`, `app/`, `lib/`
     - **tests**: `test/`, `__tests__/`, `cypress/`
     - **config**: `config/`, `.config/`
     - **docs**: `docs/`, `documentation/`
     - **build**: `dist/`, `build/`, `out/`
     - **scripts**: `scripts/`, `bin/`
     - **assets**: `assets/`, `static/`, `public/`

2. **Detect entry points**:
   - Main entry: `index.ts`, `main.py`, `app.py`
   - App entry: `app.ts`, `server.ts`, `app/page.tsx`
   - Handler: `handler.ts`, `lambda.ts`
   - CLI: `cli.ts`, `bin/`

3. **Detect architecture pattern**:
   - **MVC**: `models/`, `views/`, `controllers/`
   - **Layered**: `presentation/`, `business/`, `data/`
   - **Hexagonal**: `domain/`, `application/`, `infrastructure/`
   - **Microservices**: Multiple service directories
   - **Modular**: Feature-based organization
   - **Flat**: All files in src/

4. **Detect module system**:
   - Check `package.json` for `"type": "module"` (ESM)
   - Scan for `import`/`export` (ESM) vs `require` (CommonJS)
   - Identify mixed module systems

### Step 6: Dependency Analysis

Analyze dependency health:

1. **Count dependencies**:
   - Production dependencies
   - Development dependencies
   - Total dependency count

2. **Check for outdated packages** (optional):
   - Run `npm outdated` or equivalent
   - Parse output for outdated packages
   - Identify major version updates (breaking changes)

3. **Security scan** (optional):
   - Run `npm audit` or equivalent
   - Identify vulnerabilities by severity
   - Flag critical security issues

### Step 7: Code Quality Indicators

Detect code quality tooling:

1. **Linting Configuration**:
   - Detect: `.eslintrc.json`, `eslint.config.js`, `ruff.toml`
   - Tool: ESLint, Ruff, Flake8, Pylint
   - Run linter if configured (optional)

2. **Formatting Configuration**:
   - Detect: `.prettierrc`, `pyproject.toml` (Black/Ruff)
   - Tool: Prettier, Black, Ruff

3. **Testing Framework**:
   - Detect: Jest, Vitest, Pytest, Cypress
   - Count test files
   - Check for coverage configuration

4. **Type Safety**:
   - Detect TypeScript: `tsconfig.json`
   - Check strict mode: `"strict": true`
   - Detect Python typing: mypy, pyright

### Step 8: Pattern Detection

Identify common patterns and anti-patterns:

1. **Good Practices**:
   - Modular component structure
   - Comprehensive test coverage
   - TypeScript strict mode enabled
   - CI/CD configuration present

2. **Anti-Patterns**:
   - Large files (> 1000 lines)
   - Missing tests
   - Outdated dependencies
   - No linting configuration

3. **Neutral Patterns**:
   - Specific architecture choices
   - Framework-specific patterns

### Step 9: Technical Debt Analysis

Calculate technical debt score:

1. **Debt Indicators**:
   - **Outdated Dependencies**: Count outdated packages
   - **Missing Tests**: Low test file ratio
   - **Dead Code**: Unused imports/exports (optional)
   - **Complexity**: Large files, deep nesting
   - **Documentation**: Missing README, docs
   - **Security**: Known vulnerabilities
   - **Performance**: Bundle size, load time

2. **Debt Score** (0-100):
   - 0-20: Excellent health
   - 21-40: Good health, minor issues
   - 41-60: Moderate debt, needs attention
   - 61-80: High debt, refactoring recommended
   - 81-100: Critical debt, major overhaul needed

3. **Remediation Effort**:
   - **Trivial**: < 1 hour
   - **Minor**: 1-4 hours
   - **Moderate**: 1-3 days
   - **Major**: 1-2 weeks
   - **Massive**: > 2 weeks

### Step 10: Generate Recommendations

Create prioritized improvement recommendations:

1. **Categorize Recommendations**:
   - **Security**: Critical vulnerabilities, outdated auth
   - **Performance**: Bundle optimization, lazy loading
   - **Maintainability**: Refactor large files, add tests
   - **Testing**: Increase coverage, add E2E tests
   - **Documentation**: Add README, API docs
   - **Architecture**: Improve modularity, separation of concerns
   - **Dependencies**: Update packages, remove unused

2. **Prioritize by Impact**:
   - **P0**: Critical security, blocking production
   - **P1**: High impact, affects reliability
   - **P2**: Medium impact, improves quality
   - **P3**: Low impact, nice-to-have

3. **Estimate Effort and Impact**:
   - Effort: trivial, minor, moderate, major, massive
   - Impact: low, medium, high, critical

### Step 11: Validate Output

Validate analysis output against schema:

1. **Schema Validation**:
   - Validate against `project-analysis.schema.json`
   - Ensure all required fields present
   - Check data types and formats

2. **Output Metadata**:
   - Analyzer version
   - Analysis duration (ms)
   - Files analyzed count
   - Files skipped count
   - Errors encountered

</execution_process>

<performance>
**Performance Requirements**:

- **Target**: < 30 seconds for typical projects (< 10k files)
- **Optimization**:
  - Skip large directories: `node_modules/`, `.git/`, `dist/`
  - Use parallel file processing
  - Cache results for incremental analysis
  - Limit deep scans to essential files
  - Use streaming for large file counts
    </performance>

<integration>
**Integration with Conductor**:
- Provides automated project discovery
- Eliminates manual context gathering
- Enables 80% faster brownfield onboarding
- Feeds project context to chat interface

**Integration with Other Skills**:

- **rule-selector**: Auto-select rules based on detected frameworks
- **repo-rag**: Semantic search for architectural patterns
- **dependency-analyzer**: Deep dependency analysis
  </integration>

<best_practices>

1. **Progressive Disclosure**: Start with manifest analysis, add deep scans if needed
2. **Performance First**: Skip expensive operations for large projects
3. **Fail Gracefully**: Handle missing files, parse errors
4. **Validate Output**: Always validate against schema
5. **Cache Results**: Store analysis output for reuse
6. **Incremental Updates**: Re-analyze only changed files
   </best_practices>
   </instructions>

<examples>
<usage_example>
**Programmatic Usage**:

```bash
# Analyze current project
node .claude/tools/project-analyzer/analyzer.mjs

# Analyze specific directory
node .claude/tools/project-analyzer/analyzer.mjs /path/to/project

# Output to file
node .claude/tools/project-analyzer/analyzer.mjs --output .claude/context/artifacts/project-analysis.json

# Run tests
node .claude/tools/project-analyzer/tests/analyzer.test.mjs
```

**Agent Invocation**:

```
# Analyze current project
Analyze this project

# Generate comprehensive analysis
Perform full project analysis and save to artifacts

# Quick analysis (manifest only)
Quick project type detection
```

</usage_example>

<formatting_example>
**Sample Output** (`.claude/context/artifacts/project-analysis.json`):

```json
{
  "analysis_id": "analysis-llm-rules-20250115",
  "project_type": "fullstack",
  "analyzed_at": "2025-01-15T10:30:00.000Z",
  "project_root": "C:\\dev\\projects\\LLM-RULES",
  "stats": {
    "total_files": 1243,
    "total_lines": 125430,
    "languages": {
      "JavaScript": 45230,
      "TypeScript": 38120,
      "Markdown": 25680,
      "JSON": 12400,
      "YAML": 4000
    },
    "file_types": {
      ".js": 234,
      ".mjs": 156,
      ".ts": 89,
      ".md": 312,
      ".json": 145
    },
    "directories": 87,
    "avg_file_size_lines": 101,
    "largest_files": [
      {
        "path": ".claude/tools/enforcement-gate.mjs",
        "lines": 1520
      }
    ]
  },
  "frameworks": [
    {
      "name": "nextjs",
      "version": "14.0.0",
      "category": "framework",
      "confidence": 1.0,
      "source": "package.json"
    },
    {
      "name": "react",
      "version": "18.2.0",
      "category": "framework",
      "confidence": 1.0,
      "source": "package.json"
    }
  ],
  "structure": {
    "root_directories": [
      {
        "name": ".claude",
        "purpose": "config",
        "file_count": 543
      },
      {
        "name": "conductor-main",
        "purpose": "source",
        "file_count": 234
      }
    ],
    "entry_points": [
      {
        "path": "conductor-main/src/index.ts",
        "type": "main"
      }
    ],
    "architecture_pattern": "modular",
    "module_system": "esm"
  },
  "dependencies": {
    "production": 45,
    "development": 23
  },
  "code_quality": {
    "linting": {
      "configured": true,
      "tool": "eslint"
    },
    "formatting": {
      "configured": true,
      "tool": "prettier"
    },
    "testing": {
      "framework": "vitest",
      "test_files": 89,
      "coverage_configured": true
    },
    "type_safety": {
      "typescript": true,
      "strict_mode": true
    }
  },
  "tech_debt": {
    "score": 35,
    "indicators": [
      {
        "category": "complexity",
        "severity": "medium",
        "description": "3 files exceed 1000 lines",
        "remediation_effort": "moderate"
      }
    ]
  },
  "recommendations": [
    {
      "priority": "P1",
      "category": "maintainability",
      "title": "Refactor large files",
      "description": "Break down files > 1000 lines into smaller modules",
      "effort": "moderate",
      "impact": "high"
    }
  ],
  "metadata": {
    "analyzer_version": "1.0.0",
    "analysis_duration_ms": 2340,
    "files_analyzed": 1243,
    "files_skipped": 3420,
    "errors": []
  }
}
```

</formatting_example>
</examples>

## References

For additional detection patterns extracted from the Auto-Claude analysis framework, see:

- `references/auto-claude-patterns.md` - Monorepo indicators, SERVICE_INDICATORS, SERVICE_ROOT_FILES, infrastructure detection, convention detection
- `references/service-patterns.md` - Service type detection (frontend, backend, library), framework-specific patterns, entry point detection
- `references/database-patterns.md` - Database configuration file patterns, ORM detection (Prisma, SQLAlchemy, TypeORM, Drizzle, Mongoose), connection string patterns
- `references/route-patterns.md` - Express, FastAPI, Flask, Django, Next.js, Go, Rust API route detection patterns

These references provide comprehensive regex patterns and detection logic for brownfield codebase analysis.

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
