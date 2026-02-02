---
name: product-manager
description: Audits feature completeness by scanning codebases and comparing against PRD requirements. Identifies gaps between backend implementation and user-facing accessibility. Generates remediation tasks and integrates with prd-analyzer output. Supports multiple frameworks including Next.js, React Router, TanStack, React Native, Expo, and more.
---

# Product Manager

Ensures features are not just implemented but actually user-accessible. Bridges the gap between "code complete" and "user can use it."

**Integrates with:**
- `prd-analyzer` — Reads tasks.db, features.json, PROJECT.md
- All implementation skills — Validates their output is user-facing

## The Problem This Solves

```
PRD says: "User can export analytics to Tableau"
Backend:   ✓ analytics-api.ts exists with Tableau endpoints
Frontend:  ✗ No /analytics route
Navigation: ✗ No menu item
Result:    Feature "done" in tasks.db, but users can't access it
```

## Core Workflow

```
1. DISCOVER   → Find project structure and framework
2. READ       → Load PRD features from prd-analyzer output
3. SCAN       → Search codebase for implementation evidence
4. AUDIT      → Check user-facing accessibility
5. ANALYZE    → Compare requirements vs reality
6. REPORT     → Generate gap analysis
7. REMEDIATE  → Create tasks for missing pieces
```

---

## Quick Start

### 1. Discover Project

```bash
# Identify framework and structure
ls -la
cat package.json
```

Look for:
- Framework indicators (next.config.js, vite.config.ts, expo.json, etc.)
- Source structure (src/, app/, pages/, etc.)
- Backend location (backend/, server/, api/, etc.)

### 2. Load PRD Context

```bash
# From prd-analyzer output
cat .claude/PROJECT.md
cat .claude/features.json
sqlite3 .claude/tasks.db "SELECT id, title, status FROM epics"
```

### 3. Run Feature Audit

For each feature:
1. Check backend implementation
2. Check frontend implementation  
3. Check user accessibility
4. Record findings

### 4. Generate Report

Output:
- `audit-report.md` — Human-readable gap analysis
- `audit-results.json` — Programmatic results
- Updated `tasks.db` — Remediation tasks added

---

## Feature Completeness Model

### Completeness Levels

| Level | Name | Meaning |
|-------|------|---------|
| 0 | **Not Started** | No implementation evidence |
| 1 | **Backend Only** | Service/API exists, no frontend |
| 2 | **Frontend Exists** | UI components exist, not accessible |
| 3 | **Routable** | Has route/screen, not in navigation |
| 4 | **Accessible** | In navigation, users can reach it |
| 5 | **Complete** | Accessible + documented + tested |

### Completeness Checklist

```markdown
## Feature: [Name]

### Implementation
- [ ] Backend service/API implemented
- [ ] Database schema exists (if needed)
- [ ] Frontend components exist
- [ ] API integration complete

### Accessibility  
- [ ] Route/screen exists
- [ ] Reachable from navigation
- [ ] Mobile responsive (if web)
- [ ] Works on target platforms

### Polish
- [ ] Error states handled
- [ ] Loading states present
- [ ] Empty states designed
- [ ] Documented in help/docs

### Verdict: Level [0-5]
```

---

## Framework Detection

### Automatic Detection

```javascript
// Detection order
const frameworkIndicators = {
  // Web Frameworks
  'next.config.js':     'nextjs',
  'next.config.mjs':    'nextjs',
  'next.config.ts':     'nextjs',
  'vite.config.ts':     'vite',
  'vite.config.js':     'vite',
  'remix.config.js':    'remix',
  'astro.config.mjs':   'astro',
  
  // React Router / TanStack
  'src/routes.tsx':     'react-router',
  'src/router.tsx':     'tanstack-router',
  'app/routes/':        'remix',
  
  // Mobile
  'app.json':           'expo',
  'expo.json':          'expo',
  'react-native.config.js': 'react-native',
  'ios/':               'react-native',
  'android/':           'react-native',
  
  // Backend
  'backend/':           'separate-backend',
  'server/':            'separate-backend',
  'api/':               'api-routes',
};
```

### Framework-Specific Patterns

| Framework | Routes Location | Navigation | API Calls |
|-----------|-----------------|------------|-----------|
| Next.js (pages) | `pages/**/*.tsx` | `components/nav` | `lib/api`, `services/` |
| Next.js (app) | `app/**/page.tsx` | `app/layout.tsx` | `app/api/`, `lib/` |
| React Router | `src/routes.tsx` | `src/components/` | `src/api/`, `src/services/` |
| TanStack Router | `src/routes/` | `src/components/` | `src/lib/` |
| Remix | `app/routes/` | `app/root.tsx` | `app/routes/*.server.ts` |
| React Native | `src/screens/` | `src/navigation/` | `src/api/`, `src/services/` |
| Expo Router | `app/` | `app/_layout.tsx` | `src/api/` |

**Detailed patterns:** See [references/framework-patterns.md](references/framework-patterns.md)

