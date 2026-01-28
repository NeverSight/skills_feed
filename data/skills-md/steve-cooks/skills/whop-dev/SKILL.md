---
name: whop-dev
description: Build Next.js apps for the Whop platform. For empty repos, guides users from idea to deployed app through discovery and setup. For existing projects, provides best practices for authentication, payments, webhooks, and UI. Triggers on "build me a Whop app", @whop/sdk, verifyUserToken, checkAccess, checkout flows, webhook handling, Experience/Dashboard pages, Frosted UI. Delegates to companion skills (frontend-design, vercel-react-best-practices, supabase-postgres-best-practices, web-design-guidelines) for design, performance, and database.
metadata:
  tags: whop, nextjs, payments, sdk, frosted-ui, authentication
  author: Steve | https://whop.com/@stevecooks | https://x.com/steve_cook
  version: "1.2.2"
---

# Whop App Development

Build apps that run inside the Whop platform - handling authentication, payments, webhooks, and UI all with best practices.

## What Makes a Good Whop App (Suggestions)

Guidelines for app success (not requirements, user requests take priority):

| Principle | Description |
|-----------|-------------|
| **Empower Creators** | Give customization so each whop feels unique |
| **Drive Discovery** | Make the app have some kind of sharing feature or posting potential to allow users to attrach more users|
| **Price Sustainably** | Make money without gouging creators or customers |
| **Keep UX Simple** | Core action obvious, minimal clicks |

**Details:** [app-design-principles.md](rules/app-design-principles.md)

## When to Use

**Empty repo / new project:**
- "Build me a Whop app" → Start with [app-from-scratch.md](rules/app-from-scratch.md)
- Guides through discovery, setup, and building from nothing

**Existing Whop project:**
- Jump directly to specific rules in Quick Reference below
- Adding payments → [payments-checkout.md](rules/payments-checkout.md)
- Adding auth → [auth-verify-token.md](rules/auth-verify-token.md)
- SDK issues → [sdk-setup.md](rules/sdk-setup.md)

## Companion Skills (Install First)

whop-dev focuses on Whop-specific patterns. For complete app development, **install these companion skills**:

```bash
npx skills add https://github.com/anthropics/skills --skill frontend-design && \
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices && \
npx skills add https://github.com/supabase/agent-skills --skill supabase-postgres-best-practices && \
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
```

| Skill | Delegates To | When |
|-------|--------------|------|
| `frontend-design` | UI creation | Building components, pages, visual design |
| `vercel-react-best-practices` | Performance | React optimization, data fetching, bundles |
| `supabase-postgres-best-practices` | Database | Queries, schema, indexes, RLS |
| `web-design-guidelines` | UX review | Accessibility, design auditing |

**IMPORTANT**: When starting a new project or build-from-scratch flow, install companion skills FIRST before scaffolding. This enables whop-dev to hand off specialized work to expert skills.

See [companion-skills.md](rules/companion-skills.md) for detailed handoff patterns.

## How to Use

