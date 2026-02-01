---
name: app-audit
description: Analyzes installed Termux packages and Android apps to identify redundancies, categorize usage, and suggest cleanups. Use when the user asks to audit apps, check for bloatware, or analyze installed software.
---

# App Audit Protocol

## Goal
To provide a comprehensive analysis of the user's installed software environment, identifying redundant tools and grouping applications by function to help the user streamline their device.

## Workflow

### 1. Data Collection
First, gather the complete list of installed software from both the Termux environment and the Android system.

**Execute the following commands:**
1.  `pkg list-installed` (Termux packages)
2.  `python3 %SKILL_DIR%/scripts/get_app_labels.py` (Android apps with Friendly Names)

*Note: The Python script requires `aapt` to be installed. If it fails, check if `aapt` is present or fall back to `cmd package list packages -3`.*

### 2. Analysis Strategy
Once the lists are retrieved, analyze them using the following heuristics. Do NOT output the raw lists unless explicitly asked.

#### Categorization
Group apps into functional categories such as:
- **Development** (Compilers, Editors, Git)
- **Network & Admin** (SSH, VPN, Wifi Tools, Sync)
- **Communication** (Messengers, Email)
- **Media & Entertainment** (Music, Video, Games)
- **Productivity** (Tasks, Notes, Finance)
- **Physical World** (Weather, Maps, Fitness, Transport)

#### Redundancy Detection
Look for multiple apps serving the *exact same primary purpose*.
- **Common Overlaps:**
    - Multiple Weather apps (e.g., Windy vs. native vs. ad-heavy free apps).
    - Multiple Remote Desktop tools (TeamViewer vs. AnyDesk vs. RDP).
    - Multiple To-Do list managers.
    - Multiple Flight Trackers.
    - Termux tools overlapping with Android apps (e.g., `syncthing` in Termux vs Android App).

### 3. Reporting
Present the findings in a structured report:

1.  **Summary:** Total count of apps and packages.
2.  **Redundancy Alerts:** A high-priority section listing specifically identified redundancies with a recommendation (e.g., "Keep X, remove Y and Z").
3.  **Category Breakdown:** A concise grouping of the apps.
4.  **Cleanup Suggestions:** Specific `pkg uninstall` or `cmd package archive` commands for the identified redundant items.