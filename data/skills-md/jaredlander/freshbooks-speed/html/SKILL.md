---
name: html
description: Write semantic, accessible, performant HTML with modern best practices. Use when asked to (1) create HTML pages or documents, (2) write semantic markup, (3) improve accessibility, (4) optimize HTML structure and performance, (5) implement forms, tables, or complex layouts, or when phrases like "HTML page", "web page", "markup", "semantic HTML", "accessibility" appear.
---

# Expert HTML Development

Write clean, semantic, accessible HTML that follows modern web standards and best practices.

## MCP Integration - Context7

**CRITICAL: Before writing or editing ANY HTML code, ALWAYS use the Context7 MCP server to check for relevant context.**

Context7 provides access to a knowledge base that may contain:
- Project-specific HTML patterns and conventions
- Custom component libraries and templates
- Style guide requirements
- Accessibility standards for the project
- Performance benchmarks and requirements
- Team preferences and coding standards

**Workflow:**
1. **Before writing code:** Query Context7 for relevant patterns, conventions, or examples
2. **During editing:** Check Context7 for project-specific requirements that might affect your changes
3. **After writing:** Verify your code aligns with any Context7 guidance

Use Context7 to search for topics like:
- "HTML conventions"
- "accessibility requirements"
- "component templates"
- "form patterns"
- "performance standards"
- Specific component or pattern names

**Never skip the Context7 check** - it ensures your HTML aligns with project standards and leverages existing patterns.

## Core Principles

1. **Semantic first** - Use elements for their intended meaning, not just appearance
2. **Accessibility by default** - Every user deserves a great experience
3. **Progressive enhancement** - Start with working HTML, layer on CSS/JS
4. **Performance matters** - Optimize for speed and efficiency

## Document Structure

### Minimal Valid HTML5 Document

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Site Name</title>
  <meta name="description" content="Clear, concise page description (150-160 chars)">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>
  
  <main>
    <!-- Primary content -->
  </main>
  
  <footer>
    <!-- Footer content -->
  </footer>
  
  <script src="script.js" defer></script>
</body>
</html>
```

### Essential Meta Tags

```html
<head>
  <!-- Character encoding (must be first) -->
  <meta charset="UTF-8">
  
  <!-- Viewport for responsive design -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO basics -->
  <title>Specific, Descriptive Title | Brand</title>
  <meta name="description" content="Clear description for search results">
  <link rel="canonical" href="https://example.com/page">
  
  <!-- Open Graph for social sharing -->
  <meta property="og:title" content="Title for Social Media">
  <meta property="og:description" content="Description for social cards">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Title for Twitter">
  <meta name="twitter:description" content="Description for Twitter">
  <meta name="twitter:image" content="https://example.com/image.jpg">
  
  <!-- Favicon (use multiple sizes for best support) -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  
  <!-- Preload critical resources -->
  <link rel="preload" href="critical-font.woff2" as="font" type="font/woff2" crossorigin>
  
  <!-- Theme color for browser UI -->
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
</head>
```

## Semantic HTML Elements

### Use the Right Element for the Job

```html
<!-- ❌ Generic divs for everything -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
<div class="content">
  <div class="article">
    <div class="title">Article Title</div>
    <div class="text">Article content...</div>
  </div>
</div>

<!-- ✅ Semantic elements with clear meaning -->
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
    <p>Article content...</p>
  </article>
</main>
```

### Sectioning Elements

| Element | Purpose | When to Use |
|---------|---------|-------------|
| `<header>` | Introductory content | Site/section header, not just "top of page" |
| `<nav>` | Navigation links | Primary navigation, table of contents, breadcrumbs |
| `<main>` | Primary content | One per page, skips to main content |
| `<article>` | Self-contained content | Blog posts, news items, forum posts |
| `<section>` | Thematic grouping | Chapters, tabs, themed sections (always has heading) |
| `<aside>` | Tangentially related | Sidebars, pull quotes, related links |
| `<footer>` | Footer content | Site/section footer, not just "bottom of page" |

### Heading Hierarchy

```html
<!-- ✅ Logical hierarchy (never skip levels) -->
<h1>Page Title</h1>
  <h2>Main Section</h2>
    <h3>Subsection</h3>
    <h3>Another Subsection</h3>
  <h2>Another Main Section</h2>

