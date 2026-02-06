---
name: runhuman-testing
description: Create and manage human-powered QA tests using Runhuman CLI. Use when testing web applications, getting UX feedback, validating user flows, checking mobile responsiveness, or finding bugs that automated tests miss. Supports 40+ commands across authentication, jobs, projects, templates, GitHub integration, and more.
---

# Runhuman Testing

**Version:** 3.0.0
**Skills Format:** Agent Skills v1
**Last Updated:** 2026-02-05

## Overview

Runhuman connects AI agents to on-demand professional human testers for real user feedback. Instead of writing automated tests, describe what you want tested in natural language, and human testers provide structured feedback in 1-2 minutes.

**Key Benefits:**
- Catch UX issues and visual bugs automated tests miss
- Get real human perspective on user experience
- Average response time: 1-2 minutes
- No test maintenance overhead
- Mobile, desktop, tablet, laptop testing

## Quick Start

```bash
# One-time setup (authentication + project selection)
npx runhuman login
npx runhuman projects list
npx runhuman projects switch <project-id>

# Create a test
npx runhuman create https://example.com \
  -d "Test signup flow: fill form, check validation, verify success message"

# Check results
npx runhuman status <job-id>
npx runhuman results <job-id>

# Or wait for completion (blocking mode)
npx runhuman create https://example.com \
  -d "Test checkout flow" \
  --sync
```

## When to Use Runhuman

✅ **Ideal for:**
- User flows (signup, checkout, onboarding)
- Visual testing (layout, responsive design)
- Mobile testing (touch interactions, gestures)
- UX feedback (confusing UI, accessibility)
- Exploratory testing (edge cases)

❌ **Not for:**
- Unit tests → use Jest/Vitest
- Performance testing → use Lighthouse
- Security testing → use dedicated tools
- High-frequency tests (100+/day) → cost prohibitive (~$1-3 per test)

---

## Command Categories

The CLI has **41 commands** across 8 categories. For complete details, see [references/commands.md](references/commands.md) or use `--help`:

### 🔐 Authentication
- `login` - Authenticate via OAuth or API token
- `logout` - Clear credentials
- `whoami` - Show user info and account balance
- `tokens` - View balance and usage history

### 📋 Jobs (Test Management)
- `create` - Create a new test job
- `status` - Check job status
- `wait` - Wait for completion (polling)
- `results` - View detailed test results
- `list` - List all jobs with filtering
- `delete` - Delete a job
- `watch` - Auto-create tests on file changes

### 📁 Projects
- `projects list` - List all projects
- `projects create` - Create new project
- `projects show` - Show project details
- `projects switch` - Set default project
- `projects update` - Update project settings
- `projects delete` - Delete project

### ⚙️ Configuration
- `config list` - Show all config values
- `config get` - Get specific value
- `config set` - Set value (global or project)
- `config reset` - Reset configuration

### 📝 Templates
- `templates list` - List test templates
- `templates create` - Create reusable template
- `templates show` - Show template details
- `templates update` - Update template
- `templates delete` - Delete template

### 🔑 API Keys
- `keys list` - List API keys
- `keys create` - Create new key (for CI/CD)
- `keys show` - Show key details
- `keys delete` - Delete key

### 🐙 GitHub Integration
- `github link` - Link repository to project
- `github repos` - List linked repos
- `github issues` - List GitHub issues
- `github test` - Test a specific issue
- `github bulk-test` - Test multiple issues

### 🚀 Project Setup
- `init` - Initialize project with interactive setup

**For all commands:** `npx runhuman <command> --help`

---

## Essential Commands

### Create a Test

```bash
npx runhuman create <url> -d "description" [options]
```

**Most used options:**
- `-d, --description <text>` - Test instructions (required)
- `--screen-size <size>` - desktop|laptop|tablet|mobile
- `--sync` - Wait for completion (blocking/CI mode)
- `--project <id>` - Override default project
- `--duration <min>` - Target duration (1-60 minutes)

**Advanced options:**
- `--schema <file>` - JSON schema for structured output
- `--template <name>` - Use template configuration
- `--github-repo <owner/repo>` - Link to GitHub repo
- `--create-issues` - Auto-create GitHub issues from findings
- `--json` - Output as JSON
- `--quiet` - Minimal output (job ID only)

**Examples:**

