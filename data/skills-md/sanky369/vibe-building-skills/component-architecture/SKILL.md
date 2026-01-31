---
name: component-architecture
description: Design and build reusable, well-documented components. Master component composition, prop design, variant systems, state management, and documentation. Create a scalable component library that enables consistency and speeds up development. Works with React, TypeScript, and Tailwind CSS.
---

# Component Architecture

## Overview

Components are the building blocks of modern interfaces. A well-designed component system enables consistency, speeds up development, and makes maintenance easier. This skill teaches you to think about components systematically: designing for reusability, managing complexity, documenting thoroughly, and building a library that your team loves to use.

## Core Methodology: Atomic Design

Atomic Design is a methodology for creating design systems by breaking down interfaces into fundamental building blocks.

### The Five Levels

**1. Atoms**
The smallest, most basic components. They can't be broken down further without losing their meaning.

Examples: Button, Input, Label, Icon, Badge, Spinner

**Characteristics:**
- Single responsibility
- Highly reusable
- No dependencies on other components (except styling)
- Fully self-contained

**Example Atom: Button**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children,
}) => {
  return (
    <button
      className={`button button--${variant} button--${size}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading && <Spinner size="sm" />}
      {children}
    </button>
  );
};
```

**2. Molecules**
Groups of atoms bonded together to form relatively simple functional units.

Examples: Form Input (Label + Input + Error Message), Search Bar (Icon + Input + Button), Card Header (Avatar + Name + Date)

**Characteristics:**
- Composed of atoms
- Serve a specific purpose
- Reusable across the product
- Have a clear interface (props)

**Example Molecule: Form Input**
```typescript
interface FormInputProps {
  label: string;
  placeholder?: string;
  error?: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export const FormInput: React.FC<FormInputProps> = ({
  label,
  placeholder,
  error,
  value,
  onChange,
  disabled,
}) => {
  return (
    <div className="form-input">
      <Label>{label}</Label>
      <Input
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        aria-invalid={!!error}
      />
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};
```

**3. Organisms**
Relatively complex UI sections composed of groups of molecules and/or atoms and/or other organisms.

Examples: Navigation Bar, Form, Card, Modal, Sidebar

**Characteristics:**
- Composed of molecules and atoms
- Serve a specific business purpose
- More complex interfaces
- Often have state management

**Example Organism: Card**
```typescript
interface CardProps {
  title: string;
  description?: string;
  image?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  children?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  image,
  action,
  children,
}) => {
  return (
    <div className="card">
      {image && <img src={image} alt={title} className="card-image" />}
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        {description && <p className="card-description">{description}</p>}
        {children}
        {action && (
          <Button onClick={action.onClick} variant="secondary">
            {action.label}
          </Button>
        )}
      </div>
    </div>
  );
};
```

**4. Templates**
Page-level objects that place components into a layout and articulate the design's underlying content structure.

Examples: Blog Post Template, Product Page Template, Dashboard Template

**Characteristics:**
- Composed of organisms, molecules, and atoms
- Define page structure and layout
- Show how components work together
- Not typically reusable (specific to page type)

**Example Template: Blog Post**
```typescript
export const BlogPostTemplate: React.FC<BlogPostTemplateProps> = ({
  title,
  author,
  date,
  image,
  content,
  relatedPosts,
}) => {
  return (
    <div className="blog-post-template">
      <Header />
      <article className="blog-post">
        <div className="blog-post-hero">
          <img src={image} alt={title} />
        </div>
        <div className="blog-post-content">
          <h1>{title}</h1>
          <div className="blog-post-meta">
            <Avatar src={author.avatar} alt={author.name} />
            <span>{author.name}</span>
            <span>{formatDate(date)}</span>
          </div>
          <div className="blog-post-body">{content}</div>
        </div>
      </article>
      <section className="related-posts">
        <h2>Related Posts</h2>
        <div className="related-posts-grid">
          {relatedPosts.map((post) => (
            <Card key={post.id} {...post} />
          ))}
        </div>
      </section>
      <Footer />
    </div>
  );
};
```

**5. Pages**
Specific instances of templates that show what the UI looks like with real data.

Examples: Homepage, Product Page, User Profile, Dashboard

**Characteristics:**
- Instances of templates with real data
- Used for testing and demonstration
- Show how components behave with actual content
- Help identify edge cases and issues

## Component Design Principles

### Principle 1: Single Responsibility

Each component should have one clear purpose. If a component does too much, break it down.

**Bad:**
```typescript
// Does too much: rendering, data fetching, form handling, validation
const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    fetchUser().then(setUser);
  }, []);
  
  const handleSubmit = () => {
    // validation logic
    // submission logic
  };
  
  return (
    // complex JSX
  );
};
```

**Good:**
```typescript
// UserProfile: Orchestrates the page
const UserProfile = () => {
  const { user } = useUser();
  return (
    <>
      <UserHeader user={user} />
      <UserEditForm user={user} />
      <UserActivity user={user} />
    </>
  );
};

// UserHeader: Displays user info
const UserHeader = ({ user }) => (
  <div className="user-header">
    <Avatar src={user.avatar} />
    <h1>{user.name}</h1>
  </div>
);

// UserEditForm: Handles form state and submission
const UserEditForm = ({ user }) => {
  // form logic
};

// UserActivity: Displays user activity
const UserActivity = ({ user }) => {
  // activity logic
};
```

### Principle 2: Composition Over Inheritance

Build complex components by composing simpler ones, not by inheritance.

**Bad:**
```typescript
// Inheritance approach (avoid)
class Button extends React.Component {}
class PrimaryButton extends Button {}
class LargeButton extends Button {}
class LargePrimaryButton extends Button {}
```

**Good:**
```typescript
// Composition approach (prefer)
const Button = ({ variant = 'primary', size = 'md', ...props }) => (
  <button className={`button button--${variant} button--${size}`} {...props} />
);

// Use composition to create variants
const PrimaryButton = (props) => <Button variant="primary" {...props} />;
const LargeButton = (props) => <Button size="lg" {...props} />;
const LargePrimaryButton = (props) => <Button variant="primary" size="lg" {...props} />;
```

### Principle 3: Props Interface Design

Design component props carefully. Props should be:
- **Intuitive** — Props should be self-explanatory
- **Flexible** — Props should support common use cases
- **Constrained** — Props should prevent invalid states
- **Documented** — Props should be clearly documented

**Example: Well-Designed Props**
```typescript
interface ButtonProps {
  // Variant and size are constrained to valid options
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  
  // Boolean props are explicit
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  
  // Callbacks are clearly named
  onClick?: () => void;
  onHover?: () => void;
  
  // Content is flexible
  children: React.ReactNode;
  icon?: React.ReactNode;
  
  // HTML attributes can be passed through
  className?: string;
  'aria-label'?: string;
}
```

### Principle 4: Controlled vs. Uncontrolled

Be explicit about whether a component is controlled (parent manages state) or uncontrolled (component manages state).

**Controlled Component:**
```typescript
const ControlledInput = ({ value, onChange }) => (
  <input value={value} onChange={(e) => onChange(e.target.value)} />
);

// Parent manages state
const Parent = () => {
  const [value, setValue] = useState('');
  return <ControlledInput value={value} onChange={setValue} />;
};
```

**Uncontrolled Component:**
```typescript
const UncontrolledInput = ({ defaultValue, onSubmit }) => {
  const inputRef = useRef(null);
  
  return (
    <>
      <input ref={inputRef} defaultValue={defaultValue} />
      <button onClick={() => onSubmit(inputRef.current.value)}>Submit</button>
    </>
  );
};

// Parent doesn't manage state
const Parent = () => {
  return <UncontrolledInput onSubmit={(value) => console.log(value)} />;
};
```

## Component Variants

### Defining Variants

Variants are different versions of a component for different contexts. Define them clearly:

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  state?: 'default' | 'hover' | 'active' | 'disabled' | 'loading';
}

// Variants matrix
const Button = ({ variant = 'primary', size = 'md', state = 'default', ...props }) => {
  const variantClass = `button--${variant}`;
  const sizeClass = `button--${size}`;
  const stateClass = `button--${state}`;
  
  return (
    <button className={`button ${variantClass} ${sizeClass} ${stateClass}`} {...props} />
  );
};

// Usage
<Button variant="primary" size="md" state="default">Primary</Button>
<Button variant="secondary" size="lg" state="hover">Secondary Large</Button>
<Button variant="danger" size="sm" state="disabled">Delete</Button>
```

### Variant Documentation

Document all variants with examples:

```markdown
# Button Component

## Variants

### Variant: primary
- Default button style
- Used for primary actions
- Example: "Save", "Submit", "Create"

### Variant: secondary
- Secondary button style
- Used for secondary actions
- Example: "Cancel", "Back", "Skip"

### Variant: ghost
- Minimal button style
- Used for tertiary actions
- Example: "Learn More", "View Details"

### Variant: danger
- Danger button style
- Used for destructive actions
- Example: "Delete", "Remove", "Discard"

## Sizes

### Size: sm
- 32px height
- 12px font size
- Used in compact spaces

### Size: md
- 40px height
- 14px font size
- Default size

### Size: lg
- 48px height
- 16px font size
- Used for prominent actions

## States

### State: default
- Normal appearance

### State: hover
- Slightly darker or lighter
- Indicates interactivity

### State: active
- Pressed appearance
- Indicates the button is being clicked

### State: disabled
- Grayed out
- Cursor is not-allowed
- Not clickable

### State: loading
- Shows spinner
- Indicates action in progress
- Not clickable
```

## Component Documentation

### What to Document

1. **Purpose** — What does this component do?
2. **Props** — What props does it accept?
3. **Variants** — What variants are available?
4. **States** — What states can it be in?
5. **Examples** — How do you use it?
6. **Accessibility** — What accessibility features does it have?
7. **Edge Cases** — What edge cases should you be aware of?

### Documentation Template

```markdown
# Component Name

## Purpose
Brief description of what this component does and when to use it.

## Props

| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `variant` | 'primary' \| 'secondary' | 'primary' | Visual variant |
| `size` | 'sm' \| 'md' \| 'lg' | 'md' | Component size |
| `disabled` | boolean | false | Disable the component |
| `children` | ReactNode | - | Component content |

## Variants

### Primary
Used for primary actions.
```jsx
<Button variant="primary">Primary Action</Button>
```

### Secondary
Used for secondary actions.
```jsx
<Button variant="secondary">Secondary Action</Button>
```

## States

### Default
Normal appearance.

### Disabled
Grayed out, not clickable.
```jsx
<Button disabled>Disabled</Button>
```

### Loading
Shows spinner, not clickable.
```jsx
<Button loading>Loading...</Button>
```

## Accessibility

- Keyboard accessible (Enter, Space to activate)
- Screen reader friendly (announces button text)
- Focus visible (outline on focus)
- Aria-label support for icon-only buttons

## Examples

### Basic Button
```jsx
<Button onClick={() => alert('Clicked!')}>Click Me</Button>
```

### With Icon
```jsx
<Button icon={<SaveIcon />}>Save</Button>
```

### Full Width
```jsx
<Button fullWidth>Full Width Button</Button>
```

## Edge Cases

- Icon-only buttons must have aria-label
- Disabled buttons should not be clickable
- Loading state should show spinner
- Very long text should wrap or truncate
```

## How to Use This Skill with Claude Code

### Audit Your Components

```
"I'm using the component-architecture skill. Can you audit my components?
- Identify components that violate single responsibility
- Suggest component composition improvements
- Check component documentation completeness
- Identify reusable patterns I'm missing
- Suggest component library structure"
```

### Design a Component System

```
"Can you help me design a component system?
- Define atomic components (atoms, molecules, organisms)
- Create component architecture
- Design component props interfaces
- Define variants for each component
- Create component documentation"
```

### Refactor Components

```
"Can you help me refactor my components?
- Break down complex components
- Improve component composition
- Simplify prop interfaces
- Add missing variants
- Improve documentation"
```

### Generate Component Library

```
"Can you generate a component library?
- Create all atomic components (Button, Input, Label, etc.)
- Create molecules (FormInput, SearchBar, etc.)
- Create organisms (Card, Modal, etc.)
- Include TypeScript types
- Include Tailwind CSS styling
- Include comprehensive documentation"
```

## Design Critique: Evaluating Your Components

Claude Code can critique your components:

```
"Can you evaluate my component architecture?
- Are my components following single responsibility?
- Is my component composition good?
- Are my prop interfaces well-designed?
- Is my documentation comprehensive?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

- **design-foundation** — Component tokens and styling
- **layout-system** — Component layout patterns
- **typography-system** — Component typography
- **color-system** — Component colors
- **accessibility-excellence** — Component accessibility
- **interaction-design** — Component interactions

## Key Principles

**1. Single Responsibility**
Each component should have one clear purpose.

**2. Composition Over Inheritance**
Build complex components by composing simpler ones.

**3. Props Interface Design**
Design props carefully for clarity and flexibility.

**4. Variants Enable Reusability**
Well-designed variants make components reusable across contexts.

**5. Documentation Enables Adoption**
Comprehensive documentation helps your team use components effectively.

## Checklist: Is Your Component Architecture Ready?

- [ ] Components follow single responsibility principle
- [ ] Components are composed from simpler components
- [ ] Props interfaces are well-designed and documented
- [ ] All variants are defined and documented
- [ ] All states are defined and documented
- [ ] Components are accessible (keyboard, screen reader, focus)
- [ ] Components have comprehensive documentation
- [ ] Component library is organized (atoms, molecules, organisms)
- [ ] Components are reusable across the product
- [ ] Components are tested (unit tests, visual tests)

A well-designed component architecture is the foundation of a scalable, maintainable product.
