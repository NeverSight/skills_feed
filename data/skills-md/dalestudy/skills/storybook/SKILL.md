---
name: storybook
description: "Storybook 스토리 작성 및 CSF 3.0 베스트 프랙티스 스킬. 다음 상황에서 사용: (1) 새 스토리 파일(.stories.tsx, .stories.ts) 작성 시, (2) 기존 스토리 수정 시, (3) Args, Decorators, Parameters 설정 시, (4) Storybook 설정 파일(.storybook/) 작업 시, (5) 'story', 'stories', 'storybook', 'CSF' 키워드가 포함된 작업 시"
license: MIT
metadata:
  author: DaleStudy
  version: "1.0"
---

# Storybook

## 모범 관례

### 1. CSF 3.0 형식 사용

최신 Component Story Format 3.0 사용. 더 간결하고 타입 안전.

```tsx
// ❌ CSF 2.0 (구형)
export default {
  title: 'Components/Button',
  component: Button,
};

export const Primary = () => <Button variant="primary">Click me</Button>;

// ✅ CSF 3.0 (권장)
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'], // 자동 문서 생성
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
};
```

### 2. Args 기반 스토리 작성

컴포넌트 Props를 Args로 정의하여 Controls 패널에서 인터랙티브하게 조작 가능.

```tsx
// ❌ 하드코딩된 Props
export const Disabled: Story = {
  render: () => <Button disabled>Disabled</Button>,
};

// ✅ Args 사용
export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
};

// ✅ Args 재사용 및 오버라이드
export const DisabledPrimary: Story = {
  args: {
    ...Primary.args,
    disabled: true,
  },
};
```

### 3. 타입 안전한 Meta 정의

`satisfies` 키워드로 타입 체크와 타입 추론 동시 활용.

```tsx
// ❌ 타입 추론 불가
const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
};

// ✅ 타입 체크와 추론 모두 가능
const meta = {
  title: 'Components/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary'],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;
```

### 4. Decorators로 컨텍스트 제공

공통 래퍼나 Provider를 Decorator로 적용.

```tsx
// 개별 스토리에 Decorator 적용
export const WithTheme: Story = {
  decorators: [
    (Story) => (
      <ThemeProvider theme="dark">
        <Story />
      </ThemeProvider>
    ),
  ],
};

// 모든 스토리에 Decorator 적용
const meta = {
  component: Button,
  decorators: [
    (Story) => (
      <div style={{ padding: '3rem' }}>
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Button>;
```

### 5. Parameters로 동작 커스터마이즈

```tsx
const meta = {
  component: Button,
  parameters: {
    layout: 'centered', // 스토리를 중앙 정렬
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#000000' },
      ],
    },
  },
} satisfies Meta<typeof Button>;

// 개별 스토리에서 오버라이드
export const OnDark: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
  },
};
```

### 6. ArgTypes로 Controls 세밀하게 제어

```tsx
const meta = {
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary'],
      description: '버튼 스타일 변형',
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
    onClick: {
      action: 'clicked', // Actions 패널에 표시
    },
    children: {
      control: 'text',
    },
    disabled: {
      control: 'boolean',
    },
  },
} satisfies Meta<typeof Button>;
```

## 권장 스토리 구조

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

// 1. Meta 정의
const meta = {
  title: 'Components/Button', // 사이드바 계층 구조
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary'],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// 2. 기본 스토리
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};

// 3. 변형 스토리들
export const Secondary: Story = {
  args: {
    ...Primary.args,
    variant: 'secondary',
  },
};

export const Disabled: Story = {
  args: {
    ...Primary.args,
    disabled: true,
  },
};

// 4. 복잡한 상태나 컨텍스트가 필요한 경우
export const WithCustomTheme: Story = {
  args: Primary.args,
  decorators: [
    (Story) => (
      <ThemeProvider theme="custom">
        <Story />
      </ThemeProvider>
    ),
  ],
};
```

## 자주 사용되는 ArgTypes 옵션

```tsx
argTypes: {
  // Select dropdown
  variant: {
    control: 'select',
    options: ['primary', 'secondary'],
  },

  // Radio buttons
  size: {
    control: 'radio',
    options: ['sm', 'md', 'lg'],
  },

  // Boolean toggle
  disabled: {
    control: 'boolean',
  },

  // Text input
  label: {
    control: 'text',
  },

  // Number input
  count: {
    control: 'number',
  },

  // Range slider
  opacity: {
    control: { type: 'range', min: 0, max: 1, step: 0.1 },
  },

  // Color picker
  backgroundColor: {
    control: 'color',
  },

  // Date picker
  date: {
    control: 'date',
  },

  // Action logger (이벤트 핸들러)
  onClick: {
    action: 'clicked',
  },

  // Control 비활성화
  className: {
    control: false,
  },
}
```

## 자주 사용되는 Parameters

```tsx
parameters: {
  // 레이아웃 설정
  layout: 'centered' | 'fullscreen' | 'padded',

  // 배경 설정
  backgrounds: {
    default: 'light',
    values: [
      { name: 'light', value: '#ffffff' },
      { name: 'dark', value: '#333333' },
    ],
  },

  // Actions 패널 설정
  actions: {
    argTypesRegex: '^on[A-Z].*', // on으로 시작하는 Props 자동 감지
  },

  // Docs 설정
  docs: {
    description: {
      component: '버튼 컴포넌트 상세 설명',
    },
  },
}
```

## Decorators 패턴

```tsx
// 1. 스타일 래퍼
(Story) => (
  <div style={{ padding: '3rem' }}>
    <Story />
  </div>
)

// 2. Theme Provider
(Story) => (
  <ThemeProvider theme="dark">
    <Story />
  </ThemeProvider>
)

// 3. Router Provider (React Router 사용 시)
(Story) => (
  <MemoryRouter initialEntries={['/']}>
    <Story />
  </MemoryRouter>
)

// 4. 다국어 Provider
(Story) => (
  <I18nProvider locale="ko">
    <Story />
  </I18nProvider>
)

// 5. 전역 상태 Provider
(Story) => (
  <Provider store={mockStore}>
    <Story />
  </Provider>
)
```

## 파일 명명 규칙

```
Component.tsx           # 컴포넌트 구현
Component.stories.tsx   # 스토리 파일 (같은 디렉토리)
Component.test.tsx      # 테스트 파일
```

## Storybook 설정 파일

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-essentials', // Controls, Actions, Docs 등
    '@storybook/addon-interactions', // Play functions
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
};

export default config;
```

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
  // 모든 스토리에 적용될 전역 Decorators
  decorators: [
    (Story) => (
      <div style={{ fontFamily: 'Arial, sans-serif' }}>
        <Story />
      </div>
    ),
  ],
};

export default preview;
```
