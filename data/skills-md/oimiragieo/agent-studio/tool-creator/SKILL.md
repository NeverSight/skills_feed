---
name: tool-creator
description: Creates tool files for the Claude Code framework. Tools are executable utilities organized by category in .claude/tools/.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash]
args: '--name <tool-name> --category <category> --implementation <code>'
best_practices:
  - Tools are CLI-executable scripts (.cjs or .mjs)
  - Keep tools focused (single responsibility)
  - Add help text and usage examples
  - Include error handling
error_handling: graceful
streaming: supported
output_location: .claude/tools/
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Tool Creator

Create executable tool files in `.claude/tools/<category>/`. Tools are organized into categories like `cli`, `analysis`, `validation`, `integrations`, etc.

## Step 0: Check for Existing Tool

Before creating, check if tool already exists:

```bash
find .claude/tools/ -name "<tool-name>.*" -type f
```

If EXISTS → invoke `Skill({ skill: "artifact-updater", args: "--type tool --path .claude/tools/<category>/<tool-name>.cjs --changes '...'" })`

If NEW → continue with Step 0.5.

## Step 0.5: Companion Check

Before proceeding with creation, run the ecosystem companion check:

1. Use `companion-check.cjs` from `.claude/lib/creators/companion-check.cjs`
2. Call `checkCompanions("tool", "{tool-name}")` to identify companion artifacts
3. Review the companion checklist — note which required/recommended companions are missing
4. Plan to create or verify missing companions after this artifact is complete
5. Include companion findings in post-creation integration notes

This step is **informational** (does not block creation) but ensures the full artifact ecosystem is considered.

## When to Use

- Creating reusable command-line utilities
- Building analysis or validation scripts
- Implementing framework automation tools
- Adding workflow integration utilities

## Tool File Format

Tools are CommonJS or ESM modules with:

```javascript
#!/usr/bin/env node
/**
 * Tool Name - Brief description
 *
 * Usage:
 *   node .claude/tools/<category>/<tool-name>.cjs [options]
 *
 * Options:
 *   --help     Show help
 *   --option   Description
 */

const main = async () => {
  // Tool implementation
};

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main };
```

## Tool Categories

| Category        | Purpose                      | Examples                    |
| --------------- | ---------------------------- | --------------------------- |
| `cli`           | Command-line utilities       | validators, formatters      |
| `analysis`      | Code analysis tools          | complexity, dependencies    |
| `validation`    | Validation scripts           | schema, lint                |
| `integrations`  | External integration tools   | API clients, webhooks       |
| `maintenance`   | Framework maintenance        | cleanup, migration          |
| `optimization`  | Performance optimization     | indexing, caching           |
| `runtime`       | Runtime utilities            | config readers, loaders     |
| `visualization` | Diagram and graph generation | mermaid, graphviz           |
| `workflow`      | Workflow automation          | task runners, orchestrators |
| `gates`         | Quality gates and checks     | coverage, security          |
| `context`       | Context management           | compression, handoff        |

## Creation Workflow

### Step 1: Validate Inputs

```javascript
// Validate tool name (lowercase, hyphens, no spaces)
const toolName = args.name.toLowerCase().replace(/[^a-z0-9-]/g, '-');

// Validate category exists
const validCategories = [
  'cli',
  'analysis',
  'validation',
  'integrations',
  'maintenance',
  'optimization',
  'runtime',
  'visualization',
  'workflow',
  'gates',
  'context',
];

if (!validCategories.includes(args.category)) {
  throw new Error(`Invalid category. Must be one of: ${validCategories.join(', ')}`);
}
```

### Step 2: Create Tool File

```javascript
const toolPath = `.claude/tools/${args.category}/${toolName}.cjs`;

// Create tool directory if it doesn't exist
await mkdir(`.claude/tools/${args.category}`, { recursive: true });

// Generate tool content
const content = `#!/usr/bin/env node
/**
 * ${toolName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} - ${args.description || 'Tool description'}
 *
 * Usage:
 *   node .claude/tools/${args.category}/${toolName}.cjs [options]
 *
 * Options:
 *   --help     Show this help message
 */

${args.implementation}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main };
`;

await writeFile(toolPath, content);

// Make executable (Unix-like systems)
if (process.platform !== 'win32') {
  await chmod(toolPath, '755');
}
```

