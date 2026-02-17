---
name: linear-notifications
description: Manage Linear notifications. Use for viewing, reading, and archiving notifications.
allowed-tools: Bash
---

# Notifications

```bash
# List unread notifications
linear-cli n list
linear-cli n list --output json

# Get unread count
linear-cli n count

# Mark as read
linear-cli n read NOTIFICATION_ID

# Mark all as read
linear-cli n read-all

# Archive a notification
linear-cli n archive NOTIFICATION_ID

# Archive all notifications
linear-cli n archive-all
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
