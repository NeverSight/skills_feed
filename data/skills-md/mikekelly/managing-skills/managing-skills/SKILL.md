---
name: managing-skills
description: "Install, find, update, and manage agent skills. Use when the user wants to add a new skill, search for skills that do something, check if skills are up to date, or update existing skills. Triggers on: install skill, add skill, get skill, find skill, search skill, update skill, check skills, list skills."
---

<objective>
Manage agent skills via the `npx skills` CLI. Handle installing skills from GitHub repos, searching for available skills, checking for updates, and updating installed skills.
</objective>

<quick_start>
Determine which operation the user wants and run the appropriate command. Always include `--yes` to skip confirmations. Default to project-level install and the current agent type unless told otherwise.

Primary commands:
```
npx skills add {source} --yes --agent {agent-type}
npx skills find {keyword} --yes
npx skills check --yes
npx skills update --yes
npx skills add --list --yes
```
</quick_start>

<context>
<agent_type>
Detect the agent you are running as. Map to the correct `--agent` flag value:

| Agent | Flag value |
|-------|-----------|
| Amp | `amp` |
| Claude Code | `claude-code` |
| Cline | `cline` |
| Codex | `codex` |
| Continue | `continue` |
| Cursor | `cursor` |
| Gemini CLI | `gemini-cli` |
| GitHub Copilot | `github-copilot` |
| Goose | `goose` |
| Kilo Code | `kilo` |
| Kiro CLI | `kiro-cli` |
| OpenCode | `opencode` |
| Qwen Code | `qwen-code` |
| Roo Code | `roo` |
| Trae | `trae` |
| Windsurf | `windsurf` |

If unsure, check for config directories (e.g., `.claude/`, `.codex/`, `.cursor/`).
Only include additional agent types if the user explicitly requests it (e.g., "install for all agents" or "also install for codex").
</agent_type>

<install_scope>
- **Project** (default): Installs to `./<agent>/skills/` in the current project.
- **Global** (`-g`): Installs to `~/<agent>/skills/`. Only use when the user says "global", "globally", or "for all projects".
</install_scope>
</context>

<operations>

<operation name="install">
<trigger>User says: install, add, get, set up a skill</trigger>
<steps>
1. Identify the skill source. Accepts:
   - `owner/repo` — installs all skills from the repo
   - Full GitHub/GitLab URL to a repo, directory, or SKILL.md file (e.g., `https://github.com/owner/repo/tree/main/skills/foo`)
   - Local filesystem path
   - Use `-s skill-name` to cherry-pick a specific skill by name from a multi-skill repo
2. Determine scope: project (default) or global (`-g`).
3. Determine agent type(s) to target.
4. Run:
```bash
npx skills add {source} --yes --agent {agent-type}
```
Add `-g` if global. Add multiple `--agent` flags if targeting multiple agents.
</steps>
<examples>
"Install the vercel-labs/skills skill" →
`npx skills add vercel-labs/skills --yes --agent claude-code`

"Install just the managing-skills skill from that repo" →
`npx skills add vercel-labs/skills --yes -s managing-skills --agent claude-code`

"Install this skill: github.com/owner/repo/tree/main/skills/foo" →
`npx skills add https://github.com/owner/repo/tree/main/skills/foo --yes --agent claude-code`

"Globally install foo/bar for all agents" →
`npx skills add foo/bar --yes -g --all`
</examples>
</operation>

<operation name="find">
<trigger>User says: find, search, discover, look for, browse skills</trigger>
<steps>
1. If user gave a keyword, pass it directly.
2. Run:
```bash
npx skills find {keyword} --yes
```
3. Present results to the user. If they pick one, follow the install operation.
</steps>
</operation>

<operation name="check">
<trigger>User says: check for updates, are my skills up to date</trigger>
<steps>
Run:
```bash
npx skills check --yes
```
Report which skills have updates available. Offer to update if any are found.
</steps>
</operation>

<operation name="update">
<trigger>User says: update skills, upgrade skills</trigger>
<steps>
Run:
```bash
npx skills update --yes
```
Report what was updated.
</steps>
</operation>

<operation name="list">
<trigger>User says: list skills, show installed skills, what skills do I have</trigger>
<steps>
Run:
```bash
npx skills add --list --yes
```
</steps>
</operation>

</operations>

<guidelines>
- Always use `--yes` to skip confirmation prompts.
- Default to project scope unless the user explicitly says global.
- Default to the current agent type only. Add others only if the user asks.
- If a command fails, show the error output and suggest fixes (e.g., check the source URL, network).
- After installing, confirm success and mention where the skill was installed.
</guidelines>

<success_criteria>
- The requested skill operation completed successfully.
- Output was shown to the user confirming what happened.
- Scope and agent targeting matched user intent (project/global, correct agent).
</success_criteria>
