---
name: plugin-creator
description: Creates plugins (skills and MCPs) by guiding through the authoring process. Use when users want to create or update (1) skills that extend Claude's capabilities with specialized knowledge and workflows, or (2) MCPs (Model Context Protocol servers) that provide tools for Claude Desktop.
---

# Plugin Creator

This skill provides guidance for creating plugins that extend Claude's capabilities. Supports two plugin types:

- **Skills**: SKILL.md-based plugins with bundled scripts, references, and assets
- **MCPs**: Server-based plugins that provide tools via the Model Context Protocol

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Claude reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>100 lines), include a table of contents at the top and grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxilary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.

## Plugin Creation Process

Plugin creation involves these steps:

1. Determine plugin type (skill vs MCP)
2. Understand the plugin with concrete examples
3. Plan reusable contents
4. Initialize the plugin (run `tools/init_plugin.py`)
5. Edit the plugin (implement resources and write manifest)
6. Package the plugin (run `tools/package_plugin.py`)
7. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Determining Plugin Type

Choose based on how the plugin will be used:

| Aspect | Skill | MCP |
|--------|-------|-----|
| **Format** | SKILL.md + optional resources | MCP.md + server.py |
| **Invocation** | Claude selects based on description | Tools always available |
| **Use case** | Workflows, procedures, domain knowledge | Persistent tools, external APIs |
| **Examples** | Document processing, code review | Session memory, database queries |

**Choose Skill when**: The plugin provides workflows, domain knowledge, or procedures that Claude should follow for specific tasks.

**Choose MCP when**: The plugin needs to provide tools that are always available, interact with external systems, or maintain persistent state.

### Step 2: Understanding the Plugin with Concrete Examples

Skip this step only when the plugin's usage patterns are already clearly understood.

Clearly understand concrete examples of how the plugin will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

Example questions:
- "What functionality should this plugin support?"
- "Can you give examples of how this would be used?"
- "What would a user say that should trigger this?"

Conclude this step when there is a clear sense of the functionality the plugin should support.

### Step 3: Planning the Reusable Contents

For skills, identify what scripts, references, and assets would be helpful. For MCPs, identify what tools the server should provide.

**Skill examples:**
- `scripts/rotate_pdf.py` - deterministic code for PDF rotation
- `assets/hello-world/` - boilerplate template files
- `references/schema.md` - domain documentation

**MCP examples:**
- Tools for session persistence (save/load state)
- Tools for external API integration
- Tools for database queries

### Step 4: Initializing the Plugin

Skip this step if the plugin already exists and only needs iteration or packaging.

Use `tools/init_plugin.py` to create a new plugin:

```bash
# Create a skill
tools/init_plugin.py skill <plugin-name> --path skills/

# Create an MCP
tools/init_plugin.py mcp <plugin-name> --path mcps/
```

**For skills**, the script creates:
- SKILL.md template with frontmatter
- Example `scripts/`, `references/`, and `assets/` directories

**For MCPs**, the script creates:
- MCP.md manifest with frontmatter
- server.py boilerplate with MCP SDK integration
- config.json for configuration

After initialization, customize or remove the generated files as needed.

### Step 5: Edit the Plugin

Remember that plugins are created for another Claude instance to use. Include information that would be beneficial and non-obvious.

#### For Skills

**Frontmatter (SKILL.md):**
- `name`: hyphen-case, max 64 chars, must match directory name
- `description`: max 1024 chars, include what it does AND when to use it

**Body:** Instructions for using the skill and bundled resources.

See references/workflows.md for design patterns and references/validation-checklist.md before packaging.

#### For MCPs

**Frontmatter (MCP.md):**
- `name`: hyphen-case, max 64 chars, must match directory name
- `description`: max 1024 chars
- `type`: must be "mcp"
- `entry_point`: main Python file (e.g., "server.py")
- `dependencies`: optional list of pip packages
- `config_file`: optional config file path

**Implementation:**
1. Define tools in server.py using MCP SDK
2. Implement tool handlers
3. Test locally before packaging

### Step 6: Packaging the Plugin

Use `tools/package_plugin.py` to create a distributable `.plugin` file:

```bash
tools/package_plugin.py <path/to/plugin-folder> [output-directory]

# Examples
tools/package_plugin.py skills/my-skill
tools/package_plugin.py mcps/my-mcp ./dist
```

**Dependency**: Requires PyYAML (`pip install pyyaml`).

The script:
1. **Validates** the plugin (frontmatter, naming, structure)
2. **Packages** into a `.plugin` file (ZIP format with MANIFEST.json)

For MCPs, after packaging use `tools/install_mcp.py` to install:

```bash
tools/install_mcp.py dist/my-mcp.plugin
# Or for development (symlink):
tools/install_mcp.py mcps/my-mcp --symlink
```

### Step 7: Test and Iterate

**Testing approach:**
1. Define 3+ realistic test scenarios
2. Test with multiple models (Haiku, Sonnet, Opus)
3. Check edge cases and boundary conditions

**For MCPs specifically:**
- Test tools individually before integration
- Verify error handling
- Test with Claude Desktop

**Iteration workflow:**
1. Use on real tasks
2. Notice struggles or inefficiencies
3. Update plugin and test again
