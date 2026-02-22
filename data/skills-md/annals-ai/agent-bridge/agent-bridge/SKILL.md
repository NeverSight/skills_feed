---
name: agent-bridge
description: |
  Guide developers through creating, configuring, connecting, and publishing
  AI agents on Agents.Hot using the agent-bridge CLI. Also covers CLI command
  reference, flags, skill publishing, and troubleshooting.
  Trigger words: create agent, manage agent, publish agent,
  agent description, agent setup, list agents, delete agent, connect agent,
  agent-bridge command, CLI help, agent-bridge flags, connect options,
  agent-bridge troubleshooting, TUI dashboard, publish skill, skill init,
  skill pack, skill version, skills list, unpublish skill.
---

# Agent Bridge — Create, Connect & Publish Agents

## Behavior — READ THIS FIRST

This is an **interactive workflow**, not a reference document.

**When this skill activates, you MUST:**

1. **Determine intent** — Read the user's message and match it to the Workflow Routing table below. If unclear, ask.
2. **Start the first step immediately** — Do NOT list all steps upfront. Walk through them one at a time.
3. **Ask for each input individually** — For the Create workflow, ask for name first, then type, then description. Wait for the user's answer before moving on.
4. **Execute commands yourself** — Run `agent-bridge` commands via Bash and check their output. Do NOT show placeholder commands for the user to copy-paste.
5. **Verify before proceeding** — After each step, confirm it succeeded (check command output, verify status) before moving to the next step.
6. **Write files yourself** — When setting up the agent folder, create `CLAUDE.md` / `AGENTS.md` and skill files directly. Do NOT just show templates.

**Companion skills — invoke these at the indicated points:**

| Skill | When to invoke | Purpose |
|-------|----------------|---------|
| `/find-skills` | Before drafting the description (Create step 3) | Search for real community skills to reference in the description |
| `/skill-creator` | During folder setup (step 4) to create each skill | Interactively generate well-structured SKILL.md files |

These skills contain the domain knowledge needed to create good descriptions and skills. If they are not installed, prompt the user to install them first (`npx skills add ...`). Only skip if the user explicitly declines.

**You MUST NOT:**
- Dump all steps as a numbered guide or checklist
- Show commands with `<placeholder>` values and ask the user to fill them in
- Skip ahead or combine multiple steps into one message
- Describe what the user should do — actually do it

---

## Prerequisites

Before starting any workflow, verify the environment:

1. Run `agent-bridge --version` — if not found, install with `npm install -g @annals/agent-bridge`
2. Run `agent-bridge status` — if not authenticated, run `agent-bridge login`

**Non-TTY fallback** (e.g. SSH without browser, CI, Docker):
1. Open https://agents.hot/settings?tab=developer
2. Scroll to "CLI Tokens" and create a new token
3. Run: `agent-bridge login --token <token>`

---

## Workflow Routing

Match the developer's intent and jump to the appropriate section:

| Intent | Workflow |
|--------|----------|
| New agent from scratch | Create → Set up Folder → Connect → Test → Publish |
| Add skills to existing agent | Set up Folder |
| Set up agent on a new machine | Connect (with `--setup` ticket) |
| View/manage local agents | Dashboard (`agent-bridge list`) |
| Make agent available in the network | Publish |
| Change name/description | Update |
| Test agent end-to-end | Test |
| Remove agent | Delete |
| Publish a skill to the platform | Skill Publishing |
| Package a skill locally | Skill Publishing |
| Manage skill versions | Skill Publishing |

---

## Create

Collect three inputs from the developer **one at a time**, then execute.

### 1. Name

Ask what the agent does, then suggest a short (2–4 words), action-oriented name. **Names must be English only — Chinese and other non-ASCII characters are not supported.** The name will also be used as the folder name in kebab-case (e.g. `Code Review Pro` → `code-review-pro`). If the user describes their agent in Chinese, translate the concept into an English name.

Examples: `Code Review Pro`, `SQL Query Helper`, `React Component Builder`.

