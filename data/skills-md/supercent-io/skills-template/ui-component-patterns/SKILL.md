---
name: ui-component-patterns
description: Build reusable, maintainable UI components following modern design patterns. Use when creating component libraries, implementing design systems, or building scalable frontend architectures. Handles React patterns, composition, prop design, TypeScript, and component best practices.
tags: [UI-components, React, design-patterns, composition, TypeScript, reusable]
platforms: [Claude, ChatGPT, Gemini]
---

# UI Component Patterns


## When to use this skill

- **컴포넌트 라이브러리 구축**: 재사용 가능한 UI 컴포넌트 제작
- **디자인 시스템 구현**: 일관된 UI 패턴 적용
- **복잡한 UI**: 여러 변형이 필요한 컴포넌트 (Button, Modal, Dropdown)
- **리팩토링**: 중복 코드를 컴포넌트로 추출

## Instructions

### Step 1: Props API 설계

사용하기 쉽고 확장 가능한 Props를 설계합니다.

**원칙**:
- 명확한 이름
- 합리적인 기본값
- TypeScript로 타입 정의
- 선택적 Props는 optional (?)

**예시** (Button):
```tsx
interface ButtonProps {
  // 필수
  children: React.ReactNode;

  // 선택적 (기본값 있음)
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  isLoading?: boolean;

  // 이벤트 핸들러
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;

  // HTML 속성 상속
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  isLoading = false,
  onClick,
  type = 'button',
  className = '',
  ...rest
}: ButtonProps) {
  const baseClasses = 'btn';
  const variantClasses = `btn-${variant}`;
  const sizeClasses = `btn-${size}`;
  const classes = `${baseClasses} ${variantClasses} ${sizeClasses} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled || isLoading}
      onClick={onClick}
      {...rest}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}

// 사용 예시
<Button variant="primary" size="lg" onClick={() => alert('Clicked!')}>
  Click Me
</Button>
```

### Step 2: Composition Pattern (합성 패턴)

작은 컴포넌트를 조합하여 복잡한 UI를 만듭니다.

**예시** (Card):
```tsx
// Card 컴포넌트 (Container)
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className = '' }: CardProps) {
  return <div className={`card ${className}`}>{children}</div>;
}

// Card.Header
function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
}

// Card.Body
function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
}

// Card.Footer
function CardFooter({ children }: { children: React.ReactNode }) {
  return <div className="card-footer">{children}</div>;
}

// Compound Component 패턴
Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

export default Card;

// 사용
import Card from './Card';

function ProductCard() {
  return (
    <Card>
      <Card.Header>
        <h3>Product Name</h3>
      </Card.Header>
      <Card.Body>
        <img src="..." alt="Product" />
        <p>Product description here...</p>
      </Card.Body>
      <Card.Footer>
        <button>Add to Cart</button>
      </Card.Footer>
    </Card>
  );
}
```

### Step 3: Render Props / Children as Function

유연한 커스터마이징을 위한 패턴입니다.

**예시** (Dropdown):
```tsx
interface DropdownProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  onSelect: (item: T) => void;
  placeholder?: string;
}

function Dropdown<T>({ items, renderItem, onSelect, placeholder }: DropdownProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState<T | null>(null);

  const handleSelect = (item: T) => {
    setSelected(item);
    onSelect(item);
    setIsOpen(false);
  };

  return (
    <div className="dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>
        {selected ? renderItem(selected, -1) : placeholder || 'Select...'}
      </button>

      {isOpen && (
        <ul className="dropdown-menu">
          {items.map((item, index) => (
            <li key={index} onClick={() => handleSelect(item)}>
              {renderItem(item, index)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// 사용
interface User {
  id: string;
  name: string;
  avatar: string;
}

function UserDropdown() {
  const users: User[] = [...];

  return (
    <Dropdown
      items={users}
      placeholder="Select a user"
      renderItem={(user) => (
        <div className="user-item">
          <img src={user.avatar} alt={user.name} />
          <span>{user.name}</span>
        </div>
      )}
      onSelect={(user) => console.log('Selected:', user)}
    />
  );
}
```

### Step 4: Custom Hooks로 로직 분리

UI와 비즈니스 로직을 분리합니다.

**예시** (Modal):
```tsx
// hooks/useModal.ts
function useModal(initialOpen = false) {
  const [isOpen, setIsOpen] = useState(initialOpen);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen(prev => !prev), []);

  return { isOpen, open, close, toggle };
}

// components/Modal.tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button onClick={onClose} aria-label="Close">×</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}

// 사용
function App() {
  const { isOpen, open, close } = useModal();

  return (
    <>
      <button onClick={open}>Open Modal</button>
      <Modal isOpen={isOpen} onClose={close} title="My Modal">
        <p>Modal content here...</p>
      </Modal>
    </>
  );
}
```

### Step 5: 성능 최적화

불필요한 리렌더링을 방지합니다.

**React.memo**:
```tsx
// ❌ 나쁜 예: 부모가 리렌더링될 때마다 자식도 리렌더링
function ExpensiveComponent({ data }) {
  console.log('Rendering...');
  return <div>{/* 복잡한 UI */}</div>;
}

// ✅ 좋은 예: props가 변경될 때만 리렌더링
const ExpensiveComponent = React.memo(({ data }) => {
  console.log('Rendering...');
  return <div>{/* 복잡한 UI */}</div>;
});
```

**useMemo & useCallback**:
```tsx
function ProductList({ products, category }: { products: Product[]; category: string }) {
  // ✅ 필터링 결과 메모이제이션
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.category === category);
  }, [products, category]);

  // ✅ 콜백 메모이제이션
  const handleAddToCart = useCallback((productId: string) => {
    // 장바구니에 추가
    console.log('Adding:', productId);
  }, []);

  return (
    <div>
      {filteredProducts.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={handleAddToCart}
        />
      ))}
    </div>
  );
}

const ProductCard = React.memo(({ product, onAddToCart }) => {
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => onAddToCart(product.id)}>Add to Cart</button>
    </div>
  );
});
```

## Output format

### 컴포넌트 파일 구조

```
components/
├── Button/
│   ├── Button.tsx           # 메인 컴포넌트
│   ├── Button.test.tsx      # 테스트
│   ├── Button.stories.tsx   # Storybook
│   ├── Button.module.css    # 스타일
│   └── index.ts             # Export
├── Card/
│   ├── Card.tsx
│   ├── CardHeader.tsx
│   ├── CardBody.tsx
│   ├── CardFooter.tsx
│   └── index.ts
└── Modal/
    ├── Modal.tsx
    ├── useModal.ts          # Custom hook
    └── index.ts
