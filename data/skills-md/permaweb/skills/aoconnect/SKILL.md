---
name: aoconnect
description: CLI for interacting with AO processes using @permaweb/aoconnect - spawn processes, send messages, read results, monitor messages, and dry run
compatibility: Requires Node.js 18+, @permaweb/aoconnect package
metadata:
  author: rakis
  version: "0.0.1"
---

# AOConnect Skill

A command-line interface for interacting with AO processes using the `@permaweb/aoconnect` library.

## Phrase Mappings

| User Request | Command |
|--------------|---------|
| "use aoconnect to spawn" | `spawn` |
| "use aoconnect to message" | `message` |
| "use aoconnect to read result" | `result` |
| "use aoconnect to dryrun" | `dryrun` |
| "use aoconnect to monitor" | `monitor` |
| "use aoconnect to connect" | `connect` |

## Installation

Install the aoconnect skill and its dependency:

```bash
npx skills add https://github.com/permaweb/skills --skill aoconnect
npm install --save @permaweb/aoconnect
```

Or manually:

```bash
cd skills/aoconnect
npm install @permaweb/aoconnect
```

## Prerequisites

- **Node.js 18+**
- **@permaweb/aoconnect** package installed
- **Arweave wallet** (JWK format) for signing messages

## Available Functions

### Spawn an AO Process

```sh
node skills/aoconnect/index.mjs spawn \
  --wallet ./wallet.json \
  --module <module-txid> \
  --scheduler <scheduler-address>
```

**Options:**
- `--wallet <path>` - Path to Arweave wallet JSON
- `--module <txid>` - The arweave TxID of the ao Module
- `--scheduler <address>` - The Arweave wallet address of a Scheduler Unit
- `--data <string>` - Optional data to include in spawn message

**Example:**

```sh
node skills/aoconnect/index.mjs spawn \
  --wallet ./wallet.json \
  --module "l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc" \
  --scheduler "_GQ33BkPtZrqxA84vM8Zk-N2aO0toNNu_C-l-rawrBA"
```

**Output:**

```json
{
  "messageId": "l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc",
  "processId": "5SGJUlPwlenkyuG9-xWh0Rcf0azm8XEd5RBTiutgWAg",
  "height": 587540,
  "tags": [
    { "name": "App-Process", "value": "l3hbt..." },
    { "name": "App-Name", "value": "arweave-ao" }
  ]
}
```

### Send a Message to an AO Process

```sh
node skills/aoconnect/index.mjs message \
  --wallet ./wallet.json \
  --process <process-id> \
  --data=<message-data> \
  --tags Name=Value,Another=Tag
```

**Options:**
- `--wallet <path>` - Path to Arweave wallet JSON (required)
- `--process <id>` - The ao Process ID (required)
- `--data <string>` - Message data (optional, random string if not provided)
- `--tags <name=value,another=value>` - Message tags (optional)

**Example:**

```sh
node skills/aoconnect/index.mjs message \
  --wallet ./wallet.json \
  --process "5SGJUlPwlenkyuG9-xWh0Rcf0azm8XEd5RBTiutgWAg" \
  --data="Hello from AO!" \
  --tags "Action=greet", "User=Rakis"
```

**Output:**

```json
{
  "messageId": "l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc",
  "height": 587540,
  "tags": [
    { "name": "Action", "value": "greet" },
    { "name": "User", "value": "Rakis" },
    { "name": "Original-Message", "value": "l3hbt..." }
  ]
}
```

### Read the Result of an AO Message Evaluation

```sh
node skills/aoconnect/index.mjs result \
  --message=<message-id> \
  --process=<process-id>
```

**Options:**
- `--message=<id>` - The ao message ID to evaluate (required)
- `--process=<id>` - The ao Process ID (required)

**Example:**

```sh
node skills/aoconnect/index.mjs result \
  --message="l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc" \
  --process="5SGJUlPwlenkyuG9-xWh0Rcf0azm8XEd5RBTiutgWAg"
```

