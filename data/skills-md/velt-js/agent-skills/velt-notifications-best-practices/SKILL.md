---
name: velt-notifications-best-practices
description: Velt Notifications implementation patterns and best practices for React, Next.js, and web applications. Use when adding in-app notifications, notification panels, email notifications via SendGrid, webhook integrations, or user notification preference management.
license: MIT
metadata:
  author: velt
  version: "1.0.0"
---

# Velt Notifications Best Practices

Comprehensive implementation guide for Velt's notification system in React and Next.js applications. Contains 12 rules across 8 categories, prioritized by impact to guide automated code generation and integration patterns.

## When to Apply

Reference these guidelines when:
- Adding in-app notifications to a React/Next.js application
- Setting up the VeltNotificationsTool and VeltNotificationsPanel
- Configuring notification tabs (For You, All, Documents, People)
- Accessing notification data via hooks or REST APIs
- Managing user notification preferences and channels
- Setting up email notifications with SendGrid
- Creating custom notifications via REST API
- Integrating with external services via webhooks

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core Setup | CRITICAL | `core-` |
| 2 | Panel Configuration | HIGH | `panel-` |
| 3 | Data Access | HIGH | `data-` |
| 4 | Settings Management | MEDIUM-HIGH | `settings-` |
| 5 | Notification Triggers | MEDIUM | `triggers-` |
| 6 | Delivery Channels | MEDIUM | `delivery-` |
| 7 | UI Customization | MEDIUM | `ui-` |
| 8 | Debugging & Testing | LOW-MEDIUM | `debug-` |

## Quick Reference

### 1. Core Setup (CRITICAL)

- `core-setup` — Enable notifications and add VeltNotificationsTool

### 2. Panel Configuration (HIGH)

- `panel-tabs` — Configure notification panel tabs (forYou, all, documents, people)
- `panel-display` — Control panel open mode (popover vs sidebar)

### 3. Data Access (HIGH)

- `data-hooks` — Use React hooks to access notification data
- `data-rest-api` — Use REST APIs for server-side notification management

### 4. Settings Management (MEDIUM-HIGH)

- `settings-channels` — Configure notification delivery channels

### 5. Notification Triggers (MEDIUM)

- `triggers-custom` — Create custom notifications via REST API

### 6. Delivery Channels (MEDIUM)

- `delivery-email` — Set up email notifications with SendGrid
- `delivery-webhooks` — Integrate with external services via webhooks

### 7. UI Customization (MEDIUM)

- `ui-wireframes` — Customize notification components with wireframes

### 8. Debugging & Testing (LOW-MEDIUM)

- `debug-common-issues` — Common issues and solutions

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/shared/core/core-setup.md
rules/shared/panel/panel-tabs.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Source pointers to official documentation

## Compiled Documents

- `AGENTS.md` — Compressed index of all rules with file paths (start here)
- `AGENTS.full.md` — Full verbose guide with all rules expanded inline
