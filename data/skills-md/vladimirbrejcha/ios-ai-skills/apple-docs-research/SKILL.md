---
name: apple-docs-research
description: "Use when researching or implementing anything related to Apple platforms (iOS, iPadOS, macOS, watchOS, tvOS, visionOS), Swift/Objective-C APIs, Apple frameworks, WWDC sessions, or Apple Developer Documentation. Triggers include: \"find Apple's docs\", \"latest API guidance\", \"WWDC session\", \"platform availability\", \"SwiftUI/UIKit/AppKit/Combine/AVFoundation/etc.\", or any Apple SDK coding question where authoritative docs are needed. Always use the apple-docs MCP tools for discovery and citations instead of general web search."
---

# Apple Docs Research

## Overview

Use this skill to answer Apple platform coding and research questions by querying the Apple Developer Documentation and WWDC catalog via the apple-docs MCP tools. This skill replaces general web browsing for Apple-specific sources.

## Workflow

1. **Clarify the target**: Identify platform (iOS/macOS/etc.), framework, API, or WWDC topic. Ask a brief question if the scope is unclear.
2. **Select the right tool path**:
   - **API or framework lookup**: `search_apple_docs` → `get_apple_doc_content` for details.
   - **Framework exploration**: `list_technologies` → `search_framework_symbols`.
   - **Availability / deployment targets**: `get_platform_compatibility`.
   - **Related APIs / alternatives**: `get_related_apis` or `find_similar_apis`.
   - **WWDC sessions**: `list_wwdc_videos` or `search_wwdc_content` → `get_wwdc_video`.
   - **Recent updates / release notes**: `get_documentation_updates`.
3. **Synthesize**: Summarize findings, include version/platform constraints, and provide code or guidance grounded in the retrieved docs.
4. **If no result**: Say what was searched, broaden with adjacent frameworks or WWDC content, then report gaps clearly.

## Output Expectations

- Always use apple-docs MCP tools as the authoritative source for Apple docs and WWDC content.
- Prefer official Apple documentation content and WWDC sessions over third‑party sources.
- When user asks for “latest” or “most recent,” use `get_documentation_updates` or current WWDC year filters rather than assumptions.
*** End Patch} />]
