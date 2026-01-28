---
name: hotwire-patterns
description: Stimulus and Turbo patterns for Rails frontend development. Automatically invoked when working with Hotwire, Stimulus controllers, Turbo frames/streams, progressive enhancement, or modern Rails JavaScript. Triggers on "Stimulus", "Turbo", "Hotwire", "turbo_frame", "turbo_stream", "Stimulus controller", "data-controller", "data-action", "progressive enhancement", "SPA-like".
allowed-tools: Read, Grep, Glob
---

# Hotwire Patterns for Rails

Patterns for building modern, interactive Rails applications with Stimulus and Turbo.

## When This Skill Applies

- Creating Stimulus controllers for interactive behaviors
- Implementing Turbo frames for partial page updates
- Using Turbo streams for real-time updates
- Progressive enhancement patterns
- Form enhancements and validations
- Real-time features with ActionCable

## Core Philosophy

**HTML over the wire**: Hotwire sends HTML from the server, not JSON. JavaScript enhances server-rendered HTML rather than replacing it.

- **Progressive enhancement**: Works without JavaScript, enhanced with it
- **Server-first**: Business logic stays on the server
- **Minimal JavaScript**: Just enough JS to make HTML interactive

## Quick Reference

| Component | Purpose | Use When |
|-----------|---------|----------|
| Stimulus | JavaScript behaviors | Adding interactivity to HTML |
| Turbo Drive | SPA navigation | Default for all links/forms |
| Turbo Frames | Partial updates | Update part of page |
| Turbo Streams | Multi-target updates | Update multiple elements |

## Detailed Documentation

- [stimulus.md](stimulus.md) - Stimulus controller patterns
- [turbo.md](turbo.md) - Turbo frames and streams patterns

## Common Patterns

### Stimulus Controller Basics

```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static classes = ["hidden"]
  static values = { open: { type: Boolean, default: false } }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    this.contentTarget.classList.toggle(this.hiddenClass, !this.openValue)
  }
}
```

```erb
<div data-controller="toggle" data-toggle-hidden-class="hidden">
  <button data-action="toggle#toggle">Toggle</button>
  <div data-toggle-target="content">Content here</div>
</div>
```

### Turbo Frame Basics

```erb
<turbo-frame id="messages">
  <%= render @messages %>
</turbo-frame>

<%= link_to "Load more", messages_path(page: 2), data: { turbo_frame: "messages" } %>
```

### Turbo Stream Basics

```erb
<%# app/views/messages/create.turbo_stream.erb %>
<%= turbo_stream.prepend "messages", @message %>
<%= turbo_stream.update "message_count", Message.count %>
```

## Integration Tips

### Rails View Helpers

```erb
<%# Stimulus data attributes %>
<%= tag.div data: { controller: "dropdown", dropdown_open_value: false } do %>
  ...
<% end %>

<%# Turbo frame %>
<%= turbo_frame_tag "user_#{user.id}" do %>
  <%= render user %>
<% end %>
```

### Prevent Turbo on Specific Links

```erb
<%= link_to "Download", file_path, data: { turbo: false } %>
<%= link_to "External", "https://example.com", data: { turbo_frame: "_top" } %>
```
