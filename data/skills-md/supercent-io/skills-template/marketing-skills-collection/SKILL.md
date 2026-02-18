---
name: marketing-skills-collection
description: Generate marketing deliverables across CRO, copywriting, SEO, analytics, and growth using 23 specialized sub-skills with clear objectives, constraints, and validation.
tags: [marketing, cro, copywriting, seo, analytics, growth, automation]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - Write
  - Read
  - WebSearch
  - WebFetch
  - Task
---

# Marketing Skills Collection

마케팅 딜리버러블을 위한 23개 서브스킬 컬렉션입니다. CRO, 카피라이팅, SEO, 애널리틱스, 그로스 영역에서 반복 가능한 고품질 산출물을 생성합니다.

## When to use this skill

- **마케팅 딜리버러블 필요**: CRO, 카피, SEO, 분석, 그로스 산출물
- **반복 가능한 고품질 산출물**: 단일 KPI에 맞춘 에셋 생성
- **비즈니스 목표 → 스킬 매핑**: 목표를 구체적인 마케팅 서브스킬로 변환

---

## 23 Sub-Skills Overview

### CRO (Conversion Rate Optimization)
| Sub-Skill | Description |
|-----------|-------------|
| `page-cro` | 랜딩 페이지 전환율 최적화 |
| `signup-flow` | 회원가입 플로우 최적화 |
| `onboarding` | 온보딩 경험 개선 |
| `form-optimization` | 폼 최적화 (필드, UX) |
| `paywall` | 페이월/프라이싱 페이지 최적화 |

### Copywriting
| Sub-Skill | Description |
|-----------|-------------|
| `copywriting` | 광고/마케팅 카피 작성 |
| `copy-editing` | 기존 카피 개선 |
| `email-sequence` | 이메일 시퀀스 설계 |
| `social-content` | 소셜 미디어 콘텐츠 |

### SEO
| Sub-Skill | Description |
|-----------|-------------|
| `seo-audit` | SEO 감사 및 개선점 |
| `programmatic-seo` | 프로그래매틱 SEO 페이지 |
| `comparison-page` | 비교 페이지 작성 |
| `schema-markup` | 구조화된 데이터 마크업 |

### Ads & Analytics
| Sub-Skill | Description |
|-----------|-------------|
| `analytics-tracking` | 분석 트래킹 설정 |
| `paid-ads` | 유료 광고 전략/카피 |
| `ab-test` | A/B 테스트 설계 |

### Strategy & Growth
| Sub-Skill | Description |
|-----------|-------------|
| `launch-strategy` | 제품 런칭 전략 |
| `pricing-strategy` | 가격 전략 |
| `retention` | 리텐션 개선 전략 |
| `churn-analysis` | 이탈 분석 |
| `growth-experiments` | 그로스 실험 설계 |
| `referral-program` | 추천 프로그램 설계 |
| `content-strategy` | 콘텐츠 전략 수립 |

---

## Instructions

### Step 1: Define Objective and Constraints

```yaml
marketing_brief:
  objective: [단일 KPI - conversion rate, CTR, activation]
  target_audience:
    segment: [고객 세그먼트]
    pain_points: [주요 문제점]
    terminology: [사용하는 용어]
  channel: [LP, email, social, SEO, ads]
  format: [형식]
  offer:
    value_prop: [가치 제안]
    positioning: [포지셔닝]
    proof_points: [증거 포인트]
```

### Step 2: Select the Sub-Skill

상황에 맞는 서브스킬 선택:

```bash
# CRO 필요 시
→ page-cro, signup-flow, onboarding, form-optimization, paywall

# 카피 필요 시
→ copywriting, copy-editing, email-sequence, social-content

# SEO 필요 시
→ seo-audit, programmatic-seo, comparison-page, schema-markup

# 광고/분석 필요 시
→ analytics-tracking, paid-ads, ab-test

# 전략/그로스 필요 시
→ launch-strategy, pricing-strategy, retention, churn-analysis, growth-experiments
```

### Step 3: Build the Prompt

구조화된 프롬프트 작성:

```markdown
## Marketing Asset Request

### Product Context
- **Product**: [제품명]
- **Category**: [카테고리]
- **Stage**: [단계 - early, growth, mature]

### Audience
- **Segment**: [타겟 세그먼트]
- **Pain Points**: [1-3개 문제점]
- **Current State**: [현재 사용하는 솔루션]

### Offer
- **Value Prop**: [핵심 가치 제안]
- **Differentiator**: [차별화 포인트]
- **Proof**: [신뢰 요소 - 숫자, 고객사, 수상]

### Constraints
- **Tone**: [톤 - professional, casual, bold]
- **Brand Voice**: [브랜드 보이스 가이드]
- **Do NOT**: [하지 말아야 할 것들]

### Output Format
- [원하는 형식 - table, checklist, bullets]
```

### Step 4: Generate and Validate

```bash
# 생성
claude task "sub-skill명으로 마케팅 에셋 생성"

# 검증 체크리스트
- [ ] KPI 정합성
- [ ] 타겟 오디언스 적합성
- [ ] 브랜드 보이스 일관성
- [ ] 실행 가능성 (actionable)
```

