---
name: pptx-presentation-builder
description: Build professional PPTX presentations with brand-aligned layouts using structured deck briefs and validation steps for pitch, roadmap, and product decks.
tags: [presentation, pptx, slides, storytelling, branding, pitch-deck]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - Write
  - Read
  - Task
---

# PPTX Presentation Builder

브랜드 가이드라인에 맞춘 전문 PPTX 프레젠테이션 빌더 스킬입니다. 피치덱, 로드맵, 제품 소개 등 다양한 프레젠테이션을 구조화된 브리프와 검증 단계로 생성합니다.

## When to use this skill

- **전문 슬라이드 덱 필요**: 프롬프트에서 프레젠테이션 생성
- **브랜드 일관성 필요**: 가이드라인에 맞춘 일관된 슬라이드
- **반복 가능한 템플릿**: 제품, 피치, 로드맵 덱 템플릿화

---

## Instructions

### Step 1: Gather Brand Constraints

```yaml
brand_kit:
  colors:
    primary: "#2563EB"
    secondary: "#6366F1"
    accent: "#F59E0B"
    background: "#FFFFFF"
    text: "#1F2937"
  fonts:
    heading: "Inter"
    body: "Inter"
    mono: "JetBrains Mono"
  logo:
    placement: "top-left" | "bottom-right"
    size: "small" | "medium"
  style:
    tone: "minimal" | "bold" | "executive"
    corners: "sharp" | "rounded"
    shadows: true | false
```

### Step 2: Define Deck Structure

```markdown
## Deck Brief

### Meta
- **Title**: [덱 제목]
- **Audience**: [청중]
- **Goal**: [목표 - 투자 유치, 제품 소개, 보고]
- **Duration**: [발표 시간]

### Slides
| # | Type | Title | Key Message |
|---|------|-------|-------------|
| 1 | Title | Company Name | Tagline |
| 2 | Agenda | Today's Agenda | 3-5 bullet points |
| 3 | Problem | The Challenge | Pain point statement |
| 4 | Solution | Our Approach | Value proposition |
| 5 | Features | Key Capabilities | 3 features with icons |
| 6 | Demo | Product in Action | Screenshot/video |
| 7 | Traction | Growth Numbers | Key metrics |
| 8 | Team | Who We Are | Team photos + roles |
| 9 | Ask | The Opportunity | Investment/partnership ask |
| 10 | Contact | Get in Touch | Contact info + CTA |
```

### Step 3: Generate Slides

슬라이드별 콘텐츠 생성:

```markdown
## Slide 1: Title Slide

### Layout: Centered

### Content
- **Title**: [Company Name]
- **Subtitle**: [Tagline - 10 words max]
- **Visual**: Logo centered
- **Background**: Gradient (#2563EB → #6366F1)

### Speaker Notes
Welcome the audience. Introduce yourself and the company.
Set the context for why you're presenting today.
```

**슬라이드 타입별 템플릿**:

| Type | Layout | Elements |
|------|--------|----------|
| Title | Centered | Logo, Title, Subtitle |
| Agenda | Left-aligned | Numbered list (3-5 items) |
| Problem | Split | Text left, Visual right |
| Solution | Split | Visual left, Text right |
| Features | 3-column | Icon + Title + Description |
| Stats | Data cards | 3-4 key metrics |
| Quote | Centered | Quote text + attribution |
| Team | Grid | Photos + Names + Roles |
| CTA | Centered | Headline + Button |

### Step 4: Review and Refine

```markdown
## Review Checklist

### Layout Balance
- [ ] 시각적 균형 확인
- [ ] 여백 충분히 확보
- [ ] 정렬 일관성

### Typography
- [ ] 폰트 크기 계층 (H1 > H2 > Body)
- [ ] 가독성 확보 (최소 18pt body)
- [ ] 일관된 폰트 사용

### Content
- [ ] 슬라이드당 하나의 아이디어
- [ ] 텍스트 과밀 방지
- [ ] 데이터/주장의 출처 명시

### Accessibility
- [ ] 색상 대비 충분
- [ ] 이미지에 alt text
- [ ] 논리적 읽기 순서
```

### Step 5: Export and Handoff

