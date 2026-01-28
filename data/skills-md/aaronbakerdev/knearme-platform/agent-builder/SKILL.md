---
name: agent-builder
description: Provides guidance for building and deploying Claude Agent SDK agents and Claude Code Skills. Use when designing agents (dev or non-dev), choosing architectures/tools, or deploying to a VPS.
---

# Agent Builder Skill

Build and deploy Claude Agent SDK applications to your Hetzner VPS.

## Metadata

- **Name:** agent-builder
- **Version:** 1.1.0
- **Author:** KnearMe
- **Tags:** claude, agent-sdk, skills, vps, deployment

## When to Use

Use this skill when:
- Creating a new AI agent application (coding or non-coding use cases)
- Designing agent behavior, escalation paths, and decision boundaries
- Deploying agents to the Hetzner VPS
- Setting up multi-agent architectures
- Troubleshooting agent deployments

## Non-Dev First Principle

Always consider non-development use cases. Many high-value agents are workflow-focused, not code-focused:

- Customer support triage
- Sales qualification
- Operations checklists
- Marketing content coordination
- Finance/QA reviews
- Hiring or onboarding workflows

If the request is non-dev or mixed, start with discovery and workflow design before writing code.

## Start Here (Design → Build)

1. **Define the outcome, user, and trigger** → `references/agent-design-guide.md`
2. **Choose an architecture pattern** → `references/architectures.md`
3. **Select tools with least-privilege** → `references/tool-development.md`
4. **Define roles + escalation rules** → `references/role-definition.md`
5. **Instrument + improve** → `references/performance-monitoring.md` + `references/improving-agents.md`
6. **Add UX if needed** → `references/ui-development.md`
7. **Test before shipping** → `references/testing-guide.md`

## Reference Map (Progressive Disclosure)

- `references/agent-design-guide.md` — Discovery, use-case fit, tool decision trees, anti-patterns
- `references/architectures.md` — Single, orchestrator+subagents, multi-agent fleets
- `references/role-definition.md` — Role prompts, delegation patterns, escalation triggers
- `references/tool-development.md` — Tool selection, MCP tools, guardrails
- `references/performance-monitoring.md` — Metrics, budgets, alerts, logs
- `references/improving-agents.md` — Feedback loops, evals, regression tests
- `references/ui-development.md` — Chat UX patterns + component examples
- `references/testing-guide.md` — Test strategy, fixtures, mocks, evals
- `references/react-chat-component.tsx` — Ready-to-use chat UI (React)
- `references/agent-template.ts` — Complete agent server template
- `references/non-dev-templates.md` — Expanded non-dev templates (support, sales, ops, marketing, finance)
- `references/background-agents.md` — Background/autonomous role execution patterns
- `references/self-improving-agents.md` — Self-improving agent loop (AlphaEvolve patterns)

## Claude Code Skill Authoring Rules

- **Required frontmatter:** `name` (lowercase, hyphen/underscore) and `description` (what the skill does + when to use).
- **Optional `allowed-tools`:** If present, it limits tools in Claude Code. If omitted, tools are not restricted by the skill file.
- **Keep it short:** Aim to keep `SKILL.md` under ~500 lines and move long content into `references/`.
- **Progressive disclosure:** Link reference files at most one level deep (no nested reference chains).

## Quick Start

### Create New Agent

```bash
mkdir my-agent && cd my-agent
npm init -y
npm install @anthropic-ai/claude-agent-sdk express ws
# See references/agent-template.ts for a full server template
```

### Deploy to VPS (Short Version)

- Run `scripts/setup-vps.sh` once per server
- Use `scripts/deploy-agent.sh` per agent
- See `references/architectures.md` for multi-agent deployments

## Non-Dev Agent Templates

Use these when the goal is business workflow impact, not coding.
Expanded templates: `references/non-dev-templates.md`

### 1) Support Triage Agent

- **Outcome:** Accurate category + next action in <2 minutes
- **Trigger:** New ticket or chat created
- **Inputs:** Ticket text, user plan, last 5 interactions
- **Outputs:** Priority, summary, suggested response, escalation flag
- **Tools:** Read, Glob, Grep, AskUserQuestion (Write for drafts)
- **Escalate when:** Refunds, security, legal threats, angry users
- **Pattern:** Single agent → Orchestrator+Subagents as volume grows

### 2) Sales Qualification Agent

