---
name: shopify-theme-dev
description: Complete theme development guide including file structure, JSON templates, sections, snippets, settings schema, and Online Store 2.0 architecture. Use when creating Shopify themes, organizing theme files, building sections and blocks, working with .json template files, configuring settings_schema.json, creating snippets, or implementing theme customization features.
---

# Shopify Theme Development

Expert guidance for Shopify theme development including file structure, Online Store 2.0 architecture, sections, snippets, and configuration.

## When to Use This Skill

Invoke this skill when:

- Creating or modifying Shopify themes
- Working with `.json` template files (Online Store 2.0)
- Building theme sections with schema definitions
- Creating reusable snippets
- Organizing theme file structure
- Configuring `settings_schema.json` for theme settings
- Implementing section blocks and settings
- Setting up theme assets (CSS, JavaScript, images)
- Working with layout files (`theme.liquid`, `password.liquid`)
- Creating template variations with suffixes

## Core Capabilities

### 1. Theme File Structure

Complete directory organization for Shopify themes:

```
theme/
├── assets/                     {# Static resources #}
│   ├── style.css              {# Main stylesheet #}
│   ├── style.css.liquid       {# Dynamic CSS with Liquid #}
│   ├── theme.js               {# Main JavaScript #}
│   ├── theme.js.liquid        {# Dynamic JS with Liquid #}
│   ├── logo.png               {# Images #}
│   └── fonts/                 {# Custom fonts #}
│
├── config/                     {# Configuration #}
│   ├── settings_schema.json   {# Theme settings UI #}
│   └── settings_data.json     {# Default values #}
│
├── layout/                     {# Master templates #}
│   ├── theme.liquid           {# Main wrapper #}
│   ├── password.liquid        {# Password protection #}
│   └── checkout.liquid        {# Checkout (Plus only) #}
│
├── locales/                    {# Translations #}
│   ├── en.default.json        {# English #}
│   └── fr.json                {# French #}
│
├── sections/                   {# Reusable sections #}
│   ├── header.liquid
│   ├── hero-banner.liquid
│   ├── product-card.liquid
│   └── footer.liquid
│
├── snippets/                   {# Reusable partials #}
│   ├── product-price.liquid
│   ├── product-rating.liquid
│   └── icon.liquid
│
└── templates/                  {# Page templates #}
    ├── index.json              {# Homepage (JSON) #}
    ├── product.json            {# Product page (JSON) #}
    ├── collection.json         {# Collection page (JSON) #}
    ├── product.liquid          {# Product (Liquid - legacy) #}
    ├── cart.liquid
    ├── search.liquid
    ├── page.liquid
    ├── 404.liquid
    └── customers/
        ├── account.liquid
        ├── login.liquid
        └── register.liquid
```

### 2. JSON Templates (Online Store 2.0)

Modern template format using JSON configuration:

**templates/index.json (Homepage):**
```json
{
  "sections": {
    "hero": {
      "type": "hero-banner",
      "settings": {
        "heading": "Summer Collection",
        "subheading": "New arrivals",
        "button_text": "Shop Now",
        "button_link": "/collections/all"
      }
    },
    "featured": {
      "type": "featured-products",
      "blocks": {
        "block_1": {
          "type": "product",
          "settings": {
            "product": "snowboard"
          }
        },
        "block_2": {
          "type": "product",
          "settings": {
            "product": "skateboard"
          }
        }
      },
      "block_order": ["block_1", "block_2"],
      "settings": {
        "title": "Featured Products",
        "products_to_show": 4
      }
    }
  },
  "order": ["hero", "featured"]
}
```

**templates/product.json:**
```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {
        "show_vendor": true,
        "show_quantity": true,
        "enable_zoom": true
      }
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like",
        "products_to_show": 4
      }
    }
  },
  "order": ["main", "recommendations"]
}
```

### 3. Section Architecture

Sections are reusable content blocks with schema configuration:

