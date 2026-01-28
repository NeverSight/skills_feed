---
name: ui-ux-conventions
description: Convenciones de UI/UX, theming centralizado y componentes con Mantine
---

# UI/UX Conventions

## Sistema de Theming Centralizado

> ⚠️ **IMPORTANTE**: Todos los colores, tipografías y espaciados deben definirse en UN SOLO LUGAR.
> Si el cliente quiere cambiar un color, solo debe modificarse UN archivo.

## Estructura de Archivos de Tema

```
frontend/src/
├── theme/
│   ├── index.ts            # Exporta el tema completo
│   ├── colors.ts           # Paleta de colores
│   ├── typography.ts       # Fuentes y escalas
│   ├── spacing.ts          # Sistema de espaciado
│   ├── components.ts       # Overrides de componentes Mantine
│   └── mantine-theme.ts    # Configuración final de Mantine
```

## Definición de Colores (colors.ts)

```typescript
// theme/colors.ts

// ============================================
// COLORES DEL CLIENTE - MODIFICAR AQUÍ
// ============================================

export const brandColors = {
  // Colores principales basados en logo Santa Lucía
  indigo: {
    50: '#EEF2FF',
    100: '#E0E7FF',
    200: '#C7D2FE',
    300: '#A5B4FC',
    400: '#818CF8',
    500: '#1E3A5F',  // Color principal del logo
    600: '#1A3355',
    700: '#152B4A',
    800: '#11233F',
    900: '#0D1B34',
  },
  
  red: {
    50: '#FEF2F2',
    100: '#FEE2E2',
    200: '#FECACA',
    300: '#FCA5A5',
    400: '#F87171',
    500: '#C41E3A',  // Rojo del logo
    600: '#B01A34',
    700: '#9C162E',
    800: '#881228',
    900: '#740E22',
  },
  
  celeste: {
    50: '#F0F9FF',
    100: '#E0F2FE',
    200: '#BAE6FD',
    300: '#87CEEB',  // Celeste de la caja
    400: '#38BDF8',
    500: '#0EA5E9',
    600: '#0284C7',
    700: '#0369A1',
    800: '#075985',
    900: '#0C4A6E',
  },
  
  // Colores de la bandera italiana (acentos)
  italia: {
    green: '#008C45',
    white: '#FFFFFF',
    red: '#CD212A',
  },
} as const;

// ============================================
// COLORES SEMÁNTICOS - NO MODIFICAR
// ============================================

export const semanticColors = {
  success: '#16A34A',
  warning: '#EAB308',
  error: '#DC2626',
  info: '#0EA5E9',
} as const;

// ============================================
// COLORES DE TEMA - LIGHT/DARK
// ============================================

export const lightTheme = {
  background: '#FFFFFF',
  surface: '#F8FAFC',
  border: '#E2E8F0',
  text: {
    primary: '#1E293B',
    secondary: '#64748B',
    muted: '#94A3B8',
  },
} as const;

export const darkTheme = {
  background: '#0F172A',
  surface: '#1E293B',
  border: '#334155',
  text: {
    primary: '#F1F5F9',
    secondary: '#94A3B8',
    muted: '#64748B',
  },
} as const;
```

## Configuración de Mantine Theme

```typescript
// theme/mantine-theme.ts
import { createTheme, MantineColorsTuple } from '@mantine/core';
import { brandColors, semanticColors } from './colors';

// Convertir nuestros colores a formato Mantine
const indigoColors: MantineColorsTuple = [
  brandColors.indigo[50],
  brandColors.indigo[100],
  brandColors.indigo[200],
  brandColors.indigo[300],
  brandColors.indigo[400],
  brandColors.indigo[500],
  brandColors.indigo[600],
  brandColors.indigo[700],
  brandColors.indigo[800],
  brandColors.indigo[900],
];

export const theme = createTheme({
  // Color primario
  primaryColor: 'brand',
  primaryShade: 5,
  
  // Colores custom
  colors: {
    brand: indigoColors,
    // Agregar más si es necesario
  },
  
  // Tipografía
  fontFamily: 'Inter, system-ui, sans-serif',
  fontFamilyMonospace: 'JetBrains Mono, monospace',
  
  headings: {
    fontFamily: 'Inter, system-ui, sans-serif',
    fontWeight: '600',
  },
  
  // Border radius
  radius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
  },
  
  // Spacing (base 4px)
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  
  // Overrides de componentes
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
    Card: {
      defaultProps: {
        radius: 'md',
        shadow: 'sm',
        padding: 'md',
        withBorder: true,
      },
    },
    Modal: {
      defaultProps: {
        radius: 'md',
        centered: true,
      },
    },
    TextInput: {
      defaultProps: {
        radius: 'md',
      },
    },
    Select: {
      defaultProps: {
        radius: 'md',
      },
    },
  },
});
```

