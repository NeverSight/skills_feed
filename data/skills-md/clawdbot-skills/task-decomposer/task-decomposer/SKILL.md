---
name: task-decomposer
description: Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills at skills.sh, and creates new skills when no solution exists. This skill should be used when the user submits a complex multi-step request, wants to automate workflows, or needs help breaking down large tasks into manageable pieces.
---

# Task Decomposer & Skill Generator

This skill helps decompose complex user requests into executable subtasks, identify required capabilities for each task, search for existing skills from the open skills ecosystem, and automatically create new skills when no existing solution is available.

## Core Workflow

```
User Request → Task Decomposition → Capability Identification → Skill Search → Gap Analysis → Skill Creation → Execution Plan
```

## Phase 1: Task Analysis & Decomposition

When receiving a user request, follow these steps:

### Step 1: Understand User Intent

Analyze the request to identify:
- **Core objective**: What is the end goal?
- **Domains involved**: What areas of expertise are needed?
- **Trigger mechanism**: One-time, scheduled, or event-driven?

Example analysis:
```
User Input: "Help me get email summaries every morning and send them to Slack"

Analysis:
- Core objective: Automated email digest delivery to Slack
- Domains: Email access, content summarization, messaging
- Trigger: Scheduled (daily morning)
```

### Step 2: Decompose into Atomic Tasks

Break down the complex task into minimal executable units:

```yaml
Task Decomposition:
  - task_id: 1
    name: "Access and retrieve email list"
    type: "data_retrieval"
    input: "Email credentials/session"
    output: "List of emails with metadata"
    dependencies: []
    
  - task_id: 2
    name: "Extract key information from emails"
    type: "data_extraction"
    input: "Email list"
    output: "Structured email data"
    dependencies: [1]
    
  - task_id: 3
    name: "Generate email summary"
    type: "content_generation"
    input: "Structured email data"
    output: "Formatted summary text"
    dependencies: [2]
    
  - task_id: 4
    name: "Send message to Slack"
    type: "message_delivery"
    input: "Summary text, Slack webhook/token"
    output: "Delivery confirmation"
    dependencies: [3]
    
  - task_id: 5
    name: "Configure scheduled execution"
    type: "scheduling"
    input: "Workflow script, schedule config"
    output: "Active scheduled job"
    dependencies: [4]
```

## Phase 2: Capability Identification

Map each subtask to a capability type from the universal capability taxonomy.

### Universal Capability Types

| Capability | Description | Search Keywords |
|------------|-------------|-----------------|
| `browser_automation` | Web navigation, interaction, scraping | browser, selenium, puppeteer, playwright, scrape |
| `web_search` | Internet search and information retrieval | search, google, bing, duckduckgo |
| `api_integration` | Third-party API communication | api, rest, graphql, webhook, {service-name} |
| `data_extraction` | Parse and extract structured data | parse, extract, scrape, ocr, pdf |
| `data_transformation` | Convert, clean, transform data | transform, convert, format, clean, etl |
| `content_generation` | Create text, images, or other content | generate, write, create, summarize, translate |
| `file_operations` | Read, write, manipulate files | file, read, write, csv, excel, json, pdf |
| `message_delivery` | Send notifications or messages | notify, send, email, slack, discord, telegram |
| `scheduling` | Time-based task execution | schedule, cron, timer, daily, weekly |
| `authentication` | Identity and access management | auth, oauth, login, token, credentials |
| `database_operations` | Database CRUD operations | database, sql, mongodb, query, store |
| `code_execution` | Run scripts or programs | execute, run, script, shell, python |
| `version_control` | Git and code repository operations | git, github, gitlab, commit, pr, review |
| `testing` | Automated testing and QA | test, jest, pytest, e2e, unit |
| `deployment` | Application deployment and CI/CD | deploy, docker, kubernetes, ci-cd, release |
| `monitoring` | System and application monitoring | monitor, alert, log, metrics, health |

### Capability Identification Process

For each subtask:
1. Analyze the task description and requirements
2. Match to one or more capability types
3. Generate search keywords for skill discovery

Example:
```yaml
Task: "Send message to Slack"
Capability: message_delivery
Search Keywords: ["slack", "notification", "message", "webhook"]
```

## Phase 3: Skill Search

Use the Skills CLI to search for existing skills at https://skills.sh/