**sections/hero-banner.liquid:**
```liquid
<div class="hero" style="background-color: {{ section.settings.background_color }}">
  {% if section.settings.image %}
    <img
      src="{{ section.settings.image | img_url: '1920x' }}"
      alt="{{ section.settings.heading }}"
      loading="lazy"
    >
  {% endif %}

  <div class="hero__content">
    {% if section.settings.heading != blank %}
      <h1>{{ section.settings.heading }}</h1>
    {% endif %}

    {% if section.settings.subheading != blank %}
      <p>{{ section.settings.subheading }}</p>
    {% endif %}

    {% if section.settings.button_text != blank %}
      <a href="{{ section.settings.button_link }}" class="button">
        {{ section.settings.button_text }}
      </a>
    {% endif %}
  </div>
</div>

{% stylesheet %}
  .hero {
    position: relative;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing, 2rem);
  }

  .hero img {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
  }

  .hero__content {
    text-align: center;
    max-width: 600px;
  }
{% endstylesheet %}

{% javascript %}
  console.log('Hero banner loaded');
{% endjavascript %}

{% schema %}
{
  "name": "Hero Banner",
  "tag": "section",
  "class": "hero-section",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome"
    },
    {
      "type": "textarea",
      "id": "subheading",
      "label": "Subheading",
      "default": "Discover our collection"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Background Image"
    },
    {
      "type": "color",
      "id": "background_color",
      "label": "Background Color",
      "default": "#000000"
    },
    {
      "type": "text",
      "id": "button_text",
      "label": "Button Text",
      "default": "Shop Now"
    },
    {
      "type": "url",
      "id": "button_link",
      "label": "Button Link"
    }
  ],
  "presets": [
    {
      "name": "Hero Banner"
    }
  ]
}
{% endschema %}
```

### 4. Sections with Blocks

Sections can contain dynamic blocks for flexible layouts:

**sections/featured-products.liquid:**
```liquid
<div class="featured-products" {{ section.shopify_attributes }}>
  <h2>{{ section.settings.title }}</h2>

  <div class="product-grid">
    {% for block in section.blocks %}
      <div class="product-item" {{ block.shopify_attributes }}>
        {% case block.type %}
          {% when 'product' %}
            {% assign product = all_products[block.settings.product] %}
            {% render 'product-card', product: product %}

          {% when 'collection' %}
            {% assign collection = collections[block.settings.collection] %}
            <h3>{{ collection.title }}</h3>
            {% for product in collection.products limit: block.settings.products_to_show %}
              {% render 'product-card', product: product %}
            {% endfor %}

          {% when 'heading' %}
            <h3>{{ block.settings.heading }}</h3>

          {% when 'text' %}
            <div class="text-block">
              {{ block.settings.text }}
            </div>
        {% endcase %}
      </div>
    {% endfor %}
  </div>
</div>

{% schema %}
{
  "name": "Featured Products",
  "tag": "section",
  "settings": [
    {
      "type": "text",
      "id": "title",
      "label": "Section Title",
      "default": "Featured Products"
    },
    {
      "type": "range",
      "id": "products_per_row",
      "label": "Products per Row",
      "min": 2,
      "max": 5,
      "step": 1,
      "default": 4
    }
  ],
  "blocks": [
    {
      "type": "product",
      "name": "Product",
      "settings": [
        {
          "type": "product",
          "id": "product",
          "label": "Product"
        }
      ]
    },
    {
      "type": "collection",
      "name": "Collection",
      "settings": [
        {
          "type": "collection",
          "id": "collection",
          "label": "Collection"
        },
        {
          "type": "range",
          "id": "products_to_show",
          "label": "Products to Show",
          "min": 1,
          "max": 12,
          "step": 1,
          "default": 4
        }
      ]
    },
    {
      "type": "heading",
      "name": "Heading",
      "settings": [
        {
          "type": "text",
          "id": "heading",
          "label": "Heading Text"
        }
      ]
    },
    {
      "type": "text",
      "name": "Text Block",
      "settings": [
        {
          "type": "richtext",
          "id": "text",
          "label": "Text Content"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Featured Products",
      "blocks": [
        {
          "type": "product"
        },
        {
          "type": "product"
        },
        {
          "type": "product"
        }
      ]
    }
  ],
  "max_blocks": 12
}
{% endschema %}
```

