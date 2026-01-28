---
name: pupun-korvat-styling
description: Complete styling guide for Pupun Korvat jewelry theme. Apply phase by phase for complete restyling. Elegant artisan aesthetic with rose gold accents, corner decorations, and shimmer effects.
invocation: user
---

# Pupun Korvat - Artisan Jewelry Theme

**Brand Voice:** Elegant, artisan, warm, personal, Finnish craftsmanship
**Target Feel:** Luxury boutique meets handmade authenticity

---

## Phase 1: Foundation

### 1.1 Colors (`src/app/globals.css`)

| Role | Name | HSL | Usage |
|------|------|-----|-------|
| primary-accent | rose-gold | 15 45% 65% | Buttons, links, borders, highlights |
| secondary-accent | champagne | 38 45% 78% | Hover states, warm highlights |
| background | warm-white | 30 33% 98% | Main background |
| card-bg | cream | 35 40% 95% | Cards, sections |
| text | charcoal | 20 15% 18% | Headings, dark sections |
| accent-subtle | soft-blush | 350 35% 90% | Subtle accents, icon backgrounds |
| accent-dark | deep-burgundy | 350 45% 30% | Sale badges, alerts, emphasis |

#### Color Usage Rules
1. **Backgrounds:** Use `warm-white` as primary, `cream` for section variation
2. **Text:** Use `charcoal` for headings, `charcoal/70` or `charcoal/60` for body
3. **Accents:** Use `rose-gold` for interactive elements, borders, highlights
4. **Sales/Emphasis:** Use `deep-burgundy` for sale badges and urgent CTAs
5. **Hover States:** Transition to `rose-gold` or `champagne` on hover

### 1.2 Fonts (`src/lib/fonts.ts`)

| Role | Font | Usage |
|------|------|-------|
| Primary | Playfair Display | Headings, titles, brand name, prices |
| Secondary | Source Sans 3 | Body text, descriptions, buttons, labels |

### 1.3 Tailwind Config (`tailwind.config.ts`)
- Border radius: `0px` (sharp corners)
- All color variables mapped

### 1.4 Gradient Utilities (`globals.css`)

```css
.text-gradient-gold {
  background: linear-gradient(135deg, hsl(38 50% 55%), hsl(15 45% 65%), hsl(38 50% 55%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.shimmer-gold {
  background: linear-gradient(
    110deg,
    transparent 20%,
    hsl(38 60% 80% / 0.4) 40%,
    hsl(38 60% 90% / 0.6) 50%,
    hsl(38 60% 80% / 0.4) 60%,
    transparent 80%
  );
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}
```

---

## Phase 2: Layout Components

### 2.1 StickyNavbar (`src/components/Navigation/StickyNavbar.tsx`)
- Fixed header container
- Logo (hidden mobile, visible md+)
- Campaign banner (animated, scroll-aware)
- Navigation content slot
```tsx
```

### 2.2 Navbar (`src/components/Navigation/Navbar.tsx`)
- Mobile menu trigger (MobileLinks)
- Desktop navigation links (NavbarLinks)
- Customer dropdown (auth menu)
- Shopping cart icon
```tsx
```

### 2.3 NavbarLinks (`src/components/Navigation/NavbarLinks.tsx`)
- Products dropdown with categories tree
- About, Gallery, Contact links
- Decorative gradient underlines on hover
```tsx
```

### 2.4 DesktopDropdown (`src/components/Navigation/DesktopDropdown.tsx`)
- Category link with hover state
- Chevron icon toggle
- Recursive submenu dropdown
- Decorative gradient lines
```tsx
```

### 2.5 MobileLinks (`src/components/Navigation/MobileLinks.tsx`)
- Menu button trigger (hamburger)
- Sheet/Drawer container
- Logo header
- Products section with expand/collapse
- Expandable category list (MobileCategory recursive)
- About, Gallery, Contact links
- Decorative footer divider
```tsx
```

