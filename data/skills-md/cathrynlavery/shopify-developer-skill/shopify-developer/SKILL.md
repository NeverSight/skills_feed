---
name: shopify-developer
description: |
  Shopify development expert for Online Store 2.0, Hydrogen headless commerce, Shopify Functions, metaobjects/metafields, B2B wholesale, and checkout extensibility. Use for: theme customization, Liquid templating, section/block development, metafield configuration, Storefront/Admin API queries, checkout UI extensions, performance optimization, and Shopify Plus features. Triggers on: "Shopify", "Liquid", "theme", "metafield", "metaobject", "Hydrogen", "checkout extension", "Shopify Functions", "B2B wholesale", "Storefront API". For BestSelf.co store work, invoke BestSelf-Shopify-Skill for store-specific context.
---

# Shopify Developer

Expert guidance for Shopify development across themes, headless commerce, and platform extensions.

## Recommended: Install Context7 Skill

For up-to-date Shopify documentation lookups, install the Context7 skill:

```bash
npx skills add intellectronica/agent-skills --skill context7
```

This enables real-time API verification to prevent outdated patterns.

---

## Workflow Decision Tree

### Theme Development (Liquid)
→ *Consult [liquid-patterns.md](references/liquid-patterns.md) for metafields, loops, and performance.*

- **New section/template**: Create section with schema, use `sections everywhere` architecture
- **Editing existing theme**: Pull latest first, push to draft, test before live
- **Performance issues**: Minimize loops, use `limit:`, cache expensive lookups

### Headless Commerce (Hydrogen)
→ *Consult [apis-functions.md](references/apis-functions.md) for Storefront API queries and components.*

- **New storefront**: Use Hydrogen 2.0 + Oxygen hosting
- **Custom checkout**: Use Checkout Extensibility (checkout.liquid is deprecated)

### Backend Logic (Functions)
→ *Consult [apis-functions.md](references/apis-functions.md) for Function examples.*

- **Custom discounts, shipping, payments**: Shopify Functions (<5ms execution, Plus only)
- **Workflow automation**: Shopify Flow

### Store-Specific Work
- **BestSelf.co**: Invoke `BestSelf-Shopify-Skill` for theme IDs, `42-` section patterns, CSS conventions

---

## The API Drift Test

**CRITICAL**: Before implementing ANY Shopify feature, verify current patterns using Context7:

```bash
# Find Shopify Liquid library
curl -s "https://context7.com/api/v2/libs/search?libraryName=shopify+liquid&query=metafields" | jq '.results[0].id'

# Fetch current documentation
curl -s "https://context7.com/api/v2/context?libraryId=/shopify/liquid&query=metafield+access&type=txt"
```

**Common lookups:**
- Liquid: `libraryName=shopify+liquid`
- Storefront API: `libraryName=shopify+storefront+api`
- Hydrogen: `libraryName=shopify+hydrogen`

**Why this matters**: Shopify APIs change frequently. Code that worked in 2024 may be deprecated in 2025.

| Common Drift | Old Pattern | Current Pattern |
|--------------|-------------|-----------------|
| Checkout customization | `checkout.liquid` | Checkout UI Extensions |
| Delete metafield | `metafieldDelete` | `metafieldsDelete` |
| Metafield access | `product.metafields.namespace.key` | `product.metafields.namespace.key.value` |

**Also check**: https://changelog.shopify.com for breaking changes.

---

## Liquid Development
→ *Consult [liquid-patterns.md](references/liquid-patterns.md) for complete patterns.*

### Quick Reference
```liquid
{% comment %} Metafield (always use .value) {% endcomment %}
{{ product.metafields.custom.subtitle.value }}

{% comment %} List metafield iteration {% endcomment %}
{% for item in product.metafields.features.highlights.value %}
  {{ item }}
{% endfor %}

{% comment %} Metaobject iteration {% endcomment %}
{% for item in shop.metaobjects.testimonials.values %}
  {{ item.title }}
{% endfor %}

{% comment %} Safe defaults {% endcomment %}
{{ section.settings.title | default: 'Default Title' }}
```

### DO / DON'T

**DO**: Use `.value` accessor for metafields
**DO**: Use `limit:` on loops to prevent performance issues
**DO**: Use `where:` filter instead of nested conditionals
**DO**: Cache expensive lookups with `{% assign %}`

**DON'T**: Nest loops without limits—exponential performance hit
**DON'T**: Use `checkout.liquid`—deprecated Aug 2024
**DON'T**: Edit `settings_data.json` manually—Theme Editor overwrites it
**DON'T**: Forget `shopify_attributes` on blocks—breaks Theme Editor

---

## Section Architecture
→ *Consult [section-settings.md](references/section-settings.md) for all 20+ setting types.*

### Section Schema Template
```liquid
{% schema %}
{
  "name": "Section Name",
  "tag": "section",
  "class": "section-class",
  "settings": [
    { "type": "text", "id": "title", "label": "Title", "default": "Hello" },
    { "type": "richtext", "id": "content", "label": "Content" }
  ],
  "blocks": [
    {
      "type": "item",
      "name": "Item",
      "settings": [
        { "type": "text", "id": "heading", "label": "Heading" }
      ]
    }
  ],
  "presets": [{ "name": "Section Name" }]
}
{% endschema %}
```

**DO**: Include `presets` for sections you want in Theme Editor
**DO**: Use `shopify_attributes` on block containers
**DON'T**: Exceed 25 settings per section
**DON'T**: Exceed 50 blocks per section

---

## APIs & Functions
→ *Consult [apis-functions.md](references/apis-functions.md) for complete examples.*

### Storefront API (GraphQL)
For custom storefronts, cart operations, and product queries. Rate limit: 60 req/sec.

### Admin API (GraphQL)
For metafield management, product updates, order operations. Rate limit: 50 points/sec.

### Shopify Functions (Plus only)
Custom discounts, delivery, payments. Must execute in <5ms.

### Checkout Extensions
Modern checkout customization using React components.

---

## Platform Constraints
→ *Consult [platform-limits.md](references/platform-limits.md) for complete limits and 2024-2025 changes.*

| Limit | Value |
|-------|-------|
| Variants per product | 100 |
| Sections per template | 100 |
| Metafields per resource | 200 |
| Theme size | 50MB total, 2MB/file |
| Storefront API | 60 req/sec |
| Functions execution | <5ms |

---

## Theme CLI Workflow

```bash
# 1. Always pull latest first
shopify theme pull --theme <live-id>

# 2. Preview locally with hot reload
shopify theme dev --theme <draft-id>

# 3. Push to draft for testing
shopify theme push --theme <draft-id>

# 4. Only push to live after approval
shopify theme push --theme <live-id> --allow-live

# Push specific files only
shopify theme push --theme <id> --only assets/custom.css --only sections/hero.liquid
```

**DO**: Pull before starting work—themes change outside your session
**DO**: Push to draft first, test, then push to live
**DON'T**: Push directly to live without testing

---

## Output Checklist

When providing Shopify solutions:
- [ ] Verified current API patterns via Context7 or official docs
- [ ] Complete Liquid code with proper `.value` accessors
- [ ] Section schema with presets (if creating sections)
- [ ] Metafield configuration requirements noted
- [ ] Performance considerations (loop limits, caching)
- [ ] Testing notes for edge cases (empty states, variants)
