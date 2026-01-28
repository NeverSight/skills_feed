---
name: discord-markdown
description: >-
  Discord-specific markdown syntax for formatting message strings. Use when
  constructing strings that will be sent as Discord messages, including:
  text formatting (bold, italic, underline, strikethrough, spoilers),
  headers, subtext, code blocks, block quotes, lists, and masked links.
---

# Discord Markdown

Discord uses a variant of Markdown with some unique syntax. Key differences from standard Markdown:
- Underline: `__text__` (not standard)
- Spoilers: `||text||`
- Subtext: `-# text`
- Combinations like underline+bold+italic

## Text Formatting

| Style | Syntax | Example |
|-------|--------|---------|
| Italic | `*text*` or `_text_` | *italic* |
| Bold | `**text**` | **bold** |
| Bold Italic | `***text***` | ***bold italic*** |
| Underline | `__text__` | |
| Strikethrough | `~~text~~` | ~~strikethrough~~ |
| Spoiler | `\|\|text\|\|` | (hidden until clicked) |

### Combinations

```
__*underline italic*__
__**underline bold**__
__***underline bold italic***__
```

## Headers

Require a space after `#`. Must be at line start.

```
# Large Header
## Medium Header
### Small Header
```

## Subtext

Small, subdued text. Requires space after `-#`. Must be at line start.

```
-# This appears as subtext
```

## Code

Inline: `` `code` ``

Multi-line:
````
```
code block
multiple lines
```
````

With syntax highlighting:
````
```python
print("hello")
```
````

## Block Quotes

Single line (space required after `>`):
```
> This is a quote
```

Multi-line (everything after `>>>` is quoted):
```
>>> This is a
multi-line quote
```

## Lists

Bulleted (space required after `-` or `*`):
```
- Item one
- Item two
* Also works
```

Indented (2 spaces before bullet):
```
- Parent
  - Child
  - Child
```

Numbered:
```
1. First
2. Second
```

## Masked Links

```
[Click here](https://example.com)
```

## Common Patterns

Formatted user mention: `<@user_id>`
Formatted channel: `<#channel_id>`
Formatted role: `<@&role_id>`
Custom emoji: `<:name:id>` or `<a:name:id>` (animated)
Timestamp: `<t:unix_timestamp:format>`

Timestamp formats: `t` (short time), `T` (long time), `d` (short date), `D` (long date), `f` (short datetime), `F` (long datetime), `R` (relative)
