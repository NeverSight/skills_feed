---
name: accessibility-audit
description: "Load PROACTIVELY when task involves accessibility compliance or inclusive design. Use when user says \"check accessibility\", \"audit for WCAG\", \"fix screen reader issues\", \"add keyboard navigation\", or \"check color contrast\". Covers WCAG 2.1 AA compliance across semantic HTML, ARIA patterns, keyboard navigation, screen reader support, color contrast ratios, form accessibility, media alternatives, and focus management. Produces structured audit reports with severity ratings."
metadata:
  version: "1.0.0"
  category: quality
  tags: [accessibility, a11y, wcag, aria, semantic-html, keyboard-navigation, screen-reader]
---

## Resources
```
scripts/
  validate-accessibility-audit.sh
references/
  accessibility-patterns.md
```

# Accessibility Audit

This skill guides you through performing comprehensive accessibility audits to ensure WCAG 2.1 AA compliance. Use this when validating applications for inclusive design, preparing for accessibility reviews, or remediating accessibility issues.

## When to Use This Skill

- Conducting pre-launch accessibility compliance reviews
- Responding to accessibility complaints or legal requirements
- Performing periodic accessibility audits on existing applications
- Validating accessibility after major UI refactors
- Preparing for WCAG 2.1 AA certification
- Onboarding teams to accessibility best practices

## Audit Methodology

A systematic accessibility audit follows these phases:

### Phase 1: Reconnaissance

**Objective:** Map components and identify accessibility-critical areas.

**Use discover to map the UI surface:**
```yaml
discover:
  queries:
    - id: interactive_components
      type: grep
      pattern: "(button|input|select|textarea|a href)"
      glob: "**/*.{tsx,jsx}"
    - id: form_components
      type: grep
      pattern: "<form|onSubmit|FormProvider"
      glob: "**/*.{tsx,jsx}"
    - id: aria_usage
      type: grep
      pattern: "aria-(label|labelledby|describedby|live|role)"
      glob: "**/*.{tsx,jsx}"
    - id: image_components
      type: grep
      pattern: "(<img|<Image|next/image)"
      glob: "**/*.{tsx,jsx}"
  verbosity: files_only
```

**Identify critical areas:**
- Forms and input fields
- Navigation menus and routing
- Modal dialogs and overlays
- Data tables and lists
- Media players (audio/video)
- Custom interactive widgets

### Phase 2: Semantic HTML Audit

**Objective:** Verify proper use of HTML5 semantic elements.

#### Check Heading Hierarchy

**Search for heading usage:**
```yaml
precision_grep:
  queries:
    - id: heading_elements
      pattern: "<h[1-6]|heading.*level"
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Common violations:**
- Skipping heading levels (h1 -> h3 without h2)
- Multiple h1 elements on a page
- Using headings for visual styling instead of structure
- Missing heading hierarchy in complex components

**Correct heading structure:**
```typescript
import { ReactNode } from 'react';

interface PageLayoutProps {
  title: string;
  children: ReactNode;
}

export function PageLayout({ title, children }: PageLayoutProps) {
  return (
    <div className="page-layout">
      {/* Single h1 per page */}
      <h1 className="text-3xl font-bold">{title}</h1>
      
      <main>
        {children}
      </main>
    </div>
  );
}

interface SectionProps {
  title: string;
  children: ReactNode;
}

export function Section({ title, children }: SectionProps) {
  return (
    <section>
      {/* h2 for main sections */}
      <h2 className="text-2xl font-semibold">{title}</h2>
      {children}
    </section>
  );
}

interface SubsectionProps {
  title: string;
  children: ReactNode;
}

export function Subsection({ title, children }: SubsectionProps) {
  return (
    <div>
      {/* h3 for subsections */}
      <h3 className="text-xl font-medium">{title}</h3>
      {children}
    </div>
  );
}
```

#### Check Landmark Regions

**Search for landmark usage:**
```yaml
precision_grep:
  queries:
    - id: landmarks
      pattern: "(<header|<main|<nav|<aside|<footer|role=\"(banner|navigation|main|complementary|contentinfo)\")"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Required landmarks:**
- `<header>` or `role="banner"` for site header
- `<nav>` or `role="navigation"` for navigation
- `<main>` or `role="main"` for primary content (exactly one per page)
- `<aside>` or `role="complementary"` for sidebars
- `<footer>` or `role="contentinfo"` for site footer

