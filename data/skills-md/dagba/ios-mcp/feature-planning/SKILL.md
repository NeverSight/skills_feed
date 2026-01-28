---
name: feature-planning
description: Break down features into implementable tasks and choose architecture approach. Use when starting a new feature or receiving requirements that need technical decomposition.
---

# Feature Planning

## Overview

Systematic approach to decompose features into actionable tasks. For senior engineers who know how to code but need a structured thinking framework.

## Quick Workflow

### 1. Requirement Analysis
- Clarify user goal and acceptance criteria
- Identify screens, data flows, integration points
- Ask: API ready? Design assets available? Platform requirements?

### 2. Choose Architecture

Use **architecture-patterns** skill to decide:
- Simple (1-2 screens, local state) → MV
- Medium (3-5 screens, business logic) → MVVM
- Complex (state machines, side effects) → TCA
- Enterprise (multi-team) → Clean Architecture

### 3. Task Breakdown Structure

**Phase 1: Foundation**
- Models/entities
- API client stubs
- Navigation structure

**Phase 2: Core Logic**
- ViewModels/Reducers
- Business rules
- State management

**Phase 3: UI**
- Layouts and components
- Styling and animations
- Loading/error states

**Phase 4: Integration**
- Wire up ViewModels to Views
- Connect to backend
- Handle edge cases

**Phase 5: Quality**
- Unit tests (ViewModels, business logic)
- UI tests (critical flows)
- Accessibility audit

### 4. Risk Assessment

| Risk | Mitigation |
|------|------------|
| Unknown APIs | Define contract early, use mocks |
| New technology | POC spike first, allocate learning time |
| Performance concerns | Profile early, plan caching/pagination |
| Tight deadline | Negotiate scope, identify MVP |

### 5. Estimation

**Rule of Thumb:** Sum task estimates + 30-50% buffer

Break tasks into <1 day chunks. If a task feels >1 day, decompose further.

## Implementation Plan Template

```markdown
# Feature: [Name]

## Overview
[1-2 sentences: what and why]

## Architecture
Pattern: MVVM
State: @Observable
Navigation: NavigationStack

## Tasks

### Phase 1: Foundation (Day 1)
- [ ] Define models
- [ ] Create API client protocol
- [ ] Setup navigation routes

### Phase 2: Logic (Day 2-3)
- [ ] Implement ViewModels
- [ ] Add validation
- [ ] Handle errors

### Phase 3: UI (Day 4)
- [ ] Build main screen
- [ ] Add animations
- [ ] Loading states

### Phase 4: Testing (Day 5)
- [ ] Unit tests
- [ ] UI tests

## Dependencies
- Backend API: [Status]
- Design: [Link]
- Third-party: [None/List]

## Risks
[Table from Risk Assessment]

## Acceptance Criteria
- [ ] User can [action]
- [ ] Error handling complete
- [ ] Unit test coverage >80%
- [ ] Accessibility labels
```

## Integration with Other Skills

Typical flow:
1. **feature-planning** (this skill) - Decompose and plan
2. **architecture-patterns** - Implement chosen pattern
3. **swiftui-*-patterns** - Build UI
4. **swift-concurrency-expert** - Fix concurrency issues
5. Verify and ship

## Key Principles

- **Break tasks <1 day** - Forces clarity, enables parallelization
- **Identify MVP early** - Know what's must-have vs. nice-to-have
- **Plan for testing** - Not an afterthought
- **Document decisions** - Record why you chose an approach
- **30-50% buffer** - Accounts for unknowns and review cycles

---

**Word count:** ~400 (was 2,099)
**For:** Senior/mid engineers who need structure, not hand-holding
**Focus:** Decision-making and decomposition, not tutorials
