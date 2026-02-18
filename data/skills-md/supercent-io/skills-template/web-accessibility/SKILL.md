---
name: web-accessibility
description: Implement web accessibility (a11y) standards following WCAG 2.1 guidelines. Use when building accessible UIs, fixing accessibility issues, or ensuring compliance with disability standards. Handles ARIA attributes, keyboard navigation, screen readers, semantic HTML, and accessibility testing.
tags: [accessibility, a11y, WCAG, ARIA, semantic-HTML, screen-reader]
platforms: [Claude, ChatGPT, Gemini]
---

# Web Accessibility (A11y)


## When to use this skill

- **새 UI 컴포넌트 개발**: 접근 가능한 컴포넌트 설계
- **접근성 감사**: 기존 사이트의 접근성 문제 식별 및 수정
- **폼 구현**: 스크린 리더 친화적인 폼 작성
- **모달/드롭다운**: 포커스 관리 및 키보드 트랩 방지
- **WCAG 준수**: 법적 요구사항 또는 표준 준수

## 입력 형식 (Input Format)

### 필수 정보
- **프레임워크**: React, Vue, Svelte, Vanilla JS 등
- **컴포넌트 유형**: Button, Form, Modal, Dropdown, Navigation 등
- **WCAG 레벨**: A, AA, AAA (기본값: AA)

### 선택 정보
- **스크린 리더**: NVDA, JAWS, VoiceOver (테스트용)
- **자동 테스트 도구**: axe-core, Pa11y, Lighthouse (기본값: axe-core)
- **브라우저**: Chrome, Firefox, Safari (기본값: Chrome)

### 입력 예시

```
React 모달 컴포넌트를 접근 가능하게 만들어줘:
- 프레임워크: React + TypeScript
- WCAG 레벨: AA
- 요구사항:
  - 포커스 트랩 (모달 내부에만 포커스)
  - ESC 키로 닫기
  - 배경 클릭으로 닫기
  - 스크린 리더에서 제목/설명 읽기
```

## Instructions

### Step 1: Semantic HTML 사용

의미있는 HTML 요소를 사용하여 구조를 명확히 합니다.

**작업 내용**:
- `<button>`, `<nav>`, `<main>`, `<header>`, `<footer>` 등 시맨틱 태그 사용
- `<div>`, `<span>` 남용 지양
- 제목 계층 구조 (`<h1>` ~ `<h6>`) 올바르게 사용
- `<label>`과 `<input>` 연결

**예시** (❌ 나쁜 예 vs ✅ 좋은 예):
```html
<!-- ❌ 나쁜 예: div와 span만 사용 -->
<div class="header">
  <span class="title">My App</span>
  <div class="nav">
    <div class="nav-item" onclick="navigate()">Home</div>
    <div class="nav-item" onclick="navigate()">About</div>
  </div>
</div>

<!-- ✅ 좋은 예: 시맨틱 HTML -->
<header>
  <h1>My App</h1>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>
```

**폼 예시**:
```html
<!-- ❌ 나쁜 예: label 없음 -->
<input type="text" placeholder="Enter your name">

<!-- ✅ 좋은 예: label 연결 -->
<label for="name">Name:</label>
<input type="text" id="name" name="name" required>

<!-- 또는 label로 감싸기 -->
<label>
  Email:
  <input type="email" name="email" required>
</label>
```

### Step 2: 키보드 네비게이션 구현

마우스 없이도 모든 기능 사용 가능하도록 합니다.

**작업 내용**:
- Tab, Shift+Tab으로 포커스 이동
- Enter/Space로 버튼 활성화
- 화살표 키로 리스트/메뉴 탐색
- ESC로 모달/드롭다운 닫기
- `tabindex` 적절히 사용

**판단 기준**:
- 인터랙티브 요소 → `tabindex="0"` (포커스 가능)
- 포커스 제외 → `tabindex="-1"` (프로그래밍 방식 포커스만)
- 포커스 순서 변경 금지 → `tabindex="1+"` 사용 지양

