---
name: proxyuser
description: Creates, runs, and monitors E2E tests via ProxyUser API. Use when implementing features that need E2E test coverage, when tests fail and need diagnosis, when running tests against preview deployments, or when setting up automated QA for a web application.
---

# ProxyUser E2E Testing

ProxyUser is an AI-assisted E2E QA platform. Describe tests in plain English, and AI executes them as a human would.

## Quick Start

### Authentication

Store your API key in the environment:

```bash
export PROXYUSER_API_KEY="sk_live_your_key_here"
```

Create API keys at https://proxyuser.com/settings/api_keys

**Fallback:** If `$PROXYUSER_API_KEY` is not set in the environment, check the project's root `.env` file for `PROXYUSER_API_KEY=sk_live_xxx`.

### Verify Setup

```bash
curl -s https://proxyuser.com/api/v1/projects \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '.data.projects[].name'
```

### Key Concepts

| Concept | Description | ID Format |
|---------|-------------|-----------|
| **Project** | Groups scenarios for an application | `proj_xxx` |
| **Scenario** | Plain English test description + URL | `scen_xxx` |
| **Run** | Single test execution with status and video | `run_xxx` |
| **Folder** | Groups scenarios with shared instructions | `fold_xxx` |

---

## When Invoked Without Instructions

If the user invokes `/proxyuser` without specifying what they want to do:

**Ask the user to choose:**

1. **Generate starter tests** - Analyze the codebase and create foundational E2E tests
2. **Create test for a feature** - Write a test for something specific
3. **Run tests** - Execute existing tests against a URL
4. **Check recent failures** - Diagnose and investigate failed tests

### Starter Tests Workflow

When the user chooses "Generate starter tests":

**Step 1: Understand the application**

Analyze the codebase to identify:
- App type (e-commerce, SaaS, content site, etc.)
- Main user-facing routes and pages
- Authentication patterns (email/password, OAuth, magic link)
- Core features that deliver user value

Look at: route files, navigation components, page directories, and any existing test coverage.

**Step 2: Check existing coverage**

List all existing scenarios in the project to avoid duplicates:

```bash
curl -s "https://proxyuser.com/api/v1/projects/$PROJECT_ID/scenarios" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '.data.scenarios[].prompt'
```

**Step 3: Suggest foundational tests**

Recommend scenarios following the prioritization order:

1. **Revenue-critical paths** - Checkout, payment, upgrade flows
2. **User acquisition** - Signup, onboarding
3. **Core product value** - The main thing users come to do
4. **Authentication** - Login, logout, password reset

Limit initial suggestions to 5-10 high-impact scenarios. Quality over quantity.

**Step 4: Create scenarios with proper organization**

Group related tests into folders. Create folders first, then add scenarios to them.

Example structure for an e-commerce app:
```
📁 Authentication
   - User can sign up with email
   - User can log in with credentials
📁 Shopping
   - User can add item to cart
   - User can view cart
📁 Checkout
   - User can complete purchase
```

---

## Workflows

### Create Test for New Feature

When implementing a feature that needs E2E coverage:

```
- [ ] **List existing scenarios and review coverage before suggesting new tests**
- [ ] Identify the user journey the feature enables
- [ ] Write scenario with specific, observable assertions
- [ ] Commit scenario alongside feature code
```

**Step 1: Check existing scenarios**

```bash
curl -s "https://proxyuser.com/api/v1/projects/$PROJECT_ID/scenarios" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '.data.scenarios[].prompt'
```

**Step 2: Create the scenario**

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/scenarios" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "User clicks Add to Cart button, cart icon shows count of 1, checkout button becomes visible",
    "url": "https://example.com/products/widget-1"
  }'
```

---

### Run Scenario and Wait for Results

Test runs are async. Trigger, then poll for completion:

```bash
# Trigger run
RUN_ID=$(curl -s -X POST "https://proxyuser.com/api/v1/scenarios/$SCENARIO_ID/run" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq -r '.data.run.id')

echo "Started run: $RUN_ID"

