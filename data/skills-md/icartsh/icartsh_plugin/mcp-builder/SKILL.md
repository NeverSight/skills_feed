---
name: mcp-builder
description: LLM이 잘 설계된 도구를 통해 외부 서비스와 상호작용할 수 있게 해주는 고품질 MCP (Model Context Protocol) 서버를 만들기 위한 가이드입니다. Python (FastMCP) 또는 Node/TypeScript (MCP SDK)를 사용하여 외부 API나 서비스를 통합하는 MCP 서버를 구축할 때 사용하세요.
license: LICENSE.txt의 전체 약관 참조
---

# MCP Server Development Guide

## 개요 (Overview)

LLM이 잘 설계된 도구를 통해 외부 서비스와 상호작용할 수 있게 해주는 MCP (Model Context Protocol) 서버를 생성하세요. MCP 서버의 품질은 LLM이 실제 작업을 얼마나 잘 수행할 수 있게 하는지에 따라 결정됩니다.

---

# 프로세스 (Process)

## 🚀 워크플로우 개요 (High-Level Workflow)

고품질 MCP 서버를 만드는 과정은 크게 네 단계로 나뉩니다:

### Phase 1: 심층 조사 및 계획 (Deep Research and Planning)

#### 1.1 최신 MCP 설계 이해

**API 커버리지 vs. 워크플로우 도구:**
포괄적인 API 엔드포인트 커버리지와 특화된 워크플로우 도구 사이의 균형을 맞추세요. 워크플로우 도구는 특정 작업에 더 편리할 수 있으며, 포괄적인 커버리지는 에이전트(agent)가 작업을 자유롭게 구성할 수 있는 유연성을 제공합니다. 성능은 클라이언트에 따라 다릅니다—일부 클라이언트는 기본 도구들을 조합하는 코드 실행 방식이 효율적이며, 다른 클라이언트는 상위 수준의 워크플로우 도구가 더 잘 작동합니다. 확실하지 않을 때는 포괄적인 API 커버리지를 우선시하세요.

**도구 명명 및 발견 가능성 (Tool Naming and Discoverability):**
명확하고 설명적인 도구 이름은 에이전트가 적절한 도구를 빠르게 찾는 데 도움이 됩니다. 일관된 접두사(예: `github_create_issue`, `github_list_repos`)를 사용하고 동작 중심의 이름을 지으세요.

**컨텍스트 관리 (Context Management):**
에이전트는 간결한 도구 설명과 결과 필터링/페이지네이션 기능이 있을 때 더 효율적으로 작동합니다. 집중적이고 관련성 높은 데이터를 반환하도록 도구를 설계하세요. 일부 클라이언트는 코드 실행을 지원하며, 이는 에이전트가 데이터를 효율적으로 필터링하고 처리하는 데 도움이 됩니다.

**실행 가능한 에러 메시지 (Actionable Error Messages):**
에러 메시지는 구체적인 제안과 다음 단계를 제시하여 에이전트가 해결책을 찾을 수 있도록 안내해야 합니다.

#### 1.2 MCP 프로토콜 문서 학습

**MCP 사양 탐색:**

먼저 사이트맵에서 관련 페이지를 찾으세요: `https://modelcontextprotocol.io/sitemap.xml`

그 다음, 마크다운 형식을 위해 `.md` 접미사가 붙은 특정 페이지를 가져오세요 (예: `https://modelcontextprotocol.io/specification/draft.md`).

검토해야 할 주요 페이지:
- 사양 개요 및 아키텍처
- 전송 메커니즘 (streamable HTTP, stdio)
- 도구(Tool), 리소스(Resource), 프롬프트(Prompt) 정의

#### 1.3 프레임워크 문서 학습

**권장 스택:**
- **언어**: TypeScript (고품질 SDK 지원 및 MCPB 등 다양한 실행 환경에서 좋은 호환성 제공. 또한 AI 모델들이 광범위한 사용량, 정적 타이핑 및 우수한 린팅 도구 덕분에 TypeScript 코드를 생성하는 데 능숙함)
- **전송(Transport)**: 원격 서버의 경우 상태 비저장(stateless) JSON을 사용하는 Streamable HTTP (상태 저장 세션 및 스트리밍 응답에 비해 확장 및 유지보수가 간단함). 로컬 서버의 경우 stdio 사용.

