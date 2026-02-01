---
name: Design System Patterns
description: This skill should be used when the user asks about "디자인 시스템", "변수", "테마", "컬러 팔레트", "타이포그래피 스케일", "스페이싱 시스템", "컴포넌트 라이브러리", or wants to create or manage design system components and tokens in Pencil.
version: 0.1.0
---

# Design System Patterns

Pencil에서 디자인 시스템을 구축하고 관리하는 패턴과 모범 사례를 제공한다.

## Core Concepts

### 디자인 토큰

디자인 토큰은 디자인 시스템의 기본 단위로, 변수로 정의하여 일관성을 유지한다.

| Token Type | 예시 | 용도 |
|------------|------|------|
| Colors | primary, secondary, neutral | 브랜드 색상, UI 색상 |
| Typography | heading, body, caption | 폰트 크기, 굵기, 행간 |
| Spacing | xs, sm, md, lg, xl | 여백, 간격 |
| Radii | sm, md, lg, full | 모서리 둥글기 |
| Shadows | sm, md, lg | 그림자 효과 |

### 컴포넌트 계층

```
Primitives (기본 요소)
  └── Atoms (원자: Button, Input, Badge)
       └── Molecules (분자: SearchBar, Card, MenuItem)
            └── Organisms (유기체: Header, Sidebar, Form)
                 └── Templates (템플릿: PageLayout, DashboardLayout)
```

## Variables Management

### get_variables로 조회

```
mcp__pencil__get_variables(filePath: string)
```

현재 정의된 모든 변수와 테마를 반환한다.

### set_variables로 설정

```
mcp__pencil__set_variables(
  filePath: string,
  variables: object,
  replace?: boolean
)
```

### 변수 구조 예시

```json
{
  "colors": {
    "primary": {
      "50": "#EFF6FF",
      "100": "#DBEAFE",
      "500": "#3B82F6",
      "600": "#2563EB",
      "700": "#1D4ED8"
    },
    "neutral": {
      "50": "#F8FAFC",
      "100": "#F1F5F9",
      "500": "#64748B",
      "900": "#0F172A"
    }
  },
  "typography": {
    "fontFamily": "Inter, sans-serif",
    "fontSize": {
      "xs": 12,
      "sm": 14,
      "base": 16,
      "lg": 18,
      "xl": 20,
      "2xl": 24,
      "3xl": 30
    },
    "fontWeight": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    }
  },
  "spacing": {
    "0": 0,
    "1": 4,
    "2": 8,
    "3": 12,
    "4": 16,
    "5": 20,
    "6": 24,
    "8": 32,
    "10": 40,
    "12": 48
  },
  "radii": {
    "none": 0,
    "sm": 4,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999
  }
}
```

### 변수 참조

노드 속성에서 변수 참조:

```javascript
button=I("parentId", {
  type: "frame",
  fill: "var(colors/primary/500)",
  padding: "var(spacing/4)",
  cornerRadius: "var(radii/md)"
})
label=I(button, {
  type: "text",
  content: "Button",
  fontSize: "var(typography/fontSize/base)",
  fontWeight: "var(typography/fontWeight/medium)",
  textColor: "#FFFFFF"
})
```

## Creating Reusable Components

### 컴포넌트 정의

`reusable: true` 속성으로 컴포넌트 등록:

```javascript
// Button 컴포넌트 정의
buttonComp=I(document, {
  type: "frame",
  name: "Button",
  reusable: true,
  layout: "horizontal",
  padding: [12, 24, 12, 24],
  alignItems: "center",
  justifyContent: "center",
  gap: 8,
  fill: "var(colors/primary/500)",
  cornerRadius: "var(radii/md)"
})
btnLabel=I(buttonComp, {
  type: "text",
  name: "label",
  content: "Button",
  textColor: "#FFFFFF",
  fontWeight: "var(typography/fontWeight/medium)"
})
```

### 컴포넌트 인스턴스 사용

```javascript
// 컴포넌트 인스턴스 생성
btn1=I("formId", { type: "ref", ref: "buttonCompId" })

// 인스턴스 내부 수정
U(btn1+"/label", { content: "Submit" })
```

### 컴포넌트 Variants

상태별 변형을 별도 컴포넌트로 정의:

```javascript
// Primary Button
primaryBtn=I(document, {
  type: "frame",
  name: "Button/Primary",
  reusable: true,
  fill: "var(colors/primary/500)"
  // ... rest
})

// Secondary Button
secondaryBtn=I(document, {
  type: "frame",
  name: "Button/Secondary",
  reusable: true,
  fill: "transparent",
  stroke: "var(colors/primary/500)",
  strokeWidth: 1
  // ... rest
})

// Ghost Button
ghostBtn=I(document, {
  type: "frame",
  name: "Button/Ghost",
  reusable: true,
  fill: "transparent"
  // ... rest
})
```

