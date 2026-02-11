---
name: theme-system
description: CSS custom properties theme architecture for 4 themes (studio, earth, athlete, gradient) with data-theme attribute switching and theme-aware components. Use when implementing theme switching, defining color schemes, or creating theme-responsive UI elements.
---

# Theme System

## Theme Definitions

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Default: Studio theme */
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --radius: 0.5rem;
  }

  /* Theme: Earth - Soft organic warmth */
  [data-theme="earth"] {
    --background: 40 33% 98%;
    --foreground: 30 10% 15%;
    --card: 40 30% 97%;
    --card-foreground: 30 10% 15%;
    --primary: 30 30% 35%;
    --primary-foreground: 40 30% 98%;
    --secondary: 35 25% 92%;
    --secondary-foreground: 30 20% 25%;
    --muted: 35 20% 93%;
    --muted-foreground: 30 10% 40%;
    --accent: 35 30% 88%;
    --accent-foreground: 30 20% 20%;
    --border: 35 20% 85%;
    --input: 35 20% 88%;
    --ring: 30 30% 35%;
  }

  /* Theme: Studio - Clean minimal */
  [data-theme="studio"] {
    --background: 0 0% 100%;
    --foreground: 0 0% 5%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 5%;
    --primary: 0 0% 8%;
    --primary-foreground: 0 0% 100%;
    --secondary: 0 0% 97%;
    --secondary-foreground: 0 0% 10%;
    --muted: 0 0% 96%;
    --muted-foreground: 0 0% 40%;
    --accent: 0 0% 95%;
    --accent-foreground: 0 0% 10%;
    --border: 0 0% 92%;
    --input: 0 0% 94%;
    --ring: 0 0% 8%;
  }

  /* Theme: Athlete - Bold with purple accent */
  [data-theme="athlete"] {
    --background: 0 0% 99%;
    --foreground: 270 5% 10%;
    --card: 0 0% 100%;
    --card-foreground: 270 5% 10%;
    --primary: 270 60% 50%;
    --primary-foreground: 0 0% 100%;
    --secondary: 270 20% 95%;
    --secondary-foreground: 270 30% 25%;
    --muted: 270 10% 94%;
    --muted-foreground: 270 5% 40%;
    --accent: 270 40% 92%;
    --accent-foreground: 270 40% 30%;
    --border: 270 10% 88%;
    --input: 270 10% 90%;
    --ring: 270 60% 50%;
  }

  /* Theme: Gradient - Soft gradient hero */
  [data-theme="gradient"] {
    --background: 220 30% 99%;
    --foreground: 220 10% 10%;
    --card: 0 0% 100%;
    --card-foreground: 220 10% 10%;
    --primary: 220 80% 55%;
    --primary-foreground: 0 0% 100%;
    --secondary: 280 30% 95%;
    --secondary-foreground: 220 20% 20%;
    --muted: 220 20% 95%;
    --muted-foreground: 220 10% 40%;
    --accent: 280 40% 93%;
    --accent-foreground: 280 30% 25%;
    --border: 220 15% 90%;
    --input: 220 15% 92%;
    --ring: 220 80% 55%;
    
    /* Gradient-specific variables */
    --gradient-start: 220 80% 60%;
    --gradient-end: 280 60% 65%;
  }
}
```

## Theme Configuration

```tsx
// lib/theme.ts
export const themes = ['studio', 'earth', 'athlete', 'gradient'] as const;
export type Theme = (typeof themes)[number];
export const defaultTheme: Theme = 'studio';

export function isValidTheme(theme: string): theme is Theme {
  return themes.includes(theme as Theme);
}
```

## Theme Provider

```tsx
// components/ThemeProvider.tsx
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { type Theme, defaultTheme, isValidTheme } from '@/lib/theme';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>(defaultTheme);

  useEffect(() => {
    // Check URL param first
    const params = new URLSearchParams(window.location.search);
    const urlTheme = params.get('theme');
    
    if (urlTheme && isValidTheme(urlTheme)) {
      setTheme(urlTheme);
      document.documentElement.setAttribute('data-theme', urlTheme);
      return;
    }

    // Check localStorage
    const stored = localStorage.getItem('theme');
    if (stored && isValidTheme(stored)) {
      setTheme(stored);
      document.documentElement.setAttribute('data-theme', stored);
    }
  }, []);

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update URL without reload
    const url = new URL(window.location.href);
    url.searchParams.set('theme', newTheme);
    window.history.replaceState({}, '', url);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme: handleSetTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

## Theme Switcher (Dev Mode)

```tsx
// components/ThemeSwitcher.tsx
'use client';

import { useTheme } from './ThemeProvider';
import { themes, type Theme } from '@/lib/theme';

const themeLabels: Record<Theme, string> = {
  studio: 'Studio',
  earth: 'Earth',
  athlete: 'Athlete',
  gradient: 'Gradient',
};

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();

  // Only show in development or with ?dev query param
  if (process.env.NODE_ENV === 'production') {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 bg-card border rounded-lg p-2 shadow-lg">
      <div className="flex gap-1">
        {themes.map((t) => (
          <button
            key={t}
            onClick={() => setTheme(t)}
            className={`px-3 py-1 text-sm rounded transition-colors ${
              theme === t
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-muted'
            }`}
          >
            {themeLabels[t]}
          </button>
        ))}
      </div>
    </div>
  );
}
```

## Theme-Aware Components

```tsx
// components/Hero.tsx
'use client';

import { useTheme } from './ThemeProvider';

export function Hero() {
  const { theme } = useTheme();

  return (
    <section
      className={`
        relative min-h-[80vh] flex items-center
        ${theme === 'gradient' ? 'bg-gradient-to-br from-[hsl(var(--gradient-start))] to-[hsl(var(--gradient-end))]' : ''}
        ${theme === 'earth' ? 'bg-[url("/patterns/wave.svg")] bg-cover' : ''}
      `}
    >
      {theme === 'gradient' && (
        <div className="absolute inset-0 backdrop-blur-sm bg-background/30" />
      )}
      
      <div className="relative container mx-auto px-4">
        <h1 className={`
          text-4xl md:text-6xl font-bold
          ${theme === 'gradient' ? 'text-white drop-shadow-lg' : ''}
        `}>
          Pilates & Yoga
        </h1>
      </div>
    </section>
  );
}
```

## Background Ornaments

```tsx
// components/BackgroundOrnament.tsx
'use client';

import { useTheme } from './ThemeProvider';

export function BackgroundOrnament() {
  const { theme } = useTheme();

  if (theme === 'studio') {
    return null; // Minimal, no ornaments
  }

  if (theme === 'earth') {
    return (
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <svg className="absolute -top-20 -right-20 w-96 h-96 text-accent/30">
          {/* Organic wave shape */}
        </svg>
      </div>
    );
  }

  if (theme === 'athlete') {
    return (
      <div className="absolute top-0 left-0 w-full h-2 bg-primary" />
    );
  }

  return null;
}
```

## Layout Integration

```tsx
// app/[locale]/layout.tsx
import { ThemeProvider } from '@/components/ThemeProvider';
import { ThemeSwitcher } from '@/components/ThemeSwitcher';

export default function LocaleLayout({ children }) {
  return (
    <ThemeProvider>
      {children}
      <ThemeSwitcher />
    </ThemeProvider>
  );
}
```

## Preview via URL

Access themes via query parameter:
- `?theme=studio` - Clean minimal
- `?theme=earth` - Soft organic
- `?theme=athlete` - Bold purple
- `?theme=gradient` - Gradient hero
