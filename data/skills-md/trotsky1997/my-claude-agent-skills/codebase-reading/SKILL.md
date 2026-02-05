---
name: codebase-reading
description: Systematic methodology for reading and understanding large codebases efficiently. Use when (1) Understanding a new or unfamiliar codebase quickly, (2) Preparing to modify or extend existing code safely, (3) Debugging complex issues requiring deep code understanding, (4) Onboarding new team members to a codebase, (5) Performing code audits or security reviews, (6) Refactoring legacy code with confidence, (7) Creating documentation for existing systems, (8) Tracing execution flows and data transformations
metadata:
  short-description: Efficiently read and understand large codebases
---

# Large Codebase Reading Methodology

A systematic approach to understanding large codebases efficiently: **read to modify safely, not to memorize everything**.

## Core Principle

**Goal-oriented reading**: Always start with a concrete objective (fix bug, add feature, debug issue, security audit). Without a goal, you'll get lost in details.

**Success criteria**: You can explain the execution flow and modify code confidently, not that you've read every file.

## Documentation Structure

When documenting your understanding, use this structure:

```
code-reading/
├── README.md              # Index and progress tracking
├── code-reading.md        # Main framework (methodology + findings + terminology)
├── architecture.md        # C4 architecture map (Level 1-4)
├── api-flow.md            # Execution flow tracing
└── key-modules.md         # Detailed module analysis
```

**Progressive disclosure:**
- README: Overview and navigation
- Main doc: Methodology and high-level findings
- Specialized docs: Detailed analysis (loaded only when needed)

**Terminology section:**
- Include a dedicated "Terminology" or "Key Concepts and Terminology" section in `code-reading.md` (e.g., section 9)
- Build incrementally from day 1, don't wait until everything is understood
- Cross-reference terms throughout documentation (architecture, flows, modules)
- Maintain as a living document - update as understanding deepens


## Quick Start

### Step 1: Define Your Goal

Start with a concrete, one-sentence objective:

- ✅ Good: "Trace HTTP request from route handler to database and back"
- ✅ Good: "Understand how authentication tokens are validated and refreshed"
- ❌ Bad: "Understand the entire codebase"

### Step 2: Run the Project First

**First hour priority:**

1. Read README - project purpose, setup, minimal example
2. Read CONTRIBUTING/development guide - testing, structure, workflow
3. Run a minimal path - local build, one test, or demo

**Why:** Running code transforms reading from guessing to verification.

### Step 3: Map the Architecture (C4 Thinking)

Draw a rough map from far to near (no need to be perfect):

**Level 1: System Context** - Who uses it? What external dependencies?
**Level 2: Containers** - What are the deployable units? (services, databases, workers)
**Level 3: Components** - What are the key components within one container?

> You don't need beautiful diagrams - just enough to navigate: **where's the entry point, how does data flow, where are the boundaries?**

### Step 4: Trace a Real Request Path

Instead of reading modules, **read one execution path**:

- Web: route → controller → service → repository → external API
- CLI: main → command parser → execution path
- Async: consumer → handler → processing → ack/retry

**Strongly recommended:** Use a debugger, add logging, set breakpoints to walk through once.

### Step 5: Treat Tests as Executable Documentation

If code is old/hard to test, write **characterization tests** first - record current behavior, then refactor under protection.

## Core Workflow

### 1. Goal-Oriented Setup

**Define your reading task:**

Write a one-sentence goal that describes what you want to achieve:
- "I can explain the request flow from HTTP to database"
- "I can safely modify the authentication module"
- "I can trace the OCR pipeline from image input to result output"

**Avoid:** Reading without purpose or starting from directory trees.

### 2. Project Bootstrap

**Priority order (first hour):**

