---
name: component-docs
description: Generate or update component documentation with usage examples, props tables, and Storybook stories. Use when documenting new components or improving existing component docs.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Component Documentation Skill

This skill helps you create and maintain component documentation in `packages/ui/`.

## When to Use This Skill

- Writing documentation for new components
- Creating usage examples and code snippets
- Documenting component props and variants
- Setting up Storybook stories
- Generating API documentation
- Maintaining component README files

## Documentation Structure

```
packages/ui/
├── src/
│   ├── components/
│   │   ├── button.tsx          # Component implementation
│   │   ├── button.stories.tsx  # Storybook stories (optional)
│   │   └── __tests__/
│   │       └── button.test.tsx # Component tests
├── docs/
│   ├── components/
│   │   ├── button.md           # Component documentation
│   │   └── card.md
│   └── guides/
│       ├── getting-started.md
│       └── customization.md
└── README.md                    # Package overview
```

## Component Documentation Template

### Basic Component Documentation

```markdown
# Button

A customizable button component built with Radix UI primitives.

## Installation

This component is part of the `@sgcarstrends/ui` package.

\`\`\`bash
pnpm add @sgcarstrends/ui
\`\`\`

## Usage

\`\`\`tsx
import { Button } from "@sgcarstrends/ui";

export function Example() {
  return <Button>Click me</Button>;
}
\`\`\`

## Variants

### Default

\`\`\`tsx
<Button variant="default">Default Button</Button>
\`\`\`

### Destructive

\`\`\`tsx
<Button variant="destructive">Delete</Button>
\`\`\`

### Outline

\`\`\`tsx
<Button variant="outline">Outline Button</Button>
\`\`\`

## Sizes

\`\`\`tsx
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon">
  <Icon />
</Button>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | `"default" \| "destructive" \| "outline" \| "secondary" \| "ghost" \| "link"` | `"default"` | The visual style of the button |
| size | `"default" \| "sm" \| "lg" \| "icon"` | `"default"` | The size of the button |
| asChild | `boolean` | `false` | Render as child element |
| disabled | `boolean` | `false` | Whether button is disabled |

## Examples

### With Icon

\`\`\`tsx
import { Button } from "@sgcarstrends/ui";
import { DownloadIcon } from "lucide-react";

export function DownloadButton() {
  return (
    <Button>
      <DownloadIcon className="mr-2 h-4 w-4" />
      Download
    </Button>
  );
}
\`\`\`

### Loading State

\`\`\`tsx
"use client";

import { useState } from "react";
import { Button } from "@sgcarstrends/ui";

export function LoadingButton() {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <Button disabled={isLoading} onClick={() => setIsLoading(true)}>
      {isLoading ? "Loading..." : "Submit"}
    </Button>
  );
}
\`\`\`

### As Link

\`\`\`tsx
import { Button } from "@sgcarstrends/ui";
import Link from "next/link";

export function LinkButton() {
  return (
    <Button asChild>
      <Link href="/about">Learn More</Link>
    </Button>
  );
}
\`\`\`

## Accessibility

- Uses semantic `<button>` element
- Supports keyboard navigation (Enter, Space)
- Proper focus states
- ARIA attributes supported via props

## Styling

The Button component uses Tailwind CSS and CSS variables for theming. Customize via:

\`\`\`tsx
<Button className="custom-classes">Custom Styled</Button>
\`\`\`

## Related Components

- [Link Button](#)
- [Icon Button](#)
- [Button Group](#)
```

## JSDoc Comments

Add comprehensive JSDoc comments to components:

```typescript
/**
 * A customizable button component with multiple variants and sizes.
 *
 * @component
 * @example
 * ```tsx
 * <Button variant="default" size="md">
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /**
   * Render the button as a child element (e.g., Link)
   * @default false
   */
  asChild?: boolean;

  /**
   * The visual style variant of the button
   * @default "default"
   */
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";

  /**
   * The size of the button
   * @default "default"
   */
  size?: "default" | "sm" | "lg" | "icon";
}