<!-- ❌ Bad: skipping levels -->
<h1>Page Title</h1>
  <h4>Skipped h2 and h3</h4>
```

## Accessibility Best Practices

### ARIA Labels and Roles

```html
<!-- Landmark labels for navigation -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<nav aria-label="Footer navigation">
  <!-- Footer links -->
</nav>

<!-- Button with accessible name -->
<button aria-label="Close dialog">
  <svg aria-hidden="true"><!-- X icon --></svg>
</button>

<!-- Hide decorative content from screen readers -->
<img src="decorative.png" alt="" role="presentation">
<span aria-hidden="true">📧</span>

<!-- Associate labels with inputs -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>

<!-- Or wrap inputs in labels -->
<label>
  Email Address
  <input type="email" name="email" required>
</label>
```

### Focus Management

```html
<!-- Skip to main content link (first interactive element) -->
<a href="#main" class="skip-link">Skip to main content</a>

<main id="main" tabindex="-1">
  <!-- Content -->
</main>

<!-- Ensure custom interactive elements are keyboard accessible -->
<div role="button" tabindex="0" onclick="handleClick()" onkeydown="handleKeyPress(event)">
  Custom Button
</div>
```

### Alternative Text

```html
<!-- ✅ Descriptive alt text -->
<img src="chart.png" alt="Bar chart showing 40% increase in sales from Q1 to Q2 2024">

<!-- ✅ Empty alt for decorative images -->
<img src="decorative-border.png" alt="">

<!-- ✅ Complex images with long descriptions -->
<img src="complex-diagram.png" alt="Network topology diagram" aria-describedby="diagram-desc">
<div id="diagram-desc">
  Detailed description of the network topology showing...
</div>

<!-- ❌ Bad alt text -->
<img src="chart.png" alt="image">
<img src="chart.png" alt="chart.png">
```

### ARIA Live Regions

```html
<!-- Announce dynamic content updates -->
<div role="status" aria-live="polite" aria-atomic="true">
  <span id="status-message">Loading...</span>
</div>

<!-- Alert for critical messages -->
<div role="alert" aria-live="assertive">
  Error: Please correct the form errors below.
</div>
```

## Forms

### Accessible Form Structure

```html
<form method="post" action="/submit" novalidate>
  <fieldset>
    <legend>Personal Information</legend>
    
    <!-- Text input with validation -->
    <label for="name">Full Name</label>
    <input 
      type="text" 
      id="name" 
      name="name" 
      required 
      aria-required="true"
      aria-describedby="name-hint"
      autocomplete="name"
    >
    <small id="name-hint">Enter your first and last name</small>
    
    <!-- Email with pattern validation -->
    <label for="email">Email</label>
    <input 
      type="email" 
      id="email" 
      name="email" 
      required
      aria-required="true"
      autocomplete="email"
      aria-invalid="false"
    >
    <span id="email-error" class="error" role="alert"></span>
    
    <!-- Select with grouped options -->
    <label for="country">Country</label>
    <select id="country" name="country" required>
      <option value="">Select a country</option>
      <optgroup label="North America">
        <option value="us">United States</option>
        <option value="ca">Canada</option>
      </optgroup>
      <optgroup label="Europe">
        <option value="uk">United Kingdom</option>
        <option value="de">Germany</option>
      </optgroup>
    </select>
    
    <!-- Radio buttons (same name groups them) -->
    <fieldset>
      <legend>Preferred Contact Method</legend>
      <label>
        <input type="radio" name="contact" value="email" checked>
        Email
      </label>
      <label>
        <input type="radio" name="contact" value="phone">
        Phone
      </label>
    </fieldset>
    
    <!-- Checkboxes for multiple selection -->
    <fieldset>
      <legend>Newsletter Subscriptions</legend>
      <label>
        <input type="checkbox" name="newsletters" value="weekly">
        Weekly Updates
      </label>
      <label>
        <input type="checkbox" name="newsletters" value="monthly">
        Monthly Digest
      </label>
    </fieldset>
    
    <!-- Textarea with character counter -->
    <label for="message">Message</label>
    <textarea 
      id="message" 
      name="message" 
      rows="5" 
      maxlength="500"
      aria-describedby="char-count"
    ></textarea>
    <small id="char-count">0 / 500 characters</small>
  </fieldset>
  
  <button type="submit">Submit Form</button>
  <button type="reset">Clear Form</button>
