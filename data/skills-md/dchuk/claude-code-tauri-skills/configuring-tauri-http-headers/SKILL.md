---
name: configuring-tauri-http-headers
description: Guides developers through configuring HTTP headers security in Tauri v2 applications, covering security headers, custom headers, and CORS configuration for secure cross-origin resource handling.
---

# Tauri HTTP Headers Security Configuration

This skill covers HTTP headers configuration in Tauri v2.1.0+, enabling developers to set security headers in webview responses.

## Overview

Tauri allows configuring HTTP headers that are included in responses to the webview. These headers apply to production builds and do not affect IPC messages or error responses.

## Supported Headers (Allowlist)

Tauri restricts header configuration to a specific allowlist for security:

### CORS Headers
- `Access-Control-Allow-Credentials`
- `Access-Control-Allow-Headers`
- `Access-Control-Allow-Methods`
- `Access-Control-Expose-Headers`
- `Access-Control-Max-Age`

### Cross-Origin Policies
- `Cross-Origin-Embedder-Policy`
- `Cross-Origin-Opener-Policy`
- `Cross-Origin-Resource-Policy`

### Security Headers
- `X-Content-Type-Options`
- `Permissions-Policy`
- `Timing-Allow-Origin`
- `Service-Worker-Allowed`

### Testing Only
- `Tauri-Custom-Header` (not for production use)

## Configuration in tauri.conf.json

Headers are configured under `app.security.headers` in `src-tauri/tauri.conf.json`.

### Value Formats

1. **String**: Direct assignment
2. **Array**: Items joined by commas
3. **Object**: Key-value pairs formatted as "key value", joined by semicolons
4. **Null**: Header is ignored

### Basic Configuration Example

```json
{
  "app": {
    "security": {
      "headers": {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "X-Content-Type-Options": "nosniff"
      }
    }
  }
}
```

### Comprehensive Configuration Example

```json
{
  "app": {
    "security": {
      "headers": {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Cross-Origin-Resource-Policy": "same-origin",
        "Timing-Allow-Origin": [
          "https://example.com",
          "https://api.example.com"
        ],
        "X-Content-Type-Options": "nosniff",
        "Permissions-Policy": {
          "camera": "()",
          "microphone": "()",
          "geolocation": "(self)"
        },
        "Access-Control-Allow-Methods": ["GET", "POST", "PUT", "DELETE"],
        "Access-Control-Allow-Headers": ["Content-Type", "Authorization"],
        "Access-Control-Max-Age": "86400"
      },
      "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost"
    }
  }
}
```

## Enabling SharedArrayBuffer

`SharedArrayBuffer` requires specific cross-origin policies. Configure both headers together:

```json
{
  "app": {
    "security": {
      "headers": {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp"
      }
    }
  }
}
```

## CORS Configuration Examples

### Restrictive CORS (Recommended for Production)

```json
{
  "app": {
    "security": {
      "headers": {
        "Cross-Origin-Resource-Policy": "same-origin",
        "Access-Control-Allow-Credentials": "false",
        "Access-Control-Allow-Methods": ["GET"],
        "Access-Control-Max-Age": "3600"
      }
    }
  }
}
```

### Permissive CORS (Development/API Scenarios)

```json
{
  "app": {
    "security": {
      "headers": {
        "Cross-Origin-Resource-Policy": "cross-origin",
        "Access-Control-Allow-Methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "Access-Control-Allow-Headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "Access-Control-Expose-Headers": ["Content-Length", "X-Request-Id"],
        "Access-Control-Max-Age": "86400"
      }
    }
  }
}
```

## Development Server Configuration

Development frameworks require separate header configuration for their dev servers. Tauri header injection only applies to production builds.

### Vite (React, Vue, Svelte, Solid, Qwik)

```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'X-Content-Type-Options': 'nosniff'
    }
  }
});
```

### Angular

```json
// angular.json
{
  "projects": {
    "your-app": {
      "architect": {
        "serve": {
          "options": {
            "headers": {
              "Cross-Origin-Opener-Policy": "same-origin",
              "Cross-Origin-Embedder-Policy": "require-corp"
            }
          }
        }
      }
    }
  }
}
```

### Nuxt

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  vite: {
    server: {
      headers: {
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp'
      }
    }
  }
});
```

### Next.js

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin'
          },
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'require-corp'
          }
        ]
      }
    ];
  }
};
```

### Trunk (Yew, Leptos)

```toml
# Trunk.toml
[serve]
headers = { "Cross-Origin-Opener-Policy" = "same-origin", "Cross-Origin-Embedder-Policy" = "require-corp" }
```

## Security Headers Reference

### Cross-Origin-Opener-Policy (COOP)

Controls window opener relationships:

| Value | Description |
|-------|-------------|
| `unsafe-none` | Default, allows opener access |
| `same-origin` | Isolates browsing context to same-origin |
| `same-origin-allow-popups` | Same-origin but allows popups |

### Cross-Origin-Embedder-Policy (COEP)

Controls resource embedding:

| Value | Description |
|-------|-------------|
| `unsafe-none` | Default, no restrictions |
| `require-corp` | Requires CORP or CORS for cross-origin resources |
| `credentialless` | Cross-origin requests without credentials |

### Cross-Origin-Resource-Policy (CORP)

Controls who can load your resources:

| Value | Description |
|-------|-------------|
| `same-site` | Only same-site requests |
| `same-origin` | Only same-origin requests |
| `cross-origin` | Allows cross-origin requests |

### X-Content-Type-Options

Prevents MIME type sniffing:

```json
{
  "X-Content-Type-Options": "nosniff"
}
```

### Permissions-Policy

Controls browser feature access:

```json
{
  "Permissions-Policy": {
    "camera": "()",
    "microphone": "()",
    "geolocation": "(self)",
    "fullscreen": "(self)"
  }
}
```

## Best Practices

1. **Configure Both Dev and Prod**: Set headers in both your framework's dev server config and `tauri.conf.json` for consistent behavior.

2. **Use Restrictive Defaults**: Start with restrictive policies and loosen only as needed.

3. **Enable COOP/COEP Together**: For `SharedArrayBuffer` support, both headers must be configured.

4. **Separate CSP Configuration**: Content-Security-Policy is configured under `app.security.csp`, not in the headers section.

5. **Avoid Tauri-Custom-Header in Production**: This header is for testing purposes only.

6. **Test Cross-Origin Scenarios**: Verify that CORS headers work correctly with your API endpoints.

## Troubleshooting

### SharedArrayBuffer Not Available

Ensure both headers are set:
```json
{
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Embedder-Policy": "require-corp"
}
```

### Headers Not Applied in Development

Headers in `tauri.conf.json` only apply to production builds. Configure your dev server separately.

### CORS Errors with External APIs

Add required headers for cross-origin requests:
```json
{
  "Access-Control-Allow-Methods": ["GET", "POST", "OPTIONS"],
  "Access-Control-Allow-Headers": ["Content-Type", "Authorization"]
}
```

### Custom Headers Not Visible

Expose custom headers via:
```json
{
  "Access-Control-Expose-Headers": ["X-Custom-Header", "X-Request-Id"]
}
```

## Version Requirements

- Tauri v2.1.0 or later required for HTTP headers configuration
- Headers feature is not available in earlier versions

## Related Configuration

- **CSP**: Configure under `app.security.csp` for Content Security Policy
- **Capabilities**: Use Tauri's capability system for fine-grained permissions
- **IPC Security**: Headers do not affect IPC message handling
