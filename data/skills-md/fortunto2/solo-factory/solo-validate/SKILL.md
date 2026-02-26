---
name: solo-validate
description: Score startup idea through S.E.E.D. niche check + STREAM 6-layer analysis + Devil's Advocate inversion, auto-pick stack, and generate PRD with acceptance criteria. Use when user says "validate idea", "score this idea", "should I build this", "go or kill", "generate PRD", or "evaluate opportunity". Do NOT use for deep research (use /research first) or decision-only framework (use /stream).
license: MIT
metadata:
  author: fortunto2
  version: "2.1.1"
  openclaw:
    emoji: "✅"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, WebSearch, mcp__solograph__kb_search, mcp__solograph__project_info, mcp__solograph__web_search
argument-hint: "[idea name or description]"
---

# /validate

Validate a startup idea end-to-end: search KB, run Manifest alignment, S.E.E.D. niche check, Devil's Advocate inversion, STREAM 6-layer analysis, pick stack, generate PRD.

**Philosophy:** Validation should be honest, not optimistic. Better to kill a bad idea in 5 minutes than waste 3 months building it. The goal is truth, not encouragement.

## MCP Tools (use if available)

If MCP tools are available, prefer them over CLI:
- `kb_search(query, n_results)` — search knowledge base for related docs
- `project_info()` — list active projects with stacks
- `web_search(query)` — search for dead startups, competitor failures

If MCP tools are not available, fall back to Grep/Glob/WebSearch.

## Steps

1. **Parse the idea** from `$ARGUMENTS`. If empty, ask the user what idea they want to validate.

2. **Search for related knowledge:**
   If MCP `kb_search` tool is available, use it directly:
   - `kb_search(query="<idea keywords>", n_results=5)`
   Otherwise search locally:
   - Grep for idea keywords in `.md` files across the project and knowledge base
   Summarize any related documents found (existing ideas, frameworks, opportunities).

3. **Deep research (optional):** Check if `research.md` exists for this idea (look in `docs/` or the current working directory).
   - If it exists: read it and use findings to inform STREAM analysis and PRD filling (competitors, pain points, market size).
   - If it does not exist: ask the user if they want to run deep research first. If yes, tell them to run `/research <idea>` and come back. If no, continue without it.

4. **Manifest Alignment Check (with teeth):**

   Consult `references/manifest-checklist.md` (bundled with this skill) for the full checklist of 9 principles and 6 red flags. Check the idea against EACH one. This is not a formality — a manifest violation is a soft kill flag.

   For each principle, assess: comply or violate? If violating — cite the specific principle.

   **Key principles** (see checklist for details):
   1. Privacy-first / offline-first
   2. One pain -> one feature -> launch
   3. AI as foundation, not feature
   4. Speed over perfection (MVP in days)
   5. Antifragile architecture
   6. Money without overheating
   7. Against exploitation
   8. Subscription fatigue
   9. Creators, not robots

   **Scoring:** 0 violations = perfect, 1-2 = caution, 3+ = strong KILL signal.

   **Be honest.** If the idea conflicts with principles, SAY SO. Don't rationalize alignment.

