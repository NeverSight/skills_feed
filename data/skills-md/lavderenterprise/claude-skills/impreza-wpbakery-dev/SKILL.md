---
name: impreza-wpbakery-dev
description: "Use this skill for WordPress development with Impreza theme and WPBakery Page Builder. Triggers include: converting designs (described, visual, or Figma) to WordPress/Impreza code, creating WPBakery shortcodes, building Impreza pages, implementing responsive layouts, customizing Impreza elements, or any WordPress development task using the Impreza theme with WPBakery. Essential for producing copy-paste ready code that works seamlessly with Impreza theme structure."
license: MIT
---

# WordPress Development: Impreza Theme + WPBakery Page Builder

## Overview

This skill enables you to transform designs into production-ready WordPress code using the Impreza theme (by UpSolution) and WPBakery Page Builder. Impreza is a multipurpose WordPress theme with a customized WPBakery implementation, offering 63+ content elements, Live Builder, and extensive WooCommerce integration.

**Current Versions (as of 2026):**
- Impreza Theme: 8.43.1 (February 2, 2026)
- WPBakery: 8.7.2 (October 27, 2025)
- PHP: 8.3 fully supported
- WordPress: 6.6+ required

## Quick Reference

| Task | Approach |
|------|----------|
| Design → Code | Use shortcode syntax with Impreza native elements |
| Responsive Layout | Use `vc_row_inner`/`vc_column_inner` with `columns` param |
| Custom Styling | Use `css` param with Impreza JSON URL-encoded format |
| Typography | Let the theme handle it — use HTML tags inside `[vc_column_text]` |
| Buttons | `[us_btn label="..." style="2"]` — use `label`, not `text` |
| Dynamic Content | Use ACF integration + Grid Layouts |
| Performance | Enable "Disable extra features of WPBakery" option |

---

## ⚠️ CRITICAL RULES — Read Before Generating Any Code

These rules apply to ALL code generation. Violating them produces broken, non-functional output.

### Rule 1: Impreza CSS Format (JSON URL-encoded)

Impreza does **NOT** use the standard WPBakery CSS format. The old `.vc_custom_xxxxx{...}` syntax is **completely broken** in Impreza.

**❌ WRONG — Will NOT work:**
```
css=".vc_custom_123{padding-top:80px;background-color:#F9FAFB;border-radius:16px;}"
```

**✅ CORRECT — Impreza JSON URL-encoded format:**
```
css="%7B%22default%22%3A%7B%22padding-top%22%3A%2280px%22%2C%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"
```

The JSON structure before encoding is:
```json
{"default":{"padding-top":"80px","background-color":"#F9FAFB","border-radius":"16px"}}
```

**Encoding rules:**
- `{` → `%7B`
- `}` → `%7D`
- `"` → `%22`
- `:` → `%3A`
- `,` → `%2C`
- `#` → `%23`
- Space → `%20`

**Common CSS properties available in the `css` param:**
- `color`, `background-color`
- `font-size`, `font-weight`, `font-style`, `line-height`
- `text-align`, `text-transform`
- `padding-top`, `padding-right`, `padding-bottom`, `padding-left`
- `margin-top`, `margin-right`, `margin-bottom`, `margin-left`
- `border-radius`
- `width`, `height`, `max-width`
- `box-shadow-h-offset`, `box-shadow-v-offset`, `box-shadow-blur`, `box-shadow-spread`, `box-shadow-color`

### Rule 2: Typography Comes From the Theme

Font styles (size, weight, line-height, font-family) for headings (h1–h6) and body text are managed globally by Impreza's Theme Options > Typography. When converting from Figma or any design:

**❌ WRONG — Do NOT extract typography from Figma:**
```
[us_heading tag="h2" title="Title" size="36px" font_weight="800" color="#101828" css="...letter-spacing...line-height..."]
```

**✅ CORRECT — Use HTML tags, let the theme style them:**
```
[vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h2>Title</h2>
[/vc_column_text]
```

**Key principle:** The code must only use the correct semantic HTML tag (h1, h2, h3, h4, h5, h6, p) and assume the theme provides the appropriate visual styling. Only override with CSS when there is a specific decorative need (e.g., a gradient text effect, a color that differs from the theme, specific alignment).

### Rule 3: Never Abuse `[us_html]`

`[us_html]` is for rare cases requiring custom HTML/JS that cannot be achieved with native elements. Using it for common elements (cards, icons, stars, images, buttons) is **forbidden** — it makes content non-editable in the builder.

**❌ WRONG:**
```
[us_html]
  <div class="feature-card">
    <i class="fas fa-bolt"></i>
    <h3>Title</h3>
    <p>Description</p>
  </div>
[/us_html]
```

**✅ CORRECT — Use native shortcodes:**
```
[us_iconbox icon="far|bolt" iconpos="left" alignment="left" size="24px" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Title</h5>
Description[/vc_column_text]
```

### Rule 4: Buttons Use `label`, Not `text` — Style Is Numeric

**❌ WRONG:**
```
[us_btn text="Click me" style="raised" color="custom" size="large"]
```

**✅ CORRECT:**
```
[us_btn label="Click me" style="2" iconpos="right"]
```

Button `style` values are numeric (e.g., `"1"`, `"2"`, `"3"`, etc.), corresponding to the button styles defined in Theme Options. Do not use string names like `"raised"`, `"flat"`, or `"outlined"`.

### Rule 5: Animations & Effects Are Ignored

If the Figma design contains animations (hover effects, scroll animations, transitions, parallax on elements, fade-ins, etc.), these must be:
- **Ignored** in the generated code
- **Listed in a notes section** at the end of the output, describing what was detected and suggesting manual configuration

### Rule 6: Classic Mode Output Must Be Compact

Code intended for WPBakery Classic Mode must be **compact** — shortcodes on single lines, no indentation, no multi-line formatting. Newlines are only allowed inside `[vc_column_text]` where HTML content requires them.

**❌ WRONG — Multi-line formatted shortcodes:**
```
[vc_row 
  height="auto" 
  valign="middle" 
  el_class="hero-section"
]
  [vc_column width="1/1" align="center"]
    [us_heading 
      tag="h1" 
      title="Title"
    ]
  [/vc_column]
[/vc_row]
```

**✅ CORRECT — Compact single-line:**
```
[vc_row][vc_column][vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h1>Title</h1>
[/vc_column_text][/vc_column][/vc_row]
```

### Rule 7: No Trailing Empty Rows

Never add an empty row at the end of the generated output. The AI tends to append a blank row like:
```
[vc_row][vc_column][vc_column_text]
[/vc_column_text][/vc_column][/vc_row]
```

This creates a visible empty section on the page. The generated code must end with the last meaningful `[/vc_row]` and nothing after it.

