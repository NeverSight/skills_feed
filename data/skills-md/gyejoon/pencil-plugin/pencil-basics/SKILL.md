---
name: Pencil Basics
description: This skill should be used when the user asks about "pencil 사용법", ".pen 파일", "노드 타입", "레이아웃 시스템", "pencil mcp", "batch_design", "batch_get", or wants to understand how to work with Pencil design files. Provides comprehensive guidance for using Pencil MCP tools effectively.
version: 0.1.0
---

# Pencil Basics

Pencil MCP 서버를 사용하여 .pen 파일을 읽고, 수정하고, 디자인을 생성하는 방법을 제공한다.

## Core Concepts

### .pen 파일 구조

.pen 파일은 디자인 데이터를 저장하는 암호화된 형식이다. 반드시 Pencil MCP 도구만 사용하여 접근한다.

**중요**: Read, Grep, Write 도구로 .pen 파일을 직접 읽거나 쓰지 않는다. 항상 Pencil MCP 도구를 사용한다.

### 노드 타입

| Type | 용도 | 주요 속성 |
|------|------|-----------|
| `frame` | 컨테이너, 레이아웃 | layout, gap, padding, fill |
| `text` | 텍스트 콘텐츠 | content, fontSize, fontWeight, textColor |
| `rectangle` | 사각형 도형 | fill, stroke, cornerRadius |
| `ellipse` | 원/타원 | fill, stroke |
| `ref` | 컴포넌트 인스턴스 | ref (컴포넌트 ID 참조) |
| `image` | 이미지 프레임 | G() 오퍼레이션으로 적용 |
| `icon_font` | 아이콘 | icon, iconSize |

### 레이아웃 시스템

Auto Layout 속성:

```
layout: "horizontal" | "vertical" | "grid"
gap: number (자식 간 간격)
padding: number | [top, right, bottom, left]
alignItems: "start" | "center" | "end" | "stretch"
justifyContent: "start" | "center" | "end" | "space-between"
```

크기 지정:

```
width: number | "fill_container" | "hug_contents"
height: number | "fill_container" | "hug_contents"
```

## Essential Tools

### 1. get_editor_state

현재 에디터 상태와 선택된 노드 정보를 가져온다.

```
mcp__pencil__get_editor_state(include_schema: boolean)
```

디자인 작업 시작 전 항상 호출하여 활성 파일과 선택 상태를 확인한다.

### 2. batch_get

노드를 검색하거나 ID로 읽는다.

```
mcp__pencil__batch_get(
  filePath: string,
  patterns?: [{ reusable?: boolean, type?: string, name?: string }],
  nodeIds?: string[],
  readDepth?: number,
  searchDepth?: number
)
```

**사용 예시**:
- 재사용 컴포넌트 목록: `patterns: [{ reusable: true }]`
- 특정 노드 읽기: `nodeIds: ["nodeId1", "nodeId2"]`
- 텍스트 노드 검색: `patterns: [{ type: "text" }]`

### 3. batch_design

디자인 수정 오퍼레이션을 실행한다.

```
mcp__pencil__batch_design(
  filePath: string,
  operations: string  // JavaScript 유사 구문
)
```

### 4. get_screenshot

노드의 스크린샷을 가져와 시각적으로 검증한다.

```
mcp__pencil__get_screenshot(filePath: string, nodeId: string)
```

디자인 작업 후 항상 스크린샷으로 결과를 확인한다.

## batch_design Operations

### Insert (I)

새 노드를 삽입한다.

```javascript
// 기본 삽입
frame1=I("parentId", { type: "frame", layout: "vertical", gap: 16 })
text1=I(frame1, { type: "text", content: "Hello", fontSize: 16 })

// 컴포넌트 인스턴스 삽입
button=I("parentId", { type: "ref", ref: "ButtonComponentId" })
```

### Update (U)

기존 노드의 속성을 업데이트한다.

```javascript
// 직접 업데이트
U("nodeId", { fill: "#FF0000", padding: 16 })

// 컴포넌트 인스턴스 내부 노드 업데이트
U("instanceId/labelId", { content: "New Label" })
```

### Copy (C)

노드를 복사한다.

```javascript
// 단순 복사
copy1=C("sourceId", "parentId", { x: 100, y: 100 })

// 속성 오버라이드와 함께 복사
copy2=C("sourceId", "parentId", {
  descendants: {
    "labelId": { content: "Copied Label" }
  }
})
```

### Replace (R)

노드를 새 노드로 교체한다.

```javascript
newNode=R("oldNodeId", { type: "text", content: "Replaced" })
```

### Delete (D)

노드를 삭제한다.

```javascript
D("nodeId")
```

### Move (M)

노드를 다른 위치로 이동한다.

```javascript
M("nodeId", "newParentId", 0)  // index는 선택사항
```

### Generate Image (G)

프레임에 이미지를 적용한다.

```javascript
// AI 생성 이미지
imgFrame=I("parentId", { type: "frame", width: 400, height: 300 })
G(imgFrame, "ai", "modern office workspace")

// 스톡 이미지
G("existingFrameId", "stock", "nature landscape")
```

## Workflow Patterns

### 새 화면 생성

1. `get_editor_state`로 현재 상태 확인
2. `batch_get`으로 사용 가능한 컴포넌트 확인
3. `get_guidelines`로 디자인 가이드라인 로드
4. `get_style_guide_tags` + `get_style_guide`로 스타일 영감 얻기
5. `batch_design`으로 화면 구성
6. `get_screenshot`으로 결과 검증

### 컴포넌트 수정

1. `batch_get`으로 대상 노드 구조 파악
2. `batch_design`의 U() 오퍼레이션으로 속성 수정
3. `get_screenshot`으로 변경사항 확인

### 레이아웃 문제 해결

1. `snapshot_layout`으로 레이아웃 구조 분석
2. 오버플로우, 클리핑 문제 확인
3. `batch_design`으로 수정
4. `get_screenshot`으로 검증

## Best Practices

### Do

- 매 batch_design 후 get_screenshot으로 검증
- 작은 단위로 오퍼레이션 실행 (최대 25개)
- 바인딩 이름은 매번 새로 생성
- 컴포넌트 수정 시 인스턴스 경로 사용 (instanceId/childId)

### Don't

- Read, Write, Grep으로 .pen 파일 직접 접근
- 한 번에 너무 많은 오퍼레이션 실행
- 바인딩 이름 재사용
- id 속성 직접 지정 (자동 생성됨)

## Additional Resources

### Reference Files

- **`references/node-properties.md`** - 모든 노드 타입의 상세 속성
- **`references/layout-examples.md`** - 레이아웃 패턴 예시
