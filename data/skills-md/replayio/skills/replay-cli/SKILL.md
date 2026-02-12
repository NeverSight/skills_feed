---
name: replay-cli
description: Record your application to gather performance data and debug issues. It enables users to install Replay ClI, record a session, upload and manage them.
allowed-tools: Bash(replayio:*), mcp__replay
---

## replay-cli

**Description:** Use when the user wants help with Replay CLI commands for recording, uploading, managing recordings, or authentication. Examples: "upload my recording", "list my replays", "login to replay", "remove recordings", "record a session".

**Instructions:**

You are helping the user with the Replay CLI tool. Here is the complete reference:

### Installation

Install Replay CLI globally using your preferred package manager:

```sh
npm i -g replayio
# or
yarn add -g replayio
# or
pnpm i -g replayio
# or
bun i -g replayio
```

### Authentication

Navigate to https://app.replay.io settings page, create your API key and save the API key in the environment variable `REPLAY_API_KEY`.

### Available Commands

| Command              | Arguments    | Options                                                           |
| -------------------- | ------------ | ----------------------------------------------------------------- |
| `info`               | –            | –                                                                 |
| `list`               | –            | `--json`                                                          |
| `login`              | –            | –                                                                 |
| `logout`             | –            | –                                                                 |
| `record`             | `[url]`      | –                                                                 |
| `remove`             | `[ids...]`   | `-a`, `--all`                                                     |
| `update`             | –            | –                                                                 |
| `upload`             | `[ids...]`   | –                                                                 |
| `upload-source-maps` | `<paths...>` | `-g`, `--group`, `-x`, `--extensions`, `-i`, `--ignore`, `--root` |
| `help`               | –            | –                                                                 |

Pass `-h` or `--help` to any command for more info.

### Command Details

#### `replayio info`

Displays information about installed Replay dependencies including CLI version and Replay Browser info.

#### `replayio list`

Lists all local recordings with their ID, host, date, duration, and status (Uploaded/Recorded).

- `--json` - prints full list with details

#### `replayio login`

Opens browser to log in to your Replay account. Creates account if needed.

#### `replayio logout`

Logs out from Replay account. Does NOT invalidate API keys in environment variables.

#### `replayio record [url]`

Launches Replay Browser and starts recording the given URL. Default URL is `about:blank`.

- Recording continues until browser is closed
- If not prompted differently, agent should upload just the main URL
- Automatically checks for browser/CLI updates

#### `replayio remove [ids...]`

Removes one or more recordings.

- Without arguments: opens interactive menu to select recordings
- With IDs: removes specified recordings
- `-a`, `--all` - removes all local recordings

#### `replayio update`

Updates the Replay Browser only. CLI updates are done via npm/yarn/pnpm/bun.

#### `replayio upload [ids...]`

Uploads one or more recordings.

- Without arguments: opens interactive menu to select recordings
- With IDs: uploads specified recordings
- Returns URL to view recording after upload

#### `replayio upload-source-maps <paths...>`

Uploads source maps for a Workspace.

- `-g`, `--group <name>` - group name (e.g., commit SHA or release version)
- `-x`, `--extensions <exts>` - file extensions to process (default: ".js,.map")
- `-i`, `--ignore <pattern>` - ignore files matching pattern
- `--root <dirname>` - base directory for relative paths

#### `replayio help`

Displays all available commands and descriptions.

## Core Workflow

**Record and upload a session:**

```sh
replayio record https://myapp.com
# After recording, you'll be prompted to upload
```

**Upload a specific recording:**
If upload wasn’t done automatically after recording, agent should upload the recording manually using the recording ID from previous step

```sh
replayio upload <recording-id>
```

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
