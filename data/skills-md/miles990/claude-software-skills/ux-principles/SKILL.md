---
name: ux-principles
description: User experience design principles for developers
domain: software-design
version: 1.0.0
tags: [ux, usability, accessibility, responsive, design-system, wcag]
triggers:
  keywords:
    primary: [ux, user experience, usability, accessibility, a11y, wcag]
    secondary: [responsive, design system, heuristics, user flow, information architecture]
  context_boost: [frontend, ui, design, user, interface]
  context_penalty: [backend, database, devops]
  priority: medium
---

# UX Principles

## Overview

Essential UX principles that every developer should know. Good UX isn't just design—it's built into code, architecture, and technical decisions.

---

## Nielsen's 10 Usability Heuristics

### 1. Visibility of System Status

```typescript
// ❌ No feedback
async function saveDocument() {
  await api.save(document);
}

// ✅ Clear feedback
async function saveDocument() {
  setStatus('saving');
  try {
    await api.save(document);
    setStatus('saved');
    showToast('Document saved');
  } catch (error) {
    setStatus('error');
    showToast('Failed to save. Please try again.');
  }
}
```

```html
<!-- Progress indicators -->
<button disabled={isLoading}>
  {isLoading ? (
    <>
      <Spinner /> Saving...
    </>
  ) : (
    'Save'
  )}
</button>

<!-- Upload progress -->
<progress value={uploadProgress} max="100" />
<span>{uploadProgress}% uploaded</span>
```

### 2. Match Between System and Real World

```typescript
// ❌ Technical jargon
"Error: ECONNREFUSED 127.0.0.1:5432"

// ✅ Human language
"We couldn't connect to the database. Please check your internet connection."

// ❌ Developer terms
"Record not found in users table"

// ✅ User terms
"We couldn't find an account with that email address"
```

### 3. User Control and Freedom

```typescript
// Undo functionality
function deleteItem(id: string) {
  const item = items.find(i => i.id === id);
  setItems(items.filter(i => i.id !== id));

  showToast({
    message: 'Item deleted',
    action: {
      label: 'Undo',
      onClick: () => setItems([...items, item])
    },
    duration: 5000
  });
}

// Cancel long operations
const controller = new AbortController();

async function uploadFile(file: File) {
  try {
    await fetch('/upload', {
      method: 'POST',
      body: file,
      signal: controller.signal
    });
  } catch (e) {
    if (e.name === 'AbortError') {
      showToast('Upload cancelled');
    }
  }
}

// User can cancel
<button onClick={() => controller.abort()}>Cancel Upload</button>
```

### 4. Consistency and Standards

```typescript
// Design tokens for consistency
const theme = {
  colors: {
    primary: '#007bff',
    danger: '#dc3545',
    success: '#28a745',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
  }
};

// Consistent button patterns
<Button variant="primary">Save</Button>      // Main action
<Button variant="secondary">Cancel</Button>  // Secondary action
<Button variant="danger">Delete</Button>     // Destructive action
```

### 5. Error Prevention

```typescript
// Confirm destructive actions
function deleteAccount() {
  const confirmed = await confirm({
    title: 'Delete Account?',
    message: 'This action cannot be undone. All your data will be permanently deleted.',
    confirmText: 'Delete Account',
    confirmVariant: 'danger'
  });

  if (confirmed) {
    await api.deleteAccount();
  }
}

// Input constraints
<input
  type="number"
  min={0}
  max={100}
  step={1}
  inputMode="numeric"
/>

// Disable invalid actions
<button
  disabled={!isFormValid || isSubmitting}
  title={!isFormValid ? 'Please fill all required fields' : undefined}
>
  Submit
</button>
```

---

## Accessibility (WCAG)

### Semantic HTML

```html
<!-- ❌ Div soup -->
<div class="nav">
  <div class="nav-item" onclick="navigate()">Home</div>
</div>

<!-- ✅ Semantic HTML -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<!-- ❌ Missing labels -->
<input type="text" placeholder="Email">

<!-- ✅ Proper labeling -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" required>
```

### ARIA Attributes

```html
<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

<!-- Modal dialogs -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure you want to proceed?</p>
</div>

<!-- Loading states -->
<button aria-busy={isLoading} aria-disabled={isLoading}>
  {isLoading ? 'Loading...' : 'Submit'}
</button>

<!-- Expandable sections -->
<button
  aria-expanded={isOpen}
  aria-controls="panel-content"
>
  Show Details
</button>
<div id="panel-content" hidden={!isOpen}>
  Details here...
</div>
```

### Keyboard Navigation

```typescript
// Focus management
function openModal() {
  setIsOpen(true);
  // Focus first focusable element
  setTimeout(() => {
    modalRef.current?.querySelector('button, [href], input')?.focus();
  }, 0);
}

function closeModal() {
  setIsOpen(false);
  // Return focus to trigger
  triggerRef.current?.focus();
}

// Focus trap in modals
function handleKeyDown(e: KeyboardEvent) {
  if (e.key === 'Tab') {
    const focusable = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const first = focusable?.[0];
    const last = focusable?.[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last?.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first?.focus();
    }
  }

  if (e.key === 'Escape') {
    closeModal();
  }
}
```

