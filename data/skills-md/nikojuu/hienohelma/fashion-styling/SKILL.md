---
name: fashion-styling
description: Complete styling guide for women's fashion boutique theme. Apply phase by phase for complete restyling. Modern editorial aesthetic with elegant typography, geometric accents, and sophisticated animations. (project)
invocation: user
---

# Fashion Boutique Theme

**Brand Voice:** Modern, sophisticated, confident, feminine, editorial
**Target Feel:** High-end fashion magazine meets accessible boutique

---

## Usage

Apply phases in order:
1. "Apply fashion-styling phase 1" → Foundation
2. "Apply fashion-styling phase 2" → Layout
3. "Apply fashion-styling phase 3" → Homepage & Products
4. "Apply fashion-styling phase 4" → Cart, Checkout & Auth
5. "Apply fashion-styling phase 5" → Dashboard & Static Pages

Clear context between phases if needed.

---

# Phase 1: Foundation

**Files:**
```
src/app/globals.css
src/lib/fonts.ts
tailwind.config.ts
```

## Colors (globals.css)

Add these CSS variables:

| Name | HSL | Role |
|------|-----|------|
| blush | 350 60% 75% | Primary accent |
| champagne-gold | 45 50% 70% | Secondary accent |
| soft-ivory | 40 30% 98% | Background |
| pearl | 40 20% 96% | Card backgrounds |
| midnight | 220 25% 15% | Text, dark sections |
| whisper-pink | 350 40% 95% | Subtle backgrounds |
| wine | 350 50% 35% | Sale, errors |
| stone | 30 10% 50% | Secondary text |

## Fonts (fonts.ts)

| Role | Font | Usage |
|------|------|-------|
| Primary | Cormorant Garamond | Headings, titles |
| Secondary | Inter | Body, buttons |

## Tailwind Config

- Map all color variables
- Set border-radius to 2px (minimal rounding)
- Add font-primary and font-secondary

## CSS Utilities (globals.css)

```css
.text-gradient-fashion {
  background: linear-gradient(135deg, hsl(350 60% 65%), hsl(45 50% 70%), hsl(350 60% 75%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.shimmer-fashion {
  background: linear-gradient(110deg, transparent 20%, hsl(45 60% 85% / 0.3) 40%, hsl(350 60% 90% / 0.4) 50%, hsl(45 60% 85% / 0.3) 60%, transparent 80%);
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}
```

---

# Phase 2: Layout & Navigation

**Files:**
```
src/components/Navigation/StickyNavbar.tsx
src/components/Navigation/Navbar.tsx
src/components/Navigation/NavbarLinks.tsx
src/components/Navigation/MobileLinks.tsx
src/components/Navigation/CustomerDropdown.tsx
src/components/Footer.tsx
src/app/(auth)/(dashboard)/layout.tsx
```

## Styling Rules

**Backgrounds:** `bg-soft-ivory` or `bg-pearl`
**Text:** `text-midnight` headings, `text-midnight/70` body
**Borders:** `border-blush/20` or `border-stone/20`
**Hovers:** Transition to `blush` or `champagne-gold`

## Navigation Pattern

```tsx
{/* Link with underline animation */}
<a className="relative font-secondary text-sm text-midnight hover:text-blush transition-colors">
  Link Text
  <span className="absolute bottom-0 left-1/2 w-0 h-[1px] bg-blush transition-all duration-300 group-hover:w-full group-hover:left-0" />
</a>
```

## Footer Pattern

```tsx
<footer className="bg-soft-ivory border-t border-blush/20">
  <div className="h-[1px] bg-gradient-to-r from-transparent via-blush/30 to-transparent" />
  {/* Content */}
</footer>
```

## Dashboard Sidebar

```tsx
<aside className="bg-pearl border border-blush/10 p-6">
  <h2 className="font-primary text-xl text-midnight mb-4">My Account</h2>
  <div className="h-[1px] bg-gradient-to-r from-blush/40 to-transparent mb-4" />
  {/* Nav links */}
</aside>
```

---

# Phase 3: Homepage & Products

