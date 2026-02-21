---
name: android-saas-planning
description: "Create comprehensive planning documentation for a native Android app that integrates with an existing web-based SaaS platform. Use when building a mobile companion app for any SaaS — ERP, CRM, POS, logistics, healthcare, fintech, etc. Generates 7 production-ready planning documents: PRD, SRS, SDS, API Contract, User Journeys, Testing Strategy, and Release Plan."
---

# Android SaaS Planning Skill

Generate a complete, implementation-ready documentation suite for a native Android app that serves as a mobile client for an existing web-based SaaS system.

## When to Use

- Building a new native Android app for an existing web SaaS
- Porting a web application's functionality to Android
- Planning a mobile-first or mobile-companion SaaS experience
- Scoping MVP features for a mobile client
- Creating a structured handoff document for Android developers

## When NOT to Use

- Building a standalone mobile app with no web backend
- Cross-platform (Flutter/React Native) — this skill targets native Android (Kotlin + Jetpack Compose)
- Adding a WebView wrapper — this skill targets fully native screens
- Incremental feature additions to an existing Android app

## Prerequisites — Context the Agent MUST Gather

Before generating ANY documents, the agent must have or discover:

### 1. SaaS Profile (Required)

| Field         | What to Find                                      |
| ------------- | ------------------------------------------------- |
| Product name  | Brand name and domain                             |
| Domain        | ERP, CRM, POS, Healthcare, Fintech, etc.          |
| Target market | Region, language, currency, payment methods       |
| Backend stack | PHP/MySQL, Node/PostgreSQL, Django, Laravel, etc. |
| API base URL  | Per environment (see standard 3-env setup below)  |
| Auth model    | JWT, OAuth2, session-based, API keys              |
| Multi-tenancy | Tenant ID in JWT, subdomain, DB-per-tenant        |

### 2. Module Inventory (Required)

Audit the web app to identify all modules. For each module determine:

- **Name and description** (what the module does)
- **Mobile relevance** — does it make sense on a phone? (e.g., complex admin panels may not)
- **MVP classification** — P0 (ship without), P1 (within 2 sprints), P2 (future)
- **Offline requirement** — must it work offline?
- **API endpoints** — existing endpoints that serve this module

### 3. Feature Scope (Required — Accept from User)

The user may request a **subset** of modules. Respect their selection:

- If the user specifies "only POS and Inventory" — plan only those modules
- If the user says "full app" — plan all mobile-relevant modules
- Always include Auth and Dashboard as baseline modules unless explicitly excluded

### 4. Technical Constraints (Discover or Ask)

- Minimum Android API level (default: API 29 / Android 10)
- Apps must be tested against the latest stable Android release
- Max APK size (default: 50MB)
- Offline requirements (none / basic caching / full offline-first)
- Hardware peripherals (Bluetooth printer, barcode scanner, NFC)
- Biometric authentication (fingerprint, face)
- Push notifications (FCM)
- Local dev networking: emulator must connect to WAMP via the host machine's static LAN IP (not `localhost`)

### 5. Standard Backend Environment Setup

All SaaS companion apps target these three backend environments:

| Environment | OS | Database | API Base URL Pattern |
|---|---|---|---|
| **Development** | Windows 11 (WAMP) | MySQL 8.4.7 | `http://{LAN_IP}:{port}/{project}/api/` |
| **Staging** | Ubuntu VPS | MySQL 8.x | `https://staging.{domain}/api/` |
| **Production** | Debian VPS | MySQL 8.x | `https://{domain}/api/` |

Use Gradle build flavors to manage per-environment base URLs. All backends use `utf8mb4_unicode_ci` collation and MySQL 8.x. Always plan API contracts that work identically across all environments.

## Phase 1 Bootstrap Pattern (MANDATORY)

**Every Android SaaS app MUST start with Phase 1: Login + Dashboard + Empty Tabs.**

This is the proven foundation pattern. Before planning any business features, the first implementation phase always delivers:

### Phase 1 Scope (Non-Negotiable)

