---
name: api-integrator
description: Integrate third-party APIs and SDKs into projects. Use when user wants to connect to external services (Resend, Stripe, Zendesk, Ahrefs, Twilio, etc.) or asks to "integrate", "connect", or "add" an API. Handles documentation research, SDK selection, project pattern matching, and implementation.
---

# API Integrator

Integrate third-party APIs/SDKs by researching docs, matching project patterns, and implementing based on user intent.

## Workflow

### 1. Gather Requirements

Collect from user:
- **API/service name** (required)
- **Intent** - what they want to accomplish (required)
- **Docs URL** (optional - will search if not provided)

### 2. Research

Search web for:
1. `"[API name] API documentation"`
2. `"[API name] [project-language] SDK"` (e.g., "Stripe TypeScript SDK")
3. `"[API name] OpenAPI spec"` (if available, helps identify endpoints)

**SDK preference**: Use SDK matching project language if available, otherwise raw API.

### 3. Analyze Project

Find existing patterns:
- **Language/framework** detection
- **Service location**: `src/services/`, `lib/api/`, `utils/`
- **Naming**: `XxxService`, `XxxClient`, `XxxApi`
- **HTTP client**: axios, fetch, got (match existing usage)
- **Types**: TypeScript interfaces, Zod schemas
- **Error handling**: existing patterns
- **Env vars**: `.env` structure

### 4. Propose Implementation

Based on intent, propose:
- Specific endpoints/methods to implement
- Service structure
- Types needed

**Get user confirmation before implementing.**

### 5. Implement

Following project conventions:
- Service/wrapper class
- Types/interfaces for responses
- Error handling matching project patterns
- Requested functionality

### 6. Output Next Steps

End with checklist:
```
## Next Steps to Complete Integration

- [ ] Add `API_KEY_NAME` to `.env`
- [ ] Get API key from [service dashboard URL]
- [ ] [Any other setup: domain verification, webhooks, etc.]
```

## Example

**User**: "Connect to the Resend API to send welcome emails"

1. **Research**: Find Resend has TypeScript SDK (`resend`)
2. **Project**: TypeScript, services in `src/services/`, uses interfaces
3. **Propose**: Create `EmailService` with `sendWelcomeEmail()` → user confirms
4. **Implement**: `src/services/email.service.ts` following patterns
5. **Next Steps**: Add `RESEND_API_KEY`, get key from resend.com, verify domain
