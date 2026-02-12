---
name: web-asset-generator
description: Generate production-ready web assets through conversation. Favicons, PWA icons, and social media images from logos, emojis, or text.
original_source: https://github.com/alonw0/web-asset-generator
author: alonw0
license: MIT
---

# Web Asset Generator

Generate production-ready web assets (favicons, app icons, social images) through natural conversation with Claude.

## When to Use This Skill

- Creating favicons for a new website
- Generating PWA/mobile app icons
- Making Open Graph images for social sharing
- Converting logos to multiple sizes
- Creating quick icons from emojis
- Building a complete asset package

## What It Generates

### Favicons
```
favicon-16x16.png
favicon-32x32.png
favicon-96x96.png
favicon.ico
```

### PWA & App Icons
```
apple-touch-icon-180x180.png
android-chrome-192x192.png
android-chrome-512x512.png
```

### Social Media Images
```
og-image-1200x630.png    # Facebook, LinkedIn
twitter-card-1200x600.png # Twitter/X
whatsapp-preview.png      # WhatsApp
```

### Manifest Files
```json
{
  "name": "My App",
  "icons": [...]
}
```

## How to Use

### From Logo
```
Create all web assets from my logo: /path/to/logo.png
```

### From Emoji
```
Generate favicons using the coffee emoji for my cafe website
```

### From Text
```
Create social media images with text "Launch Day!"
on a gradient blue background
```

### Complete Package
```
Generate everything I need for my new startup website:
- Favicons
- PWA icons
- Open Graph images

Company: TechFlow
Colors: #2D9CDB primary, #27AE60 accent
```

## Interactive Workflow

The skill uses structured questions:

**1. Asset Type Selection**
```
What do you need?
○ Favicons only
○ PWA/App icons
○ Social media images
○ Everything (recommended)
```

**2. Source Material**
```
What should I use?
○ Logo image (provide path)
○ Emoji (I'll suggest options)
○ Text/slogan
○ Combination
```

**3. For Emoji-Based Icons**
```
Your project: Coffee shop website

Suggested emojis:
☕ Coffee cup
🫘 Coffee beans
☕️ Hot beverage
🏪 Store front

Or describe what you'd prefer...
```

**4. Customization**
```
Background color:
○ White (#FFFFFF)
○ Transparent
○ Custom color (enter hex)
```

## Generated Output

### Files Structure
```
assets/
├── favicons/
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   └── favicon.ico
├── app-icons/
│   ├── apple-touch-icon.png
│   └── android-chrome-512x512.png
├── social/
│   ├── og-image.png
│   └── twitter-card.png
└── manifest.json
```

### HTML Tags
```html
<!-- Favicons -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:image" content="https://yoursite.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://yoursite.com/twitter-card.png">
```

## Validation

Assets are checked for:
- Correct dimensions
- File size limits
- Color accessibility
- Platform compatibility
- Format requirements

## Framework Integration

After generation:
```
I detected you're using Next.js.

Add to your public/ folder:
1. Copy generated files to /public/
2. Update app/layout.tsx with meta tags
3. Add manifest link

Want me to show the code?
```

## Dependencies

### Required
```bash
pip install Pillow
```

### Optional (for emoji support)
```bash
pip install pilmoji emoji
```

## Examples

### Quick Favicon
```
User: "Make a quick favicon with a rocket emoji"

Generated:
- favicon-16x16.png ✓
- favicon-32x32.png ✓
- favicon.ico ✓
- HTML tags ready
```

### Full Branding Package
```
User: "Create complete web assets for my SaaS product 'DataFlow'"

Generated:
- 12 favicon sizes ✓
- 5 app icon sizes ✓
- 3 social images ✓
- manifest.json ✓
- HTML meta tags ✓
- Framework-specific code ✓
```

### Social Images Only
```
User: "I need Open Graph images for my blog post about AI"

Generated:
- og-image-1200x630.png (Facebook, LinkedIn)
- twitter-card-1200x600.png (Twitter/X)
- HTML tags for both
```

## Best Practices

1. **Start with high-res source** (512px+ for logos)
2. **Test generated assets** in social media debuggers
3. **Use transparent PNGs** when possible
4. **Verify on multiple devices**
5. **Update manifest.json** with correct paths

## Testing Tools

After generation, test with:
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
