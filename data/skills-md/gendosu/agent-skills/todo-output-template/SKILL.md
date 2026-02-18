---
name: todo-output-template
description: |
  TODO.md file output template examples for todo-task-planning command.
  Provides structured checklist format with task classification, status indicators, and research rationale.
model: Haiku
---

# TODO Output Template

This template shows the expected output format for `/todo-task-planning` command results.

## Overview

The output template demonstrates:
- **Execution Summary**: Research performance, technical analysis, and duplicate checks
- **Task Classification**: Tasks organized by feasibility (✅ Ready, ⏳ Pending, 🔍 Research, 🚧 Blocked)
- **Complete Checklist Format**: All items in markdown checklist format with status indicators
- **Research Rationale**: File references (📁) and analysis basis (📊) for each task
- **Git Workflow Integration**: Branch creation and PR tasks when `--branch` or `--pr` options are used

## Template Structure

### Option-Based Variations

**Differences by Option**:
- **`--branch` only**: Phase 0 (Branch Creation) is added, Phase 4 (PR and Merge) is NOT added
- **`--pr`**: Both Phase 0 (Branch Creation) and Phase 4 (PR and Merge) are added
- **No options**: Neither Phase 0 nor Phase 4 is added

### Full Example Template

**Note**: The following is an example when `--branch` option is specified. In practice, include only tasks directly necessary to achieve the objective.

```markdown
## 📊 Thorough Execution Summary
- [ ] **Research Performance**: 18 files and 5 directories researched and completed
- [ ] **Technical Analysis**: Confirmed Nuxt.js 3.x + MySQL configuration
- [ ] New tasks: 6 (✅3, ⏳1, 🔍1, 🚧1)
- [ ] **Research Rationale**: Detailed analysis of 8 files, confirmation of 3 technical constraints
- [ ] **Duplicate Check**: Avoided duplication of 4 past researches, 2 questions, 1 task
- [ ] **docs/memory saved**: analysis/2025-01-15-auth-flow.md, questions/auth-questions.md
- [x] **Updated file**: $ARGUMENTS file (directly updated and verified)

## 📋 Task List (Complete Checklist Format)

### Phase 0: ブランチ作成 ✅ (when --branch option is specified)

- [ ] ✅ **ブランチを作成**
  - コマンド: `git checkout -b feature/actionlog-notification`
  - 📋 このブランチで全ての変更をコミット
  - 推定時間: 1分

### 🎯 Ready Tasks (✅ Immediately Executable)
- [ ] ✅ API authentication system implementation 📁`src/api/auth/` 📊Authentication flow confirmed
  - [ ] Implement login endpoint - Create `auth/login.ts`
    - 💡 Use Express.js POST handler pattern from `auth/register.ts`
    - 💡 Validate credentials with bcrypt, generate JWT token
    - 💡 Return { token, user } on success, 401 on failure
  - [ ] Implement token verification middleware - Create `middleware/auth.ts`
    - 💡 Follow middleware pattern in `middleware/logger.ts`
    - 💡 Use jsonwebtoken.verify() to validate token from Authorization header
    - 💡 Attach decoded user to req.user for downstream handlers
  - [ ] Add session management - Extend `utils/session.ts`
    - 💡 Add createSession() and destroySession() methods
    - 💡 Use Redis client pattern from `utils/cache.ts`
- [ ] ✅ Database schema update 📁`prisma/schema.prisma` 📊MySQL support
  - [ ] Update Prisma schema - Add new model definitions
    - 💡 Follow existing User model pattern (id, createdAt, updatedAt fields)
    - 💡 Add Session model with userId foreign key relation
  - [ ] Generate migration - Execute `npx prisma migrate dev`
    - 💡 Run after schema changes, provide descriptive migration name
- [🔄] ✅ User profile page implementation 📁`pages/user/profile.vue` - In progress
  - [x] Basic profile display ✓ `components/UserProfile.vue` completed
  - [ ] Add profile edit functionality - Create `components/UserProfileEdit.vue`
    - 💡 Copy form structure from `components/UserProfile.vue`
    - 💡 Add v-model bindings for editable fields (name, email, bio)
    - 💡 Call PATCH /api/user/:id with updated data on submit
- [ ] ✅ Commit after implementation complete
  - 💡 Execute micro-commit to commit changes by context
  - 💡 Estimated time: 2-3 minutes

### ⏳ Pending Tasks (Waiting for Dependencies)
- [ ] ⏳ Frontend UI integration 📁`components/` - After API completion (waiting for `auth/login.ts` completion)
  - [ ] Login form component - Create `components/LoginForm.vue`
  - [ ] API client setup - Configure `composables/useApi.ts`

### 🔍 Research Tasks (Research Required)
- [ ] 🔍 Third-party API integration 📊To research: API documentation and authentication method
  - [ ] Review API documentation - Check endpoints and rate limits
  - [ ] Determine authentication approach - OAuth vs API key

### 🚧 Blocked Tasks (Blocked)
- [ ] 🚧 Payment integration 📊Blocking factor: Payment provider not decided, Stripe vs PayPal
  - [ ] Payment provider selection - Compare pricing and features
  - [ ] Payment flow design - Determine checkout process

## ❓ Questions Requiring Confirmation (Checklist Format with Research Rationale)
- [ ] [Specification] What authentication method should be used? 📊Current status: Session-based auth implemented, token-based TBD
- [ ] [UI] What is the design system color palette? 📊Current status: Basic Tailwind config, custom theme not set
- [ ] [UX] What are the detailed specifications of the user flow? 📊Current status: Only basic authentication flow implemented

## 🎯 Next Actions (Checklist Format)
- [ ] Collect answers to blocker questions, confirm authentication approach
- [ ] Start implementation from ✅Ready tasks, progress step-by-step
- [ ] Confirm and adjust dependencies
```

## Key Elements

### Status Indicators
- `✅` Ready - Immediately executable tasks
- `⏳` Pending - Waiting for dependencies
- `🔍` Research - Research required before implementation
- `🚧` Blocked - Blocked by unclear specifications or decisions
- `[🔄]` In progress - Currently being worked on
- `[x]` Completed - Task finished

### Reference Symbols
- `📁` File reference - Indicates target implementation files
- `📊` Research rationale - Shows analysis basis and technical constraints
- `💡` Implementation hint - Provides guidance from existing codebase patterns
- `📋` Checklist format - Indicates structured task breakdown

### Task Structure
Each task should include:
1. **Status indicator** (✅⏳🔍🚧)
2. **Task description** with clear objective
3. **File references** (📁) showing target files
4. **Research rationale** (📊) showing analysis basis
5. **Subtasks** with implementation hints (💡) when applicable
6. **Dependencies** explicitly stated for ⏳ Pending tasks
7. **Blocking factors** explicitly stated for 🚧 Blocked tasks
