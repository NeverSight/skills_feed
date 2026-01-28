---
name: testing
description: "React Testing Library 및 Vitest 기반 테스팅 모범 관례. 다음 상황에서 사용: (1) .test.tsx, .test.ts, .spec.tsx, .spec.ts 파일 작업 시, (2) 컴포넌트 테스트 작성 또는 리팩토링 시, (3) 'test', 'testing', 'vitest', 'RTL', 'getByRole', 'userEvent', 'waitFor', 'expect' 키워드 포함 작업 시, (4) 비동기 로직 또는 사용자 상호작용 테스트 작성 시"
license: MIT
metadata:
  author: DaleStudy
  version: "1.0.1"
---

# Testing Library

React Testing Library 기반 테스트 작성 모범 관례 및 안티패턴 회피 가이드.

## 핵심 원칙

Testing Library의 철학: **사용자가 사용하는 방식대로 테스트하라**

1. **접근성 기반 쿼리 우선** - 실제 사용자가 요소를 찾는 방식 사용
2. **구현 세부사항 테스트 금지** - 컴포넌트 내부 상태/메서드 직접 접근 지양
3. **실제 사용자 행동 시뮬레이션** - userEvent 사용, fireEvent 지양
4. **비동기 처리 명시적 대기** - waitFor, findBy 활용

## 쿼리 우선순위

Testing Library는 다양한 쿼리를 제공하지만, **접근성과 사용자 경험을 반영하는 순서**로 사용해야 함.

### 권장 쿼리 순서 (높음 → 낮음)

1. **`getByRole`** (최우선) - 스크린 리더가 인식하는 방식
2. **`getByLabelText`** - 폼 요소 (label과 연결된 input)
3. **`getByPlaceholderText`** - placeholder가 명확한 경우
4. **`getByText`** - 텍스트 콘텐츠로 검색
5. **`getByDisplayValue`** - 현재 입력된 값으로 검색 (폼 요소)
6. **`getByAltText`** - 이미지 alt 속성
7. **`getByTitle`** - title 속성 (tooltip 등)
8. **`getByTestId`** (최후 수단) - 다른 방법이 불가능할 때만 사용

**상세 가이드**: [references/query-priority.md](references/query-priority.md)

## 사용자 상호작용 테스트

### userEvent 사용 (권장)

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('사용자가 폼을 제출할 수 있다', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(screen.getByRole('textbox', { name: /이메일/i }), 'user@example.com');
  await user.type(screen.getByLabelText(/비밀번호/i), 'password123');
  await user.click(screen.getByRole('button', { name: /로그인/i }));

  expect(await screen.findByText(/환영합니다/i)).toBeInTheDocument();
});
```

**핵심**:

- `userEvent.setup()` 호출 후 사용
- 모든 user 메서드는 `await` 필수
- 실제 브라우저 이벤트 순서 재현 (focus, keydown, keyup 등)

### fireEvent 지양

```typescript
// ❌ 나쁜 예 - fireEvent 사용
fireEvent.click(button);
fireEvent.change(input, { target: { value: "text" } });

// ✅ 좋은 예 - userEvent 사용
await user.click(button);
await user.type(input, "text");
```

**상세 가이드**: [references/user-events.md](references/user-events.md)

## 비동기 처리

### findBy 쿼리 (권장)

```typescript
// ✅ 좋은 예 - findBy 사용
const successMessage = await screen.findByText(/저장되었습니다/i);
expect(successMessage).toBeInTheDocument();
```

`findBy` = `getBy` + `waitFor` 조합 (자동으로 요소 나타날 때까지 대기)

### waitFor 사용

```typescript
// 복잡한 비동기 검증
await waitFor(() => {
  expect(screen.getByRole("alert")).toHaveTextContent("성공");
});

// 여러 조건 검증
await waitFor(() => {
  expect(mockFn).toHaveBeenCalledTimes(1);
  expect(screen.queryByText(/로딩 중/i)).not.toBeInTheDocument();
});
```

### 안티패턴

```typescript
// ❌ 나쁜 예 - 임의의 timeout
await new Promise((resolve) => setTimeout(resolve, 1000));

// ❌ 나쁜 예 - act() 수동 사용 (보통 불필요)
await act(async () => {
  // ...
});

// ✅ 좋은 예 - findBy 또는 waitFor
await screen.findByText(/완료/i);
```

**상세 가이드**: [references/async-patterns.md](references/async-patterns.md)

## 자주 하는 실수

### 1. 구현 세부사항 테스트

```typescript
// ❌ 나쁜 예 - 내부 상태 접근
expect(component.state.isOpen).toBe(true);
wrapper.find(".internal-class").simulate("click");

// ✅ 좋은 예 - 사용자 관점 검증
expect(screen.getByRole("dialog")).toBeVisible();
await user.click(screen.getByRole("button", { name: /열기/i }));
```

### 2. container 쿼리 사용

```typescript
// ❌ 나쁜 예 - container.querySelector
const { container } = render(<MyComponent />);
const button = container.querySelector('.my-button');

// ✅ 좋은 예 - screen 쿼리
const button = screen.getByRole('button', { name: /제출/i });
```

### 3. 불필요한 waitFor

```typescript
// ❌ 나쁜 예 - 동기 요소에 waitFor
await waitFor(() => {
  expect(screen.getByText("Hello")).toBeInTheDocument();
});

// ✅ 좋은 예 - 동기 요소는 즉시 검증
expect(screen.getByText("Hello")).toBeInTheDocument();
```

**전체 안티패턴 목록**: [references/common-mistakes.md](references/common-mistakes.md)

## Vitest + MSW 설정

테스트 환경 설정이 필요한 경우 다음 템플릿 참조:

- `assets/vitest.config.ts` - Vitest 설정 (React 플러그인, 커버리지 포함)
- `assets/test-setup.ts` - Vitest 글로벌 설정
- `assets/msw-setup.ts` - MSW 핸들러 및 서버 설정
