---
name: umbraco-quickstart
description: Quick setup for Umbraco extension development - creates instance, extension, and registers it
version: 1.1.0
argument-hint: "[UmbracoProjectName] [ExtensionName] [--email admin@example.com] [--password Admin123456]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user_invocable: true
---

# Umbraco Quickstart

Sets up everything needed for Umbraco extension development in one command.

## Usage

```bash
# Full setup with custom credentials
/umbraco-quickstart MyUmbracoSite MyExtension --email a@a.co.uk --password Admin123456

# With default credentials (admin@test.com / SecurePass1234)
/umbraco-quickstart MyUmbracoSite MyExtension

# Just Umbraco instance name (will prompt for extension name)
/umbraco-quickstart MyUmbracoSite

# No arguments (will detect existing or prompt for names)
/umbraco-quickstart
```

## Workflow

### 1. Parse arguments

- **First argument**: Umbraco project name (e.g., "MyUmbracoSite")
- **Second argument**: Extension name (e.g., "MyExtension")
- **`--email`** (optional): Admin email (default: `admin@test.com`)
- **`--password`** (optional): Admin password (default: `SecurePass1234`)

If arguments not provided, check what exists and prompt for missing names.

### 2. Check what exists

**Check for Umbraco instance:**
```bash
find . -name "*.csproj" -exec grep -l "Umbraco.Cms" {} \; 2>/dev/null | head -5
```

**Check for extension projects:**
```bash
find . -name "umbraco-package.json" 2>/dev/null | head -10
```

### 3. Take action

**If no Umbraco instance:**
- Use the provided name (first argument) or prompt for one
- Create with `/package-script-writer [ProjectName]`

**If no extension:**
- Use the provided name (second argument) or prompt for one
- Create with `/umbraco-extension-template [ExtensionName]`

**If extension not registered:**
- Register with `/umbraco-add-extension-reference [ExtensionName]`

### 4. Warn about optional resources

Check extended workspace (including `/add-dir` directories) and warn if missing:

**If CMS source not found:**
```
⚠ Umbraco CMS source not found in extended workspace.
  For better code generation, add it:
  git clone https://github.com/umbraco/Umbraco-CMS.git
  /add-dir /path/to/Umbraco-CMS/src/Umbraco.Web.UI.Client
```

**If UUI source not found:**
```
⚠ UUI library source not found in extended workspace.
  For UI component reference, add it:
  git clone https://github.com/umbraco/Umbraco.UI.git
  /add-dir /path/to/Umbraco.UI/packages/uui
```

**If testing skills not installed:**
```
⚠ Testing skills not installed.
  To add testing capabilities:
  /plugin install umbraco-cms-backoffice-testing-skills@umbraco-backoffice-marketplace
```

### 5. MANDATORY: Enter Plan Mode

**Do NOT proceed to building until this step is complete.**

1. Tell the user setup is complete and show the login credentials
2. Read `PRE-BUILD-PLANNING.md` from the `umbraco-backoffice` skill
3. Ask the user what they want to build

```
✅ Setup complete! Your extension is ready.

Login: admin@test.com / SecurePass1234

What would you like to build? Describe your idea and I'll help you plan the implementation.

Examples:
- "A dashboard that shows recent content changes"
- "A property editor for picking colours"
- "A tree in Settings for managing custom data"
```

When the user describes what they want:

1. **Enter plan mode with `/plan`**
2. Follow the PRE-BUILD-PLANNING.md workflow:
   - Draw ASCII wireframe of the UI
   - Label extension types needed (section, dashboard, workspace, etc.)
   - Identify UUI components
   - Map data flow (contexts, APIs)
3. Identify which sub-skills to invoke
4. **Include these MANDATORY sections in the plan document** (they will be actioned after plan approval):

```markdown
## Pre-Build Setup
- [ ] Load `/umbraco-backoffice` skill for best practices and examples

## Implementation
[Your implementation steps here - skills to invoke, files to create]

## Post-Build Validation (REQUIRED - DO NOT SKIP)

### Step 1: Initial Build
- [ ] Run `npm run build` in extension directory
- [ ] Verify build completes without errors

### Step 2: Code Review
- [ ] Spawn `umbraco-extension-reviewer` agent
- [ ] Fix all Critical/High severity issues

### Step 3: Rebuild (if fixes were made)
- [ ] Run `npm run build` again
- [ ] Verify build still succeeds

### Step 4: Restart Umbraco
- [ ] Stop the running Umbraco instance
- [ ] Run `dotnet run` to restart
- [ ] Wait for startup to complete

### Step 5: Browser Validation
Check if browser automation is available (any of: `dev-browser` skill, Playwright MCP, Claude computer use).

If browser automation IS available:
- [ ] Navigate to backoffice login (http://localhost:5000/umbraco)
- [ ] Login with credentials
- [ ] Navigate to extension location
- [ ] Verify: no console errors, UI renders, interactions work
- [ ] Take screenshot of working extension

If NO browser automation available, output manual testing steps for user.
```

5. Exit plan mode only when wireframe AND all validation sections are in the plan

**⚠️ Do NOT generate code until planning is complete and approved by the user.**


## Goal

Get the user to a working, validated extension. Follow the workflow: PLAN → BUILD → VALIDATE. Don't just report - take action.

## Default Credentials

When creating an Umbraco instance, these defaults are used:

- **Email:** `admin@test.com`
- **Password:** `SecurePass1234`

These are safe for local development and don't contain special characters that cause escaping issues.

## Example

```bash
/umbraco-quickstart MyUmbracoSite MyDashboard
```

This will:
1. Create Umbraco instance (e.g. "MyUmbracoSite") if not exists
2. Create extension (e.g. "MyDashboard")
3. Register the extension with the Umbraco project
4. Warn about missing CMS/UUI source if applicable
5. Enter plan mode to design the extension (wireframe, extension types, validation steps)
6. Build using identified sub-skills
7. Run `npm run build`
8. Run `umbraco-extension-reviewer` and fix issues
9. Rebuild if fixes were made
10. Restart Umbraco
11. Browser validation (automatic if browser automation available, manual steps otherwise)

**Login with:** `admin@test.com` / `SecurePass1234`
