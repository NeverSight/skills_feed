---
name: ui-ux-design
description: UI/UX design patterns and best practices for the LMS. Activate when designing pages, creating layouts, working on user experience, or building navigation.
---

# UI/UX Design for DevOps LMS

## Activation Triggers
- Designing new pages or layouts
- Creating navigation structures
- Working on user flows
- Building responsive designs
- Implementing accessibility features
- Designing progress visualization

## Design System

### Color Palette (Dark Mode)

```css
/* Backgrounds */
--bg-base: #111827;      /* gray-900 - Main background */
--bg-elevated: #1f2937;  /* gray-800 - Cards, sidebars */
--bg-hover: #374151;     /* gray-700 - Hover states */

/* Text */
--text-primary: #f9fafb;   /* gray-50 - Headings */
--text-secondary: #e5e7eb; /* gray-200 - Body text */
--text-muted: #9ca3af;     /* gray-400 - Secondary info */
--text-disabled: #6b7280;  /* gray-500 - Disabled */

/* Accent Colors */
--primary: #6366f1;      /* indigo-500 - Primary actions */
--success: #22c55e;      /* green-500 - Completed */
--warning: #f59e0b;      /* amber-500 - In progress */
--error: #ef4444;        /* red-500 - Failed/errors */

/* Borders */
--border: #374151;       /* gray-700 */
```

### Typography Scale

```css
/* Headings */
.text-4xl  /* 36px - Page titles */
.text-2xl  /* 24px - Section headers */
.text-xl   /* 20px - Card titles */
.text-lg   /* 18px - Subsection headers */
.text-base /* 16px - Body text */
.text-sm   /* 14px - Secondary text */
.text-xs   /* 12px - Badges, labels */

/* Font Weights */
.font-bold     /* 700 - Headings */
.font-semibold /* 600 - Subheadings */
.font-medium   /* 500 - Emphasis */
.font-normal   /* 400 - Body */
```

### Spacing System

```css
/* Use consistent spacing */
.space-y-2  /* 8px - Tight grouping */
.space-y-4  /* 16px - Related items */
.space-y-6  /* 24px - Sections */
.space-y-8  /* 32px - Major sections */

/* Padding */
.p-4   /* 16px - Card content */
.p-6   /* 24px - Large cards */
.px-4  /* Horizontal padding */
.py-2  /* Vertical padding for buttons */
```

## Page Layouts

### Dashboard Layout (Home Page)
```
┌─────────────────────────────────────────────────────────────┐
│  Header: Logo + Navigation + Progress Summary               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Hero Section                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Overall Progress: 45/527 lessons (8.5%)            │   │
│  │  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░] 8.5%          │   │
│  │  [Continue Learning] [View Certificate]              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Phase Grid (2-3 columns)                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Phase 1      │ │ Phase 2      │ │ Phase 3      │        │
│  │ SDLC         │ │ Foundations  │ │ Cloud        │        │
│  │ ████░░ 80%   │ │ ██░░░░ 33%   │ │ ░░░░░░ 0%    │        │
│  │ 4/5 topics   │ │ 2/6 topics   │ │ 0/9 topics   │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Lesson Layout
```
┌─────────────────────────────────────────────────────────────┐
│  Breadcrumb: Home > Phase 1 > SDLC Models > Waterfall       │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  Sidebar     │  Lesson Content                              │
│  (240px)     │                                              │
│              │  ┌────────────────────────────────────────┐  │
│  Phase 1 ▼   │  │  Waterfall Model                       │  │
│  ├ SDLC      │  │  ⏱ 15 min • 🟢 Beginner               │  │
│  │ Models ▼  │  └────────────────────────────────────────┘  │
│  │ ├ ✓ Water │                                              │
│  │ ├ ○ Agile │  ## What is Waterfall?                       │
│  │ └ ○ Scrum │  The Waterfall model is a linear...          │
│  └ Phases    │                                              │
│              │  ## Key Phases                                │
│  Phase 2     │  1. Requirements                              │
│  Phase 3     │  2. Design                                    │
│              │  ...                                          │
│              │                                              │
│              │  ┌────────────────────────────────────────┐  │
│              │  │  [Mark Complete] [← Prev] [Next →]     │  │
│              │  └────────────────────────────────────────┘  │
│              │                                              │
│              │  Quiz Section (collapsible)                  │
│              │  ┌────────────────────────────────────────┐  │
│              │  │  Question 1 of 4                        │  │
│              │  │  What is the main characteristic...     │  │
│              │  │  ○ Option A                             │  │
│              │  │  ○ Option B                             │  │
│              │  │  ● Option C ✓                           │  │
│              │  │  ○ Option D                             │  │
│              │  └────────────────────────────────────────┘  │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### Progress Page Layout
```
┌─────────────────────────────────────────────────────────────┐
│  Your Learning Progress                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stats Cards (4 columns)                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 45       │ │ 8.5%     │ │ 12h 30m  │ │ 3        │       │
│  │ Completed│ │ Progress │ │ Time     │ │ Quizzes  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                             │
│  Phase Progress (Accordion)                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ▼ Phase 1: SDLC                           80% ████░ │   │
│  │   ├ SDLC Models                           100% ████ │   │
│  │   ├ SDLC Phases                           60%  ███░ │   │
│  │   └ Development Workflows                 0%   ░░░░ │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ ▶ Phase 2: Foundations                    33% ██░░░ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Patterns

### Phase Card
```vue
<UCard class="hover:ring-2 hover:ring-primary-500 transition-all cursor-pointer">
  <div class="flex items-start justify-between mb-4">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-primary-500/20 flex items-center justify-center">
        <UIcon name="i-heroicons-academic-cap" class="w-5 h-5 text-primary-500" />
      </div>
      <div>
        <h3 class="font-semibold">Phase 1: SDLC</h3>
        <p class="text-sm text-gray-400">4 topics • 20 lessons</p>
      </div>
    </div>
    <UBadge :color="progress === 100 ? 'success' : 'warning'">
      {{ progress }}%
    </UBadge>
  </div>
  
  <UProgress :value="progress" :color="progress === 100 ? 'success' : 'primary'" />
  
  <div class="mt-4 flex justify-between items-center">
    <span class="text-sm text-gray-400">Est. 2h 30m</span>
    <UButton size="sm" variant="soft">
      {{ progress > 0 ? 'Continue' : 'Start' }}
    </UButton>
  </div>
