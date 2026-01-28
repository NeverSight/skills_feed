---
name: olakai-get-started
description: >
  Get started with Olakai - install, authenticate, and set up your first agent.

  AUTO-INVOKE when: CLI is not installed, user is not authenticated, user asks
  about getting started with Olakai, user wants to try Olakai, user mentions
  they don't have an account yet, or when other skills fail due to missing prerequisites.

  TRIGGER KEYWORDS: get started, setup, install olakai, olakai account, sign up,
  signup, new to olakai, try olakai, olakai onboarding, first agent, getting started,
  no account, create account, register.

  DO NOT load for: users who are already authenticated and have agents set up
  (use olakai-create-agent, olakai-add-monitoring, or olakai-troubleshoot instead).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Get Started with Olakai

This skill helps you get set up with Olakai from scratch - from creating an account to generating your first monitored event.

## Quick Status Check

Before proceeding, let's check your current setup status.

### Step 0: Detect Current State

Run these diagnostic commands to determine where to start:

```bash
# Check 1: Is CLI installed?
which olakai || echo "CLI_NOT_INSTALLED"

# Check 2: Is user authenticated?
olakai whoami 2>/dev/null || echo "NOT_AUTHENTICATED"

# Check 3: Are there any agents?
olakai agents list --json 2>/dev/null | head -5 || echo "NO_AGENTS_OR_NOT_AUTH"
```

**Based on results, jump to the appropriate section:**

