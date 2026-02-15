---
name: workos
description: Identify which WorkOS skill to load based on the user's task — covers AuthKit, SSO, RBAC, migrations, and all API references.
---

<!-- refined:sha256:4bc2401b2288 -->

# WorkOS Skill Router

## How to Use

When a user needs help with WorkOS, consult the tables below to route to the right skill.

## Loading Skills

**AuthKit skills** are registered plugins — load them directly via the Skill tool.

**All other skills** are bundled files. To load one, Read `skills/workos/{name}.md` from this plugin directory and follow its instructions.

## Disambiguation Rules

### Feature Skill vs API Reference
- **User asks about implementation** (how to set up, configure, integrate) → Load the feature skill
- **User explicitly asks for "API reference", "endpoints", "request/response format", or "API docs"** → Load the API reference skill
- **User asks "how does X work" or "what does X do"** → Load the feature skill (conceptual guide)

### AuthKit vs Feature-Specific Skills
- **User mentions "login", "sign-up", "authentication", "sign-in", "session management" WITHOUT naming a specific feature** → Route to AuthKit (detect framework below)
- **User mentions "SSO", "SAML", "OAuth connection" explicitly** → Load `workos-sso.md` (not AuthKit)
- **User mentions "MFA", "multi-factor", "2FA", "TOTP" explicitly** → Load `workos-mfa.md`
- **User mentions "roles", "permissions", "RBAC" explicitly** → Load `workos-rbac.md`
- **User mentions "directory sync", "SCIM", "user provisioning" explicitly** → Load `workos-directory-sync.md`

**Priority rule**: If the user mentions BOTH AuthKit AND a feature (e.g., "set up AuthKit with SSO"), load AuthKit first. The AuthKit skill will reference SSO configuration as a next step.

### Multiple Features Mentioned
Route to the MOST SPECIFIC skill first. Examples:
- "SSO with MFA" → Load `workos-sso.md` (SSO is the primary integration, MFA is a configuration option)
- "Audit logs for admin portal" → Load `workos-audit-logs.md` (audit logs is the feature being configured)
- "Directory sync with RBAC" → Load `workos-directory-sync.md` (directory sync is the primary feature)

The user can request additional skills after completing the first one.

### Migration Context
- **User says "migrate from [provider]" or "switch from [provider]"** → Load the migration skill for that provider
- **User asks "how to import users" or "bring existing users" WITHOUT naming a source** → Load `workos-migrate-other-services.md` (generic migration guide)
- **User mentions a provider not in the migration table** → Load `workos-migrate-other-services.md`

### Ambiguous Requests
- **"How do I use WorkOS?"** → Load `workos-authkit-base` for architectural overview, then detect framework if they want to proceed with installation
- **"WorkOS setup"** → Ask: "Are you setting up authentication (AuthKit), or a specific feature like SSO, MFA, or Directory Sync?"
- **"WorkOS API"** → Ask: "Which WorkOS feature are you working with?" Then route to the corresponding API reference
- **"WorkOS integration"** → Ask: "Are you integrating an identity provider (SSO/Directory Sync), or embedding WorkOS features in your app?"

## Topic → Skill Map

### AuthKit (load via Skill tool)

| User wants to...                              | Skill tool name                     |
| --------------------------------------------- | ----------------------------------- |
| Install AuthKit in Next.js                    | workos-authkit-nextjs               |
| Install AuthKit in React SPA                  | workos-authkit-react                |
| Install AuthKit with React Router             | workos-authkit-react-router         |
| Install AuthKit with TanStack Start           | workos-authkit-tanstack-start       |
| Install AuthKit in vanilla JS                 | workos-authkit-vanilla-js           |
| AuthKit architecture reference                | workos-authkit-base                 |

### Features (Read `skills/workos/{name}.md`)

