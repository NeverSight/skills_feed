---
name: action-cable
description: Setup and use ActionCable for real-time features in Rails applications using WebSockets. Use when implementing real-time updates, live notifications, broadcasting changes, or when the user mentions WebSockets, ActionCable, channels, broadcasting, or Turbo Streams over cable.
---

# ActionCable Setup

## Overview

ActionCable integrates WebSockets with Rails to enable real-time features. This guide covers the basic setup in this application.

## Core Components

### 1. Connection (`app/channels/application_cable/connection.rb`)

The connection authenticates and authorizes the WebSocket connection using Devise/Warden.

```ruby
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      if verified_user = env['warden'].user
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end
```

### 2. Channel (`app/channels/application_cable/channel.rb`)

Base channel class for all application channels.

```ruby
module ApplicationCable
  class Channel < ActionCable::Channel::Base
  end
end
```

### 3. JavaScript Setup (`app/javascript/initializers/actioncable.js`)

Initialize ActionCable consumer on the client side.

```javascript
import * as ActionCable from '@rails/actioncable'

ActionCable.logger.enabled = false
```

## Broadcasting Updates

### With Turbo Streams (recommended)

Subscribe to a stream in views:

```slim
= turbo_stream_from record
= turbo_stream_from [record, "channel_name"]
```

Broadcast Turbo Stream updates from controllers or background jobs:

```ruby
# Append content to a target
Turbo::StreamsChannel.broadcast_append_to(
  [record, "channel_name"],
  target: "dom_id",
  partial: "path/to/partial",
  locals: { record: record }
)

# Replace content
Turbo::StreamsChannel.broadcast_replace_to(
  [record, "channel_name"],
  target: "dom_id",
  partial: "path/to/partial",
  locals: { record: record }
)

# Remove element
Turbo::StreamsChannel.broadcast_remove_to(
  [record, "channel_name"],
  target: "dom_id"
)
```

### Example: Organization-scoped notifications

View:
```slim
= turbo_stream_from current_organization, "timers"

#notifications
```

Controller:
```ruby
def start_timer
  # ... create timer logic ...

  Turbo::StreamsChannel.broadcast_append_to(
    [current_organization, "timers"],
    target: "notifications",
    partial: "timers/notification",
    locals: { timer: @timer }
  )
end
```

## Configuration

### Cable URL (`config/cable.yml`)

```yaml
development:
  adapter: async

test:
  adapter: test

production:
  adapter: solid_cable
  connects_to:
    database:
      writing: cable
  polling_interval: 0.1.seconds
  message_retention: 1.day
```

### Routes (`config/routes.rb`)

ActionCable is automatically mounted at `/cable`:

```ruby
Rails.application.routes.draw do
  mount ActionCable.server => '/cable'
end
```

## Debugging

Enable logging in development:

```javascript
// app/javascript/initializers/actioncable.js
ActionCable.logger.enabled = true
```

Check connection status:

```javascript
const subscription = consumer.subscriptions.create("ExampleChannel", {
  connected() {
    console.log("Connected to ExampleChannel")
  }
})

console.log(subscription)
```

## Security Considerations

- Always authenticate connections in `ApplicationCable::Connection`
- Validate params in channel subscriptions
- Use `stream_for` instead of `stream_from` when possible for automatic scoping
- Never trust client-side data without validation
- Consider rate limiting for channels that accept client messages
