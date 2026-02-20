---
name: start
description: 진단 대화 시작점. 학습자의 직무/경력/AI 경험/사전 지식/학습 목적을 5문항으로 파악하고 학습 경로를 제안할 때 사용.
---

# Start Skill

이 스킬은 `/start` 진입 시 사용한다.

## 목표

- 5문항 진단으로 학습자 프로필 생성
- 학습 모드(`module1~6`) 또는 탐색 모드(`explore`) 시작점 결정
- 결과를 `data/learner-profile.json`에 저장

## 진단 규칙

- 문항은 **한 번에 하나씩** 제시한다. 2개 이상의 질문을 한 메시지에 담지 않는다.
- **모든 문항은 반드시 `AskUserQuestion` 도구를 호출하여 제시한다.**
- 텍스트로 "1) ... 2) ..."를 나열하는 것은 **절대 금지**한다. 반드시 `AskUserQuestion` 도구 호출을 사용한다.
- 각 질문 전에 간단한 맥락 한 문장을 추가할 수 있지만, 선택지 자체는 반드시 `AskUserQuestion`으로 제시한다.
- 학습자가 자유서술로 답하면 가장 가까운 번호로 재확인한다.
- 이름, 연락처 등 개인식별정보는 요청하지 않는다.
- Q4 사전 지식 체크는 `multiSelect: true`를 사용한다. 나머지는 `multiSelect: false`이다.

## 진단 5문항 — AskUserQuestion 호출 명세

각 질문을 제시할 때 아래 파라미터를 **그대로** 사용하여 `AskUserQuestion` 도구를 호출한다.

---

### Q1 — 직무

```
AskUserQuestion 호출 파라미터:
  question: "현재 직무가 어디에 가장 가까운가요?"
  header: "직무"
  multiSelect: false
  options:
    - label: "데이터 엔지니어링"
      description: "파이프라인, ETL, 인프라"
    - label: "데이터 분석"
      description: "대시보드, 리포트, 인사이트"
    - label: "PM / 기획"
      description: "제품 기획, 프로젝트 관리"
    - label: "개발"
      description: "백엔드, 프론트엔드, 게임 클라이언트 등"
```

활용: 비유와 예시의 맥락을 결정한다.

---

### Q2 — 경력 수준

```
AskUserQuestion 호출 파라미터:
  question: "경력 수준은 어느 정도인가요?"
  header: "경력"
  multiSelect: false
  options:
    - label: "주니어"
      description: "1~3년차"
    - label: "미들"
      description: "4~7년차"
    - label: "시니어"
      description: "8년차 이상"
    - label: "리드 / 매니저"
      description: "팀 리드 또는 매니저급"
```

활용: 설명의 추상화 수준과 전략적 관점의 비중을 조절한다.

---

### Q3 — AI 활용 수준

```
AskUserQuestion 호출 파라미터:
  question: "AI 도구를 업무에서 어느 정도 사용하고 계신가요?"
  header: "AI 경험"
  multiSelect: false
  options:
    - label: "거의 안 써봤다"
      description: "AI 도구 사용 경험이 거의 없음"
    - label: "가끔 사용"
      description: "ChatGPT 등을 가끔 써본다"
    - label: "자주 사용"
      description: "업무에 꽤 자주 활용하고 있다"
    - label: "여러 도구 비교 사용"
      description: "AI 도구 여러 개를 비교하며 쓰고 있다"
```

활용: 모듈 진행 속도와 깊이를 조절한다.

---

### Q4 — 사전 지식 체크

```
AskUserQuestion 호출 파라미터:
  question: "다음 중 '대략 무슨 뜻인지' 알고 있는 것을 모두 골라주세요. (모르는 게 있어도 전혀 괜찮습니다!)"
  header: "사전 지식"
  multiSelect: true
  options:
    - label: "Token"
      description: "LLM이 텍스트를 처리하는 기본 단위"
    - label: "RAG"
      description: "외부 문서를 검색해서 LLM 답변에 활용하는 방식"
    - label: "Fine-tuning"
      description: "모델을 추가 학습시키는 방식"
    - label: "Agent"
      description: "AI가 도구를 사용하여 자율적으로 작업하는 방식"
```

활용: 어느 모듈부터 시작할지, 어떤 개념을 빠르게 넘어갈지 판단한다.
참고: 학습자가 "Other"를 선택하고 "하나도 모르겠다"라고 답하면 사전 지식 없음으로 처리한다.

---

### Q5 — 학습 목적

```
AskUserQuestion 호출 파라미터:
  question: "이 교육에서 가장 원하는 것은?"
  header: "학습 목적"
  multiSelect: false
  options:
    - label: "핵심 원리 이해"
      description: "AI의 핵심 원리를 제대로 이해하고 싶다 → 학습 모드"
    - label: "트렌드/키워드 파악"
      description: "AI 관련 용어와 트렌드를 빠르게 파악하고 싶다 → 탐색 모드"
    - label: "둘 다"
      description: "원리도 알고 싶고 트렌드도 궁금하다 → 학습 모드 + 탐색 자유 전환"
    - label: "팀 도입/전략"
      description: "우리 팀에서 AI를 어떻게 쓸지 판단하고 싶다 → Module 5~6 중심"
```

활용: 학습 모드와 모듈 우선순위를 결정한다.

---

## 경로 추천 규칙

| 진단 결과 조합 | AI의 조절 방식 |
|---|---|
| 학습 목적 = "트렌드/키워드 파악" | `explore` 우선 진입. 학습 모드 전환 항상 가능 |
| 학습 목적 = "팀 도입/전략" | `module5-tools-ecosystem` 또는 `module6-strategy` 우선 진입 |
| 학습 목적 = "핵심 원리 이해" 또는 "둘 다" | `module1-llm-basics`부터 순차 진행 |
| AI 경험 = "거의 안 써봤다" + 사전 지식 없음 | 모듈 진행 속도를 낮추고 비유를 늘린다 |
| AI 경험 = "자주 사용" 이상 + 사전 지식 일부 | Module 1은 빠르게 확인, Module 3~4에 시간 투자 |

## 출력 형식

진단 종료 후 아래를 반드시 제공한다.

1. 학습자 요약 (3줄 이내)
2. 추천 시작 모듈 1개와 이유
3. 다음 행동 선택지 — **AskUserQuestion 도구**로 제시

```
AskUserQuestion 호출 파라미터:
  question: "어떻게 시작할까요?"
  header: "시작"
  multiSelect: false
  options:
    - label: "[추천 모듈명]으로 시작하기 (추천)"
      description: "[추천 이유 한 줄]"
    - label: "다른 모듈 선택하기"
      description: "전체 모듈 목록을 보고 직접 선택"
    - label: "탐색 모드로 시작"
      description: "키워드/트렌드를 자유롭게 탐색"
```

## 저장 스키마

진단 완료 시 `data/learner-profile.json`을 갱신한다. (파일은 이미 기본 템플릿으로 존재함)

- `diagnosis_completed`
- `updated_at`
- `profile.role`
- `profile.seniority`
- `profile.ai_experience`
- `profile.prior_knowledge`
- `profile.goal`
- `recommendation.start_skill`
- `recommendation.reason`