| User wants to...                              | Read file                                       |
| --------------------------------------------- | ----------------------------------------------- |
| Configure email delivery                      | `skills/workos/workos-email.md` |
| Add WorkOS Widgets                            | `skills/workos/workos-widgets.md` |
| Encrypt data with Vault                       | `skills/workos/workos-vault.md` |
| Configure Single Sign-On                      | `skills/workos/workos-sso.md` |
| Implement RBAC / roles                        | `skills/workos/workos-rbac.md` |
| Add Multi-Factor Auth                         | `skills/workos/workos-mfa.md` |
| Set up IdP integration                        | `skills/workos/workos-integrations.md` |
| Handle WorkOS Events / webhooks               | `skills/workos/workos-events.md` |
| Set up Directory Sync                         | `skills/workos/workos-directory-sync.md` |
| Set up Custom Domains                         | `skills/workos/workos-custom-domains.md` |
| Set up Audit Logs                             | `skills/workos/workos-audit-logs.md` |
| Enable Admin Portal                           | `skills/workos/workos-admin-portal.md` |

### API References (Read `skills/workos/{name}.md`)

| User wants to...                              | Read file                                       |
| --------------------------------------------- | ----------------------------------------------- |
| Admin portal API Reference                    | `skills/workos/workos-api-admin-portal.md` |
| Audit logs API Reference                      | `skills/workos/workos-api-audit-logs.md` |
| Authkit API Reference                         | `skills/workos/workos-api-authkit.md` |
| Directory sync API Reference                  | `skills/workos/workos-api-directory-sync.md` |
| Events API Reference                          | `skills/workos/workos-api-events.md` |
| Organization API Reference                    | `skills/workos/workos-api-organization.md` |
| Roles API Reference                           | `skills/workos/workos-api-roles.md` |
| Sso API Reference                             | `skills/workos/workos-api-sso.md` |
| Vault API Reference                           | `skills/workos/workos-api-vault.md` |
| Widgets API Reference                         | `skills/workos/workos-api-widgets.md` |

### Migrations (Read `skills/workos/{name}.md`)

| User wants to...                              | Read file                                       |
| --------------------------------------------- | ----------------------------------------------- |
| Migrate from Supabase Auth                   | `skills/workos/workos-migrate-supabase-auth.md` |
| Migrate from Stytch                          | `skills/workos/workos-migrate-stytch.md` |
| Migrate from the standalone SSO API          | `skills/workos/workos-migrate-the-standalone-sso-api.md` |
| Migrate from other services                  | `skills/workos/workos-migrate-other-services.md` |
| Migrate from Firebase                        | `skills/workos/workos-migrate-firebase.md` |
| Migrate from Descope                         | `skills/workos/workos-migrate-descope.md` |
| Migrate from Clerk                           | `skills/workos/workos-migrate-clerk.md` |
| Migrate from Better Auth                     | `skills/workos/workos-migrate-better-auth.md` |
| Migrate from AWS Cognito                     | `skills/workos/workos-migrate-aws-cognito.md` |
| Migrate from Auth0                           | `skills/workos/workos-migrate-auth0.md` |

## AuthKit Installation Detection

If the user wants to install AuthKit, detect their framework by checking their project in this **exact priority order** (first match wins):

```
1. package.json contains "@tanstack/start"           → Skill tool: workos-authkit-tanstack-start
2. package.json contains "react-router"              → Skill tool: workos-authkit-react-router
3. next.config.js OR next.config.mjs exists          → Skill tool: workos-authkit-nextjs
4. vite.config.* exists AND package.json has "react" → Skill tool: workos-authkit-react
5. None of the above detected                        → Skill tool: workos-authkit-vanilla-js
```

**Why this order?**
- TanStack Start and React Router are checked FIRST because they can coexist with Vite+React, and we need the most specific match.
- Next.js is checked BEFORE generic Vite+React because Next.js projects may also have React in deps.
- Vanilla JS is the fallback for projects with no detectable framework (plain HTML/JS, non-React SPAs, or server-rendered apps without a supported framework).