**Files:**
```
src/app/(storefront)/page.tsx
src/components/Hero.tsx
src/components/subtitle.tsx
src/components/Homepage/CategorySection.tsx
src/components/Homepage/AboutMeSection.tsx
src/components/Product/ProductCarousel.tsx
src/components/ProductCard.tsx
src/components/PriceDisplay.tsx
src/components/ImageSlider.tsx
src/components/imageSliderWithZoom.tsx
src/components/Product/ProductDetail.tsx
src/components/Product/WishlistButton.tsx
src/components/Product/Breadcrumbs.tsx
src/components/Product/SortOptions.tsx
src/components/Product/Pagination.tsx
src/app/(storefront)/products/[...slug]/page.tsx
src/app/(storefront)/product/[slug]/page.tsx
```

## Section Header Pattern

```tsx
<div className="flex items-center justify-center gap-4 mb-6">
  <div className="w-16 h-[1px] bg-gradient-to-r from-transparent to-blush/60" />
  <div className="w-2 h-2 rounded-full border border-blush/60" />
  <div className="w-16 h-[1px] bg-gradient-to-l from-transparent to-blush/60" />
</div>
<h2 className="text-3xl md:text-4xl font-primary text-midnight text-center">
  Section Title
</h2>
```

## Hero Pattern

```tsx
<section className="relative min-h-[70vh] bg-soft-ivory">
  {/* Image with overlay */}
  <div className="absolute inset-0 bg-gradient-to-t from-midnight/40 via-transparent to-transparent" />

  <div className="relative z-10">
    <h1 className="text-5xl md:text-7xl font-primary text-soft-ivory tracking-tight">
      Headline
    </h1>
    <button className="px-8 py-4 bg-soft-ivory text-midnight font-secondary text-sm tracking-wider uppercase hover:bg-blush transition-colors">
      Shop Now
    </button>
  </div>
</section>
```

## Product Card Pattern

```tsx
<div className="group relative bg-soft-ivory overflow-hidden">
  {/* Image */}
  <div className="aspect-[3/4] overflow-hidden">
    <img className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
  </div>

  {/* Sale badge */}
  <span className="absolute top-3 left-3 px-2 py-1 bg-wine text-soft-ivory text-xs font-secondary uppercase">
    -30%
  </span>

  {/* Wishlist button */}
  <button className="absolute top-3 right-3 p-2 bg-soft-ivory/80 text-midnight hover:text-blush transition-colors">
    <Heart className="w-5 h-5" />
  </button>

  {/* Content */}
  <div className="p-4">
    <h3 className="font-primary text-lg text-midnight">Product Name</h3>
    <p className="text-sm font-secondary text-stone">Brand</p>
    <div className="mt-2 flex items-center gap-2">
      <span className="font-secondary text-midnight">€99.00</span>
      <span className="font-secondary text-stone line-through text-sm">€129.00</span>
    </div>
  </div>
</div>
```

## Category Card Pattern

```tsx
<a className="group relative aspect-[3/4] overflow-hidden">
  <img className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
  <div className="absolute inset-0 bg-gradient-to-t from-midnight/70 via-midnight/20 to-transparent" />
  <div className="absolute bottom-6 left-6">
    <h3 className="font-primary text-2xl text-soft-ivory">Category</h3>
    <span className="text-sm font-secondary text-soft-ivory/70">24 products</span>
  </div>
</a>
```

---

# Phase 4: Cart, Checkout & Auth

**Files:**
```
src/app/(storefront)/cart/page.tsx
src/components/Cart/Cart.tsx
src/components/Cart/CartItem.tsx
src/components/Cart/CartPage.tsx
src/components/Cart/AddToCartButton.tsx
src/components/Cart/CheckoutButton.tsx
src/components/Cart/CampaignAddedCartItems.tsx
src/components/Checkout/CheckoutSteps.tsx
src/components/Checkout/CustomerDataForm.tsx
src/components/Checkout/SelectShipmentMethod.tsx
src/components/Checkout/StripeCheckoutPage.tsx
src/components/Checkout/PaytrailCheckoutPage.tsx
src/components/Checkout/PaytrailPaymentSelection.tsx
src/app/(storefront)/payment/success/[orderId]/page.tsx
src/app/(auth)/login/page.tsx
src/app/(auth)/register/page.tsx
src/components/Auth/Loginform.tsx
src/components/Auth/RegisterForm.tsx
src/components/Auth/ForgotPasswordForm.tsx
src/components/Auth/ResetPasswordForm.tsx
```

