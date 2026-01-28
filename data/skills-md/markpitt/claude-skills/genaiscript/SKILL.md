---
name: genaiscript
description: Comprehensive expertise for working with Microsoft's GenAIScript framework - a JavaScript/TypeScript-based system for building automatable LLM prompts and AI workflows. Use when creating, debugging, or optimizing GenAIScript scripts, implementing prompts-as-code, working with tools and agents, processing files (PDF, CSV, DOCX), defining schemas, or building AI automation workflows.
version: 2.0
---

# GenAIScript Expert

You are an expert in Microsoft's GenAIScript framework, a JavaScript-based system for building automatable prompts and AI workflows. This skill provides orchestrated access to comprehensive GenAIScript documentation.

## What GenAIScript Feature Do I Need?

Use this decision table to find the right resource for your task:

| Your Task | Core Concepts | API Ref | Examples | Patterns | 
|-----------|:---:|:---:|:---:|:---:|
| **Understanding framework fundamentals** | ✓ | | | |
| Explaining script structure, workflow basics | ✓ | | | |
| **Learning specific API functions** | | ✓ | ✓ | |
| Using `$`, `def()`, `defSchema()`, `defTool()`, etc. | | ✓ | | |
| **Building practical solutions** | | ✓ | ✓ | ✓ |
| Code review, doc generation, testing scripts | | ✓ | ✓ | ✓ |
| **Designing robust solutions** | | | | ✓ |
| Performance, error handling, modular architecture | | | | ✓ |
| Advanced workflows, design patterns, optimization | | | | ✓ |
| **Token management, caching, parallelization** | | | | ✓ |

## Quick Start

### 1. Basic Script Structure
```javascript
script({
    title: "My Script",
    description: "What this does",
    model: "openai:gpt-4"
})

def("FILE", env.files)
$`Analyze the FILE and provide insights.`
```

See **resources/core-concepts.md** for detailed explanation.

### 2. Include Context
```javascript
// Include file content
def("CODE", env.files, { endsWith: ".ts", lineNumbers: true })

// Include structured data
const rows = await parsers.CSV(env.files[0])
defData("ROWS", rows)

// Define output structure
const schema = defSchema("RESULT", {
    type: "object",
    properties: { /* schema */ }
})
```

See **resources/api-reference.md** for all functions.

### 3. Common Patterns
- Code review & analysis → **resources/examples.md** (Code Quality section)
- Documentation generation → **resources/examples.md** (Documentation section)
- Data extraction → **resources/examples.md** (Data Processing section)
- Performance optimization → **resources/patterns.md** (Performance section)

## 3-Phase Orchestration Protocol

### Phase 1: Task Analysis

Determine what you're building:

**Script Purpose:**
- **Analysis**: Review code, find issues, validate structure
- **Generation**: Create tests, docs, code, configs
- **Transformation**: Convert formats, migrate code, refactor
- **Integration**: Connect APIs, process files, orchestrate workflows

**Complexity Level:**
- **Simple**: Single LLM call, clear requirements
- **Intermediate**: 2-3 LLM calls, structured outputs
- **Advanced**: Multi-step workflows, agents, tools, caching

### Phase 2: Resource Selection

Load resources based on task type:

- **Starting out** → Load `resources/core-concepts.md`
- **Need API details** → Load `resources/api-reference.md`
- **Building solution** → Load `resources/examples.md` (find similar example)
- **Optimizing** → Load `resources/patterns.md` (see advanced patterns)
- **Complex task** → Load `resources/patterns.md` (design patterns section)

### Phase 3: Execution & Validation

**While building:**
- Reference decision table above to navigate resources
- Use examples as templates
- Follow patterns for performance/reliability

**Before using script:**
- Validate file inputs are available
- Test with sample data
- Check token budget (see patterns/performance)
- Verify schema matches expected output

## Core Concepts Overview

GenAIScript enables:
- **Prompt-as-Code**: Build prompts programmatically with JavaScript/TypeScript
- **File Processing**: Import context from PDFs, DOCX, CSV, and other formats
- **Tool Integration**: Define custom tools and agents for LLMs
- **Structured Output**: Generate files, edits, and structured data from LLM responses
- **MCP Support**: Integrate with Model Context Protocol tools and resources

For detailed explanation of concepts, see **resources/core-concepts.md**

## Resource Files

| Resource | Purpose | Size | Best For |
|----------|---------|------|----------|
| [core-concepts.md](resources/core-concepts.md) | Framework fundamentals, script structure, file processing | ~280 lines | Learning basics, understanding how GenAIScript works |
| [api-reference.md](resources/api-reference.md) | Complete API documentation, function signatures, parameters | ~350 lines | Looking up function details, understanding options |
| [examples.md](resources/examples.md) | Practical examples for common use cases | ~400 lines | Building solutions, finding templates |
| [patterns.md](resources/patterns.md) | Advanced patterns, optimization, best practices, design patterns | ~350 lines | Optimizing performance, handling complex tasks |

## Common Workflows

**I want to...**

→ **Analyze existing code** 
1. Read `resources/core-concepts.md` (understand `def()`)
2. Check `resources/examples.md` → Code Quality section
3. See `resources/patterns.md` → Error Handling

→ **Generate documentation**
1. Check `resources/examples.md` → Documentation section
2. Use example as template
3. See `resources/api-reference.md` for `defFileOutput()`

→ **Process files and extract data**
1. Read `resources/core-concepts.md` (file processing section)
2. Check `resources/examples.md` → Data Processing section
3. Reference `resources/api-reference.md` → Parsers

→ **Build multi-step workflow**
1. See `resources/patterns.md` → Design Patterns (Chain of Responsibility)
2. Check `resources/examples.md` → Advanced Workflows section
3. Reference `resources/api-reference.md` for function details

→ **Optimize performance or debug**
1. See `resources/patterns.md` → Performance Optimization section
2. Check `resources/patterns.md` → Error Handling section
3. Reference `resources/api-reference.md` for token management options

## Quick Reference

| Component | Learn More |
|-----------|-----------|
| `$` template tag | api-reference.md § Core Functions |
| `def()` file inclusion | api-reference.md § Core Functions |
| `defSchema()` output structure | api-reference.md § Core Functions + examples.md |
| `defTool()`, `defAgent()` | api-reference.md § Core Functions |
| Parsers (PDF, CSV, XLSX, etc.) | api-reference.md § Parsers |
| Environment variables | api-reference.md § Environment + core-concepts.md |
| Token management | patterns.md § Performance Optimization |
| Error handling | patterns.md § Error Handling |
| Design patterns | patterns.md § Design Patterns |

## Getting Help

When helping with GenAIScript:

1. **Ask what they're building** - Analysis? Generation? Transformation?
2. **Point to resource** - Use decision table above
3. **Show example** - See `resources/examples.md` for similar use case
4. **Check patterns** - For optimization/debugging, see `resources/patterns.md`
5. **Reference API** - For specific functions, see `resources/api-reference.md`

## VS Code Integration

GenAIScript includes a VS Code extension with:
- Syntax highlighting for `.genai.mjs` files
- IntelliSense for API functions
- Debug support with breakpoints
- Script runner to test scripts
- Output preview for generated files

```bash
# Running scripts
genaiscript run <script-name>
genaiscript run <script-name> file1.ts file2.ts
genaiscript run <script-name> --var KEY=value
genaiscript run <script-name> --model openai:gpt-4
```

See `resources/core-concepts.md` for more details.

---

**Navigation Tip**: Each resource file contains cross-references. Start with the resource matching your task type, then follow "See also" links as needed.
