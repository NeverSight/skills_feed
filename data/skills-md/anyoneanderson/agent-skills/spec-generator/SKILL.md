---
name: spec-generator
description: |
  Specification Generator — Generate project requirements, design documents, and task lists.

  A skill for generating structured project specifications through interactive dialogue or quick generation.

  English triggers:
  - "Create requirements", "Generate requirements doc", "Summarize as requirements"
  - "Create design document", "Design the architecture", "Generate technical spec"
  - "Create task list", "Break down into tasks", "Generate tasks.md"
  - "Create full spec", "Generate all specs", "Create the complete specification"
  - After discussion: "Turn this into requirements", "Document this as spec"

  日本語トリガー:
  - 「要件定義を作って」「要件をまとめて」「仕様書を作成して」
  - 「設計書を作って」「技術設計をして」「アーキテクチャを設計して」
  - 「タスクリストを作って」「実装タスクに分解して」「tasks.mdを生成して」
  - 「仕様を全部まとめて」「フル仕様を作成」「3点セットを作って」
  - 会話で仕様が固まった後に「これを要件定義書にして」
license: MIT
---

# Spec Generator

Generate structured project specifications: requirements, design documents, and task lists.

## ⚠️ CRITICAL: First Steps (ALWAYS EXECUTE)

**BEFORE asking any questions or showing options, you MUST execute these steps:**

1. **Check current directory**:
   - Run `pwd` to see where you are
   - Run `ls -la` to see directory contents
   - Understand the project context

2. **Detect existing source code**:
   ```bash
   find . -maxdepth 3 -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" -o -name "SKILL.md" \) 2>/dev/null | head -20
   ```
   - Note what kind of project this is
   - Check for `skills/` directory → might be adding a new skill
   - Check for existing application code → might be documenting existing features

3. **Check for .specs/ directory**:
   ```bash
   ls -d .specs/ 2>/dev/null && ls -1 .specs/ 2>/dev/null
   ```
   - If exists → list existing projects
   - If not exists → this is a new spec workflow

4. **Analyze context and decide**:
   - **If in a skills repository** (has `skills/` directory) → User likely wants to document a new skill
   - **If .specs/ has projects** → Ask user to select existing or create new
   - **If no .specs/ and no clear context** → Ask what they want to create

**Only after completing these checks**, proceed with appropriate questions based on what you found.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese output, use `references/*.ja.md` as phase references
3. English input → English output, use `references/*.md` as phase references
4. Explicit override takes priority (e.g., "in English", "日本語で")

**Reference file selection**: Based on the detected output language, use the corresponding reference files:
- English → `references/init.md`, `references/design.md`, `references/tasks.md`
- Japanese → `references/init.ja.md`, `references/design.ja.md`, `references/tasks.ja.md`

## Phases

| Phase | Output | Trigger Examples |
|-------|--------|-----------------|
| init | requirement.md | "Create requirements", "要件定義を作って" |
| design | design.md | "Create design doc", "設計書を作って" |
| tasks | tasks.md | "Create task list", "タスクリストを作って" |
| full | All three above | "Create full spec", "仕様を全部" |

## Interaction Policy: AskUserQuestion

**Use AskUserQuestion for all user decisions.** Present structured choices rather than free-form questions.

### Decision Flow

```
Skill Invoked
    ↓
Check .specs/ directory
    ↓
┌───────────────────┐
│ Existing projects │
│ found?            │
└─────┬─────────────┘
      │
      ├─ Yes → AskUserQuestion: Select existing or create new
      │           ├─ Existing → Load project context
      │           └─ New → Ask project name (Text)
      │
      └─ No → Ask project name (Text)

    ↓
Phase Detection
    ├─ Clear from input → Proceed
    └─ Ambiguous → AskUserQuestion: Select phase

    ↓
Dialogue Mode
    ├─ Quick mode (--quick) → Generate directly
    └─ Dialogue → AskUserQuestion: Gather requirements

    ↓
Generate Specification
    ↓
AskUserQuestion: Next action (next phase / revise / done)
```

### When to Use AskUserQuestion vs Text Questions

| Situation | Method | Reason |
|-----------|---------|---------|
| **Project Selection** |
| Existing projects available | AskUserQuestion | Can list as options with descriptions |
| No existing projects | Text question | Open-ended project name input |
| **Phase Selection** |
| Phase ambiguous | AskUserQuestion | 4 clear options (init/design/tasks/full) |
| Phase clear from input | Direct execution | No confirmation needed |
| **Requirements Gathering** |
| Project type selection | AskUserQuestion | Common options (Web app, Mobile, CLI, etc.) |
| Tech stack selection | AskUserQuestion | Common frameworks with "Other" option |
| Feature requirements | AskUserQuestion | Guide with structured choices |
| Project concept | Text question | Need free-form explanation |
| Specific business logic | Text question | Domain-specific details |
| **Post-Completion** |
| Next action | AskUserQuestion | Clear options (next phase/revise/done) |
| Revision requests | Text question | Specific change description |