### Search Process

For each capability need, search using relevant keywords:

```bash
# Search for skills matching the capability
npx skills find <keyword>

# Examples:
npx skills find slack notification
npx skills find browser automation
npx skills find pdf extract
npx skills find github api
```

### Evaluate Search Results

When results are returned:
```
Install with npx skills add <owner/repo@skill>

owner/repo@skill-name
└ https://skills.sh/owner/repo/skill-name
```

Evaluate each result for:
- **Relevance**: Does it match the required capability?
- **Completeness**: Does it cover all needed functionality?
- **Quality**: Is it well-documented and maintained?

### Generate Capability Mapping

```yaml
Capability Mapping:
  - task_id: 1
    capability: browser_automation
    search_query: "browser email automation"
    found_skills:
      - name: "anthropic/claude-skills@browser-use"
        url: "https://skills.sh/anthropic/claude-skills/browser-use"
        match_score: high
    recommendation: "Install browser-use skill"
    
  - task_id: 4
    capability: message_delivery
    search_query: "slack notification"
    found_skills: []
    recommendation: "Create new skill: slack-notification"
```

## Phase 4: Gap Analysis

Identify tasks without matching skills:

### Built-in Capabilities (No Skill Needed)

These capabilities are typically handled by the agent's native abilities:
- `content_generation` - LLM's native text generation
- `data_transformation` - Basic data manipulation via code
- `code_execution` - Direct script execution
- `scheduling` - System-level cron/scheduler configuration

### Skills Required

For capabilities without built-in support, determine:
1. **Skill exists**: Install from skills.sh
2. **Skill not found**: Create new skill

## Phase 5: Skill Creation

When no existing skill matches a required capability, create a new skill.

### Skill Creation Process

1. **Define scope**: Determine what the skill should do
2. **Design interface**: Define inputs, outputs, and usage patterns
3. **Create SKILL.md**: Write the skill definition file
4. **Add resources**: Include scripts, references, or assets as needed

### Skill Template

```markdown
---
name: {skill-name}
description: {Clear description of what the skill does and when to use it. Written in third person.}
---

# {Skill Title}

{Brief introduction explaining the skill's purpose.}

## When to Use

{Describe scenarios when this skill should be triggered.}

## Prerequisites

{List any required installations, configurations, or credentials.}

## Usage

{Detailed usage instructions with examples.}

### Basic Usage

```bash
{Basic command or code example}
```

### Advanced Usage

{More complex examples and options.}

## Configuration

{Any configuration options or environment variables.}

## Examples

### Example 1: {Use Case}

{Step-by-step example with code.}

## Troubleshooting

{Common issues and solutions.}
```

### Initialize New Skill

```bash
# Create skill using the skills CLI
npx skills init <skill-name>

# Or manually create the structure:
# skill-name/
# ├── SKILL.md (required)
# ├── scripts/ (optional)
# ├── references/ (optional)
# └── assets/ (optional)
```

## Phase 6: Generate Execution Plan

Compile all information into a structured execution plan:

```yaml
Execution Plan:
  title: "{Task Description}"
  
  prerequisites:
    - "{Prerequisite 1}"
    - "{Prerequisite 2}"
  
  skills_to_install:
    - skill: "owner/repo@skill-name"
      command: "npx skills add owner/repo@skill-name -g -y"
      url: "https://skills.sh/owner/repo/skill-name"
  
  skills_to_create:
    - name: "{new-skill-name}"
      capability: "{capability_type}"
      description: "{What it does}"
  
  execution_steps:
    - step: 1
      task: "{Task name}"
      skill: "{skill-name | built-in}"
      action: "{Specific action to take}"
      
    - step: 2
      task: "{Task name}"
      skill: "{skill-name | built-in}"
      action: "{Specific action to take}"
  
  verification:
    - "{How to verify step 1 succeeded}"
    - "{How to verify step 2 succeeded}"
```

## Task Decomposition Principles

### Principle 1: Atomicity
Each subtask should be the minimal executable unit with clear input and output.

### Principle 2: Independence
Minimize dependencies between tasks to allow parallel execution where possible.

### Principle 3: Verifiability
Each task should have a clear way to verify successful completion.

### Principle 4: Reusability
Identify reusable patterns and prefer creating general-purpose skills.