### Step 5: Handoff + Measurement

```markdown
## Implementation Checklist
- [ ] 에셋 퍼블리싱
- [ ] 트래킹 이벤트 설정
- [ ] 성공 임계값 정의

## Tracking Events
| Event | Description | Success Threshold |
|-------|-------------|-------------------|
| page_view | 페이지 조회 | baseline |
| cta_click | CTA 클릭 | +20% vs control |
| signup_complete | 가입 완료 | +15% vs control |

## A/B Test Proposals
1. [가설 1]: [변형] vs [컨트롤]
2. [가설 2]: [변형] vs [컨트롤]
```

---

## Examples

### Example 1: Landing Page CRO

**Prompt**:
```
Optimize the landing page for higher signup conversion.
Audience: indie founders building side projects.
Offer: AI co-pilot for product launches.
Output: prioritized CRO changes + A/B tests.
```

**Expected output**:
- CRO checklist prioritized by impact/effort
- 3 A/B test hypotheses with expected lift
- Hero + CTA copy suggestions (3 variants each)

### Example 2: Email Sequence

**Prompt**:
```
Create a 5-email welcome sequence for a B2B SaaS.
Audience: ops managers at 50-500 employee companies.
Goal: drive first workflow setup within 7 days.
```

**Expected output**:
```markdown
## Welcome Sequence

### Email 1: Welcome (Day 0)
- **Subject**: Welcome to [Product] - Let's get started
- **Goal**: Account confirmation + quick win
- **CTA**: Complete profile

### Email 2: Value Demo (Day 1)
- **Subject**: See what [Product] can do in 2 minutes
- **Goal**: Feature awareness
- **CTA**: Watch demo video

### Email 3: First Workflow (Day 3)
- **Subject**: Create your first workflow (step-by-step)
- **Goal**: Activation milestone
- **CTA**: Create workflow

### Email 4: Use Case (Day 5)
- **Subject**: How [Customer] saved 10 hours/week
- **Goal**: Social proof + inspiration
- **CTA**: Try this template

### Email 5: Check-in (Day 7)
- **Subject**: Need help getting started?
- **Goal**: Rescue non-activated users
- **CTA**: Book a call / Reply for help

## Metrics
| Email | Open Rate Target | CTR Target |
|-------|------------------|------------|
| Email 1 | 60%+ | 30%+ |
| Email 2 | 45%+ | 15%+ |
| Email 3 | 40%+ | 20%+ |
| Email 4 | 35%+ | 12%+ |
| Email 5 | 40%+ | 15%+ |
```

### Example 3: Programmatic SEO

**Prompt**:
```
Create a programmatic SEO template for comparison pages.
Target: "[Tool A] vs [Tool B]" searches.
Include: H1, meta description, comparison table, CTA.
```

**Expected output**:
- Page template with placeholders
- Schema markup (JSON-LD)
- Internal linking strategy
- Content guidelines per section

---

## Best practices

1. **One KPI per deliverable**: 혼합 목표 방지
2. **Audience specificity**: 세그먼트별 니즈와 용어 사용
3. **Instrument measurement**: 런칭 전 트래킹 설정
4. **Iterate with data**: 산출물은 가설로 취급

---

## Common pitfalls

- **다중 목표 혼합**: 하나의 에셋에 여러 목표
- **오디언스 컨텍스트 누락**: 누구를 위한 것인지 불명확
- **트래킹/검증 계획 없음**: 효과 측정 불가

---

## Troubleshooting

### Issue: Output is generic
**Cause**: 모호한 제품/오디언스 정보
**Solution**: 포지셔닝, 경쟁사, 증거 포인트 제공

### Issue: Output conflicts with brand voice
**Cause**: 톤/보이스 제약 없음
**Solution**: 브랜드 do/don't 리스트와 샘플 카피 제공

### Issue: Can't measure impact
**Cause**: 트래킹 이벤트 미정의
**Solution**: 사전에 이벤트와 성공 임계값 정의

---

## Output format

```markdown
## Marketing Asset Report

### Brief Summary
- **Sub-Skill Used**: [sub-skill]
- **Objective**: [KPI]
- **Audience**: [segment]

### Deliverable
[generated asset]

### Implementation Checklist
- [ ] Asset ready
- [ ] Tracking configured
- [ ] Success criteria defined

### A/B Test Plan
| Test | Hypothesis | Metric | Expected Lift |
|------|------------|--------|---------------|
| Test A | [hypothesis] | [metric] | [%] |
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 5개 카테고리 23개 서브스킬 커버리지
- **Round 2 (Analyst)**: KPI 정합성, 프롬프트 구조 리뷰
- **Round 3 (Executor)**: 출력 형식, 실행 가능성 체크

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 브리프 구성, 에셋 생성 |
| Gemini | 경쟁사 리서치, 트렌드 분석 |
| Codex | 트래킹 코드 생성, 자동화 |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [presentation-builder](../../documentation/presentation-builder/SKILL.md)
- [frontend-design](../../frontend/design-system/SKILL.md)
- [image-generation](../../creative-media/image-generation/SKILL.md)

### Tags
`#marketing` `#cro` `#copywriting` `#seo` `#analytics` `#growth` `#automation`
