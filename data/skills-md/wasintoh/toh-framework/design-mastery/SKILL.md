---
name: design-mastery
version: 2.0.0
description: >
  World-class design system with extensible business type registry.
  Automatically selects appropriate design patterns based on business context.
  Anti-AI detection, trend-aware, production-ready design decisions.
  CRITICAL: Must be read before any UI creation task.
triggers:
  - /toh-vibe (new projects)
  - /toh-ui (new components)
  - /toh-design (polish)
  - Any UI creation request
---

# Design Mastery Skill v2.0.0

> **"Design is intelligence made visible."** — Alina Wheeler

World-class design system ที่ช่วยให้ AI สร้าง UI ที่สวย professional ไม่ซ้ำใคร และที่สำคัญ **ไม่ดู "AI-generated"**

---

## 🧠 Core Philosophy

### The Invisible Design Principle

```
Good design is INVISIBLE.
Users don't notice good design - they notice BAD design.

When someone says "this looks AI-generated", that's design failure.
When someone says "this looks professional", that's still not enough.
When someone DOESN'T comment on design and just USES the app - that's success.
```

### Three Pillars of Design Mastery

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN MASTERY                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CONTEXT INTELLIGENCE                                        │
│     └── Understand business + audience = right design           │
│                                                                 │
│  2. ANTI-AI VIGILANCE                                          │
│     └── Detect and eliminate AI-looking patterns                │
│                                                                 │
│  3. CRAFT EXCELLENCE                                           │
│     └── Every pixel intentional, every space meaningful         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Design Process (5 Steps)

```
USER REQUEST
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: BUSINESS ANALYSIS                                       │
│ - What type of business/app is this?                            │
│ - Who is the target audience?                                   │
│ - What emotion should it evoke?                                 │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: SELECT DESIGN PROFILE                                   │
│ - Match business to registry profile                            │
│ - Load design tokens (colors, typography, spacing)              │
│ - Load component patterns                                       │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: ANTI-AI SCAN                                           │
│ - Check for AI red flags in design choices                      │
│ - Ensure uniqueness and intentionality                          │
│ - Apply human-like variations                                   │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: IMPLEMENT DESIGN                                        │
│ - Apply design tokens to components                             │
│ - Create consistent design system                               │
│ - Add appropriate micro-interactions                            │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: QUALITY VERIFICATION                                    │
│ - Would a designer be proud of this?                            │
│ - Does it feel like a real product?                             │
│ - Is it better than competitors?                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏢 Business Type Registry (Extensible)

### How to Use This Registry

```typescript
// 1. Identify business type from user request
const businessType = analyzeBusinessType(userRequest);

// 2. Load design profile
const profile = DESIGN_REGISTRY[businessType] || DESIGN_REGISTRY['saas-dashboard'];

// 3. Apply design tokens
applyDesignTokens(profile.tokens);

// 4. Use component patterns
useComponentPatterns(profile.patterns);
```

### Registry Structure

```yaml
# Each entry in the registry follows this structure:
business_type:
  name: "Human-readable name"
  description: "When to use this profile"
  keywords: ["matching", "keywords"]
  emotion: "What users should feel"
  
  tokens:
    colors:
      primary: "#hex"
      secondary: "#hex"
      accent: "#hex"
      background: "#hex"
      surface: "#hex"
      text:
        primary: "#hex"
        secondary: "#hex"
        muted: "#hex"
      semantic:
        success: "#hex"
        warning: "#hex"
        error: "#hex"
    
    typography:
      heading: "Font Family"
      body: "Font Family"
      thai: "Thai Font (if applicable)"
      scale: [xs, sm, base, lg, xl, 2xl, 3xl, 4xl]
    
    spacing:
      unit: 4 # base unit in pixels
      scale: [1, 2, 3, 4, 6, 8, 12, 16, 24]
    
    borders:
      radius:
        sm: "0.125rem"
        md: "0.375rem"
        lg: "0.5rem"
        xl: "0.75rem"
        full: "9999px"
      default: "md" # which to use by default
    
    shadows:
      level: "subtle | moderate | elevated"
      
    animation:
      level: "minimal | moderate | expressive"
      timing: "fast | normal | slow"
  
  patterns:
    layout: "sidebar | top-nav | minimal | split"
    hero: "centered | split | background | none"
    cards: "elevated | flat | bordered | glass"
    buttons: "solid | outline | ghost | gradient"
    
  anti_patterns:
    - "Specific things to AVOID for this business type"
```

---

## 📦 Design Profile Registry

### Profile: SaaS Dashboard
```yaml
saas-dashboard:
  name: "SaaS Dashboard"
  description: "Data-driven apps, admin panels, analytics tools"
  keywords: ["dashboard", "admin", "analytics", "tracker", "management", "tool"]
  emotion: "Efficient, Clear, Trustworthy"
  
  tokens:
    colors:
      primary: "#6366F1"      # Indigo - professional yet modern
      secondary: "#8B5CF6"    # Violet - accent
      accent: "#F59E0B"       # Amber - attention
      background: "#F8FAFC"   # Slate-50
      surface: "#FFFFFF"
      text:
        primary: "#0F172A"    # Slate-900
        secondary: "#475569"  # Slate-600
        muted: "#94A3B8"      # Slate-400
      semantic:
        success: "#10B981"    # Emerald-500
        warning: "#F59E0B"    # Amber-500
        error: "#EF4444"      # Red-500
    
    typography:
      heading: "Inter"
      body: "Inter"
      thai: "Noto Sans Thai"
      mono: "JetBrains Mono"
    
    borders:
      default: "md"           # rounded-md
      cards: "lg"             # rounded-lg
      buttons: "md"           # rounded-md
      inputs: "md"            # rounded-md
    
    shadows:
      level: "subtle"
      cards: "shadow-sm hover:shadow-md"
      modals: "shadow-xl"
    
    animation:
      level: "moderate"
      timing: "200ms"
      easing: "ease-out"
  
  patterns:
    layout: "sidebar"
    hero: "none"
    cards: "bordered"         # Clean, not heavy shadows
    buttons: "solid"
    tables: "striped"
    
  anti_patterns:
    - "Heavy gradients (looks dated)"
    - "Rounded-full on cards"
    - "Too many accent colors"
    - "Bounce animations"
