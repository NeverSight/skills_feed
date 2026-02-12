---
name: shopify-liquid
description: Complete Liquid templating language reference including syntax, filters, objects, control flow, loops, and conditionals for Shopify themes. Use when working with .liquid files, creating theme templates, implementing dynamic content, debugging Liquid code, working with sections and snippets, or rendering product/collection/cart data in Shopify stores.
---

# Shopify Liquid Templating

Expert guidance for Shopify's Liquid templating language including complete syntax reference, filters, objects, and best practices.

## When to Use This Skill

Invoke this skill when:

- Working with `.liquid`, `.css.liquid`, or `.js.liquid` files
- Creating or modifying theme templates (product, collection, cart, etc.)
- Implementing dynamic content rendering
- Using Liquid filters to format data (money, dates, strings)
- Accessing Shopify objects (product, collection, cart, customer)
- Writing conditional logic or loops in templates
- Debugging Liquid syntax errors or output issues
- Creating sections or snippets with Liquid logic
- Formatting prices, dates, or other data

## Core Capabilities

### 1. Liquid Syntax Fundamentals

Three core syntax types:

**Output (display values):**
```liquid
{{ product.title }}
{{ product.price | money }}
{{ collection.products.size }}
```

**Logic (conditionals and control):**
```liquid
{% if product.available %}
  <button>Add to Cart</button>
{% else %}
  <p>Sold Out</p>
{% endif %}
```

**Assignment (variables):**
```liquid
{% assign sale_price = product.price | times: 0.8 %}
{% capture full_title %}{{ collection.title }} - {{ product.title }}{% endcapture %}
```

**Whitespace control:**
```liquid
{%- if condition -%}
  Content (strips whitespace)
{%- endif -%}
```

### 2. Control Flow Tags

**Conditionals:**
- `if/elsif/else/endif` - Standard conditionals
- `unless/endunless` - Negated if
- `case/when/else/endcase` - Switch statements

**Logical operators:**
- `and`, `or` - Combine conditions
- `==`, `!=`, `>`, `<`, `>=`, `<=` - Comparisons
- `contains` - Substring/array search

**Example:**
```liquid
{% if product.available and product.price < 100 %}
  Affordable and in stock
{% elsif product.available %}
  Available but pricey
{% else %}
  Out of stock
{% endif %}
```

### 3. Iteration (Loops)

**for loop:**
```liquid
{% for product in collection.products %}
  {{ product.title }}
{% endfor %}

{# With modifiers #}
{% for product in collection.products limit: 5 offset: 10 reversed %}
  {{ product.title }}
{% endfor %}
```

**forloop object:**
```liquid
{% for item in array %}
  {{ forloop.index }}      {# 1-based index #}
  {{ forloop.index0 }}     {# 0-based index #}
  {{ forloop.first }}      {# Boolean: first item #}
  {{ forloop.last }}       {# Boolean: last item #}
  {{ forloop.length }}     {# Total items #}
{% endfor %}
```

**Pagination:**
```liquid
{% paginate collection.products by 12 %}
  {% for product in paginate.collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}

  {% if paginate.pages > 1 %}
    {{ paginate | default_pagination }}
  {% endif %}
{% endpaginate %}
```

### 4. Essential Filters

**Money formatting:**
```liquid
{{ 1000 | money }}                          {# $10.00 #}
{{ 1000 | money_without_currency }}         {# 10.00 #}
{{ 1000 | money_without_trailing_zeros }}   {# $10 #}
```

**String manipulation:**
```liquid
{{ "hello" | upcase }}                {# HELLO #}
{{ "hello" | capitalize }}            {# Hello #}
{{ "hello world" | truncate: 8 }}     {# hello... #}
{{ "a,b,c" | split: "," }}            {# ["a","b","c"] #}
{{ text | strip_html }}               {# Remove HTML tags #}
```

**Array/collection:**
```liquid
{{ array | first }}                              {# First element #}
{{ array | last }}                               {# Last element #}
{{ array | size }}                               {# Count #}
{{ products | map: "title" }}                    {# Extract property #}
{{ products | where: "vendor", "Nike" }}         {# Filter #}
{{ products | sort: "price" }}                   {# Sort #}
{{ array | join: ", " }}                         {# Join with separator #}
```

**Date formatting:**
```liquid
{{ order.created_at | date: '%B %d, %Y' }}      {# November 10, 2025 #}
{{ order.created_at | date: '%m/%d/%Y' }}       {# 11/10/2025 #}
{{ order.created_at | date: '%H:%M %p' }}       {# 12:39 PM #}
```

**Image handling:**
```liquid
{{ product.image | img_url: '500x500' }}        {# Resize image #}
{{ product.image | img_url: 'medium' }}         {# Named size #}
{{ 'logo.png' | asset_url }}                    {# Theme asset CDN #}
```

