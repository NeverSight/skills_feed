---
name: daytona-integration
description: Daytona SDK integration for sandbox lifecycle management. Use when working with SandboxManager, creating/destroying sandboxes, executing commands in sandboxes, or transferring files between sandboxes and local filesystem.
---

# Daytona Integration

> Source: [Daytona TypeScript SDK Docs](https://www.daytona.io/docs/en/typescript-sdk)

## Installation

```bash
npm install @daytonaio/sdk
```

## SDK Setup

```typescript
import { Daytona } from '@daytonaio/sdk'

const daytona = new Daytona({
  apiKey: process.env.DAYTONA_API_KEY,          // Required for auth
  apiUrl: 'https://app.daytona.io/api',         // Default API endpoint
  target: 'us',                                  // Optional: region preference
  // Alternative auth:
  // jwtToken: 'jwt-token',                      // Requires organizationId
  // organizationId: 'org-id'
})
```

### DaytonaConfig Interface

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `apiKey` | `string` | No* | API key authentication |
| `apiUrl` | `string` | No | API endpoint (default: `https://app.daytona.io/api`) |
| `jwtToken` | `string` | No* | JWT authentication (requires organizationId) |
| `organizationId` | `string` | No | Required when using JWT |
| `target` | `string` | No | Sandbox location preference |

*One of `apiKey` or `jwtToken` required.

## Daytona Class Methods

### create()

Create a new sandbox.

```typescript
const sandbox = await daytona.create({
  language: 'typescript',      // 'python' | 'typescript' | 'javascript'
  envVars: {                   // Environment variables
    CLAUDE_CODE_OAUTH_TOKEN: token,
    NODE_ENV: 'development'
  },
  autoStopInterval: 15,        // Minutes idle before stop (default: 15)
  autoArchiveInterval: 10080,  // Minutes before archive (default: 7 days)
  autoDeleteInterval: 43200,   // Minutes before deletion
  labels: { project: 'mvp' },  // Metadata tags
  ephemeral: false             // Auto-cleanup on stop
}, {
  timeout: 60                  // Creation timeout in seconds
})
```

**Returns:** `Promise<Sandbox>`

### CreateSandboxParams

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `language` | `'python' \| 'typescript' \| 'javascript'` | `'python'` | Runtime language |
| `envVars` | `Record<string, string>` | `{}` | Environment variables |
| `autoStopInterval` | `number` | `15` | Idle minutes before stop |
| `autoArchiveInterval` | `number` | `10080` | Minutes before archive |
| `autoDeleteInterval` | `number` | - | Minutes before deletion |
| `labels` | `Record<string, string>` | - | Metadata tags |
| `ephemeral` | `boolean` | `false` | Auto-cleanup on stop |
| `volumes` | `VolumeMount[]` | - | Volume mounts |
| `image` | `string \| Image` | - | Custom Docker image |
| `resources` | `Resources` | - | CPU/memory/disk allocation |
| `snapshot` | `string` | - | Create from snapshot ID |

### get()

Retrieve a sandbox by ID or name.

```typescript
const sandbox = await daytona.get('sandbox-id-or-name')
```

**Returns:** `Promise<Sandbox>`

### list()

List sandboxes with optional filtering.

```typescript
const result = await daytona.list(
  { project: 'mvp' },  // Filter by labels
  1,                   // Page number
  10                   // Items per page
)
// result.sandboxes: Sandbox[]
// result.total: number
```

**Returns:** `Promise<PaginatedSandboxes>`

### findOne()

Find first sandbox matching filter.

```typescript
const sandbox = await daytona.findOne({
  id: 'sandbox-id',
  name: 'sandbox-name',
  labels: { project: 'mvp' }
})
```

**Returns:** `Promise<Sandbox>`

### delete()

Delete a sandbox permanently.

```typescript
await daytona.delete(sandbox, 60)  // sandbox object, timeout seconds
```

### start() / stop()

```typescript
await daytona.start(sandbox, 60)  // Start and await ready, timeout seconds
await daytona.stop(sandbox)       // Stop execution
```

## Sandbox Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique sandbox identifier |
| `name` | `string` | Sandbox name |
| `state` | `SandboxState` | `'started' \| 'stopped' \| ...` |
| `cpu` | `number` | CPU count |
| `memory` | `number` | Memory in GiB |
| `disk` | `number` | Disk space in GiB |
| `gpu` | `number` | GPU count |
| `env` | `Record<string, string>` | Environment variables |
| `labels` | `Record<string, string>` | Metadata |
| `process` | `Process` | Process execution interface |
| `fs` | `FileSystem` | File system interface |
| `git` | `Git` | Git operations interface |

### Methods

```typescript
// Lifecycle
await sandbox.start(timeout?)
await sandbox.stop(timeout?)
await sandbox.delete(timeout)
await sandbox.archive()
await sandbox.recover(timeout?)

// State
await sandbox.refreshData()
await sandbox.waitUntilStarted(timeout?)
await sandbox.waitUntilStopped(timeout?)

// Configuration
await sandbox.setLabels({ key: 'value' })
await sandbox.setAutostopInterval(minutes)
await sandbox.setAutoDeleteInterval(minutes)
await sandbox.setAutoArchiveInterval(minutes)

// Paths
const workDir = await sandbox.getWorkDir()
const homeDir = await sandbox.getUserHomeDir()

// Access
const previewUrl = await sandbox.getPreviewLink(port)
const signedUrl = await sandbox.getSignedPreviewUrl(port, expiresInSeconds?)
```

## Process Class (sandbox.process)

### executeCommand()

Execute shell commands.

```typescript
const response = await sandbox.process.executeCommand(
  'npm install',           // command
  '/workspace',            // cwd (optional)
  { NODE_ENV: 'prod' },    // env (optional)
  300                      // timeout in seconds (optional, 0=indefinite)
)
```

**Returns:** `Promise<ExecuteResponse>`

**CRITICAL WARNING - Background Processes:**
`executeCommand()` with `timeout=0` does NOT run background servers properly. Despite documentation saying "0=indefinite", the Promise resolves immediately without spawning a tracked process. Use session-based execution for background processes instead (see Session-based Execution section below).

```typescript
// ❌ WRONG - Server won't actually run
await sandbox.process.executeCommand('npm run dev', '/workspace', undefined, 0)

// ✅ CORRECT - Use sessions for background processes
await sandbox.process.createSession('preview-server')
await sandbox.process.executeSessionCommand('preview-server', {
  command: 'npm run dev',
  async: true
}, 0)
```

### ExecuteResponse Interface

| Property | Type | Description |
|----------|------|-------------|
| `exitCode` | `number` | Process exit status |
| `result` | `string` | stdout content |
| `artifacts` | `ExecutionArtifacts` | Additional data (stdout, charts) |

### codeRun()

Execute code using appropriate runtime.

```typescript
const response = await sandbox.process.codeRun(
  'console.log("Hello")',  // code
  { argv: [], env: {} },   // params (optional)
  60                       // timeout in seconds (optional)
)
```

### Session-based Execution (for streaming)

```typescript
// Create a persistent session
await sandbox.process.createSession('my-session')

// Execute with async log callbacks
await sandbox.process.executeSessionCommand('my-session', {
  command: 'npm start',
  async: true
}, 300)

// Get logs with streaming callbacks
await sandbox.process.getSessionCommandLogs(
  'my-session',
  'command-id',
  (stdout: string) => { /* handle stdout chunk */ },
  (stderr: string) => { /* handle stderr chunk */ }
)

// Cleanup
await sandbox.process.deleteSession('my-session')
```

### PTY (Interactive Terminal)

```typescript
// Create PTY session
const pty = await sandbox.process.createPty({ cols: 80, rows: 24 })

// Connect via WebSocket
await sandbox.process.connectPty(pty.sessionId, {
  onData: (data) => { /* terminal output */ },
  onExit: (code) => { /* process exited */ }
})

// Resize
await sandbox.process.resizePtySession(pty.sessionId, 120, 40)

// Kill
await sandbox.process.killPtySession(pty.sessionId)
```

## File System (sandbox.fs)

```typescript
// Download file (returns Buffer)
const buffer = await sandbox.fs.downloadFile('/workspace/file.txt')
const content = buffer.toString()

// Upload file (Buffer or local path)
await sandbox.fs.uploadFile(Buffer.from('content'), '/workspace/file.txt')
await sandbox.fs.uploadFile('/local/path.txt', '/workspace/file.txt')

// List directory (returns FileInfo[])
const files = await sandbox.fs.listFiles('/workspace')
// files[i].name, files[i].size, files[i].isDir

// Create directory
await sandbox.fs.createFolder('/workspace/new-dir', '755')

// Delete file/directory
await sandbox.fs.deleteFile('/workspace/file.txt')
await sandbox.fs.deleteFile('/workspace/dir', true)  // recursive

// File details
const info = await sandbox.fs.getFileDetails('/workspace/file.txt')

// Search
const results = await sandbox.fs.searchFiles('/workspace', '*.ts')
const matches = await sandbox.fs.findFiles('/workspace', 'pattern')
```

## Parallel Sandbox Creation (4 agents)

```typescript
const agentIds = ['agent-a', 'agent-b', 'agent-c', 'agent-d']

const sandboxes = await Promise.all(
  agentIds.map(async (agentId) => {
    const sandbox = await daytona.create({
      language: 'typescript',
      envVars: { CLAUDE_CODE_OAUTH_TOKEN: token },
      labels: { agentId },
      autoStopInterval: 60
    })
    return { agentId, sandbox }
  })
)
```

## File Transfer Patterns

### Extract from sandbox (winner selection)

```typescript
// Create tar in sandbox
await sandbox.process.executeCommand(
  'tar -czf /tmp/project.tar.gz -C /workspace .',
  undefined,
  undefined,
  60
)

// Download
const tarBuffer = await sandbox.fs.downloadFile('/tmp/project.tar.gz')

// Save locally
import { writeFileSync } from 'fs'
writeFileSync('~/.multishot/runs/run-id/winner.tar.gz', tarBuffer)
```

### Inject into sandbox (next round)

```typescript
import { readFileSync } from 'fs'

// Upload tar
const tarBuffer = readFileSync('~/.multishot/runs/run-id/winner.tar.gz')
await sandbox.fs.uploadFile(tarBuffer, '/tmp/project.tar.gz')

// Extract
await sandbox.process.executeCommand(
  'tar -xzf /tmp/project.tar.gz -C /workspace',
  undefined,
  undefined,
  60
)
```

## Error Handling

### Network Error Retry Pattern

When executing commands that make API calls (Claude Code, npm installs, etc.), implement retry logic for transient network errors:

```typescript
async function execWithRetry(
  command: string,
  maxRetries: number = 3
): Promise<ExecuteResponse> {
  let lastError: Error | null = null

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await sandbox.process.executeCommand(
        command,
        workDir,
        undefined,
        900
      )

      if (response.exitCode !== 0) {
        throw new Error(`Process exited with code ${response.exitCode}`)
      }

      return response // Success

    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err))

      // Check if error is retryable (network issues)
      const isRetryable =
        lastError.message.includes('ECONNRESET') ||
        lastError.message.includes('ETIMEDOUT') ||
        lastError.message.includes('ENOTFOUND') ||
        lastError.message.includes('EAI_AGAIN') ||
        lastError.message.includes('socket hang up')

      if (!isRetryable) {
        throw lastError // Non-network error - fail immediately
      }

      if (attempt < maxRetries) {
        // Exponential backoff: 5s, 10s, 20s
        const delayMs = 5000 * Math.pow(2, attempt - 1)
        console.warn(`Retry ${attempt}/${maxRetries} in ${delayMs / 1000}s...`)
        await new Promise(resolve => setTimeout(resolve, delayMs))
      } else {
        throw new Error(`Network error after ${maxRetries} retries: ${lastError.message}`)
      }
    }
  }

  throw lastError || new Error('Unknown error')
}
```

**Retryable errors:**
- `ECONNRESET` - Connection forcibly closed
- `ETIMEDOUT` - Connection timed out
- `ENOTFOUND` - DNS lookup failed
- `EAI_AGAIN` - Temporary DNS failure
- `socket hang up` - Connection dropped

**Non-retryable errors (fail immediately):**
- Authentication failures
- Invalid commands
- Permission errors
- Validation errors

**Benefits:**
- Prevents sandbox waste from transient network drops
- Critical for parallel agent execution (4 agents = higher network failure chance)
- Exponential backoff prevents overwhelming failing services

### Sandbox Creation

```typescript
try {
  const sandbox = await daytona.create({ language: 'typescript' })
} catch (error) {
  if (error.code === 'SANDBOX_CREATION_FAILED') {
    // Retry once
    await new Promise(r => setTimeout(r, 2000))
    const sandbox = await daytona.create({ language: 'typescript' })
  }
}

// Always cleanup in finally
try {
  // ... work with sandbox
} finally {
  await sandbox.delete(30).catch(console.error)
}
```

## MVP Implementation Notes

Current implementation uses `executeCommand()` with retry logic (not session-based streaming):

```typescript
// SandboxManager.execClaudeCommand() pattern with retries
for (let attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    const response = await sandbox.process.executeCommand(
      command,
      workDir,
      undefined,
      900 // 15 minute timeout
    )
    if (response.result) onStdout?.(response.result)
    return // Success
  } catch (err) {
    // Retry logic for ECONNRESET, ETIMEDOUT, etc.
    // Exponential backoff: 5s, 10s, 20s
  }
}
```

Preview servers use session-based execution for background processes:
```typescript
await sandbox.process.createSession(sessionId)
await sandbox.process.executeSessionCommand(sessionId, {
  command: config.command,
  async: true
}, 0)
```

Preview URL retrieval uses signed URLs:
```typescript
const preview = await sandbox.getSignedPreviewUrl(port, 3600)
return preview.url
```

## Preview Optimization Patterns

### Config Caching

Reduce filesystem operations by caching project type detection results:

```typescript
class SandboxManager {
  private previewConfigs: Map<string, PreviewConfig> = new Map()

  async detectProjectType(agentId: string): Promise<PreviewConfig> {
    // Check cache first
    const cached = this.previewConfigs.get(agentId)
    if (cached) {
      console.log(`Using cached preview config: ${cached.type}`)
      return cached
    }

    // Detect project type (filesystem operations)
    const config = await this.performDetection(agentId)

    // Cache result
    this.previewConfigs.set(agentId, config)
    return config
  }

  clearPreviewCache(): void {
    this.previewConfigs.clear()
  }

  async destroySandbox(agentId: string): Promise<void> {
    // Clear cached config when sandbox destroyed
    this.previewConfigs.delete(agentId)
    // ... destroy sandbox
  }
}
```

**Benefits:**
- Repeated preview requests reuse cached config (no filesystem access)
- Cleared on new run to detect fresh project structure
- Cleared per-agent on sandbox destruction

### Session Reuse

Prevent duplicate preview servers by reusing existing sessions:

```typescript
interface SandboxInfo {
  sandbox: Sandbox
  agentId: string
  previewSessionId?: string
}

async startPreviewServer(
  agentId: string,
  config: PreviewConfig
): Promise<void> {
  const info = this.sandboxes.get(agentId)
  const sessionId = `preview-${agentId}`

  // Reuse existing session if available
  if (info.previewSessionId === sessionId) {
    console.log(`Reusing existing preview session: ${sessionId}`)
    return
  }

  // Create new session
  info.previewSessionId = sessionId
  await sandbox.process.createSession(sessionId)
  await sandbox.process.executeSessionCommand(sessionId, {
    command: config.command,
    async: true
  }, 0)
}
```

**Benefits:**
- "Preview All" followed by single-agent preview reuses servers
- Single-agent preview can be clicked multiple times without restart
- Reduces server startup latency on repeated previews

### Server Health Check

Poll server readiness instead of blind sleep:

```typescript
async waitForServerReady(
  agentId: string,
  port: number,
  maxAttempts: number = 30,
  intervalMs: number = 1000
): Promise<boolean> {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await sandbox.process.executeCommand(
        `curl -f -s -o /dev/null -w "%{http_code}" http://localhost:${port} || echo "000"`,
        '/workspace',
        undefined,
        5
      )

      const httpCode = response.result.trim()

      // Any HTTP response (200, 404, etc.) indicates server is ready
      if (httpCode !== "000" && httpCode !== "") {
        console.log(`Server ready on port ${port} (HTTP ${httpCode})`)
        return true
      }
    } catch {}

    await new Promise(r => setTimeout(r, intervalMs))
  }

  console.warn(`Server not ready after ${maxAttempts} attempts`)
  return false
}
```

**Usage:**
```typescript
await startPreviewServer(agentId, config)
const isReady = await waitForServerReady(agentId, config.port, 30, 1000)
if (!isReady) {
  throw new Error(`Server failed to start on port ${config.port}`)
}
const url = await getPreviewUrl(agentId, config.port)
```

## CLI Installation Pattern

Robust CLI installation with verification, fallback, and retry logic:

```typescript
async installClaudeCLI(agentId: string, maxRetries: number = 3): Promise<void> {
  const installCmd = 'bash -c "set -o pipefail; curl -fsSL https://claude.ai/install.sh | bash"'
  let lastError: Error | null = null

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Try curl install first
      const response = await sandbox.process.executeCommand(installCmd)
      if (response.exitCode !== 0) {
        throw new Error(`Install failed: ${response.result}`)
      }

      // Verify installation
      const verifyResponse = await sandbox.process.executeCommand(
        'claude --version', undefined, undefined, 30
      )
      if (verifyResponse.exitCode !== 0) {
        throw new Error('Claude CLI not found after installation')
      }
      return // Success

    } catch (err) {
      // Fallback: try npm install
      try {
        const response = await sandbox.process.executeCommand(
          'npm install -g @anthropic-ai/claude-code',
          undefined, undefined,
          300 // 5 min timeout for npm
        )
        if (response.exitCode !== 0) {
          throw new Error(`NPM install failed: ${response.result}`)
        }

        const verifyResponse = await sandbox.process.executeCommand(
          'claude --version', undefined, undefined, 30
        )
        if (verifyResponse.exitCode !== 0) {
          throw new Error('Claude CLI not found after npm installation')
        }
        return // Success

      } catch (npmErr) {
        lastError = npmErr instanceof Error ? npmErr : new Error(String(npmErr))
        const errorMsg = lastError.message

        // Check if retryable (network errors)
        const isRetryable =
          errorMsg.includes('ETIMEDOUT') ||
          errorMsg.includes('ECONNRESET') ||
          errorMsg.includes('ENOTFOUND') ||
          errorMsg.includes('EAI_AGAIN') ||
          errorMsg.includes('socket hang up')

        if (!isRetryable || attempt >= maxRetries) {
          throw lastError
        }

        // Exponential backoff: 5s, 10s, 20s
        const delayMs = 5000 * Math.pow(2, attempt - 1)
        await new Promise(r => setTimeout(r, delayMs))
      }
    }
  }
  throw lastError || new Error('Installation failed')
}
```

**Key points:**
- Use `set -o pipefail` in bash to propagate curl failures
- Verify CLI is executable with `--version` check after installation
- Set timeout on npm install (300s recommended) - network may be slow
- Retry up to 3 times on network errors (ETIMEDOUT, ECONNRESET, etc.)
- Exponential backoff prevents overwhelming failing services
- Daytona sandbox networking may need time to initialize after creation

## Best Practices

1. **Timeouts**: Set appropriate timeouts for long-running commands (15 min for Claude)
2. **Cleanup**: Always destroy sandboxes in finally blocks
3. **Parallel creation**: Use Promise.all() for creating multiple sandboxes
4. **Session streaming**: Use session-based execution for real-time output (not in MVP)
5. **Ephemeral mode**: Set `ephemeral: true` for auto-cleanup scenarios
6. **CLI verification**: Always verify CLI tools are installed after installation commands
7. **Error propagation**: Throw exceptions on non-zero exit codes to ensure proper error handling
