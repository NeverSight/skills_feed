---
name: hyva-alpine-component
description: Write CSP-compatible Alpine.js components for Hyvä themes in Magento 2. This skill should be used when the user wants to create Alpine components, add interactivity to Hyvä templates, write JavaScript for Hyvä themes, or needs help with Alpine.js patterns that work with Content Security Policy. Trigger phrases include "create alpine component", "add interactivity", "alpine for hyva", "x-data component", "csp compatibility", "csp compliant javascript".
---

# Hyvä Alpine Component

## Overview

This skill provides guidance for writing CSP-compatible Alpine.js components in Hyvä themes. Alpine CSP is a specialized Alpine.js build that operates without the `unsafe-eval` CSP directive, which is required for PCI-DSS 4.0 compliance on payment-related pages (mandatory from April 1, 2025).

**Key principle:** CSP-compatible code functions in both standard and Alpine CSP builds. Write all Alpine code using CSP patterns for future-proofing.

## CSP Constraints Summary

| Capability | Standard Alpine | Alpine CSP |
|------------|-----------------|------------|
| Property reads | `x-show="open"` | Same |
| Negation | `x-show="!open"` | Method: `x-show="isNotOpen"` |
| Mutations | `@click="open = false"` | Method: `@click="close"` |
| Method args | `@click="setTab('info')"` | Dataset: `@click="setTab" data-tab="info"` |
| `x-model` | Available | **Not supported** - use `:value` + `@input` |
| Range iteration | `x-for="i in 10"` | **Not supported** |

## Component Structure Pattern

Every Alpine component in Hyvä follows this structure:

```html
<div x-data="initComponentName">
    <!-- Template content -->
</div>
<script>
    function initComponentName() {
        return {
            // Properties
            propertyName: initialValue,

            // Lifecycle
            init() {
                // Called when component initializes
            },

            // Methods for state access
            isPropertyTrue() {
                return this.propertyName === true;
            },

            // Methods for mutations
            setPropertyValue() {
                this.propertyName = this.$event.target.value;
            }
        }
    }
    window.addEventListener('alpine:init', () => Alpine.data('initComponentName', initComponentName), {once: true})
</script>
<?php $hyvaCsp->registerInlineScript() ?>
```

**Critical requirements:**
1. Register constructor with `Alpine.data()` inside `alpine:init` event listener
2. Use `{once: true}` to prevent duplicate registrations
3. Call `$hyvaCsp->registerInlineScript()` after every `<script>` block
4. Use `$escaper->escapeJs()` for PHP values in JavaScript strings
5. Use `$escaper->escapeHtmlAttr()` for data attributes (not `escapeJs`)

## Constructor Functions

### Basic Registration

```javascript
function initMyComponent() {
    return {
        open: false
    }
}
window.addEventListener('alpine:init', () => Alpine.data('initMyComponent', initMyComponent), {once: true})
```

**Why named global functions?** Constructor functions are declared as named functions in global scope (not inlined in the `Alpine.data()` callback) so they can be proxied and extended in other templates. This is an extensibility feature of Hyvä Themes - other modules or child themes can wrap or override these functions before they are registered with Alpine.

### Composing Multiple Objects

When combining objects (e.g., with `hyva.modal`), use spread syntax inside the constructor:

```javascript
function initMyModal() {
    return {
        ...hyva.modal.call(this),
        ...hyva.formValidation(this.$el),
        customProperty: '',
        customMethod() {
            // Custom logic
        }
    };
}
```

Use `.call(this)` to pass Alpine context to composed functions.

## Property Access Patterns

### Value Properties with Dot Notation

```javascript
return {
    item: {
        is_visible: true,
        title: 'Product'
    }
}
```

```html
<span x-show="item.is_visible" x-text="item.title"></span>
```

### Transforming Values (Negation, Conditions)

CSP does not allow inline transformations. Create methods instead:

**Wrong (CSP incompatible):**
```html
<span x-show="!item.deleted"></span>
<span x-text="item.title || item.value"></span>
```

**Correct:**
```html
<span x-show="isItemNotDeleted"></span>
<span x-text="itemLabel"></span>
```

