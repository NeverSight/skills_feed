---
name: readme-writing
description: A skill for writing and optimizing a project's README.md file in accordance with standard conventions and templates. It ensures compliance with standards and maintains documentation quality when creating, reviewing, or refactoring project documentation. This skill is triggered during tasks related to README generation and documentation updates.
---

# README 작성 가이드

이 스킬은 프로젝트의 README.md 파일을 작성하거나 업데이트할 때 사용합니다. 아래의 작성 규칙과 템플릿을 엄격히 준수하십시오.

## 작성 규칙

### 핵심 원칙

1. **사실 기반 작성**: 모든 `{placeholder}`는 실제 프로젝트 파일/폴더/코드/설정에서 추출한 정보로 채운다.
2. **허구 금지**: 존재하지 않는 파일, 폴더, 환경변수, 기능을 생성하거나 언급하지 않는다.
3. **간결성**: 불필요한 형용사 없이 명확하고 간결하게 작성한다.
4. **한국어 우선**: 고유명사(기술명, 라이브러리명 등)를 제외한 모든 내용은 한국어로 작성한다.

### 섹션 선택 기준

| 섹션                | 필수 | 포함 조건                                               |
| ------------------- | :--: | ------------------------------------------------------- |
| Overview            |  ✅  | 항상 포함                                               |
| Tech Stack          |  ✅  | 항상 포함                                               |
| Architecture        |  ⚪  | 서비스 간 통신 또는 외부 의존성이 있는 경우             |
| Directory Structure |  ✅  | 항상 포함                                               |
| Configuration       |  ⚪  | `.env.example` 또는 `config/` 폴더가 존재하는 경우      |
| Quick Start         |  ✅  | 항상 포함                                               |
| Operations Guide    |  ⚪  | `docker-compose.yml` 또는 배포 스크립트가 존재하는 경우 |
| Troubleshooting     |  ⚪  | 알려진 이슈가 있는 경우                                 |
| Contributing        |  ⚪  | 오픈소스 또는 `CONTRIBUTING.md`가 존재하는 경우         |
| License             |  ⚪  | `LICENSE` 파일이 존재하는 경우                          |

**프로젝트 유형 판단 기준:**

- **오픈소스**: `LICENSE` 파일 존재, public 저장소
- **내부 프로젝트**: `LICENSE` 없음, private 저장소 → Contributing, License 섹션 생략

### 섹션별 작성 지침

| 섹션          | 참조 소스                                 | 작성 방법                         |
| ------------- | ----------------------------------------- | --------------------------------- |
| Overview      | pyproject.toml, package.json, 코드 주석   | 배경-문제-목표 구조로 3~6줄 작성  |
| Tech Stack    | pyproject.toml, package.json, Dockerfile  | 실제 사용 중인 기술만 배지로 표시 |
| Architecture  | 코드 구조, Dockerfile, docker-compose.yml | Mermaid 다이어그램으로 작성       |
| Directory     | 프로젝트 루트 기준 tree 명령              | 주요 폴더만 선별하여 역할 설명    |
| Configuration | .env.example, config 폴더                 | 실제 환경변수와 설정 파일만 기재  |
| Quick Start   | main.py, entrypoint, 빌드 스크립트        | 실제 테스트된 명령어만 기재       |
| Operations    | docker-compose.yml, 배포 스크립트         | 실제 운영 환경 기준 작성          |

### 참조 데이터 우선순위

AI는 다음 파일들을 순서대로 분석하여 README를 작성한다:

1. **의존성 정의**: `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`
2. **락 파일**: `uv.lock`, `package-lock.json`, `Cargo.lock`
3. **인프라 설정**: `Dockerfile`, `docker-compose.yml`, `k8s/` 폴더
4. **환경 설정**: `.env.example`, `config/` 폴더
5. **진입점**: `main.py`, `app.py`, `index.ts`, `main.go`
6. **프로젝트 구조**: `tree -a -I 'node_modules|__pycache__|.git|.venv'`

---

## README 표준 템플릿

````markdown
# {Project Name}

{한 줄 프로젝트 설명}