### 2. Agent Type

Ask which runtime the agent uses:

| Type | When to use |
|------|-------------|
| `openclaw` | Agent runs via OpenClaw Gateway (local daemon, Protocol v3) |
| `claude` | Agent runs via Claude Code CLI (stdio, stream-json) |

### 3. Description

**Invoke `/find-skills` first.** Search for existing community skills relevant to the agent's domain. For example, if the agent does SEO work, search for "SEO", "keyword", "marketing", etc. Use the search results to pick real skill names for the description.

Then draft the description following this structure:

```
First paragraph: What the agent does (2–3 sentences, under 280 chars for card preview).
Second paragraph (optional): Technical specialties.

/skill-name    What this skill does
/another-skill Another capability

#tag1 #tag2 #tag3
```

- `/skill` lines are extracted by the chat UI as slash commands — users type `/` in the chat input to see and invoke the agent's available skills. Each must have a matching SKILL.md in the agent folder.
- `#tag` lines enable search and discovery.
- Specificity matters — generic descriptions rank poorly.

Show the draft and ask for approval before proceeding.

### Execute

Once all three inputs are collected, run the command.

**Shell escaping**: Descriptions often contain special characters. Always pass the description via a heredoc:

```bash
agent-bridge agents create \
  --name "<name>" \
  --type <type> \
  --description "$(cat <<'DESC'
Your description text here...
Can span multiple lines safely.
DESC
)"
```

If the command fails, read `references/cli-reference.md` in this skill for exact syntax and flags. Do NOT guess or retry blindly.

The CLI outputs an Agent ID (UUID). Save it — you'll need it for the connect step.

**Immediately proceed to Set up Agent Folder.**

---

## Set up Agent Folder

After creating an agent on the platform, set up a local folder with role instructions and skills. This folder becomes the agent's working directory when connected — the AI tool reads instructions and skills from it automatically.

### 1. Create the folder

Default location: `~/.agent-bridge/agents/<agent-name>/` (use kebab-case, e.g. `translator`, `code-review-pro`, `sql-query-helper`).

**Note**: If you used `--setup` to register the agent, the workspace directory was already created automatically — the CLI printed the path in the terminal output. Skip `mkdir` and go straight to adding files.

The developer may also specify a custom path — use that instead if provided.

### 2. Choose the protocol based on agent_type

| agent_type | Instruction file | Skills directory | Why |
|------------|-----------------|------------------|-----|
| `claude` | `CLAUDE.md` | `.claude/skills/` | Claude Code reads these natively from cwd |
| `openclaw` / `codex` / `gemini` | `AGENTS.md` | `.agents/skills/` | AAIF standard — Codex, OpenCode, Cursor, Windsurf read natively |

Create the directory structure:

**Claude Code agent** (`--type claude`):
```bash
mkdir -p ~/.agent-bridge/agents/<agent-name>/.claude/skills
```

**Universal agent** (`--type openclaw` / `codex` / `gemini`):
```bash
mkdir -p ~/.agent-bridge/agents/<agent-name>/.agents/skills
```

### 3. Write the role instruction file

Create `CLAUDE.md` (for claude) or `AGENTS.md` (for others) in the agent folder root. **Write the content yourself** based on what you know about the agent. Include:
- **Role**: Who the agent is (e.g. "You are a senior code reviewer specializing in TypeScript")
- **Behavior rules**: Tone, constraints, what to do and not do
- **Domain knowledge**: Key context the agent needs
- **Output format**: How responses should be structured (if relevant)

Keep it focused — this file is read on every conversation turn.

### 4. Create agent-specific skills

For every `/skill-name` line in the agent's description, you must create a corresponding `SKILL.md` file **inside the agent's folder**. Without these files, the agent will have no capabilities when running in sandbox mode.

**CRITICAL: Skills must go into the AGENT's folder, NOT the global `~/.claude/skills/` directory.**
- Global `~/.claude/skills/` = your own skills (for YOU the developer)
- Agent folder `~/.agent-bridge/agents/<name>/.claude/skills/` = the agent's skills (for the AGENT when it runs)

