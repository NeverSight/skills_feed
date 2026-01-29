---
name: nitro-ui
description: Generate NitroUI code - a Python library for programmatic HTML generation using classes instead of templates
---

# NitroUI Skill Guide

A zero-dependency Python 3.8+ library for programmatic HTML generation. Build HTML with Python classes instead of string templates.

```python
from nitro_ui import Div, H1, Paragraph

page = Div(
    H1("Welcome"),
    Paragraph("Built with NitroUI"),
    cls="container"
)
print(page.render())
# <div class="container"><h1>Welcome</h1><p>Built with NitroUI</p></div>
```

---

## Two Import Styles

### PascalCase (Traditional)
```python
from nitro_ui import Div, H1, Paragraph, UnorderedList, ListItem, Image
```

### Lowercase HTML-like
```python
from nitro_ui.html import div, h1, p, ul, li, img, a, table, tr, td

page = div(
    h1("Title"),
    p("This looks like HTML!"),
    ul(
        li(a("Home", href="/")),
        li(a("About", href="/about")),
    ),
    cls="container"
)
```

### Python Keyword Conflicts (trailing underscore)
```python
from nitro_ui.html import del_, input_, object_, map_

form_field = input_(type="text", name="username")  # <input>
deleted = del_("removed text")                      # <del>
```

### Selective Core Imports
```python
from nitro_ui.core.element import HTMLElement
from nitro_ui.core.fragment import Fragment
from nitro_ui.core.partial import Partial
from nitro_ui.core.parser import from_html
from nitro_ui.styles import CSSStyle, StyleSheet, Theme
```

---

## All Tags

### Document Structure
| PascalCase | Lowercase | HTML | Notes |
|------------|-----------|------|-------|
| `HTML` | `html` | `<html>` | Includes `<!DOCTYPE html>` |
| `Head` | `head` | `<head>` | |
| `Body` | `body` | `<body>` | |
| `Title` | `title` | `<title>` | |
| `Meta` | `meta` | `<meta>` | Self-closing |
| `HtmlLink` | `link` | `<link>` | Self-closing. `HtmlLink` avoids confusion with `Href` |
| `Script` | `script` | `<script>` | |
| `Style` | `style` | `<style>` | |
| `Base` | `base` | `<base>` | Self-closing |
| `Noscript` | `noscript` | `<noscript>` | |
| `IFrame` | `iframe` | `<iframe>` | |

### Layout
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `Div` | `div` | `<div>` |
| `Section` | `section` | `<section>` |
| `Article` | `article` | `<article>` |
| `Header` | `header` | `<header>` |
| `Footer` | `footer` | `<footer>` |
| `Nav` | `nav` | `<nav>` |
| `Main` | `main` | `<main>` |
| `Aside` | `aside` | `<aside>` |
| `HorizontalRule` | `hr` | `<hr>` (self-closing) |
| `Details` | `details` | `<details>` |
| `Summary` | `summary` | `<summary>` |
| `Dialog` | `dialog` | `<dialog>` |

### Text
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `H1`-`H6` | `h1`-`h6` | `<h1>`-`<h6>` |
| `Paragraph` | `p` | `<p>` |
| `Span` | `span` | `<span>` |
| `Strong` | `strong` | `<strong>` |
| `Em` | `em` | `<em>` |
| `Bold` | `b` | `<b>` |
| `Italic` | `i` | `<i>` |
| `Underline` | `u` | `<u>` |
| `Strikethrough` | `s` | `<s>` |
| `Small` | `small` | `<small>` |
| `Mark` | `mark` | `<mark>` |
| `Del` | `del_` | `<del>` |
| `Ins` | `ins` | `<ins>` |
| `Subscript` | `sub` | `<sub>` |
| `Superscript` | `sup` | `<sup>` |
| `Code` | `code` | `<code>` |
| `Pre` | `pre` | `<pre>` |
| `Kbd` | `kbd` | `<kbd>` |
| `Samp` | `samp` | `<samp>` |
| `Var` | `var` | `<var>` |
| `Blockquote` | `blockquote` | `<blockquote>` |
| `Quote` | `q` | `<q>` |
| `Cite` | `cite` | `<cite>` |
| `Abbr` | `abbr` | `<abbr>` |
| `Dfn` | `dfn` | `<dfn>` |
| `Time` | `time` | `<time>` |
| `Href` | `a` | `<a>` |
| `Br` | `br` | `<br>` (self-closing) |
| `Wbr` | `wbr` | `<wbr>` (self-closing) |

