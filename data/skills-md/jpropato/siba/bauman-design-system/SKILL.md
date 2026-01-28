---
name: bauman-design-system
description: Sistema de diseño para el ERP SIBA (Sistema Bauman). Debe usarse SIEMPRE al crear o modificar componentes UI, páginas, formularios, o cualquier elemento visual. Garantiza consistencia en colores, tipografía, componentes, responsive y patrones de la aplicación.
---

# Sistema de Diseño SIBA (Bauman)

Referencia obligatoria al desarrollar UI para Sistema SIBA.
**Estilo: Corporate Premium** | **Dark Mode + Light Mode** | **Responsive: Desktop-first**

---

## ⚠️ Reglas Críticas

1. **SIEMPRE responsive** - Desktop-first, debe funcionar en 375px+
2. **SIEMPRE ambos modos** - Light y Dark mode con `dark:` prefix
3. **NUNCA emojis** - Solo iconos Material Symbols
4. **NUNCA colores hardcodeados** - Usar CSS variables o tokens Tailwind
5. **SIEMPRE usar la paleta Gold** para acciones principales y estados activos

---

## Identidad Visual

### Estética

- **Corporate Premium**: Elegante, minimalista, sofisticado
- **Influencia geométrica**: Inspirado en el logo Bauman (formas cuadradas)
- **Sensación de lujo**: Uso estratégico del dorado sobre fondos neutros

### Tipografía

| Propiedad   | Valor                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------- |
| Font Family | **Manrope** (Google Fonts)                                                               |
| Weights     | 400, 500, 600, 700, 800                                                                  |
| Import      | `https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap` |

```tsx
// Clase Tailwind
className = 'font-sans'; // Manrope configurado como default
```

### Iconografía

| Librería         | Import                                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| Material Symbols | `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap` |

```tsx
<span className="material-symbols-outlined">dashboard</span>
```

---

## Paleta de Colores

### 🥇 Gold Accent (Protagonista)

| Token                   | HEX       | Uso                               |
| ----------------------- | --------- | --------------------------------- |
| `gold` / `gold-DEFAULT` | `#bd8e3d` | CTAs, estados activos, highlights |
| `gold-light`            | `#e6c489` | Hover states, fondos suaves       |
| `gold-muted`            | `#C5A36A` | Bordes, elementos secundarios     |

```tsx
// Botón primario (CTA)
className = 'bg-gold text-white hover:bg-gold-light';

// Estado activo sidebar
className = 'bg-gold/10 text-gold border-l-2 border-gold';
```

### Light Mode

| Token          | HEX / Tailwind                 | Uso              |
| -------------- | ------------------------------ | ---------------- |
| background     | `#f8f8f7` / `bg-[#f8f8f7]`     | Fondo principal  |
| surface        | `#ffffff` / `bg-white`         | Cards, modales   |
| border         | `#e5e5e3` / `border-[#e5e5e3]` | Bordes           |
| text-primary   | `#18181B` / `text-slate-900`   | Texto principal  |
| text-secondary | `#52525B` / `text-slate-500`   | Texto secundario |
| text-muted     | `#a1a1aa` / `text-slate-400`   | Placeholders     |

### Dark Mode

| Token          | HEX / Tailwind                      | Uso                  |
| -------------- | ----------------------------------- | -------------------- |
| background     | `#121416` / `dark:bg-[#121416]`     | Fondo principal      |
| surface        | `#1a1c1e` / `dark:bg-[#1a1c1e]`     | Cards, sidebar       |
| border         | `#37322a` / `dark:border-[#37322a]` | Bordes               |
| text-primary   | `#fafafa` / `dark:text-slate-100`   | Texto principal      |
| text-secondary | `#a1a1aa` / `dark:text-slate-400`   | Texto secundario     |
| charcoal       | `#2F3136`                           | Superficies elevadas |

### Semánticos

| Token   | Light     | Dark      |
| ------- | --------- | --------- |
| success | `#10b981` | `#34d399` |
| warning | `#f59e0b` | `#fbbf24` |
| error   | `#ef4444` | `#f87171` |
| info    | `#3b82f6` | `#60a5fa` |

---

## CSS Variables

```css
:root {
  /* Gold Accent */
  --gold-primary: #bd8e3d;
  --gold-light: #e6c489;
  --gold-muted: #c5a36a;

  /* Backgrounds */
  --background: #f8f8f7;
  --surface: #ffffff;
  --border: #e5e5e3;

  /* Text */
  --foreground: #18181b;
  --muted: #52525b;
}

.dark {
  --background: #121416;
  --surface: #1a1c1e;
  --border: #37322a;
  --foreground: #fafafa;
  --muted: #a1a1aa;
}
```

---

## Tailwind Config

```javascript
// tailwind.config.js
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: '#bd8e3d',
          light: '#e6c489',
          muted: '#C5A36A',
        },
        charcoal: '#2F3136',
        luxury: '#35322c',
      },
      fontFamily: {
        sans: ['Manrope', 'system-ui', 'sans-serif'],
      },
    },
  },
};
```