### 5. Snippets

Reusable template partials:

**snippets/product-card.liquid:**
```liquid
{% comment %}
  Usage: {% render 'product-card', product: product, show_vendor: true %}
{% endcomment %}

<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      <img
        src="{{ product.featured_image | img_url: '400x400' }}"
        alt="{{ product.featured_image.alt | escape }}"
        loading="lazy"
      >
    {% else %}
      {{ 'product-1' | placeholder_svg_tag: 'placeholder' }}
    {% endif %}
  </a>

  <div class="product-card__info">
    {% if show_vendor and product.vendor != blank %}
      <p class="product-card__vendor">{{ product.vendor }}</p>
    {% endif %}

    <h3 class="product-card__title">
      <a href="{{ product.url }}">{{ product.title }}</a>
    </h3>

    <div class="product-card__price">
      {% render 'product-price', product: product %}
    </div>

    {% unless product.available %}
      <p class="sold-out">Sold Out</p>
    {% endunless %}
  </div>
</div>
```

**snippets/product-price.liquid:**
```liquid
{% comment %}
  Usage: {% render 'product-price', product: product %}
{% endcomment %}

{% if product.compare_at_price > product.price %}
  <span class="price price--sale">
    {{ product.price | money }}
  </span>
  <span class="price price--compare">
    {{ product.compare_at_price | money }}
  </span>
  <span class="price__badge">
    Save {{ product.compare_at_price | minus: product.price | money }}
  </span>
{% else %}
  <span class="price">
    {{ product.price | money }}
  </span>
{% endif %}

{% if product.price_varies %}
  <span class="price__from">from</span>
{% endif %}
```

### 6. Settings Schema

Complete theme customization interface:

**config/settings_schema.json:**
```json
[
  {
    "name": "theme_info",
    "theme_name": "My Theme",
    "theme_version": "1.0.0",
    "theme_author": "Your Name",
    "theme_documentation_url": "https://...",
    "theme_support_url": "https://..."
  },
  {
    "name": "Colors",
    "settings": [
      {
        "type": "header",
        "content": "Color Scheme"
      },
      {
        "type": "color",
        "id": "color_primary",
        "label": "Primary Color",
        "default": "#000000"
      },
      {
        "type": "color",
        "id": "color_secondary",
        "label": "Secondary Color",
        "default": "#ffffff"
      },
      {
        "type": "color_background",
        "id": "color_body_bg",
        "label": "Body Background"
      }
    ]
  },
  {
    "name": "Typography",
    "settings": [
      {
        "type": "font_picker",
        "id": "type_header_font",
        "label": "Heading Font",
        "default": "helvetica_n7"
      },
      {
        "type": "font_picker",
        "id": "type_body_font",
        "label": "Body Font",
        "default": "helvetica_n4"
      },
      {
        "type": "range",
        "id": "type_base_size",
        "label": "Base Font Size",
        "min": 12,
        "max": 24,
        "step": 1,
        "default": 16,
        "unit": "px"
      }
    ]
  },
  {
    "name": "Layout",
    "settings": [
      {
        "type": "select",
        "id": "layout_style",
        "label": "Layout Style",
        "options": [
          { "value": "boxed", "label": "Boxed" },
          { "value": "full-width", "label": "Full Width" },
          { "value": "wide", "label": "Wide" }
        ],
        "default": "full-width"
      },
      {
        "type": "checkbox",
        "id": "layout_sidebar_enabled",
        "label": "Enable Sidebar",
        "default": true
      }
    ]
  },
  {
    "name": "Header",
    "settings": [
      {
        "type": "image_picker",
        "id": "logo",
        "label": "Logo"
      },
      {
        "type": "range",
        "id": "logo_max_width",
        "label": "Logo Width",
        "min": 50,
        "max": 300,
        "step": 10,
        "default": 150,
        "unit": "px"
      },
      {
        "type": "link_list",
        "id": "main_menu",
        "label": "Main Menu"
      },
      {
        "type": "checkbox",
        "id": "header_sticky",
        "label": "Sticky Header",
        "default": false
      }
    ]
  },
  {
    "name": "Social Media",
    "settings": [
      {
        "type": "header",
        "content": "Social Accounts"
      },
      {
        "type": "url",
        "id": "social_twitter",
        "label": "Twitter URL",
        "info": "https://twitter.com/username"
      },
      {
        "type": "url",
        "id": "social_facebook",
        "label": "Facebook URL"
      },
      {
        "type": "url",
        "id": "social_instagram",
        "label": "Instagram URL"
      }
    ]
  }
]
```

