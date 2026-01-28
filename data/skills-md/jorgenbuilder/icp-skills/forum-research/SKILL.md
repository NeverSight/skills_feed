---
name: forum-research
description: Research and read content on forum.dfinity.org (Discourse). Use when the user asks to browse, search, summarize, or analyze Dfinity forum topics or users. Read-only access with authenticated browsing and JSON endpoints.
---

# Forum Research (Dfinity)

## Scope

This skill supports read-only research on `forum.dfinity.org` using authenticated browsing and Discourse JSON endpoints.

## Required dependency

This skill depends on the `agent-browser` skill from vercel-labs. Install it first:

```
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser
```

## Guardrails (strict)

- Read-only only. Never post, reply, like, bookmark, or edit.
- Use GET requests for all research and reading.
- Exception: authentication may require a POST to the login endpoint. No other non-GET requests are allowed.
- If a user asks to post or modify content, refuse and explain the read-only policy.

## Stage 1: login only

1. Obtain credentials using one of the approved methods in `reference.md`.
2. Navigate to `https://forum.dfinity.org/login`.
3. Always choose the username/password option on the login page (ignore GitHub and passkey options).
4. Fill username and password, then submit.
5. Confirm login by opening `https://forum.dfinity.org/u/<username>.json`.

## Discourse JSON access

Discourse supports a JSON view for most pages by appending `.json` to the URL. Prefer JSON for structured reading:

- Topic: `https://forum.dfinity.org/t/<slug>/<id>.json`
- User: `https://forum.dfinity.org/u/<username>.json`
- Latest: `https://forum.dfinity.org/latest.json`

## Additional resources

- Credential sourcing, prompts, and constraints: `reference.md`
- Login examples: `examples.md`
- Forum category structure and navigation guide: `categories.md`