### 2.6 MobileCategory (`src/components/Navigation/MobileCategory.tsx`)
- Category link
- Expand/collapse button (Plus/Minus icons)
- Nested children with indentation
- Recursive structure
```tsx
```

### 2.7 CustomerDropdown (`src/components/Navigation/CustomerDropdown.tsx`)
- User icon button trigger
- Dropdown menu (authenticated/unauthenticated states)
- Welcome message, My Page link, Logout button
- Login/Register links
```tsx
```

### 2.8 Footer (`src/components/Footer.tsx`)
- Decorative gradient top line
- Corner accents (4 corners, hidden mobile)
- Floating diamonds (lg+ only)
- Grid: Logo, Navigation links, Social media
- Decorative divider with diamonds
- Copyright text
```tsx
```

### 2.9 DashboardSidebar (`src/app/(auth)/(dashboard)/layout.tsx`)
- Sidebar card with border frame and corner accents
- "My Account" header with diamond decoration
- Navigation menu (Overview, Orders, My Info, Wishlist)
- Logout link with danger styling
```tsx
```

---

## Phase 3: Homepage (`src/app/(storefront)/page.tsx`)

### 3.1 Hero (`src/components/Hero.tsx`)
- Decorative corner accents (4 corners)
- Background image with parallax scrolling
- Overlay gradients (horizontal + vertical)
- Floating animated diamond shapes (5 elements)
- Main title with gold gradient
- Subtitle text
- CTA buttons (primary filled, secondary bordered)
- Scroll indicator
```tsx
```

### 3.2 Subtitle (`src/components/subtitle.tsx`)
- Decorative element (5 diamonds + gradient lines)
- Main h2 title
- Optional description
- Decorative line below (scales in on view)
- Dark mode variant support
```tsx
```

### 3.3 CategorySection (`src/components/Homepage/CategorySection.tsx`)
- Background gradient
- Grid (1 col mobile, 3 col desktop)
- Category cards with:
  - Outer frame border
  - Corner accents (4 corners, expand on hover)
  - Image container (aspect 3:4)
  - Gradient overlays (rose-gold + charcoal)
  - Shimmer effect on hover
  - Title, description, explore link
  - Decorative diamond
```tsx
```

### 3.4 AboutMeSection (`src/components/Homepage/AboutMeSection.tsx`)
- Background decorations (rotated squares, diamonds)
- Image column with decorative frame
- Corner accents on image
- Floating accent card (100% stat)
- Content: label, heading with gradient, descriptions
- Features grid (3 columns with icons)
- CTA button
```tsx
```

### 3.5 LatestProducts (inline in page.tsx)
- Gradient background
- Subtitle component
- Desktop grid (2 col mobile, 3 col desktop)
- ProductCard components
- View all link with arrow
- Mobile: ProductCarousel
```tsx
```

### 3.6 FinalCTA (inline in page.tsx)
- Decorative border frame
- Corner accents (4 corners)
- Floating diamond decorations
- Decorative header with diamonds
- Heading, description
- CTA button group
```tsx
```

### 3.7 ProductCarousel (`src/components/Product/ProductCarousel.tsx`)
- Carousel wrapper (mobile-only)
- ProductCard items
- Loop functionality
```tsx
```

---

## Phase 4: Product Pages

### 4.1 ProductsPage (`src/app/(storefront)/products/[...slug]/page.tsx`)
- Breadcrumb navigation
- Sort options
- Product grid (2 col mobile, 3 col desktop)
- Pagination
- Empty state card with corner accents and diamonds
```tsx
```

### 4.2 ProductCard (`src/components/ProductCard.tsx`)
- Card frame border (transitions on hover)
- Corner accents (4, expand on hover)
- Image with aspect-square
- Overlay gradient on hover
- Sale badge (top-left, burgundy)
- Share button (top-right, appears on hover)
- View product indicator (slides up on hover)
- Product name (clamped 2 lines)
- Price display (sale + normal)
- Availability indicator (dot + text)
- Decorative gradient line (expands on hover)
```tsx
```