```bash
# Basic test
npx runhuman create https://myapp.com \
  -d "Test signup: fill form, verify email confirmation"

# Mobile test
npx runhuman create https://myapp.com \
  -d "Test mobile navigation and layout" \
  --screen-size mobile

# CI/CD blocking test
npx runhuman create https://staging.app.com \
  -d "Test checkout flow end-to-end" \
  --sync --wait 600
```

### Check Status & Results

```bash
# Quick status check
npx runhuman status <job-id>

# Wait for completion (polling)
npx runhuman wait <job-id> --timeout 600

# View detailed results
npx runhuman results <job-id>

# Get structured data only
npx runhuman results <job-id> --schema-only --json
```

### List Jobs

```bash
# List all recent jobs
npx runhuman list

# Filter by status
npx runhuman list completed
npx runhuman list pending

# Filter by project
npx runhuman list --project <id> --limit 10
```

---

## First-Time Project Setup

**IMPORTANT:** First-time users must authenticate and configure a project before creating tests.

### Setup Workflow

```bash
# Step 1: Authenticate (first-time only)
npx runhuman login

# Step 2: Check if project is configured
npx runhuman config get project

# Step 3: If returns "(not set)", list available projects
npx runhuman projects list

# Step 4: Choose and set default project
npx runhuman projects switch <project-id>

# Step 5: Verify configuration
npx runhuman config get project
```

**After initial setup:** The saved credentials and project will be used automatically for all future commands.

**When NOT to ask:**
- User is already authenticated (`whoami` succeeds)
- Project is already configured (`config get project` returns an ID)
- User explicitly passes `--project` flag
- `.runhumanrc` file exists with project configured

---

## Configuration

### Configuration Priority (highest to lowest)

1. **CLI flags** - `--api-key`, `--project`, etc.
2. **Environment variables** - `RUNHUMAN_API_KEY`, `RUNHUMAN_PROJECT`
3. **Project config** - `.runhumanrc` in current directory
4. **Global config** - `~/.config/runhuman/config.json`
5. **Defaults**

### Project Config File

Create `.runhumanrc` in your project root:

```json
{
  "project": "my-project-id",
  "defaultUrl": "https://myapp.com",
  "defaultDuration": 5,
  "defaultScreenSize": "desktop",
  "githubRepo": "owner/repo"
}
```

### Environment Variables

```bash
RUNHUMAN_API_KEY=qa_live_xxxxxxxxxxxxx
RUNHUMAN_PROJECT=my-project-id
RUNHUMAN_DEFAULT_URL=https://example.com
RUNHUMAN_DEFAULT_DURATION=5
RUNHUMAN_DEFAULT_SCREEN_SIZE=desktop
```

**Useful for CI/CD:**

```yaml
env:
  RUNHUMAN_API_KEY: ${{ secrets.RUNHUMAN_API_KEY }}
  RUNHUMAN_PROJECT: ${{ vars.RUNHUMAN_PROJECT_ID }}
```

---

## Common Workflows

See [references/workflows.md](references/workflows.md) for detailed examples:

### Pre-Deployment Testing

```bash
#!/bin/bash
npx runhuman create https://staging.app.com \
  -d "Test critical flow: signup, login, checkout" \
  --sync

if [ $? -eq 0 ]; then
  ./deploy.sh
else
  echo "Tests failed - deployment aborted"
  exit 1
fi
```

### GitHub Actions CI/CD

```yaml
- name: Run human QA test
  env:
    RUNHUMAN_API_KEY: ${{ secrets.RUNHUMAN_API_KEY }}
  run: |
    npx runhuman create https://preview.app.com \
      -d "Test PR changes: ${{ github.event.pull_request.title }}" \
      --sync
```

### Mobile Testing

```bash
npx runhuman create https://myapp.com \
  -d "Test mobile: navigation, layout, touch interactions. Report any issues." \
  --screen-size mobile
```

### Batch Testing

```bash
# Run multiple tests in parallel (faster, cheaper)
npx runhuman create url1 -d "Test flow 1" &
npx runhuman create url2 -d "Test flow 2" &
npx runhuman create url3 -d "Test flow 3" &
wait
```

**More workflows:**
- File watching for development
- GitHub issue integration
- Structured output with JSON schemas
- Template-based testing

See [references/workflows.md](references/workflows.md) for complete examples.

---

## Writing Effective Test Descriptions

### ✅ Good Descriptions

**Specific with steps:**
```
Test checkout:
1. Add item to cart
2. Click "Checkout"
3. Fill shipping address
4. Select payment method
5. Complete order

Report: bugs, UX issues, confusing elements
```