### Rule 8: Inner Rows Always Have 1rem Padding

Every `[vc_row_inner]` must include `css` with 1rem padding on all sides. Without this, inner row content touches the edges and looks broken.

**❌ WRONG — No padding on inner row:**
```
[vc_row_inner columns="3"]
```

**✅ CORRECT — Always include 1rem padding:**
```
[vc_row_inner columns="3" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"]
```

The decoded JSON is: `{"default":{"padding-left":"1rem","padding-top":"1rem","padding-bottom":"1rem","padding-right":"1rem"}}`

---

## Architecture & Dual Builder System

### Live Builder (Recommended)
Impreza's native visual editor with real-time WYSIWYG editing:
- **Activation**: Theme Options > Advanced > Theme Modules
- **Features**: Section Templates, Favorite Sections, drag-and-drop interface
- **Performance**: No frontend CSS/JS overhead when element not used
- **Interchangeable**: Full compatibility with WPBakery-created content

### WPBakery Page Builder
Bundled, customized version optimized for Impreza:
- **Backend Editor**: Schematic layout view for content-rich pages
- **Frontend Editor**: Classic WYSIWYG interface
- **Classic Mode**: Direct shortcode editing — **this is where generated code gets pasted**
- **Modifications**: Impreza adds custom options, disables non-compatible features

**CRITICAL**: Both builders are fully interchangeable — pages created in one can be edited in the other.

---

## Core Structure: Rows, Columns & Sections

### Row/Section Element (`vc_row`)

The foundational container for all layouts.

**Basic Syntax:**
```
[vc_row][vc_column]<!-- Content here -->[/vc_column][/vc_row]
```

**Row with custom width:**
```
[vc_row width="custom" width_custom="840px"][vc_column]<!-- Content -->[/vc_column][/vc_row]
```

**Row with background color:**
```
[vc_row css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%7D%7D"][vc_column]<!-- Content -->[/vc_column][/vc_row]
```

**Common Row Parameters:**
- `width` — `"custom"` to enable custom width
- `width_custom` — Custom width value (e.g., `"840px"`, `"1200px"`)
- `gap` — Column spacing: `0px`, `10px`, `20px`, `30px`, `40px`, `60px`
- `columns_type` — Layout: `default`, `boxes` (with background), `small` (reduced padding)
- `height` — Row height: `default`, `auto`, `small`, `medium`, `large`, `huge`, `full` (100vh)
- `valign` — Vertical alignment: `top`, `middle`, `bottom`
- `content_placement` — Content alignment: `top`, `middle`, `bottom`
- `color_scheme` — Color scheme: `default`, `alternate`, `primary`, `secondary`, `custom`
- `bg_color` — Background color (hex or color name)
- `bg_image` — Background image URL
- `bg_size` — Background size: `cover`, `contain`, `initial`
- `parallax` — Enable parallax: `vertical`, `horizontal`, `still`, `fixed`
- `parallax_speed` — Parallax speed factor: `0.1` to `2.0` (default `1`)
- `css` — Impreza JSON URL-encoded CSS (see Rule 1)

**⚠️ Width Control:**
Never use CSS padding to simulate narrow content areas. Always use the native `width` parameter:
```
[vc_row width="custom" width_custom="896px"]
```

### Column Layouts (`vc_column`)

**Standard Grid System:**
- `1/1` — Full width (100%)
- `1/2` — Half width (50%)
- `1/3`, `2/3` — Third layouts
- `1/4`, `3/4` — Quarter layouts
- `1/5`, `2/5`, `3/5`, `4/5` — Fifth layouts
- `1/6`, `5/6` — Sixth layouts

**Column Parameters:**
- `width` — Column width (see grid system above)
- `css` — Impreza JSON URL-encoded CSS

### Inner Rows & Columns (for Grids)

For creating grid layouts (feature grids, card grids, testimonials), use `vc_row_inner` + `vc_column_inner` **inside** a parent `vc_row > vc_column`.

**⚠️ Every `vc_row_inner` MUST have 1rem padding on all sides (see Rule 8).**

**❌ WRONG — Multiple `vc_row` for a single grid:**
```
[vc_row gap="40px"]
  [vc_column width="1/3"]Card 1[/vc_column]
  [vc_column width="1/3"]Card 2[/vc_column]
  [vc_column width="1/3"]Card 3[/vc_column]
[/vc_row]
```

**✅ CORRECT — Single `vc_row` with `vc_row_inner` + padding:**
```
[vc_row][vc_column][vc_row_inner columns="3" tablets_columns="2" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"]<!-- Card 1 -->[/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"]<!-- Card 2 -->[/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"]<!-- Card 3 -->[/vc_column_inner][/vc_row_inner][/vc_column][/vc_row]
```

**Simple inner row (single column content):**
```
[vc_row][vc_column width="1/1"][vc_row_inner css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"][vc_column_inner width="1/1"][us_text text="Content inside inner row"][/vc_column_inner][/vc_row_inner][/vc_column][/vc_row]
```

**`vc_row_inner` key parameters:**
- `columns` — Number of columns: `"2"`, `"3"`, `"4"`, etc.
- `tablets_columns` — Columns on tablet
- `gap` — Gap between columns
- `css` — **Required:** must always include 1rem padding (see Rule 8)

### Design Settings (Universal)

All Impreza elements support the `css` parameter using Impreza JSON URL-encoded format.

**Spacing example:**
```
css="%7B%22default%22%3A%7B%22padding-top%22%3A%2240px%22%2C%22padding-bottom%22%3A%2240px%22%7D%7D"
```
Which decodes to: `{"default":{"padding-top":"40px","padding-bottom":"40px"}}`

**Visibility (show/hide on devices):**
- `hide_on_desktop` — Hide on desktop: `yes`, `no`
- `hide_on_laptop` — Hide on laptops: `yes`, `no`
- `hide_on_tablet` — Hide on tablets: `yes`, `no`
- `hide_on_mobile` — Hide on mobiles: `yes`, `no`

**Custom Classes & IDs:**
- `el_class` — Custom CSS class
- `el_id` — Custom HTML ID

---

## Impreza Content Elements

### Text & Typography

#### `[vc_column_text]` — Primary Text Element

This is the **primary element for all text content** including headings. Use it whenever you need to output text with HTML tags. The theme handles the typography styling.

**Heading:**
```
[vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h1>Main Page Title</h1>
[/vc_column_text]
```

**Heading with decorative gradient span:**
```
[vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h1>Da Figma a WordPress <span style="background: linear-gradient(90deg,#155DFC 0%,#4F39F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">in un solo click</span></h1>
[/vc_column_text]
```

**Heading + paragraph together:**
```
[vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h2>Section Title</h2>
Description paragraph goes here. The theme handles font sizes and weights.
[/vc_column_text]
```

