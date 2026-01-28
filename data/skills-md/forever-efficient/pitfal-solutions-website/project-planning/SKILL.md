---
name: project-planning
description: Guide users through comprehensive project planning. Creates PRD, architecture, and requirements documents through structured questioning. Use when starting a new project or formalizing an existing idea.
---

# Project Planning Workflow

Guide the user through structured project planning with **active research** to generate comprehensive documentation.

## Phase 1: Problem Definition

Ask and document:
1. **What problem are you solving?** (pain point)
2. **Who has this problem?** (target users)
3. **How is it being solved today?** (alternatives)
4. **Why will your solution be better?** (differentiation)

## Phase 2: User Personas

For each user type:
1. **Name and demographics**
2. **Goals** - What do they want to achieve?
3. **Pain points** - What frustrates them today?
4. **User journey** - How will they use the product?

Create 2-3 personas minimum.

## Phase 3: Feature Requirements

Guide through requirements gathering:
1. List all features user envisions
2. Categorize by priority:
   - **P0** - MVP, must have for launch
   - **P1** - Important, soon after launch
   - **P2** - Nice to have, future
3. Assign requirement IDs (REQ-AREA-NNN)

## Phase 4: Research MCP Servers (CRITICAL)

Based on identified features and integrations, **actively research** available MCP servers:

**Research steps:**
1. List all external services the project will integrate with
2. Web search for each: "MCP server for [service name]"
3. Check official registry: https://github.com/modelcontextprotocol/servers
4. Check community registry: https://mcp.so/

**For each discovered server:**
- Does it cover needed functionality?
- What are the setup requirements?
- Is it actively maintained?

**Document findings in CLAUDE.md**

## Phase 5: Research Skills Needed

Identify workflows that should become skills:

**Ask:**
- What multi-step processes will be repeated?
- What commands are complex or error-prone?
- What workflows need consistency?

**Research similar projects:**
- Web search: "[project type] development workflow"
- What automation do similar teams use?

**Document planned skills in CLAUDE.md**

## Phase 6: Research Technical Architecture

**Don't assume - research what fits:**

1. Web search: "[problem domain] architecture patterns 2025"
2. Web search: "[similar product] tech stack"
3. Consider constraints: budget, team skills, scale requirements

**Evaluate options for:**
- **Frontend** - Framework, styling, state management
- **Backend** - Language, framework, hosting model
- **Database** - SQL vs NoSQL, managed vs self-hosted
- **Infrastructure** - Cloud provider, serverless vs containers

Create ASCII architecture diagram.

## Phase 7: Success Metrics

Define measurable goals:
1. **Business metrics** - Revenue, users, engagement
2. **Technical metrics** - Performance, uptime, latency
3. **Timeline** - Milestones and deadlines

## Phase 8: Risks & Mitigations

Identify:
1. Technical risks (new tech, scaling, integrations)
2. Business risks (market, competition, timing)
3. Resource risks (budget, timeline, skills)

For each: probability, impact, mitigation strategy.

## Output

Generate these documents with research findings:
1. `docs/PRD.md` - Complete product requirements
2. `docs/ARCHITECTURE.md` - Technical design with rationale
3. `docs/REQUIREMENTS.md` - Detailed feature specs
4. `.mcp.json` - Configured with researched servers
5. `.claude/skills/` - Initial skills based on research
6. `CLAUDE.md` - Updated with full project context

## Tips

- Don't skip research phases - assumptions cause rework
- Be specific - "fast" → "< 2s load time"
- Prioritize ruthlessly - MVPs should be minimal
- Document research findings - future you will thank you
- Validate MCP servers exist before planning around them
