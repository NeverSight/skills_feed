---
name: velt-comments-best-practices
description: Velt Comments implementation patterns and best practices for React, Next.js, and web applications. Use when adding collaborative commenting features, comment modes (Freestyle, Popover, Stream, Text, Page), rich text editor comments (TipTap, SlateJS, Lexical), media player comments, or chart comments.
license: MIT
metadata:
  author: velt
  version: "1.0.0"
---

# Velt Comments Best Practices

Comprehensive implementation guide for Velt's collaborative comments feature in React and Next.js applications. Contains 33 rules across 9 categories, prioritized by impact to guide automated code generation and integration patterns.

## When to Apply

Reference these guidelines when:
- Adding collaborative commenting to a React/Next.js application
- Implementing any Velt comment mode (Freestyle, Popover, Stream, Text, Page, Inline)
- Integrating comments with rich text editors (TipTap, SlateJS, Lexical)
- Adding comments to media players (Video, Lottie animations)
- Adding comments to charts (Highcharts, ChartJS, Nivo)
- Building custom comment interfaces with standalone components

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core Setup | CRITICAL | `core-` |
| 2 | Comment Modes | HIGH | `mode-` |
| 3 | Standalone Components | MEDIUM-HIGH | `standalone-` |
| 4 | Comment Surfaces | MEDIUM-HIGH | `surface-` |
| 5 | UI Customization | MEDIUM | `ui-` |
| 6 | Data Model | MEDIUM | `data-` |
| 7 | Debugging & Testing | LOW-MEDIUM | `debug-` |
| 8 | Moderation & Permissions | LOW | `permissions-` |
| 9 | Attachments & Reactions | LOW | `attach-` |

## Quick Reference

### 1. Core Setup (CRITICAL)

- `core-provider-setup` - Initialize VeltProvider with API key
- `core-authentication` - Authenticate users before using comments
- `core-document-setup` - Configure document context for comments

### 2. Comment Modes (HIGH)

- `mode-freestyle` - Pin comments anywhere on page
- `mode-popover` - Google Sheets-style cell comments
- `mode-stream` - Google Docs-style sidebar stream
- `mode-text` - Text highlight comments
- `mode-page` - Page-level comments via sidebar
- `mode-inline-comments` - Traditional inline thread style
- `mode-tiptap` - TipTap editor integration
- `mode-slatejs` - SlateJS editor integration
- `mode-lexical` - Lexical editor integration
- `mode-canvas` - Canvas/drawing comments
- `mode-lottie-player` - Lottie animation frame comments
- `mode-video-player-prebuilt` - Velt prebuilt video player
- `mode-video-player-custom` - Custom video player integration
- `mode-chart-highcharts` - Highcharts data point comments
- `mode-chart-chartjs` - ChartJS data point comments
- `mode-chart-nivo` - Nivo charts data point comments
- `mode-chart-custom` - Custom chart integration

### 3. Standalone Components (MEDIUM-HIGH)

- `standalone-comment-pin` - Manual comment pin positioning
- `standalone-comment-thread` - Render comment threads
- `standalone-comment-composer` - Add comments programmatically

### 4. Comment Surfaces (MEDIUM-HIGH)

- `surface-sidebar` - Comments sidebar component
- `surface-sidebar-button` - Toggle sidebar button

### 5. UI Customization (MEDIUM)

- `ui-comment-dialog` - Customize comment dialog
- `ui-comment-bubble` - Customize comment bubble
- `ui-wireframes` - Use wireframe components

### 6. Data Model (MEDIUM)

- `data-context-metadata` - Add custom metadata
- `data-comment-annotations` - Work with annotations
- `data-filtering-grouping` - Filter and group comments

### 7. Debugging & Testing (LOW-MEDIUM)

- `debug-common-issues` - Common issues and solutions
- `debug-verification` - Verification checklist

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/shared/core/core-provider-setup.md
rules/shared/mode/mode-popover.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Source pointers to official documentation

## Compiled Documents

- `AGENTS.md` — Compressed index of all rules with file paths (start here)
- `AGENTS.full.md` — Full verbose guide with all rules expanded inline
