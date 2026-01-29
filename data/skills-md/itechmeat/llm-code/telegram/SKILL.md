---
name: telegram
description: "Telegram Bot development playbook: bot fundamentals, aiogram 3 patterns (handlers/middlewares/FSM), webhooks, keyboard UX, inline mode, Mini Apps, payments (Stars/subscriptions), authentication. Keywords: Telegram, aiogram, Bot API, webhook, handlers, middlewares, FSM, inline keyboard, reply keyboard, callback_query, inline mode, Mini Apps, Web Apps, payments, Telegram Stars, Login Widget."
version: "3.24.0"
release_date: "2026-01-02"
---

# Telegram (Skill Router)

Router skill: pick the reference that matches your task.

## Quick Navigation

| Task                                    | Reference                                             |
| --------------------------------------- | ----------------------------------------------------- |
| New to Telegram bots                    | [bots-overview.md](references/bots-overview.md)       |
| Bot capabilities overview               | [bot-features.md](references/bot-features.md)         |
| API methods/types                       | [bot-api.md](references/bot-api.md)                   |
| Webhook setup & security                | [webhooks.md](references/webhooks.md)                 |
| aiogram 3 handlers/FSM                  | [aiogram-patterns.md](references/aiogram-patterns.md) |
| Keyboard UX                             | [keyboard-design.md](references/keyboard-design.md)   |
| Inline mode                             | [inline-mode.md](references/inline-mode.md)           |
| Mini Apps (Web Apps)                    | [mini-apps.md](references/mini-apps.md)               |
| Payments (Stars)                        | [payments.md](references/payments.md)                 |
| Authentication (Login Widget, URL Auth) | [authentication.md](references/authentication.md)     |
| Rate limits & performance               | [performance.md](references/performance.md)           |

## Critical Prohibitions

- ❌ No polling + webhooks simultaneously for same bot
- ❌ No hardcoded tokens/secrets — use environment variables
- ❌ No secrets in callback_data or logs
- ❌ No ignoring `answer_callback_query` — always respond
- ❌ No blocking work in webhook handlers — use background tasks
- ❌ No trusting Login Widget data without hash verification

## Definition of Done

- [ ] Webhook handlers validate `X-Telegram-Bot-Api-Secret-Token`
- [ ] Keyboards: max 2 buttons per row, mobile-first
- [ ] Callback data validated, not trusted blindly
- [ ] Handlers are idempotent or have de-duplication

## Related Skills

- [PostgreSQL](../postgresql/SKILL.md) — for database layer
- [FastAPI](../fastapi-api-layer/SKILL.md) — for API layer (if exists)
