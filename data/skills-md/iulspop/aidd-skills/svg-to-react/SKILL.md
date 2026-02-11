---
name: svg-to-react
description: Converts SVG files into optimized React TypeScript components with proper accessibility attributes, currentColor fills, and consistent naming conventions. Use when adding icons or SVG assets to a React project.
---

# SVG to React

Act as a senior React and TypeScript engineer specializing in SVG optimization and React component generation.

Convert the following SVG to a React component: $ARGUMENTS

## Rules

- Always use TypeScript.
- Always add aria-hidden="true" to SVGs.
- Always spread props to allow style overrides.
- Always format component name as PascalCase + "Icon" suffix.
- Always use IconProps from '~/utils/types'.
- Always use className prop for styling.
- Always use currentColor for fill.
- Format output with 2 space indentation.
- Sort SVG attributes alphabetically.
- Extract viewBox from width/height if not present.
- Remove hardcoded dimensions (width, height).
- Remove fill="none" from root svg.
- Remove fill="#fff" from paths.
- Remove unnecessary groups and clip paths.
- Export as named function component.
- Use type import for IconProps.
- Spread props last to allow overrides.
- Preserve SVG viewBox.
- Remove hardcoded colors.
- Place each component in its own file.
- Name the file same as the component in kebab-case.
- Delete original SVG file after successful conversion.

## Example Output

```tsx
import type { IconProps } from '~/utils/types';

export function ShortsIcon({ className, ...props }: IconProps) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      fill="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path
        fillRule="evenodd"
        d="..."
        clipRule="evenodd"
      />
    </svg>
  );
}
```
