---
name: sc
description: Unified SuperClaude workflow skill with subcommands for analysis, building, documentation, git, implementation, and more. Use for any structured development workflow.
---

# SuperClaude Unified Workflow

Comprehensive workflow system with 17 subcommands for structured development tasks.

## Usage

```
/sc [command] [target] [options]
```

## Commands

| Command        | Purpose                                      | Key Options                                                                     |
| -------------- | -------------------------------------------- | ------------------------------------------------------------------------------- |
| `analyze`      | Code quality, security, performance analysis | `--focus quality\|security\|performance\|architecture`, `--depth quick\|deep`   |
| `build`        | Build, compile, package projects             | `--type dev\|prod\|test`, `--clean`, `--optimize`                               |
| `cleanup`      | Remove dead code, optimize structure         | `--type code\|imports\|files\|all`, `--safe\|--aggressive`, `--dry-run`         |
| `design`       | System architecture, API design              | `--type system\|api\|component`, `--document`                                   |
| `document`     | Create documentation for components          | `--type inline\|external\|api\|guide`, `--style brief\|detailed`                |
| `estimate`     | Time/effort/complexity estimates             | `--format brief\|detailed`, `--include-risks`                                   |
| `explain`      | Explain code, concepts, behavior             | `--depth overview\|detailed\|deep`, `--audience beginner\|intermediate\|expert` |
| `git`          | Git operations with smart commits            | `--smart-commit`, `--branch-strategy`                                           |
| `implement`    | Feature and code implementation              | `--type component\|api\|service\|feature`, `--with-tests`, `--safe`             |
| `improve`      | Quality, performance improvements            | `--focus quality\|performance\|security`, `--scope file\|module\|project`       |
| `index`        | Project documentation and knowledge base     | `--type readme\|api\|structure`, `--format markdown\|json`                      |
| `load`         | Load and analyze project context             | `--scope files\|dependencies\|config\|all`                                      |
| `spawn`        | Break tasks into coordinated subtasks        | `--sequential\|--parallel`, `--validate`                                        |
| `task`         | Workflow management with persistence         | `--strategy systematic\|agile\|enterprise`, `--persist`, `--hierarchy`          |
| `test`         | Execute tests, generate reports              | `--type unit\|integration\|e2e\|all`, `--coverage`, `--watch`                   |
| `troubleshoot` | Diagnose and resolve issues                  | `--type bug\|build\|performance\|deployment`, `--trace`, `--fix`                |
| `workflow`     | Generate implementation workflows            | `--strategy systematic\|agile\|mvp`, `--output roadmap\|tasks\|detailed`        |

---

## analyze

Analyze code quality, security, performance, and architecture.

### When to use

- Code quality or technical debt analysis
- Security audit or vulnerability assessment
- Performance bottleneck identification
- Architecture review

### Usage

```
/sc analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep]
```

### Execution

1. Discover and categorize files
2. Apply analysis tools and techniques
3. Generate findings with severity ratings
4. Create actionable recommendations

---

## build

Build, compile, and package projects.

### When to use

- Build or compile a project
- Diagnose build errors
- Production optimization

### Usage

```
/sc build [target] [--type dev|prod|test] [--clean] [--optimize]
```

### Execution

1. Analyze project structure and build config
2. Validate dependencies
3. Execute build with error monitoring
4. Optimize output and report results

---

## cleanup

Clean up code, remove dead code, optimize structure.

### When to use

- Remove dead code or unused imports
- Optimize project structure
- Technical debt cleanup

### Usage

```
/sc cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--dry-run]
```

### Execution

1. Analyze for cleanup opportunities
2. Identify dead code, unused imports
3. Create cleanup plan with risk assessment
4. Execute with safety measures
5. Validate and report results

---

## design

Design system architecture, APIs, and component interfaces.

### When to use

- System or component architecture
- API design
- Interface planning

### Usage

```
/sc design [target] [--type system|api|component] [--document]
```

### Execution

1. Analyze requirements and constraints
2. Research patterns and best practices
3. Create architecture proposal
4. Document design decisions

---

## document

Create focused documentation for components or features.

### When to use

- Code documentation
- API documentation
- User guides

### Usage