### 4.3 LoadingProductCard (`src/components/ProductCard.tsx`)
- Card frame with corner accents
- Image skeleton with shimmer-gold
- Content skeleton (3 lines)
```tsx
```

### 4.4 ProductDetail (`src/components/Product/ProductDetail.tsx`)
- Breadcrumbs navigation
- Image gallery (desktop: ImageSliderWithZoom, mobile: ImageSlider)
- Product name (h1)
- Decorative gradient line
- Price section
- Description
- Stock status indicator
- Variations section (if applicable)
- Wishlist + Add to cart buttons
```tsx
```

### 4.5 ImageSliderWithZoom (`src/components/imageSliderWithZoom.tsx`)
- Main image container with corner accents
- Zoom cursor + zoom indicator
- Navigation buttons (chevrons)
- Zoom panel (400x400, 2.5x scale)
- Thumbnails grid (5 columns)
- Selected thumbnail rose-gold ring
```tsx
```

### 4.6 ImageSlider (`src/components/ImageSlider.tsx`)
- Main image container with corner accents
- Navigation buttons
- Thumbnails grid (3 columns)
- Selected thumbnail rose-gold ring
```tsx
```

### 4.7 SortOptions (`src/components/Product/SortOptions.tsx`)
- Label "Järjestä:"
- Sort buttons (newest, price low/high, popular)
- Active state: rose-gold border + background
```tsx
```

### 4.8 PaginationComponent (`src/components/Product/Pagination.tsx`)
- Previous/Next buttons
- Page links with ellipsis
- Hidden on mobile
```tsx
```

### 4.9 Breadcrumbs (`src/components/Product/Breadcrumbs.tsx`)
- Products link
- Category breadcrumb trail
- Current item (not a link)
- ChevronRight separators
```tsx
```

### 4.10 PriceDisplay (`src/components/PriceDisplay.tsx`)
- Sale percentage badge (red)
- Original price (strikethrough, gray)
- Current/sale price (bold, large)
```tsx
```

### 4.11 WishlistButton (`src/components/Product/WishlistButton.tsx`)
- Button with outline variant
- Heart icon
- Loading spinner
- Toast notifications
```tsx
```

---

## Phase 5: Category Pages

### 5.1 CategoryListing
- Uses ProductsPage with category filter
- Breadcrumbs show category hierarchy
```tsx
```

### 5.2 CategoryCard
- Part of CategorySection (see Phase 3.3)
```tsx
```

---

## Phase 6: Cart & Checkout

### 6.1 CartPage (`src/app/(storefront)/cart/page.tsx`)
- Cart items list (left column)
- Order summary sidebar (right column)
- Checkout validation banner
- Empty cart state with decorative elements
- Campaign savings display
- Free shipping badge
- Checkout button
- Continue shopping link
```tsx
```

### 6.2 CartSheet (`src/components/Cart/Cart.tsx`)
- Sheet trigger with item count badge
- Cart items scrollable list
- Footer with totals
- Campaign savings
- Free shipping status
- Empty cart state with image
- Checkout button
```tsx
```

### 6.3 CartItem (`src/components/Cart/CartItem.tsx`)
- Product image thumbnail
- Product name and options
- Campaign info (paid vs free)
- Price display with sale badge
- Quantity increment/decrement
- Remove button
```tsx
```

### 6.4 CampaignAddedCartItems (`src/components/Cart/CampaignAddedCartItems.tsx`)
- Product image with hover zoom
- Product name as link
- Variation options
- Price display
- Quantity controls
- Campaign discount banner
- Remove button
```tsx
```

### 6.5 AddToCartButton (`src/components/Cart/AddToCartButton.tsx`)
- Button states (Add, Added, Out of Stock)
- Loading state
- Disabled when out of stock
```tsx
```

### 6.6 CheckoutButton (`src/components/Cart/CheckoutButton.tsx`)
- Submit button with pending state
- Loading spinner
- Disabled styling
```tsx
```