1. **README.md** - What does it do? How to start? Minimal example?
2. **CONTRIBUTING.md / docs/** - How to test? Code structure? Branch strategy?
3. **Run minimal path** - Can you build it? Run one test? Execute a demo?

**Verify:** Model files exist, tests run, examples work.

### 3. Architecture Mapping (C4 Model)

**Level 1: System Context**
- Users/applications that interact with the system
- External dependencies (databases, APIs, services)
- System boundaries

**Level 2: Containers**
- Deployable units (frontend, API server, workers, databases, queues)
- Communication between containers

**Level 3: Components**
- Key components within a container (auth service, domain service, repository, adapter)
- Component relationships and dependencies

**Output:** A rough map that answers:
- Where's the entry point?
- How does data flow?
- Where are the boundaries?

### 4. Entry Point + Request Tracing

**Find the entry point:**
- Web: `main()`, route handlers, controllers
- CLI: `main()`, command parsers
- Library: public API functions, constructors

**Trace one complete path:**
- Use debugger to step through
- Add logging at key points
- Set breakpoints to verify understanding

**Document the flow:** Write down the execution path as you trace it.

### 5. Tests as Documentation

**Existing tests:**
- Read tests to understand expected behavior
- Tests show how components are used
- Tests document edge cases and error handling

**Missing tests:**
- Write characterization tests (record current behavior)
- Use tests as a safety net before modifications
- Tests become regression suite

### 6. Git Archaeology

**When you see "weird code":**

Don't dismiss it immediately - ask: **What historical problem is this solving?**

**Commands:**
```bash
git blame -w -- path/to/file          # Who changed this and when?
git log -p -- path/to/file            # Full change history
git log --grep="keyword"              # Find related commits
git show <commit-hash>                # View specific change
```

**What to look for:**
- Commit messages explaining why
- PR discussions showing trade-offs
- Major refactors showing architecture evolution

### 7. Use Tools Efficiently

**Code search:**
```bash
rg "keyword" -n .                     # Ripgrep (faster than grep)
git grep "keyword"                    # Git-optimized search
rg "main\(" .                         # Find entry points
rg "TODO|FIXME" .                     # Find todos
```

**Git tools:**
```bash
git log --graph --oneline --all       # Visual history
git log --follow -- path/to/file      # File rename tracking
git diff HEAD~5 HEAD                  # Compare versions
```

**Language-specific tools:**
- Rust: `cargo tree`, `cargo clippy`, `cargo doc`
- Python: `pytest`, `mypy`, `pylint`
- JavaScript: `npm list`, `eslint`, `tsc`

### 8. Build and Maintain Terminology Glossary

**Critical for understanding:** Build a living terminology glossary from day 1, not as an afterthought.

**Why it matters:**
- Domain-specific terms (OCR: detection, recognition, CTC, NMS)
- Acronyms that need expansion (CLS, DB, IOU)
- Project-specific abstractions (custom types, internal concepts)
- Confusion between similar concepts (Orientation vs CLS, Detection vs Recognition)

**When to build:**
- **Initial collection**: During first reading pass (Steps 1-4) - collect terms as you encounter them
- **Deep dive enrichment**: During detailed module analysis (Step 10) - add technical details and context
- **Continuous maintenance**: Update as understanding deepens, add cross-references, refine definitions

**What to include:**
- **Definition**: Clear explanation of what the term means
- **Context**: Where and how it's used in the codebase
- **Code references**: File paths, function names, line numbers
- **Relationships**: Related terms, parent/child concepts, synonyms
- **Examples**: Usage examples, code snippets when helpful

**Organization:**
- Classify by domain (OCR terms, ML terms, project-specific)
- Group by abstraction level (concepts, algorithms, data structures, implementation)
- Cross-reference to architecture diagrams, API flows, module analysis

**Example structure:**
```markdown
## Terminology Glossary

### Domain-Specific Terms
- **Detection (检测)**: Locating text regions in images
  - **Implementation**: `src/det.rs`
  - **Related**: Recognition, NMS, DB
  - **See**: `api-flow.md` section 4.1

### Data Structures
- **`Mat`**: Image matrix abstraction
  - **Implementation**: `src/image_impl.rs`
  - **Purpose**: Unified image representation for Pure Rust and OpenCV backends

### Algorithms
- **NMS (Non-Maximum Suppression)**: Algorithm for filtering overlapping boxes
  - **Implementation**: `src/geometry.rs::nms()`
  - **Related**: IOU (Intersection over Union)
```

**Tools for term extraction:**
```bash
# Extract acronyms (all caps, 2-5 chars)
rg "\b[A-Z]{2,5}\b" README.md docs/ | sort -u

# Extract struct/enum/trait names
rg "^(pub )?(struct|enum|trait|type) \w+" src/ -o | sort -u

# Find config-related terms
rg "Config.*\{|struct \w+Config" src/
```

**Maintenance checklist:**
- [ ] All acronyms have expansions
- [ ] All domain terms have clear definitions
- [ ] All key data structures are documented
- [ ] Cross-references to code are accurate
- [ ] Related terms are linked
- [ ] Examples provided for complex terms

## Common Patterns

### Pattern 1: Reading Without a Goal

**Problem:** Reading files alphabetically or by directory structure.

**Solution:** Start with a concrete task. Even if it's "understand how X works," make it specific.

### Pattern 2: Getting Lost in Details

**Problem:** Deep-diving into every module before understanding the flow.

**Solution:** First trace one complete execution path. Then dive into specific modules as needed.

### Pattern 3: Ignoring Tests

**Problem:** Treating tests as optional or skipping them.

**Solution:** Tests are the most reliable documentation. Read them first. If missing, write characterization tests.

### Pattern 4: Not Using Git History

**Problem:** Seeing "weird code" and assuming it's wrong.

**Solution:** Use `git blame` and `git log` to understand context. Code exists for reasons, even if not obvious.

### Pattern 5: Ignoring Terminology (Acronyms and Domain Terms)

**Problem:** Encountering acronyms (CTC, CLS, DB, NMS) or domain terms (Detection vs Recognition) and assuming you'll remember what they mean later. Repeatedly looking up the same terms.

**Solution:** Build a terminology glossary from day 1. Collect terms as you encounter them, enrich with context as understanding deepens. Cross-reference terms throughout documentation. Treat it as a living document, not a one-time task.

## Success Indicators

You've successfully understood a codebase when:

✅ You can explain the main execution flow from entry to exit
✅ You can locate where specific functionality is implemented
✅ You can trace data transformations through the system
✅ You can identify where to make changes for your goal
✅ You can explain architectural decisions (even if you'd do differently)
✅ You have a comprehensive terminology glossary that helps navigate the codebase
✅ You can explain any domain-specific term in one sentence
✅ You rarely need to re-lookup the same term
✅ You feel confident modifying code without breaking things

**Not required:**
- ❌ Having read every file
- ❌ Memorizing every function
- ❌ Understanding every detail

## Troubleshooting

**"I don't know where to start"**
→ Define a concrete goal. Even "understand how user authentication works" is better than "understand everything."

**"The codebase is too large"**
→ Focus on your goal. Trace one execution path. Ignore unrelated modules.

**"I can't find the entry point"**
→ Look for `main()`, route definitions, or public API functions. Use code search tools.

**"The code doesn't make sense"**
→ Use Git history to understand why it's written this way. Check tests for usage examples.

**"There are no tests"**
→ Write characterization tests. Record current behavior before modifying.

**"I keep forgetting what CTC/CLS/DB means"**
→ Build a terminology glossary. Start early, collect terms as you encounter them. Include definitions, context, code references, and relationships. Cross-reference throughout documentation.

**"The domain terms are confusing"**
→ Don't just look them up once. Document them with context, usage examples, and relationships to other terms. Classify by domain and abstraction level. Update as understanding deepens.

## References

For detailed methodology and examples, see:

- [methodology.md](references/methodology.md) - Complete 11-step methodology with detailed explanations
- [tool-checklist.md](references/tool-checklist.md) - Comprehensive tool checklist by category (search, Git, language-specific, debugging)
- [terminology-building.md](references/terminology-building.md) - **Complete guide to building and maintaining terminology glossaries** (5-step process, classification methods, best practices, common patterns)
