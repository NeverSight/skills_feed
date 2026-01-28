---
name: testing
description: |
  Write and manage tests using TDD with Pest (PHP), Vitest (React), pytest (Python), and Playwright (E2E). Use when writing
  feature tests, unit tests, component tests, visual regression tests, or improving test coverage. EXCLUSIVE to testing-expert agent.
allowed-tools: Read, Edit, Bash, Grep, Glob, Write, mcp_gemini-bridge, mcp_open-bridge, mcp_codex-bridge, mcp_context7, mcp_playwright, mcp_zai-mcp-server
---
# Testing

**Exclusive to:** `testing-expert` agent

## MCP Helpers (Brain + Memory)

### 🧠 Gemini-Bridge (Brain) — Test Strategy Advice
```
mcp_gemini-bridge_consult_gemini(query="Suggest comprehensive test cases for: [feature]. Include edge cases.", directory=".")
```

### 🌉 Open-Bridge — Alternative Test Strategy
```
mcp_open-bridge_consult_gemini(query="Suggest comprehensive test cases for: [feature]. Include edge cases.", directory=".")
```

### 📚 Context7 (Memory) — Up-to-Date Docs

Lookup testing patterns and assertions:
```
mcp_context7_resolve-library-id(libraryName="pytest", query="fixtures async")
mcp_context7_query-docs(libraryId="/pytest-dev/pytest", query="parametrize examples")
```

## 🖼️ Visual Testing (Web Apps)

For UI/UX testing, use Playwright MCP to capture and Vision AI to analyze:

### Capture Screenshots
```
mcp_playwright_browser_navigate(url="http://localhost:8000/[page]")
mcp_playwright_browser_take_screenshot(filename="test-screenshot.png")
```

### Analyze with Vision AI
```
mcp_zai-mcp-server_analyze_image(
  image_path="test-screenshot.png",
  prompt="Analyze this UI: check layout, colors, spacing, alignment, accessibility issues"
)
```

### Visual Regression Flow
1. Capture baseline screenshot
2. Make changes
3. Capture new screenshot
4. Use Vision AI to compare and validate

## Validation Loop (MANDATORY)

After writing or modifying tests, always verify:
```bash
composer test           # PHP tests pass
npm run test           # JS tests pass (if applicable)
```

**TDD Feedback Loop:**
1. Write test → Verify it FAILS (Red)
2. Implement minimal code → Verify it PASSES (Green)
3. Refactor → Verify it still PASSES
4. Repeat for edge cases

## Instructions (TDD Workflow)

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Write failing test | `composer test --filter=NewTest` → FAILS |
| 2 | Implement minimal code | `composer test --filter=NewTest` → PASSES |
| 3 | Refactor | `composer test` → ALL PASS |
| 4 | Add edge cases | Repeat steps 1-3 |

## Pest Patterns (Laravel)

### Feature Test
```php
test('user can create post', function () {
    $user = User::factory()->create();
    
    $this->actingAs($user)
        ->post('/posts', ['title' => 'Test'])
        ->assertRedirect('/posts');
        
    $this->assertDatabaseHas('posts', ['title' => 'Test']);
});
```

### Unit Test
```php
test('generates slug from title', function () {
    expect((new SlugGenerator)->generate('Hello World'))
        ->toBe('hello-world');
});
```

## Vitest Patterns (React)

```tsx
describe('PostForm', () => {
    it('submits with valid data', async () => {
        const onSubmit = vi.fn();
        render(<PostForm onSubmit={onSubmit} />);
        
        await userEvent.type(screen.getByLabelText(/title/i), 'Test');
        await userEvent.click(screen.getByRole('button', { name: /submit/i }));
        
        expect(onSubmit).toHaveBeenCalled();
    });
});
```

## Test Commands

```bash
# Laravel
composer test
php artisan test --filter=PostTest
php artisan test --coverage

# React
npm run test
npm run test:watch
npm run test:coverage
```

## Examples
- "Write tests for PostController"
- "Add unit tests for this service"
- "Fix failing test"
