---
name: skill-creator
description: Create, validate, and convert skills for the agent ecosystem. Enforces standardized structure for consistency. Enables self-evolution by creating new skills on demand, converting MCP servers and codebases to skills.
version: 2.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch]
args: '<action> [options]'
best_practices:
  - Always use standardized structure
  - Include Memory Protocol section
  - Create scripts/main.cjs for executable logic
  - Validate after creation
error_handling: graceful
streaming: supported
---

# Skill Creator

Create, validate, install, and convert skills for the multi-agent ecosystem.

## ROUTER UPDATE REQUIRED (CRITICAL - DO NOT SKIP)

**After creating ANY skill, you MUST update:**

```
1. CLAUDE.md - Add to Section 8.5 "WORKFLOW ENHANCEMENT SKILLS" if user-invocable
2. Skill Catalog - Add to .claude/context/artifacts/skill-catalog.md
3. learnings.md - Update with integration summary
```

**Verification:**

```bash
grep "<skill-name>" .claude/CLAUDE.md || echo "ERROR: CLAUDE.md NOT UPDATED!"
grep "<skill-name>" .claude/context/artifacts/skill-catalog.md || echo "ERROR: Skill catalog NOT UPDATED!"
```

**WHY**: Skills not in CLAUDE.md are invisible to the Router. Skills not in the catalog are hard to discover.

---

## Purpose

Enable self-healing and evolving agent ecosystem by:

1. Creating new skills from scratch based on requirements
2. Converting MCP (Model Context Protocol) servers to skills
3. Installing skills from GitHub repositories
4. Validating skill definitions
5. Assigning skills to new or existing agents

## Actions

### `create` - Create a New Skill

Create a skill from scratch with proper structure.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "my-skill" \
  --description "What this skill does" \
  --tools "Read,Write,WebSearch" \
  [--refs]              # Create references/ directory
  [--hooks]             # Create hooks/ directory with pre/post execute
  [--schemas]           # Create schemas/ directory with input/output schemas
  [--register-hooks]    # Also register hooks in settings.json
  [--register-schemas]  # Also register schemas globally
  [--create-tool]       # Force creation of companion CLI tool
  [--no-tool]           # Skip companion tool even if complex
```

**Automatic Tool Creation:**

Complex skills automatically get a companion tool in `.claude/tools/`. A skill is considered complex when it has 2+ of:

- Pre/post execution hooks
- Input/output schemas
- 6+ tools specified
- Command-line arguments
- Description with complex keywords (orchestration, pipeline, workflow, etc.)

**Examples:**

```bash
# Basic skill
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "pdf-extractor" \
  --description "Extract text and images from PDF documents" \
  --tools "Read,Write,Bash"

# Skill with hooks and schemas (auto-creates tool)
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "data-validator" \
  --description "Validate and sanitize data inputs before processing" \
  --hooks --schemas

# Skill with hooks registered immediately
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "security-check" \
  --description "Security validation hook for all operations" \
  --hooks --register-hooks

# Force tool creation for a simple skill
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "simple-util" \
  --description "A simple utility that needs CLI access" \
  --create-tool

# Skip tool for a complex skill
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "complex-internal" \
  --description "Complex integration without external CLI" \
  --hooks --schemas --no-tool
```

### `convert` - Convert MCP Server to Skill

Convert an MCP server (npm, PyPI, or Docker) into a Claude Code skill.

**IMPORTANT: Auto-Registration Enabled**

When converting MCP servers, the skill-creator automatically:

1. Creates the skill definition (SKILL.md)
2. **Registers the MCP server in settings.json** (no user action needed)
3. Assigns skill to relevant agents
4. Updates CLAUDE.md and skill catalog

```bash
node .claude/skills/skill-creator/scripts/convert.cjs \
  --server "server-name" \
  [--source npm|pypi|docker|github] \
  [--test]  # Test the converted skill
  [--no-register]  # Skip auto-registration in settings.json
```

**Known MCP Servers (Auto-detected):**

| Server                                  | Source | Description                 |
| --------------------------------------- | ------ | --------------------------- |
| @anthropic/mcp-shell                    | npm    | Shell command execution     |
| @modelcontextprotocol/server-filesystem | npm    | File system operations      |
| @modelcontextprotocol/server-memory     | npm    | Knowledge graph memory      |
| @modelcontextprotocol/server-github     | npm    | GitHub API integration      |
| @modelcontextprotocol/server-slack      | npm    | Slack messaging             |
| mcp-server-git                          | pypi   | Git operations              |
| mcp-server-time                         | pypi   | Time and timezone utilities |
| mcp-server-sentry                       | pypi   | Sentry error tracking       |
| mcp/github                              | docker | Official GitHub MCP         |
| mcp/playwright                          | docker | Browser automation          |

**Example:**

```bash
# Convert npm MCP server
node .claude/skills/skill-creator/scripts/convert.cjs \
  --server "@modelcontextprotocol/server-filesystem"