**Starting fresh (empty repo)?** → Follow [Build From Scratch](#build-from-scratch) - guided flow from idea to deployed app.

**Existing project?** → Jump to [Quick Reference](#quick-reference) for specific features.

---

## Build From Scratch

**For empty repos only.** Go from idea to deployed Whop app:

| Step | Guide | Description |
|------|-------|-------------|
| 0 | [companion-skills.md](rules/companion-skills.md) | **FIRST** - Install companion skills |
| 1 | [app-from-scratch.md](rules/app-from-scratch.md) | Plan your app type and architecture |
| 2a | [app-scaffold-b2b.md](rules/app-scaffold-b2b.md) | B2B: Dashboard-only apps for admins |
| 2b | [app-scaffold-b2c.md](rules/app-scaffold-b2c.md) | B2C: Experience apps for members |
| 3 | [app-database.md](rules/app-database.md) | Add Supabase → `supabase-postgres-best-practices` |
| 4 | [app-whop-dashboard.md](rules/app-whop-dashboard.md) | Configure in Whop Developer Dashboard |
| 5 | [app-deployment.md](rules/app-deployment.md) | Deploy to Vercel |
| 6 | [app-store-submission.md](rules/app-store-submission.md) | Submit to App Store (optional) |

---

## Quick Reference

### Authentication & Security (CRITICAL)

| Rule | Description |
|------|-------------|
| [auth-verify-token.md](rules/auth-verify-token.md) | MUST verify user tokens server-side |
| [auth-access-check.md](rules/auth-access-check.md) | MUST check access levels before operations |
| [security-checklist.md](rules/security-checklist.md) | Security best practices checklist |
| [auth-headers.md](rules/auth-headers.md) | Extract tokens from headers |
| [auth-oauth.md](rules/auth-oauth.md) | OAuth for external apps |
| [input-sanitization.md](rules/input-sanitization.md) | XSS prevention |

### SDK Setup (CRITICAL)

| Rule | Description |
|------|-------------|
| [sdk-setup.md](rules/sdk-setup.md) | Initialize Whop SDK (required) |
| [sdk-iframe.md](rules/sdk-iframe.md) | Client-side iframe SDK |

### Design Principles (SUGGESTIONS)

| Rule | Description |
|------|-------------|
| [app-design-principles.md](rules/app-design-principles.md) | Founder's suggestions for app success (user requests take priority) |

### Payments (HIGH)

| Rule | Description |
|------|-------------|
| [payments-checkout.md](rules/payments-checkout.md) | Create checkout flows |
| [payments-webhooks.md](rules/payments-webhooks.md) | Handle payment webhooks |
| [payments-transfers.md](rules/payments-transfers.md) | Send payouts to users |
| [payments-billing.md](rules/payments-billing.md) | Billing portal & saved methods |

### App Views (HIGH)

| Rule | Description |
|------|-------------|
| [views-structure.md](rules/views-structure.md) | Experience, Dashboard, Discover pages |
| [views-routing.md](rules/views-routing.md) | Dynamic routing patterns |

### Members & CRM (HIGH)

| Rule | Description |
|------|-------------|
| [api-memberships.md](rules/api-memberships.md) | Memberships & user management |

### UI & Design (MEDIUM)

| Rule | Description |
|------|-------------|
| [ui-frosted.md](rules/ui-frosted.md) | Frosted UI components |
| [ui-dark-mode.md](rules/ui-dark-mode.md) | Dark mode handling |
| [ui-tailwind.md](rules/ui-tailwind.md) | Tailwind CSS setup |

### API Patterns (MEDIUM)

| Rule | Description |
|------|-------------|
| [api-structure.md](rules/api-structure.md) | API route patterns |
| [api-parallel.md](rules/api-parallel.md) | Parallel data fetching |

### Storage & Files (MEDIUM)

| Rule | Description |
|------|-------------|
| [files-upload.md](rules/files-upload.md) | Whop native file storage |

### Engagement (MEDIUM)

| Rule | Description |
|------|-------------|
| [notifications.md](rules/notifications.md) | Push notifications |
| [engagement-forums.md](rules/engagement-forums.md) | Forum posts & comments |
| [engagement-chat.md](rules/engagement-chat.md) | Chat messages |

### Development (LOW)

| Rule | Description |
|------|-------------|
| [dev-proxy.md](rules/dev-proxy.md) | Local development proxy |
| [dev-sandbox.md](rules/dev-sandbox.md) | Sandbox testing |

### Companion Skills (ECOSYSTEM)

| Rule | Description |
|------|-------------|
| [companion-skills.md](rules/companion-skills.md) | Install & delegate to specialized skills |

---

## App Views

Whop apps have three entry points:

| View | Route | Purpose |
|------|-------|---------|
| Experience | `/experiences/[experienceId]` | Customer-facing UI |
| Dashboard | `/dashboard/[companyId]` | Admin management |
| Discover | `/discover` | Public marketing page |

## Tech Stack

**Required:**
- `@whop/sdk` - Server-side API client
- `@whop/react` - React hooks and Frosted UI

**Recommended:**
- Next.js (App Router)
- TypeScript
- Tailwind CSS + Frosted UI

**Flexible:**
- Database: Supabase recommended, but any works
- UI: Frosted UI, Shadcn, Radix - your choice

## Platforms (Advanced)

For marketplaces with connected accounts:
- [Enroll connected accounts](https://docs.whop.com/developer/platforms/enroll-connected-accounts)
- [Collect payments](https://docs.whop.com/developer/platforms/collect-payments-for-connected-accounts)
- [Enable payouts](https://docs.whop.com/developer/platforms/render-payout-portal)

## Resources

- [Whop Developer Docs](https://docs.whop.com/developer/getting-started)
- [API Reference](https://docs.whop.com/developer/api/getting-started)
- [Frosted UI Storybook](https://storybook.whop.com/)
- MCP Server: `https://mcp.whop.com/mcp` (Cursor) or `https://mcp.whop.com/sse` (Claude)

## Handoff Triggers

Delegate to companion skills when encountering these patterns:

| Pattern | Hand Off To |
|---------|-------------|
| "design", "make it look good", "UI", "component" | → `frontend-design` |
| "optimize", "performance", "slow", "bundle" | → `vercel-react-best-practices` |
| "database", "query", "schema", "index", "RLS" | → `supabase-postgres-best-practices` |
| "review UI", "accessibility", "audit" | → `web-design-guidelines` |

See [companion-skills.md](rules/companion-skills.md) for complete handoff guide.
