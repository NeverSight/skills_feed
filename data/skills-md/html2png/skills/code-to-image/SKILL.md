---
name: code-to-image
description: Generate beautiful code snippet images with syntax highlighting. Use when users want to share code as an image, create code screenshots for social media, documentation, or presentations. Produces crisp, syntax-highlighted code with customizable themes, window chrome, and professional styling.
---

# Code to Image API

Generate beautiful code snippet images with syntax highlighting via `html2png.dev`.

## How It Works

1. Write HTML with syntax-highlighted code (use Shiki or similar)
2. Style with Tailwind CSS or custom CSS
3. Send to `/api/convert` endpoint
4. Get a shareable image URL

## Endpoint

```
POST https://html2png.dev/api/convert
```

## Example

```bash
curl -X POST "https://html2png.dev/api/convert?width=800&deviceScaleFactor=2" \
  -H "Content-Type: text/html" \
  -d '<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    .shiki { background: transparent !important; }
    .line::before {
      content: attr(data-line);
      width: 2rem;
      margin-right: 1rem;
      display: inline-block;
      text-align: right;
      color: rgba(128,128,128,0.4);
    }
  </style>
</head>
<body class="p-12" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
  <div class="bg-white rounded-xl shadow-2xl overflow-hidden">
    <div class="flex items-center gap-2 px-4 py-3 border-b border-gray-200">
      <div class="w-3 h-3 rounded-full bg-red-400"></div>
      <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
      <div class="w-3 h-3 rounded-full bg-green-400"></div>
      <span class="ml-2 text-xs text-gray-500 font-mono">hello.js</span>
    </div>
    <pre class="p-6 font-mono text-sm leading-relaxed"><code class="language-javascript"><span style="color:#D73A49">function</span> <span style="color:#6F42C1">greet</span>(<span style="color:#24292E">name</span>) {
  <span style="color:#D73A49">return</span> <span style="color:#032F62">`Hello, ${name}!`</span>;
}

<span style="color:#6F42C1">console</span>.<span style="color:#6F42C1">log</span>(<span style="color:#6F42C1">greet</span>(<span style="color:#032F62">"World"</span>));</code></pre>
  </div>
</body>
</html>'
```

## Key Elements

**Syntax Highlighting:**

- Use Shiki (`shiki.style`) or highlight.js for token coloring
- Inline styles work best for standalone images

**Window Chrome:**

- Traffic light dots (red, yellow, green)
- Filename in title bar
- Rounded corners, shadows

**Typography:**

- JetBrains Mono or Fira Code for code
- Inter or system fonts for UI elements
- Line numbers optional

**Backgrounds:**

- Gradient backgrounds for the container
- White or dark code window
- Glassmorphism effects

## Shiki Integration

For server-side syntax highlighting:

```javascript
import { createHighlighter } from "shiki";

const highlighter = await createHighlighter({
  themes: ["github-light"],
  langs: ["javascript", "python", "rust"],
});

const html = highlighter.codeToHtml(code, {
  lang: "javascript",
  theme: "github-light",
});
```

## Tips

- Use `deviceScaleFactor=2` for crisp text
- Add `delay=500` if using web fonts
- Container width should match `width` param
- Use `omitBackground=true` for transparent PNGs

## Rate Limits

50 requests/hour per IP.
