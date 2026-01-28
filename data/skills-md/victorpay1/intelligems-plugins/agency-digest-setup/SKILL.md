---
name: agency-digest-setup
description: Get daily A/B test updates in Slack for multiple brands. Use when you want morning summaries of all your Intelligems tests, need to monitor tests across multiple stores or clients, or want automated Slack notifications with key metrics like revenue per visitor, profit per visitor, and conversion rates. Perfect for agencies managing multiple brands.
author: Victorpay1
version: 1.0.0
tags:
  - intelligems
  - slack
  - ab-testing
  - automation
  - ecommerce
---

# /agency-digest-setup

Create the complete Agency Morning Digest automation through conversation.

**What you'll get:**
- Daily Slack messages with all active A/B tests
- Key metrics: rev/visitor, profit/visitor, conversion, AOV
- Health indicators for tests needing attention
- One message per brand (ready to forward to clients)

---

## Setup Workflow

Follow these steps in order. Ask questions conversationally, then create files directly.

### Step 1: Project Directory

Ask where to create the project files.

Default: current working directory. If it's empty or home directory, suggest creating `~/Desktop/agency-morning-digest/`.

### Step 2: Slack Webhook

Ask: "Do you already have a Slack webhook URL, or do you need help creating one?"

**If they need help creating one:**

Guide them through:
1. Go to https://api.slack.com/apps
2. Click "Create New App" > "From scratch"
3. Name it "Agency Test Digest" and select workspace
4. Click "Incoming Webhooks" in sidebar
5. Toggle "Activate Incoming Webhooks" to On
6. Click "Add New Webhook to Workspace"
7. Select the channel and click "Allow"
8. Copy the webhook URL (starts with `https://hooks.slack.com/services/`)

**If using Chrome browser automation:** Offer to guide them through the Slack API website step by step.

Once they have the URL, save it for Step 4.

### Step 3: Brand Configuration

Ask: "What brands do you want to track? For each brand, I'll need a name and Intelligems API key."

Collect for each brand:
- **Brand name**: What shows in Slack (e.g., "Brand A", "Client Store")
- **API key**: Format is `ig_live_xxxxxxxxxx`

Allow multiple brands. Ask "Add another brand?" after each one.

If they don't have API keys, direct them to contact Intelligems support.

### Step 4: Create Files

Read the templates from `references/file-templates.md` and create these files in the project directory:

1. **agency_digest.py** - Main script (copy exactly from template)
2. **config.py** - Configuration with thresholds (copy from template)
3. **brands.json** - Fill in user's brand names and API keys
4. **`.env`** - Fill in user's Slack webhook URL
5. **requirements.txt** - Python dependencies (copy from template)
6. **`.gitignore`** - Protects credentials (copy from template)

### Step 5: Install Dependencies

Create a virtual environment and install dependencies:

```bash
cd {PROJECT_DIR}
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

This isolates packages and avoids conflicts with system Python.

### Step 6: Daily Scheduler (Optional, macOS only)

Ask: "Want to set up automatic daily messages at 8 AM?"

If yes:

1. Create the plist file at `~/Library/LaunchAgents/com.intelligems.agency-digest.plist` using template from `references/file-templates.md`
2. Replace `{PROJECT_DIR}` with the actual project path (uses venv Python automatically)
3. Load the scheduler: `launchctl load ~/Library/LaunchAgents/com.intelligems.agency-digest.plist`

Tell user: "Your computer needs to be on at 8 AM for the message to send."

### Step 7: Test

Ask: "Want to send a test message to Slack now?"

If yes, run:
```bash
./venv/bin/python3 agency_digest.py
```

If they want a preview first:
```bash
./venv/bin/python3 agency_digest.py --dry-run
```

### Step 8: Confirm Setup

Summarize what was created:
- Files location
- Brands configured
- Scheduler status
- Commands for later use

---

## Commands After Setup

```bash
# Send digest now (from project directory)
./venv/bin/python3 agency_digest.py

# Preview without sending
./venv/bin/python3 agency_digest.py --dry-run

# One combined message (instead of per-brand)
./venv/bin/python3 agency_digest.py --consolidated
```

---

## Adding More Brands Later

Edit `brands.json`:

```json
{
  "brands": [
    {"name": "Brand A", "display_name": "Brand A", "api_key": "ig_live_xxx"},
    {"name": "Brand B", "display_name": "Brand B", "api_key": "ig_live_yyy"}
  ]
}
```

---

## Customizing Thresholds

Edit `config.py`:

| Setting | Default | Purpose |
|---------|---------|---------|
| `MIN_RUNTIME_DAYS` | 10 | Days before calling winners |
| `MIN_CONFIDENCE_LEVEL` | 0.80 | 80% confidence threshold |
| `MIN_SESSIONS_FOR_SIGNIFICANCE` | 100 | Minimum visitors |
| `NEUTRAL_LIFT_THRESHOLD` | 0.05 | ±5% considered flat |

---

## Troubleshooting

**No Slack message?**
- Check `/tmp/agency-digest.log` for errors
- Verify webhook URL in `.env`
- Run with `--dry-run` to preview

**Scheduler not running (macOS)?**
```bash
launchctl list | grep agency-digest
```

**API errors?**
- Verify API key format: `ig_live_xxxxxxxxxx`
- Contact Intelligems support for access
