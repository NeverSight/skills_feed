---
name: ie6-hacks
description: Internet Explorer 6 CSS and JavaScript compatibility patterns reference. Use when identifying legacy browser-specific code for removal during codebase modernization, explaining unusual CSS patterns in legacy systems, or auditing stylesheets for deprecated workarounds.
license: MIT
metadata:
  author: adriancooney
  version: "1.0.0"
  tags: css, javascript, legacy, ie6, browser-compatibility
---

# IE6 Compatibility Patterns Reference

Technical reference for identifying and removing Internet Explorer 6 CSS and JavaScript compatibility patterns from legacy codebases.

## When to Use This Skill

- Identifying IE6-specific code that can be safely removed
- Explaining unusual CSS patterns in legacy codebases
- Auditing stylesheets for deprecated browser workarounds
- Modernizing legacy codebases

## Removal Guidelines

All IE6 patterns documented here can be safely removed from modern codebases. IE6 usage is effectively zero. After removal, test to ensure no accidental side effects (some hacks like `zoom: 1` occasionally fixed unrelated issues).

---

## 1. Star-HTML Hack

### Identify
```css
* html .selector { }
* html #id { }
* html body .class { }
```

### Problem
IE6 incorrectly treated `<html>` as if it had a parent element in the DOM, allowing `* html` to match. Standards-compliant browsers correctly ignore this selector since `html` is the root element.

### Example
```css
/* Before: IE6 hack present */
.sidebar {
  margin-left: 200px;
}
* html .sidebar {
  margin-left: 180px;
}

/* After: Remove the * html rule entirely */
.sidebar {
  margin-left: 200px;
}
```

### Fix
Delete any rule starting with `* html`.

---

## 2. Underscore Hack

### Identify
```css
.selector {
  _property: value;
  _margin: 10px;
  _display: block;
}
```

### Problem
IE6 ignored leading underscores in property names while other browsers treated them as invalid. This allowed targeting IE6 specifically within the same rule.

### Example
```css
/* Before: IE6 hack present */
.box {
  padding: 20px;
  _padding: 15px;
}

/* After: Remove underscore-prefixed properties */
.box {
  padding: 20px;
}
```

### Fix
Delete any property starting with `_`.

---

## 3. Double Margin Float Bug

### Identify
```css
.selector {
  float: left;
  margin-left: 20px;
  display: inline; /* This is the hack */
}
```

### Problem
IE6 doubled margins on floated elements when the margin was in the same direction as the float. Adding `display: inline` fixed this (despite floated elements already being block-level).

### Example
```css
/* Before: IE6 hack present */
.sidebar {
  float: left;
  margin-left: 20px;
  display: inline;
}

/* After: Remove display: inline from floated elements */
.sidebar {
  float: left;
  margin-left: 20px;
}
```

### Fix
Remove `display: inline` from elements that have `float` set. Note: Only remove if the element is floated; `display: inline` may be intentional in other contexts.

---

## 4. PNG Transparency (AlphaImageLoader)

### Identify
```css
.selector {
  filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src='image.png', sizingMethod='crop');
  _filter: progid:DXImageTransform.Microsoft.AlphaImageLoader();
  behavior: url(iepngfix.htc);
}
```

```html
<!--[if IE 6]>
<script src="DD_belatedPNG.js"></script>
<script>DD_belatedPNG.fix('.png-fix');</script>
<![endif]-->
```

### Problem
IE6 couldn't render PNG alpha transparency natively, displaying a grey background instead of transparency. The AlphaImageLoader filter was a proprietary workaround.

### Example
```css
/* Before: IE6 PNG hack present */
.logo {
  background: url(logo.png) no-repeat;
  _background: none;
  _filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(
    src='logo.png',
    sizingMethod='crop'
  );
}

/* After: Remove filter and underscore properties */
.logo {
  background: url(logo.png) no-repeat;
}
```

### Fix
Remove all `filter: progid:DXImageTransform` rules, `behavior: url(*.htc)` rules, and any associated `.htc` files or PNG-fix JavaScript libraries.

---

## 5. hasLayout / zoom:1

### Identify
```css
.selector {
  zoom: 1;
}
.selector {
  *zoom: 1; /* Star hack variant */
}
```

### Problem
IE6/7 had an internal concept called "hasLayout" that affected how elements rendered. Many bugs were caused by elements not "having layout." Setting `zoom: 1` triggered hasLayout without visual side effects.

### Example
```css
/* Before: IE6 hasLayout hack present */
.container {
  background: #eee;
  zoom: 1;
}

/* After: Remove zoom: 1 */
.container {
  background: #eee;
}
```

### Fix
Remove `zoom: 1` declarations. If `zoom` has any value other than `1`, verify intent before removing. Test after removal as `zoom: 1` occasionally fixed unrelated layout issues.

---

## 6. Peekaboo Bug (Holly Hack)

### Identify
```css
.selector {
  height: 1%;
}
/* Often combined with */
* html .selector {
  height: 1%;
}
```

