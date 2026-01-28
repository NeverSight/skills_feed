---
name: component-library
description: Build production-grade, accessible, and tested component libraries with Storybook, Chromatic, and design tokens
sasmp_version: "2.0.0"
bonded_agent: 03-component-architecture
bond_type: PRIMARY_BOND
input_validation:
  required_packages:
    - "storybook": ">=7.0.0"
    - "@storybook/react": ">=7.0.0"
output_format:
  code_examples: tsx
  test_template: jest
  storybook_template: csf3
error_handling:
  patterns:
    - prop_validation
    - error_boundary
    - fallback_component
observability:
  logging: storybook_console
  metrics: ["component_coverage", "a11y_score"]
---

# Component Library Building Skill

## Overview
Learn to build reusable, accessible, and well-documented component libraries for React applications using modern design patterns and tools.

## Learning Objectives
- Design reusable component APIs
- Implement accessible components (WCAG 2.1)
- Create component variants and compositions
- Build documentation with Storybook
- Publish and maintain npm packages

## Component Design Principles

### 1. Flexible and Composable
```jsx
// Good: Flexible API
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>

// Bad: Rigid API
<Card title="Title" content="Content" action="Action" />
```

### 2. Accessible by Default
```jsx
function Button({ children, onClick, disabled, ...props }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
```

## Essential Components

### Button Component
```jsx
const Button = forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  leftIcon,
  rightIcon,
  ...props
}, ref) => {
  return (
    <button
      ref={ref}
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {leftIcon && <span className="btn-icon-left">{leftIcon}</span>}
      {loading ? <Spinner size="sm" /> : children}
      {rightIcon && <span className="btn-icon-right">{rightIcon}</span>}
    </button>
  );
});

Button.displayName = 'Button';
```

### Input Component
```jsx
const Input = forwardRef(({
  label,
  error,
  helper,
  required,
  ...props
}, ref) => {
  const id = useId();

  return (
    <div className="input-wrapper">
      {label && (
        <label htmlFor={id}>
          {label}
          {required && <span aria-label="required">*</span>}
        </label>
      )}
      <input
        ref={ref}
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : helper ? `${id}-helper` : undefined}
        {...props}
      />
      {helper && <span id={`${id}-helper`} className="input-helper">{helper}</span>}
      {error && <span id={`${id}-error`} className="input-error" role="alert">{error}</span>}
    </div>
  );
});
```

### Modal Component
```jsx
function Modal({ isOpen, onClose, title, children }) {
  const modalRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      const previousActiveElement = document.activeElement;
      modalRef.current?.focus();

      return () => {
        previousActiveElement?.focus();
      };
    }
  }, [isOpen]);

  useOnClickOutside(modalRef, onClose);

  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div ref={modalRef} className="modal" tabIndex={-1}>
        <div className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button onClick={onClose} aria-label="Close modal">×</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>,
    document.body
  );
}
```

### Dropdown Component
```jsx
function Dropdown({ trigger, children }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useOnClickOutside(dropdownRef, () => setIsOpen(false));

  return (
    <div ref={dropdownRef} className="dropdown">
      <div onClick={() => setIsOpen(!isOpen)} role="button" aria-expanded={isOpen}>
        {trigger}
      </div>
      {isOpen && (
        <div className="dropdown-menu" role="menu">
          {children}
        </div>
      )}
    </div>
  );
}

function DropdownItem({ onClick, children }) {
  return (
    <div className="dropdown-item" role="menuitem" onClick={onClick} tabIndex={0}>
      {children}
    </div>
  );
}

Dropdown.Item = DropdownItem;
```

## Compound Components Pattern

### Tabs Component
```jsx
const TabsContext = createContext();

function Tabs({ children, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }) {
  return <div className="tab-list" role="tablist">{children}</div>;
}

function Tab({ id, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);

  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={activeTab === id ? 'active' : ''}
    >
      {children}
    </button>
  );
}

function TabPanels({ children }) {
  return <div className="tab-panels">{children}</div>;
}

function TabPanel({ id, children }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== id) return null;

  return <div role="tabpanel">{children}</div>;
}

Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panels = TabPanels;
Tabs.Panel = TabPanel;
```

## Storybook Integration

### Installation
```bash
npx storybook@latest init
```

### Button Stories
```jsx
// Button.stories.jsx
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger']
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg']
    }
  }
};

export const Primary = {
  args: {
    variant: 'primary',
    children: 'Button'
  }
};

export const WithIcons = {
  args: {
    leftIcon: <Icon name="star" />,
    children: 'Button'
  }
};

export const Loading = {
  args: {
    loading: true,
    children: 'Loading...'
  }
};
```

## TypeScript Support

```typescript
// Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button ref={ref} className={`btn btn-${variant} btn-${size}`} {...props}>
        {children}
      </button>
    );
  }
);
```

## Publishing to npm

### package.json Setup
```json
{
  "name": "@yourname/component-library",
  "version": "1.0.0",
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

## Practice Projects

1. Build a complete Button component with variants
2. Create accessible Form components (Input, Select, Checkbox)
3. Implement Modal with focus trap
4. Build Dropdown with keyboard navigation
5. Create Tabs compound component
6. Implement Toast notification system
7. Build Tooltip component

## Resources

- [Radix UI](https://www.radix-ui.com) - Headless UI components
- [Headless UI](https://headlessui.com) - Unstyled components
- [Storybook](https://storybook.js.org) - Component documentation
- [React Aria](https://react-spectrum.adobe.com/react-aria/) - Accessibility

---

**Difficulty**: Intermediate to Advanced
**Estimated Time**: 3-4 weeks
**Prerequisites**: React Fundamentals, Component Architecture