**프레임워크 문서 로드:**

- **MCP Best Practices**: [📋 Best Practices 보기](./reference/mcp_best_practices.md) - 핵심 가이드라인

**TypeScript용 (권장):**
- **TypeScript SDK**: WebFetch를 사용하여 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 로드
- [⚡ TypeScript 가이드](./reference/node_mcp_server.md) - TypeScript 패턴 및 예시

**Python용:**
- **Python SDK**: WebFetch를 사용하여 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 로드
- [🐍 Python 가이드](./reference/python_mcp_server.md) - Python 패턴 및 예시

#### 1.4 구현 계획 수립

**API 이해:**
핵심 엔드포인트, 인증 요구 사항 및 데이터 모델을 식별하기 위해 서비스의 API 문서를 검토하세요. 필요에 따라 웹 검색과 WebFetch를 활용하세요.

**도구 선택:**
포괄적인 API 커버리지를 우선시하세요. 가장 일반적인 작업부터 시작하여 구현할 엔드포인트 목록을 만듭니다.

---

### Phase 2: 구현 (Implementation)

#### 2.1 프로젝트 구조 설정

프로젝트 설정에 대해서는 언어별 가이드를 참조하세요:
- [⚡ TypeScript 가이드](./reference/node_mcp_server.md) - 프로젝트 구조, package.json, tsconfig.json
- [🐍 Python 가이드](./reference/python_mcp_server.md) - 모듈 조직, 종속성

#### 2.2 핵심 인프라 구현

공용 유틸리티 생성:
- 인증 기능이 포함된 API 클라이언트
- 에러 핸들링 헬퍼
- 응답 포맷팅 (JSON/Markdown)
- 페이지네이션 지원

#### 2.3 도구 구현 (Implement Tools)

각 도구별로 다음을 수행하세요:

**입력 스키마 (Input Schema):**
- Zod (TypeScript) 또는 Pydantic (Python) 사용
- 제약 조건과 명확한 설명 포함
- 필드 설명에 예시 추가

**출력 스키마 (Output Schema):**
- 구조화된 데이터를 위해 가능한 경우 `outputSchema` 정의
- 도구 응답에서 `structuredContent` 사용 (TypeScript SDK 기능)
- 클라이언트가 도구 출력을 이해하고 처리하는 데 도움을 줌

**도구 설명 (Tool Description):**
- 기능에 대한 간결한 요약
- 파라미터 설명
- 반환 타입 스키마

**구현:**
- I/O 작업을 위한 Async/await 사용
- 실행 가능한 메시지를 포함한 적절한 에러 핸들링
- 해당되는 경우 페이지네이션 지원
- 최신 SDK 사용 시 텍스트 콘텐츠와 구조화된 데이터 모두 반환

**어노테이션 (Annotations):**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: 검토 및 테스트 (Review and Test)

#### 3.1 코드 품질

다음을 검토하세요:
- 중복 코드 없음 (DRY 원칙)
- 일관된 에러 핸들링
- 완전한 타입 커버리지
- 명확한 도구 설명

#### 3.2 빌드 및 테스트

**TypeScript:**
- 컴파일 확인을 위해 `npm run build` 실행
- MCP Inspector로 테스트: `npx @modelcontextprotocol/inspector`

**Python:**
- 구문 확인: `python -m py_compile your_server.py`
- MCP Inspector로 테스트

상세한 테스트 접근 방식과 품질 체크리스트는 언어별 가이드를 참조하세요.

---

### Phase 4: 평가 생성 (Create Evaluations)

MCP 서버를 구현한 후, 그 효과를 테스트하기 위해 포괄적인 평가(evaluations)를 만드세요.

**전체 평가 가이드라인을 위해 [✅ Evaluation 가이드](./reference/evaluation.md)를 로드하세요.**

