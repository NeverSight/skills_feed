# Ads Optimizer v2

Гибридный skill для ежедневной оптимизации рекламных аккаунтов Facebook/Instagram.

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Ads Optimizer v2                         │
├─────────────────────────────────────────────────────────────┤
│  [1] Account Selection                                      │
│      ↓                                                      │
│  [2] Data Collection (MCP Tools)                            │
│      ├── get_campaigns, get_adsets, get_ads                │
│      ├── get_insights × 5 periods                          │
│      └── Parse briefs, creatives.md, history               │
│      ↓                                                      │
│  [3] Analysis (Python modules for formulas)                 │
│      ├── Health Scorer (5 components)                       │
│      ├── Creative Analyzer (Risk Score + Ad-Eaters)         │
│      └── Output: structured data                            │
│      ↓                                                      │
│  [4] Decision Maker                                         │
│      ├── Apply Action Matrix                                │
│      ├── Check History Rules                                │
│      └── Balance Budgets                                    │
│      ↓                                                      │
│  [5] Execution + Logging (MCP Tools)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Шаг 1: Выбор аккаунта

Прочитай список аккаунтов из `.claude/ads-agent/config/ad_accounts.md`.

Если пользователь не указал аккаунт:
```
Какой аккаунт оптимизировать?
1. Бас дент (act_805414428109857)
2. Usmile (act_703077431339797)
3. Другой аккаунт
```

---

## Шаг 2: Сбор данных

### 2.1 Локальные файлы

Прочитай:
1. **Бриф:** `.claude/ads-agent/config/briefs/{account_name}.md`
   - Извлеки: направления, campaign_id, target_cpl, daily_budget

2. **Креативы:** `.claude/ads-agent/config/creatives.md`
   - Извлеки: теги по направлениям, статусы

3. **История:** `.claude/ads-agent/history/{YYYY-MM}/{YYYY-MM-DD}.md` (за 3 дня)
   - Извлеки: действия по adsets (increased, decreased, paused)

### 2.2 MCP API

Выполни запросы:

```
# Кампании
mcp__meta-ads__get_campaigns(account_id="{account_id}", status_filter="ACTIVE")

# Adsets
mcp__meta-ads__get_adsets(account_id="{account_id}", limit=100)

# Ads
mcp__meta-ads__get_ads(account_id="{account_id}", limit=100)

# Insights за 5 периодов
mcp__meta-ads__get_insights(object_id="{account_id}", time_range="today", level="adset")
mcp__meta-ads__get_insights(object_id="{account_id}", time_range="yesterday", level="adset")
mcp__meta-ads__get_insights(object_id="{account_id}", time_range="last_3d", level="adset")
mcp__meta-ads__get_insights(object_id="{account_id}", time_range="last_7d", level="adset")

# Ad-level insights для ad-eaters
mcp__meta-ads__get_insights(object_id="{account_id}", time_range="last_7d", level="ad")
```

### 2.3 Извлечение leads

Из `actions` в insights извлекай leads:
```
action_type = "lead" или "onsite_conversion.lead_grouped" или "offsite_conversion.fb_pixel_lead"
leads = int(action.value)
```

---

## Шаг 3: Расчёт Health Score

Для каждого adset вычисли Health Score по формуле:

```
HS = round((CPL_Gap + Trends + Diagnostics + Today_Adj) × Volume_Factor)
```

### 3.1 CPL Gap (±45)

```
ratio = CPL_yesterday / target_cpl

ratio ≤ 0.5  → +45
ratio = 0.7  → +30
ratio = 1.0  → 0
ratio = 1.5  → -30
ratio ≥ 2.0  → -45

Линейная интерполяция между точками.
```

### 3.2 Trends (±15)

```
trend_pct = (CPL_3d - CPL_7d) / CPL_7d × 100

trend ≤ -20%  → +15 (улучшение)
trend = 0%    → 0
trend ≥ +20%  → -15 (ухудшение)
```

### 3.3 Diagnostics (до -30)

```
CTR < 1%           → -8
CPM > median × 1.3 → -12
Frequency > 2      → -10
```

### 3.4 Today Adjustment (+0..+30)

Если impressions_today ≥ 500:
```
improvement = (CPL_yesterday - CPL_today) / CPL_yesterday × 100
improvement ≥ 30% → +30
improvement = 0%  → 0
```

### 3.5 Volume Factor (0.6..1.0)

```
impressions < 500   → 0.6
impressions < 1000  → 0.7
impressions < 2000  → 0.8
impressions < 5000  → 0.9
impressions ≥ 5000  → 1.0
```

### 3.6 Классификация

```
HS ≥ +25  → very_good
+5 ≤ HS   → good
-5 ≤ HS   → neutral
-25 ≤ HS  → slightly_bad
HS < -25  → bad
```

---

## Шаг 4: Анализ креативов

### 4.1 Risk Score (0-100)

Группируй ads по creative_tag, вычисли для каждого:

