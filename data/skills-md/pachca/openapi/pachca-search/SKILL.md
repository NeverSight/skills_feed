---
name: pachca-search
description: >
  Полнотекстовый поиск по сотрудникам, чатам и сообщениям. Используй когда нужно:
  найти сообщение по тексту, найти чат по названию, найти сотрудника по имени. НЕ
  используй для: просмотра списка сотрудников (→ pachca-users), просмотра списка
  чатов (→ pachca-chats).
allowed-tools: Bash(curl *)
---

# pachca-search

Base URL: `https://api.pachca.com/api/shared/v1`
Авторизация: `Authorization: Bearer <ACCESS_TOKEN>`
Токен: бот (Автоматизации → Интеграции → API) или пользователь (Автоматизации → API).
Если токен неизвестен — спроси у пользователя перед выполнением запросов.

## Когда НЕ использовать

- найти сотрудника, создать пользователя, список сотрудников → **pachca-users**
- создать канал, создать беседу, создать чат → **pachca-chats**

## Пошаговые сценарии

### Найти сообщение по тексту

**Требуется:** скоуп `search:messages`

1. GET /search/messages?query=текст — полнотекстовый поиск. Пагинация: `limit` (до 200) и `cursor`. Общее количество результатов — в `meta.total`

```bash
curl "https://api.pachca.com/api/shared/v1/search/messages?query=отчёт&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

> Поиск возвращает сообщения из всех доступных чатов. Фильтры: `chat_ids[]` (конкретные чаты), `user_ids[]` (авторы), `active` (true — активные чаты, false — архивированные), `created_from`/`created_to` (период). Поле `root_chat_id` в ответе показывает корневой чат для сообщений из тредов.

### Найти чат по названию

**Требуется:** скоуп `search:chats`

1. GET /search/chats?query=название — полнотекстовый поиск по чатам. Пагинация: `limit` (до 100) и `cursor`

```bash
curl "https://api.pachca.com/api/shared/v1/search/chats?query=Разработка&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

> Фильтры: `active` (true — активные, false — архивированные), `chat_subtype` (`discussion` или `thread`), `personal` (true — только личные), `created_from`/`created_to` (период). Результаты сортируются по релевантности.

### Найти сотрудника по имени

**Требуется:** скоуп `search:users`

1. GET /search/users?query=имя — полнотекстовый поиск по сотрудникам. Пагинация: `limit` (до 200) и `cursor`. Сортировка: `sort=alphabetical` для алфавитного порядка, `sort=by_score` (по умолчанию) для релевантности

```bash
curl "https://api.pachca.com/api/shared/v1/search/users?query=Олег&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

> Фильтры: `company_roles[]` (`user`, `admin`, `multi_guest`, `guest`), `created_from`/`created_to` (период). Альтернатива GET /users?query= с более точным ранжированием.

## Ограничения и gotchas

- Rate limit: ~50 req/sec. При 429 — подожди и повтори.
- `limit`: максимум — 100 (GET /search/chats), 200 (GET /search/messages), 200 (GET /search/users)
- Пагинация: cursor-based (limit + cursor)

## Эндпоинты

| Метод | Путь | Скоуп |
|-------|------|-------|
| GET | /search/chats | search:chats |
| GET | /search/messages | search:messages |
| GET | /search/users | search:users |

## Подробнее

см. [references/endpoints.md](references/endpoints.md)
