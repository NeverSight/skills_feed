---
name: replay-cypress
description: Set up and configure Replay for recording Cypress tests with time-travel debugging.
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), mcp__replay
---

## replay-cypress

**Description:** Use when the user wants to set up Replay for recording Cypress tests, configure the Replay Cypress plugin, or run Cypress tests with the Replay browser. Examples: "set up replay for cypress", "record my cypress tests", "configure replay cypress plugin", "run cypress with replay".

**Instructions:**

You are helping the user set up and configure Replay for recording Cypress tests. Follow these steps in order.

### Step 1: Create a Test Suite Team

Direct the user to visit https://app.replay.io/team/new/tests to create a test suite team. This automatically generates an API key needed for uploading recordings.

### Step 2: Install the Replay Cypress Plugin

Install the plugin as a dev dependency:

```sh
npm install --save-dev @replayio/cypress
# or
yarn add --dev @replayio/cypress
# or
pnpm add --save-dev @replayio/cypress
# or
bun add --dev @replayio/cypress
```

### Step 3: Install the Replay Browser

```sh
npx replayio install
```

This installs the Replay Chromium browser required for recording.

### Step 4: Store the API Key

The API key must be available as the `REPLAY_API_KEY` environment variable. Save it in a `.env` file at the project root:

```
REPLAY_API_KEY=<your_api_key>
```

Alternatively, export it directly:

```sh
export REPLAY_API_KEY=<your_api_key>
```

### Step 5: Configure the Cypress Support File

Add the Replay support import to `cypress/support/e2e.js` (or `e2e.ts`):

**CommonJS:**
```js
require('@replayio/cypress/support')
```

**ESM:**
```js
import '@replayio/cypress/support'
```

### Step 6: Configure cypress.config.js (or cypress.config.ts)

Add the Replay plugin to the Cypress config:

```js
const { defineConfig } = require('cypress')
const { plugin: replayPlugin, wrapOn } = require('@replayio/cypress')
require('dotenv').config()

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(cyOn, config) {
      const on = wrapOn(cyOn)
      replayPlugin(on, config, {
        upload: true,
        apiKey: process.env.REPLAY_API_KEY,
      })
      return config
    },
  },
})
```

For TypeScript (`cypress.config.ts`):

```ts
import { defineConfig } from 'cypress'
import { plugin as replayPlugin, wrapOn } from '@replayio/cypress'
import 'dotenv/config'

export default defineConfig({
  e2e: {
    setupNodeEvents(cyOn, config) {
      const on = wrapOn(cyOn)
      replayPlugin(on, config, {
        upload: true,
        apiKey: process.env.REPLAY_API_KEY,
      })
      return config
    },
  },
})
```

### Step 7: Run Tests with Replay

```sh
npx cypress run --browser replay-chromium
```

Recordings are automatically uploaded and a URL is provided for each recording to view in Replay DevTools.

## Important Notes

- The `upload: true` option in the plugin config enables automatic upload after tests complete.
- The `wrapOn` wrapper is required — it wraps the Cypress `on` event handler so Replay can hook into test lifecycle events.
- Cypress events (test starts, commands, assertions) appear in the Replay DevTools timeline.
- For CI/CD, set the `REPLAY_API_KEY` as a secret environment variable in your CI provider.

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
