---
name: aiogram-framework
description: Build, refactor, or troubleshoot Telegram bots using aiogram v3. Use when working with aiogram routers/handlers/filters, Dispatcher lifecycle, update delivery (long polling or webhook), FSM, middleware/DI, error handling, or aiogram utilities like keyboards, formatting, and i18n.
---

# Aiogram Framework

## Overview
Use this skill to design or modify aiogram-based bots in this repository with v3 patterns and the local docs/examples.

## Workflow
1. Choose update delivery (polling vs webhook) and note any scaling or multi-bot needs. See `references/updates.md`.
2. Define dispatcher/router layout and handler registration. See `references/quickstart.md` and `references/handlers-filters.md`.
3. Add filters and context injection (including custom filters) as needed. See `references/handlers-filters.md` and `references/middleware-di-errors.md`.
4. Add middleware and error handling for cross-cutting concerns. See `references/middleware-di-errors.md`.
5. Add FSM if the flow is multi-step or needs user state. See `references/fsm.md`.
6. Use utilities (keyboards, formatting, i18n) where they reduce boilerplate. See `references/utils.md`.
7. Cross-check with local examples under `examples/` before finalizing.

## Reference Map
- Quickstart and project shape: `references/quickstart.md`
- Update delivery details: `references/updates.md`
- Routers/handlers/filters: `references/handlers-filters.md`
- Middlewares, DI, errors: `references/middleware-di-errors.md`
- FSM and storage: `references/fsm.md`
- Utilities (keyboard/formatting/i18n): `references/utils.md`
