---
name: email-whiz
description: >-
  Gmail inbox copilot via MCP. Triage, inbox zero with streak tracking, smart
  filters, auto-rules, analytics, newsletters, labels, search, senders, digest,
  cleanup, audit. Use when overwhelmed by email or building Gmail filters. NOT
  for: composing emails, calendar, Google Drive, non-Gmail.
argument-hint: "<mode> [options]"
model: opus
disable-model-invocation: true
allowed-tools: gmail_list_emails gmail_search_emails gmail_get_email gmail_get_labels gmail_create_label gmail_modify_email gmail_delete_email gmail_get_filters gmail_get_filter gmail_create_filter gmail_create_filter_from_template gmail_delete_filter gmail_batch_modify_emails gmail_batch_delete_emails gmail_get_or_create_label gmail_update_label gmail_delete_label gmail_send_email Read Grep Write
context: fork
license: MIT
metadata:
  author: wyattowalsh
  version: "3.0.0"
---

# Email Whiz

Gmail inbox management via MCP. Read current labels and filters before taking action.

---

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **4D+N** | DO / DELEGATE / DEFER / REFERENCE / NOISE — five triage buckets |
| **inbox zero** | State where inbox contains only items requiring action today |
| **routine** | Repeatable time-boxed workflow (daily 5 min, weekly 15 min) |
| **streak** | Consecutive days achieving inbox zero; stored in progress file |
| **auto-rule** | Gmail filter created from behavioral pattern analysis |
| **filter** | Gmail rule that matches incoming email and applies actions |
| **VIP** | Sender who receives consistent replies and high-priority treatment |
| **noise** | Automated or low-value email; candidate for filtering/deletion |
| **engagement** | Reply rate to a sender: replies sent ÷ emails received |
| **bankruptcy** | Inbox with 500+ unread or growing backlog — triggers staged recovery |
| **confidence** | HIGH >80% / MEDIUM 50-80% / LOW <50% — governs auto-rule actions |
| **batch op** | Single `gmail_batch_modify_emails` or `gmail_batch_delete_emails` call |

---

## Dispatch

| `$ARGUMENTS` | Action |
|--------------|--------|
| `triage` | Categorize inbox with 4D+N, batch process by category |
| `inbox-zero` | Daily/weekly routine, progress tracking, bankruptcy detection |
| `filters` | Pattern-detected filter suggestions with confidence scoring |
| `auto-rules` | Behavioral analysis → auto-create Gmail filters from templates |
| `analytics` | Volume trends, response times, sender frequency, timing patterns |
| `newsletters` | Subscription audit + unsubscribe plan |
| `labels` | Taxonomy analysis, merge/rename/delete recommendations |
| `search <goal>` | Natural language → Gmail search query |
| `senders` | VIP + noise identification |
| `digest` | Recent important email summary |
| `cleanup` | Archive candidates, duplicate detection, batch archiving |
| `audit` | Full inbox health report with score and action plan |
| _(empty)_ | Show this mode menu |

**Classification gate for ambiguous input:** If `$ARGUMENTS` could match multiple modes, ask which the user wants before proceeding.

---

## Hybrid Mode Protocol

**Read operations — execute immediately:**
- `gmail_search_emails`, `gmail_get_email`, `gmail_list_emails`
- `gmail_get_labels`, `gmail_get_filters`, `gmail_get_filter`

**Write operations — confirm before executing:**
- Single: `gmail_modify_email`, `gmail_delete_email`, `gmail_create_label`
- Batch: `gmail_batch_modify_emails`, `gmail_batch_delete_emails`
- Labels: `gmail_update_label`, `gmail_delete_label`, `gmail_get_or_create_label`
- Filters: `gmail_create_filter`, `gmail_create_filter_from_template`, `gmail_delete_filter`

**Confirmation format — always show before write ops:**
```
Action: {description}
Scope: {count} email(s) / label(s) / filter(s)
Reversible: {Yes | NO}
[Sample: first 3 subjects for batch ops]
```

Use `templates.md` for full confirmation and report formats.

---

## Phase 0: Discovery (Run First)

Before any workflow, establish context:

```
1. gmail_get_labels       → store label names + IDs
2. gmail_get_filters      → store existing filter criteria
3. gmail_search_emails    → query: "in:inbox" (maxResults: 20)
                            note unread count, top senders, label patterns
```

Use discovered label names throughout — never invent names that conflict with existing taxonomy.

---

## Mode: Triage

Categorize inbox using 4D+N. Reference: `triage-framework.md`.

```
1. Search: is:unread (maxResults: 50)
2. For each email: classify as DO / DELEGATE / DEFER / REFERENCE / NOISE
3. Collect IDs by category
4. Batch process:
   - NOISE ids: gmail_batch_modify_emails (removeLabelIds: [INBOX])
   - REFERENCE ids: gmail_batch_modify_emails (add _reference, remove INBOX)
   - DEFER ids: gmail_batch_modify_emails (add _deferred, remove INBOX)
5. Report with triage-summary template
6. Present DO items for user action
```