5. **S.E.E.D. niche check** (quick, before deep analysis):

   Score the idea on four dimensions:
   - **S — Searchability:** Can you rank? Forums/Reddit in top-10, few fresh giants, no video blocks?
   - **E — Evidence:** Real pain with real quotes/URLs? Or hypothetical?
   - **E — Ease:** MVP in 1-2 days on existing stack? No heavy dependencies?
   - **D — Demand:** Long-tail keywords exist? Clear monetization path?

   **Kill flags** (stop immediately if any):
   - Top-10 SERP dominated by media giants or encyclopedias
   - Fresh competing content (<60 days old) already covers it well
   - No evidence of real user pain (only founder's hypothesis)
   - MVP needs >1 week even on best-fit stack

   If any kill flag triggers → recommend KILL with explanation. Don't proceed to STREAM.

6. **Devil's Advocate (Inversion):**

   > "Flip the question: how would you guarantee failure?" — STREAM Layer 3 (Inversion)

   This step is mandatory — before scoring positively, actively try to kill the idea. The goal is to find reasons NOT to build it.

   **6a. Inversion — 5 ways this fails:**
   List 5 specific, concrete ways this idea could fail. Not generic risks ("competition") but specific scenarios with evidence:
   - What specific competitor could crush this? (name, funding, strategy)
   - What user behavior makes this unviable? (churn data, willingness to pay)
   - What regulatory/legal event kills this? (specific laws, precedents)
   - What technical limitation blocks this? (latency, cost, accuracy)
   - What market dynamic makes the "opportunity" a mirage?

   **6b. Dead startup search:**
   Search for startups that tried something similar and failed or pivoted:
   - WebSearch: `"<idea category>" startup failed OR pivoted OR shut down`
   - WebSearch: `"<competitor>" pivot OR layoffs OR shutdown`
   - If any found: what killed them? Does the same risk apply here?

   **6c. Unit economics stress test (if research.md exists):**
   Recalculate unit economics with PESSIMISTIC assumptions:

   | Metric | Optimistic | Realistic | Pessimistic |
   |--------|-----------|-----------|-------------|
   | Monthly churn | 10% | 30-40% (industry data) | 50%+ (first year) |
   | Average lifetime | 10 months | 2.5-3 months | 1.5 months |
   | LTV | (price × 10) | (price × 2.5) | (price × 1.5) |
   | CAC | <$20 | $30-50 | $50-80 |
   | LTV:CAC | >3:1 | ~1:1 | <1:1 (UNPROFITABLE) |

   If pessimistic LTV:CAC < 1 → flag as critical risk.

   **6d. "Empty market" test:**
   If the analysis found an "empty" market segment or pricing gap, ask:
   - **Why is it empty?** Is it opportunity or graveyard?
   - Search for companies that tried this exact positioning and failed
   - Is the segment empty because demand doesn't exist at that price point?

   **6e. Manifest conflict honesty:**
   Re-check findings from step 4. For each manifest violation found, state the conflict clearly: "This requires X, which violates principle Y because Z."
   Do NOT rationalize conflicts away. The user decides whether to proceed — not the skill.

7. **STREAM analysis:** Walk the idea through all 6 layers.

   Consult `references/stream-layers.md` (bundled with this skill) for the complete 6-layer framework with questions per layer.

   For EACH layer, provide BOTH positive and negative assessment. Use the actual framework questions:
   - **Layer 1 (Scope):** Map!=Territory, Simplicity, Boundaries — what assumptions are unproven?
   - **Layer 2 (Time):** Entropy, Lindy — will this exist in 5 years?
   - **Layer 3 (Route):** Inversion (use Devil's Advocate findings), Second-Order Effects — effects of effects?
   - **Layer 4 (Stakes):** Asymmetry, Antifragility — real risk/reward with pessimistic numbers
   - **Layer 5 (Audience):** Reputation, Network — deposit or withdrawal?
   - **Layer 6 (Meta):** Mortality, Balance — worth finite time? Aligns with mission?

   **Scoring rules:**
   - Each layer scored 1-10
   - If Devil's Advocate found critical issues, the affected layer score MUST be reduced
   - If Manifest alignment has violations, Layer 6 (Meta) score MUST be reduced
   - Final score = weighted average (Meta and Stakes weighted 1.5x)

8. **Stack selection:** Auto-detect from research data, then confirm or ask.

   **Auto-detection rules** (from `research.md` `product_type` field or idea keywords):
   - `product_type: ios` → `ios-swift`
   - `product_type: android` → `kotlin-android`
   - `product_type: web` + mentions AI/ML → `nextjs-supabase` (or `nextjs-ai-agents`)
   - `product_type: web` + landing/static → `astro-static`
   - `product_type: web` + content site + needs SSR for some pages (CDN data, transcripts, dynamic) → `astro-hybrid`
   - `product_type: web` (default) → `nextjs-supabase`
   - `product_type: api` → `python-api`
   - `product_type: cli` + Python keywords → `python-ml`
   - `product_type: cli` + JS/TS keywords → `nextjs-supabase` (monorepo)
   - Edge/serverless keywords → `cloudflare-workers`

   If auto-detected with high confidence, state the choice and proceed.
   If ambiguous (e.g., could be web or mobile), ask via AskUserQuestion with the top 2-3 options.
   If MCP `project_info` is available, show user's existing stacks as reference.

9. **Generate PRD:** Create a PRD document at `docs/prd.md` in the current project directory. Use a kebab-case project name derived from the idea.

   **PRD must pass Definition of Done:**
   - [ ] Problem statement ≥ 30 words (who suffers, when, why now)
   - [ ] ICP + JTBD — target segment + 2-3 jobs-to-be-done
   - [ ] 3-5 features, each with measurable acceptance criteria
   - [ ] 3-5 KPIs with units (daily/weekly) and target values
   - [ ] Kill/Iterate/Scale thresholds for each KPI
   - [ ] 3-5 risks with mitigation plans
   - [ ] **Honest Assessment section** (from Devil's Advocate step)
   - [ ] **Unit economics: optimistic AND pessimistic** (both columns)
   - [ ] **Dead startup precedents** (who tried this and failed?)
   - [ ] **Manifest conflicts** (explicit list of principle violations)
   - [ ] Tech stack with key packages
   - [ ] Architecture principles (SOLID, DRY, KISS, schemas-first)
   - [ ] Evidence-first — numbers/claims have source URLs (from research.md if available)

10. **Output summary:**
    - Idea name and one-liner
    - S.E.E.D. score (S/E/E/D each rated low/medium/high)
    - Manifest alignment (X/9 principles met, list violations)
    - **Two scores:**
      - **Optimistic score** (0-10): best-case assumptions
      - **Realistic score** (0-10): pessimistic unit economics, real churn, funded competitors
    - Devil's Advocate top finding (the single strongest reason NOT to build)
    - Key risk and key advantage
    - Path to generated PRD
    - **"If I'm wrong about..."** — state the single assumption that, if wrong, changes the verdict
    - **Recommended next action** (one of):
      - `/research <idea>` — if evidence is weak, get data first
      - `/scaffold <name> <stack>` — if realistic score ≥ 7, build it
      - **Fake-Door Test** — if realistic score 5-7, spend $20 on a landing stub before coding
      - **KILL** — if realistic score < 5 or kill flags triggered
      - **PIVOT** — if the idea has merit but current angle fails (suggest specific pivot)

## Important

- Do NOT skip the Devil's Advocate step (step 6). It is mandatory.
- Do NOT skip reading `references/manifest-checklist.md` and `references/stream-layers.md` (bundled with this skill). They contain the actual checklists.
- Quality and honesty are more important than speed. Take your time on steps 4, 6, and 7.
- A KILL recommendation is a valid and valuable outcome. It saves months of wasted effort.

## When to use

- Before building anything non-trivial
- After `/research` or `/swarm` to score and generate PRD
- When deciding between multiple ideas (run on each, compare realistic scores)
- When friends ask for feedback on their startup (be honest, not nice)

## Common Issues

### S.E.E.D. kill flag triggered
**Cause:** Idea fails basic niche viability (SERP dominated, no evidence, MVP too complex).
**Fix:** This is by design — kill flags save time. Consider pivoting the idea or running `/research` for deeper evidence.

### No research.md found
**Cause:** Skipped `/research` step.
**Fix:** Skill asks if you want to research first. For stronger PRDs, run `/research <idea>` before `/validate`.

### Stack auto-detection wrong
**Cause:** Ambiguous product type (could be web or mobile).
**Fix:** Skill asks via AskUserQuestion when ambiguous. Specify product type explicitly in the idea description.

### Score seems too high
**Cause:** Confirmation bias — you found evidence FOR and stopped looking.
**Fix:** Devil's Advocate step is now mandatory. If you skipped it, the score is invalid. Re-run with full inversion.

### Manifest conflicts rationalized away
**Cause:** The idea is exciting but conflicts with principles.
**Fix:** State conflicts explicitly. "This violates X because Y" is more useful than silence. The user decides whether to proceed — not the skill.
