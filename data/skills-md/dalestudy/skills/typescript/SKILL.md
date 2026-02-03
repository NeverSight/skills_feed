---
name: typescript
description: "TypeScript 타입 정의 및 베스트 프랙티스 스킬. 다음 상황에서 사용: (1) TypeScript 파일(.ts, .tsx) 작성 또는 수정 시, (2) 타입 정의(interface, type) 작업 시, (3) tsconfig.json 설정 또는 컴파일러 옵션 조정 시, (4) 타입 에러 해결 또는 타입 안전성 개선 시, (5) 제네릭, 유틸리티 타입, 타입 조작 작업 시, (6) 'typescript', 'ts', 'type', 'interface', 'generic' 키워드가 포함된 작업 시"
license: MIT
compatibility: Requires TypeScript compiler (tsc)
metadata:
  author: DaleStudy
  version: "1.0.0"
---

# TypeScript

TypeScript 핸드북 기반 타입 정의 및 베스트 프랙티스. 기본 문법·타입 조작·유틸리티 타입 상세는 [references/](references/) 및 [Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) 참고.

## 기본 원칙

### 1. 타입 추론 활용

불필요한 어노테이션 생략. 변경 시 이중 수정 부담 감소, 추론이 더 정확한 경우 많음.

```typescript
// ❌
const name: string = "John";
const user: { name: string; age: number } = { name: "John", age: 30 };

// ✅
const name = "John";
const user = { name: "John", age: 30 };
```

### 2. 명시적 반환 타입

함수 계약 명확화, 반환 타입 오변경 방지. 공개 API·복잡한 로직에서 필수.

```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}
```

### 3. any 사용 금지

타입 안전성·자동완성 무효화. `unknown` + 타입 가드 또는 구체 타입 사용.

```typescript
// ❌
function process(data: any) {
  return data.value;
}

// ✅
function process(data: unknown): number {
  if (typeof data === "object" && data !== null && "value" in data)
    return (data as { value: number }).value;
  throw new Error("Invalid data");
}
```

## 함수 · 제네릭

- 함수: 인자·반환 타입 명시. 오버로드 시 구현 시그니처는 유니온으로.
- 제네릭: `T`, `K extends keyof T` 등 제약 명시. `getProperty<T, K extends keyof T>(obj: T, key: K): T[K]` 패턴 활용.

## 타입 가드

- `typeof`, `instanceof`, `in`으로 분기 후 타입 좁히기
- 복잡한 검사는 사용자 정의 가드 `(value): value is T` 사용

> 템플릿: `assets/types.guards.ts`

## tsconfig

- 프로젝트 성격에 맞는 tsconfig를 사용
- 타입 안정성을 해치지 않는 선에서만 옵션을 조정
- 앱/서버/라이브러리는 설정 파일을 분리
- 타입 에러 회피 목적의 옵션 완화 금지

> 템플릿:
>
> - `assets/tsconfig.nextjs.ts`
> - `assets/tsconfig.node.ts`
> - `assets/tsconfig.react.ts`

## 이벤트 타입

- DOM / React 이벤트는 내장 타입 사용
- 커스텀 이벤트만 별도 타입 정의
- 이벤트 재정의 금지

> 템플릿: `assets/types.events.ts`

## 유틸리티 타입

- TypeScript 내장 유틸리티 타입은 그대로 사용
- 커스텀 유틸리티 타입만 정의

> 템플릿: `assets/types.utils.ts`

## 실전 패턴

- **interface 우선**: 객체 계약·확장은 `interface`, 유니온/인터섹션은 `type`. API 설명은 명사형으로 작성 (`/** 비활성화 상태 */`).
- **`as const`**: 리터럴·객체 불변 보존. `typeof obj[keyof typeof obj]` 로 이넘처럼 활용.
- **브랜드 타입**: `type UserId = string & { readonly brand: unique symbol }` 로 동일 원시 타입 구분.
- **타입 단언 최소화**: `as` 대신 타입 가드.
- **제네릭 제약**: `T extends object` 등 명시.

## 타입 에러 해결

| 에러                                                              | 대응                           |
| ----------------------------------------------------------------- | ------------------------------ |
| `Type 'X' is not assignable to type 'Y'`                          | 타입 가드로 분기 후 할당       |
| `Property 'X' does not exist on type 'Y'`                         | 타입 확장 또는 `optional`      |
| `Object is possibly 'null' or 'undefined'`                        | `if (x == null)` / `?.` / `??` |
| `Argument of type 'X' is not assignable to parameter of type 'Y'` | 제네릭 `T[]` 또는 오버로드     |
| `Type 'X' cannot be used as an index type`                        | `keyof typeof obj` 사용        |

디버깅: 호버로 추론 확인, 가드·제네릭·유틸리티 타입으로 해결 후 `as`는 최후 수단.

## 참고

> 이 문서들은 규칙이 아니라 참고용, 판단 기준은 각 skill 문서를 우선

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) - TypeScript 공식 개념·타입 시스템 레퍼런스
- [Playground](https://www.typescriptlang.org/play) - 타입 동작 실험 및 예제 검증용