**Proper landmark structure:**
```typescript
import { ReactNode } from 'react';

interface AppLayoutProps {
  navigation: ReactNode;
  sidebar?: ReactNode;
  children: ReactNode;
}

export function AppLayout({ navigation, sidebar, children }: AppLayoutProps) {
  return (
    <div className="app-layout">
      <header className="site-header">
        <div className="logo">MyApp</div>
        {navigation}
      </header>
      
      <div className="content-container">
        {sidebar && (
          <aside className="sidebar" aria-label="Filters">
            {sidebar}
          </aside>
        )}
        
        {/* Exactly one main per page */}
        <main className="main-content">
          {children}
        </main>
      </div>
      
      <footer className="site-footer">
        <p>&copy; 2026 MyApp. All rights reserved.</p>
      </footer>
    </div>
  );
}
```

#### Check List Semantics

**Search for list patterns:**
```yaml
precision_grep:
  queries:
    - id: list_elements
      pattern: "<(ul|ol|li|dl|dt|dd)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Common violations:**
- Using `<div>` for lists instead of `<ul>` or `<ol>`
- Nesting `<li>` outside of `<ul>` or `<ol>`
- Using lists for layout instead of semantic grouping

**Semantic list usage:**
```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

interface UserListProps {
  users: User[];
}

export function UserList({ users }: UserListProps) {
  return (
    <ul className="user-list" aria-label="Team members">
      {users.map((user) => (
        <li key={user.id}>
          <span className="user-name">{user.name}</span>
          <span className="user-email">{user.email}</span>
        </li>
      ))}
    </ul>
  );
}
```

### Phase 3: ARIA Patterns Audit

**Objective:** Validate correct ARIA usage and patterns.

#### Check ARIA Roles

**Search for ARIA role usage:**
```yaml
precision_grep:
  queries:
    - id: aria_roles
      pattern: 'role="(button|link|dialog|alertdialog|menu|menuitem|tab|tabpanel|listbox|option)"'
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Common violations:**
- Redundant roles on semantic elements (e.g., `<button role="button">`)
- Using `role="button"` without keyboard handlers
- Missing required ARIA attributes for complex roles
- Using abstract roles (e.g., `role="widget"`)

**Correct ARIA button pattern:**
```typescript
import { MouseEvent, KeyboardEvent } from 'react';

interface CustomButtonProps {
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}

export function CustomButton({ onClick, disabled, children }: CustomButtonProps) {
  const handleClick = (e: MouseEvent<HTMLDivElement>) => {
    if (!disabled) {
      onClick();
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (!disabled && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      className="custom-button"
    >
      {children}
    </div>
  );
}
```

**Note:** Prefer native `<button>` element when possible. Only use `role="button"` on non-button elements when absolutely necessary.

#### Check ARIA Labels and Descriptions

**Search for labeling patterns:**
```yaml
precision_grep:
  queries:
    - id: aria_labels
      pattern: "aria-(label|labelledby|describedby)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: context
```

**Common violations:**
- Interactive elements without accessible names
- `aria-labelledby` referencing non-existent IDs
- Redundant labels (both `aria-label` and `aria-labelledby`)
- Using `aria-label` on non-interactive elements

**Correct labeling patterns:**
```typescript
import { useId } from 'react';

interface SearchFormProps {
  onSearch: (query: string) => void;
}

export function SearchForm({ onSearch }: SearchFormProps) {
  const searchId = useId();
  const hintId = useId();

  return (
    <form role="search" onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      onSearch(formData.get('query') as string);
    }}>
      <label htmlFor={searchId} className="sr-only">
        Search articles
      </label>
      <input
        id={searchId}
        type="search"
        name="query"
        placeholder="Search..."
        aria-describedby={hintId}
      />
      <p id={hintId} className="text-sm text-gray-600">
        Search by title, author, or keyword
      </p>
      <button type="submit" aria-label="Submit search">
        <SearchIcon aria-hidden="true" />
      </button>
    </form>
  );
}
```

#### Check Live Regions

**Search for live region usage:**
```yaml
precision_grep:
  queries:
    - id: live_regions
      pattern: 'aria-live="(polite|assertive|off)"|role="(status|alert)"'
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Live region best practices:**
- Use `aria-live="polite"` for non-critical updates
- Use `aria-live="assertive"` or `role="alert"` for urgent messages
- Use `role="status"` for status updates (implicitly `aria-live="polite"`)
- Ensure live region exists in DOM before content updates

**Accessible notification pattern:**
```typescript
import { ReactNode, useEffect, useState } from 'react';

