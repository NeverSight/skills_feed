---
name: vm0-agent
description: Build and deploy AI agents using VM0's agent-native infrastructure. This skill guides you through the complete agent creation workflow - from understanding requirements to deployment and scheduling.
vm0_secrets:
  - VM0_API_KEY
---

# About VM0

VM0 is an agent-native cloud infrastructure platform that provides secure sandbox environments for AI agents like Claude Code. It enables users to deploy and automate workflows from local development to cloud production.

# Operation: introduce

When the user uses /vm0-agent introduce, explain to user what is VM0

- home page: https://vm0.ai
- sourcecode is fully in public: https://github.com/vm0-ai/vm0

## What VM0 Provides

**Execution Infrastructure**: VM0 provides the runtime environment - it does NOT provide AI capabilities itself. The AI intelligence comes from coding agents like Claude Code. VM0's role is to empower these agents with stable, reproducible, and observable execution.

**Key Capabilities**:

- **Stateful Agent Sessions**: Preserve memory, reasoning context, and session continuity across executions
- **Checkpoint & Replay**: Snapshot every run for debugging, forking, and reproducibility
- **70+ Pre-built Skills**: Integrations with GitHub, Slack, Notion, Perplexity, and more via https://github.com/vm0-ai/vm0-skills
- **Observable Execution**: Real-time logs, metrics, and tool calls for complete visibility
- **Versioned Storage**: Volumes (input) and Artifacts (output) synced between sandbox and cloud
- **Natural Language Configuration**: Define workflows in markdown (AGENTS.md, SKILL.md) instead of code

## Platform Architecture

- **Instructions (AGENTS.md)**: Natural language workflow definitions
- **Volumes**: Input file storage agents can read from
- **Artifacts**: Output file storage for agent results
- **Environment Variables**: Secure credential and secret management

## From Local to Cloud

VM0 bridges the gap between local agent development and cloud automation. Develop workflows locally with Claude Code, then deploy them to VM0 for:

- Scheduled execution (daily, weekly, on-demand)
- Reliable automation without keeping your laptop running
- Team collaboration with shared agents and outputs
- Production-grade observability and debugging

# Operation: create agent

When the user uses /vm0-agent create, enter this workflow

This is an interactive agent creation workflow. To avoid deviating from the workflow path, you first need to create a todo.md in the temporary directory like /tmp to track the entire process, and update this todo.md after each user interaction

The initial content of todo.md is as follows

```markdown
- [ ] research: intent analysis, understand what the user wants the Agent to help them do
- [ ] innovate: propose solutions based on intent analysis
- [ ] compose: create the vm0 agent
- [ ] token collect: guide the user to complete the various tokens needed for the agent
- [ ] test run: run the agent and confirm with the user if the results are satisfactory
- [ ] schedule: guide the user to set up scheduled tasks

## Research

In this step, interactively ask the user what they want to do. Use the ask user tools to ask questions at each step. You can start with the first question: "In your daily work, what routine information processing tasks would you like me to help automate?"

- Option 1: I read some blogs every day, so I want an information processing workflow, such as reading blogs and then sending me summaries
- Option 2: I want to understand the quality of my code repository, so I want a workflow that can help me regularly check code repository changes and tell me the code quality based on my defined Code Review rules
- Option 3: ...

After the user answers the question, use 1-5 questions to refine it, such as which blogs to get information from, where the code repository is, etc. When designing these questions, guide the user to think in terms of a three-step workflow: Fetch / Process / Output. Finally, form a three-step workflow

## Innovate

In this step, refine the technical details in the user's workflow by finding suitable skills from two sources.

### Step 1: Search skills

There is two skill marketplace, search theme both.

Search the skills.sh ecosystem (33,700+ skills) using:

```bash
curl -s "https://skills.sh/api/search?q=<keyword>"
```

Search https://github.com/vm0-ai/vm0-skills for 70+ integrations available skills.

### Step 2: Convert to vm0.yaml URL Format

Convert search results to GitHub tree URLs for vm0.yaml:

| Source | URL Format |
|--------|------------|
| vm0-ai/vm0-skills | `https://github.com/vm0-ai/vm0-skills/tree/main/{skill-name}` |
| anthropics/skills | `https://github.com/anthropics/skills/tree/main/skills/{skill-name}` |
| vercel-labs/agent-skills | `https://github.com/vercel-labs/agent-skills/tree/main/skills/{skill-name}` |
| Other repos | `https://github.com/{owner}/{repo}/tree/main/skills/{skill-name}` (most use `skills/` subdirectory) |