### 6.7 CheckoutSteps (`src/components/Checkout/CheckoutSteps.tsx`)
- Progress bar (background + active line)
- Step circles (completed, current, upcoming)
- Step titles
- Checkmark for completed
- Diamond accent on current
```tsx
```

### 6.8 CustomerDataForm (`src/components/Checkout/CustomerDataForm.tsx`)
- Form card with border frame + corner accents
- Header with diamond decoration
- Name fields (2-column desktop)
- Email, address, postal/city, phone fields
- Decorative divider
- Submit button
- Field error messages
```tsx
```

### 6.9 SelectShipmentMethod (`src/components/Checkout/SelectShipmentMethod.tsx`)
- Header with diamond elements
- Home delivery section
- Radio group for shipment selection
- Parcel locker section with grid
- Shipment cards with corner accents
- Parcel location cards with carrier logo
- Show more/less button
- Free shipping display
```tsx
```

### 6.10 StripeCheckoutPage (`src/components/Checkout/StripeCheckoutPage.tsx`)
- Checkout steps (3 steps)
- Step 1: CustomerDataForm
- Step 2: SelectShipmentMethod
- Back button, Continue button
```tsx
```

### 6.11 PaytrailCheckoutPage (`src/components/Checkout/PaytrailCheckoutPage.tsx`)
- Checkout steps (3 steps)
- Step 1: CustomerDataForm
- Step 2: SelectShipmentMethod
- Step 3: PaymentSelection
- Back/Continue buttons
```tsx
```

### 6.12 PaytrailPaymentSelection (`src/components/Checkout/PaytrailPaymentSelection.tsx`)
- Header with diamond elements
- Payment groups display
- Group cards with corner accents
- Provider buttons grid (2-5 columns)
- Provider logos with hover effects
```tsx
```

---

## Phase 7: Auth Pages

### 7.1 LoginForm (`src/components/Auth/Loginform.tsx`)
- Page title subtitle
- Form card with border frame + corner accents
- Header with diamond decoration
- Email + password fields
- Show/hide password toggle
- Error/success message banners
- Forgot password link
- Decorative divider
- Login button
- Resend verification button (conditional)
```tsx
```

### 7.2 RegisterForm (`src/components/Auth/RegisterForm.tsx`)
- Page title subtitle
- Form card with border frame + corner accents
- Header with diamond decoration
- Name fields (2-column desktop)
- Email + password fields
- Show/hide password toggle
- Decorative divider
- Register button
- Field error messages
```tsx
```

### 7.3 ForgotPasswordForm (`src/components/Auth/ForgotPasswordForm.tsx`)
- Page title subtitle
- Form card with border frame + corner accents
- Header with diamond decoration
- Description text
- Email field
- Error/success banners
- Decorative divider
- Submit button
- Back to login link
```tsx
```

### 7.4 ResetPasswordForm (`src/components/Auth/ResetPasswordForm.tsx`)
- Page title subtitle
- Form card with border frame + corner accents
- Header with diamond decoration
- Description text
- Password + confirm password fields
- Show/hide toggles
- Error/success banners
- Decorative divider
- Submit button
```tsx
```

---

## Phase 8: Customer Dashboard

### 8.1 MyPage (`src/app/(auth)/(dashboard)/mypage/page.tsx`)
- Header with diamond decoration + subtitle
- Welcome card with border frame + corner accents
- Welcome message with user's name
- 3-column feature cards grid:
  - My Orders
  - My Info
  - Newsletter
- Cards with expandable corner accents on hover
```tsx
```

### 8.2 MyOrdersPage (`src/app/(auth)/(dashboard)/myorders/page.tsx`)
- Header with diamond decoration + subtitle
- Order count display
- Empty state card (icon, message, browse link)
- Order cards with:
  - Order number + date
  - Status badge (color-coded + icon)
  - Total amount
  - Order items list (image, name, variation, qty, price)
  - Tracking number