### Step 3: Update Tool Catalog

```javascript
const catalogPath = '.claude/context/artifacts/catalogs/tool-catalog.md';

// Add entry to catalog under appropriate category
const newEntry = `| ${toolName} | ${args.description} | .claude/tools/${args.category}/${toolName}.cjs | active |`;

// Insert into catalog preserving category structure
```

### Step 4: Run Post-Creation Integration

```javascript
const {
  runIntegrationChecklist,
  queueCrossCreatorReview,
} = require('.claude/lib/creator-commons.cjs');

await runIntegrationChecklist('tool', toolPath);
await queueCrossCreatorReview('tool', toolPath, {
  artifactName: toolName,
  createdBy: 'tool-creator',
  category: args.category,
});
```

## Post-Creation Integration

After tool creation, run integration checklist:

```javascript
const {
  runIntegrationChecklist,
  queueCrossCreatorReview,
} = require('.claude/lib/creator-commons.cjs');

// 1. Run integration checklist
const result = await runIntegrationChecklist('tool', '.claude/tools/<category>/<tool-name>.cjs');

// 2. Queue cross-creator review
await queueCrossCreatorReview('tool', '.claude/tools/<category>/<tool-name>.cjs', {
  artifactName: '<tool-name>',
  createdBy: 'tool-creator',
  category: '<category>',
});

// 3. Review impact report
// Check result.mustHave for failures - address before marking complete
```

**Integration verification:**

- [ ] Tool added to tool-catalog.md under correct category
- [ ] Tool file is executable (Unix) or runnable (Windows)
- [ ] Tool has help text and usage examples
- [ ] Tool passes basic smoke test

## Usage Examples

### Create Validation Tool

```javascript
Skill({
  skill: 'tool-creator',
  args: `--name schema-validator --category validation --implementation "
const validateSchema = async () => {
  console.log('Validating schema...');
};

const main = async () => {
  await validateSchema();
};
"`,
});
```

### Create Analysis Tool

```javascript
Skill({
  skill: 'tool-creator',
  args: `--name complexity-analyzer --category analysis --implementation "
const analyzeComplexity = async (filePath) => {
  console.log('Analyzing complexity for:', filePath);
};

const main = async () => {
  const [,, filePath] = process.argv;
  await analyzeComplexity(filePath);
};
"`,
});
```

## Related Skills

- `skill-creator` - Create skills that invoke tools
- `artifact-updater` - Update existing tools

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New tool pattern → `.claude/context/memory/learnings.md`
- Tool creation issue → `.claude/context/memory/issues.md`
- Category decision → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

## Ecosystem Alignment Contract (MANDATORY)

This creator skill is part of a coordinated creator ecosystem. Any artifact created here must align with and validate against related creators:

- `agent-creator` for ownership and execution paths
- `skill-creator` for capability packaging and assignment
- `tool-creator` for executable automation surfaces
- `hook-creator` for enforcement and guardrails
- `rule-creator` and `semgrep-rule-creator` for policy and static checks
- `template-creator` for standardized scaffolds
- `workflow-creator` for orchestration and phase gating
- `command-creator` for user/operator command UX

### Cross-Creator Handshake (Required)

Before completion, verify all relevant handshakes:

1. Artifact route exists in `.claude/CLAUDE.md` and related routing docs.
2. Discovery/registry entries are updated (catalog/index/registry as applicable).
3. Companion artifacts are created or explicitly waived with reason.
4. `validate-integration.cjs` passes for the created artifact.
5. Skill index is regenerated when skill metadata changes.

### Research Gate (Exa First, arXiv Fallback)

For new patterns, templates, or workflows, research is mandatory:

1. Use Exa first for implementation and ecosystem patterns.
2. If Exa is insufficient, use `WebFetch` plus arXiv references.
3. Record decisions, constraints, and non-goals in artifact references/docs.
4. Keep updates minimal and avoid overengineering.

### Regression-Safe Delivery

- Follow strict RED -> GREEN -> REFACTOR for behavior changes.
- Run targeted tests for changed modules.
- Run lint/format on changed files.
- Keep commits scoped by concern (logic/docs/generated artifacts).