---

## Scanning Process

### Backend Scan

Find evidence of implementation:

```bash
# Services
find backend/src/services -name "*.ts" | head -20
grep -l "export.*class\|export.*function" backend/src/services/*.ts

# API routes/handlers
find . -path "*/api/*" -name "*.ts" | head -20
find . -path "*/handlers/*" -name "*.ts" | head -20

# Database models/schema
find . -name "schema.ts" -o -name "models.ts" -o -name "*.model.ts"
```

### Frontend Scan

Find UI implementation:

```bash
# Routes/pages (framework-dependent)
find . -path "*/pages/*" -name "*.tsx" 2>/dev/null
find . -path "*/app/*" -name "page.tsx" 2>/dev/null
find . -path "*/screens/*" -name "*.tsx" 2>/dev/null
find . -path "*/routes/*" -name "*.tsx" 2>/dev/null

# Components
find . -path "*/components/*" -name "*.tsx" | grep -i "FEATURE_NAME"

# Navigation
grep -r "href=\|to=\|navigate\|Link" --include="*.tsx" src/components/nav/
```

### API Integration Scan

Verify frontend calls backend:

```bash
# Find API calls
grep -r "fetch\|axios\|useMutation\|useQuery" --include="*.tsx" src/

# Find service imports
grep -r "import.*from.*services\|import.*from.*api" --include="*.tsx" src/
```

### Navigation Scan

Check if feature is reachable:

```bash
# Find navigation components
find . -name "*nav*" -o -name "*sidebar*" -o -name "*menu*" | grep -E "\.(tsx|jsx)$"

# Check for links to feature
grep -r "/FEATURE_ROUTE" --include="*.tsx" src/
```

---

## Audit Output

### Audit Report Structure

```markdown
# Feature Audit Report

**Project**: VoiceForm AI
**Audit Date**: 2026-01-12
**Framework**: Next.js (App Router) + Separate Backend

## Summary

| Metric | Count |
|--------|-------|
| Total Features | 30 |
| Fully Complete (L5) | 12 |
| Accessible (L4) | 5 |
| Routable (L3) | 3 |
| Frontend Exists (L2) | 2 |
| Backend Only (L1) | 8 |
| Not Started (L0) | 0 |

**Overall Completion**: 40% fully user-accessible

## Critical Gaps (P0 Features)

| Feature | Level | Missing |
|---------|-------|---------|
| F028 Analytics API | L1 | Frontend route, Navigation, UI |
| F029 Tenant Isolation | L1 | Settings UI, BYOK config screen |

## All Features

### F001: Survey Studio
**Level**: 5 - Complete ✅

**Evidence**:
- Backend: `backend/src/services/survey-studio.ts` ✓
- Route: `app/surveys/new/page.tsx` ✓
- Navigation: Sidebar "Create Survey" link ✓
- Documentation: Help article exists ✓

---

### F028: Analytics API
**Level**: 1 - Backend Only 🔴

**Evidence**:
- Backend: `backend/src/services/analytics-api.ts` ✓
- Route: ❌ No `/analytics` route found
- Navigation: ❌ No analytics link in navigation
- Documentation: ❌ No help article

**Remediation Required**:
1. Create `app/analytics/page.tsx`
2. Add Analytics to main navigation
3. Build dashboard components
4. Document analytics features

---

[...continues for all features...]
```

### JSON Output

```json
{
  "audit_date": "2026-01-12",
  "project": "VoiceForm AI",
  "framework": {
    "frontend": "nextjs-app",
    "backend": "separate",
    "mobile": null
  },
  "summary": {
    "total_features": 30,
    "by_level": {
      "L5_complete": 12,
      "L4_accessible": 5,
      "L3_routable": 3,
      "L2_frontend_exists": 2,
      "L1_backend_only": 8,
      "L0_not_started": 0
    }
  },
  "features": [
    {
      "id": "F028",
      "title": "Analytics API",
      "level": 1,
      "level_name": "backend_only",
      "evidence": {
        "backend": {
          "found": true,
          "files": ["backend/src/services/analytics-api.ts"]
        },
        "frontend": {
          "found": false,
          "files": []
        },
        "route": {
          "found": false,
          "path": null
        },
        "navigation": {
          "found": false,
          "location": null
        }
      },
      "remediation": [
        {
          "type": "create_route",
          "description": "Create analytics page",
          "path": "app/analytics/page.tsx"
        },
        {
          "type": "add_navigation",
          "description": "Add Analytics to sidebar"
        }
      ]
    }
  ]
}
```

---

## Remediation Task Generation

### Task Creation

For each gap, generate tasks in tasks.db:

```sql
-- New story for missing frontend
INSERT INTO stories (id, epic_id, title, description, status)
VALUES (
  'story-028-frontend',
  'epic-028',
  'Analytics Frontend Implementation',
  'Create user-facing analytics dashboard',
  'todo'
);

-- Tasks for the story
INSERT INTO tasks (id, story_id, title, task_type, estimate_hours, status)
VALUES 
  ('task-028-f01', 'story-028-frontend', 'Create /analytics route', 'frontend', 4, 'todo'),
  ('task-028-f02', 'story-028-frontend', 'Build analytics dashboard components', 'frontend', 8, 'todo'),
  ('task-028-f03', 'story-028-frontend', 'Add Analytics to navigation', 'frontend', 1, 'todo'),
  ('task-028-f04', 'story-028-frontend', 'Connect to analytics API', 'frontend', 4, 'todo');
```

### Priority Assignment

| Gap Type | Priority | Rationale |
|----------|----------|-----------|
| P0 feature backend-only | P0 | Critical feature unusable |
| P1 feature backend-only | P1 | Important feature unusable |
| Missing navigation | P1 | Feature exists but hidden |
| Missing documentation | P2 | Feature works but undiscoverable |
| Missing error states | P2 | Polish issue |

---

## Integration with prd-analyzer

### Reading PRD Context

```python
import sqlite3
import json

def load_prd_context(project_path: str):
    """Load features from prd-analyzer output"""
    
    # Load features.json
    with open(f"{project_path}/.claude/features.json") as f:
        features = json.load(f)
    
    # Load from tasks.db
    conn = sqlite3.connect(f"{project_path}/.claude/tasks.db")
    conn.row_factory = sqlite3.Row
    
    epics = conn.execute("""
        SELECT e.*, 
               COUNT(s.id) as story_count,
               SUM(CASE WHEN s.status = 'done' THEN 1 ELSE 0 END) as done_count
        FROM epics e
        LEFT JOIN stories s ON s.epic_id = e.id
        GROUP BY e.id
    """).fetchall()
    
    return {
        "features": features,
        "epics": [dict(e) for e in epics]
    }
```

### Updating Task Status

When audit finds discrepancies:

```sql
-- Mark feature as needing frontend work
UPDATE epics 
SET status = 'needs_frontend', 
    updated_at = datetime('now')
WHERE id = 'epic-028';

-- Add audit metadata
INSERT INTO epic_metadata (epic_id, key, value)
VALUES ('epic-028', 'audit_level', '1'),
       ('epic-028', 'audit_date', '2026-01-12'),
       ('epic-028', 'audit_gaps', 'route,navigation,documentation');
```

---

## Running an Audit

### Full Audit Command

```bash
# In Claude Code session:

# 1. Read project structure
cat package.json
ls -la src/ app/ pages/ 2>/dev/null

# 2. Load PRD context
cat .claude/features.json
sqlite3 .claude/tasks.db "SELECT id, title, priority FROM epics ORDER BY id"

# 3. For each feature, scan for evidence
# (Claude does this systematically)

# 4. Generate report
# Outputs to .claude/audit-report.md and .claude/audit-results.json
```

### Quick Audit (Single Feature)

```bash
# Audit just F028
# 1. Find backend
find . -name "*analytics*" -type f

# 2. Find frontend  
find . -path "*app*" -o -path "*pages*" | xargs grep -l "analytics" 2>/dev/null

# 3. Check navigation
grep -r "analytics" --include="*.tsx" src/components/nav/ app/layout.tsx

# 4. Report finding
echo "F028: Level 1 - Backend only, no frontend route"
```

---

## Anti-Patterns

### Audit Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Trusting tasks.db status | "Done" ≠ user-facing | Always verify in codebase |
| Only checking file existence | File may be empty/stub | Check for real implementation |
| Ignoring navigation | Feature unreachable | Verify menu/nav links |
| Skipping mobile | Desktop-only isn't complete | Check responsive/native |
| No documentation check | Users can't discover | Verify help/docs exist |

### Remediation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Generic tasks | "Add frontend" too vague | Specific: "Create /analytics route" |
| Missing dependencies | Frontend before backend | Check implementation order |
| Overloading | 50 tasks at once | Prioritize by P-level |
| No estimates | Can't plan | Add hour estimates |

---

## Checklist: Running Product Audit

### Before Audit
- [ ] prd-analyzer has run (tasks.db exists)
- [ ] Project structure understood
- [ ] Framework identified
- [ ] Backend location known
- [ ] Frontend location known

### During Audit
- [ ] Each feature checked systematically
- [ ] Backend evidence recorded
- [ ] Frontend evidence recorded
- [ ] Route existence verified
- [ ] Navigation links verified
- [ ] Level assigned (0-5)

### After Audit
- [ ] Report generated (markdown)
- [ ] Results saved (JSON)
- [ ] Remediation tasks created
- [ ] tasks.db updated
- [ ] Priorities assigned

---

**References:**
- [references/framework-patterns.md](references/framework-patterns.md) — Scanning patterns for each framework
- [references/completeness-criteria.md](references/completeness-criteria.md) — Detailed level definitions
- [references/gap-analysis.md](references/gap-analysis.md) — Analysis methodology
- [references/remediation-templates.md](references/remediation-templates.md) — Task templates for common gaps
