---
name: forth-ai-brand
description: Apply Forth AI brand guidelines when creating frontends. Use for UI components, pages, applications, and design systems. Enforces radical simplicity, polymorphic interfaces, and the Forth AI visual identity.
---

# Forth AI Design System

**Forth AI** is the AI-native enterprise. All interfaces must embody radical simplicity and joyful usability.

## Source Documents

Before building, read these canonical documents:

| Document | Path | Contains |
|----------|------|----------|
| **Design Doctrine** | `SSOT/Product/design-doctrine.md` | UX philosophy, layout doctrine, interaction principles, governance rules |
| **Brand Guide** | `SSOT/GTM/brand-guide.md` | Visual identity, colors, typography, components, messaging |
| **Product Vision** | `SSOT/Product/vision.md` | What we're building and why |

---

## Core Philosophy (Quick Reference)

### The One Interface

**Google Search simplicity × ChatGPT polymorphism × Enterprise predictability.**

One universal input box handles:
- Search
- Actions & workflows
- Automations
- Queries
- Data retrieval
- Configuration

**Rule**: If a user needs a different page to perform a fundamentally similar task, the design has failed.

### Speed = Product Value

| Metric | Target |
|--------|--------|
| Perceived latency | <500ms |
| First token | <600ms |
| Response style | Always streaming |
| Loading states | Skeletal placeholders, never spinners |

### Restraint

- Hide advanced features until intent is signaled
- Reveal tools contextually
- First-time users must feel like they already know how to use it

---

## Visual Identity (Quick Reference)

### Colors (Dark-First)

```css
/* Backgrounds */
--bg-primary: #0a0a0c;
--bg-secondary: #111114;
--bg-tertiary: #18181c;
--bg-elevated: #1f1f24;

/* Text */
--text-primary: #fafafa;
--text-secondary: #a1a1aa;
--text-muted: #71717a;

/* Accent — Amber */
--accent: #f59e0b;
--accent-soft: rgba(245, 158, 11, 0.15);

/* Semantic */
--success: #22c55e;
--warning: #eab308;
--danger: #ef4444;

/* Borders */
--border-subtle: rgba(255, 255, 255, 0.06);
--border-default: rgba(255, 255, 255, 0.1);
```

### Typography

| Use | Font |
|-----|------|
| Headlines, brand | Clash Display |
| Body, UI | General Sans |
| Code, technical | Geist Mono |

### Effects

- **Glass**: `backdrop-filter: blur(12px)` with subtle white overlay
- **Noise texture**: 2% opacity grain overlay
- **Glow**: Amber accent shadows on CTAs and active elements

---

## Canonical Components

### Universal Input Bar

The centerpiece. Identical across all modules.

```tsx
<input
  className="w-full px-4 py-3 rounded-xl text-sm outline-none"
  style={{
    background: 'var(--bg-elevated)',
    border: '1px solid var(--border-default)',
    color: 'var(--text-primary)',
  }}
  placeholder="Ask anything..."
/>
```

### Result Card

```tsx
<div
  className="rounded-xl p-4"
  style={{
    background: 'var(--bg-elevated)',
    border: '1px solid var(--border-subtle)',
  }}
>
  <h3 style={{ fontFamily: "'Clash Display', sans-serif" }}>Title</h3>
  <p style={{ color: 'var(--text-secondary)' }}>Description</p>
  <div className="flex gap-2 mt-4">
    <Button>Edit</Button>
    <Button>Automate</Button>
    <Button>Run</Button>
  </div>
</div>
```

### Status Badges

```css
.status-draft { background: rgba(113, 113, 122, 0.2); color: #a1a1aa; }
.status-sent { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.status-paid { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
.status-overdue { background: rgba(239, 68, 68, 0.2); color: #f87171; }
```

---

## Do NOT Add

- New sidebars
- New persistent panels
- New "mini dashboards"
- New icons (use existing set)
- More than 6 colors
- Any feature that breaks the "one box" metaphor

---

## Design Checklist

Before shipping any interface:

- [ ] Single obvious entry point (universal input)
- [ ] Zero learning curve (30-second test passes)
- [ ] No unnecessary UI elements
- [ ] Speed targets met (<500ms latency)
- [ ] Streaming responses where applicable
- [ ] Brand colors applied correctly
- [ ] Typography hierarchy clear
- [ ] Reversible actions available
- [ ] No disruptive navigation
- [ ] Sparks joy

---

## The Goal

A feeling of **effortless capability** — a system that "just works" for any task without overwhelming the user.
