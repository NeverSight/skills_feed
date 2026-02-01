---
name: atomic-design
description: Atomic Design methodology for React component architecture. Use for structuring component libraries, organizing UI hierarchies, and creating scalable design systems. Triggers on requests for component organization, design system structure, UI hierarchy, or questions about Atoms/Molecules/Organisms/Templates/Pages.
---

# Atomic Design Patterns

## Component Hierarchy

```
src/components/
├── atoms/           # Smallest building blocks
├── molecules/       # Simple component groups
├── organisms/       # Complex UI sections
├── templates/       # Page layouts
└── pages/           # Complete views
```

## Level Definitions

### Atoms
Indivisible UI elements. No dependencies on other components.

```tsx
// atoms/Button/Button.tsx
export const Button: FC<ButtonProps> = ({ children, variant, size, ...props }) => (
  <button className={cn('btn', `btn--${variant}`, `btn--${size}`)} {...props}>
    {children}
  </button>
);

// atoms/Input/Input.tsx
export const Input: FC<InputProps> = ({ label, error, ...props }) => (
  <div className="input-wrapper">
    {label && <label>{label}</label>}
    <input className={cn('input', error && 'input--error')} {...props} />
    {error && <span className="input-error">{error}</span>}
  </div>
);

// atoms/Icon/Icon.tsx
export const Icon: FC<IconProps> = ({ name, size = 24 }) => (
  <svg className="icon" width={size} height={size}>
    <use href={`#icon-${name}`} />
  </svg>
);
```

**Examples:** Button, Input, Label, Icon, Avatar, Badge, Spinner, Divider

### Molecules
Combine atoms into functional units with single responsibility.

```tsx
// molecules/SearchField/SearchField.tsx
export const SearchField: FC<SearchFieldProps> = ({ onSearch, placeholder }) => {
  const [value, setValue] = useState('');
  
  return (
    <div className="search-field">
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
      />
      <Button variant="ghost" onClick={() => onSearch(value)}>
        <Icon name="search" />
      </Button>
    </div>
  );
};

// molecules/FormField/FormField.tsx
export const FormField: FC<FormFieldProps> = ({ label, error, children }) => (
  <div className="form-field">
    <Label>{label}</Label>
    {children}
    {error && <ErrorMessage>{error}</ErrorMessage>}
  </div>
);
```

**Examples:** SearchField, FormField, NavItem, Card, MenuItem, Toast

### Organisms
Complex, self-contained sections with business logic.

```tsx
// organisms/Header/Header.tsx
export const Header: FC<HeaderProps> = ({ user, onLogout }) => (
  <header className="header">
    <Logo />
    <Navigation />
    <SearchField onSearch={handleSearch} />
    <UserMenu user={user} onLogout={onLogout} />
  </header>
);

// organisms/ProductCard/ProductCard.tsx
export const ProductCard: FC<ProductCardProps> = ({ product, onAddToCart }) => (
  <article className="product-card">
    <Image src={product.image} alt={product.name} />
    <div className="product-card__content">
      <Heading level={3}>{product.name}</Heading>
      <Price value={product.price} />
      <Rating value={product.rating} />
      <Button onClick={() => onAddToCart(product)}>Add to Cart</Button>
    </div>
  </article>
);
```

**Examples:** Header, Footer, ProductCard, CommentSection, Sidebar, DataTable

### Templates
Page-level layouts without real content. Define structure only.

```tsx
// templates/DashboardLayout/DashboardLayout.tsx
export const DashboardLayout: FC<DashboardLayoutProps> = ({ 
  sidebar, 
  header, 
  content 
}) => (
  <div className="dashboard-layout">
    <aside className="dashboard-layout__sidebar">{sidebar}</aside>
    <div className="dashboard-layout__main">
      <header className="dashboard-layout__header">{header}</header>
      <main className="dashboard-layout__content">{content}</main>
    </div>
  </div>
);
```

### Pages
Templates filled with real data. Connect to state/APIs.

```tsx
// pages/DashboardPage/DashboardPage.tsx
export const DashboardPage: FC = () => {
  const { data: stats } = useStats();
  const { user } = useAuth();

  return (
    <DashboardLayout
      sidebar={<DashboardSidebar />}
      header={<Header user={user} />}
      content={<StatsGrid stats={stats} />}
    />
  );
};
```

## Decision Guide

| Question | Atom | Molecule | Organism |
|----------|------|----------|----------|
| Has child components? | No | Yes | Yes |
| Has business logic? | No | Minimal | Yes |
| Reusable across projects? | Yes | Usually | Sometimes |
| Contains API calls? | No | No | Possible |

## Naming Conventions

- **Atoms:** Single noun (`Button`, `Input`, `Icon`)
- **Molecules:** Descriptive compound (`SearchField`, `NavItem`)
- **Organisms:** Domain-specific (`ProductCard`, `CheckoutForm`)
- **Templates:** Layout suffix (`DashboardLayout`, `AuthLayout`)
- **Pages:** Page suffix (`HomePage`, `ProductPage`)

## Export Pattern

```tsx
// components/atoms/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Icon } from './Icon';

// components/index.ts
export * from './atoms';
export * from './molecules';
export * from './organisms';
```