### 7. Layout Files

Master template wrappers:

**layout/theme.liquid:**
```liquid
<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">

  <title>
    {{ page_title }}
    {%- if current_tags %} &ndash; {{ 'general.meta.tags' | t: tags: current_tags.join(', ') }}{% endif -%}
    {%- if current_page != 1 %} &ndash; {{ 'general.meta.page' | t: page: current_page }}{% endif -%}
    {%- unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless -%}
  </title>

  {{ content_for_header }}

  <link rel="stylesheet" href="{{ 'style.css' | asset_url }}">
  <script src="{{ 'theme.js' | asset_url }}" defer></script>
</head>
<body class="template-{{ request.page_type }}">
  {% section 'header' %}

  <main role="main">
    {{ content_for_layout }}
  </main>

  {% section 'footer' %}
</body>
</html>
```

## Common Settings Input Types

All 28+ input types for theme customization:

- `text` - Single line text
- `textarea` - Multi-line text
- `html` - HTML editor
- `richtext` - WYSIWYG editor
- `number` - Numeric input
- `range` - Slider
- `checkbox` - Boolean toggle
- `select` - Dropdown menu
- `radio` - Radio buttons
- `color` - Color picker
- `color_background` - Color with gradient
- `image_picker` - Upload image
- `media` - Image or video
- `url` - URL input
- `font_picker` - Font selector
- `product` - Product picker
- `collection` - Collection picker
- `page` - Page picker
- `blog` - Blog picker
- `article` - Article picker
- `link_list` - Menu picker
- `date` - Date picker
- `video_url` - Video URL (YouTube, Vimeo)

See [references/settings-schema.md](references/settings-schema.md) for complete examples.

## Best Practices

1. **Use JSON templates** for Online Store 2.0 compatibility
2. **Make sections dynamic** with blocks for merchant flexibility
3. **Add `shopify_attributes`** to section/block containers for theme editor
4. **Provide sensible defaults** in schema settings
5. **Use snippets** for repeated UI components
6. **Add `{% stylesheet %}` and `{% javascript %}`** blocks in sections for scoped styles
7. **Include accessibility** attributes (ARIA labels, alt text)
8. **Test in theme editor** to ensure live preview works
9. **Document snippet parameters** with comments
10. **Use semantic HTML** for better SEO

## Detailed References

- **[references/settings-schema.md](references/settings-schema.md)** - Complete input type reference
- **[references/section-patterns.md](references/section-patterns.md)** - Common section architectures
- **[references/template-examples.md](references/template-examples.md)** - JSON template patterns

## Integration with Other Skills

- **shopify-liquid** - Use when working with Liquid code within theme files
- **shopify-performance** - Use when optimizing theme load times and asset delivery
- **shopify-api** - Use when fetching data via Ajax for dynamic sections
- **shopify-debugging** - Use when troubleshooting theme editor or rendering issues

## Quick Reference

```liquid
{# Section with settings #}
{% schema %}
{
  "name": "Section Name",
  "settings": [...],
  "blocks": [...],
  "presets": [...]
}
{% endschema %}

{# Access section settings #}
{{ section.settings.setting_id }}

{# Loop through blocks #}
{% for block in section.blocks %}
  {{ block.settings.text }}
  {{ block.shopify_attributes }}
{% endfor %}

{# Render snippet with parameters #}
{% render 'snippet-name', param: value %}

{# Access theme settings #}
{{ settings.color_primary }}

{# Section attributes for theme editor #}
<div {{ section.shopify_attributes }}>...</div>
<div {{ block.shopify_attributes }}>...</div>
```