After triage: log session to inbox-zero progress file if running as part of daily routine.

---

## Mode: Inbox Zero

Structured habit system for achieving and maintaining inbox zero. Reference: `inbox-zero-system.md`.

### Daily Routine (5 min)

```
1. Search: is:unread newer_than:1d → identify P0/P1
2. Run quick triage pass (4D+N)
3. Batch archive NOISE + REFERENCE
4. Report: inbox count before → after
5. Update ~/.claude/email-whiz/inbox-zero-progress.json
   - achieved_zero: inbox_count == 0
   - increment streak if zero
```

### Weekly Review (15 min)

```
1. Clear deferred: label:_deferred older_than:7d
2. Filter effectiveness: inbox noise still arriving? → new filter candidates
3. Newsletter sweep: label:_reading/newsletters is:unread older_than:14d
4. Update weekly_reviews entry in progress file
```

**Bankruptcy detection:** If `is:unread` count > 500 or growing 3+ consecutive days, present recovery options (Daily Blitz / Staged Approach / Nuclear Reset). Always confirm before bulk archiving. See `inbox-zero-system.md` for full protocols.

**Progress report format:**
```
📊 Streak: {n} days | Best: {n} | Last zero: {date}
Inbox: {before} → {after}
```

---

## Mode: Filters

Pattern-detected filter suggestions. Reference: `filter-patterns.md`.

```
1. Search recent inbox (maxResults: 100, last 30d)
2. Cluster by sender domain + subject patterns
3. Check gmail_get_filters for existing coverage
4. Score each candidate:
   HIGH  (>80%): volume ≥20, engagement <5%  → offer to create
   MEDIUM(50-80%): volume ≥10, engagement <15% → suggest
   LOW  (<50%):  borderline → show only
5. Present with filter-suggestions template
6. On approval: gmail_create_filter or gmail_create_filter_from_template
```

Check for conflicts before creating: scan existing filter criteria for overlaps.

---

## Mode: Auto-Rules

Deep behavioral analysis → automated filter creation. Reference: `filter-patterns.md` § Auto-Rule Detection.

### Analysis Phase

```
1. Search: in:inbox after:{90d_ago} (maxResults: 500)
2. Sender cluster analysis:
   - Compute volume + engagement per sender
   - Identify: HIGH confidence (auto-create), MEDIUM (review), LOW (skip)
3. Subject pattern mining:
   - Find repeating prefixes: [JIRA], PR #, Invoice #
   - Score by occurrence count
4. Check conflict with existing filters
```

### Creation Phase

```
5. Present auto-rules report (see templates.md)
6. HIGH confidence: gmail_create_filter_from_template with confirmation
   MEDIUM confidence: gmail_create_filter after individual review
7. Schedule learning loop re-analysis after 2 weeks
```

---

## Mode: Analytics

Email communication metrics and trends. Reference: `analytics-guide.md`.

```
1. Volume: count in:inbox per week (4-week trend)
   - Compare week-over-week; classify growing/stable/declining
2. Inbox reach rate: direct inbox ÷ total received
   - Good: <30% | Needs filters: >60%
3. Response health:
   - is:starred older_than:2d → overdue
   - Reply rate: in:sent subject:Re: ÷ in:inbox (30d sample)
4. Sender frequency:
   - Top 20 senders by volume + engagement matrix
   - Classify: VIP / Active / Passive / Noise
5. Time-of-day: extract hour from date fields in sample
6. Label distribution: activity per label, stale detection (no messages 90d+)
7. Present full analytics report (see templates.md)
```

---

## Mode: Newsletters

Newsletter subscription audit + unsubscribe plan.

```
1. Search: list:* OR subject:(newsletter OR digest OR "weekly roundup")
2. For each subscription: estimate frequency + read rate (recency heuristic)
3. Classify: UNSUBSCRIBE (low read rate) / KEEP / FILTER (keep but skip inbox)
4. Present newsletter-audit report
5. On approval: open unsubscribe links (provide URL) or create filter
```

Reference: `workflows.md` § Unsubscribe Strategies.

---

## Mode: Labels

Label taxonomy analysis and cleanup.

```
1. gmail_get_labels → list all with counts
2. Find issues:
   - Duplicates/synonyms (e.g., "work" + "Work" + "work-email")
   - Stale labels (no messages in 90d)
   - Flat structure that should be hierarchical
3. Suggest: MERGE / RENAME / DELETE / RESTRUCTURE
4. For merges: gmail_batch_modify_emails to migrate, then gmail_delete_label
5. Use gmail_update_label for renames
6. Present label-analysis report
```

Reference: `workflows.md` § Label Hierarchy Best Practices.

---

## Mode: Search

Natural language → Gmail search query.

```
Input: user's goal in plain language
Output: optimized Gmail search query with explanation

Steps:
1. Parse intent: who / what / when / status
2. Map to operators: from:, subject:, after:, is:unread, label:, etc.
3. Add negations for common noise
4. Show query + explanation + expected matches
5. Offer to run the search
```

Reference: `filter-patterns.md` § Gmail Search Operators.

---

## Mode: Senders

