---
name: robot-framework-py
description: >-
  Robot Framework skill for Python-centric test automation across API, web,
  mobile, and data layers. USE FOR: creating or refactoring .robot suites,
  .resource files, RequestsLibrary API tests, SeleniumLibrary UI tests, Browser
  (Playwright) tests, AppiumLibrary mobile tests, DatabaseLibrary data checks,
  and custom Python keyword libraries; enforcing valid Robot Framework sections,
  reusable resource layering, deterministic assertions, and guardrails.
---

# Robot Framework (Python) — Top 5 Library Playbook

Use this skill to produce deterministic, maintainable Robot Framework code with enterprise-ready patterns.

## Apply this project structure by default

```text
tests/
resources/
libraries/
variables/
```

- Place suite files in `tests/`.
- Place reusable keywords in `resources/`.
- Place custom Python keyword libraries in `libraries/`.
- Place environment-specific variable files in `variables/`.

## Universal golden patterns

- Keep test cases short; place repeated behavior in resource keywords.
- Use `Suite Setup`/`Suite Teardown` for lifecycle management.
- Use deterministic assertions (`Should Be Equal*`, `Should Contain`, `Should Not Be Empty`).
- Prefer stable local fixtures/mocks over live external systems.
- Keep secrets in environment variables or secure variable files.
- Use consistent tags: `smoke`, `enterprise`, `ui`, `api`, `mobile`, `database`, `regression`.

## Library guidance

### 1) SeleniumLibrary

**Setup**
- Install: `pip install robotframework-seleniumlibrary`
- Import: `Library    SeleniumLibrary`
- Prefer headless browser in CI and static local pages for determinism.

**Recommended patterns**
- Wrap page actions in resource keywords.
- Use resilient locators (`id`, `data-testid`) over brittle XPath.
- Keep waits explicit (`Wait Until Element Is Visible`) and bounded.

**Common pitfalls**
- Hardcoded sleeps.
- Overly broad locators.
- Asserting on transient animation text.

**Do / Don't**
- Do: centralize URL and locator variables.
- Do: isolate test data per test.
- Don't: call low-level click/type steps repeatedly in test cases.
- Don't: depend on internet websites for smoke tests.

**Minimal working example**
```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open Local Smoke Page
    Open Browser    file://${CURDIR}/fixtures/smoke.html    chrome
    Wait Until Page Contains    Robot Smoke
    [Teardown]    Close Browser
```

### 2) RequestsLibrary

**Setup**
- Install: `pip install robotframework-requests`
- Import: `Library    RequestsLibrary`

**Recommended patterns**
- Create one session per API domain.
- Keep headers/auth in reusable keywords.
- Assert both status code and payload fields.

**Common pitfalls**
- Calling Python `requests.get()` directly.
- Repeating base URL and headers in every test.
- Non-deterministic live dependencies.

**Do / Don't**
- Do: use local/mock endpoints for deterministic tests.
- Do: validate response schema fields.
- Don't: rely on random public APIs.

**Minimal working example**
```robotframework
*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Health Endpoint Smoke
    Create Session    api    http://localhost:8080
    ${resp}=    GET On Session    api    /health
    Should Be Equal As Integers    ${resp.status_code}    200
```

### 3) Browser Library (Playwright)

**Setup**
- Install: `pip install robotframework-browser`
- Initialize browser binaries: `rfbrowser init`
- Import: `Library    Browser`

**Recommended patterns**
- Use `New Browser` in suite setup and close in teardown.
- Prefer role/text/test-id selectors.
- Use context/page keywords via resources.

**Common pitfalls**
- Forgetting `rfbrowser init` in fresh environments.
- Recreating browser per test when suite-level fixture is enough.
- Using unstable CSS selectors.

**Do / Don't**
- Do: run headless in CI.
- Do: use trace/screenshot on failure hooks where needed.
- Don't: mix Selenium and Browser keywords in one suite.

**Minimal working example**
```robotframework
*** Settings ***
Library    Browser

*** Test Cases ***
Browser Smoke
    New Browser    chromium    headless=true
    New Page    about:blank
    Get Title
    [Teardown]    Close Browser
```

### 4) AppiumLibrary

**Setup**
- Install: `pip install robotframework-appiumlibrary`
- Import: `Library    AppiumLibrary`
- Start local Appium server and emulator/simulator in CI job bootstrap.

**Recommended patterns**
- Store desired capabilities in variable files.
- Wrap launch/login/common navigation in resource keywords.
- Use accessibility IDs first.

**Common pitfalls**
- Device-dependent selectors.
- Hardcoded UDIDs in test files.
- Missing teardown causing stale sessions.

**Do / Don't**
- Do: keep platform-specific caps isolated.
- Do: tag tests by platform (`android`, `ios`).
- Don't: use pixel coordinates unless unavoidable.

**Minimal working example**
```robotframework
*** Settings ***
Library    AppiumLibrary

*** Test Cases ***
Open App Session Smoke
    Open Application    http://127.0.0.1:4723/wd/hub    platformName=Android
    ...    automationName=UiAutomator2    appPackage=com.example    appActivity=.MainActivity
    Page Should Contain Text    Welcome
    [Teardown]    Close Application
```

### 5) DatabaseLibrary

**Setup**
- Install: `pip install robotframework-databaselibrary`
- Import: `Library    DatabaseLibrary`
- Use ephemeral/local DB for deterministic execution.

**Recommended patterns**
- Connect once per suite, disconnect in teardown.
- Use seeded fixtures and deterministic queries.
- Validate data through business-level keywords.

**Common pitfalls**
- Reusing mutable DB state across tests.
- Non-parameterized SQL from test input.
- Asserting entire row payloads when only critical fields matter.

**Do / Don't**
- Do: reset DB state in setup.
- Do: check row counts and key columns.
- Don't: run destructive queries on shared environments.

**Minimal working example**
```robotframework
*** Settings ***
Library    DatabaseLibrary

*** Test Cases ***
Database Smoke
    Connect To Database    sqlite3    ${CURDIR}/fixtures/app.db
    ${rows}=    Query    SELECT status FROM health_check
    Should Be Equal    ${rows}[0][0]    UP
    [Teardown]    Disconnect From Database
```

## Microsoft-style testing strategy and RALF loop

- **Understand/Plan**: map prompts to expected patterns and forbidden patterns.
- **Build**: keep reusable resources and variable layering.
- **Validate**: add scenario-driven checks and quality gates in CI.
- **Iterate** with **RALF**:
  1. **Review** failures and inconsistency reports.
  2. **Analyze** root causes (guidance gap, example drift, weak assertions).
  3. **Learn** by codifying conventions and anti-patterns.
  4. **Fix** docs/examples/tests and re-run quality checks.

## Execute with this checklist

1. Identify output type (`.robot`, `.resource`, variable file, or Python library).
2. Choose target library and fixture strategy.
3. Generate deterministic assertions and reusable keywords.
4. Refactor duplication into resources.
5. Add/refresh scenario checks and acceptance rules.
6. Ensure CI checks are green.

## References

- Robot Framework User Guide: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
- SeleniumLibrary docs: https://robotframework.org/SeleniumLibrary/
- RequestsLibrary docs: https://docs.robotframework.org/docs/different_libraries/requests
- Browser library docs: https://marketsquare.github.io/robotframework-browser/
- AppiumLibrary docs: https://docs.robotframework.org/docs/different_libraries/appium
- DatabaseLibrary docs: https://docs.robotframework.org/docs/different_libraries/database
