---
name: deepwiki
description: Generate DeepWiki-style source code documentation for local codebases, transforming engineering experience into reusable cognitive structures
metadata:
  author: Carson
  version: "2026.1.30"
---

# Codebase Documentation Generator

Transform "local codebases" through automatic analysis → engineering cognitive modeling → generating maintainable DeepWiki-style project documentation.

**One-sentence definition**: Convert an unfamiliar code directory into a set of "human-readable, AI-searchable, long-term maintainable" engineering cognitive assets.

---

## Usage Scenarios

**Use this Skill when you need to:**

- Generate structured codebase cognitive documentation for new team members
- Create systematic Wiki documentation for local/private projects
- Externalize engineering experience into reusable knowledge assets
- Establish long-term engineering memory sources that AI can retrieve

**Do NOT use this Skill when:**

- API documentation is needed (use TypeDoc/JSDoc)
- The codebase is very small (< 100 lines)
- Specific tool proprietary format output is needed (e.g., Litho)

---

## Core Principles

### DeepWiki Style Writing Guidelines

1. **Big picture first, then details** — Help readers understand "what this is" before explaining "how it works"
2. **Responsibilities before implementation** — Explain "what it does" before "how it does it"
3. **Semantic-level explanation** — Explain the design intent, parameter meanings, and reference relationships of key entities (classes/functions), **avoid line-by-line code translation**
4. **Use engineering language** — Use "domain terminology" rather than "teaching language"

### 3 Questions Every Page Must Answer

1. What is the **purpose** of this section?
2. What is its **position and boundary** in the system?
3. As a developer, **when should I care about it**?

---

## Documentation Output Structure

Generate the following DeepWiki-style project Wiki structure (can be extended based on actual project needs):

```
docs/
├── overview.md              # Project overview: what it is, tech stack, entry points
├── architecture.md          # Architecture design: module division, dependencies, diagrams
├── modules/                 # Module-level documentation
│   ├── [module-name].md     # Independent documentation for each core module
│   └── ...
├── flows.md                 # Behavior and flows: how the system runs
├── design-decisions.md      # Design decisions: why designed this way
└── appendix.md              # Appendix: glossary, references
```

Each page satisfies:

- Can be read independently
- Can be retrieved by RAG / search
- Can be updated individually without full re-generation

---

## Execution Pipeline (Five-Phase Analysis)

> Aligns with DeepWiki's "top-down cognition" + smart-docs' "engineering judgment"

---

### Phase 1: Codebase Reconnaissance

**Goal: Answer "What kind of project is this?"**

**Actions:**

- Scan overall directory structure
- Identify primary language / framework / build method
- Determine project type (application / library / tool / multi-module project)

**Ignored by default:**

- `node_modules/`, `dist/`, `build/`, `.git/`
- Obvious generated files or cache directories

**Intermediate output:**

- Project type determination
- Primary subsystem candidates
- Tech stack tags

---

### Phase 2: Structure Modeling

**Goal: Answer "How is the project organized?"**

**Actions:**

- **System-Subsystem decomposition**: Identify hierarchical structure of systems, subsystems, and modules
- **Build semantic graph**: Extract dependencies and call relationships between modules
- Build module boundaries (based on directory + dependency relationships)
- Analyze module dependency directions
- Identify core modules vs peripheral modules

**Output:**

- `architecture.md`
- Module responsibility overview
- Architecture relationship diagrams (Mermaid)
- System-Subsystem hierarchy table

**Writing guidelines:**

Use the `architecture.md` template from [templates.md](references/templates.md).

---

### Phase 3: Module Understanding

**Goal: Answer "What is the purpose of each module?"**

**For each core module:**

- **Build internal semantic graph**: Extract key entities (classes/interfaces/functions) and their call, inheritance, and dependency relationships
- Extract key files and public API
- Summarize module responsibilities and boundaries
- Identify typical usage patterns

**Output:**

- `modules/[module-name].md`
- Key entity relationship diagrams (Class Diagram / Entity Graph)

**Module documentation unified structure:**

Use the `modules/[module-name].md` template from [templates.md](references/templates.md).

---

### Phase 4: Flow Synthesis

**Goal: Answer "How does the system run?"**

**Actions:**

- Locate entry points (CLI / main / server / job)
- Track main call chains
- Abstract key flows and control transfers

**Output:**

- `flows.md`
- Main process explanation
- Optional flows / exception paths

**Writing guidelines:**

Use the `flows.md` template from [templates.md](references/templates.md).

---

### Phase 5: Design Insight

**Goal: Answer "Why was it designed this way?"**

**Actions:**

- **Auto-summary and completion**: Summarize key information and complete missing logical explanations based on context
- Identify obvious design patterns
- Infer historical decisions and engineering trade-offs
- Annotate certainty / uncertainty of inferences

**Output:**

- `design-decisions.md`

**Writing guidelines:**

Use the `design-decisions.md` template from [templates.md](references/templates.md).

---

## Detailed Documentation Templates

For detailed documentation templates, please refer to [templates.md](references/templates.md), including:

- `overview.md`
- `architecture.md`
- `modules/[module-name].md`
- `flows.md`
- `design-decisions.md`

---

## VitePress Integration

For detailed configuration, please refer to [vitepress-config.md](references/vitepress-config.md).

---

## Language/Framework Specific Patterns

### Vue 3 Projects

- **Focus**: Composables, components, reactive state, Props/Emits
- **Entry**: `main.ts`, `App.vue`
- **Config**: `vite.config.ts`, `tsconfig.json`
- **Key Patterns**:
  - Composables: Reusable logic extraction
  - Provide/Inject: Cross-level state sharing
  - Pinia: Global state management
  - Component communication: Props down, Events up

### React Projects

- **Focus**: Hooks, components, Context, state management
- **Entry**: `main.tsx`, `App.tsx`
- **Config**: `vite.config.ts`, `tsconfig.json`
- **Key Patterns**:
  - Custom Hooks: Reusable logic
  - Context API: Cross-level state sharing
  - Zustand/Redux: Global state management
  - Component composition patterns

### TypeScript/JavaScript

- **Focus**: Modules, exports, types, interfaces
- **Entry**: `index.ts`, `main.ts`
- **Config**: `tsconfig.json`, `package.json`

---

## Quality Checklist

- [ ] Each page answers "What is its purpose"
- [ ] Each page answers "Where is its position and boundary"
- [ ] Each page answers "When should I care about it"
- [ ] Avoid line-by-line code explanation
- [ ] Use engineering language rather than teaching language
- [ ] Explain big picture before details
- [ ] Explain responsibilities before implementation
- [ ] Mermaid diagrams render correctly
- [ ] Documentation links are valid
- [ ] Naming is consistent

---

## Extension Directions

- ✅ Incremental analysis (only analyze changed modules)
- ✅ Multi-subproject / Monorepo support
- ✅ Integration with Obsidian / internal Wiki
- ✅ As AI's long-term engineering memory source

---

## Summary

> **The value of this Skill is not in "writing documentation",**
> **but in solidifying "code reading engineering experience" into reusable cognitive structures.**

This is a future-facing, engineering-grade knowledge generation Skill.