```

### Profile: E-commerce
```yaml
ecommerce:
  name: "E-commerce"
  description: "Online stores, product catalogs, marketplaces"
  keywords: ["shop", "store", "product", "sell", "buy", "cart", "order", "marketplace"]
  emotion: "Trustworthy, Action-oriented, Exciting"
  
  tokens:
    colors:
      primary: "#2563EB"      # Blue - trust
      secondary: "#1E40AF"    # Darker blue
      accent: "#F97316"       # Orange - action, CTAs
      background: "#FAFAFA"
      surface: "#FFFFFF"
      text:
        primary: "#1F2937"    # Gray-800
        secondary: "#4B5563"  # Gray-600
        muted: "#9CA3AF"      # Gray-400
      semantic:
        success: "#059669"    # Emerald-600
        warning: "#D97706"    # Amber-600
        error: "#DC2626"      # Red-600
        sale: "#DC2626"       # Red for discounts
    
    typography:
      heading: "Poppins"
      body: "Inter"
      thai: "Prompt"
      price: "Tabular nums"
    
    borders:
      default: "lg"
      cards: "xl"
      buttons: "lg"
      product_cards: "xl"
    
    shadows:
      level: "elevated"
      cards: "shadow-md hover:shadow-xl"
      product: "shadow-lg"
    
    animation:
      level: "expressive"
      timing: "300ms"
      cart_add: "scale bounce"
  
  patterns:
    layout: "top-nav"
    hero: "split"
    cards: "elevated"
    buttons: "solid"
    product_grid: "responsive 2-4 cols"
    
  anti_patterns:
    - "Muted colors (needs energy)"
    - "Small product images"
    - "Hidden add-to-cart"
    - "Minimal animations (needs feedback)"
```

### Profile: AI / Chatbot
```yaml
ai-chatbot:
  name: "AI Chatbot / AI Tool"
  description: "Conversational AI, chatbots, AI assistants, AI SaaS"
  keywords: ["ai", "chatbot", "assistant", "gpt", "claude", "chat", "conversation", "bot"]
  emotion: "Friendly, Intelligent, Approachable"
  
  tokens:
    colors:
      # ⚠️ CRITICAL: Do NOT use purple-blue gradient! Every AI uses it!
      primary: "#0D9488"      # Teal - friendly, different from others
      secondary: "#14B8A6"    # Lighter teal
      accent: "#F472B6"       # Pink - warmth
      background: "#F0FDFA"   # Teal-50
      surface: "#FFFFFF"
      text:
        primary: "#134E4A"    # Teal-900
        secondary: "#115E59"  # Teal-800
        muted: "#5EEAD4"      # Teal-300
      chat:
        user_bubble: "#0D9488"
        bot_bubble: "#F0FDFA"
        typing: "#99F6E4"
    
    typography:
      heading: "Nunito"
      body: "Nunito"
      thai: "Prompt"
      chat: "system-ui"
    
    borders:
      default: "xl"
      chat_bubble: "2xl"
      buttons: "full"
      cards: "xl"
    
    shadows:
      level: "soft"
      chat: "shadow-sm"
      cards: "shadow-md"
    
    animation:
      level: "expressive"
      typing: "pulse"
      message_appear: "fade-up"
      timing: "250ms"
  
  patterns:
    layout: "split"           # Chat center, sidebar history
    hero: "centered"
    cards: "glass"
    buttons: "solid rounded-full"
    chat: "bubbles with tails"
    
  anti_patterns:
    - "Purple-blue gradient (EVERY AI uses this!)"
    - "Sparkle emoji ✨ everywhere"
    - "Robot/AI imagery (too cliché)"
    - "Cold/mechanical feeling"
    - "Generic 'AI Assistant' naming"
```

### Profile: Food & Restaurant
```yaml
food-restaurant:
  name: "Food & Restaurant"
  description: "Restaurants, food delivery, menus, F&B businesses"
  keywords: ["food", "restaurant", "menu", "order", "delivery", "cafe", "kitchen", "eat"]
  emotion: "Warm, Appetizing, Welcoming"
  
  tokens:
    colors:
      primary: "#DC2626"      # Red - appetite
      secondary: "#B91C1C"    # Darker red
      accent: "#F59E0B"       # Amber - warmth
      background: "#FFFBEB"   # Amber-50
      surface: "#FFFFFF"
      text:
        primary: "#292524"    # Stone-800
        secondary: "#57534E"  # Stone-600
        muted: "#A8A29E"      # Stone-400
      semantic:
        success: "#16A34A"
        spicy: "#DC2626"
        vegetarian: "#22C55E"
    
    typography:
      heading: "Playfair Display"  # Elegant
      body: "Source Sans Pro"
      thai: "Sarabun"
      menu: "serif"
    
    borders:
      default: "lg"
      cards: "xl"
      images: "2xl"
    
    shadows:
      level: "moderate"
      cards: "shadow-md"
      images: "shadow-lg"
    
    animation:
      level: "moderate"
      hover: "scale 1.02"
      timing: "300ms"
  
  patterns:
    layout: "top-nav"
    hero: "background"        # Full-width food imagery
    cards: "elevated"
    menu_style: "image-heavy"
    
  anti_patterns:
    - "Cold/blue colors"
    - "Small food images"
    - "Generic stock photos"
    - "Minimalist (food needs warmth)"