interface NotificationProps {
  message: string;
  type: 'success' | 'error' | 'info';
  onDismiss: () => void;
}

export function Notification({ message, type, onDismiss }: NotificationProps) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 5000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <div
      role={type === 'error' ? 'alert' : 'status'}
      aria-live={type === 'error' ? 'assertive' : 'polite'}
      className={`notification notification-${type}`}
    >
      <p>{message}</p>
      <button onClick={onDismiss} aria-label="Dismiss notification">
        <CloseIcon aria-hidden="true" />
      </button>
    </div>
  );
}
```

### Phase 4: Keyboard Navigation Audit

**Objective:** Ensure full keyboard accessibility.

#### Check Focus Management

**Search for focus-related code:**
```yaml
precision_grep:
  queries:
    - id: focus_management
      pattern: "(focus\\(\\)|autoFocus|tabIndex|useRef.*focus)"
      glob: "**/*.{tsx,jsx,ts}"
  output:
    format: standard
```

**Common violations:**
- Missing focus indicators (`:focus` styles)
- Focus traps in modals without escape mechanism
- Interactive elements with `tabIndex="-1"` that should be reachable
- Auto-focusing elements on page load unnecessarily

**Accessible modal with focus trap:**
```typescript
import { useEffect, useRef, ReactNode } from 'react';
import { createPortal } from 'react-dom';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;

    // Save previously focused element
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus first focusable element in modal
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements && focusableElements.length > 0) {
      (focusableElements[0] as HTMLElement).focus();
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }

      // Trap focus within modal
      if (e.key === 'Tab' && focusableElements) {
        const firstElement = focusableElements[0] as HTMLElement;
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Restore focus when modal closes
      previousFocusRef.current?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 id="modal-title">{title}</h2>
        <div className="modal-body">{children}</div>
        <button onClick={onClose} className="modal-close">
          Close
        </button>
      </div>
    </div>,
    document.body
  );
}
```

#### Check Skip Links

**Search for skip link implementation:**
```yaml
precision_grep:
  queries:
    - id: skip_links
      pattern: "(skip.*main|skip.*content|skip.*navigation)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Skip link implementation:**
```typescript
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="skip-link"
    >
      Skip to main content
    </a>
  );
}

// CSS (in global styles)
// .skip-link {
//   position: absolute;
//   top: -40px;
//   left: 0;
//   background: #000;
//   color: #fff;
//   padding: 8px;
//   text-decoration: none;
//   z-index: 100;
// }
//
// .skip-link:focus {
//   top: 0;
// }
```

#### Check Keyboard Event Handlers

**Search for onClick without keyboard support:**
```yaml
precision_grep:
  queries:
    - id: onclick_handlers
      pattern: "onClick=\\{"
      glob: "**/*.{tsx,jsx}"
  output:
    format: locations
```

**Manual review:** For each `onClick` handler on a non-button/non-link element, verify:
- Element has `role="button"` or appropriate role
- Element has `tabIndex={0}` for keyboard focus
- `onKeyDown` handler responds to Enter and Space keys

**Accessible click handler pattern:**
```typescript
import { MouseEvent, KeyboardEvent } from 'react';

interface ClickableCardProps {
  title: string;
  onClick: () => void;
}

export function ClickableCard({ title, onClick }: ClickableCardProps) {
  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      className="clickable-card"
    >
      <h3>{title}</h3>
    </div>
  );
}
```

### Phase 5: Screen Reader Support Audit

**Objective:** Verify screen reader compatibility.

#### Check Visually Hidden Text

**Search for sr-only patterns:**
```yaml
precision_grep:
  queries:
    - id: sr_only
      pattern: "(sr-only|visually-hidden|screen-reader)"
      glob: "**/*.{tsx,jsx,css,scss}"
  output:
    format: files_only
```