**When to use `[vc_column_text]`:**
- All headings (h1–h6) — wrap the HTML tag inside
- Paragraphs with mixed formatting
- Text that contains HTML (spans, links, bold, italic)
- Heading + description combos in the same block

#### `[us_text]` — Simple Text Element

Use for short, single-line text blocks that don't need HTML markup. Supports icon display.

**Badge/label:**
```
[us_text text="Potenziato dall'Intelligenza Artificiale" css="%7B%22default%22%3A%7B%22color%22%3A%22%231447E6%22%2C%22text-align%22%3A%22center%22%2C%22font-size%22%3A%2214px%22%2C%22line-height%22%3A%222%22%2C%22font-weight%22%3A%22400%22%2C%22background-color%22%3A%22%23DBEAFE%22%2C%22width%22%3A%22fit-content%22%2C%22margin-left%22%3A%22auto%22%2C%22margin-right%22%3A%22auto%22%2C%22padding-left%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%2C%22border-radius%22%3A%2220px%22%7D%7D" icon="far|stars"]
```

**Section label (uppercase):**
```
[us_text css="%7B%22default%22%3A%7B%22color%22%3A%22%231447E6%22%2C%22text-align%22%3A%22center%22%2C%22font-size%22%3A%2216px%22%2C%22font-weight%22%3A%22400%22%2C%22text-transform%22%3A%22uppercase%22%7D%7D" text="Caratteristiche"]
```

**Simple text with tag override:**
```
[us_text text="Scelto da migliaia di designer" tag="h3" css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
```

