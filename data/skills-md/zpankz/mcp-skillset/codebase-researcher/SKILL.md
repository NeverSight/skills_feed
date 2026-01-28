---
name: codebase-researcher
description: Deep research skill for analyzing codebases systematically. Use when comprehensive codebase understanding is needed, particularly for new projects or when documenting architecture. This skill should be used when users request deep analysis, architecture documentation, or systematic codebase research starting from root-level directories.
license: MIT
allowed-tools: Read, Glob, Grep, Bash, list_files, list_code_definition_names, search_files
---

# Codebase Researcher

Systematic deep research skill that analyzes codebases from the top level down, generating comprehensive knowledge about project structure, architecture, and implementation patterns.

## Purpose

Conduct systematic research of codebases to:
- Build comprehensive understanding of project architecture
- Document key components and their relationships
- Identify patterns, conventions, and best practices
- Generate knowledge bases (SKILL.md, CLAUDE.md, references/)
- Support onboarding and knowledge transfer

## When to Use

Use this skill when:
- Starting work on a new codebase
- Documenting existing architecture
- Creating CLAUDE.md or SKILL.md files
- Performing comprehensive code audits
- Building team knowledge bases

## Research Methodology

### Standard Deep Research Algorithm

The research process follows a hierarchical approach:

1. **Identify Root-Level Directories** - List all significant folders, excluding common ignore patterns
2. **Spawn Specialized Subagents** - Create one subagent per important directory
3. **Parallel Analysis** - Each subagent analyzes its assigned directory deeply
4. **Aggregate Findings** - Combine insights into cohesive documentation
5. **Generate Artifacts** - Produce SKILL.md, CLAUDE.md, and references/

### Directory Filtering

Automatically exclude from research:
- `node_modules/`, `venv/`, `.venv/`, `env/`
- `dist/`, `build/`, `out/`, `.next/`, `target/`
- `.git/`, `.svn/`, `.hg/`
- Hidden directories (starting with `.`) unless specifically relevant
- `__pycache__`, `*.egg-info`

Include in research:
- Source code directories (`src/`, `lib/`, `app/`)
- Configuration directories (`.roo/`, `.claude/`, `config/`)
- Documentation (`docs/`, `specs/`, `architecture/`)
- Scripts and tooling (`scripts/`, `tools/`, `cli/`)
- Tests (`tests/`, `__tests__/`, `spec/`)

## Using the Slash Command

Execute deep research via the provided slash command:

```bash
/deep-research
```

This command will:
1. Scan root-level directories
2. Determine which directories are important
3. Generate and execute a `claude` command with `--agents` flag
4. Spawn one subagent per important directory
5. Collect and synthesize findings

See [`scripts/deep_research.sh`](scripts/deep_research.sh) for implementation details.

## Script Integration

### Deep Research Script

The `scripts/deep_research.sh` script automates the research process:

**Key Features:**
- Automatically filters ignored directories via `.gitignore` patterns
- Dynamically generates subagents JSON for `claude --agents`
- Spawns parallel analysis tasks
- Aggregates results into structured output

**Usage:**
```bash
# From skill directory
./scripts/deep_research.sh [output_dir]

# From project root
./.roo/skills/codebase-researcher/scripts/deep_research.sh ./output
```

### Subagent Generation

The script uses `claude --agents` to programmatically create specialized subagents:

```json
{
  "cli-analyzer": {
    "description": "Analyze CLI directory structure and command patterns",
    "prompt": "You are an expert at analyzing CLI tooling. Examine the directory structure, identify command patterns, and document the architecture.",
    "tools": ["Read", "Glob", "Grep", "Bash"]
  },
  "skills-analyzer": {
    "description": "Analyze skills directory and documentation",
    "prompt": "You are an expert at analyzing Agent Skills. Examine skill structure, identify patterns, and document the skill ecosystem.",
    "tools": ["Read", "Glob", "Grep"]
  }
}
```

## Output Structure

Research produces:

### Primary Output: SKILL.md or CLAUDE.md

Contains:
- Project overview and purpose
- Architecture summary
- Key directories and their roles
- Important patterns and conventions
- Getting started guidance

### Supporting Output: references/

Detailed documentation organized by concern:
- `references/architecture.md` - System architecture
- `references/directory_structure.md` - Directory layout and purpose
- `references/patterns.md` - Code patterns and conventions
- `references/dependencies.md` - Dependency graph and relationships

## Research Workflow

### Phase 1: Discovery

```bash
# List root directories
ls -la

# Identify significant folders
find . -maxdepth 1 -type d ! -name ".*" ! -name "node_modules"

# Check for .gitignore patterns
cat .gitignore
```

### Phase 2: Subagent Orchestration

For each important directory, generate a specialized subagent with:
- **Name**: Derived from directory (e.g., "cli-analyzer", "docs-analyzer")
- **Description**: Directory-specific research scope
- **Prompt**: Tailored analysis instructions
- **Tools**: Read, Glob, Grep, Bash (as needed)

### Phase 3: Deep Analysis

Each subagent performs:
1. **Structure Mapping** - Document file organization
2. **Code Analysis** - Identify key functions, classes, modules
3. **Pattern Recognition** - Find conventions and idioms
4. **Dependency Tracking** - Map imports and relationships
5. **Documentation Review** - Extract existing docs

### Phase 4: Synthesis

Combine subagent findings into:
- Unified architecture documentation
- Cross-cutting concerns and patterns
- Integration points and workflows
- Knowledge base for future reference

## Best Practices

### Effective Research

1. **Start Broad, Go Deep** - Begin with high-level overview, then drill into specifics
2. **Follow the Code** - Trace execution paths and data flows
3. **Document Decisions** - Capture why things are structured as they are
4. **Identify Gaps** - Note missing documentation or unclear patterns
5. **Preserve Context** - Link related components and explain relationships

### Quality Criteria

Research output should:
- Be **accurate** - Reflect actual code structure and behavior
- Be **comprehensive** - Cover all significant components
- Be **actionable** - Enable others to work with the codebase
- Be **maintainable** - Update easily as code evolves
- Be **discoverable** - Organized for easy navigation

### Common Pitfalls

Avoid:
- **Overwhelming detail** - Focus on significant patterns, not every line
- **Outdated documentation** - Verify findings against current code
- **Isolated analysis** - Show how components relate
- **Assumption-based docs** - Confirm behavior through code inspection

## Example Research Session

```bash
# 1. Execute deep research
/deep-research

# 2. Review generated subagent plan
#    The script will show which subagents will be created

# 3. Confirm execution
#    Claude runs research with specialized subagents

# 4. Review outputs
#    - CLAUDE.md or SKILL.md in project root
#    - references/ directory with detailed documentation
```

## Integration with Existing Skills

This skill complements:
- **skill-creator** - Use research findings to create specialized skills
- **spec-writer** - Research informs specification documents
- **architecture** - Deep analysis feeds architecture documentation

## Technical Notes

### Subagent Spawning

Uses Claude Code's `--agents` flag for programmatic subagent definition:

```bash
claude --agents '{
  "subagent-name": {
    "description": "What this subagent does",
    "prompt": "Detailed instructions",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

### Headless Mode Integration

Can run non-interactively for automation:

```bash
claude -p "Perform deep research on this codebase" \
  --permission-mode plan \
  --output-format json
```

## References

See also:
- [Deep Research Script](scripts/deep_research.sh) - Implementation details
- [Subagent Templates](references/subagent_templates.md) - Example subagent configurations  
- [Research Examples](references/research_examples.md) - Sample outputs