## Button Patterns

```tsx
{/* Primary CTA */}
<button className="w-full px-8 py-4 bg-midnight text-soft-ivory font-secondary text-sm tracking-wider uppercase transition-all duration-300 hover:bg-blush hover:text-midnight">
  Add to Cart
</button>

{/* Secondary */}
<button className="px-8 py-4 border border-midnight/30 text-midnight font-secondary text-sm tracking-wider uppercase hover:border-blush hover:bg-blush/10 transition-all">
  Continue Shopping
</button>
```

## Form Input Pattern

```tsx
<div className="space-y-2">
  <label className="text-sm font-secondary text-midnight">Email</label>
  <input className="w-full px-4 py-3 bg-pearl border border-stone/20 text-midnight placeholder:text-stone/50 focus:outline-none focus:ring-2 focus:ring-blush/50 transition-all" />
</div>
```

## Card with Corner Accents

```tsx
<div className="group relative bg-soft-ivory p-6">
  {/* Border */}
  <div className="absolute inset-0 border border-blush/10 pointer-events-none group-hover:border-blush/25 transition-colors" />

  {/* Corner accents */}
  <div className="absolute top-0 left-0 w-4 h-4 border-l border-t border-blush/20 group-hover:w-6 group-hover:h-6 transition-all duration-300" />
  <div className="absolute top-0 right-0 w-4 h-4 border-r border-t border-blush/20 group-hover:w-6 group-hover:h-6 transition-all duration-300" />
  <div className="absolute bottom-0 left-0 w-4 h-4 border-l border-b border-blush/20 group-hover:w-6 group-hover:h-6 transition-all duration-300" />
  <div className="absolute bottom-0 right-0 w-4 h-4 border-r border-b border-blush/20 group-hover:w-6 group-hover:h-6 transition-all duration-300" />

  {/* Content */}
</div>
```

## Checkout Steps Pattern

```tsx
<div className="flex items-center justify-center gap-4">
  {/* Completed step */}
  <div className="w-8 h-8 rounded-full bg-blush text-midnight flex items-center justify-center">
    <Check className="w-4 h-4" />
  </div>

  {/* Line */}
  <div className="w-12 h-[1px] bg-blush/50" />

  {/* Current step */}
  <div className="w-8 h-8 rounded-full border-2 border-blush text-midnight flex items-center justify-center font-secondary text-sm">
    2
  </div>

  {/* Line */}
  <div className="w-12 h-[1px] bg-stone/30" />

  {/* Future step */}
  <div className="w-8 h-8 rounded-full border border-stone/30 text-stone flex items-center justify-center font-secondary text-sm">
    3
  </div>
</div>
```

## Toast Styling

```tsx
{/* Success */}
className="bg-blush/10 border border-blush/30 text-midnight"

{/* Error */}
className="bg-wine/10 border border-wine/30 text-wine"
```

---

# Phase 5: Dashboard & Static Pages

**Files:**
```
src/app/(auth)/(dashboard)/mypage/page.tsx
src/app/(auth)/(dashboard)/myorders/page.tsx
src/app/(auth)/(dashboard)/mywishlist/page.tsx
src/app/(auth)/(dashboard)/myinfo/page.tsx
src/components/CustomerDashboard/EditCustomerForm.tsx
src/app/(storefront)/about/page.tsx
src/components/Aboutpage/AboutHero.tsx
src/components/Aboutpage/AboutBlock.tsx
src/components/Aboutpage/AboutCTA.tsx
src/app/(storefront)/contact/page.tsx
src/components/Contactpage/ContactForm.tsx
src/app/(storefront)/privacy-policy/page.tsx
src/app/(storefront)/terms/page.tsx
src/app/(storefront)/gallery/page.tsx
```

## Page Header Pattern

