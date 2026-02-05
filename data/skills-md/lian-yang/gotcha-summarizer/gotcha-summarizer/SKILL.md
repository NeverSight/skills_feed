---
name: gotcha-summarizer
description: "Automatically summarizes technical lessons learned from conversations into docs/gotchas/. Supports 18+ programming languages with confidence scoring. Use at the end of conversations to capture: (1) Frontend/Backend bugs and root causes, (2) Framework issues (React/Vue/Next.js/Nuxt/Databases/APIs), (3) Code quality improvements (precision, caching, concurrency, etc.), (4) Performance optimization insights, (5) Testing/CI/CD/Git issues, (6) Any technical lessons worth documenting. Features: three-layer classification (Domain → Category → File), fuzzy duplicate detection, i18n support (zh/en), multi-code block grouping, error tracking statistics."
---

# Gotcha Summarizer

Automatically extracts and documents technical lessons learned from conversations into the project's `docs/gotchas/` directory.

## Features

- **Structured Extraction**: Extracts problems, causes, solutions, best practices from conversations
- **18+ Language Detection**: Automatic code language detection (JSX/TSX, SQL, Vue, Bash, PowerShell, PHP, Ruby, Swift, Kotlin, C#, Dart, Rust, Go, Python, TypeScript, Java, JavaScript, C, C++)
- **Multi-Code Block Support**: Groups and displays code blocks by programming language
- **Confidence Scoring**: Returns classification confidence scores for domain and category
- **Fuzzy Duplicate Detection**: Detects similar entries using SequenceMatcher (threshold: 0.75)
- **Internationalization**: Chinese/English interface with `LOCALE` environment variable
- **Error Tracking**: Tracks JSON parse errors, file I/O errors, classification errors with statistics

## Purpose

This skill analyzes conversation history to identify and document:

**Frontend Development:**
- Frontend bugs and root causes (hydration errors, memory leaks, rendering issues)
- Framework issues (React, Vue, Next.js, Nuxt, Svelte, Angular)
- Styling problems (CSS, SCSS, Tailwind, UnoCSS)
- Build tool issues (Vite, Webpack, Rollup, esbuild)
- State management (Redux, Pinia, Zustand, Jotai, Vuex)
- UI component library issues (Ant Design, Element Plus, shadcn/ui, Material-UI)

**Backend Development:**
- Backend bugs and root causes (nil pointer, race conditions, database errors)
- Database/ORM issues (SQL, migrations, Bun, GORM, Ent, sqlx)
- API issues (REST, GraphQL, gRPC, endpoints, controllers)
- Concurrency issues (goroutines, mutexes, channels, context, race conditions)
- Performance issues (caching, Redis, slow queries, indexing, n+1 problems)
- Precision issues (decimal vs float, money/amount handling)

**Common Development:**
- Testing problems and solutions (unit tests, integration tests, mocks, TDD)
- CI/CD pipeline issues (GitHub Actions, Docker, deployment, Kubernetes)
- Git/version control problems (merge conflicts, rebasing, branches)
- Code quality improvements (refactoring, design patterns, linting)
- Any technical lessons worth documenting

## Usage

Run this skill at the end of a conversation to capture lessons learned:

```bash
skill gotcha-summarizer
```

The skill will:
1. Analyze the conversation for technical issues
2. Use a decision tree to categorize the topic
3. Extract key information (error messages, root causes, solutions)
4. Check existing docs for duplicates
5. Update the appropriate markdown file

## Decision Tree

```
START: Analyze conversation for technical issues
│
├─ LAYER 1: Domain Classification (Common / Frontend / Backend)
│   │
│   ├─ COMMON BRANCH → LAYER 2
│   │   ├─ Testing → common/testing.md
│   │   ├─ CI/CD → common/cicd.md
│   │   ├─ Git → common/git.md
│   │   └─ Code Quality → common/code-quality.md
│   │
│   ├─ FRONTEND BRANCH → LAYER 2
│   │   ├─ Bug Issues → frontend/bugs.md
│   │   ├─ Framework → frontend/frameworks.md
│   │   ├─ Styling → frontend/styling.md
│   │   ├─ Build Tools → frontend/build-tools.md
│   │   ├─ State Management → frontend/state-mgmt.md
│   │   └─ UI Components → frontend/ui-components.md
│   │
│   └─ BACKEND BRANCH → LAYER 2
│       ├─ Bug Issues → backend/bugs.md
│       ├─ Database → backend/database.md
│       ├─ API → backend/api.md
│       ├─ Concurrency → backend/concurrency.md
│       ├─ Performance → backend/performance.md
│       └─ Precision → backend/precision.md
│
└─ LAYER 3: File Mapping (Category → markdown file)
```

### Classification Priority

The three-layer decision tree checks categories in this priority order:

**Layer 1: Domain** (Common > Frontend > Backend)
- Common domains (Testing, CI/CD, Git) are checked first as they apply to all development

**Layer 2: Category** (within each domain)
- **Bugs** always have highest priority within each domain
- Other categories follow domain-specific priority

**Frontend Priority:** Bugs > Frameworks > State Mgmt > Styling > Build Tools > UI Components
**Backend Priority:** Bugs > Database > API > Concurrency > Performance > Precision
**Common Priority:** Testing > CI/CD > Git > Code Quality

## Supported Categories

| Domain | Category | File | Examples |
|--------|----------|------|----------|
| **Frontend** | Bugs | `frontend/bugs.md` | Hydration errors, memory leaks, re-render issues |
| | Frameworks | `frontend/frameworks.md` | React, Vue, Next.js, Nuxt, Svelte, Angular |
| | Styling | `frontend/styling.md` | CSS, SCSS, Tailwind, UnoCSS, styled-components |
| | Build Tools | `frontend/build-tools.md` | Vite, Webpack, Rollup, esbuild, HMR |
| | State Mgmt | `frontend/state-mgmt.md` | Redux, Pinia, Zustand, Jotai, Vuex |
| | UI Components | `frontend/ui-components.md` | Ant Design, Element Plus, shadcn/ui, MUI |
| **Backend** | Bugs | `backend/bugs.md` | Nil pointer, race conditions, SQL errors |
| | Database | `backend/database.md` | SQL, ORM (Bun, GORM, Ent), migrations |
| | API | `backend/api.md` | REST, GraphQL, gRPC, endpoints, controllers |
| | Concurrency | `backend/concurrency.md` | Goroutines, mutexes, channels, context |
| | Performance | `backend/performance.md` | Caching (Redis), slow queries, indexing, n+1 |
| | Precision | `backend/precision.md` | Decimal vs float, money/amount handling |
| **Common** | Testing | `common/testing.md` | Unit tests, integration tests, mocks, TDD |
| | CI/CD | `common/cicd.md` | GitHub Actions, Docker, Kubernetes, deployment |
| | Git | `common/git.md` | Merge conflicts, rebasing, branch management |
| | Code Quality | `common/code-quality.md` | Refactoring, design patterns, linting |

## Script Usage

The main script can be run directly:

```bash
python3 scripts/summarize.py
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_HISTORY_PATH` | Auto-detected | Path to conversation history JSON |
| `GOTCHAS_DIR` | `./docs/gotchas` | Path to docs/gotchas directory |
| `DRY_RUN` | `false` | Set to `true` to preview changes without writing |
| `TIMESTAMP_FORMAT` | `%Y-%m-%d %H:%M:%S` | Format for timestamps in generated markdown |
| `LOCALE` | `zh` | Interface language (`zh` for Chinese, `en` for English) |
| `LOG_LEVEL` | `WARNING` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `ENABLE_ERROR_TRACKING` | `false` | Enable detailed error tracking and statistics |

### Examples

```bash
# Default: analyze latest conversation and update docs
python3 scripts/summarize.py

# Preview changes without writing
DRY_RUN=true python3 scripts/summarize.py

# Specify custom gotchas directory
GOTCHAS_DIR=/path/to/docs/gotchas python3 scripts/summarize.py

# Use specific conversation history
CLAUDE_HISTORY_PATH=/path/to/history.jsonl python3 scripts/summarize.py

# Use English locale
LOCALE=en python3 scripts/summarize.py

# Custom timestamp format (ISO 8601)
TIMESTAMP_FORMAT="%Y-%m-%dT%H:%M:%S%z" python3 scripts/summarize.py

# Enable debug logging and error tracking
LOG_LEVEL=DEBUG ENABLE_ERROR_TRACKING=true python3 scripts/summarize.py
```

## Output Format

The skill generates markdown sections following this format:

### Chinese (Default)

```markdown
## 问题：[简短标题]

> **自动生成时间**: 2026-02-04 18:00:00

### 错误信息
```
错误信息内容
```

### 相关代码
```javascript
// Code with automatic language detection
const example = "value";
```

### 问题描述
[解释为什么会发生这个问题]

### 根本原因
[问题背后的技术原因]

### 解决方案
[解决该问题的方法]

### 最佳实践清单
- [ ] 检查项 1
- [ ] 检查项 2

---
```

### English (LOCALE=en)

```markdown
## Issue: [Short Title]

> **Auto-generated time**: 2026-02-04 18:00:00

### Error Information
```
Error message content
```

### Related Code
```javascript
// Code with automatic language detection
const example = "value";
```

### Problem Description
[Explanation of why this issue occurs]

### Root Cause
[Technical reason behind the problem]

### Solution
[Method to resolve the issue]

### Best Practices Checklist
- [ ] Check item 1
- [ ] Check item 2

---
```

### Multiple Code Blocks

When multiple code blocks in different languages are detected, they are grouped:

```markdown
### 相关代码

#### JAVASCRIPT
```javascript
const App = () => <div />;
```

#### GO
```go
func main() {}
```
```

## Duplicate Detection

Before adding new content, the script:
1. Reads all existing gotcha files
2. Normalizes text (removes markdown formatting, timestamps, IDs)
3. Checks for similar titles (fuzzy matching with 0.75 threshold)
4. Checks for similar error messages
5. Checks for similar code patterns
6. Skips adding if a duplicate is detected (with warning)

## Error Statistics

When `ENABLE_ERROR_TRACKING=true`, the script outputs detailed error statistics:

```
📊 Error Statistics:
   • Total entries processed: 150
   • JSON parse errors: 3
   • File read errors: 0
   • File write errors: 1
   • Classification errors: 0
```

This helps identify data quality issues in conversation history files.

## Integration with Session End

This skill is designed to be called automatically at the end of conversations. You can set up a session-end hook in your Claude Code configuration to automatically run `gotcha-summarizer` when a conversation ends.

## Troubleshooting

### No technical issues found

If the skill doesn't detect any technical issues:
- Ensure the conversation contains error messages, code examples, or problem-solving discussions
- Try manually triggering the skill with explicit instructions about what to document

### Duplicate entries

The skill attempts to detect duplicates, but may occasionally create similar entries. Review the generated content and merge or remove duplicates as needed.

### File permission errors

Ensure the `docs/gotchas/` directory is writable:
```bash
chmod +w docs/gotchas/*.md
```

## See Also

- [docs/gotchas/README.md](../../README.md) - Gotchas documentation index
- [docs/gotchas/database.md](../../database.md) - Database and ORM issues and solutions
- [docs/gotchas/code-quality.md](../../code-quality.md) - Code quality issues and solutions
