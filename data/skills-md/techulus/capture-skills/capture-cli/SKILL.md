---
name: capture-cli
description: Capture screenshots, generate PDFs, and extract content from any URL using the Capture CLI. Use when the user wants to screenshot a website, create a PDF of a page, extract text content, get metadata from a URL, or record an animated GIF.
---

# Capture CLI

Capture screenshots, generate PDFs, extract content, and fetch metadata from any URL using the Capture CLI.

## Prerequisites

The Capture CLI must be installed and configured with environment variables:
- `CAPTURE_KEY` - Your Capture API key
- `CAPTURE_SECRET` - Your Capture API secret

Install via Homebrew:
```bash
brew tap techulus/tap && brew install capture
```

Or via Go:
```bash
go install github.com/techulus/capture-go/cmd/capture@latest
```

## Screenshot

```bash
capture screenshot <url> -o <file.png>
```

Options (pass with `-X key=value`):

| Option | Default | Description |
|--------|---------|-------------|
| vw | 1440 | Viewport width |
| vh | 900 | Viewport height |
| scaleFactor | 1 | Screen scale factor (dpr) |
| full | false | Capture full page |
| darkMode | false | Dark mode screenshot |
| delay | 0 | Delay in seconds before capturing |
| waitFor | - | Wait for CSS selector to appear |
| waitForId | - | Wait for element ID to appear |
| selector | - | Screenshot element matching this selector |
| selectorId | - | Screenshot element matching this ID |
| top | 0 | Top offset for clipping |
| left | 0 | Left offset for clipping |
| width | viewport | Clipping width |
| height | viewport | Clipping height |
| blockCookieBanners | false | Dismiss cookie consent banners |
| blockAds | false | Block ads |
| bypassBotDetection | false | Bypass bot detection / solve captchas |
| transparent | false | Transparent background |
| emulateDevice | - | Emulate device (iphone_14, iphone_15_pro, ipad, pixel_8, etc.) |
| type | png | Image type: png, jpeg, or webp |
| resizeWidth | - | Resize image width |
| resizeHeight | - | Resize image height |
| userAgent | - | Custom user agent (base64url encoded) |
| httpAuth | - | HTTP Basic Auth (base64url of username:password) |
| fresh | false | Take fresh screenshot instead of cached |

Example:
```bash
capture screenshot https://example.com -X vw=1920 -X vh=1080 -X full=true -X darkMode=true -o screenshot.png
```

## PDF

```bash
capture pdf <url> -o <file.pdf>
```

Options (pass with `-X key=value`):

| Option | Default | Description |
|--------|---------|-------------|
| format | A4 | Paper format: Letter, Legal, Tabloid, Ledger, A0-A6 |
| width | - | Custom paper width (with units, e.g., 8.5in) |
| height | - | Custom paper height (with units) |
| landscape | false | Landscape orientation |
| scale | 1 | Scale of webpage rendering |
| printBackground | false | Print background graphics |
| marginTop | - | Top margin (with units) |
| marginRight | - | Right margin (with units) |
| marginBottom | - | Bottom margin (with units) |
| marginLeft | - | Left margin (with units) |
| delay | 0 | Delay in seconds before capturing |
| userAgent | - | Custom user agent (base64url encoded) |
| httpAuth | - | HTTP Basic Auth (base64url of username:password) |

Example:
```bash
capture pdf https://example.com -X format=A4 -X landscape=true -X printBackground=true -o document.pdf
```

## Content

```bash
capture content <url> --format <markdown|html>
```

Options (pass with `-X key=value`):

| Option | Default | Description |
|--------|---------|-------------|
| delay | 0 | Delay in seconds before capturing |
| waitFor | - | Wait for CSS selector to appear |
| waitForId | - | Wait for element ID to appear |
| userAgent | - | Custom user agent (base64url encoded) |
| httpAuth | - | HTTP Basic Auth (base64url of username:password) |

CLI options:
- `--format markdown` - Output as markdown (preferred for readability)
- `--format html` - Output as HTML
- `-o <file>` - Save to file

Example:
```bash
capture content https://example.com --format markdown
```

## Metadata

```bash
capture metadata <url> --pretty
```

CLI options:
- `--pretty` - Pretty-print JSON output
- `-o <file>` - Save to file

Returns JSON with: title, description, author, logo, language, image, publisher, url, and Open Graph data.

Example:
```bash
capture metadata https://example.com --pretty
```

## Animated

```bash
capture animated <url> -o <file.gif>
```

Options (pass with `-X key=value`):

| Option | Default | Description |
|--------|---------|-------------|
| duration | 5 | Recording duration in seconds (1-30) |
| vw | 1440 | Viewport width |
| vh | 900 | Viewport height |
| scaleFactor | 1 | Device scale factor |
| delay | 0 | Seconds to wait before starting (0-25) |
| waitFor | - | Wait for CSS selector to appear |
| waitForId | - | Wait for element ID to appear |
| darkMode | false | Enable dark mode |
| hideScrollbars | true | Hide scrollbars |
| blockCookieBanners | false | Dismiss cookie consent banners |
| blockAds | false | Block ads |
| emulateDevice | - | Emulate device (iphone_15_pro, ipad, pixel_8, etc.) |
| userAgent | - | Custom user agent (base64url encoded) |
| httpAuth | - | HTTP Basic Auth (base64url of username:password) |

Example:
```bash
capture animated https://example.com -X duration=10 -X darkMode=true -o recording.gif
```

## Global CLI Options

| Option | Description |
|--------|-------------|
| -o | Output file path (required for screenshot, pdf, animated) |
| -X | Pass API options (e.g., -X vw=1920) |
| --edge | Use edge mode for faster response |
| --dry-run | Preview the API URL without executing |

## Tips

- Use `--edge` for faster responses when latency matters
- Use `--dry-run` to preview the API URL without executing
- Prefer `--format markdown` for content extraction (more readable)
- Always specify output file with `-o` for screenshot, pdf, and animated commands
- Common devices for emulation: iphone_14, iphone_15_pro, ipad, pixel_8
- For full-page screenshots, use `-X full=true`
- For dark mode, use `-X darkMode=true`