## Provider Setup

```typescript
// app/providers.tsx
import { MantineProvider, ColorSchemeScript } from '@mantine/core';
import { theme } from '@/theme/mantine-theme';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ColorSchemeScript defaultColorScheme="light" />
      <MantineProvider theme={theme} defaultColorScheme="light">
        {children}
      </MantineProvider>
    </>
  );
}
```

## CSS Variables Globales

```css
/* styles/globals.css */

/* Variables que Mantine no maneja directamente */
:root {
  /* Colores de marca - MODIFICAR AQUÍ SI CAMBIAN */
  --brand-indigo: #1E3A5F;
  --brand-red: #C41E3A;
  --brand-celeste: #87CEEB;
  
  /* Italia */
  --italia-green: #008C45;
  --italia-red: #CD212A;
}

/* Dark mode overrides */
[data-mantine-color-scheme="dark"] {
  --brand-indigo: #3B82F6;
}
```

## Cómo Cambiar Colores

### Para cambiar el color principal:

1. Abrir `theme/colors.ts`
2. Modificar `brandColors.indigo[500]` (color principal)
3. Ajustar la escala completa si es necesario
4. Los cambios se aplican automáticamente en toda la app

### Para cambiar el tema de Mantine:

1. Abrir `theme/mantine-theme.ts`
2. Modificar las propiedades necesarias
3. Los componentes Mantine se actualizan automáticamente

## Uso en Componentes

### ❌ INCORRECTO - Hardcodear colores

```tsx
// Nunca hacer esto
<Button style={{ backgroundColor: '#1E3A5F' }}>
  Guardar
</Button>

<Text color="#64748B">Texto secundario</Text>
```

### ✅ CORRECTO - Usar tema

```tsx
// Usar colores del tema
<Button color="brand">
  Guardar
</Button>

<Text c="dimmed">Texto secundario</Text>

// Si necesitás un color específico de brand
<Box bg="brand.5">...</Box>
```

### ✅ CORRECTO - Usar CSS variables

```tsx
// Para casos especiales
<div style={{ color: 'var(--brand-red)' }}>
  Texto rojo marca
</div>
```

## Componentes Reutilizables con Tema

```tsx
// shared/components/PageHeader.tsx
import { Group, Title, Button } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';

interface PageHeaderProps {
  title: string;
  onAdd?: () => void;
  addLabel?: string;
}

export function PageHeader({ title, onAdd, addLabel = 'Nuevo' }: PageHeaderProps) {
  return (
    <Group justify="space-between" mb="lg">
      <Title order={2}>{title}</Title>
      {onAdd && (
        <Button leftSection={<IconPlus size={16} />} onClick={onAdd}>
          {addLabel}
        </Button>
      )}
    </Group>
  );
}
```

## Estados y Badges

```tsx
// shared/components/StatusBadge.tsx
import { Badge, MantineColor } from '@mantine/core';

type Status = 'BORRADOR' | 'CONFIRMADO' | 'LIQUIDADO' | 'ABONADA';

const statusConfig: Record<Status, { color: MantineColor; label: string }> = {
  BORRADOR: { color: 'gray', label: 'Borrador' },
  CONFIRMADO: { color: 'blue', label: 'Confirmado' },
  LIQUIDADO: { color: 'green', label: 'Liquidado' },
  ABONADA: { color: 'violet', label: 'Abonada' },
};

export function StatusBadge({ status }: { status: Status }) {
  const config = statusConfig[status];
  return <Badge color={config.color}>{config.label}</Badge>;
}
```

## Toggle Dark/Light Mode

```tsx
// shared/components/ColorSchemeToggle.tsx
import { ActionIcon, useMantineColorScheme } from '@mantine/core';
import { IconSun, IconMoon } from '@tabler/icons-react';

export function ColorSchemeToggle() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  
  return (
    <ActionIcon 
      variant="subtle" 
      onClick={() => toggleColorScheme()}
      aria-label="Toggle color scheme"
    >
      {colorScheme === 'dark' ? <IconSun size={20} /> : <IconMoon size={20} />}
    </ActionIcon>
  );
}
```

## Checklist de UI

Antes de crear cualquier componente visual:

- [ ] ¿Usé colores del tema (`color="brand"`) en vez de hardcodear?
- [ ] ¿Usé spacing del tema (`mb="md"`) en vez de píxeles?
- [ ] ¿El componente funciona en light y dark mode?
- [ ] ¿El componente es responsive?
- [ ] ¿Tiene estados de hover/focus/disabled?
- [ ] ¿Es accesible (labels, alt, keyboard)?
