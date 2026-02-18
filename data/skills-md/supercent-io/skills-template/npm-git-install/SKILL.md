---
name: npm-git-install
description: Install npm packages directly from GitHub repositories using git URLs. Use when installing packages from private repos, specific branches, or unreleased versions not yet on npm registry.
tags: [npm, git, github, install, package-management, node]
platforms: [Claude, ChatGPT, Gemini, Opencode]
allowed-tools:
  - Bash
  - Read
  - Write
---

# npm install Git Repository Guide

GitHub 리포지토리에서 직접 npm 패키지를 설치하는 방법을 다룹니다. npm 레지스트리에 없는 패키지, 특정 브랜치, 프라이빗 리포지토리 설치에 유용합니다.

## When to use this skill

- **npm에 없는 패키지**: 아직 퍼블리시되지 않은 패키지 설치
- **특정 브랜치/태그**: main, develop, 특정 릴리스 태그 설치
- **프라이빗 리포지토리**: 조직 내부 패키지 설치
- **포크된 패키지**: 수정된 포크 버전 사용
- **최신 커밋 테스트**: 릴리스 전 최신 코드 테스트

---

## 1. 설치 명령어

### 기본 문법

```bash
npm install git+https://github.com/<owner>/<repo>.git#<branch|tag|commit>
```

### HTTPS 방식 (일반적)

```bash
# 특정 브랜치
npm install -g git+https://github.com/JEO-tech-ai/supercode.git#main

# 특정 태그
npm install git+https://github.com/owner/repo.git#v1.0.0

# 특정 커밋
npm install git+https://github.com/owner/repo.git#abc1234

# 기본 브랜치 (# 생략 시)
npm install git+https://github.com/owner/repo.git
```

### SSH 방식 (SSH 키 설정된 경우)

```bash
npm install -g git+ssh://git@github.com:JEO-tech-ai/supercode.git#main
```

### 상세 로그 보기

```bash
npm install -g git+https://github.com/JEO-tech-ai/supercode.git#main --verbose
```

---

## 2. npm install 플로우

Git URL로 설치할 때 npm이 수행하는 과정:

```
1. Git Clone
   └─ 지정된 브랜치(#main)의 리포지토리 복제
        ↓
2. 의존성 설치
   └─ package.json의 dependencies 설치
        ↓
3. Prepare 스크립트 실행
   └─ "prepare" 스크립트 실행 (TypeScript 컴파일, 빌드 등)
        ↓
4. 글로벌 바이너리 등록
   └─ bin 필드의 실행 파일을 글로벌 경로에 링크
```

### 내부 동작

```bash
# npm이 내부적으로 수행하는 작업
git clone https://github.com/owner/repo.git /tmp/npm-xxx
cd /tmp/npm-xxx
git checkout main
npm install
npm run prepare  # 있으면 실행
cp -r . /usr/local/lib/node_modules/repo/
ln -s ../lib/node_modules/repo/bin/cli.js /usr/local/bin/repo
```

---

## 3. 설치 위치 확인

```bash
# 글로벌 npm 경로 확인
npm root -g
# macOS/Linux: /usr/local/lib/node_modules
# Windows: C:\Users\<username>\AppData\Roaming\npm\node_modules

# 설치된 패키지 확인
npm list -g <package-name>

# 바이너리 위치 확인
which <command>
# 또는
npm bin -g
```

### 플랫폼별 설치 위치

| 플랫폼 | 패키지 위치 | 바이너리 위치 |
|-------|------------|--------------|
| macOS/Linux | `/usr/local/lib/node_modules/` | `/usr/local/bin/` |
| Windows | `%AppData%\npm\node_modules\` | `%AppData%\npm\` |
| nvm (macOS) | `~/.nvm/versions/node/vX.X.X/lib/node_modules/` | `~/.nvm/versions/node/vX.X.X/bin/` |

---

## 4. package.json에 의존성 추가

### dependencies에 Git URL 사용

```json
{
  "dependencies": {
    "supercode": "git+https://github.com/JEO-tech-ai/supercode.git#main",
    "my-package": "git+ssh://git@github.com:owner/repo.git#v1.0.0",
    "another-pkg": "github:owner/repo#branch"
  }
}
```

### 단축 문법

```json
{
  "dependencies": {
    "pkg1": "github:owner/repo",
    "pkg2": "github:owner/repo#branch",
    "pkg3": "github:owner/repo#v1.0.0",
    "pkg4": "github:owner/repo#commit-sha"
  }
}
```

---

## 5. 프라이빗 리포지토리 설치

### SSH 키 방식 (권장)

```bash
# 1. SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. GitHub에 공개키 등록
cat ~/.ssh/id_ed25519.pub
# GitHub → Settings → SSH Keys → New SSH Key