</UCard>
```

### Lesson Sidebar Item
```vue
<div 
  class="flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors"
  :class="[
    isActive ? 'bg-primary-500/20 text-primary-400' : 'hover:bg-gray-700',
    isCompleted ? 'text-gray-400' : 'text-gray-200'
  ]"
>
  <UIcon 
    :name="isCompleted ? 'i-heroicons-check-circle-solid' : 'i-heroicons-circle'" 
    :class="isCompleted ? 'text-success-500' : 'text-gray-500'"
    class="w-5 h-5 flex-shrink-0"
  />
  <span class="truncate">{{ title }}</span>
  <UBadge v-if="isActive" size="xs" color="primary">Current</UBadge>
</div>
```

### Quiz Question Card
```vue
<UCard>
  <div class="flex items-center justify-between mb-4">
    <span class="text-sm text-gray-400">Question {{ current }} of {{ total }}</span>
    <UBadge>{{ difficulty }}</UBadge>
  </div>
  
  <h3 class="text-lg font-medium mb-6">{{ question }}</h3>
  
  <div class="space-y-3">
    <div 
      v-for="option in options" 
      :key="option"
      class="flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-all"
      :class="[
        selected === option 
          ? 'border-primary-500 bg-primary-500/10' 
          : 'border-gray-700 hover:border-gray-600'
      ]"
      @click="select(option)"
    >
      <div 
        class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
        :class="selected === option ? 'border-primary-500' : 'border-gray-600'"
      >
        <div 
          v-if="selected === option" 
          class="w-2.5 h-2.5 rounded-full bg-primary-500"
        />
      </div>
      <span>{{ option }}</span>
    </div>
  </div>
  
  <div class="flex justify-between mt-6">
    <UButton variant="outline" @click="prev" :disabled="current === 1">
      Previous
    </UButton>
    <UButton @click="next">
      {{ current === total ? 'Finish' : 'Next' }}
    </UButton>
  </div>
</UCard>
```

## Responsive Design

### Breakpoints
```css
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

### Mobile Patterns
```vue
<!-- Sidebar: Hidden on mobile, drawer on tablet, visible on desktop -->
<div class="hidden lg:block w-64">
  <LessonSidebar />
</div>

<!-- Mobile menu button -->
<UButton 
  class="lg:hidden" 
  icon="i-heroicons-bars-3" 
  variant="ghost"
  @click="showMobileMenu = true"
/>

<!-- Mobile drawer -->
<USlideover v-model:open="showMobileMenu">
  <LessonSidebar @close="showMobileMenu = false" />
</USlideover>

<!-- Grid: 1 column mobile, 2 tablet, 3 desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <PhaseCard v-for="phase in phases" :key="phase.id" :phase="phase" />
</div>
```

## Accessibility

### Focus States
```vue
<!-- All interactive elements need visible focus -->
<UButton class="focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-gray-900">
  Click me
</UButton>

<!-- Custom focusable elements -->
<div 
  tabindex="0"
  class="focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg"
  @keydown.enter="handleClick"
  @keydown.space.prevent="handleClick"
>
  Clickable content
</div>
```

### Screen Reader Support
```vue
<!-- Always add aria labels -->
<UButton aria-label="Mark lesson as complete">
  <UIcon name="i-heroicons-check" />
</UButton>

<!-- Progress announcements -->
<div role="progressbar" :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
  <UProgress :value="progress" />
</div>

<!-- Navigation landmarks -->
<nav aria-label="Lesson navigation">
  <LessonSidebar />
</nav>
```

## Animation & Transitions

```vue
<!-- Hover effects -->
<div class="transition-all duration-200 hover:scale-[1.02] hover:shadow-lg">

<!-- Content transitions -->
<Transition name="fade" mode="out-in">
  <component :is="currentComponent" />
</Transition>

<!-- CSS -->
<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<!-- List transitions -->
<TransitionGroup name="list" tag="div">
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>
</TransitionGroup>
```

## Empty & Error States

### Empty State
```vue
<div class="flex flex-col items-center justify-center py-16 text-center">
  <div class="w-16 h-16 rounded-full bg-gray-800 flex items-center justify-center mb-4">
    <UIcon name="i-heroicons-document-text" class="w-8 h-8 text-gray-500" />
  </div>
  <h3 class="text-lg font-medium mb-2">No lessons found</h3>
  <p class="text-gray-400 mb-6 max-w-sm">
    Start exploring the roadmap to begin your DevOps learning journey.
  </p>
  <UButton to="/">Explore Roadmap</UButton>
</div>
```

### Error State
```vue
<UCard class="border-error-500/50 bg-error-500/10">
  <div class="flex items-start gap-4">
    <UIcon name="i-heroicons-exclamation-triangle" class="w-6 h-6 text-error-500 flex-shrink-0" />
    <div>
      <h3 class="font-medium text-error-400">Failed to load lesson</h3>
      <p class="text-sm text-gray-400 mt-1">{{ error.message }}</p>
      <UButton size="sm" variant="soft" color="error" class="mt-3" @click="retry">
        Try Again
      </UButton>
    </div>
  </div>
</UCard>
```