### Lists
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `UnorderedList` | `ul` | `<ul>` |
| `OrderedList` | `ol` | `<ol>` |
| `ListItem` | `li` | `<li>` |
| `Datalist` | `datalist` | `<datalist>` |
| `DescriptionList` | `dl` | `<dl>` |
| `DescriptionTerm` | `dt` | `<dt>` |
| `DescriptionDetails` | `dd` | `<dd>` |

### Forms
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `Form` | `form` | `<form>` |
| `Input` | `input_` | `<input>` (self-closing) |
| `Button` | `button` | `<button>` |
| `Textarea` | `textarea` | `<textarea>` |
| `Select` | `select` | `<select>` |
| `Option` | `option` | `<option>` |
| `Optgroup` | `optgroup` | `<optgroup>` |
| `Label` | `label` | `<label>` |
| `Fieldset` | `fieldset` | `<fieldset>` |
| `Legend` | `legend` | `<legend>` |
| `Output` | `output` | `<output>` |
| `Progress` | `progress` | `<progress>` |
| `Meter` | `meter` | `<meter>` |

### Tables
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `Table` | `table` | `<table>` |
| `TableHeader` | `thead` | `<thead>` |
| `TableBody` | `tbody` | `<tbody>` |
| `TableFooter` | `tfoot` | `<tfoot>` |
| `TableRow` | `tr` | `<tr>` |
| `TableHeaderCell` | `th` | `<th>` |
| `TableDataCell` | `td` | `<td>` |
| `Caption` | `caption` | `<caption>` |
| `Colgroup` | `colgroup` | `<colgroup>` |
| `Col` | `col` | `<col>` (self-closing) |

`Table.from_json(path)` and `Table.from_csv(path)` create tables from files (first row = headers in `<thead>`, rest in `<tbody>`).

### Media
| PascalCase | Lowercase | HTML |
|------------|-----------|------|
| `Image` | `img` | `<img>` (self-closing) |
| `Video` | `video` | `<video>` |
| `Audio` | `audio` | `<audio>` |
| `Source` | `source` | `<source>` (self-closing) |
| `Track` | `track` | `<track>` (self-closing) |
| `Picture` | `picture` | `<picture>` |
| `Figure` | `figure` | `<figure>` |
| `Figcaption` | `figcaption` | `<figcaption>` |
| `Canvas` | `canvas` | `<canvas>` |
| `Embed` | `embed` | `<embed>` (self-closing) |
| `Object` | `object_` | `<object>` |
| `Param` | `param` | `<param>` (self-closing) |
| `Map` | `map_` | `<map>` |
| `Area` | `area` | `<area>` (self-closing) |

---

## HTMLElement Constructor

```python
HTMLElement(
    *children,                  # HTMLElement, str, or nested lists (auto-flattened)
    tag: str,                   # Required HTML tag name
    self_closing: bool = False,
    **attributes                # HTML attributes as keyword arguments
)
```

**Special attribute mappings:**
- `cls` or `class_name` → renders as `class`
- `class_` → also maps to `class_name`
- `for_element` or `for_` → renders as `for`
- `data_*` → `data-*` (other underscores become hyphens)

```python
div = Div(
    H1("Title"),
    "Some text",
    id="main",
    cls="container",
    data_value="123"
)
# <div id="main" class="container" data-value="123"><h1>Title</h1>Some text</div>
```

### Properties

| Property | Type | Mutable | Notes |
|----------|------|---------|-------|
| `tag` | `str` | Yes | HTML tag name |
| `children` | `List[HTMLElement]` | Yes | Use methods preferred |
| `text` | `str` | Yes | Text content |
| `attributes` | `dict` | Yes | Setting invalidates style cache |
| `self_closing` | `bool` | Yes | |

---

## All Methods

### Children

| Method | Returns | Description |
|--------|---------|-------------|
| `append(*children)` | `self` | Add children to end |
| `prepend(*children)` | `self` | Add children to start |
| `clear()` | `self` | Remove all children |
| `pop(index=0)` | `HTMLElement` | Remove and return child |
| `remove_all(condition)` | `self` | Remove matching children |
| `replace_child(index, new)` | `None` | Replace child at index (not chainable) |
| `count_children()` | `int` | Number of direct children |
| `first()` | `HTMLElement\|None` | First child |
| `last()` | `HTMLElement\|None` | Last child |
| `filter(cond, recursive=False, max_depth=1000)` | `Iterator` | Matching children/descendants |
| `find_by_attribute(key, value, max_depth=1000)` | `HTMLElement\|None` | First descendant with matching attr |