```javascript
return {
    item: { deleted: false, title: '', value: '' },

    isItemNotDeleted() {
        return !this.item.deleted;
    },
    itemLabel() {
        return this.item.title || this.item.value;
    }
}
```

### Negation Method Shorthand

For simple boolean negation, use bracket notation:

```javascript
return {
    deleted: false,
    ['!deleted']() {
        return !this.deleted;
    }
}
```

```html
<template x-if="!deleted">
    <div>The item is present</div>
</template>
```

## Property Mutation Patterns

### Extract Mutations to Methods

**Wrong (CSP incompatible):**
```html
<button @click="open = !open">Toggle</button>
```

**Correct:**
```html
<button @click="toggle">Toggle</button>
```

```javascript
return {
    open: false,
    toggle() {
        this.open = !this.open;
    }
}
```

### Passing Arguments via Dataset

**Wrong (CSP incompatible):**
```html
<button @click="selectItem(123)">Select</button>
```

**Correct:**
```html
<button @click="selectItem" data-item-id="<?= $escaper->escapeHtmlAttr($itemId) ?>">Select</button>
```

```javascript
return {
    selected: null,
    selectItem() {
        this.selected = this.$el.dataset.itemId;
    }
}
```

**Important:** Use `escapeHtmlAttr` for data attributes, not `escapeJs`.

### Accessing Event and Loop Variables in Methods

Methods can access Alpine's special properties:

```javascript
return {
    onInput() {
        // Access event
        const value = this.$event.target.value;
        this.inputValue = value;
    },
    getItemUrl() {
        // Access x-for loop variable
        return `${BASE_URL}/product/id/${this.item.id}`;
    }
}
```

## x-model Alternatives

`x-model` is **not available** in Alpine CSP. Use two-way binding patterns instead.

### Text Inputs

```html
<input type="text"
       :value="username"
       @input="setUsername">
```

```javascript
return {
    username: '',
    setUsername() {
        this.username = this.$event.target.value;
    }
}
```

### Number Inputs

Use `hyva.safeParseNumber()` for numeric values:

```javascript
return {
    quantity: 1,
    setQuantity() {
        this.quantity = hyva.safeParseNumber(this.$event.target.value);
    }
}
```

### Textarea

```html
<textarea @input="setComment" x-text="comment"></textarea>
```

```javascript
return {
    comment: '',
    setComment() {
        this.comment = this.$event.target.value;
    }
}
```

### Checkboxes

```html
<input type="checkbox"
       :checked="isSubscribed"
       @change="toggleSubscribed">
```

```javascript
return {
    isSubscribed: false,
    toggleSubscribed() {
        this.isSubscribed = this.$event.target.checked;
    }
}
```

### Checkbox Arrays

```html
<template x-for="option in options" :key="option.id">
    <input type="checkbox"
           :value="option.id"
           :checked="isOptionSelected"
           @change="toggleOption"
           :data-option-id="option.id">
</template>
```

```javascript
return {
    selectedOptions: [],
    isOptionSelected() {
        return this.selectedOptions.includes(this.option.id);
    },
    toggleOption() {
        const optionId = this.$el.dataset.optionId;
        const index = this.selectedOptions.indexOf(optionId);
        if (index === -1) {
            this.selectedOptions.push(optionId);
        } else {
            this.selectedOptions.splice(index, 1);
        }
    }
}
```

### Select Elements

```html
<select @change="setCountry">
    <template x-for="country in countries" :key="country.code">
        <option :value="country.code"
                :selected="isCountrySelected"
                x-text="country.name"></option>
    </template>
</select>
```

```javascript
return {
    selectedCountry: '',
    isCountrySelected() {
        return this.selectedCountry === this.country.code;
    },
    setCountry() {
        this.selectedCountry = this.$event.target.value;
    }
}
```

## x-for Patterns

### Basic Iteration

```html
<template x-for="(product, index) in products" :key="index">
    <div x-text="product.name"></div>
</template>
```

### Using Methods in Loops

Loop variables (`product`, `index`) are accessible in methods:

