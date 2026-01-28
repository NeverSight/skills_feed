---
name: codebase-summary
description: Analyze a codebase and generate comprehensive documentation including architecture, components, interfaces, workflows, and dependencies. Creates an AI-optimized knowledge base (index.md) and can consolidate into AGENTS.md, README.md, or CONTRIBUTING.md. Use when the user wants to document a codebase, create AGENTS.md, understand system architecture, generate developer documentation, or asks to "summarize the codebase".
---

# Codebase Summary

Generate comprehensive codebase documentation optimized for AI assistants and developers.

## Parameters

Gather all parameters upfront in a single prompt:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `codebase_path` | Current directory | Path to analyze |
| `output_dir` | `.sop/summary` | Documentation output directory |
| `consolidate` | `false` | Create consolidated file at codebase root |
| `consolidate_target` | `AGENTS.md` | Target: AGENTS.md, README.md, or CONTRIBUTING.md |
| `check_consistency` | `true` | Check for cross-document inconsistencies |
| `check_completeness` | `true` | Identify documentation gaps |
| `update_mode` | `false` | Update existing docs based on git changes |

## Workflow

### Step 1: Setup

1. Validate `codebase_path` exists
2. Create `output_dir` if needed
3. If `update_mode` and `index.md` exists:
   - Run `git log --oneline -20` to identify recent changes
   - Focus analysis on modified components

### Step 2: Analyze Structure

Run the structure analyzer:
```bash
python {baseDir}/scripts/analyze_structure.py "{codebase_path}" --depth 4 --output "{output_dir}/codebase_info.md"
```

Run the dependency extractor:
```bash
python {baseDir}/scripts/extract_dependencies.py "{codebase_path}" --output "{output_dir}/dependencies.md"
```

Then manually analyze:
- Identify packages, modules, major components
- Map architectural patterns (MVC, microservices, etc.)
- Find key interfaces, APIs, entry points

### Step 3: Generate Documentation

Create these files in `{output_dir}/`:

**index.md** - Primary AI context file:
- AI instructions for using the documentation
- Quick reference table mapping questions to files
- Table of contents with summaries for each file
- Brief codebase overview

**architecture.md**:
- System architecture with Mermaid `graph` diagram
- Layer descriptions
- Design patterns used
- Key design decisions with rationale

**components.md**:
- Component overview with Mermaid `classDiagram`
- Per-component: purpose, location, key files, dependencies, interface

**interfaces.md**:
- API endpoints with request/response formats
- Internal interfaces and implementations
- Error codes and handling

**data_models.md**:
- ER diagram with Mermaid `erDiagram`
- Per-model: table, fields, indexes, relationships

**workflows.md**:
- Key processes with Mermaid `sequenceDiagram`
- Step-by-step breakdowns
- Error handling

See `{baseDir}/references/documentation-templates.md` for templates.

### Step 4: Review

If `check_consistency`:
- Verify terminology consistency across documents
- Check cross-references are valid

If `check_completeness`:
- Identify undocumented components
- Note gaps from language/framework limitations

Save findings to `{output_dir}/review_notes.md`.

### Step 5: Consolidate (if enabled)

If `consolidate` is `true`:

1. Create file at codebase root (not in output_dir)
2. Use `consolidate_target` as filename
3. Tailor content to target:

| Target | Focus |
|--------|-------|
| AGENTS.md | AI context, directory structure, coding patterns, testing |
| README.md | Project overview, installation, usage, getting started |
| CONTRIBUTING.md | Dev setup, coding standards, contribution workflow |

Default AGENTS.md prompt: Focus on information NOT in README.md or CONTRIBUTING.md—file purposes, directory structure, coding patterns, testing instructions, package guidance.

### Step 6: Summary

Report:
1. What was documented
2. Next steps for using documentation
3. How to add index.md to AI assistant context
4. If `update_mode`: summarize detected changes

## Output Structure

```
{consolidate_target}           # At codebase root if consolidate=true
{output_dir}/
├── index.md                   # Primary AI context (read this first)
├── codebase_info.md          # Structure analysis output
├── architecture.md           # System architecture
├── components.md             # Component details
├── interfaces.md             # APIs and interfaces
├── data_models.md            # Data models
├── workflows.md              # Key workflows
├── dependencies.md           # Dependencies output
└── review_notes.md           # Review findings
```

## Progress Indicators

Provide updates:
```
Setting up...
✅ Created {output_dir}

Analyzing structure...
✅ Found X packages across Y languages
✅ Identified Z components

Generating documentation...
✅ Created index.md
✅ Generated architecture.md, components.md...

Reviewing...
✅ Consistency check complete
✅ Found N gaps documented in review_notes.md

Done!
✅ Documentation at {output_dir}
✅ Primary context file: {output_dir}/index.md
```

## Resources

- **Scripts:** `{baseDir}/scripts/analyze_structure.py`, `{baseDir}/scripts/extract_dependencies.py`
- **Templates:** `{baseDir}/references/documentation-templates.md`
