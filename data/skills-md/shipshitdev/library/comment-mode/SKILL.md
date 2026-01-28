---
name: comment-mode
description: Granular feedback on drafts without rewriting. Generates highlighted HTML with click-to-reveal inline comments. Use when user says "comment on this", "leave comments on", "give feedback on", or asks for feedback on a draft. Supports multiple lenses—editor feedback, POV simulation ("as brian would react"), or focused angles ("word choice only", "weak arguments"). A granular alternative to rewrites that lets users review feedback incrementally without losing their voice.
---

# Comment Mode

Generate highlighted HTML with click-to-reveal comments for granular feedback on text. Alternative to rewrites—user keeps their voice, reviews feedback incrementally.

## When to Use

- User says: "comment on this", "leave comments on", "give feedback on"
- User pastes text and asks for feedback/critique
- User wants targeted feedback without a full rewrite

## Clarify Before Commenting

Use AskUserQuestion to clarify scope when the request is ambiguous. Avoid over-commenting (overwhelming) or under-commenting (missing the point).

**Clarify when:**

- No lens specified → ask what angle they want
- Long document → ask if they want full coverage or just key sections
- Unclear audience → ask who the recipient is (affects POV comments)

**Skip clarification when:**

- Lens is explicit ("comment on word choice only")
- Document is short (<500 words)
- Context is obvious from conversation

**Example clarification:**

```
User: "comment on this"
[long doc, no lens specified]

→ Use AskUserQuestion:
  "What should I focus on?"
  Options:
  - "Editor feedback (structure, clarity, word choice)"
  - "Recipient POV (how [person] would react)"
  - "Specific angle (tell me what)"
```

## Lenses

| Lens | Color | Comment style |
|------|-------|---------------|
| Editor | Yellow (#fff3cd) | observations, suggestions: "weak opener", "add proof here" |
| POV (as person) | Blue (#e3f2fd) | reactions from that person's perspective: "i know this already", "legal would freak out" |
| Focused | Yellow | specific angle only: "word choice", "tone", "weak arguments" |

## Comment Style

- Always lowercase
- Short (5-15 words)
- Smart about type: observations when noting, suggestions when alternatives help, reactions when simulating POV
- Only comment where there's something worth saying—sparse beats exhaustive

## Output Rules

**DO:**

- Write to `_private/views/{name}-comments-temp.html`
- Open with `open _private/views/{name}-comments-temp.html`
- Use highlight colors matching the lens
- Keep comments sparse and high-signal

**DO NOT:**

- Comment on everything—only where there's an obvious edit or insight
- Over-explain in comments—keep them punchy
- Mix lenses in one output—pick one and stick to it

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 700px;
      margin: 0 auto;
      padding: 40px 20px;
      line-height: 1.7;
      color: #1a1a1a;
      background: #fafafa;
    }
    h1, h2, h3 { margin-top: 2em; font-weight: 600; }
    h1 { font-size: 1.4em; }
    h2 { font-size: 1.2em; color: #333; }
    p { margin: 1em 0; }

    .highlight {
      background: {highlight-bg};  /* #fff3cd yellow for editor, #e3f2fd blue for POV */
      padding: 1px 4px;
      border-radius: 3px;
      cursor: pointer;
      border-bottom: 2px solid {highlight-border};  /* #ffc107 for editor, #2196f3 for POV */
      transition: background 0.15s;
    }
    .highlight:hover, .highlight.active {
      background: {highlight-hover};  /* #ffe69c for editor, #bbdefb for POV */
    }

    .comment {
      display: none;
      background: {comment-bg};  /* #1a1a1a for editor, #0052cc for POV */
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.85em;
      margin: 8px 0;
      line-height: 1.5;
    }
    .comment.show { display: block; }

    .section-break {
      border: none;
      border-top: 1px solid #ddd;
      margin: 2em 0;
    }

    .legend {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.1);
      font-size: 0.8em;
      color: #666;
    }
  </style>
</head>
<body>

{content with <span class="highlight" data-comment="comment text">highlighted phrase</span>}

<div class="legend">{count} comments · click highlights to reveal</div>

<script>
document.querySelectorAll('.highlight').forEach(el => {
  const commentText = el.getAttribute('data-comment');
  const commentDiv = document.createElement('div');
  commentDiv.className = 'comment';
  commentDiv.textContent = commentText;
  el.insertAdjacentElement('afterend', commentDiv);

  el.addEventListener('click', () => {
    const wasActive = el.classList.contains('active');
    document.querySelectorAll('.highlight').forEach(h => h.classList.remove('active'));
    document.querySelectorAll('.comment').forEach(c => c.classList.remove('show'));
    if (!wasActive) {
      el.classList.add('active');
      commentDiv.classList.add('show');
    }
  });
});
</script>
</body>
</html>
```

### Color Reference

**Editor lens (yellow):**

```css
.highlight { background: #fff3cd; border-bottom: 2px solid #ffc107; }
.highlight:hover, .highlight.active { background: #ffe69c; }
.comment { background: #1a1a1a; }
```

**POV lens (blue):**

```css
.highlight { background: #e3f2fd; border-bottom: 2px solid #2196f3; }
.highlight:hover, .highlight.active { background: #bbdefb; }
.comment { background: #0052cc; }
```

## Workflow

1. User pastes text + asks for comments
2. **If ambiguous**: Use AskUserQuestion to clarify lens/scope
3. Read text, identify key phrases worth commenting on (sparse, high-signal)
4. Generate HTML with highlights and `data-comment` attributes
5. Write to `_private/views/{name}-comments-temp.html`
6. Run `open _private/views/{name}-comments-temp.html`

## Examples

**Editor lens:**

```
User: "comment on this, focus on word choice"
→ Yellow highlights, suggestions like "vague, try 'specifically'" or "jargon, simplify"
```

**POV lens:**

```
User: "comment on this as brian would react"
→ Blue highlights, reactions like "i already know this" or "legal would push back here"
```

**Focused lens:**

```
User: "leave comments on this, only flag weak arguments"
→ Yellow highlights on weak claims, comments like "needs evidence" or "assumes too much"
```

**Sparse/sharp lens:**

```
User: "comment only where there's an obvious fix"
→ Minimal highlights, only typos, missing words, or clear improvements
```