# Convert PyPI server
node .claude/skills/skill-creator/scripts/convert.cjs \
  --server "mcp-server-git" --source pypi

# Convert from GitHub
node .claude/skills/skill-creator/scripts/convert.cjs \
  --server "https://github.com/owner/mcp-server" --source github
```

### MCP-to-Skill Conversion (PREFERRED APPROACH)

**BEFORE adding an MCP server, check if existing tools can do the same job!**

Many MCP servers are just API wrappers. Using existing tools (WebFetch, Exa) is **preferred** because:

| MCP Server Approach                  | Skill with Existing Tools |
| ------------------------------------ | ------------------------- |
| ❌ Requires uvx/npm/pip installation | ✅ Works immediately      |
| ❌ Requires session restart          | ✅ No restart needed      |
| ❌ External dependency failures      | ✅ Self-contained         |
| ❌ Platform-specific issues          | ✅ Cross-platform         |

**Example: arXiv - Use WebFetch instead of mcp-arxiv server**

```javascript
// INSTEAD of requiring mcp-arxiv server, use WebFetch directly:
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=ti:transformer&max_results=10',
  prompt: 'Extract paper titles, authors, abstracts',
});

// Or use Exa for semantic search:
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org transformer attention mechanism',
  numResults: 10,
});
```

**When to use existing tools (PREFERRED):**

- MCP server wraps a public REST API
- No authentication required
- Simple request/response patterns

**When MCP server is actually needed:**

- Complex state management required
- Streaming/websocket connections
- Local file system access needed
- OAuth/authentication flows required

### MCP Server Auto-Registration (ONLY IF NECESSARY)

**If existing tools won't work and MCP server is truly required, you MUST register it.**

This ensures users don't need to manually configure MCP servers - skills "just work".

#### Step 10: Register MCP Server in settings.json (BLOCKING for MCP skills)

If your skill uses tools prefixed with `mcp__<server>__*`, add the server to `.claude/settings.json`:

1. **Determine the MCP server config** based on source:

   | Source | Config Template                                             |
   | ------ | ----------------------------------------------------------- |
   | npm    | `{ "command": "npx", "args": ["-y", "<package-name>"] }`    |
   | PyPI   | `{ "command": "uvx", "args": ["<package-name>"] }`          |
   | Docker | `{ "command": "docker", "args": ["run", "-i", "<image>"] }` |

2. **Read current settings.json:**

   ```bash
   cat .claude/settings.json
   ```

3. **Add mcpServers section if missing, or add to existing:**

   ```json
   {
     "mcpServers": {
       "<server-name>": {
         "command": "<command>",
         "args": ["<args>"]
       }
     }
   }
   ```

4. **Verify registration:**
   ```bash
   grep "<server-name>" .claude/settings.json || echo "ERROR: MCP not registered!"
   ```

#### Known MCP Server Configurations

| Server Name | Package                                 | Source | Config                                                                            |
| ----------- | --------------------------------------- | ------ | --------------------------------------------------------------------------------- |
| arxiv       | mcp-arxiv                               | PyPI   | `{ "command": "uvx", "args": ["mcp-arxiv"] }`                                     |
| filesystem  | @modelcontextprotocol/server-filesystem | npm    | `{ "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem"] }` |
| memory      | @modelcontextprotocol/server-memory     | npm    | `{ "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] }`     |
| github      | @modelcontextprotocol/server-github     | npm    | `{ "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"] }`     |
| slack       | @modelcontextprotocol/server-slack      | npm    | `{ "command": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"] }`      |
| git         | mcp-server-git                          | PyPI   | `{ "command": "uvx", "args": ["mcp-server-git"] }`                                |
| time        | mcp-server-time                         | PyPI   | `{ "command": "uvx", "args": ["mcp-server-time"] }`                               |
| sentry      | mcp-server-sentry                       | PyPI   | `{ "command": "uvx", "args": ["mcp-server-sentry"] }`                             |

#### Iron Law: NO MCP SKILL WITHOUT SERVER REGISTRATION

```
+======================================================================+
|  ⛔ MCP REGISTRATION IRON LAW - VIOLATION = BROKEN SKILL             |
+======================================================================+
|                                                                      |
|  If skill uses tools matching: mcp__<server>__*                      |
|  Then MUST add to .claude/settings.json mcpServers                   |
|                                                                      |
|  WITHOUT registration:                                               |
|    - Tools appear in skill definition                                |
|    - But tools don't exist at runtime                                |
|    - Skill invocation FAILS silently                                 |
|                                                                      |
|  BLOCKING: MCP skills are INCOMPLETE without server registration     |
|                                                                      |
+======================================================================+
```

### `validate` - Validate Skill Definition

Check a skill's SKILL.md for correctness.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --validate ".claude/skills/my-skill"
```

### `install` - Install Skill from GitHub

Clone and install a skill from a GitHub repository.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --install "https://github.com/owner/claude-skill-name"
```

### `convert-codebase` - Convert External Codebase to Skill

Convert any external codebase to a standardized skill structure.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-codebase "/path/to/codebase" \
  --name "new-skill-name"
```

**What it does:**

1. Analyzes codebase structure (package.json, README, src/, lib/)
2. Extracts description from package.json or README
3. Finds entry points (index.js, main.js, cli.js)
4. Creates standardized skill structure
5. Copies original files to references/ for integration
6. Runs `pnpm format` on all created files

**Example:**

```bash
# Convert a local tool to a skill
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-codebase "./my-custom-tool" \
  --name "custom-tool"

# The resulting structure:
# .claude/skills/custom-tool/
# ├── SKILL.md (standardized)
# ├── scripts/
# │   └── main.cjs (template + integrate original logic)
# └── references/
#     ├── original-entry.js
#     └── original-README.md
```

### `consolidate` - Consolidate Skills into Domain Experts

Consolidate granular skills into domain-based expert skills to reduce context overhead.

```bash
# Analyze consolidation opportunities
node .claude/skills/skill-creator/scripts/consolidate.cjs

# Preview with all skill details
node .claude/skills/skill-creator/scripts/consolidate.cjs --verbose

# Execute consolidation (keeps source skills)
node .claude/skills/skill-creator/scripts/consolidate.cjs --execute

# Execute and remove source skills
node .claude/skills/skill-creator/scripts/consolidate.cjs --execute --remove

# List all domain buckets
node .claude/skills/skill-creator/scripts/consolidate.cjs --list-buckets
```

**What it does:**

1. Groups skills by technology domain (react, python, go, etc.)
2. Creates consolidated "expert" skills with merged guidelines
3. Preserves source skill references in `references/source-skills.json`
4. Optionally removes source skills after consolidation
5. Updates memory with consolidation summary

**Domain Buckets:**

| Bucket                   | Description                           |
| ------------------------ | ------------------------------------- |
| `react-expert`           | React, Shadcn, Radix                  |
| `python-backend-expert`  | Django, FastAPI, Flask                |
| `nextjs-expert`          | Next.js App Router, Server Components |
| `typescript-expert`      | TypeScript, JavaScript                |
| `general-best-practices` | Naming, error handling, docs          |
| ...                      | 40+ total buckets                     |

### `convert-rules` - Convert Legacy Rules to Skills

Convert old rule files (.mdc, .md) from legacy rule libraries into standardized skills.

```bash
# Convert a single rule file
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-rule "/path/to/rule.mdc"

# Convert all rules in a directory
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-rules "/path/to/rules-library"

# Force overwrite existing skills
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-rules "/path/to/rules" --force
```

**What it does:**

1. Parses `.mdc` or `.md` rule files with YAML frontmatter
2. Extracts description and globs from frontmatter
3. Creates a skill with embedded guidelines in `<instructions>` block
4. Copies original rule file to `references/`
5. Creates `scripts/main.cjs` for CLI access
6. Updates memory with conversion summary

**Example:**

```bash
# Convert legacy cursorrules to skills
node .claude/skills/skill-creator/scripts/create.cjs \
  --convert-rules ".claude.archive/rules-library"
```

### `assign` - Assign Skill to Agent

Add a skill to an existing or new agent's configuration.

```bash
# Assign to existing agent
node .claude/skills/skill-creator/scripts/create.cjs \
  --assign "skill-name" --agent "developer"

# Create new agent with skill
node .claude/tools/agent-creator/create-agent.mjs \
  --name "pdf-specialist" \
  --description "PDF processing expert" \
  --skills "pdf-extractor,doc-generator"
```

### `register-hooks` - Register Existing Skill's Hooks

Register a skill's hooks in settings.json for an existing skill.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --register-hooks "skill-name"
```

This adds the skill's pre-execute and post-execute hooks to `.claude/settings.json`.

### `register-schemas` - Register Existing Skill's Schemas

Register a skill's schemas globally for an existing skill.

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --register-schemas "skill-name"
```

This copies the skill's input/output schemas to `.claude/schemas/` for global access.

### `show-structure` - View Standardized Structure

Display the required skill structure documentation.

```bash
node .claude/skills/skill-creator/scripts/create.cjs --show-structure
```

## Workflow: User Requests New Capability

When a user requests a capability that doesn't exist:

```text
User: "I need to analyze sentiment in customer feedback"

[ROUTER] Checking existing skills...
[ROUTER] No sentiment analysis skill found
[ROUTER] ➡️ Handoff to SKILL-CREATOR

[SKILL-CREATOR] Creating new skill...
1. Research: WebSearch "sentiment analysis API MCP server 2026"
2. Found: @modelcontextprotocol/server-sentiment (hypothetical)
3. Converting MCP server to skill...
4. Created: .claude/skills/sentiment-analyzer/SKILL.md
5. Assigning to agent: developer (or creating new agent)

[DEVELOPER] Now using sentiment-analyzer skill...
```

## Workflow: Convert MCP Tool Request

When user wants to use an MCP server:

```text
User: "Add the Slack MCP server so I can send messages"

[SKILL-CREATOR] Converting MCP server...
1. Detected: @modelcontextprotocol/server-slack (npm)
2. Verifying package exists...
3. Generating skill definition...
4. Creating executor script...
5. Testing connection...
6. Created: .claude/skills/slack-mcp/SKILL.md

[ROUTER] Skill available. Which agent should use it?
```

## Skill Definition Format

Skills use YAML frontmatter in SKILL.md:

```yaml
---
name: skill-name
description: What the skill does
invoked_by: user | agent | both
user_invocable: true | false
tools: [Read, Write, Bash, ...]
args: "<required> [optional]"
---

# Skill Name

## Purpose
What this skill accomplishes.

## Usage
How to invoke and use the skill.

## Examples
Concrete usage examples.
```

## Directory Structure

```
.claude/
├── skills/
│   ├── skill-creator/
│   │   ├── SKILL.md           # This file
│   │   ├── scripts/
│   │   │   ├── create.cjs     # Skill creation tool
│   │   │   └── convert.cjs    # MCP conversion tool
│   │   └── references/
│   │       └── mcp-servers.json  # Known MCP servers database
│   └── [other-skills]/
│       ├── SKILL.md
│       ├── scripts/
│       ├── hooks/             # Optional pre/post execute hooks
│       └── schemas/           # Optional input/output schemas
├── tools/                     # Companion tools for complex skills
│   └── [skill-name]/
│       ├── [skill-name].cjs   # CLI wrapper script
│       └── README.md          # Tool documentation
└── workflows/                 # Auto-generated workflow examples
    └── [skill-name]-skill-workflow.md
```

## Output Locations

- New skills: `.claude/skills/[skill-name]/`
- Companion tools: `.claude/tools/[skill-name]/`
- Converted MCP skills: `.claude/skills/[server-name]-mcp/`
- Workflow examples: `.claude/workflows/[skill-name]-skill-workflow.md`
- **Skill catalog**: `.claude/context/artifacts/skill-catalog.md` (MUST UPDATE)
- Memory updates: `.claude/context/memory/learnings.md`
- Logs: `.claude/context/tmp/skill-creator.log`

## File Placement & Standards

### Output Location Rules

This skill outputs to: `.claude/skills/<skill-name>/`

Each skill directory should contain:

- `SKILL.md` - Main skill definition file
- `scripts/` - Executable logic (optional)
- `schemas/` - Input/output validation schemas (optional)
- `hooks/` - Pre/post execution hooks (optional)
- `references/` - Reference materials (optional)

### Mandatory References

- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement

File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previously created skills
- Known MCP server issues
- User preferences for skill configuration

**After completing:**

- New skill created -> Append to `.claude/context/memory/learnings.md`
- Conversion issue -> Append to `.claude/context/memory/issues.md`
- Architecture decision -> Append to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

---

## MANDATORY POST-CREATION STEPS (BLOCKING)

After creating ANY skill file, you MUST complete these steps in order. Skill creation is INCOMPLETE until all steps pass.

### Step 6: Update CLAUDE.md Skill Documentation (MANDATORY - BLOCKING)

This step is AUTOMATIC and BLOCKING. Do not skip.

1. **Determine skill section based on type:**
   - User-invocable workflow skills -> Section 8.5 (WORKFLOW ENHANCEMENT SKILLS)
   - Enterprise workflows -> Section 8.6 (ENTERPRISE WORKFLOWS)
   - Domain/expert skills -> Section 8.7 (AUTO-CLAUDE INTEGRATED SKILLS or create new section)
   - Infrastructure/tool skills -> Add to appropriate subsection

2. **Generate skill entry in this exact format:**

````markdown
### {Skill Name (Title Case)}

Use when {trigger condition}:

```javascript
Skill({ skill: '{skill-name}' });
```
````

{Brief description of what the skill does in 1-2 sentences.}

````

3. **Insert in appropriate section using Edit tool:**
   - Find the end of the target section (before the next ## heading)
   - Insert the new skill entry

4. **Verify update with:**
```bash
grep "{skill-name}" .claude/CLAUDE.md || echo "ERROR: CLAUDE.md NOT UPDATED - BLOCKING!"
````

**BLOCKING**: If CLAUDE.md update fails or skill is not found, skill creation is INCOMPLETE. Do not proceed.

### Step 7: Assign to Relevant Agents (MANDATORY - BLOCKING)

Based on skill domain and purpose, auto-assign to matching agents.

1. **Analyze skill keywords and domain** from name and description
2. **Find matching agents** in `.claude/agents/` using the relevance matrix below
3. **For each matching agent:**
   a. Read agent file
   b. Check if agent has YAML frontmatter with `skills:` array
   c. Add skill to `skills:` array if not present
   d. Update agent file using Edit tool
4. **Record assignments** in skill's SKILL.md under "Assigned Agents" section

**Matching Rules:**

| Skill Domain  | Keywords                                   | Assign To Agents                 |
| ------------- | ------------------------------------------ | -------------------------------- |
| Testing       | tdd, test, qa, validate                    | qa, developer                    |
| Security      | security, audit, compliance, vulnerability | security-architect, developer    |
| Planning      | plan, design, architect, analyze           | planner, architect               |
| Coding        | code, implement, refactor, debug           | developer, all domain-pro agents |
| Documentation | doc, write, readme, comment                | technical-writer, planner        |
| DevOps        | deploy, docker, k8s, terraform, ci, cd     | devops, devops-troubleshooter    |
| Git/GitHub    | git, github, commit, pr, branch            | developer, devops                |
| Communication | slack, notify, alert, message              | incident-responder               |
| Database      | sql, database, migration, schema           | database-architect, developer    |
| API           | api, rest, graphql, endpoint               | developer, architect             |

**Example agent update:**

```yaml
# Before
skills: [tdd, debugging]

# After
skills: [tdd, debugging, new-skill-name]
```

**BLOCKING**: At least one agent must be assigned. Unassigned skills are never invoked.

### Step 8: Update Skill Catalog (MANDATORY - BLOCKING)

Update the skill catalog to ensure the new skill is discoverable.

1. **Read current catalog:**

   ```bash
   cat .claude/context/artifacts/skill-catalog.md
   ```

2. **Determine skill category** based on domain:
   - Core Development (tdd, debugging, code-analyzer)
   - Planning & Architecture (plan-generator, architecture-review)
   - Security (security-architect, auth-security-expert)
   - DevOps (devops, container-expert, terraform-infra)
   - Languages (python-pro, rust-pro, golang-pro, etc.)
   - Frameworks (nextjs-pro, sveltekit-expert, fastapi-pro)
   - Mobile (ios-pro, expo-mobile-developer, android-expert)
   - Data (data-engineer, database-architect, text-to-sql)
   - Documentation (doc-generator, technical-writer)
   - Git & Version Control (git-expert, gitflow, commit-validator)
   - Code Style & Quality (code-quality-expert, code-style-validator)
   - Creator Tools (agent-creator, skill-creator, hook-creator)
   - Memory & Context (session-handoff, context-compressor)
   - Validation & Quality (qa-workflow, verification-before-completion)
   - Specialized Patterns (other domain-specific skills)

3. **Add skill entry to appropriate category table:**

   ```markdown
   | {skill-name} | {description} | {tools} |
   ```

4. **Update catalog Quick Reference** (top of file) if new category or significant skill.

5. **Verify update:**
   ```bash
   grep "{skill-name}" .claude/context/artifacts/skill-catalog.md || echo "ERROR: Skill catalog NOT UPDATED!"
   ```

**BLOCKING**: Skill must appear in catalog. Uncataloged skills are hard to discover.

### Step 9: System Impact Analysis (BLOCKING - VERIFICATION CHECKLIST)

**BLOCKING**: If ANY item fails, skill creation is INCOMPLETE. Fix all issues before proceeding.

Before marking skill creation complete, verify ALL items:

- [ ] **SKILL.md created** with valid YAML frontmatter (name, description, version, tools)
- [ ] **SKILL.md has Memory Protocol section** (copy from template if missing)
- [ ] **CLAUDE.md updated** with skill documentation (verify with grep)
- [ ] **Skill catalog updated** with skill entry (verify with grep)
- [ ] **At least one agent assigned** skill in frontmatter (verify with grep)
- [ ] **learnings.md updated** with creation record
- [ ] **Reference skill comparison** completed (compare against tdd/SKILL.md)
- [ ] **Model validation passed** (if skill spawns agents, model = haiku|sonnet|opus only)
- [ ] **Tools array validated** (no MCP tools unless whitelisted)

**Model Validation (CRITICAL):**

- If skill spawns agents, model field MUST be base name only: `haiku`, `sonnet`, or `opus`
- DO NOT use dated versions like `claude-opus-4-5-20251101`
- Skills themselves don't have models, but skill templates that generate agents must validate this

**Tools Array Validation:**

- Standard tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, TaskUpdate, TaskList, TaskCreate, TaskGet, Skill
- DO NOT add MCP tools (mcp\_\_\*) to skill outputs unless whitelisted
- MCP tools cause router enforcement failures

**Verification Commands:**

```bash
# Check SKILL.md exists and has frontmatter
head -20 .claude/skills/{skill-name}/SKILL.md | grep "^name:"

# Check CLAUDE.md has skill
grep "{skill-name}" .claude/CLAUDE.md

# Check skill catalog has skill
grep "{skill-name}" .claude/context/artifacts/skill-catalog.md

# Check agents have skill assigned
grep -r "{skill-name}" .claude/agents/

# Check learnings.md updated
tail -20 .claude/context/memory/learnings.md | grep "{skill-name}"
```

**BLOCKING**: All checkboxes must pass. If any fail, skill creation is INCOMPLETE.

---

## Workflow Integration

This skill is part of the unified artifact lifecycle. For complete multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- How the Router discovers and invokes this skill's artifacts

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Discovery, creation, update, deprecation phases
- Version management and registry updates
- CLAUDE.md integration requirements

**External Integration:** `.claude/workflows/core/external-integration.md`

- Safe integration of external artifacts
- Security review and validation phases

---

## Reference Skill

**Use `.claude/skills/tdd/SKILL.md` as the canonical reference skill.**

Before finalizing any skill, compare against tdd structure:

- [ ] Has all sections tdd has (Overview, When to Use, Iron Law, etc.)
- [ ] YAML frontmatter is complete (name, description, version, model, invoked_by, user_invocable, tools)
- [ ] Has Memory Protocol section (MANDATORY)
- [ ] Has proper invocation examples
- [ ] Has best_practices in frontmatter
- [ ] Has error_handling field

**Quick Comparison:**

```bash
# Compare your skill structure against tdd
diff <(grep "^## " .claude/skills/tdd/SKILL.md) <(grep "^## " .claude/skills/{skill-name}/SKILL.md)
```

---

## Cross-Reference: Creator Ecosystem

This skill is part of the Creator Ecosystem. After creating a skill, consider if companion artifacts are needed:

| Need                      | Creator to Invoke  | Command                                  |
| ------------------------- | ------------------ | ---------------------------------------- |
| Dedicated agent for skill | `agent-creator`    | `Skill({ skill: "agent-creator" })`      |
| Validation hooks          | `hook-creator`     | Create hooks in `.claude/hooks/`         |
| Workflow orchestration    | `workflow-creator` | Create workflow in `.claude/workflows/`  |
| Code templates            | `template-creator` | Create templates in `.claude/templates/` |
| Input/output validation   | `schema-creator`   | Create schemas in `.claude/schemas/`     |

**Chain Example:**

```text
[SKILL-CREATOR] Created: sentiment-analyzer skill
[SKILL-CREATOR] This skill needs a dedicated agent...
[SKILL-CREATOR] -> Invoking agent-creator to create sentiment-analyst agent
[AGENT-CREATOR] Created: sentiment-analyst agent with sentiment-analyzer skill
```

**Integration Verification:**

After using companion creators, verify the full chain:

```bash
# Verify skill exists
ls .claude/skills/{skill-name}/SKILL.md

# Verify agent exists (if created)
ls .claude/agents/*/{agent-name}.md

# Verify workflow exists (if created)
ls .claude/workflows/*{skill-name}*.md

# Verify all are in CLAUDE.md
grep -E "{skill-name}|{agent-name}" .claude/CLAUDE.md
```

---

## Iron Laws of Skill Creation

These rules are INVIOLABLE. Breaking them causes bugs that are hard to detect.

```
1. NO SKILL WITHOUT VALIDATION FIRST
   - Run validate-all.cjs after creating ANY skill
   - If validation fails, fix before proceeding

2. NO FILE REFERENCES WITHOUT VERIFICATION
   - Every .claude/tools/*.mjs reference must point to existing file
   - Every .claude/skills/*/SKILL.md reference must exist
   - Check with: ls <path> before committing

3. NO MULTI-LINE YAML DESCRIPTIONS
   - description: | causes parsing failures
   - Always use single-line: description: "My description here"

4. NO SKILL WITHOUT MEMORY PROTOCOL
   - Every skill MUST have Memory Protocol section
   - Agents forget everything without it

5. NO CREATION WITHOUT AGENT ASSIGNMENT
   - Skill must be added to at least one agent's skills array
   - Unassigned skills are never invoked

6. NO CREATION WITHOUT CATALOG UPDATE
   - Skill must be added to .claude/context/artifacts/skill-catalog.md
   - Uncataloged skills are hard to discover
   - Add to correct category table with description and tools

7. NO CREATION WITHOUT SYSTEM IMPACT ANALYSIS
   - Check if skill requires new routes in CLAUDE.md
   - Check if skill requires new agent (spawn agent-creator if yes)
   - Check if existing workflows need updating
   - Check if router.md agent table needs updating
   - Document all system changes made

8. NO SKILL WITHOUT REFERENCE COMPARISON
   - Compare against tdd/SKILL.md before finalizing
   - Ensure all standard sections are present
   - Verify frontmatter completeness
   - Check Memory Protocol section exists

9. NO SKILL TEMPLATES WITH MCP TOOLS
   - Unless tools are whitelisted in router-enforcer.cjs
   - MCP tools (mcp__*) cause routing failures
   - Standard tools only: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, TaskUpdate, TaskList, TaskCreate, TaskGet, Skill

10. NO SKILL WITHOUT SYSTEM IMPACT ANALYSIS
    - Update CLAUDE.md Section 7 if skill adds new capability
    - Update skill-catalog.md with proper categorization
    - Update creator-registry.json if skill is a creator
    - Verify routing keywords if skill introduces new domain

11. PREFER EXISTING TOOLS OVER MCP SERVERS
    - FIRST: Check if WebFetch/Exa can access the same API directly
    - Many MCP servers are just API wrappers - use WebFetch instead!
    - Existing tools work immediately (no uvx/npm, no restart)
    - ONLY IF existing tools won't work: register MCP server
    - See "MCP-to-Skill Conversion" section for guidance
```

## System Impact Analysis (MANDATORY)

**After creating ANY skill, you MUST analyze and update system-wide impacts.**

### Impact Checklist

Run this analysis after every skill creation:

```
[SKILL-CREATOR] 🔍 System Impact Analysis for: <skill-name>

1. ROUTING TABLE CHECK
   - Does this skill introduce a new capability type?
   - Is there an agent that can use this skill?
   - If NO agent exists → spawn agent-creator to create one
   - If new agent created → update CLAUDE.md routing table

2. AGENT ASSIGNMENT CHECK
   - Which existing agents should have this skill?
   - Update each agent's skills: array
   - Update each agent's "Step 0: Load Skills" section

3. ROUTER UPDATE CHECK
   - Does router.md know about this capability?
   - Update router.md Core/Specialized/Domain agent tables if needed
   - Update Planning Orchestration Matrix if needed

4. WORKFLOW CHECK
   - Do any existing workflows reference this capability?
   - Should a new workflow be created?
   - Update .claude/workflows/ as needed

5. RELATED ARTIFACTS CHECK
   - Are there dependent skills that need updating?
   - Are there hooks that should be registered?
   - Are there commands that should be added?
```

### Example: Creating a "writing" Skill

```
[SKILL-CREATOR] ✅ Created: .claude/skills/writing/SKILL.md

[SKILL-CREATOR] 🔍 System Impact Analysis...

1. ROUTING TABLE CHECK
   ❌ No agent handles "documentation" or "writing" tasks
   → Spawning agent-creator to create technical-writer agent
   → Adding to CLAUDE.md: | Documentation, docs | technical-writer | ...

2. AGENT ASSIGNMENT CHECK
   ✅ Assigned to: technical-writer, planner (for plan documentation)

3. ROUTER UPDATE CHECK
   ✅ Updated router.md Core Agents table
   ✅ Added row to Planning Orchestration Matrix

4. WORKFLOW CHECK
   ✅ Created: .claude/workflows/documentation-workflow.md

5. RELATED ARTIFACTS CHECK
   ✅ No dependent skills
   ✅ No hooks needed
```

### System Update Commands

```bash
# Check if routing table needs update
grep -i "<capability-keyword>" .claude/CLAUDE.md || echo "NEEDS ROUTE"

# Check router agent tables
grep -i "<capability-keyword>" .claude/agents/core/router.md || echo "NEEDS ROUTER UPDATE"

# Check for related workflows
ls .claude/workflows/*<keyword>* 2>/dev/null || echo "MAY NEED WORKFLOW"

# Verify all system changes
node .claude/tools/validate-agents.mjs
node .claude/skills/skill-creator/scripts/validate-all.cjs
```

### Validation Checklist (Run After Every Creation)

```bash
# Validate the new skill
node .claude/skills/skill-creator/scripts/validate-all.cjs | grep "<skill-name>"

# Check for broken pointers
grep -r ".claude/tools/" .claude/skills/<skill-name>/ | while read line; do
  file=$(echo "$line" | grep -oE '\.claude/tools/[^"]+')
  [ -f "$file" ] || echo "BROKEN: $file"
done

# Verify agent assignment
grep -l "<skill-name>" .claude/agents/**/*.md || echo "WARNING: Not assigned to any agent"
```

## Post-Creation: Auto-Assign to Relevant Agents (CRITICAL)

**After creating any skill, you MUST update relevant agents to include the new skill.**

### Why This Matters

Agents only use skills that are:

1. Listed in their frontmatter `skills:` array
2. Explicitly loaded in their workflow

If you create a skill but don't assign it to agents, the skill will never be used.

### Auto-Assignment Workflow

After creating a skill, execute this workflow:

```text
[SKILL-CREATOR] ✅ Skill created: .claude/skills/<skill-name>/SKILL.md

[SKILL-CREATOR] 🔍 Finding relevant agents to update...
1. Scan agents: Glob .claude/agents/**/*.md
2. For each agent, check if skill domain matches:
   - Developer: code, testing, debugging, git skills
   - Planner: planning, analysis, documentation skills
   - Architect: architecture, design, diagramming skills
   - Security-Architect: security, compliance, audit skills
   - DevOps: infrastructure, deployment, monitoring skills
   - QA: testing, validation, coverage skills

[SKILL-CREATOR] 📝 Updating agents...
- Edit agent frontmatter to add skill to `skills:` array
- Ensure agent workflow references skill loading

[SKILL-CREATOR] ✅ Updated: developer, qa
```

### Agent-Skill Relevance Matrix

| Skill Domain                                | Relevant Agents                  |
| ------------------------------------------- | -------------------------------- |
| Testing (tdd, test-\*)                      | developer, qa                    |
| Debugging (debug*, troubleshoot*)           | developer, devops-troubleshooter |
| Documentation (doc-_, diagram-_)            | planner, architect               |
| Security (_security_, audit*, compliance*)  | security-architect               |
| Infrastructure (docker*, k8s*, terraform\*) | devops                           |
| Code Quality (lint*, style*, analyze\*)     | developer, architect             |
| Git/GitHub (git*, github*)                  | developer                        |
| Planning (plan*, sequential*)               | planner                          |
| Architecture (architect*, design*)          | architect                        |
| Communication (slack*, notification*)       | incident-responder               |

### Implementation

When creating a skill:

```bash
# 1. Create the skill
node .claude/skills/skill-creator/scripts/create.cjs \
  --name "new-skill" --description "..."

# 2. Auto-assign to relevant agents (built into create.cjs)
# The script will:
#   - Analyze skill name and description
#   - Find matching agents from the matrix
#   - Update their frontmatter
#   - Add skill loading to workflow if needed
```

### Manual Assignment

If auto-assignment misses an agent:

```bash
node .claude/skills/skill-creator/scripts/create.cjs \
  --assign "skill-name" --agent "agent-name"
```

This updates:

1. Agent's `skills:` frontmatter array
2. Agent's workflow to include skill loading step

### Skill Loading in Updated Agents

When updating an agent, ensure their workflow includes:

```markdown
### Step 0: Load Skills (FIRST)

Read your assigned skill files to understand specialized workflows:

- `.claude/skills/<skill-1>/SKILL.md`
- `.claude/skills/<skill-2>/SKILL.md`
- `.claude/skills/<new-skill>/SKILL.md` # Newly added
```

## Integration with Agent Creator

The skill-creator works with agent-creator for full ecosystem evolution:

1. **New Capability Request** → skill-creator creates skill
2. **Auto-Assign** → skill-creator updates relevant agents with new skill
3. **No Matching Agent** → agent-creator creates agent (with skill auto-discovery)
4. **Execute Task** → Agent loads skills and handles request

This enables a self-healing, self-evolving agent ecosystem where:

- New skills are automatically distributed to relevant agents
- New agents automatically discover and include relevant skills
- Both intake paths ensure skills are properly loaded and used