</form>
```

### HTML5 Input Types

```html
<!-- Use specific input types for better UX and validation -->
<input type="email" name="email" autocomplete="email">
<input type="tel" name="phone" autocomplete="tel">
<input type="url" name="website">
<input type="number" name="quantity" min="1" max="100" step="1">
<input type="range" name="volume" min="0" max="100" value="50">
<input type="date" name="dob" autocomplete="bday">
<input type="time" name="appointment">
<input type="datetime-local" name="event-time">
<input type="color" name="theme-color" value="#000000">
<input type="file" name="upload" accept="image/*,.pdf" multiple>
<input type="search" name="query" autocomplete="off">
```

### Input Attributes for Better UX

```html
<!-- Autocomplete for faster input -->
<input type="text" name="given-name" autocomplete="given-name">
<input type="text" name="family-name" autocomplete="family-name">
<input type="text" name="address-line1" autocomplete="address-line1">
<input type="text" name="postal-code" autocomplete="postal-code">

<!-- Pattern validation with custom message -->
<input 
  type="text" 
  name="username" 
  pattern="[a-zA-Z0-9_]{3,16}"
  title="Username must be 3-16 characters, letters, numbers, and underscores only"
>

<!-- Autofocus (use sparingly, only once per page) -->
<input type="text" name="search" autofocus>

<!-- Input mode for mobile keyboards -->
<input type="text" inputmode="numeric" name="credit-card">
<input type="text" inputmode="decimal" name="price">
<input type="text" inputmode="email" name="email">
```

## Tables

### Accessible Data Tables

```html
<!-- Simple table with headers -->
<table>
  <caption>Quarterly Sales Report for 2024</caption>
  <thead>
    <tr>
      <th scope="col">Quarter</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Q1</th>
      <td>$1.2M</td>
      <td>+5%</td>
    </tr>
    <tr>
      <th scope="row">Q2</th>
      <td>$1.5M</td>
      <td>+25%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$2.7M</td>
      <td>+15%</td>
    </tr>
  </tfoot>
</table>

<!-- Complex table with headers for rows and columns -->
<table>
  <caption>Course Schedule by Instructor and Day</caption>
  <thead>
    <tr>
      <th scope="col">Instructor</th>
      <th scope="col">Monday</th>
      <th scope="col">Tuesday</th>
      <th scope="col">Wednesday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Dr. Smith</th>
      <td headers="smith monday">Biology 101</td>
      <td headers="smith tuesday">Biology 201</td>
      <td headers="smith wednesday">Lab</td>
    </tr>
  </tbody>
