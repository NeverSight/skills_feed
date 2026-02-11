---
name: flipswitch-setup
description: Set up the Flipswitch feature flag SDK in your project. Detects your language, installs the SDK, writes initialization code, and creates an example flag.
disable-model-invocation: true
allowed-tools: Bash Read Write Glob Grep AskUserQuestion mcp__flipswitch__authenticate mcp__flipswitch__list_organizations mcp__flipswitch__list_projects mcp__flipswitch__list_environments mcp__flipswitch__get_sdk_api_key mcp__flipswitch__create_flag mcp__flipswitch__list_flags mcp__flipswitch__get_sdk_setup_snippet
---

Set up the Flipswitch feature flag SDK in this project.

## IMPORTANT: Execute these steps directly

Do NOT create helper tasks, spawn subagents, or delegate work. Execute each step in sequence, calling the MCP tools directly and handling results inline.

## Step 0: Verify MCP Server Configuration

**Call the `authenticate` MCP tool immediately to test connectivity.**

- If it succeeds (returns auth status or URL+code): ✅ MCP server is configured. Proceed to Step 1.
- If it fails with "tool not found" or "unknown tool": ❌ MCP server is NOT configured. Tell the user they need to add the Flipswitch MCP server with URL `https://mcp.flipswitch.io/mcp` to their tool's MCP configuration, then restart and retry. Refer them to the [Flipswitch Skills README](https://github.com/flipswitch-io/skills#step-2-configure-the-mcp-server) for tool-specific instructions.
  Stop here. User must configure and retry.
- If it fails with a network error: ⚠️ MCP server is configured but unreachable. Ask user to check internet connection.

## Step 1: Check Authentication Status

After successful `authenticate` call, check the result:

- **Already authenticated**: Display the auth status and proceed to Step 2.
- **Device code provided**: Show the user the URL and device code. Tell them to visit the URL, enter the code, and authorize. **Then immediately call `authenticate` again** to confirm.

## Step 2: Detect Project Language

Use Glob to find language markers in the project root:
- Check for `package.json` or `tsconfig.json` → **javascript**
- Check for `requirements.txt`, `pyproject.toml`, `setup.py`, or `Pipfile` → **python**
- Check for `go.mod` → **go**
- Check for `pom.xml`, `build.gradle`, or `build.gradle.kts` → **java**

If you find files for multiple languages or none, ask the user to specify using `AskUserQuestion` with options: "JavaScript", "Python", "Go", "Java", "Other".

**For JavaScript projects only**: Also determine if it's a web or server (Node.js) project:
- If `next.config.js`, `vite.config.js`, `webpack.config.js`, or similar build config exists → **web**
- If it's a Next.js/Remix/similar full-stack framework → ask the user if they want snippets for web, server, or both
- If `Dockerfile` or `docker-compose.yml` exists and no obvious web build config → likely **server**
- If uncertain, ask the user: "Is this a web app (browser), Node.js server, or full-stack?". Use `AskUserQuestion` with options: "Web browser", "Node.js server", "Both (I'll use both snippets)"

Save the selected language and JS environment (if applicable).

## Step 3: Get Organizations and Projects

**Call `list_organizations` MCP tool with no arguments.**

- If only 1 org: Use it automatically.
- If multiple orgs: Use `AskUserQuestion` to let user pick one.

Save the selected org ID.

**Then call `list_projects` MCP tool with `organizationId` set to the saved org ID.**

- If only 1 project: Use it automatically.
- If multiple projects: Use `AskUserQuestion` to let user pick one.

Save the selected project ID.

## Step 4: Get Environments

**Call `list_environments` MCP tool with `organizationId` and `projectId` set to saved values.**

- If an environment named "Development" exists: Use it automatically.
- Otherwise: Use `AskUserQuestion` to let user pick an environment.

Save the selected environment ID.

## Step 5: Get SDK API Key

**Call `get_sdk_api_key` MCP tool with `organizationId`, `projectId`, and `environmentId` set to saved values.**

The tool will return an API key. Save this key — you'll need it in the next step.

## Step 6: Get SDK Setup Snippet

**Call `get_sdk_setup_snippet` MCP tool with:**
- `language`: saved language from Step 2
- `apiKey`: saved API key from Step 5
- If language is javascript: also set `jsEnvironment` based on detection from Step 2 (e.g., "web" or "server")

The tool will return install command and init code. Display these to the user.

## Step 7: Install SDK

**Use the Bash tool to run the install command returned from Step 6:**
- **javascript (web)**: `npm install @flipswitch-io/sdk @openfeature/web-sdk`
- **javascript (server)**: `npm install @flipswitch-io/sdk @openfeature/js-sdk`
- **python**: `pip install flipswitch-sdk`
- **go**: `go get github.com/flipswitch-io/go-sdk`
- **java**: For Maven/Gradle projects, use the Write tool to add the dependency to `pom.xml` or `build.gradle` instead

If the install command fails, show the error and ask the user how to proceed.

## Step 8: Write Initialization Code

Get the init code from Step 6's result. Based on the language, create a file:
- **javascript**: `src/flipswitch.ts` (or `.js` if not TypeScript)
- **python**: `flipswitch.py`
- **go**: `flipswitch.go`
- **java**: `Flipswitch.java`

**Use the Write tool to create the file with the init code from Step 6.**

Display the file path to the user.

## Step 9: Example Flag Integration (Optional)

Use `AskUserQuestion` to ask: "Would you like to add a feature flag example to your codebase?" with these options:

1. **Create a new flag** — "Create a new feature flag and generate example code"
2. **Use an existing flag** — "Pick one of your existing flags and generate example code"
3. **Skip for now** — "I'll add flags later"

### Option A: Create a new flag

Ask the user for a flag name (e.g. "Dark Mode"). Then:
- Use the name as the human-readable **name**
- Convert to kebab-case for the **key** (lowercase, replace spaces/underscores with hyphens, remove special characters)
- Call `create_flag` with the org ID, project ID, generated key, name, and `flagValueType`: `Boolean`
- If it fails with "key already exists": inform the user and suggest they pick "Use an existing flag" instead
- If it fails for another reason: report the error but continue
- Save the flag key and proceed to the code generation step below

### Option B: Use an existing flag

Call `list_flags` with the org and project IDs.
- If no flags exist: tell the user and loop back to offer "Create a new flag" or "Skip for now"
- If flags exist: use `AskUserQuestion` to let the user pick one, also if only one flag exists
- Save the selected flag's key and proceed to the code generation step below

### Option C: Skip for now

Skip to Step 10.

### Generate example code

Once a flag is selected (Option A or B), generate a real usage example:

1. **Scan the codebase** for a suitable integration point. Use Glob and Grep to look for patterns like:
   - Route handlers, API endpoints, or controller methods
   - UI component render functions
   - Configuration or feature logic
   - Middleware or request processing
2. **If a good candidate is found**: show the user the file and the specific location, then write code that wraps the existing logic in a flag evaluation using the selected flag key. Import the Flipswitch init from the file created in Step 8.
3. **If no suitable candidate is found** (e.g. empty or unfamiliar project): call `get_sdk_setup_snippet` with the `flagKey` set to the selected flag key to get evaluation code, and show it to the user as a standalone example they can paste into their code.

## Step 10: Summary

Show the user:
- ✅ SDK installed
- ✅ Initialization code written to `<file_path>`
- If a flag was integrated: ✅ Flag `{key}` integrated with example code
- If skipped: ℹ️ No flag configured yet — create one with `/flipswitch-create`
- Link: https://app.flipswitch.io
- Next steps: Enable the flag with `/flipswitch-toggle` or in the dashboard