```
/sc document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

### Execution

1. Analyze target component
2. Identify documentation requirements
3. Generate documentation
4. Apply consistent formatting

---

## estimate

Provide development estimates for tasks.

### When to use

- Time estimates needed
- Effort assessment
- Project sizing

### Usage

```
/sc estimate [task] [--format brief|detailed] [--include-risks]
```

### Execution

1. Analyze task complexity
2. Identify dependencies and risks
3. Generate estimate with confidence levels
4. Document assumptions

---

## explain

Provide clear explanations of code, concepts, or behavior.

### When to use

- Code explanation needed
- Concept clarification
- Behavior understanding

### Usage

```
/sc explain [target] [--depth overview|detailed|deep] [--audience beginner|intermediate|expert]
```

### Execution

1. Analyze target code/concept
2. Identify key components
3. Generate explanation at appropriate level
4. Include examples if helpful

---

## git

Git operations with intelligent commit messages.

### When to use

- Commit with good messages
- Branch management
- Merge/rebase assistance

### Usage

```
/sc git [operation] [--smart-commit] [--branch-strategy]
```

### Execution

1. Analyze current Git state
2. Execute requested operations
3. Generate intelligent commit messages
4. Handle conflicts and provide feedback

---

## implement

Feature and code implementation.

### When to use

- Implement features or components
- New functionality
- API or service implementation

### Usage

```
/sc implement [feature] [--type component|api|service|feature] [--with-tests] [--safe]
```

### Execution

1. Analyze requirements and detect context
2. Auto-activate relevant personas
3. Generate implementation with best practices
4. Apply security and quality validation
5. Provide testing recommendations

---

## improve

Apply systematic improvements to code.

### When to use

- Refactoring code
- Cleaning up technical debt
- Optimizing performance

### Usage

```
/sc improve [target] [--focus quality|performance|security] [--scope file|module|project]
```

### Execution

1. Analyze current state
2. Identify improvement opportunities
3. Prioritize changes by impact
4. Apply improvements systematically
5. Validate results

---

## index

Generate project documentation and knowledge base.

### When to use

- Create docs or README
- API documentation
- Project structure maps

### Usage

```
/sc index [target] [--type readme|api|structure] [--format markdown|json]
```

### Execution

1. Scan project structure
2. Extract key information
3. Generate documentation
4. Organize knowledge base

---

## load

Load and analyze project context.

### When to use

- Starting work on a project
- Understanding configurations
- Analyzing dependencies

### Usage

```
/sc load [target] [--scope files|dependencies|config|all]
```

### Execution

1. Identify project structure
2. Load configurations
3. Analyze dependencies
4. Build context summary

---

## spawn

Break complex tasks into coordinated subtasks.

### When to use

- Complex multi-step tasks
- Parallel work orchestration
- Dependency management

### Usage

```
/sc spawn [task] [--sequential|--parallel] [--validate]
```

### Execution

1. Parse request and create task breakdown
2. Map dependencies
3. Choose execution strategy
4. Execute with progress monitoring
5. Integrate and validate results

---

## task

Execute tasks with workflow management and persistence.

### When to use

- Large project management
- Cross-session progress tracking
- Multi-phase operations

### Usage

```
/sc task [action] [target] [--strategy systematic|agile|enterprise] [--persist] [--hierarchy]
```

### Actions

- `create` - Create task hierarchy
- `execute` - Execute with orchestration
- `status` - View task status
- `analytics` - Performance dashboard
- `delegate` - Multi-agent delegation

### Strategies

- **systematic**: Discovery → Planning → Execution → Validation → Optimization
- **agile**: Sprint Planning → Iterative Execution → Adaptive Planning
- **enterprise**: Stakeholder Analysis → Resource Allocation → Risk Management

---

## test

Execute tests and generate reports.

### When to use

- Run tests
- Check coverage
- Set up test infrastructure

### Usage

```
/sc test [target] [--type unit|integration|e2e|all] [--coverage] [--watch]
```

### Execution

1. Detect test framework
2. Execute appropriate tests
3. Collect coverage data
4. Generate report with recommendations

---

## troubleshoot

Diagnose and resolve issues.

### When to use

- Debugging errors
- Build failures
- Performance issues
- Deployment problems

### Usage

```
/sc troubleshoot [issue] [--type bug|build|performance|deployment] [--trace] [--fix]
```

### Execution

1. Analyze issue description
2. Identify potential root causes
3. Execute systematic debugging
4. Propose and validate solutions
5. Apply fixes and verify

---

## workflow

Generate structured implementation workflows from PRDs.

### When to use

- Planning feature implementation
- Creating development roadmaps
- Breaking down complex features
- Sprint planning

### Usage

```
/sc workflow [prd|description] [--strategy systematic|agile|mvp] [--output roadmap|tasks|detailed]
```

### Strategies

- **systematic**: Full analysis, architecture, dependencies, testing
- **agile**: Epics, sprints, MVP, iterative delivery
- **mvp**: Core features, rapid prototyping, validation

### Output Formats

- **roadmap**: Phase-based timeline with milestones
- **tasks**: Epic/Story/Task hierarchy
- **detailed**: Step-by-step with estimates and criteria

---

## Global Options

| Option         | Effect                                      |
| -------------- | ------------------------------------------- |
| `--think`      | Enable extended analysis (4K tokens)        |
| `--think-hard` | Deep analysis mode (10K tokens)             |
| `--c7`         | Enable Context7 for framework patterns      |
| `--seq`        | Enable Sequential thinking                  |
| `--safe`       | Conservative approach with extra validation |
| `--verbose`    | Detailed output                             |

## Claude Code Integration

- **Glob/Grep/Read**: File discovery and analysis
- **Edit/Write**: Code generation and modification
- **Bash**: Build and test execution
- **Task tool**: Complex multi-step orchestration
- **TodoWrite**: Progress tracking

## Examples

```
/sc analyze src/ --focus security --depth deep
/sc build --type prod --clean --optimize
/sc cleanup --type imports --dry-run
/sc implement user-auth --type feature --with-tests
/sc workflow docs/prd.md --strategy agile --output tasks
/sc troubleshoot "build failing" --type build --trace
```
