---
name: day3-clarify
description: AI Native Camp Day 3 Clarify & GitHub. Clarify 플러그인으로 모호한 요구사항을 명확하게 만들고, 나만의 스킬을 만들고, PRD를 작성하여 GitHub에 첫 PR을 제출한다. "3일차", "Day 3", "clarify", "클래리파이", "PRD", "GitHub" 요청에 사용.
---

# Day 3: Clarify

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| **Clarify** | 모호한 요구사항을 명확하게 만드는 과정. Claude가 질문을 던져서 암묵지를 명시지로 변환한다 |
| **AskUserQuestion** | Claude가 사용자에게 구조화된 질문을 하는 도구. 선택지를 제시하여 인지 부하를 줄인다 |
| **Hypothesis-as-Options** | 열린 질문 대신 가설을 선택지로 제시하는 원칙. "뭘 원해요?" 대신 "A / B / C 중 어떤 건가요?" |
| **Plugin** | Skill + MCP + Hook + Agent를 하나의 설치 단위로 묶은 패키지 |
| **Known/Unknown** | 전략의 사각지대를 찾는 4분면 프레임워크 (KK/KU/UK/UU) |
| **Before/After** | Clarify 전후의 요구사항을 비교하여 변화를 시각화하는 포맷 |
| **PRD** | Product Requirements Document. "이 프로젝트가 뭘 해결하고, 뭘 만드는지" 정리한 문서 |
| **GitHub** | 코드와 문서를 함께 관리하고 공유하는 온라인 서비스. Google Docs의 코드 버전 |
| **PR (Pull Request)** | "내 작업을 확인해주세요"라고 운영진에게 보내는 검토 요청. 제출 버튼과 같다 |

---

## STOP PROTOCOL — 절대 위반 금지

> 이 프로토콜은 이 스킬의 최우선 규칙이다.
> 아래 규칙을 위반하면 수업이 망가진다.

### 각 블록은 반드시 2턴에 걸쳐 진행한다

```
┌─ Phase A (첫 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN 섹션을 읽는다    │
│ 2. 기능을 설명한다                                        │
│ 3. references/에서 해당 블록 파일의 EXECUTE 섹션을 읽는다    │
│ 4. "지금 직접 실행해보세요"라고 안내한다                     │
│ 5. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│                                                          │
│ ❌ 절대 하지 않는 것: 퀴즈 출제, QUIZ 섹션 읽기             │
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출                  │
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
└──────────────────────────────────────────────────────────┘

  ⬇️ 사용자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항 (절대 위반 금지)

1. **Phase A에서 AskUserQuestion을 호출하지 않는다** — 설명 + 실행 안내 후 바로 Stop
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **Phase A에서 "실행해봤나요?"를 묻지 않는다** — 사용자가 먼저 말할 때까지 기다린다
4. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 형태의 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

이 문구 이후에 어떤 도구 호출(AskUserQuestion 포함)이나 추가 텍스트도 출력하지 않는다.

### 블록 특수 규칙

- **Block 0 (Concept)**: 표준 Phase A/B. AskUserQuestion 체험이 EXECUTE의 핵심.
- **Block 1 (Experience Vague)**: **예외** — Phase A에서 Claude가 clarify:vague 프로토콜을 시연한다. 학생이 모호한 요구사항을 던지면 Claude가 AskUserQuestion으로 clarify한다. 학생은 "clarify 받는 사람" 역할.
- **Block 2 (Build Clarify)**: 표준이지만 EXECUTE에서 플러그인의 vague SKILL.md를 Read로 분석한 후, 템플릿 기반으로 나만의 스킬을 작성한다.
- **Block 3 (Plugin & Unknown)**: **메인 블록** — Plugin 심화 분석 + clarify:unknown 체험.
- **Block 4 (PRD & GitHub)**: 표준 Phase A/B이지만 PRD 작성은 인터랙티브. Claude가 GitHub ID 확인 → PRD 초안 작성 → 검증 → PR 제출까지 자동으로 진행. Phase B 퀴즈 후 Day 3 과제 안내.

---

## 소요 시간

| Block | 주제 | 시간 |
|-------|------|------|
| 0 | Clarify 개념 + AskUserQuestion | ~10분 |
| 1 | clarify:vague 체험 | ~15분 |
| 2 | 나만의 Clarify 스킬 만들기 | ~25분 |
| 3 | Plugin 심화 + clarify:unknown 체험 | ~30분 |
| 4 | PRD 작성 & GitHub 첫 제출 + 과제 | ~15분 |
| | **합계** | **~95분** |

---

## 핵심 전략

> **"설치한 플러그인을 해부하고, 직접 만들어보기"**

Day 1에서 설치한 clarify 플러그인을 체험 → 구조 분석 → 나만의 버전 제작 → 심화 활용

```
Day 1에서 설치          Day 3에서 깊이 파기
┌──────────────┐       ┌──────────────────────────┐
│ /plugin      │       │ Block 0: 개념 이해        │
│   install    │  ───▶ │ Block 1: vague 체험       │
│   clarify    │       │ Block 2: 나만의 스킬 제작  │
└──────────────┘       │ Block 3: Plugin 해부 +    │
                       │          unknown 체험     │
                       │ Block 4: PRD + GitHub 제출 │
                       └──────────────────────────┘
```

---

## References 파일 맵

| 블록 | 파일 |
|------|------|
| Block 0 | `references/block0-concept.md` |
| Block 1 | `references/block1-experience-vague.md` |
| Block 2 | `references/block2-build-clarify.md` |
| Block 3 | `references/block3-plugin-and-unknown.md` |
| Block 4 | `references/block4-prd-and-github.md` |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## Templates 파일 맵

| 파일 | 용도 |
|------|------|
| `templates/clarify-vague.md` | 나만의 Clarify 스킬 작성용 템플릿 |

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다 (WebFetch는 요약/손실 위험이 있으므로 사용하지 않는다)

---

## 시작

스킬 시작 시 아래를 안내하고 AskUserQuestion으로 어디서 시작할지 물어본다.

> 아직 camp-2 스킬이 설치되지 않았다면:
> ```
> npx skills add ai-native-camp/camp-2
> ```

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | Concept | Clarify 개념 + AskUserQuestion 체험 |
| 1 | Experience | clarify:vague 플러그인 체험 |
| 2 | Build | 나만의 Clarify 스킬 만들기 |
| 3 | Plugin & Unknown | Plugin 심화 + clarify:unknown |
| 4 | PRD & GitHub | PRD 작성 + GitHub 첫 PR 제출 + 과제 |

```json
AskUserQuestion({
  "questions": [{
    "question": "어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "Block 0: Concept", "description": "Clarify 개념 + AskUserQuestion 체험"},
      {"label": "Block 1: Experience", "description": "clarify:vague 플러그인 체험"},
      {"label": "Block 2: Build", "description": "나만의 Clarify 스킬 만들기"},
      {"label": "Block 3: Plugin & Unknown", "description": "Plugin 심화 + unknown 체험"},
      {"label": "Block 4: PRD & GitHub", "description": "PRD 작성 + GitHub 첫 PR 제출"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
