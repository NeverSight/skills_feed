---
name: hevy
description: |
  Create and edit workout routines in Hevy fitness app via API. User-invocable with /hevy.

  Use when: User wants to create/edit Hevy routines, convert training programs (text/PDF/image)
  to Hevy format, or work with the Hevy API.

  Triggers: "/hevy", "hevy routine", "add to hevy", "gym routine", "gym program",
  "lifting program", "training plan", "PPL", "push pull legs", "5x5", "531",
  "GZCLP", "nSuns", "import workout", "sync to hevy", "weightlifting"
---

# Hevy Routine Creator

**Before starting**: The Hevy API is fragile. Small mistakes (wrong field, `@` in notes, missing wrapper) cause silent failures. Follow this skill exactly—shortcuts cause debugging pain.

**Paths**: All `scripts/` and `references/` paths are relative to THIS skill's directory (where this SKILL.md lives), NOT the user's current working directory. Use full path: `<skill-dir>/scripts/hevy-api`.

## Workflow

1. Parse workout plan - extract exercises, sets, reps, weights, rest times
2. **MANDATORY: Read `references/api-reference.md`** before ANY API call
   - Contains critical quirks that cause silent failures
   - Do NOT skip the "API Quirks" section
3. Map exercises to IDs (see decision tree below)
   **Do NOT load** `exercises-by-category.md` until actively mapping names to IDs.
   Search tip: Ctrl+F by muscle group header (e.g., `## quadriceps`).
4. **MANDATORY: Read `references/routine-examples.md`** for JSON structure
5. Create via `<skill-dir>/scripts/hevy-api`

**Do NOT load** all references upfront - load as needed per step.

## NEVER Do

- **NEVER** call the Hevy API directly - always use `<skill-dir>/scripts/hevy-api` which handles authentication
- **NEVER** use `@` in notes fields - causes silent Bad Request (HTML response)
- **NEVER** forget to wrap routine: `{"routine": {...}}` not just `{...}`
- **NEVER** include read-only fields in PUT:
  - `routine.id`, `routine.folder_id`, `routine.created_at`, `routine.updated_at`
  - `exercises[].index`, `exercises[].title`
  - `sets[].index`
- **NEVER** mismatch set properties and exercise type (see `quick-reference.md` for table):
  - `weight_reps` → `weight_kg`, `reps`
  - `reps_only` → `reps` only (no weight!)
  - `duration` → `duration_seconds`
  - `distance_duration` → `distance_meters`, `duration_seconds`
- **NEVER** set `rest_seconds` on first exercise of superset (only last gets rest)
- **NEVER** use `pageSize` > 10 for `/v1/routine_folders`
- **NEVER** assume exercise name matches exactly - search by keyword, verify ID against `exercises-by-category.md`
- **NEVER** create custom exercise without first searching partial name variations (e.g., "Squat" not just "Back Squat")
- **NEVER** guess exercise IDs - always verify against reference files or API response

**Note:** The `notes` field is optional—can be omitted entirely or set to empty string `""`.

## Parsing Workout Plans

Before building JSON, think through:
- **Goal**: Strength (low rep, high weight), hypertrophy (moderate rep), or conditioning (high rep/time)?
- **Structure**: Are exercises grouped (supersets/circuits) or sequential with rest?
- **Ambiguity**: What's implicit? Missing weights = leave empty. Missing rest = use 90s default.

**What type of set?**
| Input Pattern | Set Type | Notes |
|---------------|----------|-------|
| "Warmup", "warm up", "build up" | `"type": "warmup"` | Not counted in working sets |
| "5x5", "3x10", working sets | `"type": "normal"` | Standard working set |
| "AMRAP", "max reps", "test", "to failure" | `"reps": null` | Leave reps open |
| "Drop set" | `"type": "dropset"` | Reduced weight continuation |

**Superset or sequential?**
- "A1/A2", "superset", "paired with", "alternate with" - same `superset_id` (use integers: 0, 1, 2...)
- "Circuit" or "EMOM" - all exercises share one `superset_id`
- Separate exercises with rest between - `superset_id: null`

**Rest timing interpretation:**
- Hevy tracks rest per-exercise, not per-set
- "90s rest between sets" - `rest_seconds: 90`
- For supersets: rest goes on LAST exercise only
- "No rest" or "immediately" - `rest_seconds: 0`

**Weight interpretation:**
- Always use `weight_kg` (Hevy converts for display)
- "bodyweight" exercises - typically `reps_only` type, no weight field
- "BW + 20kg" - use `bodyweight_weighted` exercise variant

