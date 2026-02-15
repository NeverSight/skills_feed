---
name: replay-playwright
description: Set up and run Playwright tests with Replay Browser to record test executions for debugging and performance analysis.
allowed-tools: Bash(npx:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), mcp__replay
---

## replay-playwright

**Description:** Use when the user wants to set up Replay for Playwright tests, configure the Replay Playwright plugin, or run Playwright tests with the Replay Browser. Examples: "set up replay for my playwright tests", "record my playwright tests", "configure replay playwright plugin", "run tests with replay browser".

**Instructions:**

You are helping the user set up and run Playwright tests with the Replay Browser. Here is the complete reference:

### Installation

#### 1. Install the Replay Playwright plugin

```sh
npm install --save-dev @replayio/playwright
# or
yarn add --dev @replayio/playwright
# or
pnpm add --save-dev @replayio/playwright
# or
bun add --dev @replayio/playwright
```

#### 2. Install the Replay Browser

```sh
npx replayio install
```

### Authentication

Create a Test Suite Team at https://app.replay.io/team/new/tests to generate an API key.

Store the API key using one of these methods:

- **`.env` file** (recommended): Add `REPLAY_API_KEY=<your_api_key>` to your `.env` file and use the [dotenv](https://www.npmjs.com/package/dotenv) package to load it.
- **macOS/Linux**: `export REPLAY_API_KEY=<your_api_key>`
- **Windows**: `set REPLAY_API_KEY=<your_api_key>`

### Configuration

Update `playwright.config.ts` to use the Replay reporter and Replay Chromium browser:

```typescript
import { replayReporter, devices as replayDevices } from "@replayio/playwright";

const config: PlaywrightTestConfig = {
  reporter: [
    replayReporter({
      apiKey: process.env.REPLAY_API_KEY,
      upload: true,
    }),
    ["line"],
  ],
  projects: [
    {
      name: "replay-chromium",
      use: { ...replayDevices["Replay Chromium"] },
    },
  ],
};
```

Key configuration details:
- `replayReporter` handles uploading recordings after test runs
- `upload: true` automatically uploads recordings when tests finish
- The `replay-chromium` project uses the Replay Browser to capture recordings
- You can keep existing projects alongside `replay-chromium` for regular test runs

### Running Tests

Run Playwright tests with the Replay Browser:

```sh
npx playwright test --project replay-chromium
```

Recordings are automatically uploaded when `upload: true` is set in the reporter config.

## Core Workflow

**Set up Replay for an existing Playwright project:**

1. Install the plugin: `npm install --save-dev @replayio/playwright`
2. Install the browser: `npx replayio install`
3. Update `playwright.config.ts` with the Replay reporter and project
4. Set the `REPLAY_API_KEY` environment variable
5. Run tests: `npx playwright test --project replay-chromium`

**When modifying the user's `playwright.config.ts`:**

- Preserve existing projects and reporters — add the Replay project and reporter alongside them
- Import `replayReporter` and `devices as replayDevices` from `@replayio/playwright`
- If the config uses `defineConfig`, add the Replay project to the existing `projects` array
- If the config already has reporters, append `replayReporter` to the existing array

### Debugging your recorded application
**Run Replay MCP Server to debug your recored application**
to install the MCP server in Claude, run the following command:

```
claude --mcp-config "{
    "mcpServers": {
      "replay": {
        "type": "http",
        "url": "https://dispatch.replay.io/nut/mcp",
        "headers": {
          "Authorization": "${REPLAY_API_KEY}"
        }
      }
    }
  }"
```