| Result | Jump To |
|--------|---------|
| `CLI_NOT_INSTALLED` | [Step 1: Create Account](#step-1-create-an-olakai-account) |
| `NOT_AUTHENTICATED` | [Step 2: Install CLI](#step-2-install-the-cli) if CLI missing, else [Step 3: Authenticate](#step-3-authenticate) |
| Empty agents list | [Step 4: Create Your First Agent](#step-4-create-your-first-agent) |
| Agents exist | You're all set! Use `/olakai-create-agent` or `/olakai-add-monitoring` instead |

---

## Step 1: Create an Olakai Account

If you don't have an Olakai account yet, sign up at:

**https://app.olakai.ai/signup**

What you get:
- **Free tier** - Monitor up to 1,000 events/month
- **Dashboard** - Real-time visibility into AI usage
- **KPIs** - Track custom metrics across your agents
- **Governance** - Set policies and risk controls

After signing up, you'll have access to the dashboard where you can see your agents and events.

---

## Step 2: Install the CLI

The Olakai CLI is the primary tool for configuring agents, KPIs, and custom data.

### 2.1 Install via npm

```bash
npm install -g olakai-cli
```

### 2.2 Verify Installation

```bash
olakai --version
# Should output: olakai-cli/0.1.x
```

### 2.3 Troubleshooting Installation

**Permission errors on macOS/Linux:**
```bash
# Option 1: Use sudo (not recommended)
sudo npm install -g olakai-cli

# Option 2: Fix npm permissions (recommended)
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g olakai-cli
```

**Windows:**
```powershell
# Run PowerShell as Administrator
npm install -g olakai-cli
```

---

## Step 3: Authenticate

Connect the CLI to your Olakai account.

### 3.1 Login

```bash
olakai login
```

This opens your browser for secure authentication. After logging in:
- The CLI stores your session locally
- No API key needed for CLI operations
- Session persists until you explicitly logout

### 3.2 Verify Authentication

```bash
olakai whoami
```

Expected output:
```
Logged in as: your.email@example.com
Account: Your Organization
```

### 3.3 Troubleshooting Authentication

**"Not authenticated" errors:**
```bash
# Clear cached credentials and re-login
olakai logout
olakai login
```

**Browser doesn't open:**
```bash
# The CLI will display a URL - copy and paste it manually
olakai login
# Look for: "Open this URL in your browser: https://app.olakai.ai/..."
```

**Corporate proxy/firewall issues:**
- Ensure `app.olakai.ai` is accessible
- Check if your organization requires VPN

---

## Step 4: Create Your First Agent

An "agent" in Olakai represents any AI-powered feature you want to monitor.

### 4.1 Create the Agent

```bash
# Create agent with an API key for SDK integration
olakai agents create \
  --name "My First Agent" \
  --description "Testing Olakai integration" \
  --with-api-key \
  --json
```

**Save the output!** It contains your `apiKey` which you'll need for SDK integration:

```json
{
  "id": "cmkbteqn501kyjy4yu6p6xrrx",
  "name": "My First Agent",
  "apiKey": "sk_agent_xxxxx..."
}
```

### 4.2 Set the API Key as Environment Variable

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export OLAKAI_API_KEY="sk_agent_xxxxx..."
```

Or add to your project's `.env` file:
```
OLAKAI_API_KEY=sk_agent_xxxxx...
```

### 4.3 Retrieve API Key Later

If you need to get the API key again:
```bash
olakai agents get AGENT_ID --json | jq '.apiKey'
```

---

## Step 5: Install the SDK

Choose based on your project's language.

### TypeScript/JavaScript

```bash
npm install @olakai/sdk
```

**Quick Integration:**

```typescript
import { OlakaiSDK } from "@olakai/sdk";
import OpenAI from "openai";

// Initialize Olakai
const olakai = new OlakaiSDK({
  apiKey: process.env.OLAKAI_API_KEY!
});
await olakai.init();

// Wrap your OpenAI client
const openai = olakai.wrap(
  new OpenAI({ apiKey: process.env.OPENAI_API_KEY }),
  { provider: "openai" }
);

// Use as normal - events are automatically tracked
const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [{ role: "user", content: "Hello!" }]
});
```

### Python

```bash
pip install olakai-sdk
```

**Quick Integration:**

```python
import os
from openai import OpenAI
from olakaisdk import olakai_config, instrument_openai

# Initialize Olakai
olakai_config(os.getenv("OLAKAI_API_KEY"))
instrument_openai()

# Use OpenAI as normal - events are automatically tracked
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Step 6: Generate a Test Event

Let's verify everything is working.

### 6.1 Run Your Code

Execute the code from Step 5. This should:
1. Make an LLM call
2. Automatically send event data to Olakai

### 6.2 Fetch the Event

```bash
# List recent events (replace with your agent ID)
olakai activity list --limit 1 --json
```

### 6.3 Verify Event Details

```bash
# Get full event details
olakai activity get EVENT_ID --json | jq '{prompt, response, tokens, model}'
```

**Expected output:**
```json
{
  "prompt": "Hello!",
  "response": "Hello! How can I assist you today?",
  "tokens": 25,
  "model": "gpt-4"
}
```

### 6.4 Check the Dashboard

Open **https://app.olakai.ai** and navigate to your agent's activity view. You should see the event appear within seconds.

---

## Step 7: Next Steps

You're now set up! Here's what to explore next:

### Add Custom Data to Events

Track business-specific metrics:

```typescript
// TypeScript
const response = await openai.chat.completions.create(
  { model: "gpt-4", messages },
  {
    customData: {
      feature: "customer-support",
      ticketId: "TICKET-123",
      priority: 1
    }
  }
);
```

```python
# Python
from olakaisdk import olakai_context

with olakai_context(customData={"feature": "customer-support", "ticketId": "TICKET-123"}):
    response = client.chat.completions.create(...)
```

### Create KPIs

Define metrics that aggregate your custom data:

```bash
# First, create the custom data config
olakai custom-data create --name "Priority" --type NUMBER

# Then create a KPI
olakai kpis create \
  --name "High Priority Events" \
  --agent-id YOUR_AGENT_ID \
  --calculator-id formula \
  --formula "IF(Priority == 1, 1, 0)" \
  --aggregation SUM
```

> **Note:** KPIs are created per-agent. If you later create additional agents, you'll need to create KPIs for each one separately — they can't be shared across agents. CustomDataConfigs, on the other hand, are account-level and shared.

### Learn More

- **`/olakai-create-agent`** - Detailed guide for building agents with full observability
- **`/olakai-add-monitoring`** - Add monitoring to existing AI code
- **`/olakai-troubleshoot`** - Debug issues with events or KPIs

---

## Troubleshooting Quick Reference

### CLI Issues

| Problem | Solution |
|---------|----------|
| `command not found: olakai` | Reinstall CLI: `npm install -g olakai-cli` |
| `Not authenticated` | Run `olakai login` |
| `Network error` | Check internet connection, try again |

### SDK Issues

| Problem | Solution |
|---------|----------|
| `Invalid API key` | Verify `OLAKAI_API_KEY` env var is set correctly |
| `Events not appearing` | Check API key matches agent, verify network access |
| `Import errors` | Ensure SDK is installed: `npm install @olakai/sdk` or `pip install olakai-sdk` |

### Authentication Issues

| Problem | Solution |
|---------|----------|
| Browser doesn't open | Copy URL from terminal manually |
| Login succeeds but CLI says not authenticated | Try `olakai logout` then `olakai login` again |
| Corporate SSO issues | Contact your IT admin about OAuth access |

---

## Quick Reference

```bash
# Check status
which olakai              # CLI installed?
olakai whoami             # Authenticated?
olakai agents list        # Agents exist?

# Setup commands
npm install -g olakai-cli # Install CLI
olakai login              # Authenticate
olakai agents create --name "Name" --with-api-key --json  # Create agent

# SDK installation
npm install @olakai/sdk   # TypeScript
pip install olakai-sdk    # Python

# Verify events
olakai activity list --limit 1 --json
olakai activity get EVENT_ID --json
```

---

## Summary Checklist

- [ ] Account created at https://app.olakai.ai/signup
- [ ] CLI installed (`npm install -g olakai-cli`)
- [ ] CLI authenticated (`olakai login`)
- [ ] First agent created with API key
- [ ] `OLAKAI_API_KEY` environment variable set
- [ ] SDK installed (`@olakai/sdk` or `olakai-sdk`)
- [ ] Test event generated and visible in dashboard

Once all boxes are checked, you're ready to build production AI agents with full observability!