**Before creating custom exercise, ask:**
- Did I search partial names? (e.g., "row" finds 15+ variations)
- Did I check equipment variants? (Barbell, Dumbbell, Cable, Machine, Smith)
- Could it exist under a different name? ("Skull Crushers" = "Lying Tricep Extension")
- Is this genuinely missing from Hevy's 400+ built-in exercises?

If all yes → create custom. Otherwise, use the existing match.

## Exercise ID Lookup

| Step | Action | If Found | If Not Found |
|------|--------|----------|--------------|
| 1 | Search `quick-reference.md` | Use ID ✓ | Continue → |
| 2 | Search `exercises-by-category.md` (partial match) | Use ID ✓ | Continue → |
| 3 | Check `~/.hevy/custom-exercises.md` | Use ID ✓ | Continue → |
| 4 | Fetch API: `<skill-dir>/scripts/hevy-api GET '/v1/exercise_templates?page=1&pageSize=100'` | Cache + Use ID ✓ | Continue → |
| 5 | Create custom exercise | — | — |

**Multiple matches at step 2?** Ask user to pick variant. If no response, use default priority: Barbell > Dumbbell > Machine > Bodyweight.

## Bulk Operations (Multi-Week Programs)

For programs with many routines (e.g., 12-week plan):

1. **Create folder first** - Group routines logically
2. **Process in batches** - Create 3-5 routines, verify success, continue. Wait 2-3s between calls to avoid rate limits.
3. **Use consistent naming** - `T{week} {day} - {description}` (e.g., "T1 Mon - Upper")
4. **Track progress** - Note created routine IDs in case of partial failure
5. **If one fails** - Fix and retry that routine only; don't restart the batch

## Pre-Submission Validation

**MANDATORY before any POST/PUT:**

1. **Exercise IDs exist** - Every `exercise_template_id` verified against `exercises-by-category.md` or custom cache
2. **Set properties match type** - Cross-check against table in NEVER section
3. **No `@` in notes** - Search JSON for `@` symbol, replace with "at"
4. **Wrapper present** - JSON is `{"routine": {...}}` not bare object
5. **No read-only fields** (for PUT) - Remove `id`, `folder_id`, `created_at`, `updated_at`, `index`, `title`
6. **Superset rest correct** - Only last exercise in superset has `rest_seconds > 0`

**Quick validation command:**
```bash
jq -e '.routine and (.routine.exercises | length > 0) and ([.. | .notes? // empty | select(contains("@"))] | length == 0)' .tmp-hevy/routine.json && echo "✓ Valid" || echo "✗ Check: wrapper, exercises, @ symbols"
```

If validation fails, fix before proceeding. Do NOT attempt API call with known issues.

## API Access

Use the `hevy-api` script from this skill's directory (NOT `./scripts/`):
```bash
<skill-dir>/scripts/hevy-api GET /v1/routines                          # List routines
<skill-dir>/scripts/hevy-api GET /v1/routine_folders                   # List folders
<skill-dir>/scripts/hevy-api POST /v1/routines .tmp-hevy/routine.json  # Create routine
<skill-dir>/scripts/hevy-api PUT /v1/routines/<id> .tmp-hevy/routine.json
<skill-dir>/scripts/rename-routine.sh <id> "New Title"                 # Rename helper
```

**JSON files:** Write to `.tmp-hevy/`, validate, then clean up:
```bash
mkdir -p .tmp-hevy
# write JSON to .tmp-hevy/routine.json
jq . .tmp-hevy/routine.json >/dev/null && <skill-dir>/scripts/hevy-api POST /v1/routines .tmp-hevy/routine.json
rm -rf .tmp-hevy
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| HTML response / Bad Request | `@` in notes | Replace with "at" or remove |
| "field not allowed" on PUT | Read-only field included | Remove fields per NEVER list above |
| Exercise not found | Typo or custom exercise | Search partial name, check customs, create if needed |
| Empty response | Wrong pagination | Check `page_count`, use correct `pageSize` |
| Folder not found | Wrong folder_id | Fetch: `<skill-dir>/scripts/hevy-api GET /v1/routine_folders` |
| 401 Unauthorized | Invalid/expired API key | Check `~/.hevy/.api_key` has no quotes/whitespace |
| 429 Rate limit | Too many requests | Wait 60s, slow down batch operations |
| 500 Server error | Hevy API issue | Wait 30s, retry once; if persists, API is down |
| Partial batch failure | One routine failed | Note successful IDs, fix failed JSON only, continue |

**General debugging:** Check error message → Verify JSON against `routine-examples.md` → Test minimal routine (1 exercise, 1 set) to isolate issue.

**For complex failures:** Read `references/api-reference.md#error-recovery`
