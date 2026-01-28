---
name: toutiao-publisher
description: Publish articles to Toutiao (Today's Headlines). Handles persistent authentication (login once) and session management. Opens browser for interactive publishing.
---

# Toutiao Publisher Skill

Manage Toutiao (Today's Headlines) account, maintain persistent login session, and publish articles.

## When to Use This Skill

Trigger when user:
- Asks to publish to Toutiao/Today's Headlines
- Wants to manage Toutiao login
- Mentions "toutiao" or "头条号"

## Core Workflow

### Step 1: Authentication (One-Time Setup)

The skill requires a one-time login. The session is persisted for subsequent uses.

```bash
# Browser will open for manual login (scan QR code)
python scripts/run.py auth_manager.py setup
```

**Instructions:**
1.  Run the setup command.
2.  A browser window will open loading the Toutiao login page.
3.  Log in manually (e.g., scan QR code).
4.  Once logged in (redirected to dashboard), the script will save the session and close.

### Step 2: Publish Article

```bash
# Opens browser with authenticated session at publish page
python scripts/run.py publisher.py
```

**Instructions:**
1.  Run the publisher command.
2.  Browser opens directly to the "Publish Article" page.
3.  Write and publish the article manually.
4.  Press `Ctrl+C` in the terminal when done.

> **Note:** Toutiao requires titles to be **2-30 characters**. This tool automatically optimizes titles to fit this constraint (truncating if >30, padding if <2).

#### Advanced Usage (Automated)

You can fully automate the publishing process by providing arguments:

```bash
# Publish with title, content file, and cover image
python scripts/run.py publisher.py --title "AI Trends 2025" --content "article.md" --cover "assets/cover.jpg" --headless
```



### Management

```bash
# Check authentication status
python scripts/run.py auth_manager.py status

# Clear authentication data (logout)
python scripts/run.py auth_manager.py clear
```

## Technical Details

- **Persistent Auth**: Uses `patchright` to launch a persistent browser context. Cookies and storage state are saved to `data/browser_state/state.json`.
- **Anti-Detection**: Uses `patchright`'s stealth features to avoid bot detection.
- **Environment**: Automatically manages a virtual environment (`.venv`) with required dependencies.

## Script Reference

- `scripts/auth_manager.py`: Handles login, session validation, and state persistence.
- `scripts/publisher.py`: Launches authenticated browser for publishing.
- `scripts/run.py`: Wrapper ensuring execution in the correct virtual environment.