**Math operations:**
```liquid
{{ 5 | plus: 3 }}           {# 8 #}
{{ 5 | minus: 3 }}          {# 2 #}
{{ 5 | times: 3 }}          {# 15 #}
{{ 10 | divided_by: 2 }}    {# 5 #}
{{ 1.567 | round: 2 }}      {# 1.57 #}
```

**Chaining filters:**
```liquid
{{ collection.products | where: "available" | map: "title" | sort | first }}
```

### 5. Key Shopify Objects

**Product object:**
```liquid
{{ product.title }}
{{ product.price | money }}
{{ product.available }}              {# Boolean #}
{{ product.vendor }}
{{ product.type }}
{{ product.images }}                 {# Array #}
{{ product.variants }}               {# Array #}
{{ product.selected_variant }}
{{ product.metafields.custom.field }}
```

**Collection object:**
```liquid
{{ collection.title }}
{{ collection.products }}            {# Array #}
{{ collection.products_count }}
{{ collection.all_tags }}
{{ collection.sort_by }}
{{ collection.filters }}
```

**Cart object (global):**
```liquid
{{ cart.item_count }}
{{ cart.total_price | money }}
{{ cart.items }}                     {# Array of line items #}
{{ cart.empty? }}                    {# Boolean #}
```

**Customer object:**
```liquid
{{ customer.name }}
{{ customer.email }}
{{ customer.orders_count }}
{{ customer.total_spent | money }}
{{ customer.default_address }}
```

**Global objects:**
```liquid
{{ shop.name }}
{{ shop.currency }}
{{ shop.url }}
{{ request.path }}
{{ request.page_type }}             {# "product", "collection", etc. #}
{{ settings.color_primary }}        {# Theme settings #}
```

### 6. Template Inclusion

**render (isolated scope - PREFERRED):**
```liquid
{% render 'product-card', product: product, show_price: true %}

{# Render for each item #}
{% render 'product-card' for collection.products as item %}
```

**include (shared scope - LEGACY):**
```liquid
{% include 'product-details' %}
```

**section (dynamic sections):**
```liquid
{% section 'featured-product' %}
```

## Common Patterns

### Product availability check
```liquid
{% if product.available %}
  <button type="submit">Add to Cart</button>
{% elsif product.selected_variant.incoming %}
  <p>Coming {{ product.selected_variant.incoming_date | date: '%B %d' }}</p>
{% else %}
  <p class="sold-out">Sold Out</p>
{% endif %}
```

### Price display with sale
```liquid
{% if product.compare_at_price > product.price %}
  <span class="sale-price">{{ product.price | money }}</span>
  <span class="original-price">{{ product.compare_at_price | money }}</span>
  <span class="savings">Save {{ product.compare_at_price | minus: product.price | money }}</span>
{% else %}
  <span class="price">{{ product.price | money }}</span>
{% endif %}
```

### Loop through variants
```liquid
{% for variant in product.variants %}
  <option
    value="{{ variant.id }}"
    {% unless variant.available %}disabled{% endunless %}
  >
    {{ variant.title }} - {{ variant.price | money }}
  </option>
{% endfor %}
```

### Check collection tags
```liquid
{% if collection.all_tags contains 'sale' %}
  <div class="sale-banner">Sale items available!</div>
{% endif %}
```

## Best Practices

1. **Use whitespace control** (`{%-` and `-%}`) to keep HTML clean
2. **Prefer `render` over `include`** for better performance and isolation
3. **Cache expensive operations** by assigning to variables
4. **Use descriptive variable names** for clarity
5. **Leverage filters** instead of complex logic when possible
6. **Check for existence** before accessing nested properties
7. **Use `default` filter** for fallback values: `{{ product.metafield | default: "N/A" }}`

## Detailed References

For comprehensive documentation:

- **[references/syntax.md](references/syntax.md)** - Complete syntax reference with all tags
- **[references/filters.md](references/filters.md)** - All 60+ filters with examples
- **[references/objects.md](references/objects.md)** - Complete object property reference

## Integration with Other Skills

- **shopify-theme-dev** - Use when working with theme file structure and sections
- **shopify-api** - Use when fetching data via Ajax or GraphQL to display in Liquid
- **shopify-debugging** - Use when troubleshooting Liquid rendering issues
- **shopify-performance** - Use when optimizing Liquid template performance

## Quick Syntax Reference

```liquid
{# Output #}
{{ variable }}
{{ product.title | upcase }}

{# Conditionals #}
{% if condition %}...{% elsif %}...{% else %}...{% endif %}
{% unless condition %}...{% endunless %}
{% case variable %}{% when value %}...{% endcase %}

{# Loops #}
{% for item in array %}...{% endfor %}
{% for item in array limit: 5 offset: 10 %}...{% endfor %}
{% break %} / {% continue %}

{# Variables #}
{% assign var = value %}
{% capture var %}content{% endcapture %}

{# Inclusion #}
{% render 'snippet', param: value %}
{% section 'section-name' %}

{# Comments #}
{% comment %}...{% endcomment %}
{# Single line #}
```
