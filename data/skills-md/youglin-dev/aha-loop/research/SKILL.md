---
name: research
description: "Conducts deep technical research for Aha Loop stories. Use before implementing stories involving unfamiliar libraries or architectural decisions. Triggers on: research this, investigate, explore options, compare alternatives."
---

# Deep Research Skill

Conduct thorough technical research before implementation to ensure high-quality, informed decisions.

## Workspace Mode Note

When running in workspace mode, all paths are relative to `.aha-loop/` directory:
- Research reports: `.aha-loop/research/` (not `scripts/aha-loop/research/`)
- Knowledge base: `.aha-loop/knowledge/` (not `knowledge/`)
- Vendor directory: `.aha-loop/.vendor/` (not `.vendor/`)

The orchestrator will provide the actual paths in the prompt context.

---

## The Job

1. Identify research topics from the current story's `researchTopics` field
2. Fetch third-party library source code if needed
3. Search documentation and best practices
4. Analyze and compare alternatives
5. Generate a research report
6. Update knowledge base with findings
7. Mark `researchCompleted: true` in prd.json

---

## Research Process

### Step 1: Identify What to Research

Read the current story from `prd.json` and extract:
- `researchTopics` - explicit topics to investigate
- Dependencies mentioned in acceptance criteria
- Patterns referenced in the description

Also check:
- Previous story's `learnings` field for follow-up research needs
- `knowledge/project/gotchas.md` for related known issues

### Step 2: Fetch Library Source Code (If Needed)

For any third-party library research, fetch the source:

```bash
# Fetch specific library
./scripts/aha-loop/fetch-source.sh rust tokio 1.35.0

# Or fetch all project dependencies
./scripts/aha-loop/fetch-source.sh --from-deps
```

After fetching, the source will be at `.vendor/<ecosystem>/<name>-<version>/`

---

## Library Version Selection

### Always Prefer Latest Stable Versions

When researching or recommending libraries, **always check for and prefer the latest stable version** unless there's a specific compatibility reason not to.

### Version Research Process

1. **Query the package registry for latest version:**

   ```bash
   # Rust (crates.io)
   curl -s "https://crates.io/api/v1/crates/tokio" | jq '.crate.max_stable_version'
   
   # Or use cargo
   cargo search tokio --limit 1
   
   # Node.js (npm)
   npm view react version
   
   # Python (PyPI)
   pip index versions requests 2>/dev/null | head -1
   ```

2. **Verify stability:**
   - Released at least 1-2 weeks ago (not bleeding edge)
   - Check GitHub issues for critical bugs
   - Review changelog for breaking changes

3. **Check compatibility:**
   - Works with existing project dependencies
   - Compatible with project's minimum supported language version
   - No known conflicts

### Version Documentation

Always document version decisions:

```markdown
## Version Decision: [Library Name]

**Selected Version:** X.Y.Z
**Latest Available:** X.Y.Z (as of YYYY-MM-DD)
**Reason:** [Why this version was chosen]

**Compatibility Notes:**
- Works with [other dependency] v[X.Y]
- Requires [language] v[X.Y]+
```

### When to Use Older Versions

Only use older versions when:
- Latest version has critical bugs
- Incompatible with required dependencies
- Breaking changes require significant refactoring
- Project explicitly constrains the version

**Always document the reason** in `knowledge/project/decisions.md`:

```markdown
### ADR: Using [Library] v[Old] instead of v[New]

**Context:** [Why we're not using latest]
**Decision:** Pin to v[Old]
**Consequences:** [What we're missing, when to revisit]
```

---

### Step 3: Read Source Code Strategically

**Reading Order (Most Important First):**

1. **README.md** - Understand design intent and quick-start examples
2. **Entry Point Files:**
   - Rust: `src/lib.rs`, `src/main.rs`
   - TypeScript/JS: `src/index.ts`, `index.js`
   - Python: `__init__.py`, `main.py`
3. **Module Structure** - Scan `mod.rs` files or directory structure
4. **Type Definitions** - Find core structs, interfaces, types
5. **Target Functionality** - Locate the specific feature you need
6. **Tests** - Learn correct usage patterns from test files

**Reading Tips:**

- Use semantic search to find relevant code sections
- Focus on PUBLIC APIs, skip internal implementation unless needed
- Look for `examples/` directory for usage patterns
- Check `tests/` for edge cases and proper usage

