---
name: shadcn-studio-inspirations-vue
description: >
  A massive catalog of over 600 Vue SFC component inspirations translated from the
  shadcn-studio React codebase. Use this skill when the user asks for design inspiration,
  building full-page layouts, complex nested components, or you need to see advanced
  examples of how to compose shadcn-vue components together.
---

# Shadcn-Studio Inspirations (Vue 3)

## Overview

This skill contains reference implementations of 600+ complex component patterns
originally designed in React, translated here into Vue 3 `<script setup>` SFC formats.

## How to Use This Skill

When you (the AI) determine that a complex component design or full-page layout belongs to one of the categories below, **follow these steps**:

1. **Load Reference Material**: Open the specific reference markdown file (e.g., `references/data-table.md`) linked below to explore different variations and inspirations for that component. **Crucially, read the `**Best use case:**` description listed under each `### variant.vue` heading** to find the component sample that best matches the user's specific request. If no single variant matches perfectly, draw inspiration and synthesize approaches from multiple relevant samples.
2. **Install Missing Base Components**: If the project uses `shadcn-vue` and lacks the base component, install it first using the CLI:
   ```bash
   npx shadcn-vue@latest add <component-name>
   ```
3. **Handle Dependencies**: Ensure necessary icons are installed (e.g., `npm install lucide-vue-next`).
4. **Implement**: Adapt the chosen reference design to fit the specific requirements of the user's project, ensuring valid Vue 3 `<script setup>` syntax and proper dependency imports (e.g., `@/components/ui/...`).

> **Note**: Do not load all references at once. Use progressive disclosure: only load the specific component markdown files you need for the current task!

## Component Categories Available

- [Accordion](references/accordion.md)
- [Alert](references/alert.md)
- [Avatar](references/avatar.md)
- [Badge](references/badge.md)
- [Blocks](references/blocks.md)
- [Breadcrumb](references/breadcrumb.md)
- [Button](references/button.md)
- [Button Group](references/button-group.md)
- [Calendar](references/calendar.md)
- [Card](references/card.md)
- [Checkbox](references/checkbox.md)
- [Collapsible](references/collapsible.md)
- [Combobox](references/combobox.md)
- [Data Table](references/data-table.md)
- [Date Picker](references/date-picker.md)
- [Dialog](references/dialog.md)
- [Dropdown Menu](references/dropdown-menu.md)
- [Form](references/form.md)
- [Input](references/input.md)
- [Input Mask](references/input-mask.md)
- [Input OTP](references/input-otp.md)
- [Pagination](references/pagination.md)
- [Popover](references/popover.md)
- [Radio Group](references/radio-group.md)
- [Select](references/select.md)
- [Sheet](references/sheet.md)
- [Sonner](references/sonner.md)
- [Switch](references/switch.md)
- [Table](references/table.md)
- [Tabs](references/tabs.md)
- [Textarea](references/textarea.md)
- [Tooltip](references/tooltip.md)