### Principle 5: Single Responsibility
Each task should do one thing well.

## Output Format

Present the decomposition results in a structured format:

```
════════════════════════════════════════════════════════════════
📋 TASK DECOMPOSITION REPORT
════════════════════════════════════════════════════════════════

🎯 Original Request:
{User's original request}

────────────────────────────────────────────────────────────────
📊 SUBTASKS
────────────────────────────────────────────────────────────────
┌─────┬────────────────────────┬───────────────────┬───────────┐
│ ID  │ Task                   │ Capability        │ Status    │
├─────┼────────────────────────┼───────────────────┼───────────┤
│ 1   │ {task name}            │ {capability}      │ Found     │
│ 2   │ {task name}            │ {capability}      │ Built-in  │
│ 3   │ {task name}            │ {capability}      │ Create    │
└─────┴────────────────────────┴───────────────────┴───────────┘

────────────────────────────────────────────────────────────────
🔍 SKILL SEARCH RESULTS
────────────────────────────────────────────────────────────────
Task 1: {task name}
  Search: npx skills find {keywords}
  Found: owner/repo@skill-name
  URL: https://skills.sh/owner/repo/skill-name
  
Task 3: {task name}
  Search: npx skills find {keywords}
  Found: No matching skills
  Action: Create new skill

────────────────────────────────────────────────────────────────
🛠️ SKILLS TO CREATE
────────────────────────────────────────────────────────────────
1. {skill-name}
   Capability: {capability_type}
   Description: {what it does}

────────────────────────────────────────────────────────────────
📝 EXECUTION PLAN
────────────────────────────────────────────────────────────────
Prerequisites:
  • {prerequisite 1}
  • {prerequisite 2}

Steps:
  1. {action} using {skill}
  2. {action} using {skill}
  3. {action} using {skill}

════════════════════════════════════════════════════════════════
```

## Examples

### Example 1: Workflow Automation

**User Request:**
```
Create a workflow that monitors GitHub issues, summarizes new issues, and posts notifications to Discord
```

**Decomposition:**
```yaml
Subtasks:
  1. Monitor GitHub repository for new issues
     Capability: api_integration
     Search: "npx skills find github issues"
     
  2. Extract issue content and metadata
     Capability: data_extraction
     Status: Built-in (code)
     
  3. Generate issue summary
     Capability: content_generation
     Status: Built-in (LLM)
     
  4. Send notification to Discord
     Capability: message_delivery
     Search: "npx skills find discord notification"
     
  5. Configure webhook or polling trigger
     Capability: scheduling
     Status: Built-in (system)
```

### Example 2: Data Pipeline

**User Request:**
```
Search for AI research papers, download PDFs, extract key findings, and save to Notion
```

**Decomposition:**
```yaml
Subtasks:
  1. Search for AI research papers
     Capability: web_search
     Search: "npx skills find academic search"
     
  2. Download PDF files
     Capability: browser_automation
     Search: "npx skills find browser download"
     
  3. Extract text from PDFs
     Capability: data_extraction
     Search: "npx skills find pdf extract"
     
  4. Generate summaries of key findings
     Capability: content_generation
     Status: Built-in (LLM)
     
  5. Save to Notion database
     Capability: api_integration
     Search: "npx skills find notion"
```

## Best Practices

1. **Start with skill search**: Always check https://skills.sh/ before creating new skills
2. **Use specific search terms**: Combine capability keywords with domain terms
3. **Leverage built-in capabilities**: Don't create skills for things the agent can do natively
4. **Create reusable skills**: Design new skills to be general-purpose when possible
5. **Document thoroughly**: New skills should have clear usage instructions
6. **Verify before proceeding**: Confirm skill installation before executing tasks
7. **Handle errors gracefully**: Include fallback strategies in execution plans

## Integration with find-skills

This skill works in conjunction with the `find-skills` skill for discovering existing solutions:

```bash
# Search the skills ecosystem
npx skills find <query>

# Install a discovered skill
npx skills add <owner/repo@skill> -g -y

# Browse all available skills
# Visit: https://skills.sh/
```

## Notes

- Always search for existing skills before creating new ones
- Built-in capabilities (LLM, basic code) don't require skills
- Skill creation requires user confirmation before proceeding
- Complex workflows may need multiple skills working together
