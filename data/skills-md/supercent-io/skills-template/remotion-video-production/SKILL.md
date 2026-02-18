---
name: remotion-video-production
description: Produce programmable videos with Remotion using scene planning, asset orchestration, and validation gates for automated, brand-consistent video content.
tags: [video, remotion, animation, storytelling, automation, react]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - Bash
  - Write
  - Read
  - Task
---

# Remotion Video Production

Remotion을 사용한 프로그래머블 비디오 제작 스킬입니다. 텍스트 지침에서 자동화된 비디오를 생성하고, 일관된 브랜드 비디오를 대규모로 제작합니다.

## When to use this skill

- **자동화된 비디오 생성**: 텍스트 지침에서 비디오 생성
- **브랜드 비디오 제작**: 일관된 스타일의 대규모 비디오
- **프로그래머블 콘텐츠**: 내레이션, 비주얼, 애니메이션 통합
- **마케팅 콘텐츠**: 제품 소개, 온보딩, 프로모션 비디오

---

## Instructions

### Step 1: Define the Video Spec

```yaml
video_spec:
  audience: [타겟 오디언스]
  goal: [비디오 목적]
  duration: [총 길이 - 30s, 60s, 90s]
  aspect_ratio: "16:9" | "1:1" | "9:16"
  tone: "fast" | "calm" | "cinematic"
  voice:
    style: [내레이션 스타일]
    language: [언어]
```

### Step 2: Outline Scenes

씬 구조화 템플릿:

```markdown
## Scene Plan

### Scene 1: Hook (0:00 - 0:05)
- **Visual**: 제품 로고 페이드인
- **Audio**: 업비트 인트로
- **Text**: "Transform Your Workflow"
- **Transition**: 페이드 → Scene 2

### Scene 2: Problem (0:05 - 0:15)
- **Visual**: 문제 상황 일러스트
- **Audio**: 내레이션 시작
- **Text**: 핵심 메시지 오버레이
- **Transition**: 슬라이드 좌측

### Scene 3: Solution (0:15 - 0:30)
...
```

### Step 3: Prepare Assets

```bash
# 에셋 체크리스트
assets/
├── logos/
│   ├── logo-main.svg
│   └── logo-white.svg
├── screenshots/
│   ├── dashboard.png
│   └── feature-1.png
├── audio/
│   ├── bgm.mp3
│   └── narration.mp3
└── fonts/
    └── brand-font.woff2
```

**에셋 준비 규칙**:
- 로고: SVG 또는 고해상도 PNG
- 스크린샷: 비율에 맞게 정규화
- 오디오: MP3 또는 WAV, 볼륨 정규화
- 폰트: 웹폰트 또는 로컬 폰트 파일

### Step 4: Implement Remotion Composition

```tsx
// src/Video.tsx
import { Composition } from 'remotion';
import { IntroScene } from './scenes/IntroScene';
import { ProblemScene } from './scenes/ProblemScene';
import { SolutionScene } from './scenes/SolutionScene';
import { CTAScene } from './scenes/CTAScene';

export const RemotionVideo: React.FC = () => {
  return (
    <>
      <Composition
        id="ProductIntro"
        component={ProductIntro}
        durationInFrames={1800} // 60s at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

// Scene Component Example
const IntroScene: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <AbsoluteFill style={{ opacity }}>
      <Logo />
      <Title>Transform Your Workflow</Title>
    </AbsoluteFill>
  );
};
```

### Step 5: Render and QA

```bash
# 1. 프리뷰 렌더링 (저품질)
npx remotion preview src/Video.tsx

# 2. QA 체크
- [ ] 타이밍 확인
- [ ] 오디오 싱크
- [ ] 텍스트 가독성
- [ ] 전환 부드러움

# 3. 최종 렌더링
npx remotion render src/Video.tsx ProductIntro out/video.mp4
```

---

## Examples

### Example 1: Product Intro Video

**Prompt**:
```
Create a 60s product intro video with 6 scenes,
upbeat tone, and 16:9 output. Include a CTA at the end.
```

**Expected output**:
```markdown
## Scene Breakdown
1. Hook (0:00-0:05): Logo + tagline
2. Problem (0:05-0:15): Pain point visualization
3. Solution (0:15-0:30): Product demo
4. Features (0:30-0:45): Key benefits (3 items)
5. Social Proof (0:45-0:55): Testimonial/stats
6. CTA (0:55-1:00): Call to action + contact

## Remotion Structure
- src/scenes/HookScene.tsx
- src/scenes/ProblemScene.tsx
- src/scenes/SolutionScene.tsx
- src/scenes/FeaturesScene.tsx
- src/scenes/SocialProofScene.tsx
- src/scenes/CTAScene.tsx
```

### Example 2: Onboarding Walkthrough

**Prompt**:
```
Generate a 45s onboarding walkthrough using screenshots,
with callouts and 9:16 format for mobile.
```

**Expected output**:
- Scene plan with 5 steps
- Asset list (screenshots, callout arrows)
- Text overlays and transitions
- Mobile-safe margins applied

---

## Best practices

1. **Short scenes**: 씬당 5-10초로 명확하게
2. **Consistent typography**: 타이포그래피 스케일 정의
3. **Audio sync**: 내레이션 큐와 비주얼 정렬
4. **Template reuse**: 재사용 가능한 컴포지션 저장
5. **Safe zones**: 모바일 비율 시 여백 확보

---

## Common pitfalls

- **텍스트 과부하**: 씬당 텍스트 양 제한
- **모바일 세이프존 무시**: 9:16 비율 시 가장자리 확인
- **QA 전 최종 렌더링**: 항상 프리뷰 먼저 확인

---

## Troubleshooting

### Issue: Audio and visuals out of sync
**Cause**: 프레임 타이밍 불일치
**Solution**: 프레임 재계산 및 타임스탬프 정렬

### Issue: Render is slow or fails
**Cause**: 무거운 에셋 또는 효과
**Solution**: 에셋 압축 및 애니메이션 단순화

### Issue: Text unreadable
**Cause**: 폰트 크기 또는 대비 부족
**Solution**: 최소 24px 폰트, 고대비 색상 사용

---

## Output format

```markdown
## Video Production Report

### Spec
- Duration: 60s
- Aspect Ratio: 16:9
- FPS: 30

### Scene Plan
| Scene | Duration | Visual | Audio | Transition |
|-------|----------|--------|-------|------------|
| Hook  | 0:00-0:05 | Logo fade | BGM start | Fade |
| ...   | ...      | ...    | ...   | ...  |

### Assets
- [ ] logo.svg
- [ ] screenshots (3)
- [ ] bgm.mp3
- [ ] narration.mp3

### Render Checklist
- [ ] Preview QA passed
- [ ] Audio sync verified
- [ ] Safe zones checked
- [ ] Final render complete
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 스펙 완전성, 씬 커버리지
- **Round 2 (Analyst)**: 내러티브 일관성, 페이싱 리뷰
- **Round 3 (Executor)**: 렌더 준비 상태 체크리스트 검증

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 씬 플래닝, 스크립트 작성 |
| Gemini | 에셋 분석, 최적화 제안 |
| Codex | Remotion 코드 생성, 렌더링 실행 |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [image-generation](../image-generation/SKILL.md)
- [presentation-builder](../../documentation/presentation-builder/SKILL.md)
- [frontend-design](../../frontend/design-system/SKILL.md)

### Tags
`#video` `#remotion` `#animation` `#storytelling` `#automation` `#react`
