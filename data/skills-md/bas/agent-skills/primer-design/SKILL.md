---
name: primer-design
description: Create distinctive, production-grade frontend interfaces with high design quality using the primer design system and brand guidelines. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates polished code and UI design that fully conforms to the primer design system.
---

# Primer Design Instructions 

This skill guides creation of production-grade frontend interfaces that follow the HitHub Primer brand design guidelines. Implement real working code with exceptional attention to the primer design system guidelines, Brand UI, Primer React Components and Octicons.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a clear aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Follow GitHub's professional yet friendly brand voice - clear, welcoming, and developer-focused
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this memorable? Focus on clean, functional design with intentional visual hierarchy

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. The Primer design system emphasizes clarity and usability over decoration.

Then implement working code that is:
- Production-grade and functional
- Visually clear and usable
- Cohesive with Primer's design principles
- Meticulously refined in every detail

## Constraints

Always follow the brand guidelines: https://brand.github.com/.

Start here: https://primer.style/brand/introduction/getting-started/.

### Installation & Setup

1. Install required packages:
```bash
npm install @primer/react-brand @primer/octicons-react
```

2. **CRITICAL**: Import the Primer CSS in your root layout/app file:
```tsx
import "@primer/react-brand/lib/css/main.css";
```

3. **CRITICAL**: Handle CommonJS compatibility with Vite/React Router. Use default import with destructuring:
```tsx
// ✅ CORRECT - Use default import with destructuring for CommonJS compatibility
import pkg from "@primer/react-brand";
const { ThemeProvider, Button, Hero, Heading, Text, Grid, Stack } = pkg;
```

4. Wrap your app with ThemeProvider at the root:
```tsx
import pkg from "@primer/react-brand";
const { ThemeProvider } = pkg;

function App() {
  return (
    <ThemeProvider>
      <div>...</div>
    </ThemeProvider>
  )
}
```

### Using Primer React Components

**ALWAYS use official Primer React Brand components** instead of custom HTML/CSS. Key components:

### Hero Component

Use className prop for custom styling, or use Box component for padding/margin control:

```tsx
import pkg from "@primer/react-brand";
const { Hero, Box } = pkg;

// ✅ OPTION 1: Using className with custom CSS
<Hero className="custom-hero-padding" align="center">
  <Hero.Label>Label</Hero.Label>
  <Hero.Heading>This is my super sweet hero heading</Hero.Heading>
  <Hero.Description>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
  </Hero.Description>
  <Hero.PrimaryAction href="#">Primary action</Hero.PrimaryAction>
  <Hero.SecondaryAction href="#">Secondary action</Hero.SecondaryAction>
  <Hero.Image src="/path/to/image.png" alt="Description" />
</Hero>

// ✅ OPTION 2: Using Box component for layout
<Box paddingBlockStart={128} paddingBlockEnd={128}>
  <Hero align="center">
    <Hero.Label>Label</Hero.Label>
    <Hero.Heading>This is my super sweet hero heading</Hero.Heading>
    <Hero.Description>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </Hero.Description>
    <Hero.PrimaryAction href="#">Primary action</Hero.PrimaryAction>
  </Hero>
</Box>
```

#### Button Component with Octicons
Reference: https://primer.style/brand/components/Button/react/

```tsx
import pkg from "@primer/react-brand";
const { Button } = pkg;
import { PackageIcon, SearchIcon } from "@primer/octicons-react";

// ✅ CORRECT - Use leadingVisual/trailingVisual props for icons
<Button 
  variant="primary"
  leadingVisual={<PackageIcon />}
  hasArrow={false}
  block
>
  Add to Cart
</Button>

// Available variants: 'primary', 'secondary', 'subtle', 'accent'
// Available sizes: 'small', 'medium', 'large'
// Props: block, hasArrow, leadingVisual, trailingVisual

// ✅ Octicons support fill, className, and style props
<Button leadingVisual={<PackageIcon fill="#0969da" />}>
  Add to Cart
</Button>

// ✅ Also valid - using className
<Button leadingVisual={<PackageIcon className="custom-icon" />}>
  Add to Cart
</Button>

// ✅ Also valid - wrapping in div for additional styling
<Button leadingVisual={<div style={{ color: "#0969da" }}><PackageIcon /></div>}>
  Add to Cart
</Button>
```

#### Layout Components
```tsx
import pkg from "@primer/react-brand";
const { Grid, Stack, Box } = pkg;

// Grid for responsive layouts
<Grid>
  <Grid.Column span={{ medium: 4 }}>Content</Grid.Column>
  <Grid.Column span={{ medium: 8 }}>Content</Grid.Column>
</Grid>

// Stack for consistent spacing
<Stack direction="vertical" gap="normal" padding="spacious">
  <div>Item 1</div>
  <div>Item 2</div>
</Stack>

// Box for padding, margin, background, and borders
<Box 
  paddingBlockStart={64} 
  paddingBlockEnd={64}
  backgroundColor="subtle"
  borderRadius="medium"
>
  <Heading>Content with spacing</Heading>
</Box>
```

**Box Component**: Use Box instead of divs for layout with proper spacing:
- Padding props: `padding`, `paddingBlockStart`, `paddingBlockEnd`, `paddingInlineStart`, `paddingInlineEnd`
- Margin props: `margin`, `marginBlockStart`, `marginBlockEnd`, `marginInlineStart`, `marginInlineEnd`
- Values: Use spacing scale (8, 16, 24, 32, 40, 48, 64, 80, 96, 128) or responsive objects
- Background: `backgroundColor="default"` or `"subtle"`
- Border: `borderColor`, `borderRadius`, `borderStyle`