- Corner accents on hover
- Status indicators: Pending, Paid, Shipped, Completed, Refunded
```tsx
```

### 8.3 EditCustomerForm (`src/components/CustomerDashboard/EditCustomerForm.tsx`)
- Header with diamond decoration + subtitle
- Profile form card with border + corner accents
- User icon header
- Name fields (2-column desktop)
- Email field
- Decorative divider
- Save button
- Success/error banners
- Account deletion section (danger styling):
  - Red border + corner accents
  - Warning list
  - Delete button
  - Confirmation dialog
```tsx
```

### 8.4 WishlistPage (`src/app/(auth)/(dashboard)/mywishlist/page.tsx`)
- Header with diamond decoration + subtitle
- Item count display
- Empty state card (heart icon, message, browse link)
- Wishlist items:
  - Product image thumbnail
  - Product name as link
  - Variation options
  - Price + sale badge
  - Added date
  - View product button
  - Delete button
- Corner accents on hover
```tsx
```

---

## Phase 9: Static Pages

### 9.1 AboutPage (`src/app/(storefront)/about/page.tsx`)
- AboutHero
- AboutBlock x3 (alternating)
- AboutCTA
```tsx
```

### 9.2 AboutHero (`src/components/Aboutpage/AboutHero.tsx`)
- Background decorative diamonds + gradient lines
- Small label with decorative lines
- Main h1 title
- Decorative element with diamonds
- Description paragraph
- Scroll indicator
- Side corner frames (4 corners)
```tsx
```

### 9.3 AboutBlock (`src/components/Aboutpage/AboutBlock.tsx`)
- Image container with decorative frame + corner accents
- Image wrapper with aspect ratio
- Content card with border + diamond
- h3 title
- Paragraph content
- Bottom decorative line
```tsx
```

### 9.4 AboutCTA (`src/components/Aboutpage/AboutCTA.tsx`)
- Top/bottom gradient lines
- Corner accents (4 corners)
- Floating animated diamonds
- Decorative header with diamonds
- h2 title + description
- CTA buttons (primary + secondary)
- Social links with Instagram
```tsx
```

### 9.5 ContactPage (`src/app/(storefront)/contact/page.tsx`)
- Subtitle header
- ContactForm component
```tsx
```

### 9.6 ContactForm (`src/components/Contactpage/ContactForm.tsx`)
- Form card with border + corner accents
- Name fields (firstName, lastName)
- Email field
- Message textarea
- Submit button
- Form status message
- Alternative contact info section
```tsx
```

### 9.7 GalleryPage (`src/app/(storefront)/gallery/page.tsx`)
- Subtitle header
- PhotoGallery component
```tsx
```

### 9.8 PhotoGallery (`src/components/Aboutpage/PhotoGallery.tsx`)
- Masonry photo album
- Lightbox with thumbnails + zoom
- Image hover scale effect
```tsx
```

### 9.9 PrivacyPolicyPage (`src/app/(storefront)/privacy-policy/page.tsx`)
- Main h1 heading
- Multiple sections (h2 + paragraphs + lists)
- Typography hierarchy
```tsx
```

### 9.10 TermsPage (`src/app/(storefront)/terms/page.tsx`)
- Main h1 heading
- Multiple sections (h2/h3 + paragraphs + lists)
- Typography hierarchy
```tsx
```

---

## Phase 10: Shared UI Components

### 10.1 Buttons

**Primary CTA:**
```tsx
<button className="inline-flex items-center gap-3 px-8 py-4 bg-charcoal text-warm-white font-secondary text-sm tracking-wider uppercase transition-all duration-300 hover:bg-rose-gold">
  Button Text
  <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
</button>
```

**Secondary/Outline:**
```tsx
<button className="inline-flex items-center gap-3 px-8 py-4 border border-charcoal/30 text-charcoal font-secondary text-sm tracking-wider uppercase transition-all duration-300 hover:border-rose-gold hover:text-rose-gold">
  Button Text
</button>
```

