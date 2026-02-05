---
name: noticed
description: Build Rails notifications with the noticed gem. Full lifecycle - create notifiers, configure delivery methods (email, Slack, push, SMS, ActionCable), debug, and test. Covers individual and bulk delivery patterns.
---

<essential_principles>

## How Noticed Works

Noticed is a Rails notification system that delivers notifications across multiple channels simultaneously.

### 1. Notifiers Define What and How

Each notification is a class inheriting from `Noticed::Event`. It defines:
- What params are required
- Which delivery methods to use
- Helper methods via `notification_methods` block

```ruby
class NewCommentNotifier < Noticed::Event
  required_params :comment

  deliver_by :email do |config|
    config.mailer = "CommentMailer"
    config.method = :new_comment
  end

  notification_methods do
    def comment
      record
    end
  end
end
```

### 2. Individual vs Bulk Delivery

- **Individual** (`deliver_by`): One notification per recipient
- **Bulk** (`bulk_deliver_by`): One notification for all (e.g., team Slack channel)

### 3. The Record Pattern

Always pass the primary object as `record:`:
```ruby
NewCommentNotifier.with(record: @comment).deliver(@recipients)
```

This enables proper associations and querying from the record side.

### 4. Async by Default

Noticed uses ActiveJob. Ensure you have a background processor (Sidekiq, etc.) running.

</essential_principles>

<intake>

**What would you like to do?**

1. Set up noticed in a new project
2. Create a new notifier
3. Add a delivery method to existing notifier
4. Debug notification issues
5. Write tests for notifications
6. Something else

**If creating a notifier, which delivery methods do you need?**

**Available delivery methods:**
- **Email** - ActionMailer integration
- **ActionCable** - Real-time WebSocket
- **Slack** - Slack webhooks (individual or bulk)
- **Microsoft Teams** - Teams webhooks
- **Twilio** - SMS/WhatsApp
- **Vonage** - SMS
- **Apple Push (APNs)** - iOS push notifications
- **FCM** - Firebase Cloud Messaging (Android)
- **Discord** - Discord webhooks (bulk)
- **Bluesky** - Bluesky posts (bulk)
- **Webhook** - Generic HTTP webhooks (bulk)
- **Database only** - In-app notification center, no external delivery

**Then read the matching workflow from `workflows/` and follow it.**

</intake>

<routing>

| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "new project" | `workflows/setup-noticed.md` |
| 2, "create", "new notifier", "notification" | `workflows/create-notifier.md` |
| 3, "add", "delivery method", "channel" | `workflows/add-delivery-method.md` |
| 4, "debug", "not working", "fix", "issue" | `workflows/debug-notifications.md` |
| 5, "test", "tests", "testing" | `workflows/write-tests.md` |
| Unsupported delivery method requested | `workflows/create-custom-delivery-method.md` |

</routing>

<verification_loop>

## After Every Change

```bash
# 1. Does it build?
bin/rails runner "NewCommentNotifier"

# 2. Do tests pass?
bin/rails test test/notifiers/

# 3. Check job queue
bin/rails runner "puts Sidekiq::Queue.new.size"
```

Report to the user:
- "Notifier loads: ✓"
- "Tests: X pass, Y fail"
- "Ready for you to test delivery"

</verification_loop>

<reference_index>

## Domain Knowledge

All in `references/`:

**Delivery:** delivery-methods.md
**Patterns:** notifier-patterns.md
**Config:** configuration.md
**Database:** database-integration.md
**Mistakes:** anti-patterns.md

</reference_index>

<workflows_index>

## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| setup-noticed.md | Install and configure noticed |
| create-notifier.md | Create new notifier with delivery methods |
| add-delivery-method.md | Add delivery channel to existing notifier |
| create-custom-delivery-method.md | Build custom delivery for unsupported services |
| debug-notifications.md | Troubleshoot delivery issues |
| write-tests.md | Test notifications |

</workflows_index>
