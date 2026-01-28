---
name: auth-flow
description: Claude Code authentication in headless Daytona sandboxes. Use when implementing AuthManager, setup wizard, credential validation, or handling OAuth token/API key injection.
---

# Auth Flow

> Sources: [Claude Code Setup](https://code.claude.com/docs/en/setup), [API Key Management](https://support.claude.com/en/articles/12304248-managing-api-key-environment-variables-in-claude-code)

## MVP Status

**AuthManager not implemented.** MVP uses SetupWizard to collect credentials at runtime (no persistence). Credentials passed directly to IPC handlers.

Current flow: User enters keys in SetupWizard → passed to `window.api.startRun()` → injected into sandbox env vars.

---

## The Problem

Claude Code requires browser-based OAuth authentication, but Daytona sandboxes are headless (no browser access).

## Environment Variables

| Variable | Description | Auth Method |
|----------|-------------|-------------|
| `ANTHROPIC_API_KEY` | API key from console.anthropic.com | Pay-as-you-go API |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth token from local auth | Subscription-based |

**Priority**: `ANTHROPIC_API_KEY` overrides OAuth token if both are set.

**Warning**: Setting `ANTHROPIC_API_KEY` bypasses any subscription and charges to API pay-as-you-go rates.

## Authentication Options for Sandboxes

### Option 1: API Key (Recommended for Sandboxes)

Most reliable for headless environments.

1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Store securely (Electron safeStorage)
3. Inject as environment variable in sandbox:

```typescript
const sandbox = await daytona.create({
  language: 'typescript',
  envVars: {
    ANTHROPIC_API_KEY: credentials.apiKey
  }
})
```

**Pros**: Simple, reliable, no OAuth complexity
**Cons**: Pay-as-you-go pricing (no subscription usage)

### Option 2: OAuth Token Transfer

Transfer OAuth credentials from authenticated local machine.

1. User authenticates locally: `claude` (opens browser)
2. Token stored at: `~/.config/claude-code/auth.json`
3. User provides token to app
4. App injects as environment variable:

```typescript
const sandbox = await daytona.create({
  language: 'typescript',
  envVars: {
    CLAUDE_CODE_OAUTH_TOKEN: credentials.oauthToken
  }
})
```

**Pros**: Uses subscription plan
**Cons**: Token may expire, manual extraction needed

### auth.json Location & Format

```
~/.config/claude-code/auth.json
```

The token is portable across machines (not IP/machine-bound).

**Security**: Treat like a password. Revoke immediately if compromised via Claude.ai account settings.

## AuthManager Implementation

```typescript
import { safeStorage } from 'electron'

interface Credentials {
  daytonaApiKey: string
  authMethod: 'api_key' | 'oauth_token'
  anthropicApiKey?: string
  claudeOAuthToken?: string
}

class AuthManager {
  private readonly STORAGE_KEY = 'multishot-credentials'

  async loadCredentials(): Promise<Credentials | null> {
    try {
      const encrypted = await this.readFromStorage()
      if (!encrypted) return null

      const decrypted = safeStorage.decryptString(encrypted)
      return JSON.parse(decrypted)
    } catch {
      return null
    }
  }

  async saveCredentials(credentials: Credentials): Promise<void> {
    const encrypted = safeStorage.encryptString(JSON.stringify(credentials))
    await this.writeToStorage(encrypted)
  }

  async validateApiKey(apiKey: string): Promise<boolean> {
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json'
        },
        body: JSON.stringify({
          model: 'claude-3-haiku-20240307',
          max_tokens: 1,
          messages: [{ role: 'user', content: 'hi' }]
        })
      })
      return response.ok || response.status === 400 // 400 = valid key, bad request
    } catch {
      return false
    }
  }

  async validateDaytonaKey(apiKey: string): Promise<boolean> {
    try {
      const { Daytona } = await import('@daytonaio/sdk')
      const daytona = new Daytona({ apiKey })
      await daytona.list({}, 1, 1) // Simple list call to verify
      return true
    } catch {
      return false
    }
  }

  getEnvVarsForSandbox(credentials: Credentials): Record<string, string> {
    if (credentials.authMethod === 'api_key' && credentials.anthropicApiKey) {
      return { ANTHROPIC_API_KEY: credentials.anthropicApiKey }
    }
    if (credentials.claudeOAuthToken) {
      return { CLAUDE_CODE_OAUTH_TOKEN: credentials.claudeOAuthToken }
    }
    return {}
  }

  async clearCredentials(): Promise<void> {
    await this.deleteFromStorage()
  }

  // Platform-specific storage methods
  private async readFromStorage(): Promise<Buffer | null> {
    // Implementation using electron-store or similar
  }

  private async writeToStorage(data: Buffer): Promise<void> {
    // Implementation
  }

  private async deleteFromStorage(): Promise<void> {
    // Implementation
  }
}

export const authManager = new AuthManager()
```

## Setup Wizard Flow

```
┌─────────────────────────────────────────┐
│         Welcome to Multishot            │
│                                         │
│  Enter your Daytona API Key:            │
│  [____________________________________] │
│                                         │
│  Get key: app.daytona.io                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Claude Authentication             │
│                                         │
│  ○ API Key (recommended for sandboxes)  │
│    - Pay-as-you-go pricing              │
│    - Most reliable                      │
│                                         │
│  ○ OAuth Token                          │
│    - Uses subscription plan             │
│    - May require refresh                │
│                                         │
│  [Continue]                             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│   (If API Key selected)                 │
│                                         │
│  Anthropic API Key:                     │
│  [____________________________________] │
│                                         │
│  Get key: console.anthropic.com         │
│                                         │
│  [Validate & Save]                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│   (If OAuth Token selected)             │
│                                         │
│  1. Run 'claude' locally to auth        │
│  2. Find token in:                      │
│     ~/.config/claude-code/auth.json     │
│  3. Paste token below:                  │
│                                         │
│  [____________________________________] │
│                                         │
│  [Validate & Save]                      │
└─────────────────────────────────────────┘
```

## Credential Storage

**Requirements:**
- Never store plaintext credentials in database or files
- Use Electron's `safeStorage` API (OS keychain integration)
- Environment variables exist only during sandbox lifetime
- Redact credentials in logs

```typescript
import { safeStorage } from 'electron'

// Check if encryption is available
if (safeStorage.isEncryptionAvailable()) {
  // Encrypt before storing
  const encrypted = safeStorage.encryptString(JSON.stringify(credentials))

  // Decrypt when reading
  const decrypted = safeStorage.decryptString(encrypted)
  const credentials = JSON.parse(decrypted)
}
```

## Error Detection & Recovery

Watch for these patterns in sandbox output:

| Error Pattern | Cause | Action |
|---------------|-------|--------|
| `"Authentication failed"` | Invalid credentials | Re-prompt setup wizard |
| `"OAuth token has expired"` | Token expired | Request new token |
| `"Invalid API key"` | Wrong or revoked key | Verify key in console |
| `"Rate limit exceeded"` | Too many requests | Back off, retry |
| `"Auth conflict"` | Both token and key set | Clear one method |

```typescript
function detectAuthError(output: string): 'expired' | 'invalid' | 'conflict' | null {
  if (output.includes('OAuth token has expired')) return 'expired'
  if (output.includes('Authentication failed')) return 'invalid'
  if (output.includes('Invalid API key')) return 'invalid'
  if (output.includes('Auth conflict')) return 'conflict'
  return null
}

// In IPC handler
sandbox.process.getSessionCommandLogs(session, cmdId,
  (stdout) => {
    const error = detectAuthError(stdout)
    if (error) {
      sendToRenderer('auth-error', { type: error })
    }
  },
  (stderr) => {
    const error = detectAuthError(stderr)
    if (error) {
      sendToRenderer('auth-error', { type: error })
    }
  }
)
```

## Checking Auth Status

In interactive Claude Code:
```bash
/status
```

Shows current authentication method and account info.

## Token Revocation

If credentials are compromised:

1. **API Key**: Revoke at console.anthropic.com → API Keys
2. **OAuth Token**: Revoke at claude.ai → Account Settings → Security → Active Sessions

## Best Practices

1. **Prefer API Key** for sandbox/headless use - most reliable
2. **Validate on entry** - test credentials before saving
3. **Handle expiry** - OAuth tokens can expire, detect and prompt
4. **Secure storage** - always use safeStorage, never plaintext
5. **Minimal scope** - only request permissions needed
6. **Clear on logout** - remove credentials when user logs out