VIP and noise sender identification.

```
1. Sample last 200 inbox emails
2. Compute per sender: volume + engagement + recency
3. VIP candidates: reply rate >50% OR consistently starred
4. Noise candidates: volume >10 AND engagement 0%
5. Present sender report with recommended actions
6. On approval: create VIP filter (always important) or noise filter
```

Reference: `triage-framework.md` § Sender Shortcuts, `workflows.md` § VIP Management.

---

## Mode: Digest

Recent important email summary.

```
1. Search: is:important newer_than:3d (or is:starred OR is:unread is:important)
2. For each: extract sender, subject, 1-line summary
3. Categorize: RESPOND / FYI / READING
4. Present digest report
5. Offer: "open N" | "archive fyi"
```

Reference: `templates.md` § Digest.

---

## Mode: Cleanup

Archive candidates and batch archiving.

```
1. Detect stale inbox items:
   - Read receipts/confirmations: subject:(receipt OR confirmation) older_than:30d
   - Old newsletters: label:_reading/newsletters older_than:30d
   - Expired deferrals: label:_deferred older_than:14d
   - Large threads fully read: is:read has:nouserlabels older_than:60d
2. Show batch-operation-confirmation with samples
3. On approval: gmail_batch_modify_emails (remove INBOX / add archive label)
4. Report: inbox count before → after
```

Never use `gmail_batch_delete_emails` in cleanup — archive only.
Reference: `workflows.md` § Batch Operations.

---

## Mode: Audit

Full inbox health report.

```
1. Run Phase 0 discovery (labels, filters, sample)
2. Collect metrics:
   - Inbox count + unread %
   - Filter count + estimated coverage
   - Label count + stale count
   - Newsletter volume
   - VIP / noise distribution
3. Score: 0-100 based on inbox reach rate, filter coverage, label health
4. Identify top 3 quick wins (high impact, low effort)
5. Generate week-by-week action plan
6. Present full-audit report
```

Reference: `analytics-guide.md`, `templates.md` § Full Audit.

---

## Error Handling

| Scenario | Response |
|----------|----------|
| MCP connection failure | Report error, provide manual Gmail URL as fallback |
| Rate limit (429) | Reduce batch size to 25, wait 60s, retry once |
| Message not found (404) | Skip and continue; note in report |
| Partial batch failure | Report succeeded/failed counts; suggest retry for failures |
| Label ID mismatch | Re-fetch labels via `gmail_get_labels` and remap |

---

## Scope Boundaries

**IS for:** Gmail triage, inbox zero habits, filter creation, auto-rules, email analytics, newsletter management, label organization, search queries, sender analysis, digest, cleanup, inbox health audit.

**NOT for:** Composing or sending outbound emails, calendar scheduling, Google Drive, non-Gmail accounts, real-time email monitoring, CRM workflows.

---

## Reference File Index

| File | Content | Load When |
|------|---------|-----------|
| `references/triage-framework.md` | 5D+N decision trees, sender/subject signals, batch processing | triage, inbox-zero |
| `references/filter-patterns.md` | Gmail operators, filter templates, auto-rule algorithms, learning loop | filters, auto-rules, search |
| `references/workflows.md` | Bankruptcy, VIP, batch ops, label hierarchy, unsubscribe, security | cleanup, labels, senders, newsletters |
| `references/templates.md` | All confirmation, report, and execution result templates | Every mode |
| `references/inbox-zero-system.md` | Daily/weekly routines, progress schema, bankruptcy recovery | inbox-zero |
| `references/analytics-guide.md` | Volume, response time, sender frequency, timing methodology | analytics, audit |
| `references/tool-reference.md` | All 19 Gmail MCP tool signatures, parameters, system limits | When selecting tools |

**Scripts:**

| Script | Purpose | Run When |
|--------|---------|----------|
| `scripts/inbox_snapshot.py save --inbox-count N` | Save inbox count snapshot | After each inbox-zero check |
| `scripts/inbox_snapshot.py trend --days 7` | Compute inbox trend (growing/stable/declining) | During analytics mode |
| `scripts/inbox_snapshot.py list --days 30` | List recent snapshots | When reviewing progress |

---

## Critical Rules

1. Run Phase 0 discovery before any workflow — never assume label/filter state
2. Confirm all write operations — show scope, count, and reversibility before calling
3. Batch similar operations — never loop `gmail_modify_email` when `gmail_batch_modify_emails` applies
4. Preserve existing taxonomy — suggest improvements, never silently rename
5. Check filter conflicts before creating — call `gmail_get_filters` first
6. Include confidence scores on all filter/rule suggestions
7. Provide rollback guidance for every bulk operation
8. Handle MCP failures gracefully — surface manual fallback steps
9. Surface unsubscribe links — make newsletter cleanup actionable
10. Prioritize quick wins — high impact, low effort first in all reports
11. Update inbox-zero progress after every routine — write streak data to `~/.claude/email-whiz/inbox-zero-progress.json`
12. Never use `gmail_batch_delete_emails` in cleanup mode — archive only; deletion requires explicit user intent
