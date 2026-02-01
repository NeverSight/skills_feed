---
name: Design to Code
description: This skill should be used when the user asks to "코드 변환", "React 생성", "Tailwind 코드", "컴포넌트 코드", "디자인을 코드로", ".pen 파일에서 코드", or wants to convert Pencil designs into React + Tailwind CSS code.
version: 0.1.0
---

# Design to Code

Pencil .pen 파일의 디자인을 React + Tailwind CSS 코드로 변환하는 가이드라인을 제공한다.

## Conversion Workflow

### 1. 디자인 분석

대상 노드의 구조를 파악한다:

```
mcp__pencil__batch_get(
  filePath: "design.pen",
  nodeIds: ["targetNodeId"],
  readDepth: 5,
  resolveInstances: true,
  resolveVariables: true
)
```

`resolveInstances: true`로 컴포넌트 인스턴스를 풀어서 확인하고, `resolveVariables: true`로 변수값을 실제 값으로 확인한다.

### 2. 변수 추출

디자인 토큰을 Tailwind 설정으로 변환한다:

```
mcp__pencil__get_variables(filePath: "design.pen")
```

### 3. 코드 생성

노드 타입에 따라 적절한 React 컴포넌트로 변환한다.

### 4. 스크린샷 비교

생성된 코드를 시각적으로 검증한다.

## Node to Component Mapping

| Pencil Node | React/HTML | Tailwind Classes |
|-------------|------------|------------------|
| frame (layout: vertical) | `<div>` | `flex flex-col` |
| frame (layout: horizontal) | `<div>` | `flex flex-row` |
| frame (layout: grid) | `<div>` | `grid grid-cols-N` |
| text | `<p>`, `<span>`, `<h1-6>` | `text-*`, `font-*` |
| rectangle | `<div>` | `rounded-*`, `bg-*` |
| ref (Button) | `<button>` or `<Button>` | 컴포넌트별 |

## Property to Tailwind Mapping

### Layout

| Pencil Property | Tailwind |
|-----------------|----------|
| `layout: "horizontal"` | `flex flex-row` |
| `layout: "vertical"` | `flex flex-col` |
| `layout: "grid"` | `grid` |
| `gap: 16` | `gap-4` |
| `padding: 16` | `p-4` |
| `padding: [16, 24, 16, 24]` | `py-4 px-6` |
| `alignItems: "center"` | `items-center` |
| `justifyContent: "center"` | `justify-center` |
| `justifyContent: "space-between"` | `justify-between` |

### Sizing

| Pencil Property | Tailwind |
|-----------------|----------|
| `width: "fill_container"` | `w-full` |
| `height: "fill_container"` | `h-full` |
| `width: "hug_contents"` | `w-fit` |
| `width: 320` | `w-80` or `w-[320px]` |

### Typography

| Pencil Property | Tailwind |
|-----------------|----------|
| `fontSize: 16` | `text-base` |
| `fontSize: 24` | `text-2xl` |
| `fontWeight: "bold"` | `font-bold` |
| `fontWeight: "semibold"` | `font-semibold` |
| `textAlign: "center"` | `text-center` |
| `textColor: "#3B82F6"` | `text-blue-500` |

### Colors

| Pencil Color | Tailwind |
|--------------|----------|
| `#3B82F6` | `blue-500` |
| `#EF4444` | `red-500` |
| `#22C55E` | `green-500` |
| `#F8FAFC` | `slate-50` |
| `#0F172A` | `slate-900` |

### Border Radius

| Pencil Property | Tailwind |
|-----------------|----------|
| `cornerRadius: 4` | `rounded-sm` |
| `cornerRadius: 8` | `rounded-lg` |
| `cornerRadius: 12` | `rounded-xl` |
| `cornerRadius: 9999` | `rounded-full` |

### Effects

| Pencil Property | Tailwind |
|-----------------|----------|
| `opacity: 0.5` | `opacity-50` |
| `overflow: "hidden"` | `overflow-hidden` |
| Shadow (small) | `shadow-sm` |
| Shadow (medium) | `shadow-md` |

## Code Generation Patterns

### Basic Component

Pencil 노드:
```json
{
  "type": "frame",
  "layout": "vertical",
  "padding": 24,
  "gap": 16,
  "fill": "#FFFFFF",
  "cornerRadius": 12,
  "children": [
    { "type": "text", "content": "Title", "fontSize": 24, "fontWeight": "bold" },
    { "type": "text", "content": "Description", "textColor": "#64748B" }
  ]
}
```

React + Tailwind:
```tsx
function Card() {
  return (
    <div className="flex flex-col p-6 gap-4 bg-white rounded-xl">
      <h2 className="text-2xl font-bold">Title</h2>
      <p className="text-slate-500">Description</p>
    </div>
  )
}
```

### Interactive Component

버튼 컴포넌트:
```tsx
interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
}

function Button({ children, variant = 'primary', onClick }: ButtonProps) {
  const baseClasses = "flex items-center justify-center px-6 py-3 gap-2 rounded-lg font-medium transition-colors"
  const variantClasses = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-transparent border border-blue-500 text-blue-500 hover:bg-blue-50"
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### Layout Component

페이지 레이아웃:
```tsx
function PageLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="flex flex-col w-64 p-6 gap-4 bg-slate-50 border-r border-slate-200">
        <h1 className="text-xl font-bold">Logo</h1>
        <nav className="flex flex-col gap-2">
          <a href="#" className="px-4 py-2 rounded-lg hover:bg-slate-100">Dashboard</a>
          <a href="#" className="px-4 py-2 rounded-lg hover:bg-slate-100">Settings</a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  )
}
```

## Variable to Tailwind Config

Pencil 변수를 tailwind.config.js로 변환:

### Input (Pencil Variables)
```json
{
  "colors": {
    "primary": { "500": "#3B82F6", "600": "#2563EB" },
    "neutral": { "50": "#F8FAFC", "900": "#0F172A" }
  },
  "spacing": { "4": 16, "6": 24, "8": 32 },
  "radii": { "md": 8, "lg": 12 }
}
```

### Output (Tailwind Config)
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#3B82F6',
          600: '#2563EB',
        },
        neutral: {
          50: '#F8FAFC',
          900: '#0F172A',
        },
      },
      spacing: {
        4: '16px',
        6: '24px',
        8: '32px',
      },
      borderRadius: {
        md: '8px',
        lg: '12px',
      },
    },
  },
}
```

## Best Practices

### Component Naming

- 의미 있는 이름 사용 (Card, Button, Header)
- PascalCase 사용
- 파일명은 컴포넌트명과 일치

### Props Design

- 필수 props와 선택 props 구분
- 합리적인 기본값 제공
- TypeScript 인터페이스 정의

### Tailwind Usage

- 유틸리티 클래스 우선
- 반복되는 패턴은 컴포넌트로 추출
- 복잡한 값은 arbitrary values 사용 `w-[320px]`
- `@apply`는 최소화

### Accessibility

- 시맨틱 HTML 요소 사용
- ARIA 속성 적절히 추가
- 키보드 네비게이션 지원
- 색상 대비 확인

## Output Format

단일 TSX 파일 형식:

```tsx
// ComponentName.tsx
import { useState } from 'react'

interface ComponentNameProps {
  // props 정의
}

export function ComponentName({ ...props }: ComponentNameProps) {
  // 상태 및 로직

  return (
    // JSX
  )
}
```

## Additional Resources

### Reference Files

- **`references/tailwind-mapping.md`** - 전체 Pencil-Tailwind 매핑 테이블
- **`references/component-templates.md`** - 공통 컴포넌트 템플릿