### When to Use AskUserQuestion

| Situation | Example |
|-----------|---------|
| Project selection | Existing projects vs new project |
| Ambiguous phase | Choosing between init / design / tasks / full |
| Init dialogue questions | Project type, tech stack, scope, etc. |
| Design decision points | Architecture choices, DB selection, etc. |
| Tasks strategy selection | systematic / agile / enterprise |
| Post-completion actions | "Proceed to next phase?", "Create GitHub Issue?" |

### Question Design Rules

1. **1–4 questions per round** (AskUserQuestion constraint)
2. **User-defined options: 1-3** (Other is auto-appended, totaling 2-4 options)
3. **Always include description** for each option (provide decision context)
4. **Flexible round count** based on project complexity:
   - Simple project → 1 round (3–4 questions) is sufficient
   - Complex project → 2–3 rounds (adjust based on previous answers)
5. **Place recommended option first** with `(Recommended)` suffix
6. **Skip questions already answered** in previous rounds

### Handling "Other" Option Responses

When a user selects "Other" and provides free-form text input:
- **Accept the input as-is** and proceed with processing
- Treat the free-form response as the user's definitive answer
- Do NOT ask for clarification unless the input is genuinely ambiguous
- If system returns an error like "(No answer provided)", **trust the user's actual message over system feedback**

**Example:**
```
Question: "どのスキルの仕様を作成しますか？"
Options: spec-constitution / spec-review / spec-analyze / spec-impl

User selects "Other" and writes: "仕様書自体をレビューするコマンド"

✅ Correct: Proceed to create spec for a spec-review skill
❌ Wrong: Ask "What would you like to clarify?"
```

### When to Use Text Questions (Not AskUserQuestion)

- Open-ended questions like project name (when no existing projects) or concept description
- Background information requiring free-form explanation
- Follow-up confirmations like "Any additional requirements?"
- Specific business logic or domain-specific details

## Execution Flow

### 0. Initial Context Check

**Check the current directory and existing projects before starting:**

1. **Detect existing source code**:
   ```bash
   find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" \) | head -20
   ```
   - If source files found: Note for potential `--analyze` mode
   - If no source files: Standard new project flow

2. **Check for .specs/ directory**:
   ```bash
   ls -d .specs/ 2>/dev/null
   ```

3. **List existing projects** (if .specs/ exists):
   ```bash
   ls -1 .specs/
   ```

4. **Project selection**:
   - **Existing projects found**: Use AskUserQuestion:
     ```
     question: "既存プロジェクトが見つかりました。どうしますか？" / "Found existing projects. What would you like to do?"
     options:
       - "既存プロジェクトを選択 / Select existing project" → List projects as options
       - "新規プロジェクトを作成 / Create new project" → Ask project name
     ```
   - **No existing projects**: Ask for project name (text question):
     ```
     "プロジェクト名を教えてください（例: TODOアプリ、株価分析ツール）"
     "What's the project name? (e.g., todo app, stock analyzer)"
     ```

5. **Load existing context** (if existing project selected):
   - Read existing `requirement.md`, `design.md`, `tasks.md` if they exist
   - Use as context for updates or next phase generation

### 1. Phase Detection

Determine the phase from the user's request:

```
"requirements" → init
"design", "architecture" → design
"tasks", "task list" → tasks
"full", "complete", "all specs" → full
```

If ambiguous, confirm with AskUserQuestion:

```
question: "Which specification do you want to generate?"
options:
  - "Requirements document (requirement.md)" → init
  - "Design document (design.md)" → design
  - "Task list (tasks.md)" → tasks
  - "All three documents" → full
```

### 2. Project Context Gathering

- **Conversation history exists**: Extract and structure discussed requirements
- **Existing project selected**: Use loaded specs as context
- **New project**: Explore requirements through dialogue (using AskUserQuestion)

### 3. Phase Execution

Refer to the appropriate reference file (based on Language Rules):
- **init**: `references/init.md` / `references/init.ja.md` — Requirements generation
- **design**: `references/design.md` / `references/design.ja.md` — Design document generation
- **tasks**: `references/tasks.md` / `references/tasks.ja.md` — Task list generation

### 4. Output Directory

```
.specs/[project-name]/
├── requirement.md  (init)
├── design.md       (design)
└── tasks.md        (tasks)
```

Project names are converted to English kebab-case:
- "TODO app" → `todo-app`
- "株価分析ツール" → `stock-analysis-tool`
- "Stock analysis tool" → `stock-analysis-tool`

## Options