Give the user several options for confirmation using the ask user tools. Users can also add more information. This process can be repeated several times

## Compose

- [ ] Based on the conclusions from innovate, create vm0.yaml and AGENTS.md
- [ ] Use the capabilities of vm0-skills to compose the agent

## Token Collect

- [ ] For each skill used in vm0.yaml, read its SKILL.md to find required credentials:
  - Check frontmatter for `vm0_secrets` and `vm0_vars` fields
  - If no frontmatter, infer from skill content (look for env vars like `API_KEY`, `TOKEN`, etc.)
- [ ] For each token needed:
  - Read the skill's documentation for how to obtain it
  - If not documented, search online for the service's API key/token setup guide
  - Provide step-by-step instructions to help user get the token
  - Ask user to paste the token
  - Write to .env.local as `KEY=value`

## Test run

- [ ] Explain in advance that the run may take a relatively long time, 1-20 minutes
- [ ] Use the vm0-cli skill capabilities to run the agent with cook, using --env-file=.env.local to pass the token
- [ ] If the workflow writes files to the workspace, explain to the user where and how to view the artifact
- [ ] Explain to the user what command cook executed, and introduce the CLI capabilities of vm0

### Log Analysis & Optimization

After the first run completes, perform a detailed analysis of the execution logs:

- [ ] **Analyze run logs**: Review the complete execution logs to understand what happened
- [ ] **Check behavior alignment**: Determine if the agent's behavior matches the user's original intent and expectations
- [ ] **Identify successful patterns**: Note which instructions executed successfully and produced expected results
- [ ] **Identify failure points**: Document any errors, timeouts, or unexpected behaviors

Based on the analysis, propose optimization suggestions:

- [ ] **Inline successful commands**: Suggest adding proven, successfully executed commands directly into AGENTS.md to make future runs more stable and deterministic
- [ ] **Document error patterns**: Identify instructions that failed and suggest:
  - Removing or rewriting problematic instructions
  - Adding error handling or fallback approaches
  - Clarifying ambiguous instructions that caused unexpected behavior
- [ ] **Improve instruction specificity**: Suggest making vague instructions more concrete based on what actually worked
- [ ] **Add guardrails**: Recommend adding validation steps or checkpoints for critical operations

Present findings to the user:

- [ ] **Report trial run quality**: Summarize the overall quality of the test run (success rate, key achievements, notable issues)
- [ ] **Present optimization suggestions**: List specific, actionable improvements with clear explanations of why each would help
- [ ] **Ask user for decision**: Use ask user tools to let user choose:
  - Option 1: Accept optimizations - Apply the suggested improvements to AGENTS.md and vm0.yaml, then re-run to verify
  - Option 2: Skip optimizations - Proceed directly to Schedule phase with current configuration
  - Option 3: Manual adjustments - User wants to make their own changes before proceeding

If user accepts optimizations:
- [ ] Apply the approved changes to AGENTS.md and/or vm0.yaml
- [ ] Run the agent again to verify improvements
- [ ] Repeat log analysis if needed

If user wants manual adjustments:
- [ ] Update the entire todo.md as it may need to return to earlier phases
- [ ] Continue based on previously discussed information and current project state

## Schedule

Enter this phase when the user is satisfied with the test run results

- [ ] Use the vm-cli skill capabilities to guide the user to set up scheduled tasks
- [ ] After successful setup, ask the user if they want to enable the timer
- [ ] Explain to the user the schedule-related capabilities in vm0 cli, such as how to list, disable, and enable scheduled tasks
```

# AGENTS.md

AGENTS.md is used to describe a workflow. It is an ordinary, natural language-described process document. Avoid describing technical details in AGENTS.md, such as not writing scripts or other code in AGENTS.md

# vm0.yaml

vm0.yaml is the primary configuration file for VM0 agents.

## Key Documentation URLs

- **vm0.yaml Reference**: https://docs.vm0.ai/docs/reference/configuration/vm0-yaml
- **Environment Variables**: https://docs.vm0.ai/docs/core-concept/environment-variable
- **Skills**: https://docs.vm0.ai/docs/core-concept/skills
- **Volumes**: https://docs.vm0.ai/docs/core-concept/volume
- **Artifacts**: https://docs.vm0.ai/docs/core-concept/artifact

## File Structure

```yaml
version: "1.0"