</table>
```

## Lists

### Choosing the Right List Type

```html
<!-- Unordered list (order doesn't matter) -->
<ul>
  <li>Apples</li>
  <li>Bananas</li>
  <li>Oranges</li>
</ul>

<!-- Ordered list (sequence matters) -->
<ol>
  <li>Preheat oven to 350°F</li>
  <li>Mix dry ingredients</li>
  <li>Add wet ingredients</li>
  <li>Bake for 25 minutes</li>
</ol>

<!-- Description list (key-value pairs) -->
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language, the standard markup language for web pages.</dd>
  
  <dt>CSS</dt>
  <dd>Cascading Style Sheets, used to style HTML elements.</dd>
</dl>

<!-- Nested lists -->
<ul>
  <li>Fruits
    <ul>
      <li>Tropical
        <ul>
          <li>Mango</li>
          <li>Papaya</li>
        </ul>
      </li>
      <li>Citrus
        <ul>
          <li>Orange</li>
          <li>Lemon</li>
        </ul>
      </li>
    </ul>
  </li>
</ul>
```

## Performance Optimization

### Image Optimization

```html
<!-- Responsive images with srcset -->
<img 
  src="image-800w.jpg"
  srcset="
    image-400w.jpg 400w,
    image-800w.jpg 800w,
    image-1200w.jpg 1200w,
    image-1600w.jpg 1600w
  "
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
  alt="Descriptive alt text"
  loading="lazy"
  decoding="async"
  width="800"
  height="600"
>

<!-- Art direction with picture element -->
<picture>
  <source media="(max-width: 799px)" srcset="mobile-image.jpg">
  <source media="(min-width: 800px)" srcset="desktop-image.jpg">
  <img src="fallback-image.jpg" alt="Descriptive alt text">
</picture>

<!-- Modern image formats with fallback -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text">
</picture>

<!-- Lazy loading (native) -->
<img src="below-fold-image.jpg" alt="Alt text" loading="lazy">

<!-- Eager loading for above-fold critical images -->
<img src="hero-image.jpg" alt="Alt text" loading="eager" fetchpriority="high">
```

### Resource Loading Strategies

```html
<head>
  <!-- Preconnect to external domains -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://cdn.example.com">
  
  <!-- DNS prefetch for less critical connections -->
  <link rel="dns-prefetch" href="https://analytics.example.com">
  
  <!-- Preload critical resources -->
  <link rel="preload" href="critical-font.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="hero-image.jpg" as="image">
  <link rel="preload" href="critical-styles.css" as="style">
  
  <!-- Prefetch for likely next navigation -->
  <link rel="prefetch" href="/next-page.html">
  <link rel="prefetch" href="next-page-image.jpg" as="image">
</head>

<body>
  <!-- Defer non-critical JavaScript -->
  <script src="analytics.js" defer></script>
  
  <!-- Async for independent scripts -->
  <script src="widget.js" async></script>
  
  <!-- Module scripts (deferred by default) -->
  <script type="module" src="app.js"></script>
  
  <!-- Inline critical CSS, load rest async -->
  <style>
    /* Critical above-fold CSS */
  </style>
  <link rel="stylesheet" href="non-critical.css" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="non-critical.css"></noscript>
</body>
```

### HTML Size Optimization

```html
<!-- ❌ Unnecessary whitespace and comments -->
<div class="container">
  <!-- This is a comment -->
  <p>
    Some text here
  </p>
</div>

<!-- ✅ Minified HTML (use build tools) -->
<div class="container"><p>Some text here</p></div>

<!-- Remove unused attributes -->
<!-- ❌ --> <div id="unused-id" class="unused-class"></div>
<!-- ✅ --> <div></div>

<!-- Combine inline styles (or better, use CSS) -->
<!-- ❌ --> <p style="color: red;"><span style="font-weight: bold;">Text</span></p>
<!-- ✅ --> <p class="error-text">Text</p>
```

## Modern HTML Features

### Details and Summary (Native Disclosure)

```html
<details>
  <summary>Click to expand</summary>
  <p>Hidden content that can be toggled.</p>
</details>

<!-- Open by default -->
<details open>
  <summary>FAQ Question</summary>
  <p>Answer to the question.</p>
</details>
```

### Dialog Element (Native Modal)

```html
<dialog id="myDialog">
  <form method="dialog">
    <h2>Dialog Title</h2>
    <p>Dialog content goes here.</p>
    <button value="cancel">Cancel</button>
    <button value="confirm" autofocus>Confirm</button>
  </form>
</dialog>

<button onclick="document.getElementById('myDialog').showModal()">
  Open Dialog
</button>
```

### Data Attributes

```html
<!-- Store custom data -->
<article data-post-id="12345" data-author="jane-doe" data-category="tech">
  <h2>Article Title</h2>
</article>

<!-- Access in JavaScript: element.dataset.postId -->
<!-- Style in CSS: [data-category="tech"] { } -->
```

### Template Element

```html
<!-- Define reusable markup -->
<template id="item-template">
  <li class="item">
    <h3 class="item-title"></h3>
    <p class="item-description"></p>
  </li>
</template>

<!-- Clone and use with JavaScript -->
<script>
  const template = document.getElementById('item-template');
  const clone = template.content.cloneNode(true);
  // Populate and append
</script>
```

## Content Embedding

### Videos

```html
<!-- Native video with controls -->
<video 
  controls 
  width="640" 
  height="360"
  poster="video-thumbnail.jpg"
  preload="metadata"
>
  <source src="video.webm" type="video/webm">
  <source src="video.mp4" type="video/mp4">
  <track 
    kind="subtitles" 
    src="subtitles-en.vtt" 
    srclang="en" 
    label="English"
  >
  <track 
    kind="captions" 
    src="captions-en.vtt" 
    srclang="en" 
    label="English CC"
    default
  >
  <p>Your browser doesn't support HTML5 video. 
     <a href="video.mp4">Download the video</a> instead.</p>
</video>

<!-- YouTube embed with title for accessibility -->
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube.com/embed/VIDEO_ID" 
  title="Video Title for Accessibility"
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen
  loading="lazy"
></iframe>
```

### Audio

```html
<audio controls preload="metadata">
  <source src="audio.mp3" type="audio/mpeg">
  <source src="audio.ogg" type="audio/ogg">
  <p>Your browser doesn't support HTML5 audio. 
     <a href="audio.mp3">Download the audio</a> instead.</p>
</audio>
```

### Iframes

```html
<!-- Iframe with proper attributes -->
<iframe 
  src="https://example.com/embed"
  title="Descriptive title for screen readers"
  width="600"
  height="400"
  loading="lazy"
  sandbox="allow-scripts allow-same-origin"
></iframe>
```

## Validation and Quality

### HTML Validation Checklist

- [ ] Valid DOCTYPE declaration
- [ ] Proper nesting (no overlapping tags)
- [ ] All tags properly closed
- [ ] Unique IDs on a page
- [ ] Valid attributes for each element
- [ ] Proper character encoding (UTF-8)
- [ ] Alt text for all images (or empty alt for decorative)
- [ ] Form labels associated with inputs
- [ ] Heading hierarchy (no skipped levels)
- [ ] Lang attribute on html tag
- [ ] Valid HTML5 (use W3C validator)

### Common HTML Mistakes to Avoid

```html
<!-- ❌ Block element inside inline element -->
<a href="#"><div>Link content</div></a>

<!-- ✅ Inline element or make the link a block -->
<a href="#" style="display: block"><div>Link content</div></a>

<!-- ❌ Using <br> for spacing -->
<p>First paragraph</p>
<br><br>
<p>Second paragraph</p>

<!-- ✅ Use CSS margins -->
<p>First paragraph</p>
<p style="margin-top: 2rem;">Second paragraph</p>

<!-- ❌ Divitis (unnecessary divs) -->
<div>
  <div>
    <div>
      <p>Content</p>
    </div>
  </div>
</div>

<!-- ✅ Minimal markup -->
<p>Content</p>

<!-- ❌ Empty elements with no purpose -->
<div></div>
<span></span>

<!-- ✅ Remove or add content/styling purpose -->

<!-- ❌ Using tables for layout -->
<table>
  <tr>
    <td>Sidebar</td>
    <td>Main content</td>
  </tr>
</table>

<!-- ✅ Use CSS Grid or Flexbox -->
<div class="layout">
  <aside>Sidebar</aside>
  <main>Main content</main>
</div>
```

## Security Best Practices

### Input Sanitization Context

```html
<!-- Never trust user input - always sanitize on server -->

<!-- ❌ Dangerous: directly embedding user input -->
<div>{{userInput}}</div>

<!-- ✅ Escape HTML entities -->
<div>&lt;script&gt;alert('safe')&lt;/script&gt;</div>

<!-- Use Content Security Policy -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://trusted.cdn.com">
```

### External Resources

```html
<!-- Add integrity checks for external resources -->
<script 
  src="https://cdn.example.com/library.js"
  integrity="sha384-HASH_HERE"
  crossorigin="anonymous"
></script>

<!-- Use rel="noopener" for external links -->
<a href="https://external-site.com" target="_blank" rel="noopener noreferrer">
  External Link
</a>
```

## Progressive Enhancement

### Build from HTML Up

```html
<!-- 1. Start with working HTML -->
<details>
  <summary>Expandable Section</summary>
  <p>Content revealed when expanded.</p>
</details>

<!-- 2. Enhance with CSS (optional) -->
<style>
  details { border: 1px solid #ccc; padding: 1rem; }
  summary { cursor: pointer; font-weight: bold; }
</style>

<!-- 3. Add JavaScript enhancements (optional) -->
<script>
  // Add analytics, animations, or custom behavior
  document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
      if (detail.open) {
        // Track expansion
      }
    });
  });