```

### Profile: Finance / Fintech
```yaml
finance:
  name: "Finance / Fintech"
  description: "Banking, investments, financial tools, money management"
  keywords: ["finance", "bank", "money", "invest", "payment", "wallet", "budget", "financial"]
  emotion: "Secure, Trustworthy, Professional"
  
  tokens:
    colors:
      primary: "#0F766E"      # Teal-700 - money, growth
      secondary: "#115E59"    # Teal-800
      accent: "#0284C7"       # Sky-600 - trust
      background: "#F8FAFC"   # Slate-50
      surface: "#FFFFFF"
      text:
        primary: "#0F172A"    # Slate-900
        secondary: "#334155"  # Slate-700
        muted: "#64748B"      # Slate-500
      semantic:
        positive: "#059669"   # Emerald - gains
        negative: "#DC2626"   # Red - losses
        warning: "#D97706"
    
    typography:
      heading: "IBM Plex Sans"
      body: "IBM Plex Sans"
      thai: "IBM Plex Sans Thai"
      numbers: "Tabular lining"
    
    borders:
      default: "md"
      cards: "lg"
      buttons: "md"
    
    shadows:
      level: "subtle"
      cards: "shadow-sm"
    
    animation:
      level: "minimal"
      timing: "150ms"
      numbers: "count-up"
  
  patterns:
    layout: "sidebar"
    hero: "none"
    cards: "bordered"
    numbers: "large prominent"
    charts: "clean minimal"
    
  anti_patterns:
    - "Playful animations"
    - "Bright/loud colors"
    - "Casual typography"
    - "Excessive decoration"
```

### Profile: Healthcare / Wellness
```yaml
healthcare:
  name: "Healthcare / Wellness"
  description: "Health apps, medical, wellness, fitness tracking"
  keywords: ["health", "medical", "wellness", "fitness", "doctor", "patient", "care", "clinic"]
  emotion: "Calm, Trustworthy, Caring"
  
  tokens:
    colors:
      primary: "#0EA5E9"      # Sky-500 - calm, medical
      secondary: "#0284C7"    # Sky-600
      accent: "#10B981"       # Emerald - health, growth
      background: "#F0F9FF"   # Sky-50
      surface: "#FFFFFF"
      text:
        primary: "#0C4A6E"    # Sky-900
        secondary: "#075985"  # Sky-800
        muted: "#7DD3FC"      # Sky-300
    
    typography:
      heading: "Source Sans Pro"
      body: "Source Sans Pro"
      thai: "Sarabun"
    
    borders:
      default: "lg"
      cards: "xl"
      buttons: "lg"
    
    shadows:
      level: "none"           # Clean, clinical
      cards: "border only"
    
    animation:
      level: "minimal"
      timing: "200ms"
      transitions: "gentle"
  
  patterns:
    layout: "top-nav"
    hero: "centered"
    cards: "flat bordered"
    accessibility: "WCAG AAA"
    
  anti_patterns:
    - "Dark themes"
    - "Sharp corners"
    - "Aggressive colors"
    - "Complex animations"
```

### Profile: Creative / Portfolio
```yaml
creative:
  name: "Creative / Portfolio"
  description: "Design portfolios, creative agencies, artists"
  keywords: ["portfolio", "creative", "agency", "design", "art", "studio"]
  emotion: "Expressive, Unique, Inspiring"
  
  tokens:
    colors:
      # Unique palette - break the rules!
      primary: "#7C3AED"      # Violet - creativity
      secondary: "#A78BFA"    # Violet light
      accent: "#F472B6"       # Pink
      background: "#FAFAF9"   # Stone-50
      surface: "#FFFFFF"
      text:
        primary: "#1C1917"    # Stone-900
        secondary: "#44403C"  # Stone-700
        muted: "#A8A29E"      # Stone-400
    
    typography:
      heading: "Playfair Display"  # Or custom/unique
      body: "DM Sans"
      thai: "Prompt"
    
    borders:
      default: "none"         # Clean edges
      cards: "none"
      images: "none"
    
    shadows:
      level: "elevated"
      cards: "shadow-2xl"
    
    animation:
      level: "expressive"
      scroll: "parallax"
      hover: "dramatic"
      timing: "400ms"
  
  patterns:
    layout: "minimal"
    hero: "full-screen"
    grid: "masonry"
    transitions: "page transitions"
    
  anti_patterns:
    - "Generic templates"
    - "Standard layouts"
    - "Safe color choices"
    - "Boring typography"