**Parameters:**
- `text` — The text content
- `tag` — HTML tag to use: `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `p`, `div`
- `icon` — Icon prefix: `far|stars`, `fas|check`
- `css` — Impreza JSON URL-encoded CSS

**When to use `[us_text]`:**
- Simple one-line text (badges, labels, short captions)
- Text that needs an inline icon via the `icon` parameter
- Name/role labels in testimonials or person cards

**When NOT to use `[us_text]`:**
- Headings (use `[vc_column_text]` with `<h1>`–`<h6>` tags instead)
- Multi-line or mixed-format text
- Text containing HTML

#### Typography Decision Guide

| Content Type | Element to Use | Example |
|---|---|---|
| Main heading (h1) | `[vc_column_text]` | `<h1>Page Title</h1>` |
| Section heading (h2–h6) | `[vc_column_text]` | `<h2>Features</h2>` |
| Heading + description | `[vc_column_text]` | `<h2>Title</h2>\nDescription text` |
| Heading with gradient/effect | `[vc_column_text]` | `<h1>Text <span style="...">colored</span></h1>` |
| Simple label/badge | `[us_text]` | `text="LABEL" icon="far|stars"` |
| Person name | `[us_text]` | `text="John Doe"` with css for weight |
| Short caption | `[us_text]` | `text="14 days free trial"` |
| Card title + desc (inside column_inner) | `[vc_column_text]` | `<h5>Card Title</h5>\nCard description` |

### Separator (`us_separator`)

Used for spacing between elements.

```
[us_separator size="small"]
[us_separator size="large"]
[us_separator size="custom" height="10px"]
[us_separator size="custom" height="30px"]
```

**Sizes:** `small`, `medium`, `large`, `huge`, `custom`
When `size="custom"`, use `height` to specify exact pixel value.

### Buttons (`us_btn`)

**Basic button:**
```
[us_btn label="Inizia la prova gratuita" icon="fas|arrow-right" iconpos="right" style="2"]
```

**Secondary button:**
```
[us_btn label="Guarda la demo"]
```

**Parameters:**
- `label` — Button text (**NOT** `text`)
- `style` — Numeric style ID: `"1"`, `"2"`, `"3"`, etc. (defined in Theme Options > Buttons)
- `icon` — Icon: `fas|arrow-right`, `far|heart`, `fas|play`
- `iconpos` — Icon position: `left`, `right`
- `link` — URL (encoded): `url:https%3A%2F%2Fexample.com|title:Title|target:_blank`
- `align` — Alignment: `left`, `center`, `right`

**⚠️ Button style values:**
- Do NOT use `"raised"`, `"flat"`, `"outlined"` — these do not work
- Use numeric IDs that correspond to button styles configured in Theme Options

**Multiple buttons side by side:**
```
[us_hwrapper alignment="center" inner_items_gap="1rem" valign="middle"][us_btn label="Primary Action" icon="fas|arrow-right" iconpos="right" style="2"][us_btn label="Secondary Action"][/us_hwrapper]
```

### Horizontal Wrapper (`us_hwrapper`)

Container for placing elements side by side horizontally.

```
[us_hwrapper alignment="center" inner_items_gap="1rem" valign="middle"]<!-- Inline elements -->[/us_hwrapper]
```

**Parameters:**
- `alignment` — Horizontal alignment: `left`, `center`, `right`
- `inner_items_gap` — Gap between items: `0rem`, `0.5rem`, `1rem`, etc.
- `valign` — Vertical alignment: `top`, `middle`, `bottom`
- `wrap` — Allow wrapping: `"1"`, `"0"`

### Vertical Wrapper (`us_vwrapper`)

Container for stacking elements vertically with controlled gap.

```
[us_vwrapper inner_items_gap="0rem"][us_text text="Name" css="..."][us_text text="Role" css="..."][/us_vwrapper]
```

**Parameters:**
- `inner_items_gap` — Gap between items

### Images (`us_image`)

Always use `[us_image]` — never raw `<img>` HTML.

**Basic image:**
```
[us_image image="1415" size="full" align="center"]
```

**Image with ratio and border radius:**
```
[us_image ratio_width="21" ratio_height="9" has_ratio="1" ratio="16x9" align="center" size="full" css="%7B%22default%22%3A%7B%22border-radius%22%3A%2216px%22%7D%7D" image="1415"]
```

**Circle avatar (e.g., for testimonials):**
```
[us_image ratio_width="21" ratio_height="9" has_ratio="1" size="full" image="1415" style="circle" css="%7B%22default%22%3A%7B%22width%22%3A%2248px%22%2C%22height%22%3A%2248px%22%7D%7D"]
```

**Parameters:**
- `image` — WordPress media library ID (numeric)
- `size` — WordPress size: `thumbnail`, `medium`, `large`, `full`
- `align` — Alignment: `left`, `center`, `right`
- `style` — Style: `default`, `circle`
- `has_ratio` — Force aspect ratio: `"1"`, `"0"`
- `ratio` — Aspect ratio: `1x1`, `4x3`, `16x9`, `21x9`
- `ratio_width`, `ratio_height` — Custom ratio values
- `lightbox` — Enable lightbox: `"1"`, `"0"`
- `css` — Impreza JSON URL-encoded CSS

### Iconbox (`us_iconbox`)

Used for icons with optional styling. Can be used as a standalone icon display or as an icon+title combo.

**Icon only (e.g., in a feature card):**
```
[us_iconbox icon="far|bolt" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox]
```

**Star rating icon:**
```
[us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox]
```

**Parameters:**
- `icon` — Icon in Impreza format: `far|bolt`, `fas|check-circle`, `far|code`, `far|globe`, `far|mobile`, `far|shield-check`, `far|browser`, `far|stars`
- `iconpos` — Icon position: `top`, `left`
- `alignment` — Content alignment: `left`, `center`, `right`
- `size` — Icon size: `18px`, `24px`, `32px`, etc.
- `color` — Color mode: `primary`, `secondary`, `custom`
- `icon_color` — Custom icon color (hex)
- `el_class` — Custom CSS class
- `title` — Optional title text

**Star Rating Pattern (5 stars):**
```
[us_hwrapper inner_items_gap="0rem"][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][/us_hwrapper]
```

### Single Icon (`us_icon`)

```
[us_icon icon="fas|rocket" size="3rem" color="primary"]
```

### Message Box (`us_message`)

```
[us_message color="primary" icon="fas|info-circle" closing="1"]Important information.[/us_message]
```

**Message colors:** `success` (green), `attention` (yellow), `error` (red), `info` (blue)

### Gallery (`us_gallery`)

```
[us_gallery ids="123,456,789" columns="3" gap="20px" type="masonry" lightbox="1"]
```

**Gallery types:** `default`, `masonry`, `carousel`, `slider`

### Image Slider (`us_image_slider`)

```
[us_image_slider ids="123,456,789" arrows="1" nav="dots" autoplay="1" autoplay_period="5" ratio="16x9"]
```

### Video (`vc_video`)

```
[vc_video link="https://www.youtube.com/watch?v=xxxxx" el_aspect="16-9"]
```

### Accordion (`vc_tta_accordion`)

Collapsible content sections. Uses `vc_tta_accordion` as wrapper and `vc_tta_section` for each panel.

**Basic accordion:**
```
[vc_tta_accordion][vc_tta_section title="Sezione 1"][vc_column_text]
Content of first section. Lorem ipsum dolor sit amet.
[/vc_column_text][/vc_tta_section][vc_tta_section title="Sezione 2"][vc_column_text]
Content of second section.
[/vc_column_text][/vc_tta_section][/vc_tta_accordion]
```

**⚠️ Correct shortcode names:**
- Wrapper: `[vc_tta_accordion]` — NOT `[us_accordion]`
- Sections: `[vc_tta_section title="..."]` — NOT `[us_accordion_item]`
- Content inside sections: use `[vc_column_text]` or any other Impreza element

### Tabs (`vc_tta_tabs`)

Horizontal tabbed content. Uses `vc_tta_tabs` as wrapper and `vc_tta_section` for each tab.

**Basic tabs:**
```
[vc_tta_tabs][vc_tta_section title="Sezione 1"][vc_column_text]
Content of first tab. Lorem ipsum dolor sit amet.
[/vc_column_text][/vc_tta_section][vc_tta_section title="Sezione 2"][vc_column_text]
Content of second tab.
[/vc_column_text][/vc_tta_section][/vc_tta_tabs]
```

**⚠️ Correct shortcode names:**
- Wrapper: `[vc_tta_tabs]` — NOT `[us_tabs]`
- Sections: `[vc_tta_section title="..."]` — NOT `[us_tab]`

### Vertical Tabs / Tour (`vc_tta_tour`)

Same as tabs but with vertical tab navigation on the side.

**Basic vertical tabs:**
```
[vc_tta_tour][vc_tta_section title="Sezione 1"][vc_column_text]
Content of first section. Lorem ipsum dolor sit amet.
[/vc_column_text][/vc_tta_section][vc_tta_section title="Sezione 2"][vc_column_text]
Content of second section.
[/vc_column_text][/vc_tta_section][/vc_tta_tour]
```

### Tabbed Elements Quick Reference

| Element | Wrapper Shortcode | Section Shortcode |
|---|---|---|
| Accordion (collapsible) | `[vc_tta_accordion]` | `[vc_tta_section title="..."]` |
| Tabs (horizontal) | `[vc_tta_tabs]` | `[vc_tta_section title="..."]` |
| Vertical Tabs / Tour | `[vc_tta_tour]` | `[vc_tta_section title="..."]` |

**Key points:**
- All three use `[vc_tta_section]` for their inner panels — the wrapper determines the visual behavior
- Content inside each section can be any Impreza element (`[vc_column_text]`, `[us_image]`, `[us_btn]`, etc.)
- Each section requires a `title` parameter

### Popup (`us_popup`)

```
[us_popup show_on="click" trigger_id="open-popup-btn"]Popup content.[/us_popup]
```

### Counter (`us_counter`)

```
[us_counter initial="0" target="1500" prefix="$" suffix="+" duration="2" color="primary" size="3rem"]
```

### Progress Bar (`us_progbar`)

```
[us_progbar count="75" title="WordPress Development" style="thin" color="primary"]
```

### Social Links (`us_socials`)

```
[us_socials items="%5B%7B%22type%22%3A%22facebook%22%2C%22url%22%3A%22https%3A%2F%2Ffacebook.com%2Fyourpage%22%7D%5D" style="colored" size="1.5rem"]
```

### Contact Form (`us_cform`)

```
[us_cform receiver_email="info@example.com" button_text="Send Message"]
```

**Contact Form 7 Integration:**
```
[contact-form-7 id="1234"]
```

### Google Maps (`us_gmaps`)

```
[us_gmaps address="1600 Amphitheatre Parkway, Mountain View, CA" latitude="37.4220" longitude="-122.0841" zoom="15" height="450px" marker="1"]
```

### Person Card (`us_person`)

```
[us_person name="Jane Smith" role="CEO & Founder" image="12345" email="jane@example.com"]Short bio.[/us_person]
```

### Call to Action (`us_cta`)

```
[us_cta title="Ready to Start?" message="Join thousands today." btn_label="Sign Up" btn_link="url:https%3A%2F%2Fexample.com" btn_style="raised" color_bg="primary"]
```

### Custom HTML (`us_html`)

**Only for genuinely custom HTML/JS that cannot be built with native elements:**

```
[us_html]
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","name":"Your Business"}
</script>
[/us_html]
```

### Reusable Blocks (`us_page_block`)

```
[us_page_block id="1234"]
```

---

## Dynamic Content & Grid Layouts

### Post Grid (`us_grid`)

```
[us_grid post_type="post" items_qty="9" columns="3" items_gap="30px" pagination="ajax" filter="1" filter_taxonomy="category"]
```

**Parameters:**
- `post_type` — `post`, `page`, `product`, `portfolio`, or custom post type
- `items_qty` — Number of items
- `columns` — Grid columns: `1`–`6`
- `items_gap` — Gap: `0px` to `60px`
- `type` — Grid type: `grid`, `masonry`, `carousel`
- `pagination` — `regular`, `ajax`, `load_more`, `infinite`
- `filter` — Enable filter: `"1"`, `"0"`
- `filter_taxonomy` — `category`, `post_tag`, `product_cat`, custom taxonomy
- `orderby` — `date`, `title`, `rand`, `menu_order`, `modified`
- `order` — `DESC`, `ASC`

### WooCommerce Product Grid

```
[us_grid post_type="product" items_qty="12" columns="4" show_add_to_cart="1" show_price="1" filter="1" filter_taxonomy="product_cat" orderby="popularity"]
```

---

## Design-to-Code Workflow

### From Figma Design

#### Step 1: Analyze Layout Structure (What to Extract)
- Number of sections/rows
- Column layouts per row (how many columns, proportions)
- Element types (heading, text, button, image, icon, card)
- Spacing and alignment (padding, margins between sections)
- Background colors for rows/columns
- Special decorative effects (gradients on text, border-radius, shadows)

#### Step 1b: What to IGNORE from Figma
- **Font sizes** — theme handles h1–h6 and body text sizes
- **Font weights** — theme handles heading/body weights
- **Font families** — theme handles typography
- **Line heights** — theme handles line heights
- **Letter spacing** — theme handles letter spacing
- **Button visual styles** — theme button presets handle this
- **Animations/transitions** — note them, don't implement them
- **Hover states** — note them, don't implement them

#### Step 2: Map Figma Components to Impreza

| Figma Element | Impreza Element |
|---|---|
| Frame/Section | `[vc_row]` (outer) or `[vc_row_inner]` (grid) |
| Auto Layout horizontal | `[us_hwrapper]` |
| Auto Layout vertical | `[us_vwrapper]` |
| Heading text (h1–h6) | `[vc_column_text]` with `<h1>`–`<h6>` HTML tag |
| Body text / paragraph | `[vc_column_text]` with paragraph text |
| Short label / badge | `[us_text]` with css styling |
| Button | `[us_btn label="..." style="2"]` |
| Image | `[us_image image="ID"]` |
| Icon | `[us_iconbox icon="far|name"]` |
| Card (icon + title + text) | `[vc_column_inner]` containing `[us_iconbox]` + `[vc_column_text]` |
| Star rating | `[us_hwrapper]` with multiple `[us_iconbox]` |
| Avatar/photo circle | `[us_image style="circle" css="...width/height..."]` |
| Testimonial card | `[vc_column_inner]` with stars + text + author info |
| Grid of cards | `[vc_row_inner columns="3"]` with `[vc_column_inner]` children |
| Space between elements | `[us_separator size="small/large/custom"]` |
| Buttons side-by-side | `[us_hwrapper]` containing multiple `[us_btn]` |
| Name + Role stacked | `[us_vwrapper]` with two `[us_text]` elements |
| Accordion / FAQ | `[vc_tta_accordion]` with `[vc_tta_section]` children |
| Tabs (horizontal) | `[vc_tta_tabs]` with `[vc_tta_section]` children |
| Tabs (vertical/side) | `[vc_tta_tour]` with `[vc_tta_section]` children |

#### Step 3: Build the Shortcode Structure

Follow this hierarchy:
1. **`[vc_row]`** — One per page section (hero, features, testimonials, CTA, etc.)
2. **`[vc_column]`** — Inside each row (usually `width="1/1"` for full-width sections)
3. **`[vc_row_inner columns="N"]`** — For grids/card layouts inside a section
4. **`[vc_column_inner width="1/N"]`** — Individual cards/items within the grid
5. **Content elements** — `[vc_column_text]`, `[us_text]`, `[us_btn]`, `[us_image]`, `[us_iconbox]`, `[us_separator]`, `[us_hwrapper]`, `[us_vwrapper]`

#### Step 4: Apply Only Necessary Styling

Use `css` param only for:
- Background colors on rows/columns
- Text alignment (center, right)
- Border radius
- Box shadows
- Specific colors that differ from theme defaults
- Width/height constraints (e.g., avatar size)
- Custom margins for centering (margin-left: auto, margin-right: auto)

**Do NOT use `css` param for:**
- Font sizes of standard headings (h1–h6) — theme handles this
- Font weights of standard headings — theme handles this
- Font families — theme handles this
- Line heights — theme handles this
- Standard paragraph text styling — theme handles this

#### Step 5: Generate Notes Section

At the end of the generated code, include a `## Notes` section listing:
- Any animations/effects found in the Figma that were not implemented
- Image placeholders that need real WordPress media IDs
- Any interactive behaviors that require additional configuration
- Suggested custom CSS if decorative effects were detected