**Visually hidden text for icons:**
```typescript
interface IconButtonProps {
  onClick: () => void;
  ariaLabel: string;
  icon: React.ReactNode;
}

export function IconButton({ onClick, ariaLabel, icon }: IconButtonProps) {
  return (
    <button onClick={onClick} aria-label={ariaLabel}>
      {icon}
      <span className="sr-only">{ariaLabel}</span>
    </button>
  );
}

// CSS for sr-only class:
// .sr-only {
//   position: absolute;
//   width: 1px;
//   height: 1px;
//   padding: 0;
//   margin: -1px;
//   overflow: hidden;
//   clip: rect(0, 0, 0, 0);
//   white-space: nowrap;
//   border-width: 0;
// }
```

#### Check aria-hidden Usage

**Search for aria-hidden:**
```yaml
precision_grep:
  queries:
    - id: aria_hidden
      pattern: 'aria-hidden="true"'
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Common violations:**
- `aria-hidden="true"` on interactive elements (buttons, links)
- `aria-hidden="true"` on content that should be accessible
- Decorative icons without `aria-hidden="true"`

**Correct aria-hidden usage:**
```typescript
interface ButtonWithIconProps {
  onClick: () => void;
  label: string;
}

export function ButtonWithIcon({ onClick, label }: ButtonWithIconProps) {
  return (
    <button onClick={onClick}>
      {/* Icon is decorative, hide from screen readers */}
      <CheckIcon aria-hidden="true" />
      {/* Label provides accessible text */}
      <span>{label}</span>
    </button>
  );
}
```

### Phase 6: Color and Contrast Audit

**Objective:** Ensure sufficient color contrast and no color-only information.

#### Check Contrast Ratios

**Use browser DevTools or external tools:**
- Chrome DevTools: Inspect element -> Accessibility pane -> Contrast ratio
- Firefox DevTools: Inspector -> Accessibility panel
- axe DevTools browser extension
- Lighthouse accessibility audit

**WCAG 2.1 AA requirements:**
- Normal text (< 18pt): 4.5:1 minimum contrast ratio
- Large text (>= 18pt or >= 14pt bold): 3:1 minimum contrast ratio
- UI components and graphics: 3:1 minimum contrast ratio

**Search for color definitions:**
```yaml
precision_grep:
  queries:
    - id: color_definitions
      pattern: "(bg-|text-|color:|background:)"
      glob: "**/*.{tsx,jsx,css,scss}"
  output:
    format: count_only
```

**Accessible color palette (Tailwind example):**
```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  theme: {
    extend: {
      colors: {
        // Accessible color palette with documented contrast ratios
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          600: '#0284c7', // 4.54:1 on white (WCAG AA)
          700: '#0369a1', // 7.09:1 on white (WCAG AAA)
          900: '#0c4a6e', // 13.14:1 on white
        },
        // Error color with good contrast
        error: {
          600: '#dc2626', // 4.51:1 on white
          700: '#b91c1c', // 6.70:1 on white
        },
        // Success color
        success: {
          600: '#16a34a', // 4.51:1 on white
          700: '#15803d', // 6.68:1 on white
        },
      },
    },
  },
};

export default config;
```

#### Check Color-Only Information

**Search for status indicators:**
```yaml
precision_grep:
  queries:
    - id: status_colors
      pattern: "(bg-red|bg-green|bg-yellow|text-red|text-green|text-yellow)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Manual review:** Ensure status is conveyed through multiple means (color + icon + text).

**Accessible status indicator:**
```typescript
type Status = 'success' | 'warning' | 'error' | 'info';

interface StatusBadgeProps {
  status: Status;
  message: string;
}

const statusConfig: Record<Status, { icon: React.ReactNode; className: string }> = {
  success: { icon: <CheckCircleIcon />, className: 'bg-green-100 text-green-800' },
  warning: { icon: <AlertTriangleIcon />, className: 'bg-yellow-100 text-yellow-800' },
  error: { icon: <XCircleIcon />, className: 'bg-red-100 text-red-800' },
  info: { icon: <InfoIcon />, className: 'bg-blue-100 text-blue-800' },
};

export function StatusBadge({ status, message }: StatusBadgeProps) {
  const { icon, className } = statusConfig[status];

  return (
    <div className={`flex items-center gap-2 px-3 py-2 rounded ${className}`}>
      {/* Icon provides visual indicator beyond color */}
      <span aria-hidden="true">{icon}</span>
      {/* Text provides clear status information */}
      <span>{message}</span>
    </div>
  );
}
```

#### Check Forced Colors Mode