### 10.2 Cards

```tsx
<div className="relative bg-warm-white overflow-hidden group">
  {/* Border frame */}
  <div className="absolute inset-0 border border-rose-gold/10 z-10 pointer-events-none transition-colors duration-500 group-hover:border-rose-gold/30" />

  {/* Corner accents */}
  <div className="absolute top-0 left-0 w-6 h-6 border-l border-t border-rose-gold/30 z-10 transition-all duration-500 group-hover:w-10 group-hover:h-10" />
  <div className="absolute top-0 right-0 w-6 h-6 border-r border-t border-rose-gold/30 z-10 transition-all duration-500 group-hover:w-10 group-hover:h-10" />
  <div className="absolute bottom-0 left-0 w-6 h-6 border-l border-b border-rose-gold/30 z-10 transition-all duration-500 group-hover:w-10 group-hover:h-10" />
  <div className="absolute bottom-0 right-0 w-6 h-6 border-r border-b border-rose-gold/30 z-10 transition-all duration-500 group-hover:w-10 group-hover:h-10" />

  {/* Content */}
</div>
```

### 10.3 Badge (`src/components/ui/badge.tsx`)
- Variants: default, secondary, destructive, outline
- CVA variants with transitions
```tsx
```

### 10.4 GlassySquareButton (`src/components/ui/cta-button.tsx`)
- Frosted glass effect
- Arrow icon
- Shimmer animation borders
- Hover glow effect
```tsx
```

### 10.5 Forms / Inputs
- Cream background inputs
- Rose-gold focus ring
- Error state styling
```tsx
```

### 10.6 Modals / Dialogs
- Border frame + corner accents
- Header with diamond decoration
- Footer with action buttons
```tsx
```

### 10.7 Loading States
- Shimmer-gold animation
- Skeleton placeholders
```tsx
```

### 10.8 Toast Notifications
- Success: green styling
- Error: burgundy styling
```tsx
```

---

## Decorative Patterns

### Diamond Shape
```tsx
<div className="w-2 h-2 bg-rose-gold/60 diamond-shape" />
```
```css
.diamond-shape {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}
```

### Corner Accents
```tsx
{/* Top corners */}
<div className="absolute top-0 left-0 w-8 h-8 border-l-2 border-t-2 border-rose-gold/40" />
<div className="absolute top-0 right-0 w-8 h-8 border-r-2 border-t-2 border-rose-gold/40" />

{/* Bottom corners */}
<div className="absolute bottom-0 left-0 w-8 h-8 border-l-2 border-b-2 border-rose-gold/40" />
<div className="absolute bottom-0 right-0 w-8 h-8 border-r-2 border-b-2 border-rose-gold/40" />

{/* Animated on hover */}
className="transition-all duration-500 group-hover:w-12 group-hover:h-12 group-hover:border-rose-gold/60"
```

### Gradient Dividers
```tsx
{/* Full width */}
<div className="h-[1px] bg-gradient-to-r from-transparent via-rose-gold/30 to-transparent" />

{/* Short accent */}
<div className="w-12 h-[1px] bg-gradient-to-r from-rose-gold/60 to-transparent" />
```

### Section Header Pattern
```tsx
<div className="py-16 md:py-24 text-center">
  {/* Diamond decoration */}
  <div className="flex items-center justify-center gap-4 mb-6">
    <div className="w-2 h-2 bg-rose-gold/60 diamond-shape" />
    <div className="w-16 h-[1px] bg-gradient-to-r from-rose-gold/60 to-champagne/40" />
    <div className="w-1.5 h-1.5 bg-champagne/50 diamond-shape" />
    <div className="w-16 h-[1px] bg-gradient-to-l from-rose-gold/60 to-champagne/40" />
    <div className="w-2 h-2 bg-rose-gold/60 diamond-shape" />
  </div>

  <h2 className="text-4xl md:text-5xl font-primary text-charcoal">
    Section Title
  </h2>

  <p className="mt-4 text-base font-secondary text-charcoal/60 max-w-2xl mx-auto">
    Optional description
  </p>

  {/* Bottom line */}
  <div className="mt-6 h-[1px] bg-gradient-to-r from-transparent via-rose-gold/30 to-transparent max-w-xs mx-auto" />
</div>
```