1. **JWT Authentication** — Login/logout with the SaaS backend (access tokens + refresh token rotation + breach detection)
2. **Dashboard** — Real KPI stats from the backend, offline-first with Room caching, pull-to-refresh
3. **Bottom Navigation** — Maximum 5 major section tabs (e.g., Home, Sales, Network, Knowledge, Training). Non-dashboard tabs show "Coming Soon" placeholder screens
4. **Core Infrastructure** — Hilt DI modules, Retrofit + OkHttp interceptor chain (auth + tenant + logging), encrypted token storage, network monitor, Room database, Material 3 theme
5. **Backend Endpoints** — Mobile login, token refresh, logout, and dashboard stats API endpoints with dual auth middleware (JWT for mobile + session for web backward compatibility)
6. **Unit Tests** — Full test coverage for ViewModels, Use Cases, Repositories, Interceptors

### Phase 1 Deliverables

| Component      | Android                                                                                 | Backend                                                                                      |
| -------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Auth           | LoginScreen, LoginViewModel, AuthRepository, AuthApiService, TokenManager, interceptors | mobile-login.php, mobile-refresh.php, mobile-logout.php, MobileAuthHelper, ApiAuthMiddleware |
| Dashboard      | DashboardScreen, DashboardViewModel, DashboardRepository, Room cache                    | dashboard-stats.php (dual auth)                                                              |
| Navigation     | 5-tab BottomBar, NavGraph, PlaceholderScreen for future tabs                            | —                                                                                            |
| Infrastructure | DI modules, theme, encrypted prefs, network monitor                                     | refresh_tokens table, .env loading                                                           |
| Tests          | 40+ unit tests across all layers                                                        | curl/Postman endpoint verification                                                           |

### Why Phase 1 First

- Proves the entire vertical slice works (UI → ViewModel → UseCase → Repository → API → Backend → Database)
- Establishes all infrastructure patterns that every future feature reuses
- Gives the user a working app they can install and log into immediately
- Uncovers backend integration issues early (auth, CORS, env loading, session handling)
- Creates the navigation skeleton that future phases fill in

### Tab Selection (Max 5)

When auditing modules, group them into a **maximum of 5 bottom navigation tabs**. Common patterns:

| App Type            | Tab 1 | Tab 2        | Tab 3     | Tab 4     | Tab 5    |
| ------------------- | ----- | ------------ | --------- | --------- | -------- |
| **MLM/Distributor** | Home  | Sales        | Network   | Knowledge | Training |
| **ERP/Business**    | Home  | Sales        | Inventory | Reports   | Settings |
| **CRM**             | Home  | Contacts     | Deals     | Tasks     | Settings |
| **POS/Retail**      | Home  | Sales        | Products  | Customers | Reports  |
| **Healthcare**      | Home  | Patients     | Schedule  | Records   | Settings |
| **Fintech**         | Home  | Transactions | Cards     | Savings   | Settings |

If more than 5 sections exist, nest sub-sections within tabs or use drawer navigation for secondary items.

### Phase 1 Implementation Plan Structure

The Phase 1 plan MUST be structured as 11 sections (following the proven pattern):

```
docs/plans/phase-1-login-dashboard/
├── 00-build-variants.md          # Dev/Staging/Prod flavors
├── 01-project-bootstrap.md       # Gradle, manifest, strings, packages
├── 02-backend-api.md             # PHP JWT endpoints + DB migration
├── 03-core-infrastructure.md     # DI, security, network, interceptors
├── 04-authentication-feature.md  # Login vertical slice (DTO→Entity→Domain)
├── 05-dashboard-feature.md       # Dashboard with offline-first Room caching
├── 06-navigation-tabs.md         # Bottom nav + placeholder screens
├── 07-room-database.md           # Database class, converters, module
├── 08-theme-ui-components.md     # Material 3 theme + reusable components
├── 09-testing.md                 # 40+ unit tests across all layers
└── 10-verification.md            # Backend curl tests + Android manual checklist
```

### Phase 2+ Planning

Only after Phase 1 is **fully implemented, tested, and verified E2E** should Phase 2 features be planned. Phase 2 fills in the placeholder tabs with real functionality, reusing all the infrastructure from Phase 1.

---

## Document Generation Workflow

Generate documents **one at a time**, in order. Each document builds on the previous.

