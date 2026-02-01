---
name: css-tokens
description: Design tokens system using CSS Custom Properties for consistent styling. Use for creating color palettes, spacing scales, typography systems, and theming (dark/light mode). Triggers on requests for design tokens, CSS variables, theming, color systems, spacing scales, or consistent styling.
---

# CSS Design Tokens

## Token Structure

```css
/* tokens.css */
:root {
  /* Colors - Semantic */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Colors - Neutral */
  --color-background: #ffffff;
  --color-surface: #f8fafc;
  --color-border: #e2e8f0;
  --color-text: #1e293b;
  --color-text-muted: #64748b;
  
  /* Spacing Scale (4px base) */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Borders */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  
  /* Transitions */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Dark Mode

```css
[data-theme="dark"] {
  --color-primary: #3b82f6;
  --color-primary-hover: #60a5fa;
  
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-border: #334155;
  --color-text: #f1f5f9;
  --color-text-muted: #94a3b8;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
}
```

## Usage in Components

```tsx
// Button.tsx
const buttonStyles: CSSProperties = {
  backgroundColor: 'var(--color-primary)',
  color: 'var(--color-background)',
  padding: 'var(--space-2) var(--space-4)',
  borderRadius: 'var(--radius-md)',
  fontSize: 'var(--text-sm)',
  fontWeight: 'var(--font-medium)',
  transition: `background-color var(--duration-fast) var(--ease-default)`,
};
```

```css
/* Button.css */
.btn {
  background-color: var(--color-primary);
  color: var(--color-background);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  transition: background-color var(--duration-fast) var(--ease-default);
}

.btn:hover {
  background-color: var(--color-primary-hover);
}
```

## Token Naming Convention

```
--{category}-{property}-{variant}

Examples:
--color-primary
--color-primary-hover
--space-4
--text-lg
--radius-md
--shadow-lg
```

## Component Token Mapping

| Component | Tokens |
|-----------|--------|
| Button | `--color-primary`, `--space-2/4`, `--radius-md`, `--text-sm` |
| Input | `--color-border`, `--space-2/3`, `--radius-md`, `--text-base` |
| Card | `--color-surface`, `--space-4`, `--radius-lg`, `--shadow-md` |
| Badge | `--color-*`, `--space-1/2`, `--radius-full`, `--text-xs` |

## Theme Provider Pattern

```tsx
// ThemeProvider.tsx
type Theme = 'light' | 'dark' | 'system';

export const ThemeProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('system');
  
  useEffect(() => {
    const root = document.documentElement;
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const resolved = theme === 'system' ? (systemDark ? 'dark' : 'light') : theme;
    root.setAttribute('data-theme', resolved);
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

## Best Practices

1. Use semantic names (`--color-primary`) over literal (`--color-blue`)
2. Define scales with consistent ratios (4px spacing, modular type)
3. Keep token count minimal but comprehensive
4. Document token purpose in comments
5. Test all tokens in both light/dark modes