</script>
```

## Tools and Workflow

### Recommended Tools

| Purpose | Tool | Why |
|---------|------|-----|
| Validation | [W3C Validator](https://validator.w3.org/) | Check HTML validity |
| Accessibility | [axe DevTools](https://www.deque.com/axe/) | Find a11y issues |
| Performance | [Lighthouse](https://developers.google.com/web/tools/lighthouse) | Audit performance |
| HTML Minification | [html-minifier](https://github.com/kangax/html-minifier) | Reduce file size |
| Linting | [HTMLHint](https://htmlhint.com/) | Catch common mistakes |

### HTML in Build Pipelines

```bash
# Validate HTML
npx html-validate src/**/*.html

# Minify HTML
npx html-minifier --collapse-whitespace --remove-comments input.html -o output.html

# Check accessibility
npx pa11y http://localhost:3000
```

## Quick Reference

### Common Character Entities

| Character | Entity | Numeric |
|-----------|--------|---------|
| < | `&lt;` | `&#60;` |
| > | `&gt;` | `&#62;` |
| & | `&amp;` | `&#38;` |
| " | `&quot;` | `&#34;` |
| ' | `&apos;` | `&#39;` |
| © | `&copy;` | `&#169;` |
| ® | `&reg;` | `&#174;` |
| ™ | `&trade;` | `&#8482;` |
| non-breaking space | `&nbsp;` | `&#160;` |
| — (em dash) | `&mdash;` | `&#8212;` |
| – (en dash) | `&ndash;` | `&#8211;` |

