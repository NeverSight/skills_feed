---
name: canifi-skill-generator
description: Self-evolving skill that enables Canifi to create, install, and manage new skills autonomously
category: development
version: 1.0.0
author: Canifi LifeOS
required: true
---

# Canifi Skill Generator

## Overview

The Skill Generator is a meta-skill that enables Canifi to **create new skills for itself** and automatically install them to the global skills directory. This transforms Canifi from a static assistant into a self-evolving system that can expand its own capabilities on demand.

**Why This Skill is Required:**
- Enables Canifi to learn new workflows without manual skill creation
- Allows real-time capability expansion during conversations
- Creates a feedback loop where Canifi improves itself over time
- Reduces dependency on pre-built skills for niche use cases

---

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Global Skills Directory

Skills are installed to: `~/.claude/skills/`

Each skill lives in its own directory:
```
~/.claude/skills/
├── canifi/
│   └── SKILL.md
├── canifi-skill-generator/
│   └── SKILL.md
├── my-new-skill/
│   └── SKILL.md
└── ...
```

---

## Capabilities

### 1. Create New Skills on Demand

When a user requests a capability that doesn't exist, or when Canifi identifies a repeated pattern that could be automated:

```
User: "I need to interact with Airtable regularly"
Canifi: "I don't have an Airtable skill yet. Would you like me to create one?"
User: "Yes, please"
Canifi: [Creates and installs airtable skill]
```

### 2. Auto-Generate Skills from Patterns

When Canifi notices it's performing the same complex workflow repeatedly:

```
Canifi: "I've noticed we've done this Slack → Notion workflow 5 times.
        Should I create a skill for this so it's faster next time?"
```

### 3. Modify Existing Skills

Update skills based on user feedback or changed requirements:

```
User: "The github skill should also support GitLab"
Canifi: [Updates the skill to support both platforms]
```

### 4. Research-Driven Skill Creation

For unfamiliar services, Canifi can:
1. Research the service's API/documentation
2. Identify common use cases
3. Generate a comprehensive skill
4. Test basic functionality
5. Install and activate

---

## Skill Template

When generating a new skill, use this template structure:

```markdown
---
name: {skill-id}
description: {One-line description}
category: {category}
version: 1.0.0
author: Canifi LifeOS (Auto-Generated)
---

# {Skill Name}

## Overview

{2-3 sentence description of what this skill does and why it's useful}

---

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to {SERVICE_NAME} manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials:
```bash
canifi-env set {SERVICE}_EMAIL "your-email"
canifi-env set {SERVICE}_PASSWORD "your-password"
# OR for API-based services:
canifi-env set {SERVICE}_API_KEY "your-api-key"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine.

## Setup

{Required setup steps, environment variables, API keys, etc.}

## Capabilities

{List of what this skill enables}

## Usage Examples

{Common use case examples}

## Workflow

{Step-by-step workflow when using this skill}

## Troubleshooting

{Common issues and solutions}
```

---

## Skill Generation Workflow

### Step 1: Identify Need

Triggers for skill creation:
- User explicitly requests a new capability
- User asks about a service Canifi doesn't have a skill for
- Canifi identifies a repeated manual workflow
- User shares API documentation or service details

### Step 2: Research (if needed)

For unfamiliar services:
1. Use Gemini Deep Research via Playwright MCP
2. Find official API documentation
3. Identify authentication methods
4. Discover common use cases
5. Note any rate limits or restrictions

### Step 3: Generate Skill Content

Create the SKILL.md file with:
- Accurate metadata (name, description, category)
- Clear setup instructions
- Privacy & Authentication section (REQUIRED)
- Comprehensive capabilities list
- Practical usage examples
- Troubleshooting guidance

### Step 4: Install Skill

```bash
# Create skill directory
mkdir -p ~/.claude/skills/{skill-id}

# Write SKILL.md
cat > ~/.claude/skills/{skill-id}/SKILL.md << 'EOF'
{skill content}
EOF
```

### Step 5: Verify Installation

```bash
# Check skill exists
ls -la ~/.claude/skills/{skill-id}/

# Verify content
cat ~/.claude/skills/{skill-id}/SKILL.md
```

### Step 6: Confirm to User

```
Skill "{skill-name}" has been created and installed.

Location: ~/.claude/skills/{skill-id}/SKILL.md
Category: {category}

You can now use this skill by {activation instructions}.