```html
<template x-for="(product, index) in products" :key="index">
    <span :class="getItemClasses" @click="goToProduct" x-text="product.name"></span>
</template>
```

```javascript
return {
    products: [],
    getItemClasses() {
        return {
            'font-bold': this.index === 0,
            'text-gray-500': this.product.disabled
        };
    },
    goToProduct() {
        window.location.href = `${BASE_URL}/product/${this.product.url_key}`;
    }
}
```

### Function as Value Provider

The value provider can be a method (called without parentheses):

```html
<template x-for="(item, index) in getFilteredItems" :key="index">
    <div x-text="item.name"></div>
</template>
```

```javascript
return {
    items: [],
    filter: '',
    getFilteredItems() {
        return this.items.filter(item => item.name.includes(this.filter));
    }
}
```

**Note:** Range iteration (`x-for="i in 10"`) is not supported in Alpine CSP.

## Hyva Utility Functions

The global `hyva` object provides these utilities:

### Form and Security
- `hyva.getFormKey()` - Get/generate form key for POST requests
- `hyva.getUenc()` - Base64 encode current URL for redirects
- `hyva.postForm({action, data, skipUenc})` - Submit a POST form programmatically

### Cookies
- `hyva.getCookie(name)` - Get cookie value (respects consent)
- `hyva.setCookie(name, value, days, skipSetDomain)` - Set cookie
- `hyva.setSessionCookie(name, value, skipSetDomain)` - Set session cookie

### Formatting
- `hyva.formatPrice(value, showSign, options)` - Format currency
- `hyva.str(template, ...args)` - String interpolation with %1, %2 placeholders
- `hyva.strf(template, ...args)` - Zero-based string interpolation (%0, %1)

### Numbers
- `hyva.safeParseNumber(rawValue)` - Parse number safely (for x-model.number replacement)

### DOM
- `hyva.replaceDomElement(selector, content)` - Replace DOM element with HTML content
- `hyva.trapFocus(rootElement)` - Trap focus within element (for modals)
- `hyva.releaseFocus(rootElement)` - Release focus trap

### Storage
- `hyva.getBrowserStorage()` - Get localStorage/sessionStorage safely

### Boolean Object Helper

For toggle components, use `hyva.createBooleanObject`:

```javascript
function initToggle() {
    return {
        ...hyva.createBooleanObject('open', false),
        // Additional methods
    };
}
```

This generates: `open()`, `notOpen()`, `toggleOpen()`, `setOpenTrue()`, `setOpenFalse()`

### Alpine Initialization

```javascript
hyva.alpineInitialized(fn)  // Run callback after Alpine initializes
```

## Event Patterns

### Listening to Custom Events

```html
<div x-data="initMyComponent"
     @private-content-loaded.window="onPrivateContentLoaded"
     @update-gallery.window="onGalleryUpdate">
```

```javascript
return {
    onPrivateContentLoaded() {
        const data = this.$event.detail.data;
        // Handle customer data
    },
    onGalleryUpdate() {
        const images = this.$event.detail;
        this.images = images;
    }
}
```

### Dispatching Events

```javascript
return {
    updateQuantity() {
        this.qty = newValue;
        this.$dispatch('update-qty-' + this.productId, this.qty);
    }
}
```

### Common Hyvä Events
- `private-content-loaded` - Customer section data loaded
- `reload-customer-section-data` - Request customer data refresh
- `update-gallery` - Product gallery images changed
- `reset-gallery` - Reset gallery to initial state

## Event Listeners Object Pattern

For multiple window/document event listeners, use the `x-bind` pattern:

```html
<div x-data="initGallery" x-bind="eventListeners">
```

```javascript
return {
    eventListeners: {
        ['@keydown.window.escape']() {
            if (!this.fullscreen) return;
            this.closeFullScreen();
        },
        ['@update-gallery.window'](event) {
            this.receiveImages(event.detail);
        },
        ['@keyup.arrow-right.window']() {
            if (!this.fullscreen) return;
            this.nextItem();
        }
    }
}
```

## Dynamic Classes Pattern

Return class objects from methods:

```html
<div :class="containerClasses">
```

```javascript
return {
    fullscreen: false,
    containerClasses() {
        return {
            'w-full h-full fixed top-0 left-0 bg-white z-50': this.fullscreen,
            'relative': !this.fullscreen
        };
    }
}
```

## Passing PHP Data to Components

### Via Data Attributes

```html
<div x-data="initProductList"
     data-products="<?= $escaper->escapeHtmlAttr(json_encode($products)) ?>"
     data-config="<?= $escaper->escapeHtmlAttr(json_encode($config)) ?>">
```

```javascript
return {
    products: [],
    config: {},
    init() {
        this.products = JSON.parse(this.$root.dataset.products || '[]');
        this.config = JSON.parse(this.$root.dataset.config || '{}');
    }
}
```

### Via Inline JavaScript (with escaping)

```javascript
function initComponent() {
    return {
        productId: '<?= (int) $product->getId() ?>',
        productName: '<?= $escaper->escapeJs($product->getName()) ?>',
        config: <?= /* @noEscape */ json_encode($config) ?>
    }
}
```

## Complete Example: Quantity Selector

```php
<?php
declare(strict_types=1);

use Hyva\Theme\ViewModel\HyvaCsp;
use Magento\Framework\Escaper;

/** @var Escaper $escaper */
/** @var HyvaCsp $hyvaCsp */

$productId = (int) $product->getId();
$minQty = 1;
$maxQty = 100;
$defaultQty = 1;
?>
<div x-data="initQtySelector">
    <label for="qty-<?= $productId ?>" class="sr-only">
        <?= $escaper->escapeHtml(__('Quantity')) ?>
    </label>
    <div class="flex items-center">
        <button type="button"
                class="btn"
                @click="decrement"
                :disabled="isMinQty"
                :class="decrementClasses">
            -
        </button>
        <input type="number"
               id="qty-<?= $productId ?>"
               name="qty"
               :value="qty"
               @input="onInput"
               min="<?= $minQty ?>"
               max="<?= $maxQty ?>"
               class="form-input w-16 text-center">
        <button type="button"
                class="btn"
                @click="increment"
                :disabled="isMaxQty"
                :class="incrementClasses">
            +
        </button>
    </div>
</div>
<script>
    function initQtySelector() {
        return {
            qty: <?= (int) $defaultQty ?>,
            minQty: <?= (int) $minQty ?>,
            maxQty: <?= (int) $maxQty ?>,
            productId: '<?= $productId ?>',

            onInput() {
                let value = hyva.safeParseNumber(this.$event.target.value);
                if (value < this.minQty) value = this.minQty;
                if (value > this.maxQty) value = this.maxQty;
                this.qty = value;
                this.$dispatch('update-qty-' + this.productId, this.qty);
            },

            increment() {
                if (this.qty < this.maxQty) {
                    this.qty++;
                    this.$dispatch('update-qty-' + this.productId, this.qty);
                }
            },

            decrement() {
                if (this.qty > this.minQty) {
                    this.qty--;
                    this.$dispatch('update-qty-' + this.productId, this.qty);
                }
            },

            isMinQty() {
                return this.qty <= this.minQty;
            },

            isMaxQty() {
                return this.qty >= this.maxQty;
            },

            decrementClasses() {
                return { 'opacity-50 cursor-not-allowed': this.isMinQty() };
            },

            incrementClasses() {
                return { 'opacity-50 cursor-not-allowed': this.isMaxQty() };
            }
        }
    }
    window.addEventListener('alpine:init', () => Alpine.data('initQtySelector', initQtySelector), {once: true})
</script>
<?php $hyvaCsp->registerInlineScript() ?>
```

## References

- Hyvä CSP Documentation: https://docs.hyva.io/hyva-themes/writing-code/csp/alpine-csp.html
- Alpine.js Documentation: https://alpinejs.dev/
- Example components: `vendor/hyva-themes/magento2-default-theme-csp/`
- Core utilities: `vendor/hyva-themes/magento2-theme-module/src/view/frontend/templates/page/js/hyva.phtml`

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