**예시** (React 드롭다운):
```typescript
import React, { useState, useRef, useEffect } from 'react';

interface DropdownProps {
  label: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}

function AccessibleDropdown({ label, options, onChange }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  // 키보드 핸들러
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setSelectedIndex((prev) => (prev + 1) % options.length);
        }
        break;

      case 'ArrowUp':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setSelectedIndex((prev) => (prev - 1 + options.length) % options.length);
        }
        break;

      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen) {
          onChange(options[selectedIndex].value);
          setIsOpen(false);
          buttonRef.current?.focus();
        } else {
          setIsOpen(true);
        }
        break;

      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
    }
  };

  return (
    <div className="dropdown">
      <button
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-labelledby="dropdown-label"
      >
        {label}
      </button>

      {isOpen && (
        <ul
          ref={listRef}
          role="listbox"
          aria-labelledby="dropdown-label"
          onKeyDown={handleKeyDown}
          tabIndex={-1}
        >
          {options.map((option, index) => (
            <li
              key={option.value}
              role="option"
              aria-selected={index === selectedIndex}
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Step 3: ARIA 속성 추가

스크린 리더에게 추가 컨텍스트를 제공합니다.

**작업 내용**:
- `aria-label`: 요소의 이름 정의
- `aria-labelledby`: 다른 요소를 라벨로 참조
- `aria-describedby`: 추가 설명 제공
- `aria-live`: 동적 콘텐츠 변경 알림
- `aria-hidden`: 스크린 리더에서 숨기기

**확인 사항**:
- [x] 모든 인터랙티브 요소에 명확한 라벨
- [x] 버튼 목적이 명확 (예: "Submit form" not "Click")
- [x] 상태 변화 알림 (aria-live)
- [x] 장식용 이미지는 alt="" 또는 aria-hidden="true"

**예시** (모달):
```tsx
function AccessibleModal({ isOpen, onClose, title, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  // 모달 열릴 때 포커스 트랩
  useEffect(() => {
    if (isOpen) {
      modalRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
      ref={modalRef}
      tabIndex={-1}
      onKeyDown={(e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      }}
    >
      <div className="modal-overlay" onClick={onClose} aria-hidden="true" />

      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        <div id="modal-description">
          {children}
        </div>

        <button onClick={onClose} aria-label="Close modal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
    </div>
  );
}
```

**aria-live 예시** (알림):
```tsx
function Notification({ message, type }: { message: string; type: 'success' | 'error' }) {
  return (
    <div
      role="alert"
      aria-live="assertive"  // 즉시 알림 (error), "polite"는 순서대로 알림
      aria-atomic="true"     // 전체 내용 읽기
      className={`notification notification-${type}`}
    >
      {type === 'error' && <span aria-label="Error">⚠️</span>}
      {type === 'success' && <span aria-label="Success">✅</span>}
      {message}
    </div>
  );
}
```

### Step 4: 색상 대비 및 시각적 접근성

시각 장애인을 위한 충분한 대비율을 보장합니다.

**작업 내용**:
- WCAG AA: 텍스트 4.5:1, 큰 텍스트 3:1
- WCAG AAA: 텍스트 7:1, 큰 텍스트 4.5:1
- 색상만으로 정보 전달 금지 (아이콘, 패턴 병행)
- 포커스 표시 명확히 (outline)

**예시** (CSS):
```css
/* ✅ 충분한 대비 (텍스트 #000 on #FFF = 21:1) */
.button {
  background-color: #0066cc;
  color: #ffffff;  /* 대비율 7.7:1 */
}

/* ✅ 포커스 표시 */
button:focus,
a:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

/* ❌ outline: none 금지! */
button:focus {
  outline: none;  /* 절대 사용 금지 */
}

/* ✅ 색상 + 아이콘으로 상태 표시 */
.error-message {
  color: #d32f2f;
  border-left: 4px solid #d32f2f;
}

.error-message::before {
  content: '⚠️';
  margin-right: 8px;
}
```

### Step 5: 접근성 테스트

자동 및 수동 테스트로 접근성을 검증합니다.

**작업 내용**:
- axe DevTools로 자동 스캔
- Lighthouse Accessibility 점수 확인
- 키보드만으로 전체 기능 테스트
- 스크린 리더 테스트 (NVDA, VoiceOver)

**예시** (Jest + axe-core):
```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import AccessibleButton from './AccessibleButton';

expect.extend(toHaveNoViolations);

describe('AccessibleButton', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <AccessibleButton onClick={() => {}}>
        Click Me
      </AccessibleButton>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should be keyboard accessible', () => {
    const handleClick = jest.fn();
    const { getByRole } = render(
      <AccessibleButton onClick={handleClick}>
        Click Me
      </AccessibleButton>
    );

    const button = getByRole('button');

    // Enter 키
    button.focus();
    fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalled();

    // Space 키
    fireEvent.keyDown(button, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(2);
  });
});
```

## Output format

### 기본 체크리스트

```markdown
## Accessibility Checklist

### Semantic HTML
- [x] 시맨틱 HTML 태그 사용 (`<button>`, `<nav>`, `<main>` 등)
- [x] 제목 계층 구조 올바름 (h1 → h2 → h3)
- [x] 폼 라벨 모두 연결됨

### Keyboard Navigation
- [x] Tab으로 모든 인터랙티브 요소 접근 가능
- [x] Enter/Space로 버튼 활성화
- [x] ESC로 모달/드롭다운 닫기
- [x] 포커스 표시 명확 (outline)

### ARIA
- [x] `role` 적절히 사용
- [x] `aria-label` 또는 `aria-labelledby` 제공
- [x] 동적 콘텐츠에 `aria-live` 사용
- [x] 장식용 요소 `aria-hidden="true"`

### Visual
- [x] 색상 대비 WCAG AA 준수 (4.5:1)
- [x] 색상만으로 정보 전달 안 함
- [x] 텍스트 크기 조절 가능
- [x] 반응형 디자인

### Testing
- [x] axe DevTools 위반 사항 0
- [x] Lighthouse Accessibility 90+ 점수
- [x] 키보드 테스트 통과
- [x] 스크린 리더 테스트 완료
```

## Constraints

### 필수 규칙 (MUST)

1. **키보드 접근성**: 모든 기능은 마우스 없이 사용 가능해야 함
   - Tab, Enter, Space, 화살표, ESC 지원
   - 포커스 트랩 구현 (모달)

2. **대체 텍스트**: 모든 이미지에 `alt` 속성
   - 의미 있는 이미지: 설명적 alt text
   - 장식용 이미지: `alt=""` (스크린 리더 무시)

3. **명확한 라벨**: 모든 폼 입력에 연결된 라벨
   - `<label for="...">` 또는 `aria-label`
   - 플레이스홀더만으로 라벨 대체 금지

### 금지 사항 (MUST NOT)

1. **outline 제거 금지**: `outline: none` 절대 사용 금지
   - 키보드 사용자에게 치명적
   - 커스텀 포커스 스타일 제공 필요

2. **tabindex > 0 사용 금지**: 포커스 순서 변경 지양
   - DOM 순서를 논리적으로 유지
   - 예외: 특별한 이유가 있는 경우만

3. **색상만으로 정보 전달 금지**: 아이콘, 텍스트 병행
   - 색맹 사용자 고려
   - 예: "빨간색 항목 클릭" → "⚠️ Error 항목 클릭"

## Examples

### 예시 1: 접근 가능한 폼

```tsx
function AccessibleContactForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h2 id="form-title">Contact Us</h2>
      <p id="form-description">Please fill out the form below to get in touch.</p>

      {/* 이름 */}
      <div className="form-group">
        <label htmlFor="name">
          Name <span aria-label="required">*</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          required
          aria-required="true"
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? 'name-error' : undefined}
        />
        {errors.name && (
          <span id="name-error" role="alert" className="error">
            {errors.name}
          </span>
        )}
      </div>

      {/* 이메일 */}
      <div className="form-group">
        <label htmlFor="email">
          Email <span aria-label="required">*</span>
        </label>
        <input
          type="email"
          id="email"
          name="email"
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : 'email-hint'}
        />
        <span id="email-hint" className="hint">
          We'll never share your email.
        </span>
        {errors.email && (
          <span id="email-error" role="alert" className="error">
            {errors.email}
          </span>
        )}
      </div>

      {/* 제출 버튼 */}
      <button type="submit" disabled={submitStatus === 'loading'}>
        {submitStatus === 'loading' ? 'Submitting...' : 'Submit'}
      </button>

      {/* 성공/실패 메시지 */}
      {submitStatus === 'success' && (
        <div role="alert" aria-live="polite" className="success">
          ✅ Form submitted successfully!
        </div>
      )}

      {submitStatus === 'error' && (
        <div role="alert" aria-live="assertive" className="error">
          ⚠️ An error occurred. Please try again.
        </div>
      )}
    </form>
  );
}
```

### 예시 2: 접근 가능한 탭 UI

```tsx
function AccessibleTabs({ tabs }: { tabs: { id: string; label: string; content: React.ReactNode }[] }) {
  const [activeTab, setActiveTab] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        setActiveTab((index + 1) % tabs.length);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        setActiveTab((index - 1 + tabs.length) % tabs.length);
        break;
      case 'Home':
        e.preventDefault();
        setActiveTab(0);
        break;
      case 'End':
        e.preventDefault();
        setActiveTab(tabs.length - 1);
        break;
    }
  };

  return (
    <div>
      {/* Tab List */}
      <div role="tablist" aria-label="Content sections">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === index}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === index ? 0 : -1}
            onClick={() => setActiveTab(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {tabs.map((tab, index) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== index}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

## Best practices

1. **시맨틱 HTML 우선**: ARIA는 마지막 수단
   - 올바른 HTML 요소 사용하면 ARIA 불필요
   - 예: `<button>` vs `<div role="button">`

2. **포커스 관리**: SPA에서 페이지 전환 시 포커스 관리
   - 새 페이지 로드 시 메인 콘텐츠로 포커스 이동
   - Skip links 제공 ("Skip to main content")

3. **에러 메시지**: 명확하고 도움이 되는 에러 메시지
   - "Invalid input" ❌ → "Email must be in format: example@domain.com" ✅

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- [WebAIM](https://webaim.org/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [A11y Project](https://www.a11yproject.com/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [ui-component-patterns](../ui-component-patterns/SKILL.md): UI 컴포넌트 구현
- [responsive-design](../responsive-design/SKILL.md): 반응형 디자인

### 태그
`#accessibility` `#a11y` `#WCAG` `#ARIA` `#screen-reader` `#keyboard-navigation` `#frontend`