#### Typography Components
```tsx
import pkg from "@primer/react-brand";
const { Heading, Text } = pkg;

<Heading as="h1" size="1">Main Heading</Heading>
<Heading as="h2" size="3">Section Heading</Heading>
<Text size="300" weight="semibold">Body text</Text>
```

### Icons with Octicons

**ALWAYS use Octicons** from @primer/octicons-react for any icons:
```tsx
import { SearchIcon, PackageIcon, ChevronDownIcon } from "@primer/octicons-react";

// Use with Button leadingVisual/trailingVisual
<Button leadingVisual={<SearchIcon />}>Search</Button>
```

Find icons at: https://primer.style/octicons/

### Styling Approach

1. **Prefer Primer components** over custom HTML/CSS
2. **Use Box component** for layout spacing (padding, margin) instead of wrapper divs
3. **Use className prop** on Primer components for custom styling with external CSS
4. **Use inline styles sparingly** - only when Box and className aren't suitable
5. Use standard CSS values (px, colors like #0969da) rather than CSS variables
6. Follow GitHub's color palette:
   - Primary blue: #0969da
   - Success green: #1f883d
   - Backgrounds: #ffffff (white), #f6f8fa (light gray)
   - Borders: #d0d7de
   - Text: #24292f (primary), #57606a (secondary)

### Common Patterns

**Page Layout with Box:**
```tsx
import pkg from "@primer/react-brand";
const { Box } = pkg;

<Box backgroundColor="subtle" style={{ minHeight: "100vh" }}>
  <Box 
    as="header" 
    backgroundColor="default" 
    borderColor="default"
    borderStyle="solid-bottom"
    paddingBlockStart={16} 
    paddingBlockEnd={16}
  >
    {/* Navigation */}
  </Box>
  <Box 
    as="main" 
    style={{ maxWidth: "1280px", margin: "0 auto" }}
    paddingBlockStart={48}
    paddingBlockEnd={48}
    paddingInlineStart={24}
    paddingInlineEnd={24}
  >
    {/* Content */}
  </Box>
  <Box 
    as="footer"
    borderColor="default"
    borderStyle="solid-top"
    paddingBlockStart={32}
    paddingBlockEnd={32}
  >
    {/* Footer */}
  </Box>
</Box>
```

**Card Component with Box:**
```tsx
<Box
  backgroundColor="default"
  borderColor="default"
  borderStyle="solid"
  borderRadius="medium"
  padding={24}
>
  {/* Card content */}
</Box>
```

**Styling Icons:**
```tsx
// ✅ OPTION 1: Use fill prop directly on icon
<PackageIcon size={24} fill="#0969da" />

// ✅ OPTION 2: Use className prop
<PackageIcon size={24} className="custom-icon" />

// ✅ OPTION 3: Wrap in div (inherits currentColor)
<div style={{ color: "#0969da" }}>
  <PackageIcon size={24} />
</div>

// Octicons support: size, fill, className, style, aria-label, and all SVG props
```

### Component Reference

For complete component documentation and APIs:
- Components overview: https://primer.style/brand/components/
- Button: https://primer.style/brand/components/Button/react/
- Hero: https://primer.style/brand/components/Hero/react/
- Typography: https://primer.style/brand/typography/
- Grid/Layout: https://primer.style/brand/layout/

### Accessibility

Always follow accessibility guidelines: https://primer.style/accessibility/
- Use semantic HTML
- Proper heading hierarchy
- Alt text for images
- Focus states for interactive elements
- ARIA labels when needed

### Testing Requirements

Always build and test changes before completing your work:
1. Run `npm run build` to check for TypeScript errors
2. Test the application in development mode (`npm run dev`)
3. Verify all routes and navigation work correctly
4. Check responsive behavior and accessibility
5. Never hand back changes that fail to build or run

### Common Issues & Solutions

**Problem: "Named export not found" error or CommonJS module warning**
```tsx
// ❌ WRONG - Named imports fail with CommonJS in dev/SSR
import { Button } from '@primer/react-brand';

// ❌ WRONG - Namespace imports may be undefined
import * as PrimerBrand from "@primer/react-brand";

// ✅ CORRECT - Use default import with destructuring
import pkg from "@primer/react-brand";
const { Button } = pkg;
```

**Problem: Need custom spacing on Primer components**
```tsx
// ❌ AVOID - Wrapper divs add unnecessary DOM nesting
<div style={{ padding: "80px 24px" }}>
  <Hero>...</Hero>
</div>

// ✅ BETTER - Use className with CSS file
<Hero className="hero-spacing">...</Hero>

// ✅ BEST - Use Box component for layout
<Box paddingBlockStart={80} paddingBlockEnd={80} paddingInlineStart={24} paddingInlineEnd={24}>
  <Hero>...</Hero>
</Box>
```

**Problem: Octicon color not working**
```tsx
// ✅ CORRECT - Use fill prop for icon color
<PackageIcon fill="#0969da" />

// ✅ ALSO CORRECT - Set color on parent (icon inherits via currentColor)
<div style={{ color: "#0969da" }}>
  <PackageIcon />
</div>

// ✅ ALSO CORRECT - Use className
<PackageIcon className="text-blue" />
```

**Problem: Routes not working (404 errors)**
- Always add new routes to `app/routes.ts` using the `route()` function
```tsx
import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("products", "routes/products.tsx"),
] satisfies RouteConfig;
```