### Step 1: Audit the Existing Web App

Before writing any documents:

1. **Read the codebase** — scan API routes, controllers, models, database schema
2. **Identify modules** — group endpoints by business domain
3. **Map data models** — understand entities, relationships, field types
4. **Note auth flow** — how login, tokens, permissions, and multi-tenancy work
5. **Find existing docs** — API docs, database docs, architecture docs
6. **Present findings** to the user for confirmation before proceeding

### Step 2: Generate Documents in Order

| Order | Document              | Index File               | Sub-files Directory        |
| ----- | --------------------- | ------------------------ | -------------------------- |
| 1     | README                | `README.md`              | —                          |
| 2     | Product Requirements  | `01_PRD.md`              | `prd/`                     |
| 3     | Software Requirements | `02_SRS.md`              | `srs/`                     |
| 4     | Software Design       | `03_SDS.md`              | `sds/`                     |
| 5     | API Contract          | `04_API_CONTRACT.md`     | `api-contract/`            |
| 6     | User Journeys         | `05_USER_JOURNEYS.md`    | — (or split if >500 lines) |
| 7     | Testing Strategy      | `06_TESTING_STRATEGY.md` | `testing/`                 |
| 8     | Release Plan          | `07_RELEASE_PLAN.md`     | —                          |

### Step 3: Review and Refine

After all documents are generated, verify:

- [ ] All module requirements trace to API endpoints
- [ ] Room entities match backend data models
- [ ] Auth flow matches the web app's actual auth implementation
- [ ] Offline sync strategy covers all P0 modules
- [ ] No fabricated endpoints — every endpoint references real backend routes

## Formatting Rules (Strict)

1. **500-line max** per markdown file — split into sub-files if exceeded
2. **Numbered requirement IDs** — `FR-AUTH-001`, `NFR-PERF-003`, etc.
3. **Real Kotlin code** — not pseudocode; include actual imports and versions
4. **JSON examples** — complete request/response bodies for every endpoint
5. **ASCII diagrams** — flow charts, architecture layers, sync flows
6. **Markdown tables** — for requirements, endpoints, metrics, comparisons
7. **Cross-references** — link between documents liberally
8. **Back-links** — every sub-file links back to its parent index
9. **Navigation** — every index links to all its sub-files with descriptions

## Tech Stack Defaults

Use these unless the project context requires alternatives:

| Layer         | Technology                                  | Version                             |
| ------------- | ------------------------------------------- | ----------------------------------- |
| Language      | Kotlin                                      | 2.0+                                |
| UI            | Jetpack Compose + Material 3                | BOM 2024.06+                        |
| Icons         | Custom PNGs (no icon libraries)             | Use placeholders + PROJECT_ICONS.md |
| Reports       | Table-first for >25 rows                    | Use android-report-tables           |
| Architecture  | MVVM + Clean Architecture                   | —                                   |
| DI            | Dagger Hilt                                 | 2.51+                               |
| Networking    | Retrofit + OkHttp + Moshi                   | 2.11+ / 4.12+                       |
| Local DB      | Room                                        | 2.6+                                |
| Async         | Coroutines + Flow                           | 1.8+                                |
| Background    | WorkManager                                 | 2.9+                                |
| Navigation    | Navigation Compose                          | 2.7+                                |
| Image Loading | Coil                                        | 2.6+                                |
| Charting      | Vico (Compose-first)                        | Use guide                           |
| Security      | EncryptedSharedPreferences, BiometricPrompt | AndroidX                            |
| Logging       | Timber                                      | 5.0+                                |
| Testing       | JUnit 5, MockK, Turbine, Compose UI Testing | —                                   |
| CI/CD         | GitHub Actions                              | —                                   |

## Document Content Requirements

Detailed templates for each document are in `references/document-templates.md`.
Architecture and code patterns are in `references/architecture-patterns.md`.
API integration patterns are in `references/api-integration-patterns.md`.

### Quick Reference — What Each Document Must Contain

**01_PRD** — Vision, personas (3-5), user stories (5+ per module), MVP scope with release phases, competitive analysis, success metrics, risk register, glossary