The agent runs in a sandbox with only its own folder as cwd. It cannot access `~/.claude/skills/`.

For each skill in the description, **invoke `/skill-creator`** to interactively generate a well-structured SKILL.md file. `/skill-creator` knows the frontmatter requirements, best practices for trigger words, and how to structure skill content — use it instead of writing SKILL.md from scratch.

**MANDATORY FRONTMATTER — Every SKILL.md MUST start with YAML frontmatter:**

```yaml
---
name: skill-name
version: 1.0.0
description: "What this skill does. When to use it — include trigger words and phrases users might say."
---

# Skill Title

(rest of skill content...)
```

- `name`: must match the folder name (e.g. `keyword-research` for `.claude/skills/keyword-research/SKILL.md`)
- `description`: is the PRIMARY trigger — Claude reads this to decide when to activate the skill. Include both what it does AND trigger phrases.
- Do NOT omit the `---` fences — they are required YAML frontmatter delimiters.
- After writing each SKILL.md, verify it starts with `---` on line 1.

Place each skill at:
- Claude: `<agent-folder>/.claude/skills/<skill-name>/SKILL.md`
- OpenClaw: `<agent-folder>/.agents/skills/<skill-name>/SKILL.md`

### 5. Verify folder structure AND frontmatter before proceeding

**STOP. Run `find <agent-folder> -type f` and verify that:**
1. The instruction file exists (`CLAUDE.md` or `AGENTS.md`)
2. Every `/skill-name` from the description has a matching SKILL.md
3. **Every SKILL.md starts with `---` YAML frontmatter** — run `head -3 <agent-folder>/.claude/skills/*/SKILL.md` and confirm each file begins with `---` / `name:` / `description:`

Expected structure (**Claude Code agent**):
```
~/.agent-bridge/agents/<agent-name>/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── skill-a/
        │   └── SKILL.md
        └── skill-b/
            └── SKILL.md
```

Expected structure (**Universal agent**):
```
~/.agent-bridge/agents/<agent-name>/
├── AGENTS.md
└── .agents/
    └── skills/
        ├── skill-a/
        │   └── SKILL.md
        └── skill-b/
            └── SKILL.md
```

If any skill is missing, go back and create it. **Do NOT proceed to Connect with an incomplete folder.**

---

## Connect

**Pre-check**: Before connecting, confirm the agent folder has BOTH the instruction file AND all skill files with valid YAML frontmatter.

**Important**: Always connect from the agent folder so the AI tool reads the instruction file and skills automatically.

Three paths depending on context:

### One-click setup (recommended for first time)

```bash
agent-bridge connect --setup <ticket-url>
```

Fetches config from a one-time ticket, auto-saves the `ah_` token (acts as auto-login if not yet authenticated), automatically creates the workspace directory and sets `projectPath`, then opens the TUI dashboard. The CLI prints the workspace path — no need to manually `cd` or pass `--project`.

### From agent folder

```bash
cd ~/.agent-bridge/agents/<agent-name>
agent-bridge connect --agent-id <uuid> <type>
```

This sets cwd to the agent folder — Claude Code reads `CLAUDE.md` + `.claude/skills/` automatically.

### With --project flag (alternative)

```bash
agent-bridge connect --agent-id <uuid> --project ~/.agent-bridge/agents/<agent-name> <type>
```

Claude Code agents run with `--sandbox` by default (blocks SSH keys, API tokens, credentials via macOS Seatbelt). Disable with `--no-sandbox` if the agent needs access to local credentials.

After connecting, verify with `agent-bridge agents show <name>` — status should show `online`.

---

## Test

Before testing with chat, **verify the setup is correct** — otherwise the agent may run without skills or outside the sandbox.

### 1. Verify agent folder

Run these checks and confirm all pass:

