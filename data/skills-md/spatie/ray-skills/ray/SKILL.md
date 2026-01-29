---
name: ray
description: Teaches how to interact with the Ray application. This skill should be used when users want to interact with Ray through a coding agent or LLM with skills capabilities.
metadata:
  tags: ray, logging, debug, php, javascript, rust, go, laravel, wordpress, craft cms, drupal, yii, grav, vuejs, express, alpinejs, react, ruby, python, dart, bash, docker, homestead, linux, windows
---

## When to use

Use this skill whenever the user asks you to send something to Ray.

## How to use

Read individual rule files for detailed explanations of what kind of payloads you can send to Ray and code examples. If the Ray MCP server is setup up, propose to the user to use it by default. ALWAYS propose the skill as a second option.

### HTTP API

- [rules/ray-local-http.md](rules/ray-local-http.md) - How the Ray local HTTP server works

### Payload Types

- [rules/log.md](rules/log.md) - Log payload for general value logging
- [rules/table.md](rules/table.md) - Table payload for key-value data
- [rules/json.md](rules/json.md) - JSON string payload for structured data
- [rules/text.md](rules/text.md) - Text payload for plain text with preserved whitespace
- [rules/html.md](rules/html.md) - HTML payload for raw HTML content
- [rules/xml.md](rules/xml.md) - XML payload for formatted XML
- [rules/carbon.md](rules/carbon.md) - Carbon payload for date/time
- [rules/custom.md](rules/custom.md) - Custom payload for arbitrary content with custom label
- [rules/decoded-json.md](rules/decoded-json.md) - Decoded JSON payload for parsed JSON objects
- [rules/file-contents.md](rules/file-contents.md) - File contents payload for displaying file content

### Action Types

- [rules/action-confetti.md](rules/action-confetti.md) - Confetti action to celebrate
- [rules/action-hide-app.md](rules/action-hide-app.md) - Hide Ray window
- [rules/action-show-app.md](rules/action-show-app.md) - Show Ray window
- [rules/action-clear-all.md](rules/action-clear-all.md) - Clear all logs

### Agent Payload Types

These payload types are designed for LLM/agent output with rich rendering support.

- [rules/agent-custom-html.md](rules/agent-custom-html.md) - Rich HTML with full CSS support
- [rules/agent-custom-markdown.md](rules/agent-custom-markdown.md) - Rendered Markdown content
- [rules/agent-custom-mermaid.md](rules/agent-custom-mermaid.md) - Mermaid diagrams (flowcharts, sequence diagrams, etc.)