### Complete Real-World Example

**Input:** Figma design with hero section, features grid, testimonials, and CTA.

**Output (Classic Mode ready):**

```
[vc_row width="custom" width_custom="840px"][vc_column][us_text text="Potenziato dall'Intelligenza Artificiale" css="%7B%22default%22%3A%7B%22color%22%3A%22%231447E6%22%2C%22text-align%22%3A%22center%22%2C%22font-size%22%3A%2214px%22%2C%22line-height%22%3A%222%22%2C%22font-weight%22%3A%22400%22%2C%22background-color%22%3A%22%23DBEAFE%22%2C%22width%22%3A%22fit-content%22%2C%22margin-left%22%3A%22auto%22%2C%22margin-right%22%3A%22auto%22%2C%22padding-left%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%2C%22border-radius%22%3A%2220px%22%7D%7D" icon="far|stars"][us_separator size="small"][vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h1>Da Figma a WordPress <span style="background: linear-gradient(90deg,#155DFC 0%,#4F39F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">in un solo click</span></h1>
[/vc_column_text][us_separator size="small"][vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]Smetti di perdere tempo con il coding manuale. La nostra AI converte i tuoi design Figma in siti WordPress pixel-perfect, veloci e ottimizzati per la SEO.[/vc_column_text][us_separator size="small"][us_hwrapper alignment="center" inner_items_gap="1rem" valign="middle"][us_btn label="Inizia la prova gratuita" icon="fas|arrow-right" iconpos="right" style="2"][us_btn label="Guarda la demo"][/us_hwrapper][/vc_column][/vc_row][vc_row][vc_column][us_image ratio_width="21" ratio_height="9" has_ratio="1" ratio="16x9" align="center" size="full" css="%7B%22default%22%3A%7B%22border-radius%22%3A%2216px%22%7D%7D" image="IMAGE_ID"][/vc_column][/vc_row][vc_row][vc_column][us_text css="%7B%22default%22%3A%7B%22color%22%3A%22%231447E6%22%2C%22text-align%22%3A%22center%22%2C%22font-size%22%3A%2216px%22%2C%22font-weight%22%3A%22400%22%2C%22text-transform%22%3A%22uppercase%22%7D%7D" text="Caratteristiche"][vc_column_text css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"]
<h2>Tutto ciò che serve per scalare</h2>
La nostra tecnologia AI comprende il design meglio di qualsiasi altro strumento sul mercato.[/vc_column_text][us_separator size="large"][vc_row_inner columns="3" tablets_columns="2" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|bolt" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Velocità Fulminea</h5>
Converti design complessi in secondi, non giorni. Risparmia fino al 90% del tempo di sviluppo.[/vc_column_text][/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|code" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Codice Pulito</h5>
Codice React e PHP generato semanticamente corretto, facile da mantenere ed estendere.[/vc_column_text][/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|browser" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Pixel Perfect</h5>
Ogni margine, colore e font viene rispettato con precisione millimetrica.[/vc_column_text][/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|globe" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>SEO Ottimizzato</h5>
Struttura HTML ottimizzata per i motori di ricerca, con meta tag e performance elevate.[/vc_column_text][/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|mobile" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Totalmente Responsivo</h5>
I layout si adattano automaticamente a desktop, tablet e mobile senza configurazioni extra.[/vc_column_text][/vc_column_inner][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%2C%22border-radius%22%3A%2216px%22%7D%7D"][us_iconbox icon="far|shield-check" iconpos="left" alignment="left" size="24px" el_class="icone" color="custom" icon_color="#ffffff"][/us_iconbox][vc_column_text]
<h5>Sicurezza Integrata</h5>
Best practices di sicurezza WordPress implementate di default in ogni conversione.[/vc_column_text][/vc_column_inner][/vc_row_inner][/vc_column][/vc_row]
```

