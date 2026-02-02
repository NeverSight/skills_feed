---
name: ant-design-x
description: Ant Design X 2.x guidance for AI chat/copilot UI, streaming message state, tool rendering, and X Markdown on top of antd. Use when building AI conversations, agent tools UI, or streaming LLM experiences with @ant-design/x.
---

# Ant Design X

## S - Scope
- Target: @ant-design/x@^2 with antd@^6 and @ant-design/cssinjs.
- Cover: message/tool data models, streaming state, chat layouts, tool result rendering.
- Avoid: generic antd component questions without AI flows (use ant-design skill).
- Avoid: admin routing/layout and CRUD scaffolding (use ant-design-pro skill).

### `Reference` index (Chinese)
Topic | Description | `Reference`
--- | --- | ---
Core v2 | Version scope and baseline guidance | `references/x-v2.md`
Components advanced | Message/tool component patterns | `references/x-components-advanced.md`
SDK advanced | Streaming integration and state model | `references/x-sdk-advanced.md`
Markdown advanced | X Markdown extensions and rendering | `references/x-markdown-advanced.md`

## P - Process
1. Identify AI product context: chat/copilot/agent, message types, output formats, runtime.
2. Model messages and tools as serializable data; keep JSX as pure views.
3. Define streaming state: messages array, streamingMessageId, isGenerating, stop/retry actions.
4. Map tool outputs to dedicated visual blocks; keep them expandable and inspectable.
5. Optimize long sessions: virtualization, throttled streaming updates, stable keys.
6. Use the `Reference` index when the scenario is beyond the common path.

## O - Output
- Provide message schema, tool schema, and minimal state model.
- Recommend X components and layout patterns with short rationale.
- Call out streaming/perf risks and mitigations (jank, scroll jumps, re-renders).
- Include error/stop/retry UX requirements and acceptance checks.