Children can be `HTMLElement`, `str`, or nested lists. `None` is silently ignored. Other types raise `ValueError`.

### Attributes

| Method | Returns | Description |
|--------|---------|-------------|
| `add_attribute(key, value)` | `self` | Set single attribute |
| `add_attributes([(k,v),...])` | `self` | Set multiple attributes |
| `remove_attribute(key)` | `self` | Remove attribute |
| `get_attribute(key)` | `str\|None` | Get attribute value |
| `has_attribute(key)` | `bool` | Check existence |
| `get_attributes(*keys)` | `dict` | Get all (or specified) attributes. Returns a copy. |
| `generate_id()` | `None` | Add unique ID if none exists (not chainable) |

### Inline Styles

| Method | Returns | Description |
|--------|---------|-------------|
| `add_style(key, value)` | `self` | Set CSS property. Raises `ValueError` on dangerous values. |
| `add_styles(dict)` | `self` | Set multiple CSS properties |
| `get_style(key)` | `str\|None` | Get CSS property value |
| `remove_style(key)` | `self` | Remove CSS property |

CSS values are validated against injection patterns (`javascript:`, `expression()`, `url(data:)`, etc.).

### Rendering

| Method | Returns | Description |
|--------|---------|-------------|
| `render(pretty=False, max_depth=1000)` | `str` | HTML string. Raises `RecursionError` if depth exceeded. |
| `str(element)` | `str` | Same as `render()` |

### Serialization

| Method | Returns | Description |
|--------|---------|-------------|
| `to_dict()` | `dict` | `{tag, self_closing, attributes, text, children}` |
| `to_json(indent=None)` | `str` | JSON string |
| `HTMLElement.from_dict(data)` | `HTMLElement` | Reconstruct from dict |
| `HTMLElement.from_json(json_str)` | `HTMLElement` | Reconstruct from JSON |
| `from_html(html_str, fragment=False)` | `HTMLElement\|List\|None` | Parse HTML string |

`from_html` is also available as a standalone function: `from nitro_ui import from_html`

When `fragment=True`, returns `List[HTMLElement]`. When `False`, returns single element or `None`.

### Event Callbacks (Override in Subclasses)

| Method | Called When |
|--------|------------|
| `on_load()` | Element constructed |
| `on_before_render()` | Before `render()` |
| `on_after_render()` | After `render()` |
| `on_unload()` | Element garbage collected |

### Utility

| Method | Returns | Description |
|--------|---------|-------------|
| `clone()` | `HTMLElement` | Deep copy |
| `__enter__`/`__exit__` | `self` | Context manager support |

---

## Fragment (No Wrapper Tag)

Renders children without a wrapper element.

```python
from nitro_ui import Fragment, H1, Paragraph

frag = Fragment(H1("Title"), Paragraph("Content"))
print(frag.render())
# <h1>Title</h1><p>Content</p>
```

Use cases: conditional rendering without wrapper divs, returning multiple elements from functions, list composition.

---

## Partial (Raw HTML)

Embed raw HTML for trusted content. Bypasses escaping.

```python
from nitro_ui import Head, Meta, Title, Partial

# Inline raw HTML
Head(
    Meta(charset="utf-8"),
    Partial("""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
        <script>gtag('config', 'GA_ID');</script>
    """),
    Title("My Page")
)

# Or load from file (lazy-loaded at render time)
Partial(file="partials/analytics.html")
```

**Warning:** Only use with trusted content - bypasses XSS protections.

---

## Styling System

### CSSStyle

Represents CSS styles with pseudo-selectors and responsive breakpoints.

```python
from nitro_ui.styles import CSSStyle

style = CSSStyle(
    background_color="#007bff",    # snake_case -> kebab-case
    color="white",
    padding="10px 20px",
    border_radius="5px",
    _hover=CSSStyle(background_color="#0056b3"),   # pseudo-selector
    _md=CSSStyle(padding="15px 30px")              # breakpoint
)
```

**Pseudo-selectors** (prefix `_`): `_hover`, `_active`, `_focus`, `_visited`, `_link`, `_first_child`, `_last_child`, `_nth_child`, `_before`, `_after`

**Breakpoints** (prefix `_`): `_xs` (0px), `_sm` (640px), `_md` (768px), `_lg` (1024px), `_xl` (1280px), `_2xl` (1536px)

