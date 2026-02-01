---
name: pix-storybook
description: Autonomous pixel-perfect Stencil component implementation using Figma MCP, Storybook, and Playwright MCP for visual testing and fixing.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, skill, mcp1_browser_*, mcp2_sequentialthinking]
---

# /pix-storybook: Pixel-Perfect Stencil Components with Storybook

> **Note**: This skill requires Figma MCP, Playwright MCP, and Storybook. It leverages existing Stencil skills for component creation.

## Phase 0: Environment Setup & Discovery

### 1. Project Analysis
```bash
# Check for existing Storybook setup
ls -la .storybook/
cat package.json | grep storybook
```

If Storybook is not installed:
```bash
npx storybook@latest init --type web_components
```

### 2. Verify MCP Connections
1. **Figma MCP**: Check authentication with `whoami`
2. **Playwright MCP**: Verify browser control with `mcp1_browser_install`
3. **Storybook Port**: Default 6006, check `.storybook/main.js` for custom port

### 3. Start Storybook
```bash
# Check if already running
lsof -i :6006

# If not running, start in background
npm run storybook &
```

### 4. Initialize Playwright Browser
```javascript
// Use Playwright MCP to open Storybook
mcp1_browser_navigate({ url: "http://localhost:6006" })
```

## Phase 1: Design Analysis & Component Planning

### User Input
**Ask for Figma link**: "Paste the Figma link to the component you want to build (use 'Copy link to selection')"

### Figma Data Extraction

Execute this sequence using Figma MCP tools:

1. **Component Structure**
   ```javascript
   // Get component hierarchy
   figma_get_metadata({ node_id: "<extracted_id>" })
   ```

2. **Design Context**
   ```javascript
   // Get complete design specs
   figma_get_design_context({ node_id: "<extracted_id>" })
   ```

3. **Design Tokens**
   ```javascript
   // Extract variables and tokens
   figma_get_variable_defs({ file_id: "<file_id>" })
   ```

4. **Existing Mappings**
   ```javascript
   // Check for existing code components
   figma_get_code_connect_map({ file_id: "<file_id>" })
   ```

### Component Planning with Sequential Thinking
```javascript
mcp2_sequentialthinking({
  thought: "Analyzing Figma design to plan Stencil component structure...",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
})
```

Consider:
- Atomic level (atom, molecule, organism, template)
- Required props and slots
- Token mappings
- Existing components to reuse

## Phase 2: Stencil Component Implementation

### 1. Invoke Stencil Skills

Use the appropriate skill based on component type:

```javascript
// For new component creation
skill({ 
  SkillName: "stenciljs-component-development" 
})

// For design system components
skill({ 
  SkillName: "stencil-atomic-design-system" 
})
```

### 2. Component Structure

Create component following the cor- prefix pattern:

```typescript
// src/components/cor-[component-name]/cor-[component-name].tsx
import { Component, Prop, h, Host } from '@stencil/core';

@Component({
  tag: 'cor-[component-name]',
  styleUrl: 'cor-[component-name].css',
  shadow: true,
})
export class Cor[ComponentName] {
  // Props based on Figma analysis
  @Prop() variant: 'primary' | 'secondary' = 'primary';
  @Prop() size: 'small' | 'medium' | 'large' = 'medium';
  
  render() {
    return (
      <Host>
        {/* Slot-based composition */}
        <slot name="icon-left"></slot>
        <slot></slot>
        <slot name="icon-right"></slot>
      </Host>
    );
  }
}
```

### 3. Token Integration

Map Figma tokens to CSS variables:

```css
/* cor-[component-name].css */
:host {
  /* Map to generated token variables */
  --component-padding: var(--spacing-md);
  --component-radius: var(--radius-md);
  --component-font-size: var(--font-size-md);
  --component-font-weight: var(--font-weight-semi-bold);
  --component-color: var(--color-primary-text-default);
  --component-background: var(--color-primary-background-default);
}
```

## Phase 3: Storybook Story Creation

### 1. Invoke Story Writing Skill

```javascript
skill({ 
  SkillName: "storybook-story-writing" 
})
```

### 2. Create Component Story

```typescript
// src/components/cor-[component-name]/cor-[component-name].stories.ts
import { html } from 'lit';
import type { Meta, StoryObj } from '@storybook/web-components';

const meta: Meta = {
  title: '[AtomicLevel]/Cor[ComponentName]',
  component: 'cor-[component-name]',
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Pixel-perfect implementation from Figma design',
      },
    },
  },
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary'],
    },
    size: {
      control: { type: 'select' },
      options: ['small', 'medium', 'large'],
    },
  },
};

export default meta;
type Story = StoryObj;

// Default story matching Figma design
export const Default: Story = {
  args: {
    variant: 'primary',
    size: 'medium',
  },
  render: (args) => html`
    <cor-[component-name] 
      variant="${args.variant}"
      size="${args.size}"
    >
      Content from Figma
    </cor-[component-name]>
  `,
};

// All states for visual comparison
export const AllStates: Story = {
  render: () => html`
    <div style="display: flex; flex-direction: column; gap: 16px;">
      <cor-[component-name] variant="primary">Primary</cor-[component-name]>
      <cor-[component-name] variant="secondary">Secondary</cor-[component-name]>
      <cor-[component-name] size="small">Small</cor-[component-name]>
      <cor-[component-name] size="large">Large</cor-[component-name]>
    </div>
  `,
};
```

