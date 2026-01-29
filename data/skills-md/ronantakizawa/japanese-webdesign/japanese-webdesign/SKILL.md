---
name: japanese-webdesign
description: Provides guidance for designing websites optimized for Japanese audiences, including cultural UX principles, information density patterns, bento layouts, trust signals, and localization best practices. Use when building e-commerce sites, landing pages, SaaS products, or any web application targeting Japanese users.
globs:
  - "**/*.html"
  - "**/*.css"
  - "**/*.jsx"
  - "**/*.tsx"
---

# Japanese Web Design Skill

## Overview

Japanese web design follows fundamentally different principles than Western design. What appears "cluttered" to Western eyes is optimized for Japanese cultural values, trust-building, and user expectations.

**Market Context:**
- Rakuten Ichiba: ¥6+ trillion GMV, 494.8 million monthly visitors
- Yahoo Japan Shopping: 118.2 million monthly visitors
- 60%+ of Japanese web traffic is mobile
- Credit-card-only checkout loses up to 30% of buyers

## Reference Files

- **[reference/component-patterns.md](reference/component-patterns.md)** - HTML/CSS component examples (product cards, banners, tables, footers, mobile navigation)
- **[reference/cultural-context.md](reference/cultural-context.md)** - Deep cultural factors (Anshin, demographics, seasons, Keigo levels, numbers to avoid)

## Core Principles

### 安心 (Anshin) - Reassurance Through Information

The most important concept: providing reassurance by eliminating surprises.

- **All information visible upfront** - hiding creates suspicion
- **Complete specifications before purchase decisions**
- **Multiple confirmation points to prevent mistakes**

> "If you're not showing me everything, what are you hiding?" — Common Japanese consumer mindset

### 一目瞭然 (Ichimoku Ryouzen) - Understanding at a Glance

Everything needed should be visible without requiring clicks or navigation.

### The Ponchi-e Culture

In Japanese business, Ponchi-e slides pack all relevant details into a single page. This approach directly influences web UI/UX expectations—no white space goes to waste.

## Design Patterns

### 1. Information Density

| Western Approach | Japanese Approach |
|------------------|-------------------|
| "Less is more" | "More is trust" |
| Progressive disclosure | Everything visible |
| Clean whitespace | Productive use of space |
| Single call-to-action | Multiple detailed options |
| "Learn more" buttons | Information already present |

**Why it works:** Kanji characters carry meaning without being sounded out, enabling faster scanning of dense layouts.

**Product cards should include:** ranking badges, review count, shipping info, full specs, original/sale price, discount %, points, delivery estimates.

### 2. Bento Box Layouts (弁当箱レイアウト)