### Dark Section Pattern
```tsx
<section className="relative py-24 bg-charcoal overflow-hidden">
  {/* Top gradient line */}
  <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-rose-gold/30 to-transparent" />

  {/* Corner accents */}
  <div className="absolute top-8 left-8 w-16 h-16 border-l border-t border-rose-gold/20" />

  {/* Floating diamonds */}
  <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-rose-gold/20 diamond-shape" />

  {/* Content with light text */}
  <div className="text-warm-white">
    {/* ... */}
  </div>
</section>
```

### Image Overlays
```tsx
{/* Gradient from bottom */}
<div className="absolute inset-0 bg-gradient-to-t from-charcoal/70 via-charcoal/20 to-transparent" />

{/* Soft vignette */}
<div className="absolute inset-0 bg-gradient-to-b from-warm-white/40 via-transparent to-warm-white/90" />
```

---

## Typography Patterns

```tsx
{/* Hero Title */}
className="text-6xl sm:text-8xl lg:text-9xl font-primary tracking-tight"

{/* Section Titles */}
className="text-4xl md:text-5xl lg:text-6xl font-primary tracking-tight text-charcoal"

{/* Subtitles/Labels */}
className="text-xs tracking-[0.3em] uppercase font-secondary text-charcoal/70"

{/* Body Text */}
className="text-base lg:text-lg font-secondary text-charcoal/70 leading-relaxed"

{/* Small Text */}
className="text-xs text-charcoal/60 font-secondary"
```

---

## Animation Patterns

### Framer Motion - Scroll Fade Up
```tsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
  transition={{ duration: 0.8, ease: "easeOut" }}
>
```

### Framer Motion - Staggered Children
```tsx
const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.15 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }
  }
};
```

### Framer Motion - Floating
```tsx
animate={{
  y: [0, -15, 0],
  rotate: [0, 5, 0],
}}
transition={{
  duration: 6,
  repeat: Infinity,
  ease: "easeInOut",
}}
```

### CSS Transition Durations
- Fast: `duration-300`
- Medium: `duration-500`
- Slow: `duration-700`

---

## Responsive Patterns

```tsx
{/* Hide on mobile, show on desktop */}
className="hidden sm:block"
className="hidden lg:flex"

{/* Show on mobile, hide on desktop */}
className="sm:hidden"
className="lg:hidden"

{/* Responsive grid */}
className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8"

{/* Responsive text */}
className="text-4xl md:text-5xl lg:text-6xl"

{/* Responsive spacing */}
className="py-16 md:py-24"
className="px-4 sm:px-8"
```

---

## Image Aspect Ratios

| Element | Ratio |
|---------|-------|
| Hero | `min-h-screen` |
| Category cards | `aspect-[3/4]` |
| Product cards | `aspect-square` |
| About section | `aspect-[4/5]` |

---

## Completion Checklist

- [ ] Phase 1: Foundation (colors, fonts, gradients)
- [ ] Phase 2: Layout (Navbar, Footer, Sidebar)
- [ ] Phase 3: Homepage (Hero, Categories, About, Products)
- [ ] Phase 4: Product Pages (Listing, Card, Detail, Gallery)
- [ ] Phase 5: Category Pages
- [ ] Phase 6: Cart & Checkout (Cart, Forms, Payment)
- [ ] Phase 7: Auth Pages (Login, Register, Password Reset)
- [ ] Phase 8: Customer Dashboard (MyPage, Orders, Info, Wishlist)
- [ ] Phase 9: Static Pages (About, Contact, Gallery, Legal)
- [ ] Phase 10: Shared UI Components