## Phase 4: Visual Testing with Playwright MCP

### 1. Navigate to Story

```javascript
// Navigate to the specific story
mcp1_browser_navigate({ 
  url: "http://localhost:6006/iframe.html?id=[atomic-level]-cor[component-name]--default&viewMode=story" 
})

// Wait for component to render
mcp1_browser_wait_for({ time: 2 })
```

### 2. Take Screenshots

```javascript
// Screenshot Storybook component
mcp1_browser_take_screenshot({ 
  filename: "storybook-component.png",
  fullPage: false
})

// Get Figma reference screenshot
figma_get_screenshot({ 
  node_id: "<node_id>",
  scale: 2
})
```

### 3. Visual Comparison Loop

```javascript
mcp2_sequentialthinking({
  thought: "Comparing Storybook component with Figma design...",
  thoughtNumber: 1,
  totalThoughts: 3,
  nextThoughtNeeded: true
})
```

Check for discrepancies:
- Font weight and size
- Colors and opacity
- Spacing and padding
- Border radius
- Icon size and color
- Shadow effects

### 4. Interactive State Testing

```javascript
// Test hover states
mcp1_browser_hover({ 
  ref: "button",
  element: "component button"
})
mcp1_browser_take_screenshot({ 
  filename: "hover-state.png" 
})

// Test focus states
mcp1_browser_click({ 
  ref: "button",
  element: "component button"
})
mcp1_browser_take_screenshot({ 
  filename: "focus-state.png" 
})

// Test disabled states (if applicable)
```

## Phase 5: Iterative Refinement

### 1. Identify Issues

Use Playwright MCP to inspect elements:

```javascript
// Get computed styles
mcp1_browser_evaluate({
  function: "(element) => window.getComputedStyle(element)",
  ref: "component-element"
})
```

### 2. Fix Discrepancies

For each issue found:

1. **Explain the problem**: "Font weight is 400 but should be 600 according to Figma"

2. **Update the code**:
   ```css
   /* Fix in component CSS */
   --component-font-weight: var(--font-weight-semi-bold); /* 600 */
   ```

3. **Rebuild and refresh**:
   ```javascript
   // Refresh Storybook
   mcp1_browser_navigate_back()
   mcp1_browser_navigate({ url: "http://localhost:6006/..." })
   ```

4. **Re-test**: Take new screenshot and compare

### 3. Success Criteria

Component is complete when:
- All visual properties match Figma exactly
- Interactive states work correctly
- Component renders properly in all story variations
- No console errors in Storybook

## Phase 6: Final Validation

### 1. Create Comparison Story

Create a special story for side-by-side comparison:

```typescript
export const PixelPerfectComparison: Story = {
  render: () => html`
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">
      <div>
        <h3>Storybook Component</h3>
        <cor-[component-name]>Content</cor-[component-name]>
      </div>
      <div>
        <h3>Figma Reference</h3>
        <img src="/figma-reference.png" alt="Figma design" />
      </div>
    </div>
  `,
};
```

### 2. Documentation

Update component readme with:
- Figma link reference
- Token mappings used
- Any deviations and rationale
- Usage examples

### 3. User Review

**Ask for feedback**:
- "Component is ready in Storybook. Please review at http://localhost:6006"
- "Are you satisfied with the implementation?"
- "Any specific areas need adjustment?"

## Workflow Summary

1. **Setup**: Start Storybook, initialize Playwright browser
2. **Extract**: Get all design data from Figma MCP
3. **Plan**: Use sequential thinking to plan component structure
4. **Implement**: Create Stencil component using appropriate skills
5. **Story**: Write Storybook stories for all states
6. **Test**: Use Playwright MCP for visual comparison
7. **Refine**: Fix discrepancies iteratively
8. **Validate**: Final review with user

## Key Advantages

- **Isolated Testing**: Storybook provides clean component isolation
- **State Management**: Easy to test all component states
- **Visual Regression**: Stories serve as visual regression tests
- **Documentation**: Stories document component usage
- **Collaboration**: Shareable Storybook URL for team review
- **Automation**: Playwright MCP enables automated visual testing

## Example Usage

```
/pix-storybook
> Starting Storybook and preparing environment...
> Paste Figma link: https://figma.com/design/abc123/MyApp?node-id=42-100
> Analyzing design... Creating cor-button component...
> Writing Storybook stories...
> Testing visual accuracy with Playwright...
> Found 2px padding difference, fixing...
> Component ready for review at http://localhost:6006/?path=/story/atoms-corbutton--default
```