### Step 4: Web Search for Context

Search for:
- Official documentation
- Best practices and common patterns
- Known issues and gotchas
- Performance considerations
- Alternative libraries

Use MCP tools like `context7` for up-to-date documentation.

### Step 5: Compare Alternatives (If Applicable)

When multiple solutions exist, create a comparison:

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Performance | ... | ... | ... |
| API Ergonomics | ... | ... | ... |
| Maintenance Status | ... | ... | ... |
| Bundle Size | ... | ... | ... |
| Learning Curve | ... | ... | ... |

Include a **recommendation** with reasoning.

---

## Research Report Template

Save to: `scripts/aha-loop/research/[story-id]-research.md`

```markdown
# Research Report: [Story ID] - [Story Title]

**Date:** YYYY-MM-DD
**Status:** Complete | Needs Follow-up

## Research Topics

1. [Topic from researchTopics array]
2. ...

## Findings

### Topic 1: [Name]

**Summary:** Brief answer to the research question

**Source Code Analysis:**
- Library: [name] v[version]
- Key File: `.vendor/rust/tokio-1.35.0/src/runtime/mod.rs`
- Relevant Code: Lines 123-189
- Pattern Observed: [description]

**Documentation Notes:**
- [Key insight from docs]
- [Another insight]

**Code Example:**
```[language]
// Example from source or docs
```

### Topic 2: [Name]
...

## Alternatives Comparison

| Criterion | Option A | Option B | Recommendation |
|-----------|----------|----------|----------------|
| ... | ... | ... | ... |

**Recommendation:** [Option X] because [reasoning]

## Implementation Recommendations

Based on research, the story should be implemented as follows:

1. [Specific implementation guidance]
2. [Pattern to follow]
3. [Pitfalls to avoid]

## Follow-up Research Needed

- [ ] [Topic that needs deeper investigation]
- [ ] [Question that emerged during research]

## Knowledge Base Updates

The following should be added to knowledge base:

**To `knowledge/project/patterns.md`:**
- [Pattern specific to this project]

**To `knowledge/domain/[topic]/`:**
- [Reusable knowledge about a library or technique]
```

---

## Updating Knowledge Base

### Project Knowledge (`knowledge/project/`)

Add patterns specific to THIS project:
- How this codebase uses a library
- Project-specific conventions discovered
- Gotchas specific to this codebase

### Domain Knowledge (`knowledge/domain/`)

Add reusable technical knowledge:
- Library usage patterns (applicable to any project)
- Comparison documents
- Best practices

**Create new topic directories as needed:**

```
knowledge/domain/
└── [topic-name]/
    ├── README.md           # Overview
    ├── patterns.md         # Common patterns
    ├── gotchas.md          # Known issues
    └── examples/           # Code examples
```

---

## Source Code Reading Report

When you read library source code, document your findings:

```markdown
## Source Code Analysis: [Library] v[Version]

### Module Structure
```
src/
├── lib.rs          # Main entry, exports public API
├── runtime/        # Async runtime implementation
│   ├── mod.rs      # Module exports
│   └── scheduler.rs # Task scheduling
└── sync/           # Synchronization primitives
```

### Key Types

- `Runtime` (src/runtime/mod.rs:45) - Main runtime struct
- `Handle` (src/runtime/handle.rs:23) - Runtime handle for spawning

### Key Functions

- `Runtime::new()` (L89-L120) - Creates new runtime with default config
- `spawn()` (L156-L189) - Spawns a new async task

### Usage Patterns from Tests

From `tests/runtime.rs:34`:
```rust
let rt = Runtime::new().unwrap();
rt.block_on(async {
    // ...
});
```

### Important Notes

- Thread safety: Runtime is Send + Sync
- Performance: Use `spawn_blocking` for CPU-heavy tasks
- Gotcha: Don't call `block_on` from async context
```

---

## Checklist

Before marking research complete:

- [ ] All `researchTopics` investigated
- [ ] Library source code fetched and key files read (if applicable)
- [ ] Web search performed for documentation and best practices
- [ ] Alternatives compared (if multiple options exist)
- [ ] Research report saved to `scripts/aha-loop/research/`
- [ ] Knowledge base updated with reusable findings
- [ ] Implementation recommendations documented
- [ ] `researchCompleted: true` set in prd.json