/**
 * Button component
 *
 * @param {ButtonProps} props - Button props
 * @returns {React.ReactElement} Button element
 *
 * @example
 * Basic usage
 * ```tsx
 * <Button>Click me</Button>
 * ```
 *
 * @example
 * With variant
 * ```tsx
 * <Button variant="destructive">Delete</Button>
 * ```
 *
 * @example
 * As a link
 * ```tsx
 * <Button asChild>
 *   <Link href="/about">About</Link>
 * </Button>
 * ```
 */
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";
```

## Storybook Stories

### Installing Storybook (if not present)

```bash
cd packages/ui

# Initialize Storybook
npx storybook@latest init
```

### Basic Story

```typescript
// packages/ui/src/components/button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta = {
  title: "Components/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "destructive", "outline", "secondary", "ghost", "link"],
    },
    size: {
      control: "select",
      options: ["default", "sm", "lg", "icon"],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Button",
  },
};

export const Destructive: Story = {
  args: {
    variant: "destructive",
    children: "Delete",
  },
};

export const Outline: Story = {
  args: {
    variant: "outline",
    children: "Outline",
  },
};

export const Small: Story = {
  args: {
    size: "sm",
    children: "Small Button",
  },
};

export const Large: Story = {
  args: {
    size: "lg",
    children: "Large Button",
  },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <span className="mr-2">📥</span>
        Download
      </>
    ),
  },
};

export const Disabled: Story = {
  args: {
    children: "Disabled Button",
    disabled: true,
  },
};
```

### Complex Story with Interactions

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { within, userEvent, expect } from "@storybook/test";
import { Card, CardHeader, CardTitle, CardContent } from "./card";

const meta = {
  title: "Components/Card",
  component: Card,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
      </CardHeader>
      <CardContent>
        <p>Card content goes here.</p>
      </CardContent>
    </Card>
  ),
};

export const WithInteraction: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Interactive Card</CardTitle>
      </CardHeader>
      <CardContent>
        <button data-testid="card-button">Click me</button>
      </CardContent>
    </Card>
  ),
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByTestId("card-button");

    await userEvent.click(button);
    await expect(button).toBeInTheDocument();
  },
};
```

## TypeDoc for API Documentation

### Setup TypeDoc

```bash
cd packages/ui

pnpm add -D typedoc
```

Add to `package.json`:

```json
{
  "scripts": {
    "docs:generate": "typedoc --out docs/api src/index.ts"
  }
}
```

### TypeDoc Configuration

```typescript
// packages/ui/typedoc.json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "exclude": ["**/*.test.ts", "**/*.stories.tsx"],
  "excludePrivate": true,
  "excludeProtected": true,
  "plugin": ["typedoc-plugin-markdown"],
  "readme": "README.md",
  "theme": "default"
}
```

Generate documentation:

```bash
pnpm docs:generate
```

## README Documentation

### Package README Template

```markdown
# @sgcarstrends/ui

Shared UI component library for SG Cars Trends platform.

## Installation

\`\`\`bash
pnpm add @sgcarstrends/ui
\`\`\`

## Usage

\`\`\`tsx
import { Button, Card, Dialog } from "@sgcarstrends/ui";

export function Example() {
  return (
    <Card>
      <Button>Click me</Button>
    </Card>
  );
}
\`\`\`

## Components

### Core Components
- [Button](docs/components/button.md) - Customizable button with variants
- [Card](docs/components/card.md) - Container for content
- [Dialog](docs/components/dialog.md) - Modal dialog
- [Badge](docs/components/badge.md) - Status badges

### Form Components
- [Input](docs/components/input.md) - Text input
- [Textarea](docs/components/textarea.md) - Multi-line text input
- [Select](docs/components/select.md) - Dropdown select
- [Checkbox](docs/components/checkbox.md) - Checkbox input

### Layout Components
- [Separator](docs/components/separator.md) - Visual divider
- [Tabs](docs/components/tabs.md) - Tabbed interface

## Styling

Components use Tailwind CSS and CSS variables for theming.

### Dark Mode

Dark mode is supported via CSS variables defined in \`globals.css\`.

### Customization

Customize component styles:

\`\`\`tsx
<Button className="custom-classes">Custom Button</Button>
\`\`\`

## Development

\`\`\`bash
# Install dependencies
pnpm install

# Run tests
pnpm test

# Run Storybook
pnpm storybook

# Build package
pnpm build
\`\`\`

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## License

MIT
```