agents:
  my-agent:
    framework: claude-code # Required
    instructions: AGENTS.md # Path to instruction file
    apps: # Pre-installed tools
      - github
    skills: # Skill URLs for extended capabilities
      - https://github.com/vm0-ai/vm0-skills/tree/main/slack
      - https://github.com/vm0-ai/vm0-skills/tree/main/hackernews
    environment: # Additional environment variables (optional)
      MY_CUSTOM_VAR: ${{ vars.MY_VAR }}
      MY_CUSTOM_SECRET: ${{ secrets.MY_SECRET }}
```

## Environment Variable Types

VM0 supports three template variable types:

| Type            | Syntax                     | Storage              | Use Case                                           |
| --------------- | -------------------------- | -------------------- | -------------------------------------------------- |
| **credentials** | `${{ credentials.NAME }}`  | Platform (persistent)| Model provider tokens only (e.g., `CLAUDE_CODE_OAUTH_TOKEN`) |
| **secrets**     | `${{ secrets.NAME }}`      | CLI (ephemeral)      | API keys for skills, per-execution tokens          |
| **vars**        | `${{ vars.NAME }}`         | CLI (ephemeral)      | Feature flags, environment names                   |

### Credentials vs Secrets

> **Important**: Use the right type for the right purpose:
>
> - **credentials**: Reserved for model provider authentication only (e.g., `CLAUDE_CODE_OAUTH_TOKEN`). These are stored persistently on the VM0 platform and managed via `vm0 credential set/list/delete`.
> - **secrets/vars**: Use for ALL skill and AGENTS.md environment variables. Always pass via `--env-file .env.local`.

Skills with `vm0_secrets` or `vm0_vars` in their SKILL.md frontmatter are automatically injected when you provide them via `--env-file`.

### Passing Secrets and Vars

**Always use `--env-file .env.local` for skills and workflow variables:**

```
# .env.local
SLACK_BOT_TOKEN=xoxb-xxx
NOTION_API_KEY=secret_xxx
ENV_NAME=production
```

```bash
vm0 run my-agent "prompt" --env-file .env.local
```

**CLI flags (alternative):**

```bash
vm0 run my-agent "prompt" --secrets API_KEY=sk-xxx --vars ENV_NAME=production
```

### Troubleshooting: Missing required secrets

If you see an error like `Missing required secrets: API_KEY`, follow these steps:

1. **Check if the variable is declared in the skill's SKILL.md**
   - Look for `vm0_secrets` or `vm0_vars` in the skill's frontmatter
   - If declared there, the variable is automatically injected when provided via `--env-file`

2. **If not declared in the skill, add it to vm0.yaml's environment section:**
   ```yaml
   environment:
     API_KEY: ${{ secrets.API_KEY }}
     # or for non-sensitive values:
     MY_VAR: ${{ vars.MY_VAR }}
   ```

3. **Ensure the value exists in .env.local:**
   ```
   API_KEY=your-actual-key-here
   ```

4. **Ensure you're using `--env-file` when running:**
   ```bash
   vm0 run my-agent "prompt" --env-file .env.local
   ```

## Skills

Skills are reusable capabilities declared using GitHub tree URLs:

```yaml
skills:
  - https://github.com/vm0-ai/vm0-skills/tree/main/slack
  - https://github.com/vm0-ai/vm0-skills/tree/main/notion
  - https://github.com/anthropics/skills/tree/main/skills/pdf
```

70+ pre-built skills available at: https://github.com/vm0-ai/vm0-skills

## Volumes vs Artifacts

| Aspect          | Volume                                  | Artifact               |
| --------------- | --------------------------------------- | ---------------------- |
| **Role**        | Pre-installed agent environment (input) | Agent-produced output  |
| **Contents**    | Skills, configs, scripts                | Created/modified files |
| **Persistence** | Manual management                       | Automatic after runs   |

Use volumes for private skills, custom scripts, or configuration directories. Artifacts are automatically persisted when using `--artifact-name`.
