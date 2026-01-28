---
name: svelte-ui-design
description: ALWAYS use this skill for ANY Svelte component styling, design, or UI work. Svelte 5 UI design system using Tailwind CSS 4, Skeleton Labs design tokens/presets/Tailwind Components, and Bits UI headless components. Covers class composition, color systems, interactive components, forms, overlays, and all visual design.
---

# Svelte UI Design System

Svelte 5 + Tailwind CSS 4 + Skeleton Labs + Bits UI 통합 디자인 시스템

## When to Use This Skill

**자동 활성화:**
- ANY Svelte component creation or modification
- ALL styling, design, and UI work in Svelte projects
- Component props, layouts, colors, spacing, typography
- Forms, buttons, cards, chips, badges, tables, dialogs, overlays
- Animations, transitions, hover effects, responsive design
- Dark mode, themes, conditional styling, dynamic values

## Core Principles

1. **컴포넌트**: Bits UI headless 컴포넌트만 사용
2. **스타일링**:
   - Skeleton Labs 토큰/프리셋 (preset-filled, preset-tonal 등)
   - Skeleton Labs Tailwind Components (card, chip, badge, placeholder 등 - 클래스 조합)
   - Tailwind CSS 유틸리티
3. **Skeleton 색상/프리셋**: 반드시 공식 문서 참고, 직접 shade 조합 만들지 말 것
4. **Progressive disclosure**: 필요한 문서만 참조
5. **1-level deep 참조**: SKILL.md → reference 파일만

## Available References

### Get Started
- [introduction.md](reference/introduction.md) - Skeleton 개요
- [installation.md](reference/installation.md) - 프레임워크별 설치
- [fundamentals.md](reference/fundamentals.md) - 핵심 개념
- [core-api.md](reference/core-api.md) - @base, @theme, @utility, @variant

### Design System
- [colors-design.md](reference/colors-design.md) - **색상 팔레트 및 Color Pairings** (필수 참고)
- [presets-design.md](reference/presets-design.md) - **프리셋 시스템** (필수 참고)
- [themes.md](reference/themes.md) - 테마 시스템
- [typography-design.md](reference/typography-design.md) - 타이포그래피
- [spacing-design.md](reference/spacing-design.md) - 간격 시스템
- [iconography.md](reference/iconography.md) - 아이콘

### Tailwind CSS 4
- [tailwind-utilities.md](reference/tailwind-utilities.md) - Tailwind CSS 4 유틸리티
- [tailwind-colors.md](reference/tailwind-colors.md) - OKLCH 색상
- [tailwind-theme.md](reference/tailwind-theme.md) - CSS @theme 설정
- [tailwind-variants.md](reference/tailwind-variants.md) - 상태 variant

### Svelte 5
- [svelte-class-syntax.md](reference/svelte-class-syntax.md) - 클래스 조합

### Tailwind Components (Skeleton Labs 클래스 조합)
클래스로 디자인을 뭉쳐놓은 기본 요소. card, chip, badge, placeholder 등.
- [badges.md](reference/badges.md), [buttons.md](reference/buttons.md), [cards.md](reference/cards.md), [chips.md](reference/chips.md)
- [dividers.md](reference/dividers.md), [forms.md](reference/forms.md), [placeholders.md](reference/placeholders.md), [tables.md](reference/tables.md)

### Bits UI - Headless Components
- [bits-ui-complete.md](reference/bits-ui-complete.md) - **Bits UI 42개 headless 컴포넌트 완전 문서**

### Guides
- [dark-mode.md](reference/dark-mode.md) - 다크 모드
- [layouts.md](reference/layouts.md) - 레이아웃
- [cookbook.md](reference/cookbook.md) - 레시피

### Migration
- [migrate-v2-to-v3.md](reference/migrate-v2-to-v3.md) - v2 → v3
- [migrate-v3-to-v4.md](reference/migrate-v3-to-v4.md) - v3 → v4

## Bits UI - Headless Components (42개)

완전히 커스터마이징 가능한 unstyled 컴포넌트. Skeleton Labs 토큰/프리셋으로 스타일링.

**주요 카테고리:**
- Layout: Accordion, Collapsible, Tabs, Separator
- Overlays: Dialog, Popover, Tooltip, Context Menu, Drawer
- Forms: Checkbox, Radio Group, Switch, Slider, Select, Combobox
- Date/Time: Calendar, Date Picker, Date Range Picker, Time Field
- Navigation: Dropdown Menu, Menubar, Navigation Menu, Pagination
- Display: Avatar, Progress, Meter, Badge
- Interactive: Button, Toggle, Link Preview

## Quick Reference

### Skeleton Labs 중요 규칙

**Color Pairings** (반드시 [colors-design.md](reference/colors-design.md) 참고):
- 패턴: `{property}-{color}-{lightShade}-{darkShade}`
- 허용 조합: 50-950, 100-900, 200-800, 300-700, 400-600, **500**, 600-400, 700-300, 800-200, 900-100, 950-50
- 규칙: **두 shade의 합이 1000** 또는 **500 단독**
- 예: `bg-surface-50-950`, `text-primary-200-800`

**Presets** (반드시 [presets-design.md](reference/presets-design.md) 참고):
- Filled: `preset-filled-{color}-{lightShade}-{darkShade}` 또는 `preset-filled-{color}-500`
- Tonal: `preset-tonal-{color}`
- Outlined: `preset-outlined-{color}-{lightShade}-{darkShade}`

### Svelte 5 Class Composition

```svelte
<!-- Array form -->
<div class={['base', condition && 'extra']}>

<!-- Object form -->
<div class={{ 'active': isActive, 'disabled': !enabled }}>

<!-- Style directive for dynamic values -->
<div
  class="bg-(--brand-color)"
  style:--brand-color={dynamicValue}>
```

### Usage Pattern

```svelte
<script lang="ts">
  import { Dialog } from "bits-ui";
</script>

<Dialog.Root>
  <Dialog.Trigger class="btn preset-filled-primary-500">
    Open
  </Dialog.Trigger>
  <Dialog.Content class={[
    'card preset-filled-surface-50-950',
    'p-8 rounded-xl shadow-xl'
  ]}>
    <Dialog.Title class="h3 text-primary-600-400">
      Title
    </Dialog.Title>
  </Dialog.Content>
</Dialog.Root>
```

## Best Practices

1. **컴포넌트**: Bits UI headless 컴포넌트만 사용
2. **스타일링**: Skeleton Labs 토큰/프리셋 + Tailwind Components (card, chip, badge 등) + Tailwind 유틸리티
3. **Skeleton 색상/프리셋**: 반드시 공식 문서([colors-design.md](reference/colors-design.md), [presets-design.md](reference/presets-design.md))에서 확인
4. **Class 조합 순서**: Tailwind Components → 프리셋 → 레이아웃 → 간격 → 조건부 → variant
5. **접근성**: WCAG 대비 비율, focus-visible 상태
6. **성능**: Svelte class 배열/객체 사용, Skeleton 프리셋 활용
7. **일관성**: 동일한 용어 사용, 3인칭 작성