```markdown
## Handoff Package

### Files
- presentation.pptx
- presentation.pdf (backup)
- assets/ (images, logos)

### Summary
- **Total Slides**: [count]
- **Estimated Duration**: [minutes]
- **Key Narrative Arc**: [brief description]

### Editing Notes
- Slide 5: [specific edit note]
- Slide 8: [specific edit note]

### Post-Export Checklist
- [ ] Font embedding verified
- [ ] Images high resolution
- [ ] Animations functional
- [ ] Links active
```

---

## Examples

### Example 1: 5-Slide Roadmap

**Prompt**:
```
Create a 5-slide roadmap deck for Q2–Q4
with modern design and speaker notes.
Target: Engineering leadership.
```

**Expected output**:
```markdown
## Roadmap Deck

### Slide 1: Title
- Q2-Q4 Product Roadmap
- Engineering Review | [Date]

### Slide 2: Executive Summary
- 3 key themes for the period
- Success metrics overview

### Slide 3: Timeline
- Gantt-style view
- Q2: Foundation | Q3: Scale | Q4: Optimize
- Key milestones marked

### Slide 4: Dependencies & Risks
- Cross-team dependencies
- Risk matrix (Impact vs Likelihood)
- Mitigation strategies

### Slide 5: Next Steps
- Immediate action items
- Review cadence
- Feedback channels
```

### Example 2: Investor Pitch Deck

**Prompt**:
```
Build a 10-slide investor pitch deck for an AI SaaS.
Include: problem, solution, market, traction, team, ask.
Series A context, $5M target.
```

**Expected output**:
- Slide-by-slide content with speaker notes
- Consistent brand styling
- Data visualization for traction
- Clear ask slide with use of funds

### Example 3: Product Demo Deck

**Prompt**:
```
Create an 8-slide product demo deck.
Audience: Potential enterprise customers.
Focus: Features, integrations, security.
```

**Expected output**:
- Feature showcase slides
- Integration diagram
- Security compliance overview
- Customer success stories
- Next steps / trial CTA

---

## Best practices

1. **One idea per slide**: 과밀 방지
2. **Visual hierarchy**: Titles > Headings > Body
3. **Use speaker notes**: 슬라이드 텍스트 최소화
4. **Data clarity**: 차트 > 텍스트 단락
5. **Consistent theming**: 색상, 폰트, 간격 통일

---

## Common pitfalls

- **테마 혼합**: 하나의 덱에 여러 스타일
- **일관성 없는 간격/타이포**: 슬라이드마다 다름
- **내러티브 흐름 없음**: 논리적 연결 부재

---

## Troubleshooting

### Issue: Slides feel inconsistent
**Cause**: 브랜드 토큰 누락
**Solution**: 템플릿 제공, 테마 강제 적용

### Issue: Slides are too dense
**Cause**: 슬라이드당 텍스트 과다
**Solution**: 콘텐츠 분할, 비주얼 활용

### Issue: Narrative unclear
**Cause**: 슬라이드 순서 문제
**Solution**: 스토리 아크 재구성

---

## Output format

```markdown
## Presentation Report

### Overview
- **Title**: [deck title]
- **Slides**: [count]
- **Duration**: [minutes]
- **Audience**: [target]

### Slide-by-Slide

#### Slide 1: [Title]
**Type**: [slide type]
**Layout**: [layout description]
**Content**:
- [content items]

**Speaker Notes**:
[notes]

---
#### Slide 2: [Title]
...

### Brand Tokens Applied
- Primary: [color]
- Font: [font family]
- Style: [tone]

### Files Delivered
- [ ] presentation.pptx
- [ ] assets.zip
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 내러티브 아크, 슬라이드 수 정합성
- **Round 2 (Analyst)**: 레이아웃 일관성, 브랜드 준수
- **Round 3 (Executor)**: 내보내기 준비 상태 체크

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 내러티브 구성, 콘텐츠 생성 |
| Gemini | 데이터 시각화 제안, 레퍼런스 리서치 |
| Codex | 템플릿 코드 생성, 자동화 |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [technical-writing](../technical-writing/SKILL.md)
- [image-generation](../../creative-media/image-generation/SKILL.md)
- [marketing-automation](../../marketing/marketing-automation/SKILL.md)

### Tags
`#presentation` `#pptx` `#slides` `#storytelling` `#branding` `#pitch-deck`