```
Risk Score = CPL_Component + Trend_Component + Volume_Component + Consistency_Bonus

CPL_Component (0-40):
  ratio ≤ 1.0 → 0
  ratio = 1.5 → 20
  ratio = 2.0 → 35
  ratio ≥ 3.0 → 40
  no leads   → 25

Trend_Component (0-20):
  improving ≥10% → 0
  stable         → 5
  declining ≤20% → 15
  declining >20% → 20

Volume_Component (0-20):
  spend ≥ 2× min  → 0
  spend ≥ min     → 10
  spend ≥ 0.5×min → 15
  spend < 0.5×min → 20

Consistency_Bonus (-20 to 0):
  variance ≤10% → -20
  variance ≤20% → -10
  variance ≤30% → -5
  variance >30% → 0
```

Risk Levels:
- Low (0-25) → scale
- Medium (26-50) → monitor
- High (51-75) → reduce
- Critical (76-100) → pause

### 4.2 Ad-Eaters Detection

```
CRITICAL: CPL > 3× target → немедленная пауза
HIGH: 0 leads + spend ≥ 2× avg → пауза сегодня
MEDIUM: CPL > 1.5× target + spend_share > 50% → снижение
```

---

## Шаг 5: Decision Maker

### 5.1 Матрица действий по HS

| HS Класс | Действие |
|----------|----------|
| very_good (≥ +25) | +10% to +30% |
| good (+5..+24) | +0% to +10% |
| neutral (-5..+4) | мониторинг |
| slightly_bad (-25..-6) | -20% to -40% |
| bad (≤ -26) | -50% или пауза |

### 5.2 Правила истории

| Флаг | Действие |
|------|----------|
| `is_new` (< 48h) | Не трогать (кроме CPL > 3×) |
| `was_decreased_yesterday` | Не снижать сегодня |
| `was_increased_yesterday` | Не снижать сегодня |
| `consecutive_decreases ≥ 3` | Пауза |

### 5.3 Ad-Eaters

| Priority | will_adset_be_empty | Действие |
|----------|---------------------|----------|
| CRITICAL | false | pause_ad |
| CRITICAL | true + HS ≤ -25 | pause_adset |
| CRITICAL | true + HS > -25 | warning only |
| HIGH | - | pause_ad |
| MEDIUM | - | reduce or pause |

### 5.4 Бюджетный баланс

Для каждого направления проверь коридор 95-105%:
```
budget_ratio = sum(adset_budgets) / plan_budget × 100%
```

**Underspend (< 95%):**
1. Увеличь best performer (very_good/good HS)
2. Или создай новый adset с unused_creative

**Overspend (> 105%):**
1. Снизь worst performers первыми

---

## Шаг 6: Формирование ActionPlan

Выведи таблицу:

```markdown
## ActionPlan для {account_name}

### Направление: {direction_name}
Budget: ${budget_fact}/${budget_plan} ({ratio}%)

| Adset | HS | Action | Budget Change | Reason |
|-------|-----|--------|---------------|--------|
| Set 1 | +40 (very_good) | increase | $37.50 → $45.00 (+20%) | CPL $2.51 < target |
| Set 2 | -30 (bad) | decrease | $25.00 → $12.50 (-50%) | CPL $8.50 > 2× target |

### Ad-Eaters
| Ad | Adset | Priority | Action | Reason |
|----|-------|----------|--------|--------|
| promo_cold | Brain bm35 | CRITICAL | pause | CPL > 3× target |

### Budget Summary
| Direction | Plan | Before | After | Change |
|-----------|------|--------|-------|--------|
| Имплантация | $100 | $98.50 | $102.50 | +$4.00 |
```

---

## Шаг 7: Execution

После подтверждения выполни через MCP:

### Изменение бюджета
```
mcp__meta-ads__update_adset(adset_id="{id}", daily_budget={cents})
```

### Пауза adset
```
mcp__meta-ads__pause_adset(adset_id="{id}")
```

### Пауза ad
```
mcp__meta-ads__pause_ad(ad_id="{id}")
```

---

## Шаг 8: Логирование

Запиши в `.claude/ads-agent/history/{YYYY-MM}/{YYYY-MM-DD}.md`:

```markdown
# Optimization Log: {date}

## Account: {account_name}

### Summary
- Total actions: {count}
- Budget changes: {increases}↑ {decreases}↓
- Paused: {paused_count}

### Actions

#### Adset: {name} ({id})
- Direction: {direction}
- Action: {action}
- Budget: ${old} → ${new}
- HS: {hs} ({hs_class})
- CPL: ${cpl} (target: ${target})
- Reason: {reason}
```

---

## Quick Reference

### Health Score формула
```
HS = round((CPL_Gap + Trends + Diagnostics + Today_Adj) × Volume_Factor)
```

### Risk Score уровни
| Level | Score | Action |
|-------|-------|--------|
| Low | 0-25 | scale |
| Medium | 26-50 | monitor |
| High | 51-75 | reduce |
| Critical | 76-100 | pause |

### MCP Tools
- `get_campaigns` — список кампаний
- `get_adsets` — список adsets
- `get_ads` — список объявлений
- `get_insights` — статистика за период
- `update_adset` — изменение бюджета
- `pause_adset` / `pause_ad` — пауза