Would you like me to demonstrate it?
```

---

## Category Reference

Use these categories when generating skills:

| Category | Description | Examples |
|----------|-------------|----------|
| `productivity` | Task management, notes, organization | Notion, Todoist, Obsidian |
| `communication` | Messaging, email, social | Slack, Discord, Gmail |
| `development` | Code, CI/CD, repositories | GitHub, GitLab, Vercel |
| `automation` | Workflows, integrations | Zapier, Make, n8n |
| `data` | Databases, analytics, storage | Airtable, Supabase, S3 |
| `ai` | AI services, ML platforms | OpenAI, Anthropic, HuggingFace |
| `finance` | Banking, payments, crypto | Stripe, Plaid, Coinbase |
| `media` | Images, video, audio | Figma, YouTube, Spotify |
| `health` | Fitness, wellness, medical | Apple Health, Oura, Whoop |
| `smart-home` | IoT, home automation | HomeKit, SmartThings, IFTTT |
| `travel` | Booking, maps, transport | Google Maps, Uber, Airbnb |
| `education` | Learning, courses, research | Coursera, Anki, Zotero |
| `shopping` | E-commerce, deals, inventory | Amazon, Shopify, eBay |
| `gaming` | Games, streaming, communities | Steam, Twitch, Discord |
| `security` | Auth, passwords, privacy | 1Password, Authy, VPNs |

---

## Auto-Generation Triggers

Canifi should proactively offer to create skills when:

### Explicit Requests
- "Can you help me with [Service]?"
- "I need to integrate [Platform]"
- "How do I automate [Workflow]?"

### Implicit Patterns
- User mentions a service 3+ times in conversation
- User describes a multi-step workflow manually
- User asks "Is there a skill for...?"

### Capability Gaps
- When Canifi says "I don't have direct access to..."
- When a task requires manual user intervention
- When existing skills don't cover a use case

---

## Example: Creating a Skill

### User Request
```
"I want Canifi to help me manage my Todoist tasks"
```

### Canifi Response
```
I don't have a Todoist skill yet. Let me create one for you.

[Researching Todoist API and best practices...]
[Generating skill content...]
[Installing to ~/.claude/skills/todoist/]

Done! I've created and installed the Todoist skill.

**Capabilities:**
- List tasks and projects
- Create new tasks with due dates
- Complete/uncomplete tasks
- Organize tasks into projects
- Set priorities and labels

**Setup Required:**
You'll need to get a Todoist API token from:
https://todoist.com/app/settings/integrations/developer

Then set it with:
```bash
canifi-env set TODOIST_API_KEY "your-token-here"
```

Would you like me to demonstrate by listing your current tasks?
```

---

## Skill Quality Guidelines

When generating skills, ensure:

### 1. Completeness
- All sections from template are included
- Privacy & Authentication section is ALWAYS present
- Setup steps are clear and actionable
- Examples cover common use cases

### 2. Accuracy
- API endpoints and methods are correct
- Authentication flows match service requirements
- Rate limits and restrictions are noted
- Error handling is addressed

### 3. Usability
- Instructions are beginner-friendly
- Commands can be copy-pasted
- Examples show expected outputs
- Troubleshooting covers common issues

### 4. Safety
- Never hardcode credentials
- Always use environment variables
- Include privacy warnings where appropriate
- Note any data handling considerations

---

## Managing Installed Skills

### List All Skills
```bash
ls ~/.claude/skills/
```

### View Skill Content
```bash
cat ~/.claude/skills/{skill-id}/SKILL.md
```

### Update a Skill
```bash
# Edit directly or regenerate
cat > ~/.claude/skills/{skill-id}/SKILL.md << 'EOF'
{updated content}
EOF
```

### Remove a Skill
```bash
rm -rf ~/.claude/skills/{skill-id}
```

---

## Troubleshooting

### Skill Not Recognized
- Verify the skill directory exists: `ls ~/.claude/skills/{skill-id}/`
- Check SKILL.md has correct frontmatter with `name` field
- Restart Claude Code to reload skills

### Permission Errors
- Ensure write access: `chmod -R u+w ~/.claude/skills/`
- Check directory ownership: `ls -la ~/.claude/`

### Skill Not Working
- Verify all required environment variables are set
- Check service API is accessible
- Review troubleshooting section of the specific skill

---

## Universal Rules for Generated Skills

1. **Privacy First** - Always include Privacy & Authentication section
2. **Never Hardcode** - All credentials use environment variables
3. **Clear Setup** - Users should be able to follow setup without confusion
4. **Practical Examples** - Show real use cases, not abstract concepts
5. **Error Guidance** - Include troubleshooting for common issues
6. **Version Track** - Include version in metadata for updates
7. **Attribution** - Mark auto-generated skills with `author: Canifi LifeOS (Auto-Generated)`