### Testimonial Section Example

```
[vc_row css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%7D%7D"][vc_column][us_text text="Scelto da migliaia di designer" tag="h3" css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"][us_separator][vc_row_inner columns="3" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"][vc_column_inner width="1/3" css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23ffffff%22%2C%22border-radius%22%3A%2216px%22%2C%22box-shadow-h-offset%22%3A%220%22%2C%22box-shadow-v-offset%22%3A%221px%22%2C%22box-shadow-blur%22%3A%223px%22%2C%22box-shadow-spread%22%3A%220%22%2C%22box-shadow-color%22%3A%22%23000000%22%7D%7D"][us_hwrapper inner_items_gap="0rem"][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][us_iconbox size="18px" color="custom" icon_color="#FDC700"][/us_iconbox][/us_hwrapper][us_separator size="custom" height="10px"][vc_column_text css="%7B%22default%22%3A%7B%22color%22%3A%22%234A5565%22%2C%22font-size%22%3A%2216px%22%2C%22font-style%22%3A%22italic%22%7D%7D"]"Quote text goes here."[/vc_column_text][us_separator size="custom" height="30px"][us_hwrapper valign="middle"][us_image ratio_width="21" ratio_height="9" has_ratio="1" size="full" image="IMAGE_ID" style="circle" css="%7B%22default%22%3A%7B%22width%22%3A%2248px%22%2C%22height%22%3A%2248px%22%7D%7D"][us_vwrapper inner_items_gap="0rem"][us_text text="Author Name" css="%7B%22default%22%3A%7B%22font-size%22%3A%2216px%22%2C%22font-weight%22%3A%22700%22%7D%7D"][us_text text="Author Role" css="%7B%22default%22%3A%7B%22color%22%3A%22%236A7282%22%2C%22font-size%22%3A%2214px%22%7D%7D"][/us_vwrapper][/us_hwrapper][/vc_column_inner][/vc_row_inner][/vc_column][/vc_row]
```

### CTA Section Example

```
[vc_row width="custom" width_custom="896px"][vc_column css="%7B%22default%22%3A%7B%22color%22%3A%22%23ffffff%22%2C%22text-align%22%3A%22center%22%2C%22background-color%22%3A%22%23155DFC%22%2C%22border-radius%22%3A%2220px%22%7D%7D"][us_text text="Pronto a trasformare il tuo workflow?" tag="h3"][us_separator size="small"][vc_column_text css="%7B%22default%22%3A%7B%22width%22%3A%22643px%22%2C%22margin-left%22%3A%22auto%22%2C%22margin-right%22%3A%22auto%22%7D%7D"]Unisciti a oltre 10.000 designer e sviluppatori che stanno già costruendo il web del futuro, oggi.[/vc_column_text][us_separator size="small"][us_hwrapper alignment="center" inner_items_gap="1rem" valign="middle"][us_btn label="Inizia Gratuitamente" iconpos="right" style="2"][us_btn label="Contatta il team"][/us_hwrapper][us_separator size="small"][vc_column_text css="%7B%22default%22%3A%7B%22color%22%3A%22%23BEDBFF%22%2C%22font-size%22%3A%2214px%22%7D%7D"]Nessuna carta di credito richiesta. 14 giorni di prova gratuita.[/vc_column_text][/vc_column][/vc_row]
```

### From Written Description

#### Example Input:
"Create a hero section with a large heading, subheading, two CTAs side by side, and a background image"

#### Output:
```
[vc_row css="%7B%22default%22%3A%7B%22background-color%22%3A%22%23000000%22%7D%7D" height="large" valign="middle"][vc_column css="%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D"][vc_column_text css="%7B%22default%22%3A%7B%22color%22%3A%22%23ffffff%22%2C%22text-align%22%3A%22center%22%7D%7D"]
<h1>Transform Your Business Today</h1>
[/vc_column_text][us_separator size="small"][vc_column_text css="%7B%22default%22%3A%7B%22color%22%3A%22%23ffffff%22%2C%22text-align%22%3A%22center%22%7D%7D"]Join thousands of companies already succeeding with our platform.[/vc_column_text][us_separator size="small"][us_hwrapper alignment="center" inner_items_gap="1rem" valign="middle" wrap="1"][us_btn label="Get Started Free" style="2" icon="fas|arrow-right" iconpos="right"][us_btn label="Watch Demo"][/us_hwrapper][/vc_column][/vc_row]
```

---

## Responsive Design Best Practices

### Device Breakpoints

Impreza uses these breakpoints:
- **Desktop**: 1280px+
- **Laptop**: 1024px – 1279px
- **Tablet**: 768px – 1023px
- **Mobile**: < 768px

### Responsive Strategies

#### 1. Grid Column Adjustments
Use `vc_row_inner` with `columns` and `tablets_columns` (always include 1rem padding):
```
[vc_row_inner columns="3" tablets_columns="2" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"]
```