```

### Profile: Enterprise / B2B
```yaml
enterprise:
  name: "Enterprise / B2B"
  description: "Corporate software, B2B tools, enterprise systems"
  keywords: ["enterprise", "corporate", "b2b", "crm", "erp", "business"]
  emotion: "Professional, Reliable, Efficient"
  
  tokens:
    colors:
      primary: "#1E40AF"      # Blue-800 - trust
      secondary: "#1E3A8A"    # Blue-900
      accent: "#0369A1"       # Sky-700
      background: "#F8FAFC"
      surface: "#FFFFFF"
      text:
        primary: "#1E293B"    # Slate-800
        secondary: "#475569"  # Slate-600
        muted: "#94A3B8"      # Slate-400
    
    typography:
      heading: "IBM Plex Sans"
      body: "IBM Plex Sans"
      thai: "IBM Plex Sans Thai"
    
    borders:
      default: "sm"
      cards: "md"
      tables: "sm"
    
    shadows:
      level: "minimal"
      cards: "shadow-sm"
    
    animation:
      level: "minimal"
      timing: "150ms"
  
  patterns:
    layout: "sidebar"
    density: "high"           # More information visible
    tables: "full-featured"
    forms: "multi-step"
    
  anti_patterns:
    - "Playful elements"
    - "Casual tone"
    - "Low information density"
    - "Decorative elements"
```

---

## 🚨 Anti-AI Detection System

### Level 1: Obvious AI Tells (CRITICAL - Always check!)

| AI Pattern | Why It's Bad | Fix |
|------------|--------------|-----|
| Purple-blue gradient | Every AI uses it | Solid color or subtle gradient |
| `rounded-full` everywhere | Thoughtless default | Vary by element type |
| `shadow-md` on everything | No hierarchy | Use shadow scale purposefully |
| Inter font everywhere | Default choice | Choose font for business |
| Emoji in headings 👋🚀 | Looks unprofessional | Remove or use sparingly |
| "Welcome back, User!" | Generic placeholder | Use actual name or remove |
| Pure black `#000` text | Too harsh | Use slate-900 or gray-900 |
| Bounce animations | Childish | Use ease-out transitions |

### Level 2: Subtle AI Tells (Important)

| AI Pattern | Why It's Bad | Fix |
|------------|--------------|-----|
| Same border-radius everywhere | No visual hierarchy | Vary: sm for inputs, lg for cards |
| Gradient text | Overused trend | Solid color or subtle highlight |
| Card → Card → Card layout | Monotonous | Mix layouts: cards, tables, lists |
| Centered everything | Lazy alignment | Use grids, asymmetry |
| Generic hero sections | Template-looking | Custom layout per business |
| Stock illustration style | Obvious AI | Custom icons or real photos |
| Equal spacing everywhere | No rhythm | Create visual rhythm |

### Level 3: Deep AI Tells (Polish)

| AI Pattern | Why It's Bad | Fix |
|------------|--------------|-----|
| Same hover effect everywhere | Thoughtless | Vary by element importance |
| No empty states | Incomplete | Design proper empty states |
| Generic loading spinners | Lazy | Custom skeleton or branded loader |
| Copy-paste component styles | Inconsistent | Create design tokens |
| No micro-interactions | Lifeless | Add subtle feedback |
| Perfect symmetry | Unnatural | Introduce subtle asymmetry |
| Generic icons | No personality | Choose icon set that fits brand |

### Anti-AI Checklist (Run before delivery!)

```markdown
□ No purple-blue gradients?
□ Border-radius varies by element?
□ Shadows have purpose and hierarchy?
□ Typography chosen for business (not just Inter)?
□ No emoji in headings?
□ Text colors are soft (not pure black)?
□ Animations are subtle (no bounce)?
□ Layout has variety (not all cards)?
□ Empty states are designed?
□ Loading states are polished?
□ Would a human designer approve?
```

---

## 🎨 Design Token System

### Color Scale Generator

```typescript
// Generate consistent color scales
function generateColorScale(baseHue: number, saturation: number) {
  return {
    50:  `hsl(${baseHue}, ${saturation}%, 97%)`,
    100: `hsl(${baseHue}, ${saturation}%, 94%)`,
    200: `hsl(${baseHue}, ${saturation}%, 86%)`,
    300: `hsl(${baseHue}, ${saturation}%, 76%)`,
    400: `hsl(${baseHue}, ${saturation}%, 62%)`,
    500: `hsl(${baseHue}, ${saturation}%, 50%)`,  // Primary
    600: `hsl(${baseHue}, ${saturation}%, 42%)`,
    700: `hsl(${baseHue}, ${saturation}%, 34%)`,
    800: `hsl(${baseHue}, ${saturation}%, 26%)`,
    900: `hsl(${baseHue}, ${saturation}%, 18%)`,
  };
}
```

### Typography Scale

```css
/* Consistent type scale (1.25 ratio) */
--text-xs: 0.64rem;    /* 10.24px */
--text-sm: 0.8rem;     /* 12.8px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.25rem;    /* 20px */
--text-xl: 1.563rem;   /* 25px */
--text-2xl: 1.953rem;  /* 31.25px */
--text-3xl: 2.441rem;  /* 39px */
--text-4xl: 3.052rem;  /* 48.8px */
```

### Spacing Scale

```css
/* 4px base unit */
--space-1: 0.25rem;    /* 4px */
--space-2: 0.5rem;     /* 8px */
--space-3: 0.75rem;    /* 12px */
--space-4: 1rem;       /* 16px */
--space-5: 1.25rem;    /* 20px */
--space-6: 1.5rem;     /* 24px */
--space-8: 2rem;       /* 32px */
--space-10: 2.5rem;    /* 40px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */
```

---

## 🌍 Trend Awareness (2024-2025)

