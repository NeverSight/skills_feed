---
name: frontend-design-system
description: Produce production-grade UI designs using clear design tokens, layout rules, motion guidance, and accessibility checks for consistent, scalable frontend development.
tags: [frontend, design, ui, ux, typography, animation, design-tokens, accessibility]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - Write
  - Read
  - Task
---

# Frontend Design System

프로덕션 수준의 UI 디자인을 위한 스킬입니다. 명확한 디자인 토큰, 레이아웃 규칙, 모션 가이드라인, 접근성 체크를 통해 일관되고 확장 가능한 프론트엔드 개발을 지원합니다.

## When to use this skill

- **프로덕션 품질 UI 필요**: 프롬프트에서 고품질 UI 생성
- **일관된 디자인 언어**: 화면 간 일관된 시각적 언어
- **타이포그래피/레이아웃/모션 가이드**: 체계적인 디자인 시스템

---

## Instructions

### Step 1: Define Design Tokens

```typescript
// design-tokens.ts
export const tokens = {
  // Colors
  colors: {
    primary: {
      50: '#EFF6FF',
      100: '#DBEAFE',
      500: '#3B82F6',
      600: '#2563EB',
      700: '#1D4ED8',
    },
    secondary: {
      500: '#6366F1',
      600: '#4F46E5',
    },
    accent: '#F59E0B',
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    background: {
      primary: '#FFFFFF',
      secondary: '#F9FAFB',
      tertiary: '#F3F4F6',
    },
    text: {
      primary: '#1F2937',
      secondary: '#6B7280',
      tertiary: '#9CA3AF',
      inverse: '#FFFFFF',
    },
  },

  // Typography
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',     // 12px
      sm: '0.875rem',    // 14px
      base: '1rem',      // 16px
      lg: '1.125rem',    // 18px
      xl: '1.25rem',     // 20px
      '2xl': '1.5rem',   // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem',  // 36px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },

  // Spacing (8px base unit)
  spacing: {
    0: '0',
    1: '0.25rem',  // 4px
    2: '0.5rem',   // 8px
    3: '0.75rem',  // 12px
    4: '1rem',     // 16px
    5: '1.25rem',  // 20px
    6: '1.5rem',   // 24px
    8: '2rem',     // 32px
    10: '2.5rem',  // 40px
    12: '3rem',    // 48px
    16: '4rem',    // 64px
  },

  // Border Radius
  borderRadius: {
    none: '0',
    sm: '0.25rem',  // 4px
    md: '0.375rem', // 6px
    lg: '0.5rem',   // 8px
    xl: '0.75rem',  // 12px
    '2xl': '1rem',  // 16px
    full: '9999px',
  },

  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
  },

  // Breakpoints
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
};
```

### Step 2: Define Layout + UX Goals

```yaml
page_spec:
  type: "landing" | "dashboard" | "form" | "blog" | "e-commerce"

  hierarchy:
    primary_action: [주요 CTA]
    secondary_actions: [부가 액션들]
    information_architecture:
      - section: hero
        priority: 1
      - section: features
        priority: 2
      - section: social_proof
        priority: 3
      - section: cta
        priority: 4

  responsive:
    mobile_first: true
    breakpoints:
      - mobile: "< 640px"
      - tablet: "640px - 1024px"
      - desktop: "> 1024px"
    stack_behavior: "vertical on mobile, horizontal on desktop"
```

### Step 3: Generate UI Output

**섹션별 컴포넌트 구조**:

```tsx
// Hero Section
<section className="hero">
  <div className="container">
    <div className="hero-content">
      <Badge>New Release</Badge>
      <Heading level={1}>
        Main Headline Here
      </Heading>
      <Paragraph size="lg">
        Supporting copy that explains the value proposition
        in 1-2 sentences.
      </Paragraph>
      <div className="cta-group">
        <Button variant="primary" size="lg">
          Primary CTA
        </Button>
        <Button variant="secondary" size="lg">
          Secondary CTA
        </Button>
      </div>
    </div>
    <div className="hero-visual">
      <Image src="hero-image.png" alt="Product screenshot" />
    </div>
  </div>
</section>
```

**모션/인터랙션 노트**:

```css
/* Motion Guidelines */
:root {
  /* Duration */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  /* Easing */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
}

/* Hover States */
.button {
  transition: all var(--duration-fast) var(--ease-in-out);
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Page Transitions */
.page-enter {
  opacity: 0;
  transform: translateY(10px);
}
.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all var(--duration-normal) var(--ease-out);
}
```

### Step 4: Validate Accessibility