#### 2. Hide on Devices
```
[us_image image="12345" hide_on_tablet="yes" hide_on_mobile="yes"]
[us_btn label="Call Now" hide_on_desktop="yes" hide_on_laptop="yes"]
```

#### 3. Image Aspect Ratios
```
[us_image image="12345" has_ratio="1" ratio="16x9"]
```

---

## Performance Optimization

### Essential Settings

Navigate to **Impreza > Theme Options > Advanced Settings > Website Performance**:

#### 1. Disable Extra WPBakery Features
✅ **ALWAYS ENABLE** (unless you specifically need Grid Builder)

```
Theme Options > Advanced Settings > Website Performance
☑ Disable extra features of WPBakery Page Builder
```

#### 2. Assets Optimization
```
Theme Options > Advanced Settings > Website Performance
☑ Optimize CSS Output
☑ Optimize JavaScript Output
☑ Lazy Load Images
☑ Minify HTML Output
```

#### 3. Icon Library
Load only icons actually used:
```
Theme Options > Advanced Settings > Icon Sets
☑ Load only used icons (automatic detection)
```

### Image Optimization

- **Use WebP format** (with JPG fallback)
- **Compress before upload** (TinyPNG, Squoosh)
- **Use appropriate sizes**: Full-width hero: 1920px, Grid items: 800px, Thumbnails: 400px
- **Enable lazy loading**: Impreza has built-in lazy load
- **Use CDN**: Cloudflare, CloudFront, or similar

### Caching Strategy

**Recommended Plugins:**
1. **WP Rocket** (premium) — most comprehensive
2. **Hummingbird** — WPMU DEV
3. **WP Super Cache** — free alternative

---

## Custom CSS Integration

### Adding Custom Styles

Navigate to **Impreza > Theme Options > Custom CSS**:

```css
/* Custom button hover effect */
.us-btn-container .us-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

/* Responsive utilities */
@media (max-width: 767px) {
    .hide-mobile {
        display: none !important;
    }
}
```

### Element-Specific CSS

Use `el_class` parameter:
```
[us_iconbox icon="far|bolt" el_class="icone"][/us_iconbox]
```

Then in Custom CSS:
```css
.icone .w-iconbox-icon {
    background: linear-gradient(135deg, #155DFC 0%, #4F39F6 100%);
    border-radius: 8px;
    padding: 8px;
}
```

### CSS Variables

Impreza uses CSS variables for theming:
```css
:root {
    --color-primary: #1E88E5;
    --color-secondary: #FF6F00;
}
```

---

## Version Control & Deployment

### Export/Import Pages

#### Export Single Page:
1. Edit page in WPBakery Backend Editor
2. Click "Classic Mode" tab
3. Copy all shortcode content (compact format)
4. Save to version control

#### Import Page:
1. Create new page
2. Switch to "Classic Mode"
3. Paste shortcode content
4. Update to Frontend/Backend editor
5. Publish

### Child Theme Development

Always use child theme for customizations:

**style.css:**
```css
/*
Theme Name: Impreza Child
Template: Impreza
Version: 1.0.0
*/
```

**functions.php:**
```php
<?php
add_action('wp_enqueue_scripts', 'impreza_child_enqueue_styles');
function impreza_child_enqueue_styles() {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array('parent-style'),
        wp_get_theme()->get('Version')
    );
}
?>
```

---

## Security Best Practices

### Sanitization & Escaping

```php
$clean_text = sanitize_text_field($_POST['input']);
$clean_url = esc_url($_POST['url']);
$clean_email = sanitize_email($_POST['email']);
echo esc_html($user_content);
echo esc_attr($attribute_value);
```

### Nonce Verification

```php
wp_nonce_field('custom_form_action', 'custom_form_nonce');
if (!wp_verify_nonce($_POST['custom_form_nonce'], 'custom_form_action')) {
    wp_die('Security check failed');
}
```

### SQL Injection Prevention

```php
global $wpdb;
$results = $wpdb->get_results($wpdb->prepare(
    "SELECT * FROM table WHERE id = %d",
    $_GET['id']
));
```

---

## Accessibility (a11y) Guidelines

### Semantic HTML
Use proper heading hierarchy — always via `[vc_column_text]`:
```
[vc_column_text]<h1>Main Page Title</h1>[/vc_column_text]
[vc_column_text]<h2>Section Title</h2>[/vc_column_text]
[vc_column_text]<h3>Subsection Title</h3>[/vc_column_text]
```

### Color Contrast
Maintain WCAG AA standards (4.5:1 for normal text).