### Current Design Trends (Use selectively!)

| Trend | When to Use | When to Avoid |
|-------|-------------|---------------|
| **Bento Grid** | Creative, Portfolio | Enterprise, Healthcare |
| **Glassmorphism** | AI apps, Modern SaaS | Finance, Traditional |
| **Dark Mode** | Dev tools, Creative | Healthcare, Kids |
| **Neubrutalism** | Creative, Youth brands | Corporate, Medical |
| **Microinteractions** | E-commerce, SaaS | Enterprise, Minimal |
| **3D Elements** | Gaming, Creative | Finance, Medical |
| **Variable Fonts** | Editorial, Creative | Corporate, Forms |
| **Scroll Animations** | Marketing, Portfolio | Dashboards, Forms |

### Timeless Principles (Always apply!)

```
1. HIERARCHY - Clear visual importance
2. CONTRAST - Readable, accessible
3. ALIGNMENT - Consistent, intentional
4. PROXIMITY - Related items grouped
5. REPETITION - Consistent patterns
6. WHITESPACE - Room to breathe
```

---

## 🔌 Extensibility: Adding New Business Types

### How to Add a New Profile

```yaml
# Template for new business type
new-business-type:
  name: "Display Name"
  description: "When to use this profile"
  keywords: ["keyword1", "keyword2", "keyword3"]
  emotion: "What users should feel"
  
  tokens:
    colors:
      primary: "#hexcode"
      secondary: "#hexcode"
      accent: "#hexcode"
      background: "#hexcode"
      surface: "#hexcode"
      text:
        primary: "#hexcode"
        secondary: "#hexcode"
        muted: "#hexcode"
      semantic:
        success: "#hexcode"
        warning: "#hexcode"
        error: "#hexcode"
    
    typography:
      heading: "Font Name"
      body: "Font Name"
      thai: "Thai Font"
    
    borders:
      default: "size"
      cards: "size"
    
    shadows:
      level: "subtle | moderate | elevated"
    
    animation:
      level: "minimal | moderate | expressive"
  
  patterns:
    layout: "sidebar | top-nav | minimal"
    hero: "centered | split | background | none"
    cards: "elevated | flat | bordered | glass"
    
  anti_patterns:
    - "Thing to avoid 1"
    - "Thing to avoid 2"
```

### Examples of Extensible Types

```
# Future business types that can be added:
- gaming
- education-kids
- education-professional
- real-estate
- travel-booking
- social-media
- news-media
- government
- nonprofit
- sports-fitness
- music-entertainment
- legal-services
- logistics-shipping
```

---

## 🎯 Quick Reference

### Business Type → Design Profile Mapping

```typescript
function selectDesignProfile(keywords: string[]): DesignProfile {
  const mapping = {
    // E-commerce
    ['shop', 'store', 'product', 'cart', 'order']: 'ecommerce',
    
    // SaaS Dashboard
    ['dashboard', 'admin', 'analytics', 'tracker', 'management']: 'saas-dashboard',
    
    // AI / Chatbot
    ['ai', 'chatbot', 'assistant', 'gpt', 'claude', 'chat']: 'ai-chatbot',
    
    // Food
    ['food', 'restaurant', 'menu', 'delivery', 'cafe']: 'food-restaurant',
    
    // Finance
    ['finance', 'bank', 'money', 'invest', 'payment', 'budget']: 'finance',
    
    // Healthcare
    ['health', 'medical', 'wellness', 'fitness', 'doctor']: 'healthcare',
    
    // Creative
    ['portfolio', 'creative', 'agency', 'design', 'art']: 'creative',
    
    // Enterprise
    ['enterprise', 'corporate', 'b2b', 'crm', 'erp']: 'enterprise',
  };
  
  // Find best match
  for (const [keys, profile] of Object.entries(mapping)) {
    if (keywords.some(k => keys.includes(k.toLowerCase()))) {
      return DESIGN_REGISTRY[profile];
    }
  }
  
  // Default fallback
  return DESIGN_REGISTRY['saas-dashboard'];
}
```

---

## 📝 Integration with Agents

### For Vibe Agent (New Projects)
```
1. Analyze user request for business keywords
2. Select design profile from registry
3. Apply design tokens to project setup
4. Use component patterns from profile
5. Run anti-AI checklist before delivery
```

### For Design Agent (Polish)
```
1. Load current design system
2. Compare against appropriate profile
3. Identify deviations and AI patterns
4. Fix issues following profile guidelines
5. Verify with anti-AI checklist
```

### For UI Agent (Components)
```
1. Check project's design profile (from memory)
2. Use tokens for new components
3. Follow patterns from profile
4. Ensure consistency with existing design
```

---

## ✅ Success Criteria

A design passes if:

- [ ] Matches the business type appropriately
- [ ] No obvious AI tells (Level 1)
- [ ] No subtle AI tells (Level 2)
- [ ] Consistent design tokens throughout
- [ ] Would pass review by professional designer
- [ ] User focuses on content, not design
- [ ] Feels like a real product from a real company

---

*Design Mastery Skill v2.0.0 - World-Class Extensible Design System*


---

## 📦 Additional Business Profiles (Extended Registry)

