---
name: ant-design-pro
description: Ant Design Pro 5.x guidance for enterprise admin apps, including layouts, routing, access control, and ProComponents (ProTable/ProForm). Use when building or reviewing Pro-based CRUD systems, route/menu design, or permission models on top of antd.
---

# Ant Design Pro

## S - Scope
- Target: ant-design-pro@^5 and @ant-design/pro-components on top of antd@^6.
- Cover: layout shell, routing/menu, access control, CRUD standardization with ProTable/ProForm.
- Avoid: low-level antd component styling and token details (use ant-design skill).
- Avoid: AI chat/copilot UI (use ant-design-x skill).

### `Reference` index (Chinese)
Topic | Description | `Reference`
--- | --- | ---
Core v5 | Version scope and baseline guidance | `references/pro-v5.md`
Layout advanced | Layouts, menus, access, multi-layout patterns | `references/pro-layout-advanced.md`
ProTable advanced | Query/table coupling, request patterns, perf | `references/protable-advanced.md`
ProForm advanced | Step forms, dynamic fields, table linkage | `references/proform-advanced.md`

## P - Process
1. Identify business context: roles/RBAC, page types, data sources, multi-tenant needs.
2. Define structure: layouts/, pages/, services/, access.ts; keep routes as the menu source of truth.
3. Design routing and permissions: page-level access first; UI hides, backend enforces.
4. Standardize CRUD: ProTable for list/search/action patterns; ProForm for form state/validation.
5. Centralize data access: keep network calls in services; pages adapt data shape only.
6. Use the `Reference` index when the scenario is beyond the common path.

## O - Output
- Provide route/layout plan and access model (roles, rules, page gates).
- Provide ProTable/ProForm schemas or column/field definitions as the source of truth.
- Call out anti-patterns (ad-hoc layouts, in-page fetch, inconsistent tables) and fixes.
- Include testing checkpoints for permissions, menu visibility, and CRUD workflows.