### Alt Text for Images
```
[us_image image="12345" alt="Descriptive alt text for screen readers"]
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: CSS not applying
**Cause**: Using old `.vc_custom_xxx{}` format
**Solution**: Use Impreza JSON URL-encoded format: `css="%7B%22default%22%3A%7B...%7D%7D"`

#### Issue: Shortcodes not rendering after paste in Classic Mode
**Cause**: Multi-line formatted shortcodes with indentation
**Solution**: Use compact single-line format

#### Issue: Buttons not styled correctly
**Cause**: Using `text=` or `style="raised"`
**Solution**: Use `label=` and numeric style `style="2"`

#### Issue: Columns Not Responsive
**Cause**: Using multiple `vc_row` instead of `vc_row_inner`
**Solution**: Use `[vc_row_inner columns="3" tablets_columns="2" css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"]`

#### Issue: Content not editable in builder
**Cause**: Using `[us_html]` for standard elements
**Solution**: Replace with native Impreza shortcodes

#### Issue: Accordion or Tabs not rendering
**Cause**: Using wrong shortcodes `[us_accordion]`, `[us_tabs]`
**Solution**: Use `[vc_tta_accordion]`, `[vc_tta_tabs]`, or `[vc_tta_tour]` with `[vc_tta_section]` children

#### Issue: Inner row content touching edges
**Cause**: Missing padding on `[vc_row_inner]`
**Solution**: Always add `css="%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D"`

#### Issue: Empty section appearing at bottom of page
**Cause**: Trailing empty row in generated code
**Solution**: Remove any `[vc_row][vc_column][vc_column_text][/vc_column_text][/vc_column][/vc_row]` at the end

#### Issue: Typography looks wrong
**Cause**: Overriding font styles that should come from the theme
**Solution**: Remove font-size, font-weight, font-family from headings; let theme handle it

---

## Resources & Documentation

### Official Resources
- **Impreza Documentation**: https://help.us-themes.com/impreza/
- **WPBakery Knowledge Base**: https://kb.wpbakery.com/
- **Impreza Support**: https://support.us-themes.com/
- **Changelog**: https://help.us-themes.com/impreza/changelog/

### Recommended Plugins
- **WP Rocket** — Caching & performance
- **Smush** — Image optimization
- **Yoast SEO** / **Rank Math** — SEO optimization
- **WP Mail SMTP** — Email deliverability
- **UpdraftPlus** — Backups
- **Wordfence** — Security

---

## Best Practices Summary

### DO:
✅ Use Impreza JSON URL-encoded CSS format (`%7B%22default%22%3A%7B...%7D%7D`)
✅ Use `[vc_column_text]` with HTML tags for headings (h1–h6)
✅ Use `[us_text]` for short labels, badges, and simple text
✅ Use `label=` for button text, numeric `style=` for button style
✅ Use `[vc_row_inner]` + `[vc_column_inner]` for grids
✅ Always add 1rem padding on all sides to every `[vc_row_inner]`
✅ Use `width="custom" width_custom="Xpx"` for row width control
✅ Let the theme handle typography (sizes, weights, families)
✅ Use native Impreza elements for all standard components
✅ Output compact single-line code for Classic Mode
✅ End the output with the last meaningful `[/vc_row]` — no trailing empty rows
✅ List ignored animations/effects in a Notes section
✅ Use `[us_separator]` for spacing between elements
✅ Use `[us_hwrapper]` for horizontal layouts (buttons, author info)
✅ Use `[us_vwrapper]` for vertical stacking with controlled gaps
✅ Use `[vc_tta_accordion]` for accordions, `[vc_tta_tabs]` for tabs, `[vc_tta_tour]` for vertical tabs
✅ Use `[vc_tta_section]` inside all tabbed elements (accordion, tabs, tour)
✅ Test on multiple devices and browsers
✅ Optimize images before upload
✅ Create child theme for customizations

### DON'T:
❌ Use `.vc_custom_xxx{}` CSS format — it's broken in Impreza
❌ Use `[us_html]` for standard elements (icons, cards, images, stars)
❌ Extract font sizes/weights/families from Figma for standard tags
❌ Use `text=` for buttons (use `label=`)
❌ Use `style="raised"` for buttons (use numeric style IDs)
❌ Use multiple `vc_row` to create a single grid
❌ Use CSS padding to control row width
❌ Format shortcodes with multi-line indentation
❌ Implement animations/hover effects from Figma designs
❌ Use inline `<img>`, `<i>`, `<div class="card">` HTML for standard components
❌ Use `[us_heading]` for headings — use `[vc_column_text]` with HTML tags instead
❌ Override theme typography in generated code
❌ Add empty trailing rows at the end of output
❌ Forget 1rem padding on `[vc_row_inner]`
❌ Use `[us_accordion]`, `[us_tabs]` — these are wrong shortcodes
❌ Use `[us_accordion_item]`, `[us_tab]` — use `[vc_tta_section]` instead

---

## CSS Encoding Quick Reference

For quick encoding of common CSS properties:

| JSON | URL-encoded |
|---|---|
| `{"default":{"text-align":"center"}}` | `%7B%22default%22%3A%7B%22text-align%22%3A%22center%22%7D%7D` |
| `{"default":{"background-color":"#F9FAFB"}}` | `%7B%22default%22%3A%7B%22background-color%22%3A%22%23F9FAFB%22%7D%7D` |
| `{"default":{"color":"#ffffff","text-align":"center","background-color":"#155DFC","border-radius":"20px"}}` | `%7B%22default%22%3A%7B%22color%22%3A%22%23ffffff%22%2C%22text-align%22%3A%22center%22%2C%22background-color%22%3A%22%23155DFC%22%2C%22border-radius%22%3A%2220px%22%7D%7D` |
| `{"default":{"width":"48px","height":"48px"}}` | `%7B%22default%22%3A%7B%22width%22%3A%2248px%22%2C%22height%22%3A%2248px%22%7D%7D` |
| `{"default":{"font-size":"14px","font-weight":"700"}}` | `%7B%22default%22%3A%7B%22font-size%22%3A%2214px%22%2C%22font-weight%22%3A%22700%22%7D%7D` |
| `{"default":{"box-shadow-h-offset":"0","box-shadow-v-offset":"1px","box-shadow-blur":"3px","box-shadow-spread":"0","box-shadow-color":"#000000"}}` | `%7B%22default%22%3A%7B%22box-shadow-h-offset%22%3A%220%22%2C%22box-shadow-v-offset%22%3A%221px%22%2C%22box-shadow-blur%22%3A%223px%22%2C%22box-shadow-spread%22%3A%220%22%2C%22box-shadow-color%22%3A%22%23000000%22%7D%7D` |
| `{"default":{"padding-left":"1rem","padding-top":"1rem","padding-bottom":"1rem","padding-right":"1rem"}}` | `%7B%22default%22%3A%7B%22padding-left%22%3A%221rem%22%2C%22padding-top%22%3A%221rem%22%2C%22padding-bottom%22%3A%221rem%22%2C%22padding-right%22%3A%221rem%22%7D%7D` |

---

## Version History

- **v2.1.0** (2026-02-20): Bug fixes from testing
  - Fixed: trailing empty rows `[vc_row][vc_column][vc_column_text][/vc_column_text][/vc_column][/vc_row]` (Rule 7)
  - Fixed: `vc_row_inner` now always requires 1rem padding on all sides (Rule 8)
  - Fixed: accordion shortcode — `[vc_tta_accordion]` + `[vc_tta_section]` instead of wrong `[us_accordion]` + `[us_accordion_item]`
  - Fixed: tabs shortcode — `[vc_tta_tabs]` + `[vc_tta_section]` instead of wrong `[us_tabs]` + `[us_tab]`
  - Added: vertical tabs / tour — `[vc_tta_tour]` + `[vc_tta_section]`
  - Added: tabbed elements quick reference table
  - Updated: all inner row examples now include required 1rem padding
  - Updated: Figma-to-Impreza mapping table with accordion/tabs/tour
  - Updated: DO/DON'T checklist with new rules
  - Added: inner row 1rem padding to CSS encoding quick reference
- **v2.0.0** (2026-02-20): Major rewrite — corrected critical errors
  - Fixed CSS format: Impreza JSON URL-encoded instead of `.vc_custom_xxx{}`
  - Fixed typography: theme handles h1–h6 styling, not generated code
  - Fixed buttons: `label` instead of `text`, numeric `style` values
  - Fixed grids: `vc_row_inner`/`vc_column_inner` instead of multiple `vc_row`
  - Fixed row width: native `width`/`width_custom` parameters
  - Fixed Classic Mode output: compact single-line format
  - Removed `[us_html]` abuse — all examples use native shortcodes
  - Added complete real-world examples from manual testing
  - Added CSS encoding quick reference table
  - Added comprehensive Critical Rules section
  - Added Typography Decision Guide
  - Animations/effects: ignored in code, noted separately
- **v1.0.0** (2026-02-19): Initial release