---

## Responsive Breakpoints

```
Mobile:   < 768px  (default)
Tablet:   md: 768px
Desktop:  lg: 1024px
Wide:     xl: 1280px
```

### Layout por Breakpoint

| Elemento  | Mobile         | Tablet         | Desktop         |
| --------- | -------------- | -------------- | --------------- |
| Sidebar   | Drawer (Sheet) | Colapsado 64px | Expandido 260px |
| Header    | Hamburger      | Full           | Full            |
| Grid cols | 1              | 2              | 3-4             |

---

## Componentes Core

### Sidebar

```tsx
// Desktop expandido: 260px
<aside className="hidden lg:flex w-[260px] bg-white dark:bg-surface-dark border-r">

// Desktop colapsado: 64px (solo iconos)
<aside className="hidden lg:flex w-16 bg-white dark:bg-surface-dark">

// Mobile: Sheet/Drawer
<Sheet>
  <SheetTrigger className="lg:hidden">
    <span className="material-symbols-outlined">menu</span>
  </SheetTrigger>
  <SheetContent side="left">...</SheetContent>
</Sheet>
```

### Navegación Sidebar

```
Dashboard           (icon: dashboard)        [SELECCIONADO]
Comercial           (icon: trending_up)      → Tickets, Obras
Finanzas            (icon: account_balance)  → Tesorería Ingresos, Tesorería Egresos
Administración      (icon: corporate_fare)   → Clientes, Sedes, Vehículos, Zonas
Seguridad           (icon: admin_panel)      → Usuarios, Roles
---
Soporte             (icon: help_outline)
Configuración       (icon: settings)
```

### Estado Activo Sidebar

```tsx
// Link activo
<div className="relative flex items-center gap-3 px-3 py-3 rounded-lg bg-gold/10 text-gold">
  <div className="absolute left-0 top-[20%] bottom-[20%] w-[3px] bg-gold rounded-r shadow-[0_0_10px_rgba(189,142,61,0.4)]" />
  <span className="material-symbols-outlined">dashboard</span>
  <span className="font-semibold">Dashboard</span>
</div>
```

### Botones

```tsx
// CTA Primary (Gold)
<button className="bg-gold hover:bg-gold-light text-white font-bold rounded-lg px-4 py-2 transition-all shadow-lg shadow-gold/10">
  Iniciar Sesión
</button>

// Secondary
<button className="bg-white dark:bg-gold/10 border border-border-light dark:border-gold/20 text-slate-700 dark:text-gold font-bold rounded-lg px-4 py-2">
  Cancelar
</button>
```

### Cards

```tsx
<div className="bg-white dark:bg-charcoal/30 rounded-xl border border-[#e5e5e3] dark:border-[#37322a] p-6 shadow-sm">
```

### Empty State

```tsx
<div className="flex flex-col items-center justify-center min-h-[400px] border-2 border-dashed border-slate-200 dark:border-[#37322a] rounded-xl bg-white/50 dark:bg-charcoal/20 p-12 text-center">
  <div className="size-20 bg-gold/10 rounded-full flex items-center justify-center mb-6 border border-gold/20">
    <span className="material-symbols-outlined text-gold text-5xl">dashboard_customize</span>
  </div>
  <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">Título</h3>
  <p className="text-slate-500 dark:text-slate-400 mb-8">Descripción...</p>
</div>
```

---

## Animaciones y Transiciones

```tsx
// Transiciones globales (150-200ms)
className = 'transition-all duration-200';

// Hover en cards
className = 'hover:shadow-lg hover:-translate-y-0.5';

// Fade in entrada
className = 'animate-fade-in'; // Definir en CSS

// Sidebar collapse
className = 'transition-[width] duration-300 ease-in-out';
```

---

## Checklist Pre-Desarrollo

- [ ] Componente funciona en 375px (iPhone SE)
- [ ] Componente tiene clases `dark:`
- [ ] Usa Material Symbols, NO emojis
- [ ] Sidebar es Sheet en mobile
- [ ] CTAs usan color Gold
- [ ] Touch targets mínimo 44x44px
- [ ] Tipografía es Manrope

---

## Mockups de Referencia

| Pantalla    | Archivo                                                       |
| ----------- | ------------------------------------------------------------- |
| Login Light | `docs/mockup-ui/siba_login_-_light_mode_1/screen.png`         |
| Login Dark  | `docs/mockup-ui/siba_login_-_light_mode_2/screen.png`         |
| Dashboard   | `docs/mockup-ui/siba_dashboard_-_desktop_expanded/screen.png` |

---

## Logo

- Archivo: `docs/assets/logo-bauman.png`
- Estilo: "BAUMAN" con "BAU" negro, "MAN" gris
- Subtítulo: "SOLUCIONES CORPORATIVAS"
- Icono placeholder: Escaleras geométricas SVG en gold