### Global Attributes

Available on all HTML elements:

- `id` - Unique identifier
- `class` - CSS class names (space-separated)
- `style` - Inline CSS styles
- `title` - Advisory information (tooltip)
- `lang` - Language of element content
- `dir` - Text directionality (ltr, rtl, auto)
- `hidden` - Hide element
- `tabindex` - Tab order (-1, 0, positive numbers)
- `contenteditable` - Make element editable
- `data-*` - Custom data attributes
- `draggable` - Enable drag and drop
- `spellcheck` - Enable spell checking

## Best Practices Summary

1. **Always check Context7 MCP before writing/editing code** - Leverage project-specific patterns and requirements
2. **Always use semantic HTML** - Choose elements based on meaning, not appearance
3. **Validate your HTML** - Use W3C validator to catch errors
4. **Prioritize accessibility** - Use ARIA attributes, alt text, and keyboard navigation
5. **Optimize for performance** - Lazy load images, defer scripts, minimize HTML
6. **Use progressive enhancement** - Start with HTML, layer on CSS and JavaScript
7. **Keep it simple** - Don't over-engineer with unnecessary divs and complexity
8. **Test across browsers** - Ensure compatibility with all major browsers
9. **Think mobile-first** - Design for small screens, enhance for larger ones
10. **Use meaningful names** - IDs and classes should describe purpose, not appearance
11. **Comment sparingly** - Code should be self-documenting, comments for complex logic only