```markdown
## Accessibility Checklist

### Color Contrast (WCAG 2.1 AA)
- [ ] Text/background: 4.5:1 minimum (normal text)
- [ ] Text/background: 3:1 minimum (large text)
- [ ] UI components: 3:1 minimum

### Keyboard Navigation
- [ ] All interactive elements focusable
- [ ] Focus order logical (left→right, top→bottom)
- [ ] Focus indicator visible
- [ ] Skip links present

### Screen Reader
- [ ] Semantic HTML used
- [ ] Images have alt text
- [ ] Form labels associated
- [ ] ARIA labels where needed

### Text & Readability
- [ ] Minimum 16px body text
- [ ] Line height ≥ 1.5
- [ ] Paragraph width < 80 characters
- [ ] No text in images
```

### Step 5: Handoff

```markdown
## Design Handoff Package

### Component Breakdown
| Component | Props | Variants |
|-----------|-------|----------|
| Button | size, variant, disabled | primary, secondary, ghost |
| Input | size, error, placeholder | default, error, success |
| Card | padding, shadow | elevated, flat, outlined |

### CSS/Token Summary
- Colors: [link to color palette]
- Typography: [link to type scale]
- Spacing: 8px base unit
- Breakpoints: 640/768/1024/1280px

### Files
- Figma: [link]
- Tokens: design-tokens.ts
- Components: /src/components/
```

---

## Examples

### Example 1: SaaS Landing Page

**Prompt**:
```
Design a SaaS landing page with modern typography,
soft gradients, and subtle motion.
Include hero, features, pricing, and CTA.
```

**Expected output**:
- Section layout with visual direction
- Typography scale (H1: 48px → Body: 16px)
- Color palette with gradient definitions
- Motion/interaction specifications
- Component list with props

### Example 2: Admin Dashboard

**Prompt**:
```
Create a clean admin dashboard with data cards,
filters, and tables. Focus on clarity and fast scanning.
```

**Expected output**:
- Grid layout (12-column)
- Component breakdown (cards, tables, filters)
- Visual hierarchy documentation
- Responsive behavior specification

### Example 3: Mobile-First Form

**Prompt**:
```
Design a multi-step form optimized for mobile.
Include progress indicator, validation states,
and success confirmation.
```

**Expected output**:
- Step-by-step flow diagram
- Form field specifications
- Error/success state designs
- Touch-friendly sizing (min 44px targets)

---

## Best practices

1. **Start with content hierarchy**: UI follows content priority
2. **Consistent spacing scale**: 8px 기반 시스템, ad-hoc 간격 금지
3. **Motion with intent**: 의미 있는 전환만 애니메이션
4. **Test on mobile**: 레이아웃 무결성 확인
5. **Accessibility first**: 디자인 단계에서 접근성 고려

---

## Common pitfalls

- **효과와 그라데이션 과용**: 단순함 유지
- **일관성 없는 타이포그래피 스케일**: 정의된 스케일 사용
- **접근성 고려 누락**: 색상 대비, 키보드 네비게이션

---

## Troubleshooting

### Issue: UI feels generic
**Cause**: 시각적 방향이나 토큰 없음
**Solution**: 스타일 레퍼런스와 팔레트 제공

### Issue: Layout breaks on mobile
**Cause**: 반응형 그리드 규칙 없음
**Solution**: 브레이크포인트와 스태킹 동작 정의

### Issue: Inconsistent components
**Cause**: 토큰 미사용
**Solution**: 모든 값을 토큰에서 참조

---

## Output format

```markdown
## Design System Report

### Tokens Applied
- **Colors**: [primary, secondary, accent]
- **Typography**: [font-family, scale]
- **Spacing**: [base unit, scale]
- **Shadows**: [levels]

### Section Layout
| Section | Grid | Components |
|---------|------|------------|
| Hero | 2-col | Badge, Heading, CTA |
| Features | 3-col | Card, Icon |
| Pricing | 3-col | PricingCard |
| CTA | 1-col | Button |

### Component List
- [ ] Button (primary, secondary, ghost)
- [ ] Card (elevated, flat)
- [ ] Input (default, error)
- [ ] Badge
- [ ] Icon

### Accessibility Audit
- [x] Contrast ratios pass
- [x] Focus indicators visible
- [x] Semantic HTML
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 시각적 방향, 섹션 완전성
- **Round 2 (Analyst)**: 접근성, 계층 구조 리뷰
- **Round 3 (Executor)**: 핸드오프 체크리스트 검증

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 토큰 정의, 컴포넌트 설계 |
| Gemini | 접근성 분석, 레퍼런스 리서치 |
| Codex | CSS/컴포넌트 코드 생성 |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [ui-component-patterns](../ui-component-patterns/SKILL.md)
- [responsive-design](../responsive-design/SKILL.md)
- [web-accessibility](../web-accessibility/SKILL.md)
- [image-generation](../../creative-media/image-generation/SKILL.md)

### Tags
`#frontend` `#design` `#ui` `#ux` `#typography` `#animation` `#design-tokens` `#accessibility`
