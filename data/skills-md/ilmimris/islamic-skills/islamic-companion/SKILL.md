---
name: islamic-companion
description: Unified Islamic utilities for prayer times, fasting schedules, and Zakat calculations using a shared configuration.
---

# Islamic Companion Skill

**Unified tool for prayer times, fasting schedules, and Zakat calculations.**

This skill consolidates Islamic utilities into a single CLI with shared configuration and efficient caching.

## Features

- **Prayer Times:** Retrieve daily prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha).
- **Fasting:** Check Imsak and Maghrib times for fasting.
- **Zakat:** Calculate Nisab thresholds for Gold and Silver based on current market prices.
- **Quran:** Search for verses by keyword or fetch specific Surah/Ayah with translation.
- **Calendar:** Generate a monthly prayer schedule for any city.
- **Quotes:** Fetch and display random Islamic quotes or setup daily automation.
- **Scheduler:** Generate OpenClaw cron commands to schedule daily prayer reminders.
- **Caching:** Minimizes API calls by caching daily results locally.

## Usage

Run the CLI using the bash script:

```bash
# Get today's prayer times for Jakarta (explicit timezone override)
./bin/islamic-companion prayer --today --lat -6.2088 --long 106.8456 --tz Asia/Jakarta

# Setup daily quote automation for specific location
./bin/islamic-companion prayer --sync --lat -6.2088 --long 106.8456 --timezone Asia/Jakarta

# Get a random quote
./bin/islamic-companion quotes --random

# Get monthly calendar (Example: Serang, Banten)
./bin/islamic-companion calendar --city "Serang" --month 2 --year 2026

# Sync prayer schedule to cron (generates commands)
./bin/islamic-companion prayer --sync

# Check fasting times (Imsak/Maghrib)
./bin/islamic-companion fasting --today --lat -6.2088 --long 106.8456

# Check Zakat Nisab values
./bin/islamic-companion zakat --nisab

# Search Quran for keyword
./bin/islamic-companion quran --search "sabar"

# Get specific Surah (e.g., Al-Fatihah)
./bin/islamic-companion quran --surah 1

# Get specific Ayah (e.g., Al-Baqarah:255)
./bin/islamic-companion quran --surah 2 --ayah 255
```

## Configuration

Edit `config.json` to set your calculation method and Zakat preferences. Location is now provided on-the-fly via CLI arguments. The system defaults to **UTC** if no timezone is specified.

```json
{
  "calculation": {
    "method": 20,
    "school": 0
  },
  "zakat": {
    "currency": "IDR",
    "gold_gram_threshold": 85,
    "api_key": ""
  },
  "timezone": "Asia/Jakarta",
  "quran_language": "id"
}
```

### Calculation Methods
- **Method 20:** Kemenag RI (Indonesia)
- **School 0:** Standard (Shafi, Maliki, Hanbali)
- **School 1:** Hanafi

| User Intent | Command Executed |
| :--- | :--- |
| "Get prayer times" | `./bin/islamic-companion prayer --today --lat [LAT] --long [LONG]` |
| "Show me the calendar for [City]" | `./bin/islamic-companion calendar --city [City]` |
| "Setup daily Islamic quotes" | `./bin/islamic-companion quotes --setup` |
| "Give me a random Islamic quote" | `./bin/islamic-companion quotes --random` |
| "Sync prayer schedule" | `./bin/islamic-companion prayer --sync` |
| "When is Imsak?" | `./bin/islamic-companion fasting --today` |
| "Check Zakat Nisab" | `./bin/islamic-companion zakat --nisab` |
| "Search Quran for [keyword]" | `./bin/islamic-companion quran --search "[keyword]"` |
| "Read Surah [Name/Number]" | `./bin/islamic-companion quran --surah [Number]` |
| "Read Surah [Number] Ayah [Number]" | `./bin/islamic-companion quran --surah [Number] --ayah [Number]` |

## Dependencies

- **System:** `bash`, `curl`, `jq` (highly recommended)
- **Python (Optional for some features):** `python3`, `requests` (Install via `pip install -r requirements.txt`)

## Security & Privacy

> [!WARNING]
> **API Keys**: The Zakat feature uses an API key. You can store it in `config.json` (less secure) or export it as an environment variable `ZAKAT_API_KEY` (recommended).

> [!IMPORTANT]
> **Automation**: The `--sync` and `--setup` commands generate cron schedules. Always review the output before adding it to your system crontab.

## Installation

1. Clone the repository or download the skill.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `curl` is installed. `jq` is recommended for JSON parsing speed and reliability.

Run the CLI using the bash script wrapper, which handles configuration loading and environment setup. Location must be provided on-the-fly:

```bash
# Get today's prayer times (uses HTTPS)
./bin/islamic-companion prayer --today --lat -6.2088 --long 106.8456
```