```tsx
<div className="mb-8">
  <div className="flex items-center gap-3 mb-2">
    <div className="w-2 h-2 rounded-full border border-blush/60" />
    <h1 className="text-2xl md:text-3xl font-primary text-midnight">Page Title</h1>
  </div>
  <p className="font-secondary text-midnight/60 ml-5">Page description</p>
</div>
```

## Status Badges

```tsx
{/* Pending */}
<span className="px-3 py-1 bg-champagne-gold/20 text-midnight border border-champagne-gold/40 text-xs font-secondary uppercase">
  Pending
</span>

{/* Paid/Success */}
<span className="px-3 py-1 bg-blush/20 text-midnight border border-blush/40 text-xs font-secondary uppercase">
  Paid
</span>

{/* Shipped */}
<span className="px-3 py-1 bg-blush/30 text-midnight border border-blush/50 text-xs font-secondary uppercase">
  Shipped
</span>
```

## Empty State Pattern

```tsx
<div className="relative bg-soft-ivory p-12 text-center">
  {/* Border */}
  <div className="absolute inset-0 border border-blush/10 pointer-events-none" />

  {/* Corner accents */}
  <div className="absolute top-0 left-0 w-8 h-8 border-l border-t border-blush/30" />
  <div className="absolute top-0 right-0 w-8 h-8 border-r border-t border-blush/30" />
  <div className="absolute bottom-0 left-0 w-8 h-8 border-l border-b border-blush/30" />
  <div className="absolute bottom-0 right-0 w-8 h-8 border-r border-b border-blush/30" />

  <Icon className="w-16 h-16 text-midnight/20 mx-auto mb-6" />
  <h3 className="text-xl font-primary text-midnight mb-3">No items yet</h3>
  <p className="text-sm font-secondary text-midnight/60 mb-6">Description text</p>
  <a href="/products" className="inline-flex px-8 py-3 bg-midnight text-soft-ivory font-secondary text-sm tracking-wider uppercase hover:bg-blush hover:text-midnight transition-all">
    Start Shopping
  </a>
</div>
```

## About Page Blocks

```tsx
{/* Alternating layout */}
<div className="grid md:grid-cols-2 gap-12 items-center">
  <div className={reverse ? "md:order-2" : ""}>
    <img className="w-full aspect-[4/5] object-cover" />
  </div>
  <div>
    <span className="text-xs tracking-[0.2em] uppercase font-secondary text-stone">Our Story</span>
    <h2 className="mt-2 text-3xl font-primary text-midnight">Headline</h2>
    <div className="mt-2 w-12 h-[1px] bg-gradient-to-r from-blush to-transparent" />
    <p className="mt-6 font-secondary text-midnight/70 leading-relaxed">Content</p>
  </div>
</div>
```

---

# Quick Reference

## Typography
```tsx
font-primary    → Headings (Cormorant Garamond)
font-secondary  → Body/buttons (Inter)

text-midnight        → Dark text
text-midnight/70     → Body text
text-stone           → Muted text
text-soft-ivory      → Light text (on dark bg)
```

## Backgrounds
```tsx
bg-soft-ivory   → Main background
bg-pearl        → Cards, sections
bg-midnight     → Dark sections
bg-blush/10     → Subtle highlight
```

## Accents
```tsx
border-blush/20     → Subtle borders
border-blush/40     → Corner accents
bg-blush            → Hover states
bg-wine             → Sale badges
bg-champagne-gold   → Premium accents
```

## Decorative
```tsx
{/* Circle */}
<div className="w-2 h-2 rounded-full border border-blush/60" />

{/* Gradient line */}
<div className="h-[1px] bg-gradient-to-r from-blush/40 to-transparent" />

{/* Center line */}
<div className="h-[1px] bg-gradient-to-r from-transparent via-blush/30 to-transparent" />
```

---

## Checklist

- [ ] Phase 1: Foundation (3 files)
- [ ] Phase 2: Layout & Navigation (7 files)
- [ ] Phase 3: Homepage & Products (17 files)
- [ ] Phase 4: Cart, Checkout & Auth (20 files)
- [ ] Phase 5: Dashboard & Static (14 files)