#### 4.1 평가 목적 이해

평가를 통해 LLM이 실제적이고 복잡한 질문에 답하기 위해 당신의 MCP 서버를 효과적으로 사용할 수 있는지 테스트합니다.

#### 4.2 10개의 평가 질문 작성

효과적인 평가를 위해 가이드에 설명된 프로세스를 따르세요:

1. **도구 점검 (Tool Inspection)**: 사용 가능한 도구를 나열하고 기능을 이해합니다.
2. **콘텐츠 탐색 (Content Exploration)**: 읽기 전용(READ-ONLY) 작업을 사용하여 사용 가능한 데이터 탐색
3. **질문 생성**: 10개의 복잡하고 실제적인 질문 생성
4. **답변 검증**: 직접 질문을 해결하여 답변 확인

#### 4.3 평가 요구 사항

각 질문이 다음을 충족하는지 확인하세요:
- **독립성 (Independent)**: 다른 질문에 의존하지 않음
- **읽기 전용 (Read-only)**: 비파괴적인 작업만 필요함
- **복잡성 (Complex)**: 여러 도구 호출 및 심층적인 탐색 필요
- **실제성 (Realistic)**: 인간이 관심을 가질 만한 실제 유스케이스 기반
- **검증 가능성 (Verifiable)**: 문자열 비교로 검증 가능한 명확한 단일 답변
- **안정성 (Stable)**: 답변이 시간이 지나도 변하지 않음

#### 4.4 출력 형식

다음 구조의 XML 파일을 생성하세요:

```xml
<evaluation>
  <qa_pair>
    <question>동물 코드명을 가진 AI 모델 출시에 관한 토론을 찾으세요. 한 모델은 ASL-X 형식을 사용하는 특정 안전 지정이 필요했습니다. 점박이 야생 고양이의 이름을 딴 모델에 대해 결정된 숫자 X는 무엇입니까?</question>
    <answer>3</answer>
  </qa_pair>
<!-- 더 많은 qa_pair... -->
</evaluation>
```

---

# 참조 파일 (Reference Files)

## 📚 문서 라이브러리 (Documentation Library)

개발 중에 필요에 따라 다음 리소스를 로드하세요:

### 핵심 MCP 문서 (가장 먼저 로드)
- **MCP Protocol**: `https://modelcontextprotocol.io/sitemap.xml`의 사이트맵부터 시작하여 `.md` 접미사가 붙은 특정 페이지를 가져오세요.
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - 다음을 포함한 범용 MCP 가이드라인:
  - 서버 및 도구 명명 규칙
  - 응답 형식 가이드라인 (JSON vs Markdown)
  - 페이지네이션 모범 사례
  - 전송 방식 선택 (streamable HTTP vs stdio)
  - 보안 및 에러 핸들링 표준

### SDK 문서 (Phase 1/2 중에 로드)
- **Python SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`에서 가져오기
- **TypeScript SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`에서 가져오기

### 언어별 구현 가이드 (Phase 2 중에 로드)
- [🐍 Python 구현 가이드](./reference/python_mcp_server.md) - 다음을 포함한 전체 Python/FastMCP 가이드:
  - 서버 초기화 패턴
  - Pydantic 모델 예시
  - `@mcp.tool`을 이용한 도구 등록
  - 전체 작동 예시 코드
  - 품질 체크리스트

- [⚡ TypeScript 구현 가이드](./reference/node_mcp_server.md) - 다음을 포함한 전체 TypeScript 가이드:
  - 프로젝트 구조
  - Zod 스키마 패턴
  - `server.registerTool`을 이용한 도구 등록
  - 전체 작동 예시 코드
  - 품질 체크리스트

### 평가 가이드 (Phase 4 중에 로드)
- [✅ Evaluation 가이드](./reference/evaluation.md) - 다음을 포함한 전체 평가 생성 가이드:
  - 질문 작성 가이드라인
  - 답변 검증 전략
  - XML 형식 사양
  - 질문 및 답변 예시
  - 제공된 스크립트를 이용한 평가 실행 방법