## Common Component Patterns

### Button

```javascript
button=I(document, {
  type: "frame",
  name: "Button",
  reusable: true,
  layout: "horizontal",
  padding: [12, 24, 12, 24],
  alignItems: "center",
  justifyContent: "center",
  gap: 8,
  fill: "var(colors/primary/500)",
  cornerRadius: "var(radii/md)"
})
icon=I(button, {
  type: "frame",
  name: "iconSlot",
  width: 20,
  height: 20,
  placeholder: true
})
label=I(button, {
  type: "text",
  name: "label",
  content: "Button",
  fontSize: "var(typography/fontSize/base)",
  fontWeight: "var(typography/fontWeight/medium)",
  textColor: "#FFFFFF"
})
```

### Input Field

```javascript
inputField=I(document, {
  type: "frame",
  name: "InputField",
  reusable: true,
  layout: "vertical",
  gap: 8,
  width: "fill_container"
})
label=I(inputField, {
  type: "text",
  name: "label",
  content: "Label",
  fontSize: "var(typography/fontSize/sm)",
  fontWeight: "var(typography/fontWeight/medium)"
})
input=I(inputField, {
  type: "frame",
  name: "input",
  layout: "horizontal",
  width: "fill_container",
  height: 44,
  padding: [0, 16, 0, 16],
  alignItems: "center",
  fill: "#FFFFFF",
  stroke: "var(colors/neutral/200)",
  strokeWidth: 1,
  cornerRadius: "var(radii/md)"
})
placeholder=I(input, {
  type: "text",
  name: "placeholder",
  content: "Enter value...",
  textColor: "var(colors/neutral/400)"
})
helper=I(inputField, {
  type: "text",
  name: "helperText",
  content: "",
  fontSize: "var(typography/fontSize/xs)",
  textColor: "var(colors/neutral/500)"
})
```

### Card

```javascript
card=I(document, {
  type: "frame",
  name: "Card",
  reusable: true,
  layout: "vertical",
  width: 320,
  fill: "#FFFFFF",
  cornerRadius: "var(radii/lg)",
  clipContent: true
})
media=I(card, {
  type: "frame",
  name: "mediaSlot",
  width: "fill_container",
  height: 180,
  placeholder: true
})
content=I(card, {
  type: "frame",
  name: "content",
  layout: "vertical",
  padding: 24,
  gap: 12
})
title=I(content, {
  type: "text",
  name: "title",
  content: "Card Title",
  fontSize: "var(typography/fontSize/lg)",
  fontWeight: "var(typography/fontWeight/semibold)"
})
description=I(content, {
  type: "text",
  name: "description",
  content: "Card description...",
  textColor: "var(colors/neutral/600)"
})
actions=I(card, {
  type: "frame",
  name: "actionsSlot",
  layout: "horizontal",
  padding: [0, 24, 24, 24],
  gap: 12,
  placeholder: true
})
```

## Theming

### 테마 축 정의

라이트/다크 모드 지원:

```json
{
  "themeAxes": {
    "mode": ["light", "dark"]
  },
  "colors": {
    "background": {
      "mode:light": "#FFFFFF",
      "mode:dark": "#0F172A"
    },
    "text": {
      "primary": {
        "mode:light": "#0F172A",
        "mode:dark": "#F8FAFC"
      },
      "secondary": {
        "mode:light": "#64748B",
        "mode:dark": "#94A3B8"
      }
    }
  }
}
```

### 테마 적용

```javascript
// 변수 참조 시 현재 테마 값 자동 적용
container=I("parentId", {
  type: "frame",
  fill: "var(colors/background)"
})
title=I(container, {
  type: "text",
  content: "Title",
  textColor: "var(colors/text/primary)"
})
```

## Best Practices

### Naming Conventions

- 컴포넌트: PascalCase (`Button`, `InputField`, `Card`)
- Variants: Slash 구분 (`Button/Primary`, `Button/Secondary`)
- 내부 노드: camelCase (`label`, `iconSlot`, `contentArea`)
- 변수: lowercase/슬래시 (`colors/primary/500`, `spacing/4`)

### Component Organization

1. **Primitives first**: 기본 요소부터 정의
2. **Compose up**: 작은 컴포넌트로 큰 컴포넌트 구성
3. **Single responsibility**: 하나의 역할만 담당
4. **Prop slots**: placeholder로 커스터마이징 지점 제공

### Variable Usage

1. **Consistent tokens**: 하드코딩 대신 변수 참조
2. **Semantic names**: 용도 기반 이름 (primary, danger, not blue, red)
3. **Scale systems**: 일관된 스케일 (4px 단위 스페이싱)

## Additional Resources

### Reference Files

- **`references/token-scales.md`** - 표준 토큰 스케일 정의
- **`references/component-catalog.md`** - 공통 컴포넌트 카탈로그