**Search for forced-colors media query:**
```yaml
precision_grep:
  queries:
    - id: forced_colors
      pattern: "@media.*forced-colors|prefers-contrast"
      glob: "**/*.{css,scss,tsx,jsx}"
  output:
    format: files_only
```

**Support Windows High Contrast Mode:**
```css
/* Ensure borders are visible in forced-colors mode */
.card {
  border: 1px solid #e5e7eb;
}

@media (forced-colors: active) {
  .card {
    border: 1px solid CanvasText;
  }
}

/* Ensure custom controls are visible */
.custom-checkbox {
  border: 2px solid #3b82f6;
}

@media (forced-colors: active) {
  .custom-checkbox {
    border: 2px solid ButtonText;
  }
  
  .custom-checkbox:checked {
    background-color: Highlight;
  }
}
```

### Phase 7: Forms and Validation Audit

**Objective:** Ensure forms are accessible and error handling is clear.

#### Check Form Labels

**Search for input elements:**
```yaml
precision_grep:
  queries:
    - id: input_elements
      pattern: "<input|<textarea|<select"
      glob: "**/*.{tsx,jsx}"
  output:
    format: locations
```

**Manual review:** Verify each input has an associated label via:
- `<label>` with matching `htmlFor` attribute
- `aria-label` attribute
- `aria-labelledby` pointing to label element

**Common violations:**
- Placeholder-only inputs without labels
- Labels without `htmlFor` attribute
- Multiple inputs sharing one label

**Accessible form pattern:**
```typescript
import { useId, FormEvent } from 'react';

interface FormData {
  email: string;
  password: string;
}

interface LoginFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const emailId = useId();
  const passwordId = useId();
  const emailErrorId = useId();
  const passwordErrorId = useId();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    await onSubmit({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="form-field">
        {/* Explicit label with htmlFor */}
        <label htmlFor={emailId}>
          Email address
        </label>
        <input
          id={emailId}
          type="email"
          name="email"
          required
          aria-required="true"
          aria-describedby={emailErrorId}
          autoComplete="email"
        />
        {/* Error message linked via aria-describedby */}
        <p id={emailErrorId} className="error-message" role="alert">
          {/* Error text populated on validation */}
        </p>
      </div>

      <div className="form-field">
        <label htmlFor={passwordId}>
          Password
        </label>
        <input
          id={passwordId}
          type="password"
          name="password"
          required
          aria-required="true"
          aria-describedby={passwordErrorId}
          autoComplete="current-password"
        />
        <p id={passwordErrorId} className="error-message" role="alert">
          {/* Error text populated on validation */}
        </p>
      </div>

      <button type="submit">
        Sign in
      </button>
    </form>
  );
}
```

#### Check Error Handling

**Search for error patterns:**
```yaml
precision_grep:
  queries:
    - id: error_messages
      pattern: "(error|invalid|required).*message"
      glob: "**/*.{tsx,jsx,ts}"
  output:
    format: standard
```

