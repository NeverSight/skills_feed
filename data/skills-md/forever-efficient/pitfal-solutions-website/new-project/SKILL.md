---
name: new-project
description: Initialize a new project with the standard Claude Code structure. Creates CLAUDE.md, PRD, architecture docs, MCP config, skills, and settings. Use when starting any new project.
---

# Initialize New Project

**IMPORTANT:** Every project gets the same skeleton structure, but the CONTENT (architecture, MCP servers, skills, requirements) is unique and must be researched.

## Phase 1: Create Skeleton Structure (ALWAYS THE SAME)

```bash
mkdir -p {{PROJECT_PATH}}/{docs,.claude/skills}
```

Create these files immediately (with placeholders):
```
project/
├── CLAUDE.md                    # Project context
├── .mcp.json                    # MCP servers (empty initially)
├── .claude/
│   ├── settings.json            # Hooks and permissions
│   └── skills/                  # Custom commands
└── docs/
    ├── PRD.md                   # Product requirements
    ├── ARCHITECTURE.md          # System design
    └── REQUIREMENTS.md          # Functional specs
```

## Phase 2: Gather Project Context

Ask user:
1. **Project name** and one-line description
2. **Problem being solved** - What pain point?
3. **Target users** - Who will use this?
4. **Key features** - What must it do?
5. **Constraints** - Budget, timeline, existing systems?

## Phase 3: Research MCP Servers (CRITICAL)

Based on project needs, research available MCP servers:

**Search for MCP servers:**
- Web search: "MCP server for [technology/service]"
- Check: https://github.com/modelcontextprotocol/servers
- Check: https://mcp.so/ (MCP registry)

**Common MCP servers by domain:**
| Domain | Servers to Research |
|--------|---------------------|
| AWS Infrastructure | `terraform`, `aws-docs`, `aws-pricing` |
| Payments | `stripe` |
| Databases | `sqlite`, `postgres`, `supabase` |
| Source Control | `github`, `gitlab` |
| Communication | `slack`, `discord` |
| AI/ML | `openai`, `anthropic` |
| Productivity | `notion`, `linear`, `jira` |
| File Operations | `filesystem` (always include) |

**For each potential server, evaluate:**
- Does it solve a real need for this project?
- What credentials/setup does it require?
- Will it be used frequently enough to justify the context cost?

## Phase 4: Research Skills Needed

Identify repetitive workflows that should become skills:

**Universal skills (most projects need):**
- `build` - Compile/bundle the application
- `test` - Run test suite
- `deploy` - Push to production

**Research project-specific skills:**
- What multi-step processes will be repeated?
- What commands are complex and error-prone?
- What workflows need standardization?

**Example skill patterns by project type:**
| Type | Skills to Consider |
|------|-------------------|
| Web App | `preview`, `lighthouse`, `e2e-test` |
| API | `api-test`, `generate-docs`, `db-migrate` |
| Mobile | `build-ios`, `build-android`, `publish` |
| Data | `run-pipeline`, `validate-data`, `generate-report` |
| Infrastructure | `plan`, `apply`, `destroy`, `logs` |

## Phase 5: Research Architecture Options

Don't assume architecture - research what fits:

**Questions to answer:**
1. What scale is expected? (users, requests, data volume)
2. What's the budget constraint?
3. What does the team already know?
4. What are similar products built with?

**Web search for:**
- "[problem domain] architecture patterns"
- "[similar product] tech stack"
- "best practices [technology] 2025"

## Phase 6: Fill Planning Documents

With research complete, populate:

### CLAUDE.md
- Project overview and goals
- Chosen tech stack with rationale
- MCP servers configured and why
- Available skills and when to use them
- Common commands
- Code standards for this project

### docs/PRD.md
- User personas from Phase 2
- Feature requirements with priorities
- Success metrics
- Timeline and milestones

### docs/ARCHITECTURE.md
- System diagram
- Data models
- API design
- Infrastructure plan

### docs/REQUIREMENTS.md
- Detailed functional requirements (REQ-XXX-NNN format)
- Non-functional requirements (performance, security)

## Phase 7: Configure MCP Servers

Create `.mcp.json` with researched servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    }
    // Add other researched servers
  }
}
```

## Phase 8: Create Initial Skills

For each identified skill, create `.claude/skills/{name}/SKILL.md`:

```markdown
---
name: skill-name
description: When to use this skill. Be specific.
---

# Skill Name

Steps to execute...
```

## Phase 9: Initialize Git

```bash
cd {{PROJECT_PATH}}
git init
cat > .gitignore << 'EOF'
node_modules/
.env*
.next/
out/
dist/
*.tfstate*
.terraform/
.claude/session.log
.claude/settings.local.json
EOF
git add -A
git commit -m "Initial project setup with Claude Code structure"
```

## Output

Display:
1. Project structure tree
2. Configured MCP servers with purpose
3. Created skills with descriptions
4. Next steps:
   - [ ] Add MCP server credentials to environment
   - [ ] Run `/mcp` to verify server connections
   - [ ] Review and refine PRD with stakeholders
   - [ ] Begin implementation per architecture plan
