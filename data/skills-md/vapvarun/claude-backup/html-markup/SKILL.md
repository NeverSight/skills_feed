---
name: html-markup
description: Write semantic, accessible HTML5 markup following best practices for structure, SEO, and accessibility. Use when creating HTML templates, fixing markup issues, or building web page structures.
---

# HTML Markup Skill

## Instructions

When writing HTML:

### 1. Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description for SEO">
  <title>Page Title | Brand</title>

  <!-- Preconnect to external domains -->
  <link rel="preconnect" href="https://fonts.googleapis.com">

  <!-- Critical CSS inline -->
  <style>/* Critical styles */</style>

  <!-- External stylesheets -->
  <link rel="stylesheet" href="styles.css">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
</head>
<body>
  <!-- Content -->

  <!-- Scripts at end -->
  <script src="main.js" defer></script>
</body>
</html>
```

### 2. Semantic Elements

```html
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time datetime="2025-01-15">January 15, 2025</time>
    </header>

    <section>
      <h2>Section Heading</h2>
      <p>Content...</p>
    </section>

    <aside>
      <h3>Related Content</h3>
    </aside>

    <footer>
      <p>Article footer content</p>
    </footer>
  </article>
</main>

<aside aria-label="Sidebar">
  <section>
    <h2>Widget Title</h2>
  </section>
</aside>

<footer>
  <nav aria-label="Footer navigation">
    <!-- Footer links -->
  </nav>
  <p>&copy; 2025 Company Name</p>
</footer>
```

### 3. Headings Hierarchy

```html
<!-- Correct hierarchy -->
<h1>Page Title (one per page)</h1>
  <h2>Main Section</h2>
    <h3>Subsection</h3>
      <h4>Sub-subsection</h4>
  <h2>Another Main Section</h2>
    <h3>Subsection</h3>

<!-- Never skip levels -->
<!-- ❌ Bad: h1 → h3 -->
<!-- ✓ Good: h1 → h2 → h3 -->
```

### 4. Forms

```html
<form action="/submit" method="POST" novalidate>
  <fieldset>
    <legend>Contact Information</legend>

    <div class="form-group">
      <label for="name">Full Name <span aria-hidden="true">*</span></label>
      <input
        type="text"
        id="name"
        name="name"
        required
        autocomplete="name"
        aria-required="true"
      >
    </div>

    <div class="form-group">
      <label for="email">Email Address</label>
      <input
        type="email"
        id="email"
        name="email"
        required
        autocomplete="email"
        aria-describedby="email-hint"
      >
      <p id="email-hint" class="hint">We'll never share your email.</p>
    </div>

    <div class="form-group">
      <label for="message">Message</label>
      <textarea
        id="message"
        name="message"
        rows="5"
        required
      ></textarea>
    </div>

    <div class="form-group">
      <input type="checkbox" id="newsletter" name="newsletter">
      <label for="newsletter">Subscribe to newsletter</label>
    </div>
  </fieldset>

  <button type="submit">Send Message</button>
</form>
```

### 5. Images

```html
<!-- Standard image -->
<img
  src="image.jpg"
  alt="Descriptive alt text"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>

<!-- Responsive images -->
<picture>
  <source
    media="(min-width: 1200px)"
    srcset="large.webp"
    type="image/webp"
  >
  <source
    media="(min-width: 800px)"
    srcset="medium.webp"
    type="image/webp"
  >
  <img
    src="small.jpg"
    alt="Description"
    width="400"
    height="300"
    loading="lazy"
  >
</picture>

<!-- Figure with caption -->
<figure>
  <img src="chart.png" alt="Sales growth chart showing 50% increase">
  <figcaption>Fig 1: Sales growth Q1-Q4 2024</figcaption>
</figure>

<!-- Decorative image -->
<img src="decoration.svg" alt="" role="presentation">
```

### 6. Links

```html
<!-- Internal link -->
<a href="/about">About Us</a>

<!-- External link -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Site
  <span class="visually-hidden">(opens in new tab)</span>
</a>

<!-- Download link -->
<a href="/file.pdf" download>Download PDF</a>

<!-- Skip link (accessibility) -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Anchor link -->
<a href="#section-2">Jump to Section 2</a>
```

### 7. Lists

```html
<!-- Unordered list -->
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- Ordered list -->
<ol>
  <li>First step</li>
  <li>Second step</li>
</ol>

<!-- Description list -->
<dl>
  <dt>Term</dt>
  <dd>Definition</dd>

  <dt>Another term</dt>
  <dd>Its definition</dd>
</dl>

<!-- Navigation list -->
<nav>
  <ul role="list">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

### 8. Tables

```html
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
      <td>+5%</td>
    </tr>
    <tr>
      <th scope="row">February</th>
      <td>$12,000</td>
      <td>+20%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$22,000</td>
      <td>—</td>
    </tr>
  </tfoot>
</table>
```

### 9. Interactive Elements

```html
<!-- Button -->
<button type="button" onclick="handleClick()">
  Click Me
</button>

<!-- Details/Summary (accordion) -->
<details>
  <summary>Click to expand</summary>
  <p>Hidden content revealed on click.</p>
</details>

<!-- Dialog/Modal -->
<dialog id="modal">
  <h2>Modal Title</h2>
  <p>Modal content</p>
  <button onclick="document.getElementById('modal').close()">
    Close
  </button>
</dialog>
```

### 10. Accessibility Checklist

- [ ] All images have alt text
- [ ] Proper heading hierarchy
- [ ] Form inputs have labels
- [ ] Links are descriptive
- [ ] Color isn't only indicator
- [ ] Focus states visible
- [ ] Skip link present
- [ ] ARIA used correctly
- [ ] Keyboard navigable
- [ ] Language declared