### Profile: Education / E-Learning
```yaml
education:
  name: "Education / E-Learning"
  description: "Online courses, LMS, tutoring, educational platforms"
  keywords: ["education", "course", "learn", "school", "student", "teacher", "quiz", "lesson"]
  emotion: "Encouraging, Clear, Engaging"
  
  tokens:
    colors:
      primary: "#4F46E5"      # Indigo - knowledge, wisdom
      secondary: "#6366F1"    # Lighter indigo
      accent: "#F59E0B"       # Amber - achievement, stars
      background: "#F5F3FF"   # Violet-50 (soft)
      surface: "#FFFFFF"
      text:
        primary: "#1E1B4B"    # Indigo-950
        secondary: "#4338CA"  # Indigo-600
        muted: "#A5B4FC"      # Indigo-300
      semantic:
        success: "#10B981"    # Completed/Passed
        warning: "#F59E0B"    # In progress
        error: "#EF4444"      # Failed/Wrong
        star: "#FBBF24"       # Achievement
    
    typography:
      heading: "Nunito"       # Friendly, approachable
      body: "Inter"
      thai: "Prompt"
    
    borders:
      default: "lg"
      cards: "xl"
      progress: "full"
    
    shadows:
      level: "moderate"
      cards: "shadow-md"
    
    animation:
      level: "expressive"
      progress: "smooth fill"
      achievement: "bounce once"
      timing: "300ms"
  
  patterns:
    layout: "sidebar"
    hero: "split"             # Image + CTA
    cards: "elevated"
    progress: "prominent"
    gamification: "badges, streaks, points"
    
  anti_patterns:
    - "Boring corporate look"
    - "Dense text walls"
    - "No progress indicators"
    - "Static, no feedback"
```

### Profile: Travel / Booking
```yaml
travel:
  name: "Travel / Booking"
  description: "Travel booking, hotels, flights, vacation planning"
  keywords: ["travel", "hotel", "flight", "booking", "vacation", "trip", "tour", "destination"]
  emotion: "Adventurous, Exciting, Trustworthy"
  
  tokens:
    colors:
      primary: "#0891B2"      # Cyan-600 - sky, ocean
      secondary: "#06B6D4"    # Cyan-500
      accent: "#F97316"       # Orange - sunset, excitement
      background: "#ECFEFF"   # Cyan-50
      surface: "#FFFFFF"
      text:
        primary: "#164E63"    # Cyan-900
        secondary: "#0E7490"  # Cyan-700
        muted: "#67E8F9"      # Cyan-300
      semantic:
        success: "#10B981"
        deal: "#DC2626"       # Special deals
        popular: "#F59E0B"    # Popular choices
    
    typography:
      heading: "Poppins"
      body: "Inter"
      thai: "Prompt"
      price: "Tabular nums"
    
    borders:
      default: "xl"
      cards: "2xl"
      images: "xl"
    
    shadows:
      level: "elevated"
      cards: "shadow-lg hover:shadow-xl"
    
    animation:
      level: "expressive"
      images: "zoom on hover"
      timing: "300ms"
  
  patterns:
    layout: "top-nav"
    hero: "full-width image"
    search: "prominent center"
    cards: "image-heavy"
    gallery: "carousel"
    
  anti_patterns:
    - "Muted colors"
    - "Small destination images"
    - "Complex booking forms"
    - "No price transparency"
```

### Profile: Real Estate
```yaml
real-estate:
  name: "Real Estate"
  description: "Property listings, real estate agencies, home buying/selling"
  keywords: ["property", "real estate", "house", "apartment", "rent", "buy", "home", "listing"]
  emotion: "Trustworthy, Premium, Clear"
  
  tokens:
    colors:
      primary: "#1E3A5F"      # Navy - trust, premium
      secondary: "#2D5A87"    # Lighter navy
      accent: "#B8860B"       # Gold - premium feel
      background: "#F8FAFC"   # Slate-50
      surface: "#FFFFFF"
      text:
        primary: "#0F172A"    # Slate-900
        secondary: "#334155"  # Slate-700
        muted: "#94A3B8"      # Slate-400
      semantic:
        success: "#059669"
        featured: "#B8860B"   # Gold for premium
        new: "#2563EB"        # New listing
    
    typography:
      heading: "Playfair Display"  # Elegant, premium
      body: "Source Sans Pro"
      thai: "Sarabun"
      price: "Tabular lining"
    
    borders:
      default: "md"
      cards: "lg"
      images: "md"
    
    shadows:
      level: "subtle"
      cards: "shadow-sm hover:shadow-md"
    
    animation:
      level: "minimal"
      timing: "200ms"
  
  patterns:
    layout: "top-nav"
    hero: "search-focused"
    cards: "image-dominant"
    gallery: "full-screen lightbox"
    map: "integrated"
    
  anti_patterns:
    - "Playful colors"
    - "Small property images"
    - "Hidden pricing"
    - "Cluttered listings"
```