# Poll until complete (timeout after 5 minutes)
for i in {1..30}; do
  RESULT=$(curl -s "https://proxyuser.com/api/v1/runs/$RUN_ID" \
    -H "Authorization: Bearer $PROXYUSER_API_KEY")

  STATUS=$(echo $RESULT | jq -r '.data.run.status')

  case $STATUS in
    passed)
      echo "Test passed!"
      exit 0
      ;;
    failed)
      echo "Test failed:"
      echo $RESULT | jq -r '.data.run.ai_diagnosis'
      exit 1
      ;;
    *)
      echo "Status: $STATUS..."
      sleep 10
      ;;
  esac
done

echo "Timeout waiting for test"
exit 1
```

---

### Run All Tests on Preview Deploy

Run your entire test suite against a preview/staging URL:

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/run_all" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://preview-abc123.vercel.app"}'
```

Filter to specific folders:

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/run_all" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://staging.example.com",
    "folder_ids": ["fold_abc123", "fold_def456"]
  }'
```

---

### Diagnose a Failed Test

Get the AI diagnosis and video for a failed run:

```bash
curl -s "https://proxyuser.com/api/v1/runs/$RUN_ID" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '{
    status: .data.run.status,
    diagnosis: .data.run.ai_diagnosis,
    video: .data.run.video_url,
    scenario: .data.run.scenario.prompt
  }'
```

**Common diagnosis patterns:**

| Diagnosis | Likely Cause | Action |
|-----------|--------------|--------|
| "Element not found" | Selector changed, element removed | Check if UI changed |
| "Timeout waiting for" | Slow load, async issue | Check performance |
| "Unexpected text" | Copy changed, display bug | Verify expected text |
| "Navigation failed" | Route broken, redirect issue | Check routing |

---

### List Recent Failures

```bash
curl -s "https://proxyuser.com/api/v1/runs?status=failed&limit=10" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '.data.runs[] | {
    id: .id,
    scenario_id: .scenario_id,
    completed: .completed_at
  }'
```

---

## Writing Effective Scenarios

### Keep It Simple

ProxyUser's AI browses like a human. Trust it to figure out the details—don't write step-by-step instructions.

**Good:**
```
User can sign up with a valid email address
```

**Bad:**
```
User enters "test@example.com" in email field, clicks Submit button,
sees "Check your inbox" confirmation message on screen
```

### Code-to-Test Translation

When you implement a feature, ask: "What capability does this give the user?"

| Code Change | Test Prompt |
|-------------|-------------|
| Add delete button | "User can delete an item from the list" |
| Implement search | "User can search for items by name" |
| Add form validation | "User sees error when submitting with empty email" |
| Add pagination | "User can load more items at bottom of list" |
| Implement login | "User can log in with {{EMAIL}} and {{PASSWORD}}" |

### Environment Variables

Use `{{VAR}}` for credentials (configured in ProxyUser dashboard):

```
User can log in with {{EMAIL}} and {{PASSWORD}}
```

### Common Patterns

See [examples/prompt-patterns.md](examples/prompt-patterns.md) for a library of reusable test scenario templates.

### Prioritizing Test Scenarios

Focus on high-impact tests first. If this breaks, does the business suffer?

**Test these first (in order):**

1. **Revenue-critical paths** - Checkout, payment, subscription upgrades
2. **User acquisition** - Signup, onboarding completion
3. **Core product value** - The main thing users come to do
4. **Authentication** - Login, logout, password reset
5. **Key error states** - Validation errors, failure messages users need to see

**Skip these (low impact):**
- Cosmetic hover states
- Admin-only features (test manually)
- Edge cases that affect <1% of users

### Scenario Guardrails

**Before suggesting any new scenarios:**

1. **List existing scenarios first** - Run the list scenarios API call and review what's already covered
2. **Check for overlapping coverage** - Don't suggest tests that duplicate existing functionality
3. **Limit recommendations** - Recommend a maximum of 20 scenarios per session. Quality > quantity.

**When reviewing existing scenarios, look for:**
- Similar user journeys (e.g., "User can add item" vs "User adds product to cart")
- Overlapping test coverage (e.g., login tested in multiple scenarios)
- Tests that could be consolidated

**Red flags that you're over-testing:**
- More than 5 scenarios for a single feature
- Scenarios testing minor variations of the same flow
- Tests for edge cases affecting <1% of users

### Test Boundaries

**Only test what can be completed entirely within the browser.**

ProxyUser controls a browser. It cannot check email inboxes, receive SMS codes, or interact with external services.

❌ **Do NOT create scenarios that require:**

- Checking email (verification links, password reset emails)
- SMS or phone verification
- Third-party OAuth (Google, Apple, Facebook login buttons)
- External service responses (Slack notifications, webhook deliveries)
- Real payment processing (use test/sandbox modes instead)
- Mobile app interactions
- Desktop notifications or OS-level prompts

✅ **Instead, test the browser-side behavior:**

| Don't test this | Test this instead |
|-----------------|-------------------|
| "User receives verification email" | "User sees 'Check your email' confirmation" |
| "User logs in with Google" | "User sees Google login button and it's clickable" |
| "Payment completes successfully" | "User can submit payment form" (in test mode) |
| "User gets Slack notification" | "User sees 'Notification sent' message in UI" |

---

## Organizing Scenarios

### Use Folders to Group Related Tests

Avoid creating a flat list of scenarios. Group tests by feature area, user flow, or page section.

**Good organization:**
```
📁 Authentication
   - User can sign up with email
   - User can log in with credentials
   - User can reset password