**02_SRS** — Numbered functional requirements (10+ per core module), non-functional requirements (performance, security, offline, accessibility, localization), Room entity definitions, traceability matrix

**03_SDS** — Architecture layers, complete Gradle config, project structure, Hilt modules, security implementation (cert pinning, encrypted storage, biometrics, ProGuard), offline sync (Room DAOs, SyncWorker, conflict resolution, staleness budgets), networking (Retrofit services, interceptors, token refresh), CI/CD workflows

**04_API_CONTRACT** — Base URLs, auth model, JWT structure, every endpoint with method + path + request JSON + response JSON + validation rules + error responses, pagination model, rate limits, error code reference

**05_USER_JOURNEYS** — 8-12 journeys with ASCII flow diagrams, step-by-step breakdowns, error paths, offline behavior. Must include: first-time setup, login, primary transaction, offline transaction, search, dashboard, error recovery

**06_TESTING_STRATEGY** — Test pyramid (60/25/10/5), unit test examples (ViewModel with Turbine, UseCase, Repository), UI test examples (Compose), integration tests (MockWebServer, Room), security tests, performance benchmarks, CI gates, test data fixtures

**07_RELEASE_PLAN** — Play Store setup, signing strategy, release channels with staged rollout, versioning, privacy policy checklist, app store listing, in-app update strategy, release checklist, rollback procedure, post-launch monitoring

## Adaptation Rules

### Partial Module Selection

When the user requests only specific modules:

1. Still generate ALL 7 documents, but scope content to selected modules
2. Auth module is always included (required for any authenticated app)
3. Dashboard adapts to show only KPIs relevant to selected modules
4. API Contract only documents endpoints for selected modules
5. User Journeys only cover flows for selected modules
6. Room entities only include tables needed by selected modules

### No Offline Requirement

If the user says offline support is not needed:

1. Remove `sds/04-offline-sync.md` entirely
2. Simplify Repository pattern (no local-first fallback)
3. Remove SyncWorker and WorkManager sync setup
4. Remove offline-related NFRs from SRS
5. Remove offline user journeys
6. Keep Room for caching only (not as offline data store)

### Module-Gated vs All-Inclusive

If modules are subscription-gated:

- Add module unlock system to SDS (feature flags, ModuleAccessManager)
- Add module discovery journey to User Journeys
- Add locked-module UI patterns (upgrade prompts, feature previews)

If all modules are available to all users:

- Remove module gating from SDS
- Remove module discovery journey
- Gate features by role/permission only

### Regional Customization

Adapt to target market:

- **East Africa**: M-Pesa/Mobile Money, UGX/KES/TZS, Swahili/English, low-bandwidth optimization
- **West Africa**: Paystack, NGN/GHS, French/English/Hausa, USSD fallback
- **Southeast Asia**: GrabPay/GCash, local currencies, multi-script support
- **Global**: Stripe, multi-currency, broad language support

## Quality Checklist (Run After All Documents)

- [ ] Every FR traces to at least one API endpoint
- [ ] Every API endpoint has complete request/response JSON
- [ ] Every Room entity maps to a backend data model
- [ ] Auth flow matches the web app's actual implementation
- [ ] All Kotlin code compiles conceptually (correct imports, types, annotations)
- [ ] No file exceeds 500 lines
- [ ] All sub-files have back-links to parent index
- [ ] All indexes link to all sub-files
- [ ] Requirement IDs are unique and sequential
- [ ] Version numbers for libraries are realistic and compatible
- [ ] Personas reflect the actual target market
- [ ] Success metrics have specific numeric targets
- [ ] Release plan includes rollback procedure

## Cross-Skill References

Load these skills alongside for deeper implementation guidance:

- `android-development` — Kotlin/Android coding standards
- `android-tdd` — Test-driven development workflow
- `android-data-persistence` — Room, DataStore, offline-first patterns
- `jetpack-compose-ui` — Compose UI standards and Material 3
- `dual-auth-rbac` — Authentication and permission system
- `api-error-handling` — API error response patterns
- `modular-saas-architecture` — Module toggle and subscription gating
- `multi-tenant-saas-architecture` — Tenant isolation patterns
