---
name: skill-creator
description: "DaleStudy/skills 저장소에 새로운 스킬을 생성하거나 기존 스킬을 수정할 때 사용. 다음 상황에서 활성화: (1) 새 스킬 생성 요청 시, (2) SKILL.md 파일 작성 또는 수정 시, (3) 스킬 구조나 frontmatter 관련 질문 시, (4) 'skill', 'SKILL.md', 'frontmatter' 키워드가 포함된 작업 시"
license: MIT
compatibility: Git repository with skills/ directory
metadata:
  author: DaleStudy
  version: "1.0"
---

# Skill Creator for DaleStudy

DaleStudy/skills 저장소에 새로운 스킬을 추가하기 위한 가이드.

## 스킬 구조

```
skills/{skill-name}/
└── SKILL.md          # YAML frontmatter + Markdown 지시사항 (필수)
```

## SKILL.md 형식

```yaml
---
name: skill-name # 필수: 디렉토리명과 일치 (최대 64자, 소문자/숫자/하이픈)
description: "스킬 설명" # 필수: 트리거 조건 포함 (최대 1024자)
license: MIT # 선택
compatibility: Required CLI tools # 선택: 필요한 도구
metadata: # 선택
  author: DaleStudy
  version: "1.0"
allowed-tools: Bash(command:*) # 선택: 허용할 도구 패턴
---
# 스킬 제목

스킬 지시사항 (Markdown)
```

## 스킬 생성 절차

### 1. 디렉토리 생성

```bash
mkdir -p skills/{skill-name}
```

### 2. SKILL.md 작성

#### Frontmatter 작성 규칙

**name 필드:**

- 디렉토리명과 동일해야 함
- 소문자, 숫자, 하이픈만 사용
- 연속된 하이픈 불가 (`my--skill` ❌)
- 최대 64자

**description 필드 (가장 중요):**

- 스킬의 목적과 **트리거 조건**을 명확히 기술
- Body는 트리거 후에만 로드되므로, "언제 사용"은 반드시 description에 포함
- 패턴: `"{스킬 설명}. 다음 상황에서 사용: (1) ..., (2) ..., (3) ..."`

```yaml
# ✅ 좋은 예
description: "Node.js 대신 Bun 런타임 사용을 위한 스킬. 다음 상황에서 사용: (1) 새 JavaScript/TypeScript 프로젝트 생성 시, (2) package.json 또는 의존성 관련 작업 시"

# ❌ 나쁜 예
description: "Bun 관련 스킬"  # 트리거 조건 없음
```

#### Body 작성 규칙

- 간결하게 유지 (500줄 이하 권장)
- Claude가 이미 아는 내용은 생략
- 예제 코드 > 장황한 설명
- 명령형/부정사 형태 사용

### 3. README.md 업데이트

저장소 루트의 README.md에 새 스킬 추가:

```markdown
## Current Skills

- **bun**: Node.js 대신 Bun 런타임 사용
- **github-actions**: GitHub Actions 워크플로우 작성 및 보안
- **{new-skill}**: {간단한 설명} <!-- 추가 -->
```

### 4. 워크플로우 매트릭스 업데이트

`.github/workflows/ci.yml`의 matrix에 새 스킬 추가:

```yaml
matrix:
  skill:
    - bun
    - github-actions
    - { new-skill } # 추가
```

## 기존 스킬 참고

| 스킬             | 특징                                           |
| ---------------- | ---------------------------------------------- |
| `bun`            | 명령어 매핑 테이블, 코드 예제 중심             |
| `github-actions` | 보안 모범 사례, YAML 예제 중심                 |
| `skill-creator`  | 메타 스킬, 구조화된 절차, frontmatter 가이드   |
| `storybook`      | CSF 3.0 베스트 프랙티스, TypeScript 타입 예제  |

새 스킬 작성 시 기존 스킬의 스타일을 참고하여 일관성 유지.

## 검증

스킬 설치 테스트:

```bash
npx skills add DaleStudy/skills --skill {skill-name} --agent claude-code --global --yes
```