**Edge cases:**
- **Multiple frameworks detected** (e.g., Next.js config + TanStack Start dep): Follow the priority order — TanStack Start wins.
- **Monorepo with multiple frameworks**: Ask the user which app/package they want to add AuthKit to, then detect framework in that specific directory.
- **Framework not listed** (e.g., SvelteKit, Remix, Angular): Load `workos-authkit-base` for architectural guidance, then direct the user to https://workos.com/docs/llms.txt to check if their framework is supported.

## General Decision Flow

```
User request about WorkOS?
  |
  +-- Mentions "migrate", "switch from", or "import from [provider]"?
  |     → Read skills/workos/workos-migrate-[provider].md
  |     → If provider not in table → Read skills/workos/workos-migrate-other-services.md
  |
  +-- Mentions SPECIFIC feature by name (SSO, MFA, RBAC, Directory Sync, Audit Logs, Vault, etc.)?
  |     → Read skills/workos/workos-[feature].md
  |     → Exception: If also mentions "API reference" → Read skills/workos/workos-api-[feature].md
  |
  +-- Explicitly asks for "API reference", "endpoints", or "request/response format"?
  |     → Read skills/workos/workos-api-[feature].md
  |     → If feature unclear → Ask which feature's API they need
  |
  +-- Mentions "login", "sign-up", "authentication", "sign-in", or "session" WITHOUT naming a feature?
  |     → Detect framework using AuthKit Installation Detection rules above
  |     → Skill tool: workos-authkit-[framework]
  |
  +-- Mentions "IdP", "identity provider", "SAML setup", or "OAuth provider setup"?
  |     → Read skills/workos/workos-integrations.md
  |
  +-- Mentions "webhooks" or "events"?
  |     → Read skills/workos/workos-events.md
  |
  +-- Request is vague ("How do I use WorkOS?", "WorkOS setup", "WorkOS integration")?
  |     → Ask clarifying question (see "Ambiguous Requests" above)
  |
  +-- No clear match?
  |     → WebFetch https://workos.com/docs/llms.txt
  |     → Find the relevant section URL
  |     → WebFetch that section
  |     → Synthesize an answer OR route to the closest skill if one exists
```

## Edge Cases

### Multiple Features in One Request
Examples:
- **"Set up SSO with MFA"** → Load `workos-sso.md` first (SSO is the primary integration). The skill will reference MFA configuration.
- **"AuthKit with custom domains"** → Load the AuthKit skill for their framework first. After installation, load `workos-custom-domains.md`.
- **"Directory Sync with RBAC"** → Load `workos-directory-sync.md` first (directory sync is the source of user data). RBAC is configured after users are synced.

**General rule**: Route to the skill that represents the PRIMARY integration or feature being configured. Dependent features can be loaded as follow-up steps.

### Framework Detection Failures
- **No framework detected** → Load `workos-authkit-vanilla-js` (covers plain HTML/JS and server-rendered apps)
- **Unsupported framework** (e.g., Laravel, Django, Ruby on Rails) → Load `workos-authkit-base` for architecture overview, then WebFetch https://workos.com/docs/llms.txt to check for backend SDK docs

### User Asks About Multiple Topics
Examples:
- **"How do SSO and Directory Sync work together?"** → Load `workos-sso.md` first (explains SSO connections), then load `workos-directory-sync.md` (explains user provisioning from IdP)
- **"What's the difference between SSO and AuthKit?"** → Load `workos-authkit-base` (explains AuthKit's role), then explain that SSO is a CONNECTION TYPE that AuthKit can use

### No Skill Matches
If the user's request does not match ANY skill in the tables above:
1. WebFetch https://workos.com/docs/llms.txt to get the full documentation index
2. Identify the relevant section URL from the index
3. WebFetch that section URL
4. If the fetched content suggests a skill exists but wasn't matched, re-evaluate routing rules
5. Otherwise, synthesize an answer from the fetched documentation

## If No Skill Matches

WebFetch the full docs index: https://workos.com/docs/llms.txt
Then WebFetch the specific section URL for the user's topic.