- **Outcome:** Score lead + recommended next step
- **Trigger:** Inbound form or sales inbox message
- **Inputs:** Form fields, source, company size, prior contact
- **Outputs:** Fit score, objections, suggested reply
- **Tools:** Read, Glob, Grep, AskUserQuestion (Write for drafts)
- **Escalate when:** Enterprise/legal requirements, pricing exceptions
- **Pattern:** Single agent

### 3) Ops Checklist Agent

- **Outcome:** Runbook completed with clear status
- **Trigger:** Daily/weekly ops cadence, incident checklist
- **Inputs:** Runbook file, system status snapshots
- **Outputs:** Checklist state, anomalies, recommended follow-ups
- **Tools:** Read, Glob, Grep (Bash only if strictly required)
- **Escalate when:** Missing signals, critical thresholds
- **Pattern:** Single agent (orchestrator if many systems)

### 4) Marketing Content Coordinator

- **Outcome:** On-brand draft + distribution checklist
- **Trigger:** New campaign request or content brief
- **Inputs:** Brand voice docs, product updates, target persona
- **Outputs:** Draft content, channel checklist, CTA options
- **Tools:** Read, Glob, Grep, Write, Edit
- **Escalate when:** Claims need legal review, sensitive topics
- **Pattern:** Orchestrator+Subagents (researcher/writer/reviewer)

### 5) Finance/QA Review Agent

- **Outcome:** Flag anomalies + recommend follow-ups
- **Trigger:** Monthly close, QA batch, or audit request
- **Inputs:** Reports, threshold rules, last period baselines
- **Outputs:** Findings list, confidence, next steps
- **Tools:** Read, Glob, Grep (no Write unless drafting)
- **Escalate when:** Large variances, policy violations
- **Pattern:** Single agent with strict constraints

### Non-Dev Decision Checklist

- Is the **source of truth** clear and accessible?
- What actions are **advisory vs automatic**?
- What requires **human approval**?
- What are the **escalation triggers**?
- What does **success** look like in measurable terms?
- What is the **lowest-risk toolset** that still works?

## Background Agents (Summary)

- Use job-based execution for discrete tasks (events, cron).
- Use continuous execution for live routing and monitoring.
- Map authority to an autonomy ladder and enforce escalation rules.
- See `references/background-agents.md` for full patterns.

## Self-Improving Agents (Summary)

- Use a generate → evaluate → promote loop with automated evaluators.
- Treat best prompts/workflows as a "skill library" that evolves over time.
- Only promote when metrics improve on a fixed regression suite.
- See `references/self-improving-agents.md` for AlphaEvolve-inspired patterns.

## Architecture Patterns (Summary)

- **Single Agent:** One domain, simple logic
- **Orchestrator + Subagents:** Multi-specialty, parallel work
- **Multi-Agent Fleet:** Separate products/domains
- See `references/architectures.md` for the full decision tree

## SDK Essentials (Summary)

```typescript
const response = query({
  prompt,
  options: {
    systemPrompt,
    allowedTools: ["Read", "Glob", "Grep", "Task", "Skill"],
    agents: SUBAGENTS,
    permissionMode: "acceptEdits",
    settingSources: ["user", "project"],
  },
});
```

- `Task` must be in `allowedTools` for subagents to spawn
- Subagents cannot spawn other subagents
- Skills load only with `settingSources` and `"Skill"` in `allowedTools`
- Include `"project"` to load `CLAUDE.md` instructions
- `allowed-tools` frontmatter applies to Claude Code CLI, not SDK
- See `references/agent-template.ts` for streaming/session examples

## Deployment & Ops (Summary)

- Use `scripts/setup-vps.sh` + `scripts/deploy-agent.sh`
- Put Nginx + SSL in front of web UIs
- Track latency, cost, and error budgets (`references/performance-monitoring.md`)
- Add feedback loops and evals (`references/improving-agents.md`)

## Testing & Quality (Summary)

- Test behavior, not phrasing; keep regression fixtures
- Validate tool safety boundaries and escalation paths
- See `references/testing-guide.md` for full patterns

## Resources

```text
Claude Agent SDK Docs: https://docs.anthropic.com/claude-code/agent-sdk
Hetzner Cloud Console: https://console.hetzner.cloud
PM2 Documentation: https://pm2.keymetrics.io/docs
Cloudflare Tunnel Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
```

## Scripts

- `scripts/setup-vps.sh` - Initial VPS configuration
- `scripts/deploy-agent.sh` - Deploy a new agent
- `scripts/new-agent.sh` - Scaffold a new agent project