### Problem
IE6 had a bug where content inside floated containers would randomly disappear until the user scrolled or resized the window. Setting `height: 1%` (the "Holly hack") triggered hasLayout and fixed this.

### Example
```css
/* Before: Holly hack present */
.wrapper {
  background: #fff;
  height: 1%;
}

/* After: Remove height: 1% if it was only for IE6 */
.wrapper {
  background: #fff;
}
```

### Fix
Remove `height: 1%` if the element doesn't need a specific height. Verify the height isn't being used for actual layout purposes before removing.

---

## 7. Box Model Hack

### Identify
```css
.selector {
  width: 250px;
  voice-family: "\"}\"";
  voice-family: inherit;
  width: 200px;
}
html>body .selector {
  width: 200px;
}
```

### Problem
IE5 and IE6 in quirks mode calculated width incorrectly, including padding and border inside the width. The voice-family hack exploited a CSS parsing bug to serve different widths to different browsers.

### Example
```css
/* Before: Box model hack present */
.box {
  width: 250px;
  voice-family: "\"}\"";
  voice-family: inherit;
  width: 200px;
}
html>body .box {
  width: 200px;
}

/* After: Remove the hack, keep intended width */
.box {
  width: 200px;
}
```

### Fix
Remove `voice-family` declarations and duplicate width/height properties. Remove `html>body` selector rules if they only exist to reset box model values. Keep the standards-compliant value.

---

## 8. Min-Height Hack

### Identify
```css
.selector {
  min-height: 300px;
  height: auto !important;
  height: 300px;
}
/* Or */
.selector {
  min-height: 300px;
  _height: 300px;
}
```

### Problem
IE6 didn't support `min-height` but incorrectly treated `height` as a minimum height (allowing content to expand the element). This hack exploited that behavior.

### Example
```css
/* Before: min-height hack present */
.panel {
  min-height: 300px;
  height: auto !important;
  height: 300px;
}

/* After: Keep only min-height */
.panel {
  min-height: 300px;
}
```

### Fix
Remove duplicate `height` declarations and `!important` overrides that exist only for IE6 compatibility. Keep the `min-height` value.

---

## 9. CSS Expressions

### Identify
```css
.selector {
  width: expression(document.body.clientWidth > 800 ? "800px" : "auto");
  height: expression(this.scrollHeight > 300 ? "300px" : "auto");
  background-color: expression((new Date()).getHours() > 12 ? "#fff" : "#000");
}
```

### Problem
IE6 didn't support `min-width`, `max-width`, `min-height`, or `max-height`. CSS expressions allowed embedding JavaScript directly in CSS to calculate values dynamically. These were performance-intensive as they re-evaluated constantly.

### Example
```css
/* Before: CSS expression present */
.content {
  max-width: 800px;
  min-width: 400px;
  width: expression(
    document.body.clientWidth < 401 ? "400px" :
    document.body.clientWidth > 801 ? "800px" : "auto"
  );
}

/* After: Remove expression, keep standard properties */
.content {
  max-width: 800px;
  min-width: 400px;
}
```

### Fix
Remove all `expression()` values. The standard CSS properties (`min-width`, `max-width`, etc.) will work in all modern browsers.

---

## 10. Conditional Comments

### Identify
```html
<!--[if IE 6]>
<link rel="stylesheet" href="ie6.css" />
<![endif]-->

<!--[if lt IE 7]>
<script src="ie6-fixes.js"></script>
<![endif]-->

<!--[if lte IE 6]>
<style>.selector { margin: 10px; }</style>
<![endif]-->
```

### Problem
Microsoft's official method for targeting specific IE versions. While cleaner than CSS hacks, these still load unnecessary resources for a browser that no longer exists.

### Operators
- `IE 6` - exactly IE6
- `lt IE 7` - less than IE7 (IE6 and below)
- `lte IE 7` - less than or equal to IE7
- `gt IE 6` - greater than IE6
- `gte IE 6` - greater than or equal to IE6

### Example
```html
<!-- Before: Conditional comments present -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="main.css" />
  <!--[if IE 6]>
  <link rel="stylesheet" href="ie6.css" />
  <![endif]-->
  <!--[if lt IE 9]>
  <script src="html5shiv.js"></script>
  <![endif]-->
</head>

<!-- After: Remove IE6-specific conditionals -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="main.css" />
  <!--[if lt IE 9]>
  <script src="html5shiv.js"></script>
  <![endif]-->
</head>
```

### Fix
Remove conditional comments targeting IE6 specifically (`[if IE 6]`, `[if lt IE 7]`, `[if lte IE 6]`). Also delete the referenced files (ie6.css, etc.). Conditionals targeting IE7+ may still be needed in some enterprise environments—verify before removing.

---

## Quick Reference: Patterns to Search For

```
* html
_margin
_padding
_display
_width
_height
_filter
zoom: 1
*zoom
height: 1%
voice-family
expression(
progid:DXImageTransform
AlphaImageLoader
behavior: url(
.htc
<!--[if IE 6]>
<!--[if lt IE 7]>
<!--[if lte IE 6]>
DD_belatedPNG
iepngfix
```