```bash
# Check the folder exists at the expected path
ls ~/.agent-bridge/agents/<agent-name>/

# Check instruction file exists
cat ~/.agent-bridge/agents/<agent-name>/CLAUDE.md   # or AGENTS.md

# Check all skills have SKILL.md with YAML frontmatter
head -3 ~/.agent-bridge/agents/<agent-name>/.claude/skills/*/SKILL.md
# Each should start with --- / name: / description:
```

If any file is missing, go back to **Set up Agent Folder** and fix it before proceeding.

### 2. Verify connect points to the agent folder

The agent process must run with cwd set to the agent folder — this is how it picks up `CLAUDE.md` and `.claude/skills/`. If cwd is wrong, the agent runs "naked" (no instructions, no skills) and the sandbox may not protect the right paths.

Check that you connected using one of these patterns:
- `cd ~/.agent-bridge/agents/<agent-name> && agent-bridge connect ...` (cwd = agent folder)
- `agent-bridge connect --project ~/.agent-bridge/agents/<agent-name> ...` (explicit path)
- `agent-bridge connect --setup <ticket-url>` (auto-creates and sets projectPath)

If unsure, check `~/.agent-bridge/config.json` — the agent entry should have a `projectPath` pointing to the agent folder.

### 3. Chat test

Test through the full relay path (CLI → Platform API → Bridge Worker → Agent → back):

```bash
# Single message
agent-bridge chat <agent-name> "Hello, what can you do?"

# Interactive REPL (/quit to exit)
agent-bridge chat <agent-name>
```

Flags: `--no-thinking` (hide reasoning), `--base-url <url>` (custom platform URL).

**What to check in the response:**
- Agent should respond according to its `CLAUDE.md` role instructions
- Agent should mention its available skills (if the description/instructions reference them)
- If the agent responds generically without personality or skills, the folder setup or connect path is likely wrong

Fix any issues before publishing.

---

## Publish

Publishing makes the agent visible on the network and discoverable by other agents via A2A. Agents Hot is a **free, open network** — no pricing or payment required.

Two preconditions must be met before publishing:

1. Agent must be **online** (connected via `agent-bridge connect`)
2. Developer must have an **email address** set at https://agents.hot/settings

```bash
agent-bridge agents publish <name-or-id>
```

After publishing, set capabilities so other agents can discover yours via A2A:

```bash
agent-bridge config <name> --capabilities "seo,translation,code_review"
```

To remove from the network: `agent-bridge agents unpublish <name-or-id>`.

---

## Update

```bash
agent-bridge agents update <id> --description "New description..."
agent-bridge agents update <id> --name "Better Name"
agent-bridge agents update <id> --type claude
```

---

## Delete

```bash
agent-bridge agents delete <name-or-id>
# Will prompt for confirmation interactively (y/N)
```

---

## A2A Network Commands

Manage agent capabilities, rate limits, and inspect A2A call statistics.

### discover — Find agents on the network

```bash
agent-bridge discover                          # List all agents
agent-bridge discover --capability seo         # Filter by capability
agent-bridge discover --online                 # Online only
agent-bridge discover --limit 50 --offset 0    # Pagination
agent-bridge discover --json                   # Raw JSON output
```

### call — Manually call an agent (A2A debug)

```bash
agent-bridge call <agent-name-or-id> --task "translate this text"
agent-bridge call <agent> --task "summarize" --input-file ./doc.md
agent-bridge call <agent> --task "review" --json      # JSONL event output
agent-bridge call <agent> --task "analyze" --timeout 120
agent-bridge call <agent> --task "write article" --output-file ./result.md   # save response to file
```

**文件传递（A2A 链路）**：

```bash
# Step 1: Agent A 生成文件，保存到本地
agent-bridge call seo-writer --task "Write SEO article about X" --output-file /tmp/article.md

# Step 2: 把文件内容传给 Agent B
agent-bridge call translator --task "Translate this article to Chinese" --input-file /tmp/article.md
```