```

### 컴포넌트 템플릿

```tsx
import React from 'react';

export interface ComponentProps {
  // Props 정의
  children: React.ReactNode;
  className?: string;
}

/**
 * Component description
 *
 * @example
 * ```tsx
 * <Component>Hello</Component>
 * ```
 */
export const Component = React.forwardRef<HTMLDivElement, ComponentProps>(
  ({ children, className = '', ...rest }, ref) => {
    return (
      <div ref={ref} className={`component ${className}`} {...rest}>
        {children}
      </div>
    );
  }
);

Component.displayName = 'Component';

export default Component;
```

## Constraints

### 필수 규칙 (MUST)

1. **단일 책임 원칙**: 한 컴포넌트는 하나의 역할만
   - Button은 버튼만, Form은 폼만

2. **Props 타입 정의**: TypeScript interface 필수
   - 자동완성 지원
   - 타입 안정성

3. **접근성 고려**: aria-*, role, tabindex 등

### 금지 사항 (MUST NOT)

1. **과도한 props drilling**: 5단계 이상 금지
   - Context 또는 Composition 사용

2. **비즈니스 로직 포함**: UI 컴포넌트에 API 호출, 복잡한 계산 금지
   - Custom hooks로 분리

3. **inline 객체/함수**: 성능 저하
   ```tsx
   // ❌ 나쁜 예
   <Component style={{ color: 'red' }} onClick={() => handleClick()} />

   // ✅ 좋은 예
   const style = { color: 'red' };
   const handleClick = useCallback(() => {...}, []);
   <Component style={style} onClick={handleClick} />
   ```

## Examples

### 예시 1: Accordion (Compound Component)

```tsx
import React, { createContext, useContext, useState } from 'react';

// Context로 상태 공유
const AccordionContext = createContext<{
  activeIndex: number | null;
  setActiveIndex: (index: number | null) => void;
} | null>(null);

function Accordion({ children }: { children: React.ReactNode }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  return (
    <AccordionContext.Provider value={{ activeIndex, setActiveIndex }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ index, title, children }: {
  index: number;
  title: string;
  children: React.ReactNode;
}) {
  const context = useContext(AccordionContext);
  if (!context) throw new Error('AccordionItem must be used within Accordion');

  const { activeIndex, setActiveIndex } = context;
  const isActive = activeIndex === index;

  return (
    <div className="accordion-item">
      <button
        className="accordion-header"
        onClick={() => setActiveIndex(isActive ? null : index)}
        aria-expanded={isActive}
      >
        {title}
      </button>
      {isActive && <div className="accordion-body">{children}</div>}
    </div>
  );
}

Accordion.Item = AccordionItem;
export default Accordion;

// 사용
<Accordion>
  <Accordion.Item index={0} title="Section 1">
    Content for section 1
  </Accordion.Item>
  <Accordion.Item index={1} title="Section 2">
    Content for section 2
  </Accordion.Item>
</Accordion>
```

### 예시 2: Polymorphic Component (as prop)

```tsx
type PolymorphicComponentProps<C extends React.ElementType> = {
  as?: C;
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<C>;

function Text<C extends React.ElementType = 'span'>({
  as,
  children,
  ...rest
}: PolymorphicComponentProps<C>) {
  const Component = as || 'span';
  return <Component {...rest}>{children}</Component>;
}

// 사용
<Text>Default span</Text>
<Text as="h1">Heading 1</Text>
<Text as="p" style={{ color: 'blue' }}>Paragraph</Text>
<Text as={Link} href="/about">Link</Text>
```

## Best practices

1. **Composition over Props**: 많은 props 대신 children 활용
2. **Controlled vs Uncontrolled**: 상황에 맞게 선택
3. **Default Props**: 합리적인 기본값 제공
4. **Storybook**: 컴포넌트 문서화 및 개발

## References

- [React Patterns](https://reactpatterns.com/)
- [Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)
- [Radix UI](https://www.radix-ui.com/) - Accessible components
- [Chakra UI](https://chakra-ui.com/) - Component library
- [shadcn/ui](https://ui.shadcn.com/) - Copy-paste components

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [web-accessibility](../web-accessibility/SKILL.md): 접근 가능한 컴포넌트
- [state-management](../state-management/SKILL.md): 컴포넌트 상태 관리

### 태그
`#UI-components` `#React` `#design-patterns` `#composition` `#TypeScript` `#frontend`