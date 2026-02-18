---
name: canvas-component-utils
description:
  Use utility components to render formatted text and media correctly. Use when
  (1) Rendering HTML text content from props, (2) Displaying images, (3) Working
  with formatted text or media. Covers FormattedText and Image utilities.
---

Import utilities from the `drupal-canvas` package:

```jsx
import { FormattedText, Image } from "drupal-canvas";
```

## FormattedText

Use `FormattedText` to render HTML content from props. This is required for any
prop with `contentMediaType: text/html` in component.yml.

```yaml
# component.yml
props:
  properties:
    text:
      title: Text
      type: string
      contentMediaType: text/html
      x-formatting-context: block
      examples:
        - <p>This is <strong>formatted</strong> text.</p>
```

```jsx
import { FormattedText } from "drupal-canvas";

const Text = ({ text, className }) => (
  <FormattedText className={className}>{text}</FormattedText>
);
```

**When to use FormattedText:**

- Props that accept rich text/HTML content
- Any prop with `contentMediaType: text/html`
- Content that may contain `<p>`, `<strong>`, `<em>`, `<a>`, or other HTML tags

**Do NOT use FormattedText for:**

- Plain text props (type: string without contentMediaType)
- Headings or titles (use regular elements)

## Image

Use `Image` for responsive image rendering. It handles responsive behavior and
optimization automatically.

```yaml
# component.yml
props:
  properties:
    image:
      title: Image
      type: object
      $ref: json-schema-definitions://canvas.module/image
      examples:
        - src: https://example.com/photo.jpg
          alt: Description of image
          width: 800
          height: 600
```

```jsx
import { Image } from "drupal-canvas";

const Card = ({ image }) => {
  const { src, alt, width, height } = image;
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      className="w-full rounded-lg object-cover"
    />
  );
};
```

**Image props:**

- `src` - Image URL (required)
- `alt` - Alt text for accessibility (required)
- `width` - Original image width
- `height` - Original image height
- `className` - Tailwind classes for styling