Modern Japanese design uses modular content blocks inspired by bento boxes:

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
  grid-auto-flow: dense;
}
.bento-item { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }
```

**Best Practice:** Limit to 9 or fewer boxes for clarity while maintaining density.

### 3. Visual Hierarchy (No Uppercase)

Japanese has no uppercase/lowercase. Create hierarchy through:
- **Size variation** (larger = more important)
- **Color backgrounds** (colored boxes for sections)
- **Borders and frames** (明確な区切り)
- **Icons and badges**
- **Bold text** (avoid italics—renders poorly)

### 4. Trust Signals (信頼性)

Required trust indicators:
- **Customer service photo** - Staff with headset showing human support available
- ISO/Privacy Mark certifications
- Years in business (創業○○年)
- Customer satisfaction % (お客様満足度)
- Full company info: address, phone, fax, representative name
- Review count with actual text content
- **Shipping badges** - 「当日出荷」(same-day shipping), 「送料無料」prominently displayed

### 5. Form Design: Show Everything First

Japanese users want to see the entire process before starting.

**Wrong:** Step-by-step wizard hiding fields
**Right:** All fields visible with progress indicator (入力項目: 12項目中 0項目入力済み)

### 6. Confirmation Culture (確認)

Add multiple confirmation points:
1. Order summary (注文内容確認)
2. Explicit confirmation dialog
3. Final verification screen (最終確認)
4. Completion with detailed next steps

### 7. Color Usage

Common patterns:
- **Bright, saturated colors** (red, yellow, orange for attention)
- **Section color-coding** for organization
- **Seasonal colors** (桜ピンク in spring, 紅葉 in autumn)
- **Blue themes** for comparison/information sites (Kakaku.com style)
- **Orange/red** for e-commerce CTAs and sale badges

```css
:root {
  --sale-red: #e60012;
  --attention-yellow: #ffeb3b;
  --trust-blue: #0066cc;
  --kakaku-blue: #002d7a;
  --sakura-pink: #fcc;
  --category-purple: #6b5b95;
}
```

**Site type color conventions:**
- E-commerce: Red/orange accents (Rakuten style)
- Price comparison: Blue headers (Kakaku.com style)
- Portals: Multi-color sections (Yahoo Japan style)

### 8. Navigation

Show all options—avoid hamburger menus:
- Mega navigation with categories + item counts
- Inline popular items and current promotions
- Tab bars for mobile (not hamburger)

### 9. Category Grids (Kakaku.com Style)

Display categories as icon grids with subcategories inline:
- **Icon + category name** in colored box
- **Subcategories listed below** each main category
- **Item counts** per category (パソコン 15,234件)
- Blue/purple color coding for different sections

### 10. Trending Keywords (人気キーワード)

Show popular search terms as clickable tag buttons:
- Colored background tags (red for 注目, blue for trending)
- Displayed prominently near search bar
- Updated frequently to show freshness

### 11. Portal Layouts (Yahoo Japan Style)

Multi-column layouts for portal/news sites:
- **3+ columns** on desktop
- **Service sidebar** with icons for each service
- **News section** with thumbnail + headline
- **Topic tabs** (経済, エンタメ, スポーツ, etc.)
- **Weather widget** with location
- **"NEW" badges** (新着) on fresh content
- **Login/account section** in sidebar

## Typography

### Font Terminology
- **Serif** = **明朝 (Mincho)**
- **Sans-Serif** = **ゴシック (Gothic)**

### Font Stack

Japanese fonts require 7,000-16,000 glyphs (vs. ~230 for English).

```css
body {
  font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic Medium", "Meiryo", "Noto Sans JP", sans-serif;
}
.formal-text {
  font-family: "Hiragino Mincho ProN", "Yu Mincho", "Noto Serif JP", serif;
}
```

### Typography Rules

| Guideline | Recommendation |
|-----------|----------------|
| Font size | 10-15% smaller than Latin equivalent |
| Line height | 185-200% of font size |
| Line length | ~35 characters optimal |
| Italics | **Avoid** - renders poorly |
| Bold | Use sparingly, prefer color/size |

## E-Commerce Patterns

### Product Grid Layout

Dense thumbnail grids are standard:
- **Small thumbnails** (80-120px) in tight grid
- **Price overlay** on each thumbnail
- **Discount badges** (50%OFF, セール) as corner ribbons
- **Category icons** above product sections
- **Promotional banners** interspersed in grid

### Product Pages (商品ページ)

Must include:
- Ranking indicators with date/category
- 10-20 product images (not 3-5)
- Exhaustive specifications table
- Shipping details (carrier, timing, costs)
- Full return policy text (not just link)
- **Same-day shipping badge** if applicable (当日出荷)

### Price Display

Always show:
- Original price with label (メーカー希望小売価格)
- Sale price highlighted
- Discount amount AND percentage
- Tax status (税込/税抜)
- Points earned

### Payment Methods

Include all common options:
- Credit cards (VISA, Master, JCB, AMEX)
- コンビニ決済 (convenience store)
- PayPay, LINE Pay, 楽天ペイ
- 銀行振込 (bank transfer)
- 代金引換 (cash on delivery)

## SaaS & B2B Requirements

### Key Differences

- Extended trial periods expected
- Detailed documentation required before sales calls
- Formal language (敬語) required

### B2B-Specific CTAs

Primary flow: 資料ダウンロード (document download) → 無料トライアル → お問い合わせ

### Required Content
- Comprehensive feature documentation with screenshots
- Pricing with all tiers, features, and limits visible
- Security certifications (ISO 27001, SOC 2, ISMS)
- Support options with hours (日本語電話サポート: 平日9:00-18:00)
- Extensive FAQ section

### Language Formality (敬語)

| Context | Casual (B2C) | Formal (B2B) |
|---------|--------------|--------------|
| Submit | 送信する | 送信いたします |
| Error | エラーが発生しました | エラーが発生いたしました。お手数ですが、再度お試しください。 |

## Mobile Design

### Principles

- **Tab bars preferred** over hamburger menus
- **Information density maintained** on mobile
- **2-3 column grids** (not single column)
- **Smaller font (12px)** acceptable

```css
@media (max-width: 768px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .mobile-tab-nav { position: fixed; bottom: 0; display: flex; justify-content: space-around; }
}
```

## Cultural Considerations

### Mascot Characters (ゆるキャラ)

Use mascots to:
- Make institutions approachable
- Reduce anxiety about complex processes
- Guide onboarding, errors, and help sections

### Seasonal Content (季節感)

Update designs for seasons:
- **春**: Cherry blossoms, graduation
- **夏**: Cool blues, festival themes
- **秋**: Maple leaves (紅葉)
- **冬**: New Year, Valentine's

### Error Messages

Japanese errors should be apologetic:
```javascript
// Western: "Invalid email address"
// Japanese: "メールアドレスの形式が正しくありません。お手数ですが、再度ご確認ください。"
```

## Localization Mistakes to Avoid

1. **Translation ≠ Localization** - translated English loses nuance
2. **Machine translation** - Japanese is too complex
3. **Informal language** - sounds strange to customers
4. **Wrong Keigo level** - damages brand perception
5. **Credit-card only** - loses 30% of buyers
6. **No Japanese support** - deters repeat customers
7. **Cultural insensitivity** - improper imagery causes backlash

## Anti-Patterns

### Don't Do This:

1. Hide information behind "Learn More"
2. Use hamburger menus as primary navigation
3. Minimize form fields
4. Skip confirmation steps
5. Use vague CTAs ("Get Started" → 「資料ダウンロード」)
6. Remove trust signals for aesthetics
7. Assume minimal = professional
8. Use italics for Japanese text
9. Rely on machine translation

### Cultural Missteps:

- Number **4** (四 sounds like 死 = death)
- Number **9** (九 sounds like 苦 = suffering)
- Red ink for names (funeral association)
- Casual language in business contexts

## 2025 Trends

1. **Neo-retro design** - Y2K meets Showa nostalgia
2. **Immersive 3D** - tailored for precision
3. **AI personalization** - with human touch
4. **Microinteractions** - hover effects, scroll feedback
5. **Bento layouts** - modular, mobile-friendly
6. **Collapsible sections** - managing density

**Key insight:** Change is gradual. Japanese users adjust slowly—proven patterns are safer than innovation.

## A/B Testing Reality

| Test | Result |
|------|--------|
| Rakuten: Clean vs. cluttered | Cluttered converts better |
| Yahoo Japan: Modernized design | Users complained, reverted |
| Amazon Japan: Added MORE info | Sales increased |

## Reference Sites

- **Rakuten** (rakuten.co.jp) - E-commerce benchmark
- **Yahoo Japan** (yahoo.co.jp) - Portal density
- **Kakaku.com** - Price comparison
- **PayPay** - Mobile payment design
- **Mercari** - Mobile marketplace
- **LINE** - Super app patterns

## Quick Checklist

- [ ] All critical information visible without clicking
- [ ] Detailed specifications provided
- [ ] Trust signals prominent (company info, certifications)
- [ ] Multiple confirmation steps
- [ ] Full contact information (including fax)
- [ ] Reviews with actual text
- [ ] Price breakdown with tax (消費税10%)
- [ ] Multiple payment methods
- [ ] Shipping/return policies visible
- [ ] Navigation shows all categories
- [ ] Mobile maintains density with tab navigation
- [ ] Appropriate keigo level
- [ ] Seasonal elements if applicable
- [ ] Comprehensive FAQ
- [ ] Japanese-language support
- [ ] Professional localization (no machine translation)
- [ ] Typography: no italics, 185-200% line-height
- [ ] Numbers 4 and 9 not prominent
