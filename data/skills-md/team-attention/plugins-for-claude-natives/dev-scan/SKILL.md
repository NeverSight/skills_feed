---
name: dev-scan
description: 개발 커뮤니티에서 기술 주제에 대한 다양한 의견 수집. "개발자 반응", "커뮤니티 의견", "developer reactions" 요청에 사용. Reddit, HN, Dev.to, Lobsters 등 종합.
version: 1.0.0
---

# Dev Opinions Scan

여러 개발 커뮤니티에서 특정 주제에 대한 다양한 의견을 수집하여 종합.

## Purpose

기술 주제에 대한 **다양한 시각**을 빠르게 파악:
- 찬반 의견 분포
- 실무자들의 경험담
- 숨겨진 우려사항이나 장점
- 독특하거나 주목할 만한 시각

## Data Sources

| Platform | Method |
|----------|--------|
| Reddit | Gemini CLI |
| Hacker News | WebSearch |
| Dev.to | WebSearch |
| Lobsters | WebSearch |

## Execution

### Step 1: Topic Extraction
사용자 요청에서 핵심 주제 추출.

예시:
- "React 19에 대한 개발자들 반응" → `React 19`
- "Bun vs Deno 커뮤니티 의견" → `Bun vs Deno`

### Step 2: Parallel Search (Single Message, 4 Sources)

**Reddit** (Gemini CLI - WebFetch blocked):
```bash
# 단일 Gemini 호출로 Reddit 검색 (명시적 검색 지시 필수)
gemini -p "Search Reddit for discussions about {TOPIC}. Summarize the main opinions, debates, and insights from developers. Include Reddit post URLs where possible. Focus on: 1) Common opinions 2) Controversies 3) Notable perspectives from experienced developers."
```

**주의사항**:
- `site:reddit.com` 형식은 작동하지 않음 - Gemini가 검색 쿼리가 아닌 작업 요청으로 해석
- 반드시 "Search Reddit for..." 형태로 명시적 검색 지시 필요
- 단일 호출이 병렬 호출보다 안정적 (출력 혼재 방지)

**Other Sources** (WebSearch, parallel):
```
WebSearch: "{topic} site:news.ycombinator.com"
WebSearch: "{topic} site:dev.to"
WebSearch: "{topic} site:lobste.rs"
```

**CRITICAL**: 4개 검색을 반드시 **하나의 메시지**에서 병렬로 실행. Gemini는 단일 호출, WebSearch는 3개 병렬.

### Step 3: Synthesize & Present

수집된 데이터를 분석하여 의미 있는 인사이트를 도출한다.

#### 3-1. 의견 분류 및 패턴 파악

각 소스에서 수집된 의견들을 다음 기준으로 분류:

- **찬성/긍정**: 해당 기술/도구를 지지하는 의견
- **반대/부정**: 우려, 비판, 대안 제시
- **중립/조건부**: "~한 경우에만", "~와 함께 쓰면" 등의 조건부 의견
- **경험 기반**: 실제 프로덕션 사용 경험을 바탕으로 한 의견

#### 3-2. 공통 의견(Consensus) 도출

여러 커뮤니티에서 **반복적으로 등장하는** 의견을 식별:

- 2개 이상의 소스에서 동일한 포인트가 언급되면 공통 의견으로 분류
- 특히 Reddit과 HN에서 동시에 언급되는 의견은 신뢰도 높음
- 구체적인 수치나 사례가 포함된 의견 우선
- **최소 5개 이상의 공통 의견** 도출 목표

#### 3-3. 논쟁점(Controversy) 식별

커뮤니티 간 또는 커뮤니티 내에서 **의견이 갈리는** 지점 파악:

- 같은 주제에 대해 상반된 의견이 존재하는 경우
- 댓글에서 활발한 토론이 벌어진 스레드
- "depends on...", "but actually..." 등의 반론이 많은 주제
- **최소 3개 이상의 논쟁점** 식별 목표

#### 3-4. 주목할 시각(Notable Perspective) 선별

독특하거나 깊이 있는 인사이트 발굴:

- 다수 의견과 다르지만 논리적 근거가 탄탄한 의견
- 시니어 개발자나 해당 분야 전문가의 의견
- 실제 대규모 프로젝트 경험에서 나온 인사이트
- 다른 사람들이 놓치기 쉬운 엣지 케이스나 장기적 관점
- **최소 3개 이상의 주목할 시각** 선별 목표

## Output Format

**핵심 원칙**: 모든 의견에 출처를 인라인으로 붙인다. 출처 없는 의견은 포함하지 않는다.

```markdown
## Key Insights

### Consensus (공통 의견)

1. **[의견 제목]**
   - [구체적인 내용 설명]
   - [추가 맥락이나 예시]
   - Sources: [Reddit](url), [HN](url)

2. **[의견 제목]**
   - [구체적인 내용]
   - Source: [Dev.to](url)

(최소 5개 이상)

---

### Controversy (논쟁점)

1. **[논쟁 주제]**
   - 찬성측: "[인용]" - [Source](url)
   - 반대측: "[인용]" - [Source](url)
   - 맥락: [왜 의견이 갈리는지]

2. **[논쟁 주제]**
   - ...

(최소 3개 이상)

---

### Notable Perspective (주목할 시각)

1. **[인사이트 제목]**
   > "[원문 인용 또는 핵심 문장]"
   - [왜 주목할 만한지 설명]
   - Source: [Platform](url)

2. **[인사이트 제목]**
   - ...

(최소 3개 이상)
```

### 출처 표기 규칙

- **인라인 링크 필수**: 모든 의견 끝에 `Source: [Platform](url)` 형식으로 붙임
- **복수 출처**: 동일 의견이 여러 곳에서 언급되면 `Sources: [Reddit](url), [HN](url)`
- **직접 인용**: 가능하면 원문을 `"..."` 형태로 인용
- **URL 정확성**: 실제 접근 가능한 링크만 포함 (검색 결과에서 확인된 URL)

## Error Handling

| 상황 | 대응 |
|------|------|
| 검색 결과 없음 | 해당 플랫폼 생략, 다른 소스에 집중 |
| Gemini CLI 실패 | Reddit 생략하고 나머지 3개로 진행 |
| 주제가 너무 새로움 | 결과 부족 안내, 관련 키워드 제안 |

## Examples

**단순 주제**:
```
User: "Tailwind v4 개발자들 반응 어때?"
→ topic: "Tailwind v4"
→ 4개 소스 병렬 검색
→ 종합 인사이트 제공
```

**비교 주제**:
```
User: "pnpm vs yarn vs npm 커뮤니티 의견"
→ topic: "pnpm vs yarn vs npm comparison"
→ 4개 소스 병렬 검색
→ 각 도구별 선호도 정리
```

**논쟁적 주제**:
```
User: "Claude Code Plugin 에 대한 개발자들 생각"
→ topic: "Claude Code Plugin tips"
→ 4개 소스 병렬 검색
→ 종합 인사이트 제공
```