### Color and Contrast

```css
/* WCAG AA: 4.5:1 for normal text, 3:1 for large text */
:root {
  --text-primary: #1a1a1a;     /* High contrast on white */
  --text-secondary: #6b7280;   /* 4.5:1 on white */
  --text-on-primary: #ffffff;  /* White on brand color */
}

/* Don't rely on color alone */
.error-message {
  color: #dc3545;
  /* Also include icon */
  &::before {
    content: "⚠ ";
  }
}

/* Focus indicators */
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Never remove focus styles entirely */
/* ❌ */ :focus { outline: none; }
```

---

## Responsive Design

### Mobile-First Approach

```css
/* Base styles for mobile */
.container {
  padding: 16px;
}

.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Touch Targets

```css
/* Minimum 44x44px touch targets (WCAG) */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* Adequate spacing between interactive elements */
.button-group {
  display: flex;
  gap: 8px;
}

/* Make entire area tappable */
.card-link {
  position: relative;
}

.card-link::after {
  content: '';
  position: absolute;
  inset: 0;
}
```

---

## Performance as UX

### Perceived Performance

```typescript
// Optimistic updates
function likePost(postId: string) {
  // Update UI immediately
  setLiked(true);
  setLikeCount(prev => prev + 1);

  // Sync with server in background
  api.likePost(postId).catch(() => {
    // Rollback on failure
    setLiked(false);
    setLikeCount(prev => prev - 1);
    showToast('Failed to like post');
  });
}

// Skeleton loading
function PostList() {
  if (isLoading) {
    return (
      <div className="post-list">
        {[1, 2, 3].map(i => (
          <div key={i} className="post-skeleton">
            <div className="skeleton-avatar" />
            <div className="skeleton-text" />
            <div className="skeleton-text short" />
          </div>
        ))}
      </div>
    );
  }

  return <div className="post-list">{posts.map(renderPost)}</div>;
}
```

### Content Prioritization

```html
<!-- Critical content first -->
<head>
  <!-- Preload critical assets -->
  <link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
  <link rel="preload" href="/hero-image.webp" as="image">

  <!-- Defer non-critical CSS -->
  <link rel="preload" href="/non-critical.css" as="style" onload="this.rel='stylesheet'">
</head>

<!-- Lazy load below-fold images -->
<img src="product.jpg" loading="lazy" alt="Product image">

<!-- Intersection Observer for infinite scroll -->
<div ref={sentinelRef}>
  {hasMore && <Spinner />}
</div>
```

---

## Forms UX

### Input Design

```html
<!-- Clear labels and help text -->
<div class="form-field">
  <label for="password">Password</label>
  <input
    type="password"
    id="password"
    aria-describedby="password-help"
    minlength="8"
  >
  <small id="password-help">At least 8 characters</small>
</div>

<!-- Inline validation -->
<input
  type="email"
  class={hasError ? 'input-error' : ''}
  aria-invalid={hasError}
  aria-describedby={hasError ? 'email-error' : undefined}
>
{hasError && (
  <span id="email-error" class="error-message" role="alert">
    Please enter a valid email address
  </span>
)}
```

### Form Patterns

```typescript
// Auto-save drafts
const debouncedSave = useMemo(
  () => debounce((data) => saveDraft(data), 1000),
  []
);

useEffect(() => {
  debouncedSave(formData);
}, [formData]);

// Clear error on input
function handleChange(field: string, value: string) {
  setFormData(prev => ({ ...prev, [field]: value }));
  setErrors(prev => ({ ...prev, [field]: undefined }));
}

// Preserve form state on navigation
useBeforeUnload(
  useCallback((e) => {
    if (hasUnsavedChanges) {
      e.preventDefault();
      return 'You have unsaved changes';
    }
  }, [hasUnsavedChanges])
);
```

---

## Empty States

```tsx
function EmptyState({ type }: { type: 'search' | 'empty' | 'error' }) {
  const content = {
    search: {
      icon: <SearchIcon />,
      title: 'No results found',
      message: 'Try adjusting your search or filters',
      action: <Button onClick={clearFilters}>Clear filters</Button>
    },
    empty: {
      icon: <FolderIcon />,
      title: 'No projects yet',
      message: 'Create your first project to get started',
      action: <Button onClick={createProject}>Create Project</Button>
    },
    error: {
      icon: <AlertIcon />,
      title: 'Something went wrong',
      message: 'We couldn\'t load the data. Please try again.',
      action: <Button onClick={retry}>Retry</Button>
    }
  }[type];

  return (
    <div className="empty-state">
      {content.icon}
      <h3>{content.title}</h3>
      <p>{content.message}</p>
      {content.action}
    </div>
  );
}
```

---

## Related Skills

- [[frontend]] - UI implementation
- [[design-patterns]] - UI patterns
- [[accessibility]] - Detailed WCAG compliance