## Props Table Generator

Create a script to generate props tables from TypeScript:

```typescript
// scripts/generate-props-table.ts
import * as ts from "typescript";
import * as fs from "fs";

function generatePropsTable(componentPath: string) {
  const program = ts.createProgram([componentPath], {});
  const sourceFile = program.getSourceFile(componentPath);

  if (!sourceFile) return;

  const checker = program.getTypeChecker();

  ts.forEachChild(sourceFile, (node) => {
    if (ts.isInterfaceDeclaration(node) && node.name.text.endsWith("Props")) {
      console.log(`| Prop | Type | Default | Description |`);
      console.log(`|------|------|---------|-------------|`);

      node.members.forEach((member) => {
        if (ts.isPropertySignature(member) && member.name) {
          const name = member.name.getText(sourceFile);
          const type = checker.typeToString(
            checker.getTypeAtLocation(member)
          );
          const docs = ts.displayPartsToString(
            member.symbol?.getDocumentationComment(checker)
          );

          console.log(`| ${name} | \`${type}\` | - | ${docs} |`);
        }
      });
    }
  });
}

// Usage
generatePropsTable("src/components/button.tsx");
```

## Component Checklist

When documenting a component, ensure:

- [ ] Component file has JSDoc comments
- [ ] Props interface is fully documented
- [ ] Markdown documentation file exists
- [ ] Usage examples provided
- [ ] Props table included
- [ ] Variants documented
- [ ] Accessibility notes added
- [ ] Related components linked
- [ ] Storybook stories created (if using Storybook)
- [ ] Exported from package index
- [ ] Added to README component list

## Documentation Patterns

### Code Examples

Always provide working code examples:

```markdown
## Example: Search Form

\`\`\`tsx
"use client";

import { useState } from "react";
import { Input, Button } from "@sgcarstrends/ui";

export function SearchForm() {
  const [query, setQuery] = useState("");

  return (
    <form className="flex gap-2">
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <Button type="submit">Search</Button>
    </form>
  );
}
\`\`\`
```

### Do's and Don'ts

```markdown
## Best Practices

### ✅ Do

- Use semantic HTML elements
- Provide accessible labels
- Test keyboard navigation
- Support dark mode

### ❌ Don't

- Nest buttons inside buttons
- Forget hover states
- Override core styles directly
- Skip accessibility attributes
```

## Automated Documentation

### Using react-docgen

```bash
pnpm add -D react-docgen-typescript
```

```typescript
// scripts/generate-docs.ts
import { parse } from "react-docgen-typescript";

const options = {
  savePropValueAsString: true,
  shouldExtractLiteralValuesFromEnum: true,
};

const docs = parse("src/components/button.tsx", options);

console.log(JSON.stringify(docs, null, 2));
```

## Testing Documentation

Ensure examples work:

```typescript
// __tests__/docs/examples.test.tsx
import { render } from "@testing-library/react";

// Test all documented examples
describe("Documentation Examples", () => {
  it("renders basic button example", () => {
    const { container } = render(<Button>Click me</Button>);
    expect(container.querySelector("button")).toBeInTheDocument();
  });

  it("renders button with icon example", () => {
    const { container } = render(
      <Button>
        <span className="mr-2">📥</span>
        Download
      </Button>
    );
    expect(container.textContent).toContain("Download");
  });
});
```

## References

- Related files:
  - `packages/ui/docs/` - Component documentation
  - `packages/ui/README.md` - Package overview
  - `packages/ui/src/components/*.stories.tsx` - Storybook stories
  - `packages/ui/CLAUDE.md` - UI package documentation

## Best Practices

1. **Clear Examples**: Provide complete, working code examples
2. **Props Documentation**: Document every prop with type and description
3. **Accessibility**: Include accessibility notes
4. **Visual Examples**: Use Storybook for interactive demos
5. **Keep Updated**: Update docs when components change
6. **Search Friendly**: Use clear headings and keywords
7. **Code Quality**: Test documented examples
8. **Version History**: Track changes in documentation
