---
name: vercel-deploy
description: Deploy applications and websites to Vercel instantly. Use when asked to "Deploy my app", "Deploy this to production", "Create a preview deployment", or "Push this live". No authentication required - returns preview URL and claimable deployment link.
tags: [deployment, vercel, preview, production, hosting, serverless]
platforms: [Claude]
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel Deploy

Deploy any project to Vercel instantly. No authentication required.

## When to use this skill

- **앱 배포**: "Deploy my app" 요청 시
- **프리뷰 배포**: "Create a preview deployment" 요청 시
- **프로덕션 배포**: "Deploy this to production" 요청 시
- **링크 공유**: "Deploy and give me the link" 요청 시

## How It Works

1. Packages your project into a tarball (excludes `node_modules` and `.git`)
2. Auto-detects framework from `package.json`
3. Uploads to deployment service
4. Returns **Preview URL** (live site) and **Claim URL** (transfer to your Vercel account)

## Instructions

### Step 1: 프로젝트 준비

배포할 프로젝트 디렉토리를 확인합니다.

**지원 프레임워크**:
- **React**: Next.js, Gatsby, Create React App, Remix, React Router
- **Vue**: Nuxt, Vitepress, Vuepress, Gridsome
- **Svelte**: SvelteKit, Svelte, Sapper
- **Other Frontend**: Astro, Solid Start, Angular, Ember, Preact, Docusaurus
- **Backend**: Express, Hono, Fastify, NestJS, Elysia, h3, Nitro
- **Build Tools**: Vite, Parcel
- **And more**: Blitz, Hydrogen, RedwoodJS, Storybook, Sanity, etc.

### Step 2: 배포 실행

**스크립트 사용** (claude.ai 환경):
```bash
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh [path]
```

**Arguments:**
- `path` - Directory to deploy, or a `.tgz` file (defaults to current directory)

**Examples:**
```bash
# Deploy current directory
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh

# Deploy specific project
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project

# Deploy existing tarball
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project.tgz
```

### Step 3: 결과 확인

배포 성공 시 두 개의 URL이 반환됩니다:
- **Preview URL**: 즉시 접근 가능한 라이브 사이트
- **Claim URL**: Vercel 계정으로 배포 이전

## Output Format

### 콘솔 출력

```
Preparing deployment...
Detected framework: nextjs
Creating deployment package...
Deploying...
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

### JSON 출력 (프로그래밍 용)

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## Static HTML Projects

For projects without a `package.json`:
- If there's a single `.html` file not named `index.html`, it gets renamed automatically
- This ensures the page is served at the root URL (`/`)

## Present Results to User

Always show both URLs:

```
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...

View your site at the Preview URL.
To transfer this deployment to your Vercel account, visit the Claim URL.
```

## Troubleshooting

### Network Egress Error

If deployment fails due to network restrictions (common on claude.ai), tell the user:

```
Deployment failed due to network restrictions. To fix this:

1. Go to https://claude.ai/settings/capabilities
2. Add *.vercel.com to the allowed domains
3. Try deploying again
```

### Framework Not Detected

프레임워크가 감지되지 않으면:
1. `package.json` 존재 여부 확인
2. dependencies에 프레임워크 패키지 포함 확인
3. 수동으로 `framework` 파라미터 지정

## Constraints

### 필수 규칙 (MUST)

1. **두 URL 모두 표시**: Preview URL과 Claim URL 모두 사용자에게 표시
2. **프레임워크 감지**: package.json에서 자동 감지
3. **에러 메시지 표시**: 배포 실패 시 명확한 에러 메시지

### 금지 사항 (MUST NOT)

1. **node_modules 포함**: tarball에 node_modules 포함하지 않음
2. **.git 포함**: tarball에 .git 디렉토리 포함하지 않음
3. **인증 정보 하드코딩**: 인증 필요 없음 (claimable deploy)

## Best practices

1. **프레임워크 자동 감지**: package.json 분석으로 최적 설정
2. **Clean Tarball**: node_modules, .git 제외로 빠른 업로드
3. **명확한 출력**: Preview URL과 Claim URL 구분 표시

## References

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel CLI](https://vercel.com/docs/cli)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2026-01-22
- **호환 플랫폼**: Claude (claude.ai)
- **원본 출처**: vercel/agent-skills

### 관련 스킬
- [deployment-automation](../deployment-automation/SKILL.md): CI/CD 및 Docker/K8s 배포

### 태그
`#deployment` `#vercel` `#preview` `#production` `#hosting` `#serverless` `#infrastructure`