📁 Shopping Cart
   - User can add item to cart
   - User can remove item from cart
   - User can update quantity
📁 Checkout
   - User can complete purchase
   - User can apply discount code
```

**Bad organization:**
```
- User can sign up
- User can add to cart
- User can log in
- User can checkout
- User can reset password
- User can remove from cart
... (12 more unorganized scenarios)
```

### Before Creating Scenarios

**Step 1: List existing folders**

```bash
curl -s "https://proxyuser.com/api/v1/projects/$PROJECT_ID/folders" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" | jq '.data.folders[] | {id, name, scenarios_count}'
```

To see scenarios within each folder, add `?include_scenarios=true`.

**Step 2: Choose the right folder**

- If a folder exists that matches the feature area → use it
- If no folder fits → create one (see below)
- If adding multiple related scenarios → create a folder for them

### Creating a Folder

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/folders" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shopping Cart",
    "instructions": "All tests start from the product catalog page",
    "schedule": "0 9 * * *"
  }'
```

Parameters:
- `name` (required) - Folder name
- `instructions` (optional) - Shared context for all scenarios in the folder
- `schedule` (optional) - Cron expression for recurring test runs

**For folders requiring authentication:**

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/folders" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Dashboard",
    "instructions": "First, log in with {{EMAIL}} and {{PASSWORD}}"
  }'
```

**Note:** Set the scenario URLs to the login page (e.g., `https://example.com/login`) when using auth instructions.

### Folder Instructions and Inheritance

When you set `instructions` on a folder, **all scenarios in that folder inherit those instructions**. This is ideal for shared setup steps like authentication.

#### When to Use Folder-Level Authentication

Use folder-level instructions when:
- Multiple scenarios in the folder require the same login
- All tests start from an authenticated state
- You want DRY (Don't Repeat Yourself) test organization

Use scenario-level authentication when:
- Only one or two scenarios need authentication
- Different scenarios need different credentials
- The auth flow IS what you're testing

#### Example: Folder with Authentication

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/folders" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dashboard Features",
    "instructions": "First, log in with {{EMAIL}} and {{PASSWORD}}"
  }'
```

Now scenarios in this folder are simple:
```
User can view analytics chart
User can export data to CSV
User can update notification settings
```

The AI will log in first (from folder instructions), then execute the scenario.

#### Before/After: DRY Principle

**Before (repetitive):**
```
📁 Dashboard (no instructions)
   - User logs in with {{EMAIL}} and {{PASSWORD}}, then views analytics
   - User logs in with {{EMAIL}} and {{PASSWORD}}, then exports data
   - User logs in with {{EMAIL}} and {{PASSWORD}}, then updates settings
```

**After (using folder instructions):**
```
📁 Dashboard
   instructions: "First, log in with {{EMAIL}} and {{PASSWORD}}"
   - User can view analytics chart
   - User can export data to CSV
   - User can update notification settings
```

#### Starting URL for Authentication

When tests require authentication, set the scenario's starting URL to the login page:

| Scenario Type | Starting URL |
|--------------|--------------|
| Public page test | `https://example.com/` |
| Authenticated test | `https://example.com/login` |
| Deep-link after auth | `https://example.com/login` (AI navigates after login) |

**Note:** Even if your folder instructions say to log in, the browser needs to start on a page where login is possible.

### Running All Scenarios in a Folder