### Profile: Gaming / Entertainment
```yaml
gaming:
  name: "Gaming / Entertainment"
  description: "Games, gaming platforms, entertainment apps"
  keywords: ["game", "gaming", "play", "entertainment", "esports", "stream", "player"]
  emotion: "Exciting, Immersive, Dynamic"
  
  tokens:
    colors:
      # Bold, vibrant palette
      primary: "#7C3AED"      # Violet - gaming culture
      secondary: "#8B5CF6"    # Lighter violet
      accent: "#10B981"       # Emerald - online/active
      background: "#0F0F23"   # Near black (dark theme!)
      surface: "#1A1A2E"
      text:
        primary: "#F8FAFC"    # White
        secondary: "#CBD5E1"  # Slate-300
        muted: "#64748B"      # Slate-500
      semantic:
        online: "#10B981"     # Green = online
        offline: "#64748B"    # Gray = offline
        live: "#EF4444"       # Red = live
        gold: "#FBBF24"       # Achievements
    
    typography:
      heading: "Rajdhani"     # Tech/gaming feel
      body: "Inter"
      thai: "Prompt"
    
    borders:
      default: "lg"
      cards: "xl"
      avatars: "full"
    
    shadows:
      level: "dramatic"
      glow: "colored glow effects"
    
    animation:
      level: "expressive"
      timing: "200ms"
      hover: "scale + glow"
      transitions: "smooth"
  
  patterns:
    layout: "sidebar"
    theme: "DARK MODE by default"
    cards: "glass morphism"
    avatars: "prominent"
    stats: "real-time updates"
    
  anti_patterns:
    - "Light theme (feels wrong)"
    - "Corporate/boring look"
    - "Static content"
    - "Slow animations"
```

### Profile: Social Media / Community
```yaml
social-media:
  name: "Social Media / Community"
  description: "Social platforms, communities, forums, networking"
  keywords: ["social", "community", "forum", "network", "post", "share", "follow", "feed"]
  emotion: "Connected, Engaging, Personal"
  
  tokens:
    colors:
      primary: "#3B82F6"      # Blue - connection
      secondary: "#60A5FA"    # Lighter blue
      accent: "#EC4899"       # Pink - likes, hearts
      background: "#F8FAFC"
      surface: "#FFFFFF"
      text:
        primary: "#1E293B"
        secondary: "#475569"
        muted: "#94A3B8"
      semantic:
        like: "#EC4899"       # Hearts
        success: "#10B981"
        notification: "#EF4444"
    
    typography:
      heading: "Inter"
      body: "Inter"
      thai: "Noto Sans Thai"
    
    borders:
      default: "lg"
      cards: "xl"
      avatars: "full"
      posts: "lg"
    
    shadows:
      level: "subtle"
      cards: "shadow-sm"
    
    animation:
      level: "expressive"
      like: "heart pop"
      notification: "shake"
      timing: "200ms"
  
  patterns:
    layout: "centered feed"
    cards: "bordered"
    feed: "infinite scroll"
    interactions: "instant feedback"
    avatars: "prominent"
    
  anti_patterns:
    - "Slow interactions"
    - "No feedback animations"
    - "Hidden engagement metrics"
    - "Complex navigation"
```

---

## 🔮 Trend Registry (2024-2025 Updates)

### How to Use Trends

```typescript
// Trends are OPTIONAL enhancements, not requirements
// Apply only when they fit the business type

interface TrendConfig {
  name: string;
  suitableFor: string[];     // Business types
  notSuitableFor: string[];  // Avoid for these
  implementation: string;    // How to implement
  overuseWarning: string;    // When it becomes a problem
}
```

### Active Trends Registry

```yaml
bento-grid:
  name: "Bento Grid Layout"
  suitableFor: ["creative", "saas-dashboard", "social-media"]
  notSuitableFor: ["enterprise", "healthcare", "finance"]
  implementation: |
    grid grid-cols-4 gap-4
    Items span different col/row counts
    Asymmetric but balanced
  overuseWarning: "Not for data-heavy dashboards"

glassmorphism:
  name: "Glass Morphism"
  suitableFor: ["ai-chatbot", "gaming", "creative"]
  notSuitableFor: ["finance", "healthcare", "enterprise"]
  implementation: |
    bg-white/10 backdrop-blur-lg
    border border-white/20
    Works best on colorful/image backgrounds
  overuseWarning: "Performance issues on older devices"

dark-mode-first:
  name: "Dark Mode as Default"
  suitableFor: ["gaming", "creative", "ai-chatbot"]
  notSuitableFor: ["healthcare", "food-restaurant", "education"]
  implementation: |
    Start with dark palette
    bg-slate-900/950
    Light text, subtle surfaces
  overuseWarning: "Not appropriate for all audiences"

micro-interactions:
  name: "Micro-interactions"
  suitableFor: ["ALL except enterprise"]
  notSuitableFor: ["enterprise (minimal only)"]
  implementation: |
    Button press feedback
    Form field focus effects
    Loading state animations
    Success/error feedback
  overuseWarning: "Too many = distracting"

variable-fonts:
  name: "Variable Fonts"
  suitableFor: ["creative", "editorial", "education"]
  notSuitableFor: ["enterprise", "finance"]
  implementation: |
    Font-weight animations
    Responsive typography
    Custom font-variation-settings
  overuseWarning: "Larger file sizes"

scroll-animations:
  name: "Scroll-Triggered Animations"
  suitableFor: ["creative", "ecommerce", "travel"]
  notSuitableFor: ["saas-dashboard", "enterprise", "healthcare"]
  implementation: |
    Framer Motion useInView
    Subtle fade-in, slide-up
    Parallax (sparingly)
  overuseWarning: "Annoying if overdone"
```

### Emerging Trends (Watch List)

```yaml
# These are emerging - use with caution

ai-generated-art:
  status: "emerging"
  note: "Custom AI art for illustrations - but make it unique"
  
spatial-design:
  status: "emerging"  
  note: "3D elements, depth - for Vision Pro ready"
  
voice-ui:
  status: "emerging"
  note: "Voice commands integration"
```

---

## 🌐 Design Inspiration Sources

### By Business Type

