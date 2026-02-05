---
name: notte-browser
description: Command-line interface for browser automation, web scraping, and AI-powered web interactions using the notte.cc platform.
version: 1.0.0
allowed-tools: Bash(notte:*)
---

# Notte Browser CLI Skill

Command-line interface for browser automation, web scraping, and AI-powered web interactions using the notte.cc platform.

## Quick Start

```bash
# 1. Authenticate
notte auth login

# 2. Start a browser session
notte sessions start

# 3. Navigate and observe
notte page goto "https://example.com"
notte page observe
notte page screenshot

# 4. Execute actions (use @IDs from observe, or Playwright selectors)
notte page click "@B3"
notte page fill "@I1" "hello world"
# If @IDs don't work, use Playwright selectors:
# notte page click "button:has-text('Submit')"

# 5. Scrape content
notte page scrape --instructions "Extract all product names and prices"

# 6. Stop the session
notte sessions stop
```

## Command Categories

### Session Management

Control browser session lifecycle:

```bash
# Start a new session
notte sessions start [flags]
  --headless                 Run in headless mode (default: true)
  --browser-type             Browser type: chromium, chrome, firefox (default: chromium)
  --idle-timeout-minutes     Idle timeout in minutes
  --max-duration-minutes     Maximum session lifetime in minutes
  --proxies                  Use default proxies
  --solve-captchas           Automatically solve captchas
  --viewport-width           Viewport width in pixels
  --viewport-height          Viewport height in pixels
  --user-agent               Custom user agent string
  --cdp-url                  CDP URL of remote session provider
  --use-file-storage         Enable file storage for the session

# Get current session status
notte sessions status

# Stop current session
notte sessions stop

# List active sessions
notte sessions list
```

**Note:** When you start a session, it automatically becomes the "current" session (i.e NOTTE_SESSION_ID environment variable is set). All subsequent commands use this session by default. Use `--session-id <session-id>` only when you need to manage multiple sessions simultaneously or reference a specific session.

Session debugging and export:

```bash
# Get network logs
notte sessions network

# Get replay URL/data
notte sessions replay

# Export session steps as Python workflow code
notte sessions workflow-code
```

Cookie management:

```bash
# Get all cookies
notte sessions cookies

# Set cookies from JSON file
notte sessions cookies-set --file cookies.json
```

### Page Actions

Simplified commands for page interactions:

**Element Interactions:**
```bash
# Click an element (use either the ids from an observe, or a selector)
notte page click "@B3"
notte page click "#submit-button"
  --timeout     Timeout in milliseconds
  --enter       Press Enter after clicking

# Fill an input field
notte page fill "@I1" "hello world"
  --clear       Clear field before filling
  --enter       Press Enter after filling

# Check/uncheck a checkbox
notte page check "#my-checkbox"
  --value       true to check, false to uncheck (default: true)

# Select dropdown option
notte page select "#dropdown-element" "Option 1"

# Download file by clicking element
notte page download "@L5"

# Upload file to input
notte page upload "#file-input" --file /path/to/file
```

**Navigation:**
```bash
notte page goto "https://example.com"
notte page new-tab "https://example.com"
notte page back
notte page forward
notte page reload
```

**Scrolling:**
```bash
notte page scroll-down [amount]
notte page scroll-up [amount]
```

**Keyboard:**
```bash
notte page press "Enter"
notte page press "Escape"
notte page press "Tab"
```

**Tab Management:**
```bash
notte page switch-tab 1
notte page close-tab
```

**Page State:**
```bash
# Observe page state and available actions
notte page observe [--url <url>]

# Save a screenshot in tmp folder
notte page screenshot

# Scrape content with instructions
notte page scrape --instructions "Extract all links" [--only-main-content]
```

**Utilities:**
```bash
# Wait for specified duration
notte page wait 1000

# Solve CAPTCHA
notte page captcha-solve "recaptcha_v2"

# Mark task complete
notte page complete "Task finished successfully" [--success=true]

# Fill form with JSON data
notte page form-fill --data '{"email": "test@example.com", "name": "John"}'
```

### AI Agents

Start and manage AI-powered browser agents:

```bash
# List all agents
notte agents list

# Start a new agent (auto-uses current session if active)
notte agents start --task "Navigate to example.com and extract the main heading"
  --session-id             Session ID (uses current session if not specified)
  --vault-id               Vault ID for credential access
  --persona-id             Persona ID for identity
  --max-steps              Maximum steps for the agent (default: 30)
  --reasoning-model        Custom reasoning model

# Get current agent status
notte agents status

# Stop current agent
notte agents stop

# Export agent steps as workflow code
notte agents workflow-code

# Get agent execution replay
notte agents replay
```

**Note:** When you start an agent, it automatically becomes the "current" agent (saved to `~/.notte/cli/current_agent`). All subsequent commands use this agent by default. Use `--agent-id <agent-id>` only when you need to manage multiple agents simultaneously or reference a specific agent.

**Agent ID Resolution:**
1. `--agent-id` flag (highest priority)
2. `NOTTE_AGENT_ID` environment variable
3. `~/.notte/cli/current_agent` file (lowest priority)

### Functions (Workflow Automation)

Create, manage, and schedule reusable workflows:

```bash
# List all functions
notte functions list

# Create a function from a workflow file
notte functions create --file workflow.py [--name "My Function"] [--description "..."] [--shared]

# Show current function details
notte functions show

# Update current function code
notte functions update --file workflow.py

# Delete current function
notte functions delete

# Run current function
notte functions run

# List runs for current function
notte functions runs

# Stop a running function execution
notte functions run-stop --run-id <run-id>

# Get run logs and results
notte functions run-metadata --run-id <run-id>

# Schedule current function with cron expression
notte functions schedule --cron "0 9 * * *"

# Remove schedule from current function
notte functions unschedule

# Fork a shared function to your account
notte functions fork --function-id <shared-function-id>
```

**Note:** When you create a function, it automatically becomes the "current" function. All subsequent commands use this function by default. Use `--function-id <function-id>` only when you need to manage multiple functions simultaneously or reference a specific function (like when forking a shared function).


### Account Management

**Personas** - Auto-generated identities with email/phone:

```bash
# List personas
notte personas list

# Create a persona
notte personas create [--create-phone-number] [--create-vault]

# Show persona details
notte personas show --persona-id <persona-id>

# Delete a persona
notte personas delete --persona-id <persona-id>

# List emails received by persona
notte personas emails --persona-id <persona-id>

# List SMS messages received
notte personas sms --persona-id <persona-id>
```

**Vaults** - Store your own credentials:

```bash
# List vaults
notte vaults list

# Create a vault
notte vaults create [--name "My Vault"]

# Update vault name
notte vaults update --vault-id <vault-id> --name "New Name"

# Delete a vault
notte vaults delete --vault-id <vault-id>

# Manage credentials
notte vaults credentials list --vault-id <vault-id>
notte vaults credentials add --vault-id <vault-id> --url "https://site.com" --password "pass" [--email "..."] [--username "..."] [--mfa-secret "..."]
notte vaults credentials get --vault-id <vault-id> --url "https://site.com"
notte vaults credentials delete --vault-id <vault-id> --url "https://site.com"
```

## Global Options

Available on all commands:

```bash
--output, -o    Output format: text, json (default: text)
--timeout       API request timeout in seconds (default: 30)
--no-color      Disable color output
--verbose, -v   Verbose output
--yes, -y       Skip confirmation prompts
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NOTTE_API_KEY` | API key for authentication |
| `NOTTE_SESSION_ID` | Default session ID (avoids --session-id flag) |
| `NOTTE_API_URL` | Custom API endpoint URL |

## Session ID Resolution

Session ID is resolved in this order:
1. `--session-id` flag
2. `NOTTE_SESSION_ID` environment variable
3. Current session file (set automatically by `sessions start`)

## Examples

### Basic Web Scraping

```bash
# Scrape with session
notte sessions start --headless
notte page goto "https://news.ycombinator.com"
notte page scrape --instructions "Extract top 10 story titles"
notte sessions stop

# Multi-page scraping
notte sessions start --headless
notte page goto "https://example.com/products"
notte page observe
notte page scrape --instructions "Extract product names and prices"
notte page click "@L3"
notte page scrape --instructions "Extract product names and prices"
notte sessions stop
```

### Form Automation

```bash
notte sessions start
notte page goto "https://example.com/signup"
notte page fill "#email-field" "user@example.com"
notte page fill "#password-field" "securepassword"
notte page click "#submit-button"
notte sessions stop
```

### Authenticated Session with Vault