| Method | Returns | Description |
|--------|---------|-------------|
| `to_inline()` | `str` | CSS string for `style="..."` (base styles only) |
| `merge(other)` | `CSSStyle` | New merged style (other overrides) |
| `has_pseudo_or_breakpoints()` | `bool` | Has pseudo/responsive styles |
| `is_complex(threshold=3)` | `bool` | Has many properties |
| `to_dict()` / `CSSStyle.from_dict(data)` | | Serialization |

### StyleSheet

Manages CSS classes and generates `<style>` tag content.

```python
from nitro_ui.styles import StyleSheet, CSSStyle, Theme

# Optional theme for CSS variables
stylesheet = StyleSheet(theme=Theme.modern())

# Register classes
btn = stylesheet.register("btn-primary", CSSStyle(
    background_color="#007bff",
    color="white",
    _hover=CSSStyle(background_color="#0056b3")
))

# BEM naming
card = stylesheet.register_bem("card", style=CSSStyle(padding="20px"))
# "card"
card_header = stylesheet.register_bem("card", element="header",
    style=CSSStyle(font_weight="bold"))
# "card__header"
card_featured = stylesheet.register_bem("card", modifier="featured",
    style=CSSStyle(border="2px solid blue"))
# "card--featured"

# Use in elements
Button("Click", cls=btn)
Div(cls=f"{card} {card_featured}")

# Generate output
css = stylesheet.render()                  # CSS string
tag = stylesheet.to_style_tag()            # <style>...</style>
```

| Method | Returns | Description |
|--------|---------|-------------|
| `register(name, style)` | `str` | Register style, returns class name |
| `register_bem(block, element=, modifier=, style=)` | `str` | BEM class name |
| `get_style(name)` | `CSSStyle\|None` | Get registered style |
| `has_class(name)` | `bool` | Check if registered |
| `unregister(name)` | `bool` | Remove class |
| `clear()` | `None` | Remove all classes |
| `set_breakpoint(name, value)` | `None` | Set breakpoint value |
| `render(pretty=True)` | `str` | CSS output |
| `to_style_tag(pretty=True)` | `str` | `<style>` tag |
| `count_classes()` | `int` | Number of classes |
| `get_all_class_names()` | `List[str]` | All class names |
| `to_dict()` / `StyleSheet.from_dict(data, theme=)` | | Serialization |

### Theme

Preset design systems with CSS variables.

```python
from nitro_ui.styles import Theme

theme = Theme.modern()    # Blue primary, Inter font, modern components
theme = Theme.classic()   # Traditional blue, Georgia serif
theme = Theme.minimal()   # Black/white, system fonts

# Custom
theme = Theme(
    name="Custom",
    colors={"primary": "#007bff", "secondary": "#6c757d"},
    typography={"font_family": "Inter, sans-serif"},
    spacing={"sm": "8px", "md": "16px", "lg": "24px"},
    components={"button": {"primary": CSSStyle(...)}}
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `get_css_variables()` | `dict` | `{"--color-primary": "#007bff", ...}` |
| `get_component_style(component, variant="default")` | `CSSStyle\|None` | Component style |
| `to_dict()` / `Theme.from_dict(data)` | | Serialization |

---

## Common Patterns

### Complete Page
```python
from nitro_ui import HTML, Head, Body, Title, Meta, Div, H1, Paragraph

page = HTML(
    Head(
        Title("My Page"),
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1")
    ),
    Body(
        Div(
            H1("Welcome"),
            Paragraph("Hello, world!"),
            cls="container"
        )
    )
)
html = page.render(pretty=True)
```

### Navigation
```python
from nitro_ui.html import nav, ul, li, a

navbar = nav(
    ul(
        li(a("Home", href="/")),
        li(a("About", href="/about")),
        li(a("Contact", href="/contact")),
    ),
    cls="navbar"
)
```

### Form
```python
from nitro_ui.html import form, label, input_, button

login_form = form(
    label("Email:", for_element="email"),
    input_(type="email", id="email", name="email", required=True),
    label("Password:", for_element="password"),
    input_(type="password", id="password", name="password", required=True),
    button("Log In", type="submit"),
    action="/login",
    method="post"
)
```

### Table from Data
```python
from nitro_ui.html import table, thead, tbody, tr, th, td

data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

t = table(
    thead(tr(th("Name"), th("Age"))),
    tbody(*[
        tr(td(row["name"]), td(str(row["age"])))
        for row in data
    ])
)
```

### Dynamic List
```python
from nitro_ui.html import ul, li

items = ["Apple", "Banana", "Orange"]
list_element = ul(*[li(item) for item in items])
```

### Method Chaining
```python
container = (Div()
    .add_attribute("id", "hero")
    .add_styles({"background": "#f0f0f0", "padding": "2rem"})
    .append(H1("Welcome"))
    .append(Paragraph("Get started today.")))
