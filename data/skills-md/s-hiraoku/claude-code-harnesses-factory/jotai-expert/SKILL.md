---
name: jotai-expert
description: |
  Jotai状態管理ライブラリのエキスパートスキル。Reactアプリケーションでのatomベースの状態管理を実装する際に使用。以下の場合にこのスキルを使用:
  (1) Jotaiのatom設計・実装
  (2) 派生atom、非同期atom、atomFamilyの実装
  (3) Jotaiのベストプラクティスに基づくリファクタリング
  (4) パフォーマンス最適化（selectAtom、splitAtom等）
  (5) 永続化（localStorage/sessionStorage連携）
  (6) TypeScript型定義
  (7) テスト実装
  ユーザーが「Jotai」「atom」「状態管理」に関する質問や実装依頼をした場合に発動。
---

# Jotai Expert

Jotaiを使用したReact状態管理の実装ガイド。

## Core Concepts

### Atom

状態の最小単位。値を持たず、Storeに保存される。

```typescript
// Primitive atom
const countAtom = atom(0)
const nameAtom = atom('')

// Derived read-only atom
const doubleAtom = atom((get) => get(countAtom) * 2)

// Derived read-write atom
const countWithLabelAtom = atom(
  (get) => `Count: ${get(countAtom)}`,
  (get, set, newValue: number) => set(countAtom, newValue)
)

// Write-only atom (action atom)
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1)
})
```

### Hooks

```typescript
// Read and write
const [value, setValue] = useAtom(countAtom)

// Read only
const value = useAtomValue(countAtom)

// Write only
const setValue = useSetAtom(countAtom)
```

## Implementation Patterns

### Pattern 1: Feature Module

```typescript
// atoms/user.ts
const baseUserAtom = atom<User | null>(null)

// Public read-only atom
export const userAtom = atom((get) => get(baseUserAtom))

// Actions
export const setUserAtom = atom(null, (get, set, user: User) => {
  set(baseUserAtom, user)
})

export const clearUserAtom = atom(null, (get, set) => {
  set(baseUserAtom, null)
})
```

### Pattern 2: Async Data Fetching

```typescript
const userIdAtom = atom<number | null>(null)

// Suspenseと連携する非同期atom
const userDataAtom = atom(async (get) => {
  const userId = get(userIdAtom)
  if (!userId) return null
  const response = await fetch(`/api/users/${userId}`)
  return response.json()
})

// Component
function UserProfile() {
  const userData = useAtomValue(userDataAtom)
  return <div>{userData?.name}</div>
}

// Suspenseでラップ
<Suspense fallback={<Loading />}>
  <UserProfile />
</Suspense>
```

### Pattern 3: atomFamily

動的にatomを生成・キャッシュ。メモリリーク対策必須。

```typescript
const todoFamily = atomFamily((id: string) =>
  atom({ id, text: '', completed: false })
)

// 使用
const todoAtom = todoFamily('todo-1')

// クリーンアップ
todoFamily.remove('todo-1')

// 自動削除ルール設定
todoFamily.setShouldRemove((createdAt, param) => {
  return Date.now() - createdAt > 60 * 60 * 1000 // 1時間後削除
})
```

### Pattern 4: Persistence

```typescript
import { atomWithStorage } from 'jotai/utils'

// localStorage永続化
const themeAtom = atomWithStorage('theme', 'light')

// sessionStorage永続化
import { createJSONStorage } from 'jotai/utils'
const sessionAtom = atomWithStorage(
  'session',
  null,
  createJSONStorage(() => sessionStorage)
)
```

### Pattern 5: Reset

```typescript
import { atomWithReset, useResetAtom, RESET } from 'jotai/utils'

const formAtom = atomWithReset({ name: '', email: '' })

// コンポーネント内
const resetForm = useResetAtom(formAtom)
resetForm() // 初期値に戻る

// 派生atomでRESETシンボル使用
const derivedAtom = atom(
  (get) => get(formAtom),
  (get, set, newValue) => {
    set(formAtom, newValue === RESET ? RESET : newValue)
  }
)
```

## Performance Optimization

### selectAtom

大きなオブジェクトから一部のみ取得。派生atomを優先し、必要な場合のみ使用。

```typescript
import { selectAtom } from 'jotai/utils'

const personAtom = atom({ name: 'John', age: 30, address: {...} })

// nameのみを購読
const nameAtom = selectAtom(personAtom, (person) => person.name)

// 安定した参照が必要（useMemoまたは外部定義）
const stableNameAtom = useMemo(
  () => selectAtom(personAtom, (p) => p.name),
  []
)
```

### splitAtom

配列の各要素を独立したatomとして管理。

```typescript
import { splitAtom } from 'jotai/utils'

const todosAtom = atom<Todo[]>([])
const todoAtomsAtom = splitAtom(todosAtom)

function TodoList() {
  const [todoAtoms, dispatch] = useAtom(todoAtomsAtom)

  return (
    <>
      {todoAtoms.map((todoAtom) => (
        <TodoItem
          key={`${todoAtom}`}
          todoAtom={todoAtom}
          onRemove={() => dispatch({ type: 'remove', atom: todoAtom })}
        />
      ))}
    </>
  )
}
```

## TypeScript

```typescript
// 型推論を活用（明示的型定義は不要な場合が多い）
const countAtom = atom(0) // PrimitiveAtom<number>

// 明示的型定義が必要な場合
const userAtom = atom<User | null>(null)

// Write-only atomの型
const actionAtom = atom<null, [string, number], void>(
  null,
  (get, set, str, num) => { ... }
)

// 型抽出
type CountValue = ExtractAtomValue<typeof countAtom> // number
```

## Testing

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Provider } from 'jotai'
import { useHydrateAtoms } from 'jotai/utils'

// 初期値を注入するヘルパー
function HydrateAtoms({ initialValues, children }) {
  useHydrateAtoms(initialValues)
  return children
}

function TestProvider({ initialValues, children }) {
  return (
    <Provider>
      <HydrateAtoms initialValues={initialValues}>
        {children}
      </HydrateAtoms>
    </Provider>
  )
}

// テスト
test('increments counter', async () => {
  render(
    <TestProvider initialValues={[[countAtom, 5]]}>
      <Counter />
    </TestProvider>
  )

  await userEvent.click(screen.getByRole('button'))
  expect(screen.getByText('6')).toBeInTheDocument()
})
```

## Debugging

```typescript
// デバッグラベル追加
countAtom.debugLabel = 'count'

// useAtomsDebugValueでProvider内の全atom確認
import { useAtomsDebugValue } from 'jotai-devtools'
function DebugObserver() {
  useAtomsDebugValue()
  return null
}

// Redux DevTools連携
import { useAtomDevtools } from 'jotai-devtools'
useAtomDevtools(countAtom, { name: 'count' })
```

## Best Practices

1. **Atom粒度**: 小さく再利用可能な単位に分割
2. **カプセル化**: base atomを隠蔽し、派生atomのみをexport
3. **Action atom**: 複雑な更新ロジックはwrite-only atomに分離
4. **非同期処理**: SuspenseとError Boundaryを適切に配置
5. **atomFamily**: メモリリーク対策として`remove()`または`setShouldRemove()`を使用
6. **TypeScript**: 型推論を活用し、必要な場合のみ明示的に型定義
7. **テスト**: ユーザー操作に近い形でテストを記述

## References

詳細は以下を参照:
- [patterns.md](references/patterns.md): 高度な実装パターン
- [api.md](references/api.md): API詳細リファレンス