**Output:**

```json
{
  "messages": [
    {
      "messageId": "l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc",
      "tags": [
        { "name": "Action", "value": "greet" },
        { "name": "User", "value": "Rakis" }
      ],
      "data": "Hello from AO!"
    }
  ],
  "spawns": [],
  "output": {
    "messages": [
      {
        "from": "address",
        "to": "process-id",
        "target": "process-id",
        "tags": [
          { "name": "Response", "value": "Hello from AO!" }
        ],
        "data": "",
        "height": 587541
      }
    ],
    "size": 256
  },
  "error": null
}
```

### Dry Run a Message (No Memory Commit)

```sh
node skills/aoconnect/index.mjs dryrun \
  --message=<message-id> \
  --process=<process-id>
```

**Options:**
- `--message=<id>` - The ao message ID to dry run (required)
- `--process=<id>` - The ao Process ID (required)

**Example:**

```sh
node skills/aoconnect/index.mjs dryrun \
  --message="l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc" \
  --process="5SGJUlPwlenkyuG9-xWh0Rcf0azm8XEd5RBTiutgWAg"
```

**Output:**

```json
{
  "messages": [
    {
      "messageId": "l3hbt-rIJ_dr9at-eQ3EVajHWMnxPNm9eBtXpzsFWZc",
      "tags": [
        { "name": "Action", "value": "greet" }
      ]
    }
  ],
  "spawns": [],
  "output": {
    "messages": [
      {
        "from": "address",
        "to": "process-id",
        "target": "process-id",
        "tags": [
          { "name": "Response", "value": "Hello from AO!" }
        ],
        "height": 587541
      }
    ],
    "size": 256
  },
  "error": null
}
```

**Note:** Dry run evaluates the message but doesn't save it to memory. Perfect for testing without committing to the chain.

### Monitor Messages

```sh
node skills/aoconnect/index.mjs monitor \
  --process <process-id> \
  --on-message "<callback>"
```

**Options:**
- `--process <id>` - The ao Process ID to monitor (required)
- `--on-message "<function>"` - JavaScript function to call for each new message (required)

**Example:**

```sh
node skills/aoconnect/index.mjs monitor \
  --process "5SGJUlPwlenkyuG9-xWh0Rcf0azm8XEd5RBTiutgWAg" \
  --on-message 'return { tags: msg.tags, data: msg.data }'
```

**Note:** In chat interface, use this pattern:
```bash
node skills/aoconnect/index.mjs monitor --process <id> --on-message "{console.log(msg.tags)}"
```

### Connect to Custom Nodes

```sh
node skills/aoconnect/index.mjs connect --mu <url> --cu <url> --gateway <url>
```

**Options:**
- `--mu <url>` - Message Unit URL (optional)
- `--cu <url>` - Compute Unit URL (optional)
- `--gateway <url>` - Arweave gateway URL (optional)

**Example:**

```sh
node skills/aoconnect/index.mjs connect \
  --mu "https://mu.ao-testnet.xyz" \
  --cu "https://cu.ao-testnet.xyz" \
  --gateway "https://arweave.net"
```

## Usage with AI Tools

Claude Code / OpenCode will automatically invoke the aoconnect skill when you:

```bash
use aoconnect to spawn <process>
use aoconnect to message <process> --data=<string>
use aoconnect to read result --message=<id>
use aoconnect to dryrun --message=<id>
```

The skill will prompt for wallet path if not configured.

## Common Use Cases

### Send a Transfer Message

```sh
node skills/aoconnect/index.mjs message \
  --wallet ./wallet.json \
  --process "ao-token-demo-AOe5Hdg4UQhOiE0ZYvRjB_8YDhROi3pA0YCEhPzb_KQ" \
  --data=<raw-balance-value> \
  --tags "Action=Transfer", "Recipient=<address>"
```

