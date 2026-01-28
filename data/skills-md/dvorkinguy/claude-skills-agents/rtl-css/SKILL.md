---
name: rtl-css
description: RTL (Right-to-Left) CSS for Hebrew and Arabic. Use when building UI that needs RTL support, fixing RTL layout issues, or auditing CSS for RTL compliance.
---

# RTL CSS with Logical Properties

## The Golden Rule
NEVER use physical properties. ALWAYS use logical properties.

## Property Mapping

| Physical (❌) | Logical (✅) | Tailwind |
|--------------|-------------|----------|
| padding-left | padding-inline-start | ps-* |
| padding-right | padding-inline-end | pe-* |
| margin-left | margin-inline-start | ms-* |
| margin-right | margin-inline-end | me-* |
| left | inset-inline-start | start-* |
| right | inset-inline-end | end-* |
| text-align: left | text-align: start | text-start |
| text-align: right | text-align: end | text-end |
| border-left | border-inline-start | border-s-* |
| border-right | border-inline-end | border-e-* |

## Tailwind Examples

```tsx
// ❌ WRONG - Breaks in RTL
<div className="pl-4 pr-2 ml-auto text-left border-l-2">

// ✅ CORRECT - Works everywhere
<div className="ps-4 pe-2 ms-auto text-start border-s-2">
```

## Next.js Layout with RTL

```typescript
// app/[locale]/layout.tsx
import { isRtlLang } from 'rtl-detect';

export default function LocaleLayout({
  children,
  params: { locale },
}) {
  const dir = isRtlLang(locale) ? 'rtl' : 'ltr';

  return (
    <html lang={locale} dir={dir}>
      <body>{children}</body>
    </html>
  );
}
```

## Icon Flipping

```tsx
// Directional icons need flip
<ChevronRight className="rtl:rotate-180" />
<ArrowRight className="rtl:rotate-180" />
<ArrowLeft className="rtl:rotate-180" />

// Universal icons - don't flip
<Check /> <X /> <Search /> <Menu /> <Home />
```

## Audit Command

Run `scripts/audit_rtl.sh` to find violations in your codebase.

## Checklist
- [ ] All padding uses ps-/pe-
- [ ] All margins uses ms-/me-
- [ ] Positioning uses start-/end-
- [ ] Text uses text-start/text-end
- [ ] Directional icons have rtl:rotate-180
- [ ] Layout has dir attribute