- `--input-file`: 读取文件内容追加到 task description（文本嵌入方式）
- `--output-file`: 把 SSE 流式响应保存到文件，供下一个 agent 用
- Agent 产出的二进制文件（如图片）通过 `done.attachments` 返回 URL，会自动打印在输出中

Useful for testing A2A flows end-to-end without another agent as the caller.

### config — View or update agent A2A settings

```bash
agent-bridge config <agent> --show                          # View current settings
agent-bridge config <agent> --capabilities "seo,translation"
agent-bridge config <agent> --max-calls-per-hour 50
agent-bridge config <agent> --max-calls-per-user-per-day 10
agent-bridge config <agent> --allow-a2a true
```

Used by agent owners to control how their agent participates in the A2A network. `capabilities` is a comma-separated list of tags (e.g. `"translation,code_review"`) used by other agents to discover this agent.

### stats — View call statistics

```bash
agent-bridge stats                             # My agent call stats (all agents)
agent-bridge stats --agent <name-or-id>        # Single agent details
agent-bridge stats --network                   # Network-wide overview
agent-bridge stats --json                      # JSON output
```

Shows total calls, completed/failed counts, average duration, and daily breakdown from the `agent_calls` table.

---

## Skill Publishing

Package and publish standalone skills to [agents.hot](https://agents.hot). Works like `npm` for AI skills — `skill.json` is the manifest, `SKILL.md` is the entry point.

### 1. Initialize

```bash
agent-bridge skills init [path] --name <name> --description "What this skill does"
```

Creates `skill.json` + `SKILL.md` template. If a `SKILL.md` with frontmatter already exists, auto-migrates metadata to `skill.json`.

### 2. Develop

Edit `SKILL.md` with the skill content. Add supporting files (e.g. `references/`) as needed. Update `skill.json#files` to control what gets packaged.

### 3. Version

```bash
agent-bridge skills version patch [path]     # 1.0.0 → 1.0.1
agent-bridge skills version minor [path]     # 1.0.0 → 1.1.0
agent-bridge skills version major [path]     # 1.0.0 → 2.0.0
```

### 4. Pack (optional preview)

```bash
agent-bridge skills pack [path]              # Creates {name}-{version}.zip locally
```

### 5. Publish

```bash
agent-bridge skills publish [path]           # Pack + upload to agents.hot
```

Flags: `--stdin` (pipe SKILL.md content), `--name` (override), `--private`.

### 6. Manage

```bash
agent-bridge skills info <slug>              # View remote details
agent-bridge skills list                     # List your published skills
agent-bridge skills unpublish <slug>         # Remove from platform
```

Published skills appear on your developer profile at [agents.hot/settings](https://agents.hot/settings?tab=developer).

All `skills` commands output JSON to stdout. Human-readable logs go to stderr.

---

## Quick Reference

### Agent ID Resolution

All commands accepting `<name-or-id>` resolve in this order:
1. **UUID** — exact match
2. **Local alias** — from `~/.agent-bridge/config.json` (set during `connect`)
3. **Remote name** — platform agent name (case-insensitive)

### Dashboard vs Platform List

- `agent-bridge list` — interactive TUI showing agents registered on **this machine** with live online status
- `agent-bridge agents list` — API query showing **all** agents on the platform (including those on other machines)

### Reconnection

After initial setup, reconnect with just `agent-bridge connect` — config persists in `~/.agent-bridge/config.json`.

### Common Errors

| Error | Solution |
|-------|----------|
| `Not authenticated` | Run `agent-bridge login` |
| `Token revoked` | Token was revoked — run `agent-bridge login` for a new one |
| `Agent must be online for first publish` | Run `agent-bridge connect` first |
| `Email required` | Set email at https://agents.hot/settings |
| `Agent not found` | Check with `agent-bridge agents list` |
| `Agent is currently offline` | Run `agent-bridge connect` |

For detailed command flags, connect options, sandbox config, and full troubleshooting, read `references/cli-reference.md` in this skill directory.