### Dry Run Before Committing

Always dry run first to verify your message works:

```sh
node skills/aoconnect/index.mjs message \
  --wallet ./wallet.json \
  --process <process-id> \
  --data="test"

node skills/aoconnect/index.mjs dryrun \
  --message=<message-id> \
  --process=<process-id>
```

### Monitor Active Process

```sh
node skills/aoconnect/index.mjs monitor \
  --process "<active-process-id>" \
  --on-message "{console.log('New message:', msg.tags)}"
```

## Error Handling

### Missing Wallet

```
Error: walletPath is required. Please provide a path to your Arweave wallet JSON file.
```

**Solution:** Provide a wallet path:
```sh
--wallet ./wallet.json
```

### Invalid Process ID

```
Error: Failed to send message: Invalid process ID
```

**Solution:** Verify the process ID is correct and valid.

### Authentication Failures

```
Error: Failed to send message: Unauthorized
```

**Solution:** Ensure your wallet has sufficient balance and proper permissions.

## API Reference

### messageAo(processId, options)
Send a message to an ao Process.

**Parameters:**
- `processId` (string): The ao Process ID
- `options` (Object): Message options
  - `data` (string): Message data
  - `tags` (Array): Message tags
  - `walletPath` (string): Path to wallet JSON

**Returns:** Promise<Object> - Message result

### resultAo(options)
Read the result of an ao message evaluation.

**Parameters:**
- `options` (Object)
  - `message` (string): The message ID
  - `process` (string): The Process ID

**Returns:** Promise<Object> - Result object

### dryrunAo(options)
Dry run a message without committing to memory.

**Parameters:**
- `options` (Object)
  - `message` (string): The message ID
  - `process` (string): The Process ID

**Returns:** Promise<Object> - Dry run result

### spawnAo(options)
Spawn an ao Process.

**Parameters:**
- `options` (Object)
  - `module` (string): Module TxID
  - `scheduler` (string): Scheduler address
  - `walletPath` (string): Path to wallet JSON
  - `tags` (Array): Tags for spawn message

**Returns:** Promise<Object> - Spawn result

### monitorAo(options)
Monitor messages from a Process.

**Parameters:**
- `options` (Object)
  - `process` (string): Process ID
  - `onMessage` (Function): Callback for new messages

**Returns:** string - Monitor ID

### unmonitorAo(monitorId)
Stop monitoring messages.

**Parameters:**
- `monitorId` (string): Monitor ID

### connectAo(config)
Connect to ao nodes with custom configuration.

**Parameters:**
- `config` (Object)
  - `MU_URL` (string): Message Unit URL
  - `CU_URL` (string): Compute Unit URL
  - `GATEWAY_URL` (string): Arweave gateway URL

**Returns:** Object - aoconnect functions

### getConnection(config)
Get connected aoconnect functions.

**Parameters:**
- `config` (Object): Connection config

**Returns:** Object - aoconnect functions

## Node.js vs Browser

This skill works in both Node.js and browser environments.

### Node.js
```javascript
import { messageAo, createDataItemSigner } from "./index.mjs";
import { readFileSync } from "node:fs";

const wallet = JSON.parse(readFileSync("./wallet.json", "utf-8"));
const result = await messageAo("process-id", {
  walletPath: "./wallet.json",
  data: "Hello AO!",
  tags: [{ name: "Action", value: "greet" }]
});
```

### Browser
```javascript
import { messageAo, createDataItemSigner } from "./index.mjs";

const result = await messageAo("process-id", {
  walletPath: "/path/to/wallet.json", // or loaded from localStorage
  data: "Hello AO!",
  tags: [{ name: "Action", value: "greet" }]
});
```

## See Also

- [AO Cookbook](https://cookbook_ao.arweave.net)
- [@permaweb/aoconnect Package](https://www.npmjs.com/package/@permaweb/aoconnect)
- [AR.IO Documentation](https://ar.io)