```

### Custom Component Class
```python
from nitro_ui import HTMLElement, H2, Paragraph

class Card(HTMLElement):
    def __init__(self, title, content, **kwargs):
        super().__init__(tag="div", cls="card", **kwargs)
        self.append(
            H2(title, cls="card-title"),
            Paragraph(content, cls="card-body")
        )

card = Card("My Card", "Card content here", id="card-1")
```

### Parsing and Modifying HTML
```python
from nitro_ui import from_html, Paragraph

element = from_html('<div class="old"><h1>Title</h1></div>')
element.add_attribute("class_name", "new")
element.add_style("padding", "20px")
element.append(Paragraph("New content"))
html = element.render()
```

### Serialization Round-Trip
```python
from nitro_ui import Div, H1, HTMLElement

page = Div(H1("Title"), id="page")
json_str = page.to_json(indent=2)
loaded = HTMLElement.from_json(json_str)
html = loaded.render()
```

### Page with StyleSheet
```python
from nitro_ui import HTML, Head, Body, Button, Style
from nitro_ui.styles import CSSStyle, StyleSheet, Theme

theme = Theme.modern()
stylesheet = StyleSheet(theme=theme)

btn = stylesheet.register("btn", CSSStyle(
    background_color="var(--color-primary)",
    color="white",
    padding="10px 20px",
    _hover=CSSStyle(background_color="var(--color-primary-dark)")
))

page = HTML(
    Head(Style(stylesheet.render())),
    Body(Button("Click Me", cls=btn))
)
```

---

## Framework Integration

### FastAPI
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nitro_ui.html import html, head, body, title, h1

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return html(
        head(title("FastAPI + NitroUI")),
        body(h1("Hello!"))
    ).render()
```

### Flask
```python
from flask import Flask
from nitro_ui.html import html, head, body, title, h1

app = Flask(__name__)

@app.route("/")
def home():
    return html(
        head(title("Flask + NitroUI")),
        body(h1("Hello!"))
    ).render()
```

### Django
```python
from django.http import HttpResponse
from nitro_ui.html import html, head, body, title, h1

def home(request):
    page = html(
        head(title("Django + NitroUI")),
        body(h1("Hello!"))
    )
    return HttpResponse(page.render())
```

---

## Security

- **Automatic HTML escaping**: All text content and attribute values are escaped
- **CSS value validation**: `add_style`/`add_styles` reject `javascript:`, `expression()`, `url(data:)`, etc. (raises `ValueError`)
- **CSS class name validation**: StyleSheet rejects class names containing injection patterns
- **No raw HTML injection**: Cannot inject unescaped HTML (use `Partial` for trusted raw HTML)
- **Recursion protection**: `render()`, `filter()`, `find_by_attribute()` have `max_depth` parameter (default 1000) to prevent stack overflow from circular references
- **Child type validation**: Only `HTMLElement` and `str` accepted as children. `None` silently ignored, other types raise `ValueError`.

---

## Gotchas

- **Package name mismatch**: PyPI is `nitro-ui`, import is `nitro_ui`
- **HtmlLink vs Href**: `Href`/`a` is for `<a>` links. `HtmlLink`/`link` is for `<link>` tags.
- **`get_attributes()` returns a copy**: Mutating the returned dict does not affect the element. Use `add_attribute()` to modify.
- **`replace_child()` and `generate_id()` return `None`**: Not chainable, unlike other methods.
- **`from_dict()` expects normalized keys**: Designed for round-tripping with `to_dict()`. Attribute keys should already be in their final form (e.g. `data-value`, not `data_value`).

---

## Quick Checklist

When generating NitroUI code:

- [ ] Choose import style: PascalCase (`from nitro_ui import`) or lowercase (`from nitro_ui.html import`)
- [ ] Use `cls` for CSS classes (or `class_name` - both work, `cls` is shorter)
- [ ] Use `for_element` not `for` (Python keyword)
- [ ] Use `input_`, `del_`, `object_`, `map_` for Python keyword conflicts (lowercase only)
- [ ] Children go as positional args, attributes as keyword args
- [ ] Call `.render()` to get HTML string
- [ ] Use `pretty=True` for readable output during development
- [ ] All manipulation methods return `self` for chaining (except `replace_child`, `generate_id`)
- [ ] Use `Fragment` when you need multiple elements without a wrapper
- [ ] Use `Partial` for raw HTML (analytics, embeds) - bypasses escaping
