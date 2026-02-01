---
name: ant-design
description: Ant Design 6.x guidance for selecting components, theming/tokens, css-in-js/SSR setup, and resolving antd component behavior in React/Next.js/Umi/Vite apps. Use when building or reviewing UI with antd, configuring ConfigProvider/theme, or troubleshooting Ant Design UI/SSR/performance issues.
---

# Ant Design

## S - Scope
- Target: antd@^6 with React 18-19 (per official docs).
- Cover: core components, theming/tokens, css-in-js, SSR, a11y, and performance patterns.
- Avoid: Pro routing/layout and ProComponents (use ant-design-pro skill).
- Avoid: AI chat/copilot UI (use ant-design-x skill).

### `Reference` index (Chinese)
Topic | Description | `Reference`
--- | --- | ---
Core v6 | Version scope, migration notes, theming/SSR overview | `references/antd-v6.md`
Legacy v5 | Existing v5 projects and migration guardrails | `references/antd-v5.md`
Form advanced | Dynamic forms, dependencies, validation perf | `references/form-advanced.md`
Table advanced | Sorting/filtering/virtualization patterns | `references/table-advanced.md`
Upload advanced | Controlled upload, customRequest, edge cases | `references/upload-advanced.md`
Select advanced | Remote search, tags, rendering and a11y | `references/select-advanced.md`
Tree advanced | Async load, checkStrictly, virtual | `references/tree-advanced.md`

## P - Process
1. Identify app context: product type, rendering mode (CSR/SSR/streaming), theming depth, data scale.
2. Set providers: single ConfigProvider at app root; add StyleProvider when SSR or strict style ordering is required.
3. Choose component patterns: Form as source of truth; stable rowKey for Table; destroyOnClose for stateful Modal/Drawer.
4. Plan theming: global tokens -> component tokens -> alias tokens; avoid global .ant-* overrides.
5. When complexity appears, open the matching `Reference` file from the index above.
6. Validate a11y/perf: keyboard/focus, virtualization, memoized columns, throttled updates.

## O - Output
- Recommend components and layout primitives with short rationale.
- Provide token/theming strategy and the minimal provider setup needed.
- Call out SSR, perf, and a11y risks plus concrete mitigations.
- Include a short checklist for acceptance or regression testing.