```bash
# Setup credentials once
notte vaults create --name "MyService"
notte vaults credentials add --vault-id <vault-id> \
  --url "https://myservice.com" \
  --email "me@example.com" \
  --password "mypassword" \
  --mfa-secret "JBSWY3DPEHPK3PXP"

# Use in automation (vault credentials auto-fill on matching URLs)
notte sessions start
notte page goto "https://myservice.com/login"
# Credentials from vault are used automatically
notte sessions stop
```

### Scheduled Data Collection

```bash
# Create workflow file
cat > collect_data.py << 'EOF'
# Notte workflow script
# ...
EOF

# Upload as function
notte functions create --file collect_data.py --name "Daily Data Collection"

# Schedule to run every day at 9 AM
notte functions schedule --function-id <function-id> --cron "0 9 * * *"

# Check run history
notte functions runs --function-id <function-id>
```

## Tips & Troubleshooting

### Handling Inconsistent `observe` Output

The `observe` command may sometimes return stale or partial DOM state, especially with dynamic content, modals, or single-page applications. If the output seems wrong:

1. **Use screenshots to verify**: `notte page screenshot` always shows the current visual state
2. **Fall back to Playwright selectors**: Instead of `@ID` references, use standard selectors like `#id`, `.class`, or `button:has-text('Submit')`
3. **Add a brief wait**: `notte page wait 500` before observing can help with dynamic content

### Selector Syntax

Both element IDs from `observe` and Playwright selectors are supported:

```bash
# Using element IDs from observe output
notte page click "@B3"
notte page fill "@I1" "text"

# Using Playwright selectors (recommended when @IDs don't work)
notte page click "#submit-button"
notte page click ".btn-primary"
notte page click "button:has-text('Submit')"
notte page click "[data-testid='login']"
notte page fill "input[name='email']" "user@example.com"
```

**Handling multiple matches** - Use `>> nth=0` to select the first match:

```bash
# When multiple elements match, select by index
notte page click "button:has-text('OK') >> nth=0"
notte page click ".submit-btn >> nth=0"
```

### Working with Modals and Dialogs

Modals and popups can interfere with page interactions. Tips:

- **Close modals with Escape**: `notte page press "Escape"` reliably dismisses most dialogs and modals
- **Wait after modal actions**: Add `notte page wait 500` after closing a modal before the next action
- **Check for overlays**: If clicks aren't working, a modal or overlay might be blocking - use screenshot to verify

```bash
# Common pattern for handling unexpected modals
notte page press "Escape"
notte page wait 500
notte page click "#target-element"
```

### Viewing Headless Sessions

Running with `--headless` (the default) doesn't mean you can't see the browser:

- **ViewerUrl**: When you start a session, the output includes a `ViewerUrl` - open it in your browser to watch the session live
- **Viewer command**: `notte sessions viewer` opens the viewer directly
- **Non-headless mode**: Use `--headless=false` only if you need a local browser window (not available on remote/CI environments)

```bash
# Start headless session and get viewer URL
notte sessions start -o json | jq -r '.viewer_url'

# Or open viewer for current session
notte sessions viewer
```

### Bot Detection / Stealth

If you're getting blocked or seeing CAPTCHAs, try these approaches (requires restarting the session with new parameters):

1. **Change browser type**: Some sites have different detection for different browsers
   ```bash
   notte sessions stop
   notte sessions start --browser-type firefox
   ```

2. **Enable proxies**: Rotate IP addresses to avoid rate limiting
   ```bash
   notte sessions stop
   notte sessions start --proxies
   ```

3. **Firefox + CAPTCHA solving**: The `--solve-captchas` flag works best with Firefox
   ```bash
   notte sessions stop
   notte sessions start --browser-type firefox --solve-captchas
   ```

4. **Combine strategies**: For heavily protected sites, combine multiple options
   ```bash
   notte sessions stop
   notte sessions start --browser-type firefox --proxies --solve-captchas
   ```

**Note**: Always stop the current session before starting a new one with different parameters. Session configuration cannot be changed mid-session.

## Additional Resources

- [Session Management Reference](references/session-management.md) - Detailed session lifecycle guide
- [Function Management Reference](references/function-management.md) - Workflow automation guide
- [Account Management Reference](references/account-management.md) - Personas and vaults guide

### Templates

Ready-to-use shell script templates:

- [Form Automation](templates/form-automation.sh) - Fill and submit forms
- [Authenticated Session](templates/authenticated-session.sh) - Login with credential vault
- [Data Extraction](templates/data-extraction.sh) - Scrape structured data
