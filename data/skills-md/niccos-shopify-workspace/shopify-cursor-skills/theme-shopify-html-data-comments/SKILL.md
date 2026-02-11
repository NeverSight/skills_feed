---
name: theme-shopify-html-data-comments
description: HTML structure, data attributes, and commenting guidelines for Shopify themes. Use when structuring HTML markup and adding comments to Shopify theme code.
---

# Shopify HTML, Data Attributes & Comments

Guidelines for HTML structure, data attributes usage, and code commenting in Shopify themes.

## When to Use

- Structuring HTML markup in sections
- Passing data to JavaScript via attributes
- Adding comments to Liquid templates
- Organizing HTML elements

## HTML & Data Attributes

### Custom HTML Tags

- Use custom HTML tags when appropriate
- Custom elements work well with JavaScript custom elements
- Improves semantic structure

### Example

```liquid
<product-card data-product-id="{{ product.id }}">
  <!-- Content -->
</product-card>
```

### Data Attributes

- Pass dynamic data via `data-*` attributes
- Access in JavaScript via `dataset` property
- Use kebab-case for attribute names

### Data Attribute Naming

```liquid
<!-- Good - kebab-case -->
<div 
  data-product-id="{{ product.id }}"
  data-variant-id="{{ variant.id }}"
  data-product-handle="{{ product.handle }}">
</div>

<!-- Bad - camelCase or other formats -->
<div data-productId="{{ product.id }}"></div>
```

### Accessing Data in JavaScript

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super();
    this.productId = this.dataset.productId;
    this.variantId = this.dataset.variantId;
    this.productHandle = this.dataset.productHandle;
  }
}
```

### Data Attributes for Configuration

Use data attributes to pass configuration from Liquid to JavaScript:

```liquid
<image-gallery 
  data-autoplay="{{ section.settings.autoplay }}"
  data-interval="{{ section.settings.interval }}"
  data-transition="{{ section.settings.transition }}">
  <!-- Gallery content -->
</image-gallery>
```

```javascript
class ImageGallery extends HTMLElement {
  constructor() {
    super();
    this.autoplay = this.dataset.autoplay === 'true';
    this.interval = parseInt(this.dataset.interval, 10);
    this.transition = this.dataset.transition;
  }
}
```

## Comments

### Comment Guidelines

- Keep comments minimal
- Comment only non-obvious logic
- Do NOT explain every line
- Use comments to explain "why", not "what"

### Liquid Comments

```liquid
{%- comment -%}
  Calculate discount percentage for products with compare_at_price.
  Only show discount badge if discount is greater than 20%.
{%- endcomment -%}

{% liquid
  if product.compare_at_price > product.price
    assign discount = product.compare_at_price | minus: product.price
    assign discount_percent = discount | times: 100 | divided_by: product.compare_at_price
    if discount_percent > 20
      assign show_badge = true
    endif
  endif
%}
```

### Snippet Usage Comments

Always include usage comments in snippets:

```liquid
{%- comment -%}
Usage:
{% render 'product-card', 
  product: product, 
  show_vendor: true, 
  show_price: true %}
{%- endcomment -%}
```

### HTML Comments

Use HTML comments sparingly for section organization:

```liquid
{%- comment -%}
  Product Card Section
  Displays product information with image, title, price, and add to cart button
{%- endcomment -%}

<div class="product-card">
  <!-- Product Image -->
  <div class="product-card__image">
    {{ product.featured_image | image_tag: widths: '360, 720', loading: 'lazy' }}
  </div>

  <!-- Product Info -->
  <div class="product-card__info">
    <h3 class="product-card__title">{{ product.title }}</h3>
    <p class="product-card__price">{{ product.price | money }}</p>
  </div>
</div>
```

### When to Comment

**Do comment:**
- Complex business logic
- Non-obvious calculations
- Workarounds or hacks
- Snippet usage instructions
- Section-level documentation

**Don't comment:**
- Obvious code (e.g., `{% if product.available %}`)
- Every line of code
- Self-explanatory variable names
- Standard Liquid syntax

### Example: Good vs Bad Comments

```liquid
{%- comment -%}
  Good: Explains why, not what
  Calculate discount percentage. Shopify doesn't provide this directly,
  so we calculate it from compare_at_price and current price.
{%- endcomment -%}
{% liquid
  assign discount = product.compare_at_price | minus: product.price
  assign discount_percent = discount | times: 100 | divided_by: product.compare_at_price
%}

{%- comment -%}
  Bad: Explains what, which is obvious
  Check if product is available. If available, show add to cart button.
{%- endcomment -%}
{% if product.available %}
  <button>Add to Cart</button>
{% endif %}
```

## HTML Structure Best Practices

### Semantic HTML

Use semantic HTML elements:

```liquid
<article class="product-card">
  <header class="product-card__header">
    <h2 class="product-card__title">{{ product.title }}</h2>
  </header>
  <div class="product-card__image">
    {{ product.featured_image | image_tag: widths: '360, 720', loading: 'lazy' }}
  </div>
  <footer class="product-card__footer">
    <p class="product-card__price">{{ product.price | money }}</p>
    <button class="product-card__button">Add to Cart</button>
  </footer>
</article>
```

### Accessibility

Include proper accessibility attributes:

```liquid
<button 
  aria-label="Add {{ product.title }} to cart"
  data-product-id="{{ product.id }}">
  Add to Cart
</button>
```

## Shopify Theme Documentation

Reference these official Shopify resources:

- [HTML Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [Data Attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*)
- [Web Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Shopify Theme Structure](https://shopify.dev/docs/themes/architecture)

## Instructions

1. **Use custom HTML tags** when appropriate for semantic structure
2. **Pass data via `data-*` attributes** using kebab-case
3. **Keep comments minimal** - only for non-obvious logic
4. **Comment "why", not "what"** - explain reasoning, not obvious code
5. **Include usage comments** in all snippets
6. **Use semantic HTML** for better structure and accessibility
7. **Add accessibility attributes** (aria-label, alt text, etc.)
