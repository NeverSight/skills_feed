---
name: codefocus
description: CodeFocus for Quarto Revealjs. Use when creating presentations with progressive code highlighting.
---

# CodeFocus for Quarto Revealjs

Use this syntax to add progressive code highlighting with explanations in Quarto revealjs presentations.

## When to use

- When creating Quarto revealjs presentations
- When you need step-by-step code walkthroughs
- When teaching code concepts progressively

## Setup

1. Install the extension:

```bash
quarto add reuning/codefocus
```

2. Add to `_quarto.yml`:

```yaml
revealjs-plugins:
  - codefocus
```

## Instructions

### Syntax

````markdown
## Slide Title

```python
import requests
import json

api_url = "https://api.example.com/data"
headers = {"Authorization": "Bearer token"}

response = requests.get(api_url, headers=headers)
data = response.json()
```

::: {.fragment .current-only data-code-focus="1-2"}
First, we import the required libraries for HTTP requests and JSON handling.
:::

::: {.fragment .current-only data-code-focus="4-5"}
Define the API endpoint URL and authentication headers.
:::

::: {.fragment .current-only data-code-focus="7-8"}
Make the GET request and parse the JSON response.
:::
````

### Key Attributes

- **`.fragment`** - Makes content appear progressively
- **`.current-only`** - Fragment disappears when advancing (keeps slide clean)
- **`data-code-focus="N"`** - Line number to highlight (1-indexed)
- **`data-code-focus="1-3"`** - Range of lines
- **`data-code-focus="1,3,5"`** - Multiple specific lines

## Notes

- Code block must come BEFORE the fragment divs
- Each fragment highlights different lines as you press arrow keys
- The explanation text appears below the code when that fragment is active