**Clear objective:**
```
Test mobile navigation:
- Tap hamburger menu
- Verify all items visible
- Try each section
- Check menu closes properly

Report: layout issues, hard-to-tap buttons
```

### ❌ Bad Descriptions

- Too vague: "Test the site"
- Too technical: "Verify JWT expires after 15min"
- Missing context: "Click the button"
- No success criteria: "Test checkout"

**Better:** Be specific about what to test and what to report.

---

## Best Practices

### When to Use `--sync`

**✅ Use sync when:**
- CI/CD pipelines (need to block deployment)
- Critical pre-release flows
- Script needs to wait for results

**❌ Don't use sync when:**
- Running multiple tests (slower)
- Testing non-critical features
- Want faster turnaround

### Test Frequency

- **Per commit:** Critical flows only (signup, checkout)
- **Per PR:** Flows changed in PR
- **Nightly:** Full regression suite
- **Pre-release:** Everything + edge cases

### Cost Optimization

Tests cost ~$1-3 each. Optimize by:

1. **Batch related tests:** "Test signup AND login" (1 test) vs two tests
2. **Avoid excessive sync:** Only use in CI/CD
3. **Test staging, not production:** Catch bugs early
4. **Prioritize critical flows:** Not every page needs daily testing

### Screen Sizes

- `desktop` - Default, 1920x1080
- `laptop` - Smaller screens, 1366x768
- `tablet` - iPad, 768x1024
- `mobile` - Phone, 375x667

---

## Exit Codes

Use in scripts for conditional logic:

- `0` - Success
- `1` - General error
- `2` - Authentication failed (run `login`)
- `3` - Resource not found
- `4` - Validation error (missing required fields)
- `5` - Timeout (increase `--wait`)

```bash
npx runhuman create url -d "..." --sync
if [ $? -eq 0 ]; then
  echo "✅ Test passed"
else
  echo "❌ Test failed"
  exit 1
fi
```

---

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions.

**Quick fixes:**

| Error | Solution |
|-------|----------|
| "Authentication failed" | `npx runhuman login` |
| "Project ID required" | `npx runhuman projects switch <id>` |
| "Invalid URL" | Add `https://` protocol |
| "URL must be public" | Use tunnel (ngrok) for localhost |
| Test timeout | Increase `--duration` |

**Get help:**
```bash
npx runhuman --help
npx runhuman <command> --help
npx runhuman whoami          # Verify auth
npx runhuman config list     # Check config
```

---

## Reference Documentation

### 📚 Complete Command Reference
**[references/commands.md](references/commands.md)** - All 41 commands with full options, examples, and details.

**Use this for:**
- Detailed command syntax
- All available options and flags
- Advanced features (schemas, templates, GitHub integration)
- Configuration files and environment variables

### 🔧 Workflows & Examples
**[references/workflows.md](references/workflows.md)** - Real-world integration patterns and best practices.

**Includes:**
- Pre-deployment testing scripts
- GitHub Actions CI/CD examples
- Mobile responsiveness testing
- Batch testing strategies
- Cost optimization techniques
- Template usage patterns
- Structured output with JSON schemas

### 🔍 Troubleshooting Guide
**[references/troubleshooting.md](references/troubleshooting.md)** - Common errors and solutions.

**Covers:**
- Authentication issues
- Project configuration problems
- Validation errors
- Job status issues
- CI/CD troubleshooting
- Performance problems

---

## CLI Help

**The CLI has comprehensive built-in help via Commander.js:**

```bash
npx runhuman --help              # List all commands
npx runhuman create --help       # Create command details
npx runhuman projects --help     # Projects subcommands
npx runhuman github test --help  # Specific command help
```

**Always up-to-date:** Use `--help` for the latest options and features.

---

## Additional Resources

- **Dashboard:** https://runhuman.com/dashboard - View jobs, results, and analytics
- **API Docs:** https://runhuman.com/docs/api - REST API reference
- **GitHub Action:** https://github.com/marketplace/actions/runhuman-qa-test

---

## API Key Format

API keys follow this format: `qa_live_` + 40 hexadecimal characters

**Example:** `qa_live_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

**Get your key:**
```bash
npx runhuman login              # OAuth + auto-save
npx runhuman keys create "Key" # Generate for CI/CD
```

---

**End of Skill**

For detailed documentation, see the `references/` directory or use `npx runhuman <command> --help` for always up-to-date information.