```bash
curl -X POST "https://proxyuser.com/api/v1/folders/$FOLDER_ID/run" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY"
```

All triggered tests share a `batch_id` for unified tracking.

### Assigning Scenarios to Folders

Include `folder_id` when creating scenarios:

```bash
curl -X POST "https://proxyuser.com/api/v1/projects/$PROJECT_ID/scenarios" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "User can add item to cart",
    "url": "https://example.com/products",
    "folder_id": "fold_abc123"
  }'
```

### Moving Scenarios Between Folders

To move an existing scenario to a different folder:

```bash
curl -X PATCH "https://proxyuser.com/api/v1/scenarios/$SCENARIO_ID" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"folder_id": "fold_newFolder123"}'
```

To remove a scenario from its folder (move to root/unfiled):

```bash
curl -X PATCH "https://proxyuser.com/api/v1/scenarios/$SCENARIO_ID" \
  -H "Authorization: Bearer $PROXYUSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"folder_id": null}'
```

---

## API Reference

### Base URL

```
https://proxyuser.com/api/v1
```

### Authentication

```
Authorization: Bearer sk_live_xxx
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects` | List all projects |
| POST | `/projects` | Create project |
| GET | `/projects/:id` | Get project with scenarios |
| PATCH | `/projects/:id` | Update project |
| DELETE | `/projects/:id` | Delete project |
| POST | `/projects/:id/run_all` | Run all active scenarios |
| GET | `/projects/:id/scenarios` | List scenarios |
| POST | `/projects/:id/scenarios` | Create scenario |
| GET | `/projects/:id/folders` | List folders |
| POST | `/projects/:id/folders` | Create folder |
| GET | `/folders/:id` | Get folder details |
| PATCH | `/folders/:id` | Update folder |
| DELETE | `/folders/:id` | Delete folder |
| POST | `/folders/:id/run` | Run all scenarios in folder |
| GET | `/scenarios/:id` | Get scenario with recent runs |
| PATCH | `/scenarios/:id` | Update scenario (including folder assignment) |
| DELETE | `/scenarios/:id` | Delete scenario |
| POST | `/scenarios/:id/run` | Trigger test run |
| GET | `/runs` | List runs (filter: status, project_id, scenario_id) |
| GET | `/runs/:id` | Get run with AI diagnosis |

### Scenario Object

```json
{
  "id": "scen_xxx",
  "project_id": "proj_xxx",
  "folder_id": "fold_xxx",  // null if not in a folder
  "prompt": "User can sign up with email",
  "url": "https://example.com",
  "is_active": true,
  "schedule": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Response Format

```json
{
  "data": { ... },
  "meta": {
    "request_id": "abc-123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Run Status Values

- `pending` - Queued for execution
- `running` - Currently executing
- `passed` - Test completed successfully
- `failed` - Test failed (check ai_diagnosis)

### Error Response

```json
{
  "error": {
    "code": "scenario_not_found",
    "message": "Scenario with ID 'scen_xxx' not found",
    "hint": "Use GET /api/v1/projects/:id to see available scenarios"
  }
}
```

---

## CI/CD Integration

### GitHub Actions (Vercel Preview Deploys)

```yaml
name: E2E Tests
on:
  deployment_status:

jobs:
  test:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: proxyuserai/action@v1
        with:
          api-key: ${{ secrets.PROXYUSER_API_KEY }}
          project-id: 'proj_xxx'
          target-url: ${{ github.event.deployment_status.target_url }}
          fail-on-test-failure: 'true'
```

### Other CI Systems

Use the API directly with the polling script from "Run Scenario and Wait for Results" above.

Full CI/CD documentation: https://proxyuser.com/docs#github-integration

---

## Troubleshooting

### Test passes locally but fails in CI

- Check if `target_url` override is correct
- Verify environment variables are set in ProxyUser dashboard
- Check if preview deploy is fully ready before tests run

### Video not available

Videos take ~30 seconds to process after test completion. Poll the run endpoint until `video_available: true`.

### Rate limits

The API allows 100 requests per minute per API key. For bulk operations, use `run_all` instead of individual scenario runs.

---

## Resources

- **Full API Docs**: https://proxyuser.com/docs
- **Dashboard**: https://proxyuser.com
- **GitHub Action**: https://github.com/proxyuserai/action
