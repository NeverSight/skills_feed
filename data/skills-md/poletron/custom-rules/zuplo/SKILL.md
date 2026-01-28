---
name: zuplo
description: >
  Zuplo API gateway configuration and best practices.
  Trigger: When configuring Zuplo API gateway.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with zuplo"

## When to Use

Use this skill when:
- Configuring Zuplo API gateway
- Setting up API authentication
- Implementing rate limiting
- Managing API policies

---

## Critical Patterns

### Route Configuration (REQUIRED)

```json
{
  "routes": [
    {
      "path": "/api/users",
      "methods": ["GET", "POST"],
      "handler": {
        "module": "$import(@zuplo/runtime)",
        "export": "urlRewriteHandler",
        "options": {
          "rewritePattern": "https://api.example.com/users"
        }
      },
      "policies": {
        "inbound": ["rate-limit", "api-key-auth"]
      }
    }
  ]
}
```

### API Key Auth (REQUIRED)

```typescript
// ✅ ALWAYS: Use built-in API key authentication
export default {
  policies: {
    inbound: [
      {
        name: "api-key-auth",
        policyType: "api-key-inbound",
        handler: {
          export: "ApiKeyInboundPolicy",
          module: "$import(@zuplo/runtime)"
        }
      }
    ]
  }
};
```

---

## Decision Tree

```
Need auth?                 → Use api-key-inbound policy
Need rate limiting?        → Use rate-limit policy
Need caching?              → Use cache policy
Need transforms?           → Use custom policy handler
Need monitoring?           → Enable analytics
```

---

## Resources

- **Gateway Setup**: [gateway-setup.md](gateway-setup.md)
- **GitOps**: [gitops.md](gitops.md)
- **Performance**: [performance.md](performance.md)
- **Security**: [security.md](security.md)
