---
name: workos-authkit-base
description: Architectural reference for WorkOS AuthKit integrations. Fetch README first for implementation details.
---

# WorkOS AuthKit Integration

## Step 1: Fetch AuthKit Documentation (BLOCKING)

**STOP. Do not proceed until complete.**

WebFetch: `https://workos.com/docs/user-management/authkit`

This page is the source of truth for AuthKit concepts, supported frameworks, and setup requirements. If this skill conflicts with the docs, follow the docs.

## Step 2: Detect User's Framework

Run these commands to identify the project's framework. Check each in order; use the first match.

```bash
# Next.js
grep -q '"next"' package.json 2>/dev/null && echo "DETECTED: nextjs"

# React Router / Remix
grep -qE '"react-router"|"@remix-run"' package.json 2>/dev/null && echo "DETECTED: react-router"

# TanStack Start
grep -q '"@tanstack/start"' package.json 2>/dev/null && echo "DETECTED: tanstack-start"

# React (standalone SPA — check AFTER framework-specific entries)
grep -q '"react"' package.json 2>/dev/null && echo "DETECTED: react"
```

If none match, check for a plain HTML/JS project:

```bash
# Vanilla JS — no package.json or no framework dependency
[ ! -f package.json ] && echo "DETECTED: vanilla-js"
ls index.html 2>/dev/null && echo "DETECTED: vanilla-js"
```

## Step 3: Route to Framework-Specific Skill

Use the detection result from Step 2 to select the correct skill. **Do not continue past this step if a framework matched — switch to the matching skill immediately.**

```
Detection result         -->  Skill to invoke
─────────────────────────────────────────────
nextjs                   -->  workos-authkit-nextjs
react-router             -->  workos-authkit-react-router
tanstack-start           -->  workos-authkit-tanstack-start
react                    -->  workos-authkit-react
vanilla-js               -->  workos-authkit-vanilla-js
```

**If a framework is detected:** Stop here. The framework-specific skill handles everything from install through verification.

**If no framework is detected:** Ask the user: "Which framework are you using? (Next.js, React, React Router, TanStack Start, or vanilla JS)". If they name something not listed (e.g., Astro, Remix, SvelteKit), use `workos-authkit-vanilla-js` as the closest starting point and WebFetch `https://workos.com/docs/user-management/authkit` for framework-specific guidance.

## Related Skills

- **workos-authkit-nextjs** — Next.js App Router (13+), server-side rendering
- **workos-authkit-react** — React SPA with client-side AuthKit
- **workos-authkit-react-router** — React Router / Remix integration
- **workos-authkit-tanstack-start** — TanStack Start framework
- **workos-authkit-vanilla-js** — Plain HTML/JS without a framework
