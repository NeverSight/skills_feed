---
name: webapp-testing
description: Playwright를 사용하여 로컬 웹 애플리케이션과 상호작용하고 테스트하기 위한 툴킷입니다. 프런트엔드 기능 검증, UI 동작 디버깅, 브라우저 스크린샷 캡처 및 브라우저 로그 확인을 지원합니다.
license: LICENSE.txt의 전체 약관 참조
---

# Web Application Testing

로컬 웹 애플리케이션을 테스트하려면 파이썬(Python) Playwright 스크립트를 작성하세요.

**사용 가능한 헬퍼 스크립트**:
- `scripts/with_server.py` - 서버 라이프사이클 관리 (다중 서버 지원)

**항상 스크립트를 `--help`와 함께 먼저 실행**하여 사용법을 확인하세요. 스크립트를 직접 실행해보고 커스텀 솔루션이 절대적으로 필요하다고 판단되기 전까지는 소스 코드를 읽지 마세요. 이러한 스크립트들은 매우 방대하여 컨텍스트 윈도우를 오염시킬 수 있습니다. 이들은 컨텍스트에 담기보다는 블랙박스(black-box) 스크립트로 직접 호출하도록 만들어졌습니다.

## 결정 트리: 접근 방식 선택 (Decision Tree)

```
사용자 작업 → 정적 HTML인가?
    ├─ 예 → HTML 파일을 직접 읽어 셀렉터(selectors) 식별
    │         ├─ 성공 → 식별된 셀렉터로 Playwright 스크립트 작성
    │         └─ 실패/불충분 → 동적 앱으로 간주 (아래 참조)
    │
    └─ 아니오 (동적 웹앱) → 서버가 이미 실행 중인가?
        ├─ 아니오 → 실행: python scripts/with_server.py --help
        │            그다음 헬퍼를 사용하여 간소화된 Playwright 스크립트 작성
        │
        └─ 예 → 정찰 후 행동(Reconnaissance-then-action):
            1. 이동(Navigate) 후 networkidle 상태까지 대기
            2. 스크린샷 캡처 또는 DOM 검사
            3. 렌더링된 상태에서 셀렉터 식별
            4. 찾은 셀렉터로 작업 수행
```

## 예시: with_server.py 사용

서버를 시작하려면 먼저 `--help`를 실행한 다음 헬퍼를 사용하세요:

**단일 서버:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**다중 서버 (예: 백엔드 + 프런트엔드):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

자동화 스크립트를 작성할 때는 Playwright 로직만 포함하세요 (서버는 자동으로 관리됩니다):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # 항상 chromium을 headless 모드로 실행하세요
    page = browser.new_page()
    page.goto('http://localhost:5173') # 서버는 이미 실행되어 준비된 상태입니다
    page.wait_for_load_state('networkidle') # 매우 중요: JS가 실행될 때까지 대기하세요
    # ... 자동화 로직 작성
    browser.close()
```

## 정찰 후 행동 패턴 (Reconnaissance-Then-Action Pattern)

1. **렌더링된 DOM 검사**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **검사 결과에서 셀렉터 식별**

3. **찾은 셀렉터를 사용하여 작업 실행**

## 주의해야 할 함정

❌ **나쁨**: 동적 앱에서 `networkidle` 상태를 기다리지 않고 DOM을 검사하는 것
✅ **좋음**: 검사 전에 `page.wait_for_load_state('networkidle')`를 호출하여 대기하는 것

## 모범 사례 (Best Practices)

- **번들링된 스크립트를 블랙박스로 활용하세요** - 작업을 수행할 때 `scripts/`에 있는 스크립트가 도움이 될 수 있는지 고려하세요. 이 스크립트들은 컨텍스트 윈도우를 어지럽히지 않으면서 복잡한 일반 워크플로우를 안정적으로 처리합니다. `--help`로 사용법을 확인한 후 직접 호출하세요.
- 동기식 스크립트에는 `sync_playwright()`를 사용하세요.
- 작업이 끝나면 항상 브라우저를 닫으세요.
- 설명적인 셀렉터를 사용하세요: `text=`, `role=`, CSS 셀렉터 또는 ID.
- 적절한 대기 시간을 추가하세요: `page.wait_for_selector()` 또는 `page.wait_for_timeout()`.

## 참조 파일 (Reference Files)

- **examples/** - 일반적인 패턴을 보여주는 예시:
  - `element_discovery.py` - 페이지 내 버튼, 링크 및 입력 필드 찾기
  - `static_html_automation.py` - 로컬 HTML에 file:// URL 사용하기
  - `console_logging.py` - 자동화 중 콘솔 로그 캡처하기