```yaml
saas-dashboard:
  sources:
    - "Linear.app"
    - "Notion.so"
    - "Vercel Dashboard"
    - "Stripe Dashboard"
  why: "Clean, functional, developer-friendly"

ecommerce:
  sources:
    - "Shopify themes"
    - "Apple Store"
    - "Nike.com"
    - "Glossier"
  why: "Conversion-focused, visual-heavy"

ai-chatbot:
  sources:
    - "Claude.ai" # But differentiate!
    - "Perplexity.ai"
    - "ChatGPT"
    - "Character.ai"
  why: "But AVOID copying purple-blue gradient!"

food-restaurant:
  sources:
    - "Uber Eats"
    - "DoorDash"
    - "OpenTable"
    - "Resy"
  why: "Appetite-inducing, image-focused"

finance:
  sources:
    - "Wise (TransferWise)"
    - "Robinhood"
    - "Mercury Bank"
    - "Ramp"
  why: "Trust, clarity, security-feeling"

healthcare:
  sources:
    - "Oscar Health"
    - "One Medical"
    - "Headspace"
    - "Calm"
  why: "Calming, accessible, trustworthy"

creative:
  sources:
    - "Awwwards winners"
    - "Behance"
    - "Dribbble"
    - "Minimal Gallery"
  why: "Break conventions, be unique"

gaming:
  sources:
    - "Discord"
    - "Steam"
    - "Twitch"
    - "Epic Games Store"
  why: "Dark theme, vibrant, immersive"

education:
  sources:
    - "Duolingo"
    - "Khan Academy"
    - "Coursera"
    - "Skillshare"
  why: "Engaging, progress-focused"

travel:
  sources:
    - "Airbnb"
    - "Booking.com"
    - "Expedia"
    - "Google Travel"
  why: "Dreamy imagery, trust signals"
```

---

## 🔌 Agent Integration Protocol (MANDATORY!)

### For Vibe Orchestrator (New Projects)

```markdown
## REQUIRED: Design Profile Selection

BEFORE spawning UI Builder, MUST:

1. Extract keywords from user request
2. Match to design profile using registry
3. Store selected profile in memory

Example:
User: "สร้างแอพขายกาแฟ"
Keywords: ["ขาย", "กาแฟ"]
Matches: "food-restaurant" (keywords: food, cafe)
Action: Load food-restaurant profile

Tell UI Builder:
"Apply design profile: food-restaurant
- Primary: #DC2626 (red - appetite)
- Typography: Playfair Display + Source Sans Pro
- Layout: top-nav
- Hero: background (food imagery)
- Cards: elevated
- Emotion: Warm, Appetizing, Welcoming"
```

### For Design Reviewer (Polish)

```markdown
## REQUIRED: Profile-Based Review

1. Read project's design profile from memory
   - If none set, detect from project content
   
2. Compare current design against profile
   - Colors match profile?
   - Typography matches profile?
   - Layout follows profile patterns?
   - Anti-patterns avoided?

3. Fix deviations
   - Align to profile standards
   - Apply profile's anti-pattern fixes

4. Run Anti-AI checklist
   - All 3 levels (Obvious, Subtle, Deep)
```

### For UI Builder (Components)

```markdown
## REQUIRED: Profile-Consistent Components

1. Check memory for project's design profile
   - If exists, use profile tokens
   - If not, use saas-dashboard default

2. Apply profile tokens to new components
   - Colors from profile.tokens.colors
   - Typography from profile.tokens.typography
   - Borders from profile.tokens.borders
   - Shadows from profile.tokens.shadows

3. Follow profile patterns
   - Card style from profile.patterns.cards
   - Button style from profile.patterns.buttons
   - Layout from profile.patterns.layout
```

---

## 📊 Design Decision Matrix

### Quick Selection Guide

| User Request | Detected Keywords | Profile | Key Design Choices |
|--------------|-------------------|---------|-------------------|
| "expense tracker" | tracker, budget | finance | Navy+Teal, IBM Plex, numbers prominent |
| "coffee shop menu" | menu, cafe | food-restaurant | Red+Amber, Playfair, food imagery |
| "AI assistant" | ai, assistant | ai-chatbot | Teal (NOT purple!), friendly rounded |
| "online course" | course, learn | education | Indigo+Amber, progress bars, gamification |
| "hotel booking" | hotel, booking | travel | Cyan+Orange, big images, search prominent |
| "property listing" | property, rent | real-estate | Navy+Gold, premium feel, map integration |
| "gaming platform" | game, play | gaming | Dark mode, violet+emerald, glow effects |
| "social app" | social, share | social-media | Blue+Pink, feed layout, instant feedback |
| "CRM system" | crm, b2b | enterprise | Blue, high density, professional |
| "fitness app" | fitness, workout | healthcare | Sky+Emerald, calming, accessible |

---

## ✅ Pre-Delivery Design Checklist

### Level 1: Profile Alignment
- [ ] Correct profile selected for business type?
- [ ] Colors match profile palette?
- [ ] Typography matches profile fonts?
- [ ] Layout follows profile patterns?

### Level 2: Anti-AI Verification
- [ ] No purple-blue gradients (unless gaming/creative)?
- [ ] Border-radius varies by element type?
- [ ] Shadows have purpose/hierarchy?
- [ ] No emoji in headings?
- [ ] No pure black text?

### Level 3: Quality Assurance
- [ ] Would a human designer approve?
- [ ] Feels like a real product?
- [ ] User focuses on content, not design?
- [ ] Consistent across all pages?

---

*Design Mastery Skill v2.1.0 - World-Class Extensible Design System with Extended Registry*
