---
name: angular-20
description: Angular 20 knowledge and best practices. Use this skill when asked about Angular 20 development, architecture, components, routing, state management, performance, testing, and deployment. Includes standalone components, signals, and modern Angular patterns.
license: MIT
---

# Angular 20 Skill

## Rules

### Component Architecture

**MUST use standalone components:**
- All new components MUST be standalone
- Components MUST use `standalone: true` in decorator
- Components MUST explicitly import dependencies in `imports` array

**MUST NOT use NgModule-based components in new code:**
- NgModule declarations are forbidden for new components

### State Management

**MUST use Signals for local state:**
- Use `signal()` for component-level reactive state
- Use `computed()` for derived state
- Use `effect()` for side effects

**MUST use @ngrx/signals for global state:**
- Centralized application state MUST use @ngrx/signals
- MUST NOT use custom state management solutions

### Routing

**MUST use lazy-loaded routes for large modules:**
- Feature modules MUST be lazy loaded
- Use `loadChildren` or `loadComponent` for routing

**MUST implement prefetching strategies:**
- Configure preloading strategy for performance optimization

### HTTP & API

**MUST use HttpClient with typed responses:**
- All HTTP calls MUST specify response types
- API services MUST centralize HTTP logic
- Error handling MUST be implemented for all HTTP calls

### Testing

**MUST include unit tests:**
- Use Jasmine/Karma or Jest for unit testing
- Components MUST have corresponding spec files

**MUST include E2E tests for critical flows:**
- Use Playwright for E2E testing

### Performance

**MUST use AOT compilation for production:**
- Production builds MUST use `ng build` with AOT

**MUST use OnPush change detection where applicable:**
- Components with Signals SHOULD use `ChangeDetectionStrategy.OnPush`

### Accessibility

**MUST enforce accessibility (a11y) guidelines:**
- Templates MUST follow WCAG standards
- Interactive elements MUST be keyboard accessible

### Build & Deployment

**MUST use Angular CLI for builds:**
- Use `ng build` to create production artifacts

**MUST configure environment-specific settings:**
- Separate configurations for development, staging, and production

## Context

### Purpose
This skill provides structured guidance and best practices for Angular 20 development, including typical workflows, common patterns, quality standards, and example templates.

### Angular 20 Core Concepts
- Angular 20 features & changes  
- TypeScript-first architecture  
- Standalone components  
- Signals and reactivity  
- Composition API  
- Angular CLI workflows

### When to Use This Skill

Use this skill when:
- Developing Angular 20 applications
- Setting up new Angular projects
- Implementing components, routing, state management
- Optimizing performance
- Writing tests
- Deploying Angular applications

### Key Tasks & Workflows

#### 1) Create a new Angular 20 app
Use Angular CLI to bootstrap projects:
```bash
ng new your-app --routing --style=scss
```

#### 2) Component & Template Patterns
- Use standalone components where possible
- Keep templates clean & concise
- Enforce accessibility (a11y) guidelines

#### 3) Routing & Navigation
- Setup RouterModule with routes
- Use lazy-loaded routes for large modules
- Implement prefetching strategies for performance

#### 4) State & Reactivity
- Prefer Signals for local state
- Consider @ngrx/signals for global state
- Manage effects/rx workflows carefully

#### 5) HTTP & REST
- Use HttpClient with typed responses
- Centralize API service layer with error handling

#### 6) Testing
- Unit test with Jasmine/Karma or Jest
- E2E tests with Playwright

#### 7) Performance
- Use AOT compilation
- Optimize bundle with `ng build`
- Use OnPush change detection where applicable

#### 8) Deployment
- Build artifacts: `ng build`
- Serve with static hosts / CDNs
- Configure environment-specific settings

## 📌 Examples & Code Snippets

### Example Standalone Component
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (showContent()) {
      <div>Content here</div>
    }
  `
})
export class ExampleComponent {
  showContent = signal(true);
}
```

### Example Reactive Form
```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form">
      <input formControlName="name" />
    </form>
  `
})
export class FormComponent {
  private fb = inject(FormBuilder);
  
  form = this.fb.group({
    name: ['', Validators.required]
  });
}
```

### Example API Service
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  
  getData(): Observable<any[]> {
    return this.http.get<any[]>('/api/data');
  }
}
```

Refer to official Angular docs and community standards for evolving best practices.

---

## 📂 Installation Path

### 🎯 Project-specific skill
`.github/skills/angular-20/SKILL.md`

### 🎯 Personal global skill
`~/.github/skills/angular-20/SKILL.md`

💡 Copilot will automatically load this skill based on your prompt content.