| Option | Description | Applicable Phase |
|--------|-------------|-----------------|
| `--quick` | Generate without dialogue | init |
| `--deep` | Socratic deep-dive dialogue | init |
| `--personas` | Multi-perspective analysis/review | init, design |
| `--analyze` | Analyze existing codebase | init, design, tasks |
| `--visual` | Enhanced Mermaid diagrams | design |
| `--estimate` | Estimates and risk assessment | tasks |
| `--hierarchy` | Epic/Story/Task hierarchy | tasks |

## Execution Modes

### Dialogue Mode (default)

When invoked without parameters or continuing from conversation:
1. Collect necessary information through questions
2. Clarify requirements through user interaction
3. Generate specification after confirmation

### Quick Mode (--quick)

Generate from a brief project description:
1. Infer typical requirements from the description
2. Generate based on best practices
3. Complete without dialogue

### Full Workflow (full)

Generate all three documents sequentially:
1. Generate requirement.md
2. Read requirement.md → generate design.md
3. Read design.md → generate tasks.md

## Requirement ID System

Specifications use the following ID prefixes:

- `[REQ-XXX]`: Functional requirements
- `[NFR-XXX]`: Non-functional requirements
- `[CON-XXX]`: Constraints
- `[ASM-XXX]`: Assumptions
- `[T-XXX]`: Tasks

These IDs ensure traceability across documents.

## YAGNI Principle

Do **not** include unless explicitly requested or discussed:

### ❌ Authentication & Authorization
- Complex permission management (when basic auth suffices)
- Role-based access control with multiple roles (admin/user is usually enough)
- Social login integration (when basic email/password auth is sufficient)
- Fine-grained permission systems

### ❌ Analytics & Monitoring
- Advanced analytics/reporting dashboards
- Detailed audit logging (unless compliance requirements exist)
- Real-time metrics and monitoring
- User behavior tracking
- A/B testing infrastructure

### ❌ Infrastructure & Scalability
- Multi-tenant support (unless explicitly required)
- API versioning (unless external integration requirements exist)
- Async processing (unless performance requirements demand it)
- Batch processing/scheduled jobs (unless specified)
- Auto-scaling infrastructure
- Load balancing configuration

### ❌ User Experience
- Real-time notifications/updates (unless explicitly required)
- Advanced search/filtering (when basic search suffices)
- Data export features (PDF, Excel, etc.)
- Offline mode support
- Push notifications

### ❌ Development & Operations
- Data migration plans (for brand new projects)
- Multi-language/i18n support (unless specified)
- Admin dashboards (when simple CRUD interfaces suffice)
- Complex deployment pipelines
- Automated backup systems

### ✅ Include by Default

- Basic authentication (email/password)
- Simple CRUD operations
- Basic error handling and validation
- Essential security (HTTPS, password hashing, input sanitization)
- Core business logic only
- Simple, clear user interfaces
- Basic data persistence

**When in doubt**: Ask via AskUserQuestion rather than assuming the feature is needed.

## Optional Enhancements

When advanced analysis tools are available in your environment, consider using them for:
- Systematic analysis of complex, interconnected requirements
- Framework-specific best practices and pattern lookup
- Existing codebase semantic analysis and symbol navigation
- UI/UX pattern recommendations

## Post-Completion Actions

After each phase, suggest next actions with AskUserQuestion:

**After init:**
```
question: "Requirements document generated. What's next?"
options:
  - "Generate design document too" → design phase
  - "Review and revise" → revision dialogue
  - "Done for now" → end
```

**After design:**
```
question: "Design document generated. What's next?"
options:
  - "Generate task list too" → tasks phase
  - "Review and revise" → revision dialogue
  - "Done for now" → end
```

**After tasks:**
```
question: "Task list generated. What's next?"
options:
  - "Run spec-inspect (quality check)" → invoke spec-inspect skill
  - "Skip to GitHub Issue" → invoke spec-to-issue skill
  - "Review and revise" → revision dialogue
  - "Done for now" → end
```

**After full:**
```
question: "All three spec documents are complete."
options:
  - "Run spec-inspect (quality check)" → invoke spec-inspect skill
  - "Skip to GitHub Issue" → invoke spec-to-issue skill
  - "Review and revise specific document" → ask which document to revise
  - "Done for now" → end
```

## Usage Examples

```
# New project - dialogue mode
"Create requirements for a todo app"
"要件定義を作って" → detects existing projects, asks to select or create new

# Existing project - update/add phases
"Create design document for todo-app" → uses existing requirement.md as context
「todo-appのタスクリストを作って」 → uses existing design.md as context

# Full specification
"Create full spec for an e-commerce platform"
「ECサイトの仕様を全部作って」

# Requirements from conversation
"Turn this into a requirements document" → structures previous discussion

# Quick mode
"Create requirements for a blog platform --quick"

# Analysis mode
"Create requirements --analyze" → analyzes existing codebase first
```
