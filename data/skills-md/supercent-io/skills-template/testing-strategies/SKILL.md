---
name: testing-strategies
description: Design comprehensive testing strategies for software quality assurance. Use when planning test coverage, implementing test pyramids, or setting up testing infrastructure. Handles unit testing, integration testing, E2E testing, TDD, and testing best practices.
tags: [testing, test-strategy, TDD, unit-test, integration-test, E2E, test-pyramid]
platforms: [Claude, ChatGPT, Gemini]
---

# Testing Strategies


## When to use this skill

- **신규 프로젝트**: 테스트 전략 수립
- **품질 문제**: 버그 빈번히 발생
- **리팩토링 전**: 안전망 구축
- **CI/CD 구축**: 자동화된 테스트

## Instructions

### Step 1: Test Pyramid 이해

```
       /\
      /E2E\          ← 적음 (느림, 비용 높음)
     /______\
    /        \
   /Integration\    ← 중간
  /____________\
 /              \
/   Unit Tests   \  ← 많음 (빠름, 비용 낮음)
/________________\
```

**비율 가이드**:
- Unit: 70%
- Integration: 20%
- E2E: 10%

### Step 2: Unit Testing 전략

**Given-When-Then 패턴**:
```typescript
describe('calculateDiscount', () => {
  it('should apply 10% discount for orders over $100', () => {
    // Given: 주어진 상황
    const order = { total: 150, customerId: '123' };

    // When: 행동을 실행
    const discount = calculateDiscount(order);

    // Then: 결과 검증
    expect(discount).toBe(15);
  });

  it('should not apply discount for orders under $100', () => {
    const order = { total: 50, customerId: '123' };
    const discount = calculateDiscount(order);
    expect(discount).toBe(0);
  });

  it('should throw error for invalid order', () => {
    const order = { total: -10, customerId: '123' };
    expect(() => calculateDiscount(order)).toThrow('Invalid order');
  });
});
```

**Mocking 전략**:
```typescript
// 외부 의존성 모킹
jest.mock('../services/emailService');
import { sendEmail } from '../services/emailService';

describe('UserService', () => {
  it('should send welcome email on registration', async () => {
    // Arrange
    const mockSendEmail = sendEmail as jest.MockedFunction<typeof sendEmail>;
    mockSendEmail.mockResolvedValueOnce(true);

    // Act
    await userService.register({ email: 'test@example.com', password: 'pass' });

    // Assert
    expect(mockSendEmail).toHaveBeenCalledWith({
      to: 'test@example.com',
      subject: 'Welcome!',
      body: expect.any(String)
    });
  });
});
```

### Step 3: Integration Testing

**API 엔드포인트 테스트**:
```typescript
describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.user.deleteMany();  // Clean DB
  });

  it('should create user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        username: 'testuser',
        password: 'Password123!'
      });

    expect(response.status).toBe(201);
    expect(response.body.user).toMatchObject({
      email: 'test@example.com',
      username: 'testuser'
    });

    // DB에 실제로 저장되었는지 확인
    const user = await db.user.findUnique({ where: { email: 'test@example.com' } });
    expect(user).toBeTruthy();
  });

  it('should reject duplicate email', async () => {
    // 첫 번째 사용자 생성
    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', username: 'user1', password: 'Pass123!' });

    // 중복 시도
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', username: 'user2', password: 'Pass123!' });

    expect(response.status).toBe(409);
  });
});
```

### Step 4: E2E Testing (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should complete full registration process', async ({ page }) => {
    // 1. 홈페이지 방문
    await page.goto('http://localhost:3000');

    // 2. 회원가입 버튼 클릭
    await page.click('text=Sign Up');

    // 3. 폼 작성
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'Password123!');

    // 4. 제출
    await page.click('button[type="submit"]');

    // 5. 성공 메시지 확인
    await expect(page.locator('text=Welcome')).toBeVisible();

    // 6. 대시보드로 리다이렉트 확인
    await expect(page).toHaveURL('http://localhost:3000/dashboard');

    // 7. 사용자 정보 표시 확인
    await expect(page.locator('text=testuser')).toBeVisible();
  });

  test('should show error for invalid email', async ({ page }) => {
    await page.goto('http://localhost:3000/signup');
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Invalid email')).toBeVisible();
  });
});
```

### Step 5: TDD (Test-Driven Development)

**Red-Green-Refactor Cycle**:

```typescript
// 1. RED: 실패하는 테스트 작성
describe('isPalindrome', () => {
  it('should return true for palindrome', () => {
    expect(isPalindrome('racecar')).toBe(true);
  });
});

// 2. GREEN: 테스트 통과하는 최소 코드
function isPalindrome(str: string): boolean {
  return str === str.split('').reverse().join('');
}

// 3. REFACTOR: 코드 개선
function isPalindrome(str: string): boolean {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  return cleaned === cleaned.split('').reverse().join('');
}

// 4. 추가 테스트 케이스
it('should ignore case and spaces', () => {
  expect(isPalindrome('A man a plan a canal Panama')).toBe(true);
});

it('should return false for non-palindrome', () => {
  expect(isPalindrome('hello')).toBe(false);
});
```

## Output format

### 테스트 전략 문서

```markdown
## Testing Strategy

### Coverage Goals
- Unit Tests: 80%
- Integration Tests: 60%
- E2E Tests: Critical user flows

### Test Execution
- Unit: Every commit (local + CI)
- Integration: Every PR
- E2E: Before deployment

### Tools
- Unit: Jest
- Integration: Supertest
- E2E: Playwright
- Coverage: Istanbul/nyc

### CI/CD Integration
- GitHub Actions: Run all tests on PR
- Fail build if coverage < 80%
- E2E tests on staging environment
```

## Constraints

### 필수 규칙 (MUST)

1. **테스트 격리**: 각 테스트는 독립적
2. **Fast Feedback**: Unit tests는 빠르게 (<1분)
3. **Deterministic**: 같은 입력 → 같은 결과

### 금지 사항 (MUST NOT)

1. **테스트 의존성**: 테스트 A가 테스트 B에 의존 금지
2. **프로덕션 DB**: 테스트에서 실제 DB 사용 금지
3. **Sleep/Timeout**: 시간 기반 테스트 지양

## Best practices

1. **AAA 패턴**: Arrange-Act-Assert
2. **테스트 이름**: "should ... when ..."
3. **Edge Cases**: 경계값, null, 빈 값 테스트
4. **Happy Path + Sad Path**: 성공/실패 시나리오 모두

## References

- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Jest](https://jestjs.io/)
- [Playwright](https://playwright.dev/)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [backend-testing](../../backend/testing/SKILL.md)
- [code-review](../code-review/SKILL.md)

### 태그
`#testing` `#test-strategy` `#TDD` `#unit-test` `#integration-test` `#E2E` `#code-quality`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
