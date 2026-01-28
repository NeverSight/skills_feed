---
name: learning-localization-engineering
description: Convert measurement systems, format dates/times/numbers/currency by locale, adapt address formats, and handle locale-specific sorting. Use when localizing technical content for regions. Activates on "localization", "date format", "measurement conversion", or "locale adaptation".
---

# Learning Localization Engineering

Handle technical localization of formats, measurements, and locale-specific conventions in educational content.

## When to Use

- Localizing technical content
- Converting measurement systems
- Formatting for regional conventions
- Adapting data presentations
- Regional number/date/time handling

## Localization Areas

### 1. Measurement Systems

**Conversions**:
- Metric ↔ Imperial ↔ US Customary
- Temperature (Celsius ↔ Fahrenheit ↔ Kelvin)
- Paper sizes (A4 ↔ Letter)
- Clothing sizes (EU ↔ US ↔ UK)

### 2. Date and Time Formats

**Regional Variations**:
- Date order: DD/MM/YYYY vs MM/DD/YYYY vs YYYY-MM-DD
- Time: 12-hour vs 24-hour
- Week start: Sunday vs Monday
- Calendar systems (Gregorian, Islamic, Hebrew, etc.)

### 3. Number Formatting

**Separators**:
- Decimal: . (US) vs , (EU)
- Thousands: , (US) vs . (EU) vs space (ISO)
- Negative numbers: -123 vs (123) vs 123-

### 4. Currency

**Formatting**:
- Symbol position: $100 vs 100$ vs 100 USD
- Decimal places by currency
- Exchange rate context

### 5. Address Formats

**Regional Structures**:
- US: Street, City, State ZIP
- UK: Street, Town, County, Postcode
- Japan: Prefecture, City, Block, Building
- Korea: Province, City, District, Street

## CLI Interface

```bash
/learning.localization-engineering --content "physics-course/" --source-locale "en-US" --target-locales "en-GB,fr-FR,ja-JP"
```

## Output

- Localized content with proper formats
- Measurement conversion log
- Locale-specific formatting rules
- Validation report

## Exit Codes

- **0**: Localization complete
- **1**: Unsupported locale
- **2**: Conversion ambiguities
