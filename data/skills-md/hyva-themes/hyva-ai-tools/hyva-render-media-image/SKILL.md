---
name: hyva-render-media-image
description: Generate responsive image code for Hyvä Theme templates using the Media view model. This skill should be used when the user wants to render images in a Hyvä template, create responsive picture elements, add hero images, product images, or any image that needs responsive breakpoints. Trigger phrases include "render image", "add image to template", "responsive image", "picture element", "hero image", "responsive banner", "image for mobile and desktop", or "banner image".
---

# Hyvä Render Image

Generate responsive `<picture>` elements for Hyvä Theme templates using the `\Hyva\Theme\ViewModel\Media` view model.

## When to Use

- Adding images to Hyvä PHTML templates
- Creating responsive images with different sources for mobile/desktop
- Implementing hero banners, product images, or CMS content images
- Optimizing images for Core Web Vitals (LCP, CLS)

## Workflow

### 1. Gather Image Requirements

The user may provide image data in one of these ways:

**Option A: Direct values** - Ask the user for:
1. **Image path(s)** - Location in `pub/media/` (e.g., `wysiwyg/hero.jpg`, `catalog/product/...`)
2. **Image dimensions** - Width and height in pixels
3. **Responsive requirements** - Different images for mobile vs desktop?
4. **Image purpose** - Hero/LCP image (eager loading) or below-fold (lazy loading)?
5. **Alt text** - Meaningful description for accessibility

**Option B: PHP variable** - The user provides a variable name (e.g., `$imageData`, `$heroImage`). Inform the user of the required array structure documented in `references/rendering-images.md` under `## Image Configuration Format`.

### 2. Generate the Code

Refer to `references/rendering-images.md` for the complete API reference, code examples, and all configuration options.

**Choose the appropriate pattern:**

| Scenario | Pattern to Use |
|----------|---------------|
| Single image, literal values | Single Image Example |
| Single image from variable | Wrap in array: `[$imageData]` |
| Multiple images from variable | Pass directly: `$images` |
| Different images for mobile/desktop | Responsive Images with Media Queries |
| Need to style the `<picture>` wrapper | Picture Element Attributes |

**Base template:**

```php
<?php
/** @var \Hyva\Theme\ViewModel\Media $mediaViewModel */
$mediaViewModel = $viewModels->require(\Hyva\Theme\ViewModel\Media::class);

echo $mediaViewModel->getResponsivePictureHtml(
    $images,        // Array of image configs (see reference for format)
    $imgAttributes, // Optional: alt, class, loading, fetchpriority
    $pictureAttributes // Optional: class, data-* attributes for <picture>
);
```

### 3. Set Loading Strategy

| Image Type | Attributes |
|------------|------------|
| Hero/LCP (above fold) | `'loading' => 'eager', 'fetchpriority' => 'high'` |
| Below fold | `'loading' => 'lazy'` |

## Resources

- `references/rendering-images.md` - Complete API reference with method signature, all configuration options, code examples, and best practices

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->
