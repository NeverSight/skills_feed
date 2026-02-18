---
name: image-generation-mcp
description: Generate high-quality images via MCP (Gemini models or compatible services) using structured prompts, ratios, and validation for marketing, UI, or presentations.
tags: [image-generation, gemini, mcp, design, creative, ai-art]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - mcp__gemini-cli__ask-gemini
  - mcp__gemini-cli__brainstorm
  - Write
  - Read
---

# Image Generation via MCP

MCP를 통한 AI 이미지 생성 스킬입니다. Gemini 모델 또는 호환 서비스를 사용하여 마케팅, UI, 프레젠테이션용 고품질 이미지를 생성합니다.

## When to use this skill

- **마케팅 에셋**: 히어로 이미지, 배너, 소셜 미디어 콘텐츠
- **UI/UX 디자인**: 플레이스홀더 이미지, 아이콘, 일러스트레이션
- **프레젠테이션**: 슬라이드 배경, 제품 시각화
- **브랜드 일관성**: 스타일 가이드 기반 이미지 생성

---

## Instructions

### Step 1: Configure MCP Environment

```bash
# MCP 서버 설정 확인
claude mcp list

# Gemini CLI 사용 가능 여부 확인
# gemini-cli가 설치되어 있어야 함
```

**필수 설정**:
- Model name (gemini-2.5-flash, gemini-3-pro 등)
- API key reference (환경 변수로 저장)
- Output directory

### Step 2: Define the Prompt

구조화된 프롬프트 작성:

```markdown
**Subject**: [주요 피사체]
**Style**: [스타일 - 미니멀, 일러스트, 사진풍, 3D 등]
**Lighting**: [조명 - 자연광, 스튜디오, 골든아워 등]
**Mood**: [분위기 - 차분한, 역동적, 전문적 등]
**Composition**: [구성 - 중앙 배치, 삼분할 등]
**Aspect Ratio**: [비율 - 16:9, 1:1, 9:16]
**Brand Colors**: [브랜드 컬러 제약사항]
```

### Step 3: Choose the Model

| 모델 | 용도 | 특징 |
|-----|------|------|
| `gemini-3-pro-image` | 고품질 | 복잡한 구성, 디테일 |
| `gemini-2.5-flash-image` | 빠른 반복 | 프로토타이핑, 테스트 |
| `gemini-2.5-pro-image` | 균형 | 품질/속도 밸런스 |

### Step 4: Generate and Review

```bash
# 2-4개 변형 생성
ask-gemini "Create a serene mountain landscape at sunset,
  wide 16:9, minimal style, soft gradients in brand blue #2563EB"

# 단일 변수 변경으로 반복
ask-gemini "Same prompt but with warm orange tones"
```

**리뷰 체크리스트**:
- [ ] 브랜드 적합성
- [ ] 구성 명확성
- [ ] 비율 정확성
- [ ] 텍스트 가독성 (텍스트 포함 시)

### Step 5: Deliverables

최종 산출물:
- 최종 이미지 파일
- 프롬프트 메타데이터 기록
- 모델, 비율, 사용 노트

```json
{
  "prompt": "serene mountain landscape at sunset...",
  "model": "gemini-3-pro-image",
  "aspect_ratio": "16:9",
  "style": "minimal",
  "brand_colors": ["#2563EB"],
  "output_file": "hero-image-v1.png",
  "timestamp": "2026-01-21T10:30:00Z"
}
```

---

## Examples

### Example 1: Hero Image

**Prompt**:
```
Create a serene mountain landscape at sunset,
wide 16:9, minimal style, soft gradients in brand blue #2563EB.
Focus on clean lines and modern aesthetic.
```

**Expected output**:
- 16:9 hero image
- Prompt parameters saved
- 2-3 variants for selection

### Example 2: Product Thumbnail

**Prompt**:
```
Generate a 1:1 thumbnail of a futuristic dashboard UI
with clean interface, soft lighting, and professional feel.
Include subtle glow effects and dark theme.
```

**Expected output**:
- 1:1 square image
- Low visual noise
- App store ready

### Example 3: Social Media Banner

**Prompt**:
```
Create a LinkedIn banner (1584x396) for a SaaS startup.
Modern gradient background with abstract geometric shapes.
Colors: #6366F1 to #8B5CF6.
Leave space for text overlay on the left side.
```

**Expected output**:
- LinkedIn-optimized dimensions
- Safe zone for text
- Brand-aligned colors

---

## Best practices

1. **Specify ratio early**: 의도하지 않은 크롭 방지
2. **Use style anchors**: 일관된 미적 스타일 유지
3. **Iterate with constraints**: 한 번에 하나의 변수만 변경
4. **Track prompts**: 재현 가능성 확보
5. **Batch similar requests**: 일관된 스타일 세트 생성

---

## Common pitfalls

- **모호한 프롬프트**: 구체적인 스타일과 구성 지정 필요
- **크기 제약 무시**: 대상 채널의 크기 요구사항 확인
- **과도하게 복잡한 장면**: 명확성을 위해 단순화

---

## Troubleshooting

### Issue: Outputs are inconsistent
**Cause**: 안정적인 스타일 제약 누락
**Solution**: 스타일 레퍼런스와 고정 팔레트 추가

### Issue: Wrong aspect ratio
**Cause**: 비율 미지정 또는 지원하지 않는 비율
**Solution**: 정확한 비율 제공 후 재생성

### Issue: Brand mismatch
**Cause**: 컬러 코드 미지정
**Solution**: HEX 코드로 브랜드 컬러 명시

---

## Output format

```markdown
## Image Generation Report

### Request
- **Prompt**: [full prompt]
- **Model**: [model used]
- **Ratio**: [aspect ratio]

### Output Files
1. `filename-v1.png` - [description]
2. `filename-v2.png` - [variant description]

### Metadata
- Generated: [timestamp]
- Iterations: [count]
- Selected: [final choice]

### Usage Notes
[Any notes for implementation]
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 프롬프트 완전성, 비율 정합성
- **Round 2 (Analyst)**: 스타일 일관성, 브랜드 정합성
- **Round 3 (Executor)**: 출력 파일명, 전달 체크리스트 검증

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 프롬프트 구성, 품질 검증 |
| Gemini | 이미지 생성 실행 |
| Codex | 파일 관리, 배치 처리 |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [frontend-design](../../frontend/design-system/SKILL.md)
- [presentation-builder](../../documentation/presentation-builder/SKILL.md)
- [video-production](../video-production/SKILL.md)

### Tags
`#image-generation` `#gemini` `#mcp` `#design` `#creative` `#ai-art`