# 3. SSH 방식으로 설치
npm install git+ssh://git@github.com:owner/private-repo.git
```

### Personal Access Token 방식

```bash
# 1. GitHub에서 PAT 생성
# GitHub → Settings → Developer settings → Personal access tokens

# 2. 토큰 포함 URL로 설치
npm install git+https://<token>@github.com/owner/private-repo.git

# 3. 환경변수 사용 (보안 권장)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
npm install git+https://${GITHUB_TOKEN}@github.com/owner/private-repo.git
```

### .npmrc 설정

```bash
# ~/.npmrc
//github.com/:_authToken=${GITHUB_TOKEN}
```

---

## 6. 자주 발생하는 오류 & 해결

### Permission denied (EACCES)

```bash
# 방법 1: 소유권 변경
sudo chown -R $(whoami) /usr/local/lib/node_modules

# 방법 2: npm 디렉토리 변경 (권장)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Git이 설치되지 않음

```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Windows
# https://git-scm.com/download/win
```

### GitHub 인증 오류

```bash
# SSH 연결 테스트
ssh -T git@github.com

# 인증 정보 캐시
git config --global credential.helper store
# 또는 macOS
git config --global credential.helper osxkeychain
```

### prepare 스크립트 실패

```bash
# TypeScript 프로젝트인 경우
npm install -g typescript

# 빌드 실패 시 상세 로그
npm install git+https://... --verbose 2>&1 | tee npm-install.log
```

### 캐시 문제

```bash
# npm 캐시 삭제
npm cache clean --force

# 재설치
npm uninstall -g <package>
npm install -g git+https://...
```

---

## 7. 업데이트 & 관리

### 업데이트

```bash
# 최신 버전으로 업데이트 (재설치)
npm uninstall -g <package>
npm install -g git+https://github.com/owner/repo.git#main

# package.json 의존성 업데이트
npm update <package>
```

### 버전 확인

```bash
# 설치된 버전 확인
npm list -g <package>

# 원격 최신 커밋 확인
git ls-remote https://github.com/owner/repo.git HEAD
```

### 제거

```bash
npm uninstall -g <package>
```

---

## 8. Cursor/VS Code 확장 통합 예시

### Supercode 설치 예시

```bash
# 글로벌 설치
npm install -g git+https://github.com/JEO-tech-ai/supercode.git#main

# 설치 확인
supercode --version
```

### 프로젝트 설정 파일

```json
// .supercoderc 또는 supercode.config.json
{
  "aiRules": {
    "enabled": true,
    "techStack": ["TypeScript", "React", "Node.js"]
  },
  "smartActions": [
    {
      "name": "Generate Documentation",
      "icon": "docs",
      "prompt": "Generate comprehensive documentation"
    }
  ],
  "architectureMode": {
    "enabled": true,
    "detailLevel": "detailed"
  }
}
```

---

## 9. Best Practices

### DO (권장)

1. **특정 버전/태그 사용**: `#v1.0.0` 형태로 버전 고정
2. **SSH 방식 선호**: 프라이빗 리포 접근 시 SSH 키 사용
3. **환경변수로 토큰 관리**: PAT는 환경변수로 관리
4. **lockfile 커밋**: package-lock.json 커밋으로 재현성 확보
5. **verbose 옵션 활용**: 문제 발생 시 상세 로그 확인

### DON'T (금지)

1. **토큰 하드코딩**: package.json에 토큰 직접 입력 금지
2. **최신 커밋 의존**: 프로덕션에서 `#main` 대신 태그 사용
3. **sudo 남용**: 권한 문제는 디렉토리 설정으로 해결
4. **캐시 무시**: 이상 동작 시 캐시 클리어 필수

---

## Constraints

### 필수 규칙 (MUST)

1. **Git 설치 필수**: npm git URL 설치 전 git 설치 확인
2. **네트워크 접근**: GitHub에 접근 가능한 환경 필요
3. **Node.js 버전**: package.json의 engines 필드 확인

### 금지 사항 (MUST NOT)

1. **인증 토큰 노출**: 로그, 코드에 토큰 노출 금지
2. **무분별한 sudo**: 권한 문제는 설정으로 해결
3. **프로덕션에서 #main**: 특정 버전/태그로 고정

---

## References

- [npm-install 공식 문서](https://docs.npmjs.com/cli/v9/commands/npm-install/)
- [How To Install NPM Packages Directly From GitHub](https://www.warp.dev/terminus/npm-install-from-github)
- [npm install from GitHub - Stack Overflow](https://stackoverflow.com/questions/17509669/how-to-install-an-npm-package-from-github-directly)
- [Working with the npm registry - GitHub Docs](https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-npm-registry)

---

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2026-01-10
- **호환 플랫폼**: Claude, ChatGPT, Gemini, Opencode

### 관련 스킬
- [environment-setup](../environment-setup/SKILL.md)
- [git-workflow](../git-workflow/SKILL.md)

### 태그
`#npm` `#git` `#github` `#install` `#package-management` `#node`