[![{Language}](https://img.shields.io/badge/{Language}-{Version}-blue?logo={logo})]()
[![License](https://img.shields.io/badge/License-{License}-green.svg)]()

[시작하기](#-quick-start) · [문서](#-documentation)

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Directory Structure](#-directory-structure)
- [Configuration](#-configuration)
- [Quick Start](#-quick-start)
- [Operations Guide](#-operations-guide)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

## 📘 Overview

### 배경

{프로젝트가 시작된 배경과 맥락}

### 해결하려는 문제

- {핵심 문제 1}
- {핵심 문제 2}
- {핵심 문제 3}

### 목표

{이 프로젝트가 달성하려는 구체적인 목표}

### 주요 기능

- **{기능명 1}**: {설명}
- **{기능명 2}**: {설명}
- **{기능명 3}**: {설명}

> 🔗 상세 기획: [{문서명}]({Notion URL})

## 🛠 Tech Stack

| Category       | Technology     | Version |
| -------------- | -------------- | ------- |
| Language       | {언어명}       | {버전}  |
| Framework      | {프레임워크명} | {버전}  |
| Database       | {DB명}         | {버전}  |
| Infrastructure | {인프라}       | {버전}  |

### 기술 선택 근거

| 기술     | 선택 이유   | 검토했던 대안       |
| -------- | ----------- | ------------------- |
| {기술명} | {선택 이유} | {대안 및 제외 이유} |

## 🏗 Architecture

### System Overview

```mermaid
flowchart TB
    subgraph Client
        A[{클라이언트 유형}]
    end

    subgraph Service
        B[{서비스/API}]
        C[{처리 로직}]
    end

    subgraph Data
        D[(Database)]
        E[{외부 서비스}]
    end

    A --> B
    B --> C
    C --> D
    C --> E
```

### Data Flow

```mermaid
flowchart LR
    A[{입력}] --> B[{처리 1}]
    B --> C[{처리 2}]
    C --> D[{출력}]
    B --> E[(저장소)]
```

### 주요 컴포넌트

| 컴포넌트     | 역할        | 기술        |
| ------------ | ----------- | ----------- |
| {컴포넌트명} | {역할 설명} | {사용 기술} |

> 🔗 아키텍처 상세: [{문서명}]({링크})

## 📁 Directory Structure

```text
{project-root}/
├── src/               # 소스 코드
│   ├── {folder}/     # {역할}
│   └── {folder}/     # {역할}
├── tests/            # 테스트 코드
├── config/           # 설정 파일
├── {file}            # {역할}
└── README.md
```

### 폴더별 상세 설명

| 폴더       | 역할   | 주요 파일     |
| ---------- | ------ | ------------- |
| `{폴더명}` | {역할} | {주요 파일들} |

## ⚙ Configuration

### 환경 변수

| 변수명      | 필수 | 설명   | 기본값   | 예시   |
| ----------- | :--: | ------ | -------- | ------ |
| `{ENV_VAR}` |  ✅  | {설명} | {기본값} | {예시} |
| `{ENV_VAR}` |  ⚪  | {설명} | {기본값} | {예시} |

### 설정 파일

| 파일       | 용도   |
| ---------- | ------ |
| `{파일명}` | {용도} |

### 환경별 설정

| 환경       | 설정 파일 | 특이사항   |
| ---------- | --------- | ---------- |
| Local      | {파일명}  | {특이사항} |
| Production | {파일명}  | {특이사항} |

> 🔗 환경 설정 가이드: [{문서명}]({링크})

## ⚡ Quick Start

### 요구사항

- {Runtime}: {버전}
- {Package Manager}: {버전}
- {기타 의존성}

### 설치

```bash
# 1. 저장소 클론
git clone {repository_url}
cd {project_name}

# 2. 환경 설정
cp .env.example .env

# 3. 의존성 설치
{install_command}
```

### 실행

```bash
# 로컬 개발
{run_command}

# Docker 실행 (선택)
docker-compose up -d
```

### 동작 확인

```bash
{health_check_command}
```

### 테스트

```bash
{test_command}
```

## 🛠 Operations Guide

### 배포

| 환경   | 방법   | 명령어     |
| ------ | ------ | ---------- |
| {환경} | {방법} | `{명령어}` |

### 서비스 관리

```bash
# 서비스 상태 확인
{status_command}

# 서비스 재시작
{restart_command}
```

### 로그 확인

```bash
{log_command}
```

### 모니터링

| 항목   | 도구     | 접근 방법       |
| ------ | -------- | --------------- |
| {항목} | {도구명} | {URL 또는 명령} |

> 🔗 운영 매뉴얼: [{문서명}]({링크})

## 🧩 Troubleshooting

### 자주 발생하는 문제

#### {에러 메시지 또는 증상}

- **원인**: {원인 설명}
- **해결**: {해결 방법}

### 알려진 제약사항

| 제약사항 | 영향   | 대응 방안 |
| -------- | ------ | --------- |
| {제약}   | {영향} | {대응}    |

## 🤝 Contributing

프로젝트 기여를 환영합니다.

1. 이 저장소를 Fork합니다
2. Feature 브랜치를 생성합니다 (`git checkout -b feature/{feature-name}`)
3. 변경사항을 커밋합니다 (`git commit -m 'feat: {description}'`)
4. 브랜치에 Push합니다 (`git push origin feature/{feature-name}`)
5. Pull Request를 생성합니다

### 커밋 컨벤션

| Type       | 설명             |
| ---------- | ---------------- |
| `feat`     | 새로운 기능 추가 |
| `fix`      | 버그 수정        |
| `docs`     | 문서 수정        |
| `refactor` | 리팩토링         |
| `test`     | 테스트 추가/수정 |
| `chore`    | 빌드, 설정 변경  |

## 📚 Documentation

| 문서     | 설명   | 링크               |
| -------- | ------ | ------------------ |
| {문서명} | {설명} | [{문서명}]({링크}) |

## 📄 License

이 프로젝트는 [{라이선스명}] 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
````