**Accessible error handling:**
```typescript
import { useState, useId } from 'react';

interface FieldError {
  field: string;
  message: string;
}

interface FormWithValidationProps {
  onSubmit: (data: Record<string, string>) => void;
}

export function FormWithValidation({ onSubmit }: FormWithValidationProps) {
  const [errors, setErrors] = useState<FieldError[]>([]);
  const nameId = useId();
  const nameErrorId = useId();
  const errorSummaryId = useId();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const name = formData.get('name') as string;

    // Validation
    const newErrors: FieldError[] = [];
    if (!name || name.length < 2) {
      newErrors.push({ field: 'name', message: 'Name must be at least 2 characters' });
    }

    if (newErrors.length > 0) {
      setErrors(newErrors);
      // Focus error summary for screen readers
      document.getElementById(errorSummaryId)?.focus();
      return;
    }

    setErrors([]);
    onSubmit({ name });
  };

  const nameError = errors.find((e) => e.field === 'name');

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Error summary at top of form */}
      {errors.length > 0 && (
        <div
          id={errorSummaryId}
          role="alert"
          aria-labelledby="error-summary-title"
          className="error-summary"
          tabIndex={-1}
        >
          <h2 id="error-summary-title">There are {errors.length} errors</h2>
          <ul>
            {errors.map((error) => (
              <li key={error.field}>
                <a href={`#${error.field}`}>{error.message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="form-field">
        <label htmlFor={nameId}>Name</label>
        <input
          id={nameId}
          name="name"
          aria-required="true"
          aria-invalid={nameError ? 'true' : 'false'}
          aria-describedby={nameError ? nameErrorId : undefined}
        />
        {nameError && (
          <p id={nameErrorId} className="error-message" role="alert">
            {nameError.message}
          </p>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

#### Check Required Fields

**Search for required field indicators:**
```yaml
precision_grep:
  queries:
    - id: required_fields
      pattern: "(required|aria-required)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Accessible required field indicator:**
```typescript
interface RequiredFieldLabelProps {
  htmlFor: string;
  children: React.ReactNode;
}

export function RequiredFieldLabel({ htmlFor, children }: RequiredFieldLabelProps) {
  return (
    <label htmlFor={htmlFor}>
      {children}
      {/* Visual indicator */}
      <span className="text-red-600" aria-hidden="true"> *</span>
      {/* Screen reader text */}
      <span className="sr-only"> (required)</span>
    </label>
  );
}
```

### Phase 8: Media Accessibility Audit

**Objective:** Ensure images, videos, and audio content are accessible.

#### Check Image Alt Text

**Search for images:**
```yaml
precision_grep:
  queries:
    - id: img_elements
      pattern: "(<img|<Image|next/image)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Manual review:** Verify each image has:
- Meaningful `alt` text for content images
- Empty `alt=""` for decorative images
- Alt text that describes function for linked images

**Common violations:**
- Missing `alt` attribute
- Generic alt text ("image", "photo", "icon")
- Redundant alt text ("image of...", "picture of...")
- Alt text describing file name ("IMG_1234.jpg")

**Accessible image patterns:**
```typescript
import Image from 'next/image';

interface ProductImageProps {
  src: string;
  productName: string;
}

// Content image with descriptive alt
export function ProductImage({ src, productName }: ProductImageProps) {
  return (
    <Image
      src={src}
      alt={`${productName} product photo`}
      width={400}
      height={400}
    />
  );
}

// Decorative image with empty alt
export function DecorativePattern() {
  return (
    <div className="background-pattern">
      <Image
        src="/patterns/dots.svg"
        alt=""
        fill
        aria-hidden="true"
      />
    </div>
  );
}

// Functional image (icon button)
interface DeleteButtonProps {
  onDelete: () => void;
}

export function DeleteButton({ onDelete }: DeleteButtonProps) {
  return (
    <button onClick={onDelete} aria-label="Delete item">
      <Image
        src="/icons/trash.svg"
        alt=""
        width={20}
        height={20}
        aria-hidden="true"
      />
    </button>
  );
}
```

#### Check Video Captions

**Search for video elements:**
```yaml
precision_grep:
  queries:
    - id: video_elements
      pattern: "(<video|<track)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: standard
```

**Accessible video with captions:**
```typescript
interface AccessibleVideoProps {
  src: string;
  captionsSrc: string;
  title: string;
}

export function AccessibleVideo({ src, captionsSrc, title }: AccessibleVideoProps) {
  return (
    <video controls aria-label={title}>
      <source src={src} type="video/mp4" />
      {/* Captions for deaf/hard of hearing users */}
      <track
        kind="captions"
        src={captionsSrc}
        srcLang="en"
        label="English captions"
        default
      />
      {/* Fallback text */}
      <p>
        Your browser does not support the video element.
        <a href={src}>Download the video</a>
      </p>
    </video>
  );
}
```

#### Check Reduced Motion

**Search for animations:**
```yaml
precision_grep:
  queries:
    - id: animations
      pattern: "(animate|transition|prefers-reduced-motion)"
      glob: "**/*.{tsx,jsx,css,scss}"
  output:
    format: files_only
```

**Respect prefers-reduced-motion:**
```typescript
import { motion, useReducedMotion } from 'framer-motion';

interface AnimatedCardProps {
  children: React.ReactNode;
}

export function AnimatedCard({ children }: AnimatedCardProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: shouldReduceMotion ? 0 : 0.3,
      }}
    >
      {children}
    </motion.div>
  );
}
```

**CSS approach:**
```css
/* Default: animated */
.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

/* Reduced motion: disable animations */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
  
  .card:hover {
    transform: none;
  }
}
```

## Automated Testing

### Precision Tool Workflow

**Run comprehensive accessibility checks:**
```yaml
discover:
  queries:
    # Missing alt attributes
    - id: missing_alt
      type: grep
      pattern: "<img(?![^>]*alt=)"
      glob: "**/*.{tsx,jsx}"
    
    # onClick without keyboard handler
    - id: onclick_no_keyboard
      type: grep
      pattern: 'onClick=\\{(?!.*onKeyDown)'
      glob: "**/*.{tsx,jsx}"
    
    # Non-button with role=button without keyboard
    - id: role_button_no_keyboard
      type: grep
      pattern: 'role="button"(?!.*onKeyDown)'
      glob: "**/*.{tsx,jsx}"
    
    # Missing form labels
    - id: unlabeled_inputs
      type: grep
      pattern: "<input(?![^>]*aria-label)(?![^>]*id=)"
      glob: "**/*.{tsx,jsx}"
    
    # Heading level skips
    - id: heading_usage
      type: grep
      pattern: "<h[1-6]"
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

### Browser-Based Testing

Run these tools for comprehensive automated testing:

1. **Lighthouse Accessibility Audit**
   ```bash
   npx lighthouse https://localhost:3000 --only-categories=accessibility --view
   ```

2. **axe DevTools**
   - Install: [axe DevTools Chrome Extension](https://chrome.google.com/webstore)
   - Run: F12 -> axe DevTools -> Scan

3. **Pa11y CI**
   ```bash
   npm install --save-dev pa11y-ci
   npx pa11y-ci --sitemap https://yoursite.com/sitemap.xml
   ```

## Audit Reporting

### Structure Findings by WCAG Criteria

**Report template:**
```markdown
# Accessibility Audit Report

**Date:** 2026-02-16
**Auditor:** [Name]
**WCAG Version:** 2.1 Level AA
**Pages Audited:** 12

## Executive Summary

- **Critical Issues:** 3
- **Serious Issues:** 8
- **Moderate Issues:** 15
- **Minor Issues:** 22

## Findings by WCAG Principle

### 1. Perceivable

#### 1.1.1 Non-text Content (Level A) - FAIL

**Issue:** 12 images missing alt text

**Location:**
- `src/components/ProductCard.tsx:45`
- `src/components/Gallery.tsx:78`

**Impact:** Screen reader users cannot understand image content

**Recommendation:**
```typescript
// Before
<img src="/product.jpg" />

// After
<img src="/product.jpg" alt="Blue cotton t-shirt" />
```

#### 1.4.3 Contrast (Minimum) (Level AA) - FAIL

**Issue:** Primary button text has 3.2:1 contrast ratio (requires 4.5:1)

**Location:** `src/styles/globals.css:45`

**Impact:** Low vision users may not be able to read button text

**Recommendation:**
```css
/* Before: #60a5fa on #3b82f6 = 3.2:1 */
.btn-primary {
  background: #3b82f6;
  color: #60a5fa;
}

/* After: white on #2563eb = 4.5:1 */
.btn-primary {
  background: #2563eb;
  color: #ffffff;
}
```

### 2. Operable

#### 2.1.1 Keyboard (Level A) - FAIL

**Issue:** Custom dropdown not keyboard accessible

**Location:** `src/components/Dropdown.tsx`

**Impact:** Keyboard users cannot operate dropdown

**Recommendation:** Implement arrow key navigation and Enter/Space activation

### 3. Understandable

#### 3.3.2 Labels or Instructions (Level A) - FAIL

**Issue:** Form inputs missing visible labels

**Location:** `src/components/ContactForm.tsx:23-45`

**Recommendation:** Add explicit `<label>` elements with `htmlFor` attributes

### 4. Robust

#### 4.1.2 Name, Role, Value (Level A) - FAIL

**Issue:** Custom checkbox missing ARIA states

**Location:** `src/components/CustomCheckbox.tsx`

**Recommendation:** Add `aria-checked` state and `role="checkbox"`

## Priority Actions

1. **Critical:** Add alt text to all images (affects 100% of screen reader users)
2. **Critical:** Fix keyboard navigation in dropdown (blocks keyboard users)
3. **High:** Fix color contrast on primary buttons (affects ~4.5% of users)
4. **High:** Add form labels (affects screen reader and cognitive users)
```

## Related Skills

- **code-review** - Apply accessibility checks during code review
- **component-architecture** - Design accessible component APIs
- **testing-strategy** - Include accessibility in test suites

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
